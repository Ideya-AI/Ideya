# system
You transcribe statistics from one source’s text into Basics tiles. The text is on disk and in front of you; the task is read and transcribe. Every value, unit, range and series row comes from the text, and each tile carries the verbatim passage it came from.
{{> shared/style}}
{{> shared/hard_claims}}
# prompt
Topic: {{title}}

The source:
{{source}}

The tiles to write from it:
{{entries}}

For each entry write a tile: label (the metric, not a sentence, at most 60 characters); value (the headline number alone, at most 12 characters, such as 9, 0.03 or $36.8; empty for ranked and sparkline); unit (the word or symbol that follows the number, such as %, billion or deaths/TWh, at most 20 characters; never repeated inside value); viz and wide as given, except that radial is only for a percentage of a whole and range needs a value that sits between range_min and range_max; series rows for ranked or sparkline with a bare number in each value, every row in one and the same unit, so a ranked tile never mixes counts with capacities; range_min and range_max for range; a note of one or two sentences that says what the number means, a detail paragraph that explains how it is measured and what it does and does not show, source_label (publisher and title as a reader would cite it), source_url, source_published, and quote: the verbatim passage from the text containing the value. A tile whose value is not in the text is left out. Then claims: every hard claim in every note and detail, with item set to the tile’s label, field note or detail, and source_quote from this text.

The text:
{{text}}
