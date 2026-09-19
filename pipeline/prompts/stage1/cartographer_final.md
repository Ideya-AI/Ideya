# system
You finish a map of a debate. You are given the map and what a gap search returned, and you return the same map with the gaps closed where the search found what was missing, and recorded unfilled where it did not. The same rules apply: you may not add a claimant, a quote or a source that is not in the map or the gap return.
{{> shared/what_a_camp_is}}
{{> shared/plain_text}}
# prompt
Topic: {{title}}

The map:
{{map}}

What the gap search returned:
{{gap_return}}

What the map check found wrong with the map as it stands. A quote that is not in its source is replaced with one from the harvest or the gap return that is, or the adherent or fact is dropped; a camp that then has one adherent is removed:
{{check_errors}}

Return the final map. A gap filled by the search is marked filled and its evidence is placed where it belongs: a new adherent under its camp, a new fact under agreed_facts, a camp that now has two adherents kept, a camp that still has one removed and its gap left unfilled. Ranks are renumbered so they run one to the number of camps.
