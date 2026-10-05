Targeted re-audit of: durable-dates pass

# Audit: Nuclear Energy
2026-10-05, verdict: ready

This re-audit covers only the durable-dates pass in the 21 changed fields of topic.json (git diff). Both mechanical checks pass. check_topic_text gives 0 errors and 1 warning that was already there (the stat 14 note is 211 characters). check_links finds 31 links: 27 ok, 4 blocked (OECD-NEA and IEA hosts return 403 to scripts), 0 dead and 0 placeholder. Every changed sentence keeps the same figures, dates, names and attribution. The why-now now reads in the past tense, tied to 8 September 2026 ("none had run by then"). Stat 4 now reads "benchmark as of 2024". Stat 18 now says Russia was the only HALEU supplier "as of 2026". Stat 16 now credits its 2026 forecast to the IEA. Questions 0 to 6 and positions 1 and 3 now carry "as of 2026" or "in 2026". The question 0 change ("built … in the decade to 2024") matches the period the page already dates China's build times to. All of these will still read true after 2026. A search of the whole file for now-anchored wording ("now", "currently", "today", "still", "yet", "pending", "will", "so far", "to date", "recent") finds only wording that stays true: "the table is now more than a decade old" (an IPCC 2014 table), "at current consumption", the chart label "China, recent average", and lines inside a camp's own argument ("Nuclear supplies that today", "is still being installed at record scale", "does not exist yet either"). The crux and actions contain no dated wording. The editor asked about Palisades "paused fuel loading". That wording comes from the earlier fix cycle, and the last audit accepted it. It does not contradict "had loaded fuel", because loading can begin and then pause. It is outside this pass and is left as it stands. The glance text changed (why-now, stat 16 note, question 4 why), so the orchestrator re-runs the card and poster renders afterwards.

## Issues for editorial
none

## Issues for icons
none

## Needs research (stops the run)
none

## Notes for the human
none
