// Runs a workflow script (research_topic.js / distribute_topic.js) UNCHANGED,
// supplying the tiny API it was written against — agent(), parallel(),
// pipeline(), phase(), log(), args, budget — over a JSON-lines RPC to the
// Python harness on stdin/stdout. The harness answers every agent() call by
// running headless Claude Code on the subscription, journals it, and handles
// usage limits. This file has no other job.
//
//   node bridge.mjs <script.js> <args.json>
import fs from "node:fs";
import readline from "node:readline";

const [, , scriptPath, argsPath] = process.argv;
const args = JSON.parse(fs.readFileSync(argsPath, "utf8"));

let nextId = 1;
const pending = new Map();
const send = (msg) => process.stdout.write(JSON.stringify(msg) + "\n");

readline.createInterface({ input: process.stdin }).on("line", (line) => {
  if (!line.trim()) return;
  const m = JSON.parse(line);
  const p = pending.get(m.id);
  if (!p) return;
  pending.delete(m.id);
  p.resolve(m.result ?? null); // Workflow semantics: a failed agent resolves to null
});

function agent(prompt, opts = {}) {
  return new Promise((resolve) => {
    const id = nextId++;
    pending.set(id, { resolve });
    send({ id, type: "agent", prompt, opts });
  });
}
// parallel(): barrier; a thunk that throws resolves to null, never rejects.
async function parallel(thunks) {
  return Promise.all(thunks.map((t) => Promise.resolve().then(t).catch(() => null)));
}
// pipeline(): each item through every stage independently; a throw drops the item to null.
async function pipeline(items, ...stages) {
  return Promise.all(
    items.map(async (item, i) => {
      let v = item;
      try {
        for (const s of stages) v = await s(v, item, i);
        return v;
      } catch {
        return null;
      }
    }),
  );
}
const phase = (title) => send({ type: "phase", title });
const log = (message) => send({ type: "log", message });
const budget = { total: null, spent: () => 0, remaining: () => Infinity };

// Load the script body: keep `meta` as a plain const, run the rest as the body
// of one async function so top-level `await` and `return` behave as they do
// under the Workflow tool.
const src = fs.readFileSync(scriptPath, "utf8").replace(/^export const meta/m, "const meta");
const AsyncFunction = Object.getPrototypeOf(async function () {}).constructor;
const run = new AsyncFunction("agent", "parallel", "pipeline", "phase", "log", "args", "budget", src);

// Exit only after the final line has been flushed: process.exit() right after a
// pipe write truncates a large result mid-line (seen at 61KB of a 200KB result).
const finish = (msg, code) => process.stdout.write(JSON.stringify(msg) + "\n", () => process.exit(code));
run(agent, parallel, pipeline, phase, log, args, budget)
  .then((result) => finish({ type: "result", result }, 0))
  .catch((e) => finish({ type: "error", error: String(e && e.stack ? e.stack : e) }, 1));
