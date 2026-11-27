# Audit: Embryo Selection & Editing
2026-11-24 (re-audit), verdict: ready

This is a re-audit, and all five issues from the first pass are fixed. The autism sentence now names its source (Herasight, 2026). The Alabama news line in the "Embryos are persons" side has been replaced with argument: the continuity of the organism, the arbitrariness of any later line, and the reply to natural embryo loss. That side now runs 97 words against 100, and its lean label reads "Already persons", which sits on one line at 390. The "Never safe enough" side now makes the verification argument and the 2026 base-editing result and quotes Egli, so it runs 117 words against 103. The ban camp's unattributed quotation is now the camp's own statement. The editing question's why now reads "possible future uses". None of the fixes disturbed the text around them, and the live page at localhost:8641 carries every one. The page still tells one coherent story. Basics moves from current practice to the limits that shape the arguments, the eight questions run even, and the four camps are named by what they want and written with comparable weight (236 to 278 words each). The crux follows from the questions, and the why-now belongs to the topic. The renders postdate topic.json, and the glance hash matches. check_topic_text: 0 errors (one warning, "Fertilisation", which is inside a proper noun). check_links: the ASRM link is reported dead again. This is the same checker false positive (curl gets HTTP 200), so it does not block.

## Issues for editorial
none

## Issues for icons
none

## Needs research (stops the run)
none

## Notes for the human
- check_links still flags the ASRM action URL as dead (HTTP 302). The ASRM site answers a cookieless request with a 302 back to itself and sets cookies; browsers and curl get 200. `topics/management/commands/check_links.py` `_request` (about line 159) builds its opener without a cookie jar. Adding `urllib.request.HTTPCookieProcessor()` to `build_opener` would stop this false positive from blocking every future audit of this topic.
