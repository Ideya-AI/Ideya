"""Seed the canonical Nuclear Energy topic (the design fixture) + categories and
stub topics that populate the discovery tiers (Home directory, Category, Search)."""

from django.db import migrations

CATEGORIES = [
    (
        "Energy & Environment",
        "energy",
        "leaf",
        "energy",
        "How we power civilization without wrecking the climate — and the trade-offs between every option.",
    ),
    (
        "AI & Technology",
        "ai-technology",
        "cpu",
        "tech",
        "The promise and peril of systems that increasingly decide, create, and act.",
    ),
    (
        "Political & Governance",
        "governance",
        "bank",
        "gov",
        "How societies decide, distribute power, and hold it accountable.",
    ),
    (
        "Economic & Social",
        "economy-society",
        "chart-line-up",
        "econ",
        "Markets, money, work, and the social fabric they shape.",
    ),
    (
        "Ethics & Philosophy",
        "ethics",
        "scales",
        "ethics",
        "What we owe each other, and how to live well under deep uncertainty.",
    ),
    (
        "Existential & Global Risk",
        "existential-risk",
        "warning-diamond",
        "risk",
        "The low-probability, civilization-scale threats that could end the story.",
    ),
]

# (slug_a, slug_b) sibling links.
CAT_LINKS = [
    ("energy", "ai-technology"),
    ("energy", "existential-risk"),
    ("energy", "economy-society"),
    ("ai-technology", "existential-risk"),
    ("ai-technology", "governance"),
    ("ethics", "ai-technology"),
]

# Stub topics: (title, slug, icon, summary, [category slugs])
STUBS = [
    (
        "Solar Power",
        "solar-power",
        "sun",
        "Photovoltaics on a relentless cost-decline curve — abundant but weather-dependent and land-hungry.",
        ["energy"],
    ),
    (
        "Grid Storage",
        "grid-storage",
        "battery-charging",
        "Batteries, pumped hydro and the firming problem that decides how far renewables can go.",
        ["energy"],
    ),
    (
        "AI Existential Risk",
        "ai-existential-risk",
        "brain",
        "Whether advanced AI poses a catastrophic, civilization-scale threat — and how near it might be.",
        ["existential-risk", "ai-technology"],
    ),
    (
        "Carbon Pricing",
        "carbon-pricing",
        "currency-circle-dollar",
        "Taxing emissions vs. cap-and-trade — the cleanest economic lever, and why it keeps stalling.",
        ["economy-society", "energy"],
    ),
    (
        "Geoengineering",
        "geoengineering",
        "thermometer-hot",
        "Deliberately cooling the planet — an emergency brake, or a moral hazard with global side effects.",
        ["energy", "existential-risk"],
    ),
    (
        "Universal Basic Income",
        "universal-basic-income",
        "hand-coins",
        "An unconditional income floor — freedom and simplicity, or unaffordable and work-eroding.",
        ["economy-society", "governance"],
    ),
    (
        "Gene Editing",
        "gene-editing",
        "dna",
        "Rewriting the human genome — curing disease versus designing people.",
        ["ethics", "ai-technology"],
    ),
    (
        "Lab-Grown Meat",
        "lab-grown-meat",
        "cow",
        "Cultivated meat without the animal — a climate and welfare win, if it can ever scale.",
        ["ethics", "economy-society"],
    ),
]

STATS = [
    dict(
        order=10,
        viz="ranked",
        wide=True,
        label="Deaths per TWh · lifecycle",
        series=[
            {"label": "Coal", "value": "24.6", "pct": 100, "highlight": False},
            {"label": "Gas", "value": "2.8", "pct": 11, "highlight": False},
            {"label": "Nuclear", "value": "0.03", "pct": 3, "highlight": True},
            {"label": "Solar", "value": "0.03", "pct": 3, "highlight": False},
        ],
        note="Among the safest sources — including Chernobyl and Fukushima.",
        source_url="https://ourworldindata.org/safest-sources-of-energy",
        source_label="ourworldindata.org",
        reveal="condensed",
    ),
    dict(
        order=20,
        viz="bar",
        label="Share of global power",
        value="9",
        unit="%",
        fill_pct=9,
        note="Down from a ~17% peak in 1996.",
        reveal="condensed",
    ),
    dict(
        order=30,
        viz="radial",
        label="Capacity factor",
        value="92",
        unit="%",
        fill_pct=92,
        note="Highest of any source — runs around the clock.",
        reveal="condensed",
    ),
    dict(
        order=40,
        viz="range",
        label="Lifecycle CO₂ · g/kWh",
        value="12",
        unit=" g",
        range_min="clean",
        range_max="gas ~490",
        range_at=5,
        note="Among the lowest of any source.",
        source_label="IPCC AR5",
        reveal="normal",
    ),
    dict(
        order=50,
        viz="bar",
        label="Build cost · West vs Korea",
        value="~4",
        unit="×",
        fill_pct=25,
        note="Korea builds at ~¼ the Western per-kW cost.",
        reveal="normal",
    ),
    dict(
        order=60,
        viz="bar",
        label="High-level waste, all-time",
        value="~400",
        unit="kt",
        fill_pct=18,
        note="Would cover one football field a few metres deep.",
        reveal="normal",
    ),
]

