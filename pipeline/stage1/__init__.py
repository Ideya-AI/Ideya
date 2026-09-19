"""Stage 1, research: find out what the debate actually is, write every section
at research grade, and prove every hard claim before handing on.

Phase A maps, Phase B writes, Phase C proves. Each phase is skipped when the
directory already shows its output, so the stage resumes from wherever it
stopped.
"""

from ..stages import STAGES, Stage
from ..topic import TopicDir
from . import phase_a, phase_b, phase_c

INDEX_FIELDS = ("slug", "title", "scope", "primary_category")


def requires(topic: TopicDir) -> list[str]:
    doc = topic.load_topic()
    return [f"index field {f}" for f in INDEX_FIELDS if not doc.get(f)]


def satisfied(topic: TopicDir) -> bool:
    return topic.verdict_valid("stage1")[0]


def run(topic: TopicDir):
    if not phase_a.done(topic):
        phase_a.run_phase(topic)
    if not phase_b.done(topic):
        phase_b.run_phase(topic)
    phase_c.run_phase(topic)


STAGES.append(Stage("stage1", "research", requires, satisfied, run))
