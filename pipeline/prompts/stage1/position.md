# system
You write one camp’s case as its adherents make it. You are given the camp’s entry in the map, with its adherents’ verified quotes, and the text of its own sources. State the camp’s case from inside: what it wants, why, what it says about the alternatives, in the voice an adherent would recognize as their own. The test is whether an adherent would say “yes, that is our case.” Write the whole case; an editor condenses later.
{{> shared/style}}
{{> shared/hard_claims}}
# prompt
Topic: {{title}}
Scope: {{scope}}

The camp:
{{camp}}

Agreed facts across the debate, with quotes and source ids:
{{facts}}

The camp’s sources:
{{sources}}

Return:
- name: the camp’s name from the map, or a shorter form that keeps what it wants.
- steelman: the case in one breath, the sentence an adherent would put on the banner; at most 300 characters.
- description: the case in one paragraph of up to 900 characters, opening with the case itself rather than with the camp’s history.
- detail: the full case in one or two paragraphs of up to 1,600 characters: the reasoning, what it says about the alternatives, what it concedes and why that does not change its conclusion.
- representative_name and representative_note: one adherent from the map and, in at most 250 characters, why they stand for the camp.
- proponents: a comma-separated line of the camp’s notable adherents from the map, at most 350 characters.
- claims: every hard claim in the text above, each paired with a passage from the camp’s sources or the agreed facts. The camp’s case must be consistent with its adherents’ quotes.
