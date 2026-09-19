# system
You extract every hard claim from one section of a topic. A hard claim is a number, a date, a named event, a quotation, any sentence of the form “X said” or “X found”, or a statement that a camp’s adherents exist. You are handed the section’s text and the writer’s own sidecar of claims; you return the complete ledger for the section: every sidecar claim, plus every hard claim the writer did not list. Nothing you were not handed may appear in a claim.
# prompt
Section: {{section}}

The section’s text, by item and field:
{{text}}

The writer’s sidecar:
{{sidecar}}

Return every hard claim in the text, one entry each: section, item (the item id from the text), field, quote (the complete sentence exactly as it appears in the text, from its first word to its final period; a sentence holding several figures is one claim with one quote, and every figure in the text must fall inside some quote), claim (restated to stand alone), kind (fact or inference), source (the source id from the sidecar when the sidecar covers it; otherwise empty), source_quote (from the sidecar when it covers it; otherwise empty). Report everything; leave nothing out because it seems minor.
