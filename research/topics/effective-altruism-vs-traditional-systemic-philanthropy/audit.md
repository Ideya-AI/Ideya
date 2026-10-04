# Audit: Effective Altruism
2026-10-02 (re-audit), verdict: ready

This is a re-audit after the editor fixed the one issue the first audit raised. The issue is fixed. The question now reads "Who decides how charitable money is used: donors judging by measured results, or the communities served?" and its leans read "Donors decide" / "Communities decide". The page no longer hands "evidence" to one side of a vote, and the question's why and detail still read cleanly under the new wording. Nothing around the fix broke. The page still tells one coherent story about how much the well-off owe strangers and how to give. It has five distinct, evenly argued camps, and its crux follows from the questions. Mechanical checks are clean: 0 text errors, and 29 of 30 links ok with 1 blocked (the OECD 403). The renders are newer than topic.json, and the glance hash matches renders/glance.hash. The dev server at :8641 serves the new question text and leans. I reviewed the share cards (og, sq, pt) and they pass.

## Issues for editorial
none

## Issues for icons
none

## Needs research (stops the run)
none

## Notes for the human
- Carried from the first audit, unchanged and still notes:
  - Overview summary: "where evidence says it helps most" attaches "evidence" to the first camp alone, in the page's voice. It also appears on all three share cards.
  - The why-now hook (the Pentagon "Americanism, Not Effective Altruism!" post) concerns the AI-safety wing, which the scope excludes. Whether it is the best current hook is a judgment call.
  - The growth-not-aid argument is credited to "those who favor systemic change" in the under-five deaths and extreme poverty details, while that camp itself credits movements. There is no separate aid-skeptic camp.
  - The crux gives "good per dollar" to one side, while Q4 frames systemic change as claiming more good per dollar. The crux subtitle softens this.
  - The GiveDirectly action is tagged to the trust-based camp. A null (cross-camp) tag would match the Q5 why.
  - Repetition: taxpayer co-funding through the deduction appears in three places. GiveWell's four top charities are listed twice. "86,000" is used for both lives saved and the donor count.
  - US households that give to charity is the oldest figure (2020). Its detail spends a sentence on a 49.6 to 50.9 revision.
  - Proponent lists are uneven (six for the evidence-led camp, two for trust-based and two for curb); the arguments are not.
  - Patriotic Millionaires' own phrase "fairer tax system" is used in the page's voice.
- Template (views.md): "$ billion" units render tight ("174.3$ billion", "~2$ billion", "70.7$ billion"). Ranked charts carry no unit at a glance.
- Layout (views.md): "nearly 90" wraps beside the radial ring at 1440. Lean labels wrap to two lines at 390 on Q1, Q3, Q4, Q5 ("Communities decide") and Q6. Nothing is clipped.
- The OECD source returns 403 to the checker (blocked, not dead).
