# Ideya

**Ideya is an atlas of humanity's hardest debates** — existential risk, governance, economics, ethics. Each topic lays out the shared facts, the strongest case for every position, and the crux where the disagreement actually lives, so you can find where you stand, and why.

The site: https://ideya1.org · Part of the [Ideya-AI](https://github.com/Ideya-AI) project set.

## What it is

A visual wiki between an encyclopedia and a debate platform. Every topic is one structured page on the same six-section spine — learn it once, navigate them all:

- **Overview** — what the topic covers, what it deliberately excludes, and why it matters now.
- **Basics** — the decision-relevant facts nearly every position accepts, each verified against a real source and dated. Visual comparisons appear only where they're true: a bar means a real share of a named whole.
- **Questions** — what's actually contested, split into empirical questions (evidence could settle them) and value questions (evidence can't).
- **Positions** — every genuine camp, each given its strongest case in its own voice, at its real prevalence. Not strawmen, not balance theatre.
- **Crux** — the editorial narrowing to where disagreement actually sits, with the split: how it resolves if it's empirical, and what's really being weighed if it's values.
- **Actions** — vetted paths into the topic across the landscape, with comparable coverage for every camp.

Every page reads at the depth you have time for: glance at the shape of a debate, or go deep into sourced numbers and named proponents.

## Why this exists — in a world with AI

Text is now effectively free. Takes, summaries, and confident verdicts can be generated in unlimited volume, and most of that volume compresses hard questions into answers. What gets scarcer as generation gets cheaper is the opposite artifact: a curated, accountable map that says *here is what's known, here is who disagrees, here is precisely where and why* — with a named human responsible for every word.

Ideya is built on that inversion. AI does the labor it's genuinely good at — deep research, drafting each position's strongest case, adversarially checking claims against sources — inside a pipeline with hard gates for neutrality, steelmanning, and fact-sourcing. Nothing publishes without a human editor approving it. The bet is that this is the honest division of labor for the AI era: machine depth, human accountability.

It matters in the other direction too. As more reading and summarizing is delegated to AI systems, the material those systems draw on shapes what people end up believing. A neutral, sourced, structurally honest map of a debate is the input that degrades least — useful to a person at a glance and to a machine as ground truth.

## Why this exists — in a fractured political world

Most coverage flattens hard issues into verdicts or drowns them in takes, and feed algorithms reward meeting the other side at its weakest. The result isn't disagreement — disagreement is healthy — it's disagreement *about a cartoon*.

Ideya takes no side. Its editorial rules are the product:

- **Genuine steelman.** Every position gets its strongest case, in its own voice, such that a real proponent would endorse it. You can't honestly disagree with an argument you've only met at its weakest.
- **Honest non-balance.** Every genuine position is included and none is forced into a fake 50/50. Asymmetry between camps is carried by the shared facts, each position's real prevalence, and the crux — never by a house verdict.
- **The crux move.** Naming whether a disagreement is ultimately empirical or ultimately about values changes what arguing should even look like. Empirical cruxes can name the evidence that would settle them; value cruxes can at least name what's being weighed. Either is progress over a shouting match.

The goal is not agreement. It's that two people who disagree can point at the same map and say "here — this is the part we differ on."

## How it's made

Content moves through a staged pipeline: research that maps every camp and checks every hard claim against a fetched source, a separate writing stage that rewords but never changes facts, rendering and review, and a packet a human editor approves before anything publishes. Every statistic carries its source and two dates — when the data is from, and when it was verified. Each topic lives as one reviewable directory under `research/topics/`, from first title to published page.

Reader participation is anonymous by design (no accounts): votes, leans, and written responses feed back into the maps behind reveal gates, so small early samples never masquerade as consensus. Curation leads; participation refines.

## About this repo

This repository is public for clarity of intentions — so the editorial rules, the pipeline, and the sourcing behind every published claim are inspectable. It is not packaged as a turnkey product, and self-hosting it is not a supported path.

Stack: Django + HTMX + Alpine, token-native CSS, SQLite.

- `ideya/`, `topics/`, `templates/`, `static/` — the web app: settings, the content models and views, the management commands that load, render, and check content, and the product surface (design tokens in `static/css/tokens.css`).
- `accounts/` — the email-keyed user model that participation rows and the admin point at. No public entry points.
- `research/topics/<slug>/` — the set of topics, one directory each, cradle to grave. `topic.json` is the source of truth for everything except participation. `categories.json` is the taxonomy.
- `research/pipeline/` — the authoring pipeline: `PIPELINE.md` (the design).
- `docs/` — `DESIGN.md` (the locked design system), `DEPLOY.md` (how the site goes live), `PARTICIPATION.md` (reading what readers did).
