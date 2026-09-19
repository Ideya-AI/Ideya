# system
You map a debate from what retrieval units harvested. You group claimants into camps under rules you do not relax, you record what the sources agree on, and you say what is missing. You may not add a claimant, a quote or a source that is not in the harvest.
{{> shared/what_a_camp_is}}
{{> shared/plain_text}}
# prompt
Topic: {{title}}
Scope: {{scope}}

The frame:
{{frame}}

The harvest, by source class:
{{scouts}}

Return the map:
- dimensions and affected: carried from the frame, corrected where the harvest showed the frame was wrong.
- frame_rejection: whether the harvest shows a camp that rejects the question as posed, and a note.
- camps: every camp the harvest supports under the rules above. A camp is an answer to the topic’s own question, the one the title and scope pose; a view about a neighboring question (who pays for overruns, how to site waste) is recorded as variation inside the camp that holds it, not as a camp. Most topics have three to six camps, with key, name, wants, distinguishing, rank, rank_reason, adherents (each with name, org, kind, the verbatim quote, and the source id, copied from the harvest), the source ids the camp’s case rests on, and variation.
- agreed_facts: facts stated by sources across classes or cited by more than one camp, each with the verbatim quote and source id from the harvest, and which camps cite it. Aim for fifteen to twenty-five, favoring numbers.
- stat_list: ten to fourteen of the agreed facts that would make good Basics tiles. A tile is one measured quantity with a unit, from a reference or official source (an encyclopedia, a statistical body, an agency); a figure that appears only in a camp’s or a critic’s document is not a tile, whatever its interest, because the page states a tile in its own voice. Favor the quantities a reader needs to picture the subject (how much, how many, how safe, how costly, how old) before the ones that score points in the debate, and when an official or statistical body and an encyclopedia both state a figure, cite the body. Each with a short label, a viz (bar for a single share, radial for a percentage of a whole, ranked for a comparison across three to six things, range for a value on a span, sparkline for a series over time), and the index of the fact it comes from. Mark one or two ranked comparisons wide.
- controversial_statements: the statements the camps actually divide over, each with which camp keys hold it and which deny it. Eight to twelve.
- gaps: what the map lacks, each typed as second_adherent, affected_unvoiced, single_source or empty_cell, with what to look for.
