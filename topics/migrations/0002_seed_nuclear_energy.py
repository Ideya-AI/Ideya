from django.db import migrations

L1_PLACEHOLDER = """
<div class="space-y-8">
  <p class="text-sm uppercase tracking-wide text-ink-400">The core question</p>
  <p class="text-2xl font-medium leading-snug">
    Should nuclear power be a major part of the world's energy mix?
  </p>

  <div class="grid gap-4 sm:grid-cols-3">
    <div class="rounded-xl border border-ink-100 p-4">
      <div class="text-xs uppercase tracking-wide text-ink-400">Deaths per TWh</div>
      <div class="mt-2 text-2xl font-semibold">0.03</div>
      <p class="mt-1 text-xs text-ink-600">
        Nuclear — among the lowest of any energy source, alongside wind and solar.
      </p>
    </div>
    <div class="rounded-xl border border-ink-100 p-4">
      <div class="text-xs uppercase tracking-wide text-ink-400">Capacity factor</div>
      <div class="mt-2 text-2xl font-semibold">~92%</div>
      <p class="mt-1 text-xs text-ink-600">
        Time spent producing at full power — higher than any other source.
      </p>
    </div>
    <div class="rounded-xl border border-ink-100 p-4">
      <div class="text-xs uppercase tracking-wide text-ink-400">CO2 g per kWh</div>
      <div class="mt-2 text-2xl font-semibold">~12</div>
      <p class="mt-1 text-xs text-ink-600">
        Lifecycle carbon — comparable to wind, well below gas (~490) or coal (~820).
      </p>
    </div>
  </div>

  <div>
    <p class="text-sm uppercase tracking-wide text-ink-400">Where people stand</p>
    <ul class="mt-3 space-y-2 text-sm">
      <li class="rounded-lg bg-ink-100 px-3 py-2">
        <span class="font-medium">Climate pragmatists</span> — favor nuclear as the only proven, scalable, dispatchable low-carbon source.
      </li>
      <li class="rounded-lg bg-ink-100 px-3 py-2">
        <span class="font-medium">Traditional environmentalists</span> — wary of waste, accident risk, and proliferation; prefer renewables-only.
      </li>
      <li class="rounded-lg bg-ink-100 px-3 py-2">
        <span class="font-medium">New-nuclear advocates</span> — bet on SMRs and advanced reactors to fix cost and safety concerns.
      </li>
      <li class="rounded-lg bg-ink-100 px-3 py-2">
        <span class="font-medium">Cost skeptics</span> — argue nuclear has lost the economic race regardless of safety merits.
      </li>
    </ul>
  </div>

  <p class="text-xs text-ink-400">
    Placeholder L1. Real infographic with charts, deaths-per-TWh visual, and cost curves goes here.
  </p>
</div>
"""


L2_PLACEHOLDER = """
<h2>The question, sharpened</h2>
<p>
  Nuclear power is the most polarizing low-carbon energy source. The disagreement
  splits across at least four genuine positions — and most of the heat comes from
  conflating empirical claims (safety, cost, waste) with value claims (acceptable
  risk, intergenerational obligation, technology trust).
</p>

<h2>Where empirical questions end and value questions begin</h2>
<p>
  Empirically, the safety record is settled in a way that surprises many readers:
  nuclear has the lowest deaths-per-TWh of any energy source except wind and
  solar, including when major accidents are amortized. The contested empirical
  questions are about <em>cost trajectory</em> and <em>build timelines</em>,
  where the data are harder to read and trend differs sharply between national
  contexts (France vs. the US vs. South Korea vs. China).
</p>
<p>
  The value questions — what risks society should accept, how to weigh
  catastrophic-but-rare events against routine harms, what we owe future
  generations on waste storage — are where genuine moral disagreement lives.
</p>

<h2>Positions and their best arguments</h2>
<p><em>Placeholder L2. Each position gets a proper steelman, with citations.</em></p>

<h2>Open questions</h2>
<ul>
  <li>Why have costs diverged so much between countries with similar technology?</li>
  <li>How should small modular reactors (SMRs) change the analysis?</li>
  <li>What's the right framework for comparing waste storage across millennia to direct climate harm?</li>
</ul>
"""


L3_PLACEHOLDER = """
<p class="text-ink-600">
  A curated path for going deeper. Read in roughly this order — each step
  assumes the previous one.
</p>

<ol class="mt-6 space-y-6">
  <li>
    <div class="text-xs uppercase tracking-wide text-ink-400">1 — Get the numbers right</div>
    <a class="block mt-1 font-medium hover:text-ink-600"
       href="https://ourworldindata.org/safest-sources-of-energy" target="_blank" rel="noopener">
      Our World in Data — What are the safest and cleanest sources of energy?
    </a>
    <p class="mt-1 text-sm text-ink-600">
      The deaths-per-TWh framing in one chart. Start here.
    </p>
  </li>
  <li>
    <div class="text-xs uppercase tracking-wide text-ink-400">2 — Understand the cost question</div>
    <a class="block mt-1 font-medium hover:text-ink-600"
       href="https://energy.mit.edu/research/future-of-nuclear-energy-in-a-carbon-constrained-world/" target="_blank" rel="noopener">
      MIT — The Future of Nuclear Energy in a Carbon-Constrained World
    </a>
    <p class="mt-1 text-sm text-ink-600">
      Why nuclear costs diverge across countries, and what would have to change for new builds to be economic.
    </p>
  </li>
  <li>
    <div class="text-xs uppercase tracking-wide text-ink-400">3 — Hear the critique on its own terms</div>
    <p class="mt-1 font-medium">[Curated source goes here]</p>
    <p class="mt-1 text-sm text-ink-600">
      A strong-form anti-nuclear argument from someone who has done the math, not a vibe.
    </p>
  </li>
</ol>

<p class="mt-8 text-xs text-ink-400">
  Placeholder L3. Real version will have 6–10 ordered resources with substantive annotations.
</p>
"""


def seed(apps, schema_editor):
    Topic = apps.get_model("topics", "Topic")
    Topic.objects.update_or_create(
        slug="nuclear-energy",
        defaults={
            "title": "Nuclear Energy",
            "summary": (
                "Should nuclear power be a major part of the world's energy mix? "
                "The disagreement is scrambled — climate pragmatists, traditional "
                "environmentalists, new-nuclear advocates, and cost skeptics all argue past each other."
            ),
            "l1_content": L1_PLACEHOLDER,
            "l2_content": L2_PLACEHOLDER,
            "l3_content": L3_PLACEHOLDER,
        },
    )


def unseed(apps, schema_editor):
    Topic = apps.get_model("topics", "Topic")
    Topic.objects.filter(slug="nuclear-energy").delete()


class Migration(migrations.Migration):
    dependencies = [
        ("topics", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