QUESTIONS = [
    dict(
        order=10,
        kind="empirical",
        votes=142,
        reveal="condensed",
        text="Are runaway Western nuclear costs fixable, or structural?",
        why="South Korea builds at ~¼ the per-kW cost of recent Western projects. If costs reflect lost supply chains, reform could restore them — if democratic safety preferences, no reform will.",
        lean_label_a="Fixable",
        lean_label_b="Structural",
        lean_pct_a=61,
    ),
    dict(
        order=20,
        kind="value",
        votes=98,
        reveal="condensed",
        text="Is the waste problem solved in principle, but unsolved in practice?",
        why="Deep geological disposal is settled science; Finland's Onkalo is operating. Yet most countries have no sited repository — the gap is political siting, not engineering.",
        lean_label_a="Solved",
        lean_label_b="Not in practice",
        lean_pct_a=43,
    ),
    dict(
        order=30,
        kind="empirical",
        votes=64,
        reveal="normal",
        text="Can new nuclear deploy fast enough to matter for 2050?",
        why="Even optimistic build rates add capacity slowly versus solar's exponential growth. Critics say the money decarbonizes more elsewhere; advocates say firm power is needed regardless.",
    ),
]

POSITIONS = [
    dict(
        key="pragmatist",
        order=10,
        name="Climate Pragmatist",
        color_key="green",
        importance=88,
        steelman="The only proven, scaled, firm low-carbon source we have.",
        description="Nuclear is the only dispatchable zero-carbon power at scale. IPCC 1.5 °C pathways lean on expanding it; Germany's phase-out raised emissions.",
        representative_name="James Hansen",
        representative_note="climate scientist who broke with much of the green movement to back nuclear.",
        proponents="James Hansen, Stewart Brand, Clean Air Task Force",
    ),
    dict(
        key="cost-skeptic",
        order=20,
        name="Cost Skeptic",
        color_key="amber",
        importance=74,
        steelman="Too slow and costly to be the rational marginal climate dollar.",
        description="Vogtle and Hinkley ran years late and billions over. Solar, wind and storage keep cheapening on a learning curve nuclear has never shown.",
        representative_name="Amory Lovins",
        representative_note="physicist and advocate of the efficiency-and-renewables path.",
        proponents="Amory Lovins, BNEF analysts, Mark Z. Jacobson",
    ),
    dict(
        key="advocate",
        order=30,
        name="New-Nuclear Advocate",
        color_key="blue",
        importance=61,
        steelman="Advanced reactors and serial builds can fix the cost problem.",
        description="SMRs and Gen-IV trade gigawatt megaprojects for factory-built units. Korea and France prove learning-by-building drives costs down.",
        representative_name="TerraPower",
        representative_note="Gen-IV developer betting on factory-built reactors.",
        proponents="TerraPower, NuScale, DOE",
    ),
    dict(
        key="risk-first",
        order=40,
        name="Risk-First Skeptic",
        color_key="rust",
        importance=52,
        steelman="Catastrophic, intergenerational risks justify deep caution.",
        description="Meltdowns, proliferation and waste that outlasts institutions aren't ordinary risks. A decentralized renewable grid fails gracefully; a reactor does not.",
        representative_name="Naomi Oreskes",
        representative_note="historian of science writing on risk and trust.",
        proponents="Naomi Oreskes, anti-nuclear NGOs",
    ),
]

ACTIONS = [
    dict(
        order=10,
        kind="learn_more",
        reveal="condensed",
        pos=None,
        title="Our World in Data — energy",
        description="Lifecycle emissions and death rates across every source.",
        url="https://ourworldindata.org/energy",
    ),
    dict(
        order=20,
        kind="donate",
        reveal="condensed",
        pos="advocate",
        title="Good Energy Collective",
        description="Progressive nuclear policy research. 4-star rated.",
        url="#",
    ),
    dict(
        order=30,
        kind="donate",
        reveal="condensed",
        pos="cost-skeptic",
        title="Rocky Mountain Institute",
        description="Renewables-and-efficiency research.",
        url="#",
    ),
    dict(
        order=40,
        kind="policy",
        reveal="normal",
        pos=None,
        title="Comment on NRC reform",
        description="Open dockets on advanced-reactor rules.",
        url="#",
    ),
    dict(
        order=50,
        kind="local",
        reveal="normal",
        pos="risk-first",
        title="Relicensing hearing",
        description="Aging plants hold public hearings near the site.",
        url="#",
    ),
    dict(
        order=60,
        kind="submit_view",
        reveal="normal",
        pos=None,
        title="Add your view",
        description="Your reasoning joins the position landscape — not posted as a comment.",
        url="#",
    ),
]

CRUX = dict(
    lead="Is the West's nuclear cost problem one we can engineer away — or one we've chosen?",
    lead_highlight="or one we've chosen?",
    subtitle="Almost everyone agrees nuclear is low-carbon and historically safe. The real split is narrower: whether runaway Western build costs are a fixable industrial failure or the deliberate price of democratic caution about catastrophic risk.",
    empirical="Then the cost gap is contingent, not intrinsic — the residue of lost supply chains, first-of-a-kind designs, and stop-start programs. Korea still builds at a fraction of Western cost, and France once did by repeating one standardized reactor. Freeze a design, build it in series, and costs slide down the learning curve — so evidence and execution could settle it.",
    values="Then the high price isn't failure but caution made visible — the safety margins, licensing rigor, and veto points a democracy chose against meltdown, proliferation, and waste outlasting its institutions. If that's the real fault line, building cheaper just means caring less — and no data can close that gap. Only a choice can.",
)

# Energy category meta-Basics (facts about the category itself).
ENERGY_CAT_STATS = [
    dict(
        order=10,
        viz="bar",
        label="Topics mapped",
        value="9",
        fill_pct=60,
        note="Across generation, storage, pricing and climate intervention.",
        reveal="condensed",
    ),
    dict(
        order=20,
        viz="bar",
        label="Share of global emissions",
        value="73",
        unit="%",
        fill_pct=73,
        note="Energy is ~73% of global greenhouse-gas emissions.",
        reveal="condensed",
    ),
    dict(
        order=30,
        viz="bar",
        label="Where debates split",
        value="cost",
        unit=" vs risk",
        fill_pct=50,
        note="Most energy fights reduce to cost, speed, and tolerated risk.",
        reveal="condensed",
    ),
]


def seed(apps, schema_editor):
    Category = apps.get_model("topics", "Category")
    Topic = apps.get_model("topics", "Topic")
    Section = apps.get_model("topics", "Section")
    Stat = apps.get_model("topics", "Stat")
    Question = apps.get_model("topics", "Question")
    Position = apps.get_model("topics", "Position")
    Crux = apps.get_model("topics", "Crux")
    Action = apps.get_model("topics", "Action")
    TopicEdge = apps.get_model("topics", "TopicEdge")

    cats = {}
    for name, slug, icon, color_key, desc in CATEGORIES:
        cats[slug] = Category.objects.create(
            name=name, slug=slug, icon=icon, color_key=color_key, description=desc
        )
    for a, b in CAT_LINKS:
        cats[a].connects_to.add(cats[b])

    # ---- Nuclear Energy (the fully authored topic) ----
    nuclear = Topic.objects.create(
        title="Nuclear Energy",
        slug="nuclear-energy",
        icon="atom",
        summary="Fission-based electricity — among the lowest-carbon, lowest-death sources, in a debate that scrambles partisan lines.",
        scope_covered="Civilian fission for grid power: cost, safety, waste, the climate case.",
        scope_excluded="Weapons, fusion, naval propulsion.",
        why_now="A retiring fleet meets climbing demand from AI and electrification, just as climate targets need firm clean power.",
        primary_category=cats["energy"],
    )
    nuclear.categories.add(cats["energy"], cats["ai-technology"])

    sections = {
        kind: Section.objects.create(topic=nuclear, kind=kind)
        for kind in ["overview", "basics", "questions", "positions", "crux", "actions"]
    }

    for s in STATS:
        Stat.objects.create(section=sections["basics"], **s)

    for q in QUESTIONS:
        Question.objects.create(section=sections["questions"], **q)

    pos_objs = {}
    for p in POSITIONS:
        data = {k: v for k, v in p.items() if k != "key"}
        pos_objs[p["key"]] = Position.objects.create(
            section=sections["positions"], **data
        )

    Crux.objects.create(section=sections["crux"], **CRUX)

    for a in ACTIONS:
        Action.objects.create(
            section=sections["actions"],
            order=a["order"],
            kind=a["kind"],
            title=a["title"],
            description=a["description"],
            url=a["url"],
            reveal=a["reveal"],
            position=pos_objs.get(a["pos"]) if a["pos"] else None,
        )

    # ---- Stub topics ----
    stubs = {}
    for title, slug, icon, summary, cat_slugs in STUBS:
        t = Topic.objects.create(
            title=title,
            slug=slug,
            icon=icon,
            summary=summary,
            primary_category=cats[cat_slugs[0]],
        )
        t.categories.add(*[cats[c] for c in cat_slugs])
        stubs[slug] = t

    for slug in ["solar-power", "grid-storage", "ai-existential-risk"]:
        TopicEdge.objects.create(source=nuclear, target=stubs[slug], kind="relates_to")

    # ---- Energy category page content ----
    Section.objects.create(
        category=cats["energy"],
        kind="overview",
        body=cats["energy"].description,
    )
    energy_basics = Section.objects.create(category=cats["energy"], kind="basics")
    for s in ENERGY_CAT_STATS:
        Stat.objects.create(section=energy_basics, **s)
    Section.objects.create(category=cats["energy"], kind="topics")


def unseed(apps, schema_editor):
    for model in (
        "TopicEdge",
        "Action",
        "Crux",
        "Position",
        "Question",
        "Stat",
        "Section",
        "Topic",
        "Category",
    ):
        apps.get_model("topics", model).objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [("topics", "0001_initial")]
    operations = [migrations.RunPython(seed, unseed)]
