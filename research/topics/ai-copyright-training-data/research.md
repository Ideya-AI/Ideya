# AI & Copyright — research

Slug: ai-copyright-training-data
Scope: Copyright and payment for works used to train generative models.
Researched: 2026-11-23

## Overview

Generative AI models, the systems that write text, make images, compose music and produce video, are built by copying enormous quantities of existing material into training sets: books, news articles, photographs, song recordings, code, and much of the public web. Most of that material is under copyright, and most of it was copied without the permission of, or payment to, the people who made it. This topic covers the fight over whether that copying is lawful and whether, how and how much the makers of the works should be paid: the lawsuits testing fair use in the United States, the text-and-data-mining exceptions and opt-outs of the European Union, the United Kingdom and Japan, licensing deals between AI companies and publishers, labels and image libraries, and proposals for collective or statutory licenses. It deliberately leaves aside whether AI-generated output can itself be copyrighted, deepfakes and the misuse of a person’s likeness or voice, the privacy of personal data in training sets, and the wider effect of AI on jobs, touching them only where they bear on training data and payment.

The why-now event: on 29 September 2026 the US Court of Appeals for the Third Circuit, in Thomson Reuters v. ROSS Intelligence, held that a legal research startup’s copying of 2,243 Westlaw headnotes to train its AI search tool was not fair use, finding the use “minimally transformative, at best” and holding that “the market for licensing headnotes as text to train AI is rapidly developing” (opinion, https://www2.ca3.uscourts.gov/opinarch/252153p.pdf). Nieman Lab called it the first AI copyright case to reach a federal appeals court (https://www.niemanlab.org/2026/09/federal-appeals-court-upholds-thomson-reuters-landmark-ai-copyright-win/). The court stressed that ROSS’s tool “cannot generate original expression,” so the ruling leaves open the question for generative models. Four weeks earlier, on 1 September 2026, the US Justice Department filed a statement of interest in the consolidated New York Times and authors’ cases against OpenAI and Microsoft in Manhattan, arguing that training large language models on copyrighted text is fair use (cited in the Third Circuit opinion, n.7; Boston Globe, 2 September 2026). OpenAI, Microsoft and the news plaintiffs have cross-moved for summary judgment there, with reply briefs filed in November 2026 and Judge Sidney Stein’s ruling still to come (ChatGPT Is Eating the World tracker, 21 November 2026). On 20 July 2026 a federal court gave final approval to the US$1.5 billion settlement in Bartz v. Anthropic over pirated books, which TechCrunch reported is believed to be the largest in the history of US copyright law; in March 2026 the UK government dropped its preferred plan for a training exception with an opt-out; and in November 2026 the UK Court of Appeal heard Getty Images’ appeal against Stability AI.

The debate is live because the law is unsettled in every major jurisdiction while the money and the models are already moving. Two US district judges in June 2025 found training on books to be fair use on the records before them, yet one of them wrote that “in most cases” unpermitted copying for training will likely be illegal; the Third Circuit has now ruled against fair use for a non-generative tool; and more than 160 copyright suits against AI companies are pending in US courts. Meanwhile AI developers have signed licensing deals with news publishers, record labels and stock-image libraries, which one side reads as proof that a market for training licenses exists and the other as voluntary arrangements for access and quality. The argument runs between authors, artists, musicians, news publishers and their guilds and collecting societies, who want consent and payment; AI developers, many technology-policy groups, open-source advocates and the current US administration, who see training as lawful learning from works; governments in Europe and Asia that have adopted or weighed exceptions with opt-outs; and a growing set of legislators, academics and collecting societies proposing a statutory or collective license that would let training proceed in exchange for payment.

## Basics

### 1. Copyright lawsuits against AI companies in US courts
- Label: US copyright suits against AI companies
- Value: 169
- Unit: lawsuits (cumulative count on the tracker’s map)
- Comparison rows (same source, same unit): 14 February 2026 — 81; 8 October 2026 — 148; 23 November 2026 — 169
- Data year: as of 23 November 2026
- Source label: ChatGPT Is Eating the World, US map of copyright suits v. AI companies
- Source URL: https://chatgptiseatingtheworld.com/category/map-of-ai-copyright-lawsuits/
- Note: A widely used litigation tracker counted 169 copyright suits against AI companies in US courts on 23 November 2026, roughly double its count in February.
- Context: The count is kept by Edward Lee, a law professor at Santa Clara University. It counts each filed suit, so related cases later consolidated (the New York Times, Daily News, Authors Guild and other suits against OpenAI and Microsoft now sit in one multidistrict proceeding in Manhattan) still appear separately, and it includes a few claims beyond classic training disputes, such as removal of copyright information. The tracker’s companion world map counted 27 further suits outside the United States in February 2026, among them GEMA’s cases against OpenAI and Suno in Munich and Getty Images’ case against Stability AI in London. The tracker’s world map of 15 February 2026 noted only seven court decisions on AI training so far (https://chatgptiseatingtheworld.com/2026/02/15/world-map-of-copyright-suits-v-ai-cos-total-107-feb-15-2026-only-7-decision-on-ai-training-so-far/).
- Visualization: ranked (three dates); or bar

### 2. The Anthropic books settlement
- Label: Bartz v. Anthropic class settlement
- Value: 1.5
- Unit: billion US dollars (non-reversionary fund), covering 482,460 works, about US$3,000 per work before fees and costs
- Data year: final approval 20 July 2026
- Source label: US District Court, Northern District of California, Order on Final Approval, Bartz v. Anthropic, No. 3:24-cv-05417-AMO (Dkt. 680)
- Source URL: https://www.susmangodfrey.com/wp-content/uploads/2026/07/Order-on-Final-Approval.pdf
- Note: Anthropic agreed to pay US$1.5 billion, about US$3,000 for each of 482,460 books, to settle claims that it downloaded pirated copies to build its training library.
- Context: The settlement does not turn on whether training is fair use. Judge William Alsup had already ruled in June 2025 that training on the books was fair use, but sent to trial Anthropic’s downloading of pirated copies from Books3, Library Genesis and the Pirate Library Mirror to keep in a central library (stat 4). Facing a class trial over statutory damages on hundreds of thousands of works, Anthropic settled. The final approval order notes that the per-work payment of about US$3,000 is four times the US$750 statutory minimum, and records that by 16 April 2026 claims had been filed for 440,490 of the 482,460 works on the list, 91.3 percent. The court awarded class counsel US$101,561,111 in fees, about 6.8 percent of the fund, well below the 12.5 percent they sought. The release covers past conduct only, not future training or model outputs. Authors’ groups read the settlement as proof that piracy carries a price; AI developers point out that it left the fair use ruling on training untouched.
- Visualization: bar

### 3. Statutory damages per infringed work in the United States
- Label: US statutory damages per work infringed
- Value: 750 to 30,000
- Unit: US dollars per work; up to 150,000 per work if infringement is willful; as low as 200 if innocent
- Data year: current law (17 U.S.C. § 504(c))
- Source label: 17 U.S. Code § 504, via Cornell Legal Information Institute
- Source URL: https://www.law.cornell.edu/uscode/text/17/504
- Note: US copyright law lets a court award between US$750 and US$30,000 for each infringed work, and up to US$150,000 when the infringement is willful, without proof of actual loss.
- Context: Statutory damages are what turn AI training cases into existential risks for developers. A training set holds millions of works, and a class of rights holders who registered their copyrights can claim damages per work without proving how much each lost. At the US$750 floor, a class of 482,460 works, the size of the Anthropic class (stat 2), carries more than US$360 million in minimum exposure, and a willful finding raises the ceiling to over US$72 billion. Defenders of the remedy say it exists because actual harm from copying is hard to prove; critics, including AI developers and some copyright scholars, say it was designed for individual infringers and produces damages untethered to any real loss when applied to mass copying.
- Visualization: range (US$200 innocent floor to US$150,000 willful ceiling, with the ordinary US$750 to US$30,000 band marked)

### 4. Pirated book copies downloaded by Anthropic
- Label: Pirated book copies in Anthropic’s training library
- Value: over 7
- Unit: million copies of books
- Comparison rows (same source, same unit): Books3 — 196,640 books (downloaded early 2021); Library Genesis — at least 5 million (June 2021); Pirate Library Mirror — at least 2 million (July 2022)
- Data year: downloads 2021 to 2022; court finding June 2025
- Source label: Bartz v. Anthropic, Order on Fair Use, N.D. Cal., 23 June 2025 (Dkt. 231)
- Source URL: https://www.govinfo.gov/content/pkg/USCOURTS-cand-3_24-cv-05417/pdf/USCOURTS-cand-3_24-cv-05417-0.pdf
- Note: A federal court found that Anthropic downloaded over seven million copies of books from pirate libraries before it began buying and scanning print books.
- Context: Judge Alsup found that Anthropic later spent many millions of dollars buying millions of print books, whose bindings its service providers stripped before scanning the pages and discarding the paper, and held that training on books, whether bought or pirated, was fair use, calling the technology “among the most transformative many of us will see in our lifetimes.” But he held that downloading pirated copies to keep in a permanent central library was a separate use that was not justified, and that part went toward trial before the settlement (stat 2). In Kadrey v. Meta two days later, thirteen authors sued Meta for downloading their books from shadow libraries, partly by torrenting, to train its Llama models; Judge Vince Chhabria ruled for Meta on fair use on the record before him, while a separate claim over Meta’s redistribution of files during torrenting remained, and in June 2026 the authors asked him to certify the downloading question for immediate appeal. Shadow libraries matter to the debate because they show what developers chose when lawful sources were slower or costlier: the Bartz order says Anthropic preferred pirating to avoid what its chief executive Dario Amodei called the “legal/practice/business slog” of acquiring books lawfully.
- Visualization: ranked (three sources)

### 5. UK public consultation responses on AI and copyright
- Label: UK consultation respondents preferring each option
- Value: 81
- Unit: percent of respondents (Citizen Space responses) who named option 1, licensing required in all cases, as their preference
- Comparison rows (same source, same unit): option 1, strengthen copyright and require licenses in all cases — 81 percent; option 0, keep the current law — 10 percent; option 3, a training exception with a rights holder opt-out (the government’s preferred option at the time) — 3 percent; option 2, a broad exception with no opt-out — “a very low number” (no percentage given)
- Data year: consultation December 2024 to February 2025; report published 18 March 2026
- Source label: UK Government, Report on Copyright and Artificial Intelligence (section 136, Data (Use and Access) Act 2025)
- Source URL: https://www.gov.uk/government/publications/report-and-impact-assessment-on-copyright-and-artificial-intelligence/report-on-copyright-and-artificial-intelligence
- Note: Of those who answered the UK government’s 2024–25 consultation online, 81 percent preferred requiring licenses for all AI training and 3 percent backed the government’s own proposal of an exception with an opt-out.
- Context: The consultation received 11,520 responses, 10,110 through the online Citizen Space form (on which the percentages are based) and 1,410 by email. A consultation is not a poll: respondents choose themselves, and it ran during a public campaign by the creative industries against the opt-out proposal, so the shares measure who engaged, not the views of the population. The government nonetheless concluded that “a broad copyright exception with opt-out is no longer the government’s preferred way forward” and said it would gather more evidence before changing the law. The fight had spilled into Parliament in 2025, when the House of Lords repeatedly amended the Data (Use and Access) Bill to require AI transparency; the compromise was the statutory duty to publish this report and an economic impact assessment.
- Visualization: ranked (three options with percentages)

### 6. Support for disclosing training sources, UK consultation
- Label: UK respondents who want AI developers to disclose training sources
- Value: over 90
- Unit: percent of consultation respondents answering question 17
- Data year: consultation December 2024 to February 2025; report March 2026
- Source label: UK Government, Report on Copyright and Artificial Intelligence
- Source URL: https://www.gov.uk/government/publications/report-and-impact-assessment-on-copyright-and-artificial-intelligence/report-on-copyright-and-artificial-intelligence
- Note: Over 90 percent of those who answered the relevant UK consultation question agreed that AI developers should disclose the sources of their training material.
- Context: Transparency is the one demand that draws support well beyond the licensing camp, because rights holders cannot enforce any rule, whether a license, an opt-out or a levy, without knowing what was used. The EU’s AI Act already requires general-purpose model providers to publish a “sufficiently detailed summary” of training content on a Commission template, applying to new models since 2 August 2025 (Regulation (EU) 2024/1689, Article 53(1)(d), https://eur-lex.europa.eu/eli/reg/2024/1689/oj); the European Parliament’s March 2026 resolution asked for an itemized list of works instead (stat 7). AI developers generally accept summaries but resist work-by-work disclosure, citing trade secrets and the impracticality of listing billions of documents.
- Visualization: radial (a share)

### 7. European Parliament vote on copyright and generative AI
- Label: European Parliament vote on its copyright and generative AI resolution
- Value: 460
- Unit: votes in favor
- Comparison rows (same source, same unit): in favor — 460; against — 71; abstentions — 88
- Data year: 10 March 2026
- Source label: European Parliament press release, “Protecting copyrighted work and the EU’s creative sector in the age of AI”
- Source URL: https://www.europarl.europa.eu/news/en/press-room/20260306IPR37511/protecting-copyrighted-work-and-the-eu-s-creative-sector-in-the-age-of-ai
- Note: The European Parliament voted 460 to 71, with 88 abstentions, to call for fair pay for creators whose works train generative AI, including for past use.
- Context: The resolution, drafted by German MEP Axel Voss, is non-binding: only the European Commission can propose legislation, and it is preparing a review of the 2019 Copyright in the Digital Single Market Directive, whose Article 4 currently permits text and data mining unless rights holders have reserved their rights in machine-readable form. Parliament asked that generative AI use be “fairly remunerated,” that the Commission examine payment for past use, that providers give an itemized list of works used in training with missing records potentially treated as infringement, that the EU Intellectual Property Office could manage an opt-out list, and that EU rules apply to any model on the EU market “regardless of the place of training.” It rejected a global license in exchange for a flat-rate payment. Technology groups such as ITIF urged the Commission instead to keep the existing exception as the basis for AI training.
- Visualization: ranked (for, against, abstain)

### 8. American opinion on training AI on the open internet
- Label: US adults on whether AI may train on the open internet
- Value: 44
- Unit: percent of US adults who say AI companies should not be allowed to train models on the open internet
- Comparison rows (same source, same unit): should not be allowed — 44 percent; should be allowed — 20 percent; not sure — the remainder (about 36 percent)
- Data year: survey 2–3 May 2024, 12,876 US adults
- Source label: YouGov, “Should consent be required for data used to train AI models?”
- Source URL: https://yougov.com/en-us/articles/49867-americans-consent-be-required-data-used-to-train-ai-models-artificial-intelligence-poll
- Note: In a 2024 YouGov poll, 44 percent of Americans said AI companies should not be allowed to train on the open internet, which the question noted contains large amounts of copyrighted material; 20 percent said they should.
- Context: The question told respondents that the open internet includes large amounts of copyrighted data, which may have shaped answers. Opposition was bipartisan: 43 percent of Democrats and 48 percent of Republicans said such training should not be allowed. In the same poll, 28 percent said AI companies rarely or never have permission from copyright holders, against 22 percent who said they always or usually do, and 40 percent expected creators rather than AI companies to win the lawsuits. The survey is from 2024; no more recent national poll asking the same question was found.
- Visualization: ranked (three answers)

### 9. Americans who say AI should credit its sources
- Label: US adults who say generative AI should credit sources
- Value: 75
- Unit: percent of US adults who say credit is needed when AI produces text nearly word for word from a journalist’s work
- Comparison rows (same source, same unit): near word-for-word journalist content — 75 percent; images imitating a current artist’s style — 67 percent; text imitating a current author’s style — 67 percent; credit sources in general — 54 percent (14 percent say not needed, about a third unsure)
- Data year: survey 7–11 February 2024, 10,133 US adults
- Source label: Pew Research Center, “Many Americans think generative AI programs should credit the sources they rely on”
- Source URL: https://www.pewresearch.org/short-reads/2024/03/26/many-americans-think-generative-ai-programs-should-credit-the-sources-they-rely-on/
- Note: Three in four Americans say an AI program that reproduces a journalist’s work nearly word for word should credit the source; the survey asked about credit, not payment.
- Context: Pew asked whether generative AI programs should credit the sources they rely on in a series of scenarios. Majorities said credit was needed in every scenario, including about six in ten for summaries of information reported by many news organizations. The survey did not ask whether creators should be paid or whether training without permission should be allowed, so it measures a norm of attribution rather than support for any licensing regime.
- Visualization: ranked (four scenarios)

### 10. Web content closed to AI crawlers
- Label: Share of a major training corpus restricted by websites
- Value: 5
- Unit: percent or more of all tokens in the C4 web corpus fully restricted by robots.txt, April 2023 to April 2024
- Comparison rows (same source, different bases noted): all tokens in C4, restricted by robots.txt — 5 percent or more; tokens from the most actively maintained, critical sources in C4, restricted by robots.txt — 28 percent or more; C4 restricted by terms of service — 45 percent
- Data year: audit of 14,000 web domains, April 2023 to April 2024
- Source label: Longpre et al., “Consent in Crisis: The Rapid Decline of the AI Data Commons,” Data Provenance Initiative (NeurIPS 2024)
- Source URL: https://arxiv.org/abs/2407.14933
- Note: Within one year, websites fully closed 28 percent or more of the most important sources in a widely used AI training corpus to crawlers, and 5 percent or more of all its text.
- Context: Robots.txt is a voluntary signal, a file in which a website asks crawlers not to visit; it was built for search engines, and compliance by AI crawlers is a matter of each company’s policy. The researchers found the restrictions concentrated among news sites, forums and other high-quality sources, and found the instructions often inconsistent with sites’ terms of service. The finding cuts both ways in the debate: rights holders cite it as evidence that creators do not consent and that opt-outs built on robots.txt do not work for content already scraped, while AI developers cite it as evidence that the opt-out tools the EU and others rely on already function. Infrastructure firms have since moved further: on 1 July 2025 Cloudflare began asking every new customer domain whether to allow AI crawlers, blocking them by default, and said more than one million customers had already used its one-click block (https://cloudflare.com/press-releases/2025/cloudflare-just-changed-how-ai-crawlers-scrape-the-internet-at-large).
- Visualization: ranked (three measures, bases noted)

### 11. AI crawler traffic by purpose
- Label: Share of AI bot crawling done for training
- Value: 79
- Unit: percent of AI crawler activity on Cloudflare’s network, by stated purpose
- Comparison rows (same source, same unit): July 2025 — training 79 percent, search 17 percent, user actions 3.2 percent; July 2024 — training 72 percent, search 26 percent, user actions 2 percent
- Data year: July 2025
- Source label: Cloudflare, “The crawl-to-click gap: Cloudflare data on AI bots, training, and referrals” (29 August 2025)
- Source URL: https://blog.cloudflare.com/crawlers-click-ai-bots-training/
- Note: About four in five AI crawler requests on Cloudflare’s network in July 2025 were collecting content for model training rather than for search or answering a user.
- Context: Cloudflare, which handles a large share of global web traffic, classifies crawlers by declared purpose and compares how often each AI platform crawls a site with how often it sends a visitor back. From January to July 2025 it measured Anthropic’s crawlers at about 38,066 pages crawled per referral in July (down from about 286,930 in January, after Claude gained web search with clickable citations), OpenAI at about 1,091 and Perplexity at about 195. Google’s referrals to news sites in April 2025 were 15 percent below January. Publishers read the numbers as evidence that AI systems take value without returning traffic; the ratios vary widely by period and method, and secondary reports of later figures differ, so they are best read as orders of magnitude.
- Visualization: radial (training share); or ranked (crawl-to-referral ratios by platform)

### 12. How much text one frontier model is trained on
- Label: Training data for Meta’s Llama 3
- Value: over 15
- Unit: trillion tokens (a token is a word or part of a word)
- Data year: April 2024
- Source label: Meta AI, “Introducing Meta Llama 3”
- Source URL: https://ai.meta.com/blog/meta-llama-3/
- Note: Meta trained Llama 3 on more than 15 trillion tokens, all collected from publicly available sources, about seven times the data used for its predecessor.
- Context: The scale is central to both sides. Developers argue that no licensing market could clear rights for billions of documents from millions of owners, so a permission requirement would end the technology or hand it to the few firms that can afford deals. Rights holders reply that developers have chosen which sources to scrape, that the most valuable material comes from a few thousand publishers, labels and libraries who can license it, and that scale is a reason for collective licensing, not for free use. “Publicly available” means reachable on the web, not licensed or out of copyright.
- Visualization: bar

### 13. The stock of human-written public text
- Label: Estimated stock of public human-generated text
- Value: about 300
- Unit: trillion tokens (90 percent confidence interval 100 to 1,000 trillion), quality-adjusted
- Data year: published 2024
- Source label: Villalobos et al., Epoch AI, “Will we run out of data? Limits of LLM scaling based on human-generated data”
- Source URL: https://epoch.ai/blog/will-we-run-out-of-data-limits-of-llm-scaling-based-on-human-generated-data
- Note: Epoch AI estimates the world’s stock of public, human-written text usable for training at about 300 trillion tokens, which it projects frontier models could fully use within roughly the next decade.
- Context: The estimate counts text of sufficient quality and allows for training on the same data more than once. Epoch projected that at current growth rates frontier training runs could exhaust the stock somewhere between 2026 and 2032, though it notes that this need not halt progress, since developers can turn to synthetic data, private data, images and video. For the copyright debate the estimate matters in two directions: it suggests human-made work is becoming scarce and therefore more valuable to license, and it gives developers a reason to argue that the next gains will come from sources other than copyrighted text.
- Visualization: range (100 to 1,000 trillion, central 300)

### 14. Reported value of selected AI content licensing deals
- Label: Reported value of AI content licensing deals
- Value: about 60
- Unit: million US dollars a year (Reddit and Google, the largest annual figure reported for a single training-data deal)
- Comparison rows (different sources and bases, noted): Reddit–Google, February 2024 — about US$60 million a year (Reuters, one source); News Corp–OpenAI, May 2024 — more than US$250 million over five years, cash plus credits for OpenAI technology (Wall Street Journal report; terms undisclosed); Wiley, total AI licensing revenue — US$23 million in fiscal 2024 and US$40 million in fiscal 2025 (company report)
- Data year: 2024 to 2025
- Source label: Reuters via NBC News (Reddit); Engadget citing the Wall Street Journal (News Corp); Wiley fiscal 2025 results release
- Source URL: https://www.nbcnews.com/tech/tech-news/reddit-strikes-60m-deal-allowing-google-train-ai-models-posts-unveils-rcna140168 (News Corp: https://www.engadget.com/openai-will-reportedly-pay-250-million-to-put-news-corps-journalism-in-chatgpt-214615249.html; Wiley: https://newsroom.wiley.com/press-releases/press-release-details/2025/Research-Growth-AI-Licensing-and-Cost-Reduction-Drive-Wileys-Fiscal-2025-Results/default.aspx)
- Note: The largest disclosed or reported training-data deals run to tens of millions of dollars a year per licensor, with most terms kept confidential.
- Context: Licensing has spread across news (Associated Press, Axel Springer, the Financial Times, News Corp and others with OpenAI; publishers with Amazon, Google, Microsoft and Perplexity), music (Universal and Warner with Udio, Warner with Suno, in late 2025, settling their lawsuits), stock images and academic publishing. Most deals bundle training rights with display rights for real-time answers and with attribution, so the price of training alone is rarely visible. The figures are not comparable: Reddit’s is an anonymous-source estimate of a yearly fee, News Corp’s a reported multi-year total including non-cash credits, Wiley’s an audited revenue line covering several deals. Rights holders cite the deals as proof of a working market that unlicensed training harms; developers say they pay for access, freshness and display, not because training requires permission.
- Visualization: ranked (with the note that bases differ)

### 15. Creative-sector income at risk, CISAC study
- Label: Creators’ revenue at risk from generative AI by 2028
- Value: 24
- Unit: percent of music creators’ revenues at risk in 2028, compared with a scenario without generative AI
- Comparison rows (same source, same unit): music creators — 24 percent; audiovisual creators — 21 percent
- Data year: projection for 2028, published December 2024
- Source label: CISAC (International Confederation of Societies of Authors and Composers) and PMP Strategy, global economic study
- Source URL: https://www.cisac.org/Newsroom/news-releases/global-economic-study-shows-human-creators-future-risk-generative-ai
- Note: A study commissioned by the world body of authors’ collecting societies projects that, without new rules, generative AI could put 24 percent of music creators’ revenues and 21 percent of audiovisual creators’ revenues at risk by 2028.
- Context: The study projects a cumulative loss of €22 billion over five years, €10 billion in music and €12 billion in audiovisual, while the market for generative AI music and audiovisual output grows from about €3 billion to €64 billion in 2028. It is a projection by a commissioning party that advocates for licensing, built on interviews and market modeling, not a measurement of losses already incurred. It models substitution by AI output, which is the harm the licensing camp says training enables; developers counter that losses from competition by new works are not a copyright harm at all, a point Judge Chhabria’s “market dilution” analysis in Kadrey v. Meta treated as open (see Questions).
- Visualization: ranked (music, audiovisual)

### 16. Creators reporting work lost to generative AI
- Label: UK illustrators and translators who say they have lost work to AI
- Value: 36
- Unit: percent of translator respondents who say they have already lost work due to generative AI
- Comparison rows (same source, same unit): translators, lost work — 36 percent; illustrators, lost work — 26 percent; translators, income decreased in value — 43 percent; illustrators, income decreased in value — 37 percent
- Data year: survey January 2024, 787 responses
- Source label: Society of Authors, AI survey (April 2024), as reported by the European Writers’ Council
- Source URL: https://europeanwriterscouncil.eu/soa-survey-uk-ai-2024/
- Note: In a 2024 Society of Authors survey, 36 percent of translators and 26 percent of illustrators who responded said they had already lost work to generative AI.
- Context: The Society of Authors, the UK trade union for writers, illustrators and translators, surveyed its roughly 12,500 members and other authors and received 787 responses, so the results are self-reported by a self-selected group rather than a random sample. The lost work is a labor-market effect of AI outputs; whether copyright on training data is the right tool to address it is itself one of the questions on this page.
- Visualization: ranked (four measures)

### 17. Signatories of the Statement on AI Training
- Label: Signatories of the Statement on AI Training
- Value: 50,544
- Unit: signatories
- Data year: as of 23 November 2026
- Source label: Statement on AI Training
- Source URL: https://www.aitrainingstatement.org/
- Note: More than 50,000 people have signed a one-sentence statement that unlicensed use of creative works to train generative AI is an unjust threat to creators and must not be permitted.
- Context: The statement was organized in October 2024 by Ed Newton-Rex, a composer and former Stability AI executive who resigned over the company’s position on fair use and later founded Fairly Trained, which certifies models trained only on licensed or public-domain data. Signatories include authors, actors, musicians and visual artists, among them well-known names in each field. It is a petition, not a sample, and measures the reach of the licensing campaign rather than the distribution of opinion.
- Visualization: bar

### 18. Public comments to the US Copyright Office on AI
- Label: Comments to the US Copyright Office’s AI inquiry
- Value: over 10,000
- Unit: public comments received
- Data year: August to December 2023
- Source label: US Copyright Office, Copyright and Artificial Intelligence
- Source URL: https://copyright.gov/ai/
- Note: The US Copyright Office received over 10,000 public comments on AI and copyright by December 2023, and drew on them for a report on training published in pre-publication form in May 2025.
- Context: Part 3 of the Office’s report, on generative AI training, concluded that some training uses will be fair use and others will not, that training on large, diverse datasets “will often be transformative,” and that using pirated material or producing outputs that compete with the originals weighs against fair use; it saw voluntary licensing as feasible in some sectors and, “at this point in time,” recommended “allowing the licensing market to continue to develop without government intervention” (report: https://www.copyright.gov/ai/Copyright-and-Artificial-Intelligence-Part-3-Generative-AI-Training-Report-Pre-Publication-Version.pdf). It also treated “market dilution,” the flooding of a market with AI works that compete with the originals, as a harm courts may weigh. It was released on 9 May 2025, a day before the Register of Copyrights, Shira Perlmutter, was removed by the White House, and as of November 2026 the Office’s page still says a final version “will be published in the future.” The report has no force of law, and courts have cited it on both sides.
- Visualization: bar

## Questions

### 1. Is training a model on a work more like learning from it or copying it?
- Tag: value
- Poles: “Learning, not copying” / “Copying at industrial scale”
- Why contested: Copyright protects expression, not ideas, facts or style, and has long let people read, study and imitate. But a model is not a person: training makes full digital copies, the resulting system can be sold and run at a scale no human matches, and models sometimes retain and reproduce passages. Which analogy governs shapes how every court and legislature reads the existing law, and the US courts have split on how far it reaches: Judges Alsup and Chhabria both called training on books highly transformative in June 2025, while the Third Circuit in September 2026 found a non-generative AI’s copying for a competing product “minimally transformative, at best.”
- Case for “Learning, not copying”: Training extracts statistical patterns about language, images or sound from many works; the model does not store a library and, in most cases, cannot reproduce the works it learned from. That is what human readers, students and artists do, and copyright has never required permission to learn. Judge Alsup put it that the models trained on works “not to race ahead and replicate or supplant them” but to create something different, like “any reader aspiring to be a writer.” The copies made along the way are intermediate, never shown to anyone, like the copies the courts allowed in Google Books and in software reverse-engineering cases. If a model does output a substantial copy of a protected work, existing law already treats that output as infringing; the training is not the problem.
- Case for “Copying at industrial scale”: Copyright law is about copies, and training begins by making complete, exact copies of millions of works, often from pirate sites, for a commercial product. The analogy to human learning flatters the machine: a person cannot read every book ever written in a month, cannot be duplicated a million times, and does not compete with every author at once. Research by A. Feder Cooper, Mark Lemley and colleagues found that while most models tested did not memorize most books, Meta’s Llama 3.1 70B “entirely memorizes some books, like the first Harry Potter book and 1984” (https://arxiv.org/abs/2505.12546v4). And the purpose of the copying is to build a system that produces the same kind of expressive goods, at a fraction of the cost, for the same buyers. Calling that “learning” describes the mechanism, not the economic use.

### 2. Should creators be able to refuse, or only to be paid?
- Tag: value
- Poles: “Consent comes first” / “Payment without veto”
- Why contested: Even many who agree that creators deserve something split over what. One side holds that copyright is a property right whose core is the power to say no, so any regime that lets training proceed without permission, even with payment, takes something. The other holds that the public interest in AI is too large to let individual owners block it, and that a guaranteed payment, a collective license or a levy, serves creators better than a veto most could never enforce. The split runs through the creative sector itself: the European Parliament in March 2026 asked for both remuneration and an opt-out, and rejected a global flat-rate license, while India’s DPIIT committee proposed a mandatory license with statutory royalties and no opt-out.
- Case for “Consent comes first”: The right to decide how one’s work is used is the heart of copyright and of an artist’s control over their own voice. Some creators do not want their work to train systems that will compete with them, imitate their style, or be used for purposes they find objectionable, and no royalty rate compensates for that. A compulsory license sets the price by government decree rather than by negotiation, and history suggests such rates settle low. Consent also produces a better market: when owners can refuse, AI firms must bargain, and the price reflects value. The Statement on AI Training, signed by more than 50,000 people, says unlicensed use “must not be permitted.”
- Case for “Payment without veto”: A veto is meaningful only for owners large enough to enforce it; for millions of individual writers, photographers and posters, a consent rule produces either no license or a license signed by an intermediary on their behalf. Training needs breadth, and a model that leaves out every owner who refuses, or who cannot be found, is weaker and more biased. A statutory license or levy guarantees that every creator whose work is used is paid, including those no AI company would ever approach. Proposals of this kind, such as India’s, aim to make the payment certain while removing the power of a few large owners to hold the technology hostage.

### 3. Does AI output take away the market for the works it learned from?
- Tag: empirical
- Poles: “Real substitution” / “Little measurable harm”
- Why contested: Under US fair use the fourth factor, harm to the market for the original, is often decisive, and in the EU and UK the debate over remuneration turns on the same question. Judge Chhabria wrote in Kadrey v. Meta that the plaintiffs’ “potentially winning argument” was that AI would “flood the market with similar works, causing market dilution,” but that they presented no evidence of it; the US Copyright Office treated dilution as a harm courts may weigh; Judge Alsup compared the complaint to objecting that teaching schoolchildren to write well would create competing works. The evidence is early.
- Case for “Real substitution”: The products compete for the same buyers. A study of an online freelancing platform by Xiang Hui, Oren Reshef and Luofeng Zhou (Organization Science, 2024) found that after ChatGPT’s release, writing-related freelancers saw about 2 percent fewer monthly jobs and 5.2 percent lower monthly earnings (https://olin.washu.edu/about/news-and-media/news/2023/08/study-ai-tools-cause-a-decline-in-freelance-work-and-incomeat-least-in-the-short-run.php). In the Society of Authors’ 2024 survey, 26 percent of illustrators and 36 percent of translators who responded reported lost work. AI-written books, stock images and music flood marketplaces, and AI answers replace visits to the news sites they summarize; Cloudflare’s data show some AI crawlers taking tens of thousands of pages per visitor returned. A separate harm is the lost licensing market itself: the Third Circuit held that the market for licensing headnotes as AI training data was real and that unlicensed copying usurped it.
- Case for “Little measurable harm”: Most evidence of harm concerns competition from new works, not copying of old ones, and copyright has never protected creators from competition by new works in their genre. Fair use asks whether the use substitutes for the specific work copied; a model trained on a novel does not supply that novel to anyone. The freelancer and survey effects measure what AI tools do to labor markets, which would happen equally with models trained only on licensed or public-domain data. Total spending on books, music and news has not collapsed, and AI tools are also used by creators to produce more. On the licensing market, the argument is circular: there is a market for training licenses only if the law requires one, which is the question being decided; Judge Chhabria held that the authors “are not entitled to the market for licensing their works as AI training data.”

### 4. Can licensing work at the scale models are trained on?
- Tag: empirical
- Poles: “Markets can clear it” / “Too many owners”
- Why contested: Frontier models are trained on trillions of tokens from billions of documents with millions of owners, many unknown. Licensing advocates point to a fast-growing market of deals; developers say those deals cover a sliver of what a model needs. The US Copyright Office found voluntary licensing feasible in some sectors and recommended letting the market develop, while acknowledging practical challenges for the full range of works.
- Case for “Markets can clear it”: Licensing is already happening. AI companies have signed deals with news publishers, academic publishers, stock-image libraries, Reddit and record labels; Wiley alone booked US$40 million in AI licensing revenue in fiscal 2025. Collecting societies have licensed mass uses before: radio, public performance and photocopying all involved millions of works and owners, and were solved with blanket licenses. Most of the value of a training set sits in a manageable number of large catalogs. Firms such as Fairly Trained certify models trained without unlicensed data, showing it can be done, and the Anthropic settlement shows that a works list and a claims process can reach more than 90 percent of the works at issue.
- Case for “Too many owners”: The deals so far cover large owners of premium content and are often about real-time display and access rather than training. The open web, the bulk of any training set, consists of billions of pages by people and small firms who cannot be identified, located or paid economically; transaction costs would exceed the value of most individual licenses. A model limited to licensable data is smaller, older and skewed toward the catalogs of a few large rights holders. And licensing at scale favors the companies that can afford it: the Justice Department argued in its September 2026 statement that a ruling against OpenAI would leave only the largest firms able to pay.

### 5. Would a licensing requirement entrench the biggest AI companies?
- Tag: empirical
- Poles: “Locks in incumbents” / “Levels the field”
- Why contested: Both sides claim to be protecting competition. Those favoring fair use say only trillion-dollar firms can pay for licenses at scale, so a license requirement would crush startups, academic researchers and open-source models. Those favoring licensing say free use already hands the advantage to the firms with the most compute and distribution, and that paying for inputs is what every other industry does.
- Case for “Locks in incumbents”: Clearing rights is a fixed cost that scales with the data, not with the firm’s revenue. Google, Microsoft, Meta and OpenAI can sign nine-figure deals; a university lab, a startup or an open-weight project cannot. Large firms also own data troves of their own, from user content to search indexes, that would become a moat if public data required licenses. The Justice Department and the Electronic Frontier Foundation have both made this argument, and some note that the largest AI companies have been among the first to sign licensing deals.
- Case for “Levels the field”: Training costs are dominated by compute, which already concentrates the industry; paying creators would be a modest addition for frontier firms valued in the hundreds of billions of dollars. A clear licensing system, especially a collective or statutory one with set rates, would let small developers buy access on the same terms as large ones, while today only the largest can afford the litigation risk of unlicensed training. And free use protects not startups but the business model of whoever can scrape fastest, at the expense of millions of creators who are the smallest players of all.

### 6. Does the money from licensing reach the people who made the works?
- Tag: empirical
- Poles: “Reaches creators” / “Intermediaries capture it”
- Why contested: Most deals are signed by publishers, labels, platforms and image libraries that own or control rights, not by individual writers, musicians and photographers. Whether licensing is a creators’ remedy or a rights-holders’ revenue stream depends on contracts, many of which predate AI.
- Case for “Reaches creators”: Collective licensing has a long record of paying individuals: performing rights organizations and reproduction rights societies distribute money to millions of members. In the Anthropic settlement the default split for trade and university press books is 50-50 between author and publisher, and authors who hold their rights receive the whole award (Authors Guild, https://authorsguild.org/anthropic). Guilds and unions can bargain for creators’ shares, as the Writers Guild and SAG-AFTRA did for AI terms in 2023. Without a licensing requirement, creators get nothing at all.
- Case for “Intermediaries capture it”: The largest deals so far have gone to platforms and publishers: Reddit was paid for posts its users wrote, and Taylor & Francis licensed its authors’ research to Microsoft for AI in 2024 without consulting them, authors told The Bookseller (https://thebookseller.com/news/academic-authors-shocked-after-taylor--francis-sells-access-to-their-research-to-microsoft-ai). Individual creators have little leverage over how their publisher or label divides AI revenue, and statutory schemes can be eaten by administration costs or distributed by formulas that favor the largest catalogs. Those who argue this point, among them the writer Cory Doctorow, say that creators’ real problem is bargaining power, and that expanding copyright mostly enlarges what intermediaries can demand of them.

### 7. Is a trained model itself a copy of the works it learned from?
- Tag: empirical
- Poles: “Model holds copies” / “Model holds patterns”
- Why contested: If the model’s weights contain the works in a recoverable form, then every copy and download of the model is a reproduction, which matters for where liability falls, for open-weight releases, and for whether training abroad can be reached at home. Courts have split. The Munich Regional Court held in November 2025, in GEMA v. OpenAI, that song lyrics memorized in a model were reproduced in it; the English High Court held in Getty Images v. Stability AI the same month that the Stable Diffusion model was not an “infringing copy” because it does not store the images, a finding Getty has appealed.
- Case for “Model holds copies”: Memorization is a measured fact for some works. Models can be prompted to reproduce song lyrics, news articles and book passages verbatim, and the Cooper and Lemley study reconstructed nearly the entire first Harry Potter book from one model. If information sufficient to reproduce a work is encoded in the weights, the form of the encoding should not matter, any more than a compressed file escapes copyright because it is not human-readable. The Munich court applied that reasoning and held OpenAI liable.
- Case for “Model holds patterns”: A model’s weights are far smaller than the data it was trained on and represent statistical relationships, not stored works. Most works are not memorized at all; memorization of a small share of highly duplicated texts is a defect developers work to reduce, not the function of the model. The English High Court found that Stable Diffusion’s weights had never contained or stored the copyrighted images. Treating the whole model as a copy because a few works can be extracted would make every model unlawful to distribute over a fraction of its contents.

### 8. Should competition with China shape the rules?
- Tag: value
- Poles: “The race comes first” / “Rights are not bargaining chips”
- Why contested: US developers and the current US administration argue that restricting training in the West would cede AI leadership to China, where training on copyrighted works is not seriously constrained. Creators and many legislators reply that national competition does not justify taking property, and that the argument proves too much.
- Case for “The race comes first”: AI capability depends on data, and the country whose firms can train on the broadest data will lead in a technology with economic and military stakes. President Trump said at the launch of the AI Action Plan in July 2025 that paying for every work used is “not doable” and “China’s not doing it” (transcript excerpt, Innovation and Policy Institute (IPI), https://www.ipi.org/policy_blog/detail/president-trumps-comments-on-copyright-ai-excerpt). The Justice Department told the court in September 2026 that the benefits of AI training overlap with national security. OpenAI argued to the White House in March 2025 that if Chinese developers have unfettered access to data and American companies do not, the race is effectively over. Japan (Article 30-4 of its Copyright Act, 2018) and Singapore (its 2021 computational data analysis exception) already allow training without a general opt-out.
- Case for “Rights are not bargaining chips”: Every industry could claim that competition with China justifies ignoring the property of others; the United States does not let carmakers take steel because Chinese rivals might. America’s creative industries are themselves a strategic asset and a major export, and weakening their rights to subsidize AI firms trades one industry for another. A Republican senator, Josh Hawley, joined Democrat Richard Blumenthal in July 2025 to propose requiring express consent for training on copyrighted works, a sign that the national-competition argument has not settled the question even within the President’s party. And the evidence that licensing would cripple US developers is thin: they are among the most valuable companies in history and are already paying for data when courts or deals require it.

## Positions

### 1. Require permission and payment for training
- Adherents:
  - The Authors Guild (institution), the largest US organization of professional writers and a lead plaintiff against OpenAI, told the US Copyright Office “that consent and compensation must be required for all AI training on copyrighted works,” proposing voluntary collective licensing through author organizations and extended collective licensing for past uses: https://authorsguild.org/news/ag-to-copyright-office-require-consent-and-compensation-for-ai-training/
  - Ed Newton-Rex, composer, founder of Fairly Trained and organizer of the Statement on AI Training, which reads that “the unlicensed use of creative works for training generative AI is a major, unjust threat to the livelihoods of the people behind those works, and must not be permitted”; it has 50,544 signatories: https://www.aitrainingstatement.org/
  - The New York Times (institution), whose spokesperson Graham James responded to the Justice Department’s September 2026 filing that “AI companies simply need to pay fairly for the content that makes their products possible, as copyright law requires”: https://www.bostonglobe.com/2026/09/02/business/justice-department-new-york-times-openai/
  - Also in this camp: the News/Media Alliance, the Society of Authors, the Human Artistry Campaign, the major record labels, GEMA and CISAC; in the US Congress, Senators Josh Hawley and Richard Blumenthal, whose AI Accountability and Personal Data Protection Act (S. 2367, July 2025) would require express prior consent to train on copyrighted works (https://www.congress.gov/119/bills/s2367/BILLS-119s2367is.htm); and in the UK, the creative-industries campaign against the government’s opt-out plan.
- The case, in its own voice: Copyright gives authors the exclusive right to make copies of their work, and building a training set means making complete copies of millions of works, very often pirated, for a commercial product that will compete with those works. There is no exception in law for copying a great deal, or for copying in order to build something valuable. Every other input an AI company uses, from chips to electricity to engineers, is paid for; only the creative work that gives the models their capabilities is treated as free. The companies doing this are among the most valuable in the world and can afford to pay. When they have wanted content badly enough, they have paid for it, which shows that licensing is possible. A rule requiring permission does not stop AI; it makes the industry negotiate with the people whose work it depends on, as radio, streaming and every previous technology eventually did, and it preserves the incentive to create the human work that future models will also need.
- Best evidence: Courts and regulators have accepted key parts of the argument. Judge Chhabria wrote in Kadrey v. Meta that “in most cases” copying protected works to train without permission will likely be illegal and that the companies “will generally need to pay copyright holders,” ruling for Meta only because the authors had not built a record of market harm. The Third Circuit held in September 2026 that copying to train a competing AI product was not fair use and recognized a “rapidly developing” market for licensing training data. The Munich court held OpenAI liable in GEMA’s lyrics case in November 2025. The Anthropic case produced a US$1.5 billion settlement over pirated books, and the deals with news publishers, labels and image libraries show a functioning market. In the UK, 81 percent of consultation respondents preferred licenses in all cases, and the government abandoned its opt-out plan.
- Answer to the strongest objection (licensing cannot work at scale and will entrench incumbents): The scale problem is a problem of the companies’ own making and is solvable the way music solved it, with collective licensing through organizations that represent many owners, backed by transparency so creators can see what was used. A license fee is small next to the compute budgets of frontier labs. And the alternative does not help small developers: it hands the value of everyone’s work to whoever has the most compute and distribution, which today is the same few firms.
- Variation inside the camp: Members differ on mechanism. Some, like the Authors Guild, favor voluntary and extended collective licensing with an exemption from antitrust law so authors can bargain together; others want individual licensing only. The European Parliament’s March 2026 resolution pairs remuneration with an opt-out and rejects a global flat-rate license, sitting between this camp and the opt-out camp. Most members also demand full disclosure of training data and payment for models already trained.

### 2. Treat training as lawful use that needs no permission
- Adherents:
  - OpenAI (institution), in its March 2025 submission to the White House on the US AI Action Plan, proposed “a copyright strategy that promotes the freedom to learn,” argued that its training “aligns with the core objectives of copyright and the fair use doctrine,” and wrote that if Chinese developers have unfettered access to data “and American companies are left without fair use access, the race for AI is effectively over”: https://cdn.openai.com/global-affairs/ostp-rfi/ec680b75-d539-4653-b297-8bcf6e5f7686/openai-response-ostp-nsf-rfi-notice-request-for-information-on-the-development-of-an-artificial-intelligence-ai-action-plan.pdf
  - The US Department of Justice (institution), in a 1 September 2026 statement of interest in In re OpenAI, argued that training large language models is transformative fair use and that the public benefits “far outweigh any competitive harm” (as reported in the Boston Globe): https://www.bostonglobe.com/2026/09/02/business/justice-department-new-york-times-openai/
  - President Donald Trump, at the July 2025 launch of the AI Action Plan: “When a person reads a book or an article, you’ve gained great knowledge. That does not mean you’re violating copyright laws or have to make deals with every content provider” (transcript excerpt): https://www.ipi.org/policy_blog/detail/president-trumps-comments-on-copyright-ai-excerpt
  - The Electronic Frontier Foundation (institution), which argues that requiring licenses for training would “limit competition” to the largest firms and that “pricey licensing deals offer a way to lock in their dominant positions”: https://www.eff.org/deeplinks/2026/01/copyright-kills-competition
  - Also in this camp: Meta, Google, Microsoft, Anthropic and Stability AI in litigation; the Computer & Communications Industry Association and Chamber of Progress; open-source and research groups; and many copyright scholars.
- The case, in its own voice: Copyright protects particular expression, not the facts, ideas, styles and patterns that run through it, and it has never required anyone’s permission to learn from a work. Training is learning at scale: a model studies billions of examples to extract the statistical structure of language or images and keeps no library of the works. The copies made along the way are intermediate and unseen, the same kind of copying courts allowed in Google Books, in search engines and in software reverse-engineering, because what comes out is new. Where a model does reproduce a protected work, that output can infringe and should be treated that way; the remedy is to police outputs, not to forbid learning. A permission rule would be impossible to comply with for the open web, would exclude everyone but the richest firms, and would push the frontier of the most important technology of the age to countries that do not ask.
- Best evidence: The two US district judges who ruled on training generative models in June 2025 both found it fair use on the records before them: Judge Alsup called training transformative, “spectacularly so,” and wrote that “the technology at issue was among the most transformative many of us will see in our lifetimes,” and Judge Chhabria found no evidence that Llama could reproduce enough of the plaintiffs’ books “to matter.” The US Copyright Office agreed that training on large, diverse datasets “will often be transformative.” Research led by A. Feder Cooper and Mark Lemley found that most models tested do not memorize most books. The Third Circuit itself distinguished its ruling against ROSS on the ground that ROSS’s tool “cannot generate original expression.” Japan and Singapore have broad exceptions for computational analysis, including training, without a general opt-out.
- Answer to the strongest objection (AI output competes with and displaces the creators whose work trained it): Competition from new works is not a copyright harm. Every writer learned from earlier writers and competes with them; copyright protects against copies of a particular work, not against a flood of new works in the same genre, a point Judge Alsup made when he compared the authors’ complaint to objecting that teaching schoolchildren to write well would create competitors. Where creators are hurt by the arrival of a cheaper technology, the remedies lie in labor, competition and social policy, which would be needed just as much if every model were trained only on licensed data.
- Variation inside the camp: Developers argue mainly from innovation and national competition. A second strand, led by the EFF and the writer Cory Doctorow, argues from creators’ own interests: individual creators have little leverage over the corporations that hold their rights, so any new licensing right would be signed away to publishers, labels and platforms, and creators would be better helped by labor law, collective bargaining and antitrust (https://eff.org/deeplinks/2025/02/ai-and-copyright-expanding-copyright-hurts-everyone-heres-what-do-instead). Members also differ on pirated sources: developers have litigated them as fair use, while many scholars in the camp accept Judge Alsup’s holding that building a library from pirate sites is a separate wrong.

### 3. Allow training unless creators opt out
- Adherents:
  - The Tony Blair Institute for Global Change (institution), whose April 2025 report “Rebooting Copyright” backed a text-and-data-mining exception with an opt-out for rights holders as “sound policy for legal, economic, and geopolitical reasons” that “will require careful implementation to be effective,” and called for internationally harmonized standards for opt-out signals (report: https://institute.global/insights/tech-and-digitalisation/rebooting-copyright-how-the-uk-can-be-a-global-leader-in-the-arts-and-ai; quoted in The Register: https://theregister.com/2025/04/03/blair_institute_ai_copyright)
  - Nasscom (institution), India’s technology industry association, which dissented from the DPIIT committee’s hybrid model and recommended text and data mining “for both commercial and non-commercial purposes where access is lawful,” with rights holders able to reserve publicly accessible works “through a machine readable opt out” and other works through contract (DPIIT working paper, Part 1, December 2025, Annexure): https://openfuture.eu/wp-content/uploads/2026/02/251208one_nation_one_license_one_payment.pdf
  - Also in this camp: the European Union’s current law, Article 4 of the 2019 Copyright in the Digital Single Market Directive, which the AI Act requires general-purpose model providers to respect wherever they train, and the EU’s 2025 General-Purpose AI Code of Practice, whose copyright chapter commits signatories to crawlers that obey robots.txt and other machine-readable reservations; the UK government’s preferred option from December 2024 until March 2026; and Google, which told the UK it supports an opt-out model for creators but that it does not “translate to remuneration rights” (TechRepublic, https://www.techrepublic.com/article/news-openai-google-reject-uk-ai-copyright/).
- The case, in its own voice: Neither extreme works. A licensing requirement for every work cannot be met for the open web and would drive AI development to other countries, while a free-for-all ignores creators who clearly do not want their work used. An exception with an opt-out gives each side what it most needs: developers get legal certainty to train on the vast body of material whose owners do not object, and rights holders who care get a simple, enforceable way to say no, which also gives them the leverage to license on their own terms. It is the existing law across the European Union, so it is not a theory but a working regime that can be improved with better technical standards and transparency.
- Best evidence: The EU has run the system since 2019 and extended it to AI developers through the AI Act, whose obligations have applied to new general-purpose models since August 2025, without halting European AI development. Opt-out signals are spreading: the Data Provenance Initiative found that 28 percent or more of the most critical sources in a major training corpus had restricted AI crawlers within one year, and Cloudflare reported more than one million customers using its one-click AI-crawler block by July 2025. The European Parliament’s March 2026 resolution, for all its demands on pay, keeps the opt-out and asks that it be made workable through a central list.
- Answer to the strongest objection (opt-outs put the burden on creators, most of whom will never use them, and cannot reach works already scraped or copied onto other sites): The burden can be reduced with standards, registries and defaults: a single machine-readable signal recognized by all developers, a public registry like the EU Intellectual Property Office list the European Parliament proposed, and transparency rules so that rights holders can check compliance. A system with imperfect uptake still gives far more control than fair use, which gives none, and far more access than a licensing rule the open web cannot satisfy.
- Variation inside the camp: Members differ on whether opting out should open a path to payment (the European Parliament wants remuneration alongside the opt-out; Google rejects any remuneration right), on whether the exception should cover all commercial training or only research, and on how much transparency developers owe.

### 4. Let training proceed and pay creators through a statutory license
- Adherents:
  - The DPIIT Committee on AI and copyright of India’s Department for Promotion of Industry and Internal Trade (institution), whose majority recommended in December 2025 “a mandatory blanket license in favour of AI Developers for the use of all lawfully accessed copyright-protected works in the training of AI Systems, accompanied by a statutory remuneration right for the copyright holders,” with no option for rights holders to withhold their works, royalties set as a percentage of revenue from AI systems by a government-appointed committee, and a central non-profit collecting body; India’s Ministry of Electronics and IT supported the model: https://openfuture.eu/wp-content/uploads/2026/02/251208one_nation_one_license_one_payment.pdf
  - Martin Senftleben, professor of intellectual property law at the University of Amsterdam, who argues for removing copyright obstacles to training and instead channeling “a certain share of revenue” from generative AI to human authors through a lump-sum, output-based remuneration system, collected by collecting societies (“Win-Win,” Chicago-Kent Law Review, 2025): https://scholarship.kentlaw.iit.edu/cklawreview/vol100/iss1/5
  - Also in this camp: other academics who propose an AI levy or a compulsory license for training, and the collective-management proposals that would let training proceed in exchange for a fixed royalty; the US Copyright Office surveyed compulsory and extended collective licensing in its 2025 report but did not recommend them.
- The case, in its own voice: The real choice is not between permission and free use, because neither will happen at the scale of the internet. Individual licensing will cover only the largest catalogs and leave out the millions of writers, photographers and musicians no AI company will ever approach, while free use pays no one. A statutory license makes training lawful for everyone on the same terms, startups included, and makes payment certain for every creator whose work is used, through collecting bodies that also pay non-members. Rates set by a public body and subject to judicial review avoid both the transaction costs of millions of negotiations and the hold-up power of a few large owners. Collecting payment from the revenue of commercial AI systems ties creators’ income to the value their work helped create, and spares researchers and non-commercial uses.
- Best evidence: Statutory and collective licenses have handled mass uses before, from mechanical licenses for recorded music to broadcast retransmission and private-copying levies, and collecting societies already distribute money to millions of creators. The DPIIT committee examined voluntary licensing, extended collective licensing, a blanket exception and an exception with opt-out and found that each, in its traditional form, either leaves small creators unpaid or burdens developers; it concluded that an opt-out “leaves small creators largely unprotected owing to lack of awareness to opt-out, bargaining power to negotiate, and the mechanisms to see if their content has been scraped.” The UK consultation and the European Parliament both found broad support for remuneration, and the US litigation shows that the alternative to a rule is years of uncertainty and settlements that reach only some owners.
- Answer to the strongest objection (it takes away creators’ right to say no and lets the state set a price that will settle too low): Most creators never had a practical right to say no to web-scale scraping; what they lack is payment, and a statutory right to remuneration delivers it. Rate-setting can be made independent and subject to review, as music royalty boards are, and a revenue share rises with the industry’s success. Creators who object to particular uses remain protected against infringing outputs.
- Variation inside the camp: Members differ on where to collect: on training (India’s model, triggered when the system is commercialized) or on output (Senftleben’s levy on AI services that substitute for human works). They also differ on whether money goes to individual creators or partly into cultural funds, and on whether an opt-out should survive alongside the license.

## Crux

Does training a generative model on a work take something from its creator that the developer should have to pay for?

Almost every camp’s answer turns on two parts of this question. Those who require licenses say yes, because training copies the work and builds a product that competes with it. Those who treat training as lawful use say no, because the model learns patterns rather than keeping the work, and competition from new works is not a taking. The opt-out and statutory-license camps both answer “something, but not a veto”: they disagree with each other over whether the remedy is the right to refuse or the right to be paid.

What evidence could settle: whether models trained on copyrighted works measurably displace sales, commissions and licensing revenue for those works or their authors, as opposed to the effects any capable AI would have whatever it was trained on; how often and how much models retain and reproduce what they were trained on; whether licensing, individual or collective, can reach the long tail of the open web at a cost developers of different sizes can bear; and whether money from licensing deals and settlements actually reaches individual writers, artists and musicians. Courts are already asking the first two questions under fair use, the Third Circuit and Judge Chhabria reached different conclusions about whether a market for training licenses counts, and the next rulings in the OpenAI litigation in Manhattan, the Getty appeal in London and the GEMA cases in Munich will add records.

What no data can close: how much weight a creator’s control over the use of a work deserves against the public’s interest in broad access to knowledge and in fast-improving AI; whether a machine’s learning should be judged by the same standard as a person’s; whether competition with other nations can justify narrowing creators’ rights; and, if creators are owed something, whether it is the right to say no or only the right to a share. Even complete evidence of harm or of harmlessness would leave these choices standing.

## Actions

### 1. Follow the lawsuits on a public tracker
- Kind: learn_more
- Title: Track the AI copyright lawsuits
- What it is: A law professor’s regularly updated map and docket summaries of every US copyright suit against AI companies, with links to key rulings and filings.
- URL: https://chatgptiseatingtheworld.com/
- Resolved: yes (200)
- Serves: neutral

### 2. Read the US Copyright Office’s report on AI training
- Kind: learn_more
- Title: Read the Copyright Office’s analysis of AI training
- What it is: The US Copyright Office’s AI project page, with its 2025 report on generative AI training, the public comments it drew on, and its reports on digital replicas and authorship.
- URL: https://copyright.gov/ai/
- Resolved: yes (200)
- Serves: neutral

### 3. Read the UK government’s report and impact assessment
- Kind: learn_more
- Title: Read the UK’s March 2026 report on copyright and AI
- What it is: The UK government’s statutory report and economic impact assessment, laying out the four policy options, the consultation results and the evidence on each side.
- URL: https://www.gov.uk/government/publications/report-and-impact-assessment-on-copyright-and-artificial-intelligence
- Resolved: yes (200)
- Serves: neutral

### 4. Sign the Statement on AI Training
- Kind: policy
- Title: Add your name to the Statement on AI Training
- What it is: A one-sentence public statement, signed by more than 50,000 creators and others, that unlicensed training on creative works must not be permitted.
- URL: https://www.aitrainingstatement.org/
- Resolved: yes (200)
- Serves: Require permission and payment for training

### 5. Join a writers’ organization pressing for consent and pay
- Kind: volunteer
- Title: Join the Authors Guild
- What it is: Membership in the US writers’ organization that is a lead plaintiff against OpenAI, campaigns for consent, compensation and transparency in AI training, and published guidance for authors filing claims in the Anthropic settlement.
- URL: https://authorsguild.org/join/
- Resolved: yes (200)
- Serves: Require permission and payment for training

### 6. Contact your senators about the AI Accountability and Personal Data Protection Act
- Kind: policy
- Title: Tell your senators where you stand on S. 2367
- What it is: The text of the Hawley–Blumenthal bill, which would let people sue AI companies that train on their copyrighted works or personal data without express prior consent; readers on either side can use it to write to their senators.
- URL: https://www.congress.gov/119/bills/s2367/BILLS-119s2367is.htm
- Resolved: yes (200)
- Serves: Require permission and payment for training (support) or Treat training as lawful use that needs no permission (opposition)

### 7. Support a digital-rights group defending fair use
- Kind: donate
- Title: Donate to the Electronic Frontier Foundation
- What it is: The EFF litigates and lobbies for fair use in AI training, arguing that licensing mandates would entrench the largest technology firms and harm independent creators and researchers.
- URL: https://supporters.eff.org/donate
- Resolved: yes (200)
- Serves: Treat training as lawful use that needs no permission

### 8. Read the authors’ case for fair use
- Kind: learn_more
- Title: Read Authors Alliance’s brief for fair use in AI training
- What it is: Authors Alliance, a nonprofit of authors who want their work widely read and used, explains its amicus brief arguing that AI training should be fair use, filed in the Thomson Reuters v. ROSS appeal.
- URL: https://www.authorsalliance.org/2025/09/30/authors-alliance-files-amicus-brief-in-thomson-reuters-v-ross/
- Resolved: yes (200)
- Serves: Treat training as lawful use that needs no permission

### 9. Set AI-crawler rules for your own website
- Kind: local
- Title: Decide whether AI crawlers may use your site
- What it is: Cloudflare’s documentation for letting site owners see which AI crawlers visit, and allow, block or charge them; similar controls exist through robots.txt on any host.
- URL: https://developers.cloudflare.com/ai-crawl-control/
- Resolved: yes (200)
- Serves: Allow training unless creators opt out

### 10. Block AI crawlers on any web host
- Kind: local
- Title: Add AI crawlers to your robots.txt
- What it is: A community-maintained list of known AI crawlers with ready-made robots.txt and web-server rules, so anyone running a website, on any host, can reserve their content from AI training.
- URL: https://github.com/ai-robots-txt/ai.robots.txt
- Resolved: yes (200)
- Serves: Allow training unless creators opt out

### 11. Choose AI tools trained on licensed data
- Kind: learn_more
- Title: See which AI models are certified as trained on licensed data
- What it is: Fairly Trained, founded by Ed Newton-Rex, lists about 19 companies, products and models it has certified under its “Licensed Model” certification, mostly in music and audio.
- URL: https://www.fairlytrained.org/certified-models
- Resolved: yes (200)
- Serves: Require permission and payment for training

### 12. Read India’s proposal for a statutory AI license
- Kind: learn_more
- Title: Read the DPIIT working paper on a mandatory license with royalties
- What it is: The December 2025 working paper of India’s DPIIT committee, which proposes letting AI developers train on all lawfully accessed works in exchange for royalties set by a government committee and paid through a central collecting body, with Nasscom’s dissent annexed.
- URL: https://openfuture.eu/wp-content/uploads/2026/02/251208one_nation_one_license_one_payment.pdf
- Resolved: yes (200)
- Serves: Let training proceed and pay creators through a statutory license

## Sources

All accessed 2026-11-23.

- Third Circuit, Thomson Reuters v. ROSS Intelligence, No. 25-2153, opinion filed 29 September 2026: https://www2.ca3.uscourts.gov/opinarch/252153p.pdf
- Nieman Lab, “Federal appeals court upholds Thomson Reuters’ landmark AI copyright win” (September 2026): https://www.niemanlab.org/2026/09/federal-appeals-court-upholds-thomson-reuters-landmark-ai-copyright-win/
- Boston Globe, Justice Department statement of interest in New York Times v. OpenAI (2 September 2026): https://www.bostonglobe.com/2026/09/02/business/justice-department-new-york-times-openai/
- Bloomberg Law, “Trump Administration Backs OpenAI in NY Times Copyright Suit”: https://news.bloomberglaw.com/ip-law/trump-administration-backs-openai-in-ny-times-copyright-suit
- The Rio Times, “Where US Courts Stand on AI Training” (5 November 2026): https://www.riotimesonline.com/us-courts-ai-training-copyright-where-things-stand/
- ChatGPT Is Eating the World, homepage and news (OpenAI MDL briefing, 21 November 2026): https://chatgptiseatingtheworld.com/
- ChatGPT Is Eating the World, US map of copyright suits v. AI companies (169 on 23 November 2026; 148 on 8 October 2026): https://chatgptiseatingtheworld.com/category/map-of-ai-copyright-lawsuits/
- ChatGPT Is Eating the World, US map, total 81 (14 February 2026): https://chatgptiseatingtheworld.com/2026/02/15/u-s-map-of-copyright-suits-v-ai-cos-total-81-feb-14-2026/
- ChatGPT Is Eating the World, world map, 15 February 2026 (seven decisions on AI training): https://chatgptiseatingtheworld.com/2026/02/15/world-map-of-copyright-suits-v-ai-cos-total-107-feb-15-2026-only-7-decision-on-ai-training-so-far/
- ChatGPT Is Eating the World, Kadrey motion for interlocutory appeal (9 June 2026): https://chatgptiseatingtheworld.com/2026/06/09/kadrey-asks-judge-chhabria-to-certify-for-interlocutory-appeal-to-9th-circuit-the-judges-2025-summary-judgment-re-metas-downloading-from-shadow-libraries-for-the-purpose-of-ai-training/
- PYMNTS, “AI Copyright Rulings Put Data Governance on the Institutional Agenda” (November 2026): https://www.pymnts.com/news/artificial-intelligence/2026/ai-copyright-rulings-put-data-governance-on-the-institutional-agenda/
- Bartz v. Anthropic, Order on Fair Use, N.D. Cal., 23 June 2025: https://www.govinfo.gov/content/pkg/USCOURTS-cand-3_24-cv-05417/pdf/USCOURTS-cand-3_24-cv-05417-0.pdf
- Bartz v. Anthropic, Order on Final Approval, 20 July 2026: https://www.susmangodfrey.com/wp-content/uploads/2026/07/Order-on-Final-Approval.pdf
- TechCrunch, “Anthropic’s landmark $1.5B copyright settlement is approved” (20 July 2026): https://techcrunch.com/2026/07/20/anthropics-landmark-1-5b-copyright-settlement-is-approved/
- Anthropic Copyright Settlement website: https://www.anthropiccopyrightsettlement.com/
- Authors Guild, Anthropic settlement information: https://authorsguild.org/anthropic
- Kadrey v. Meta, Order on cross-motions for partial summary judgment, N.D. Cal., 25 June 2025: https://storage.courtlistener.com/recap/gov.uscourts.cand.415175/gov.uscourts.cand.415175.598.0.pdf
- 17 U.S. Code § 504 (Cornell LII): https://www.law.cornell.edu/uscode/text/17/504
- UK Government, Report on Copyright and Artificial Intelligence (18 March 2026): https://www.gov.uk/government/publications/report-and-impact-assessment-on-copyright-and-artificial-intelligence/report-on-copyright-and-artificial-intelligence
- UK Government, Report and impact assessment collection page: https://www.gov.uk/government/publications/report-and-impact-assessment-on-copyright-and-artificial-intelligence
- European Parliament press release, “Protecting copyrighted work and the EU’s creative sector in the age of AI” (10 March 2026): https://www.europarl.europa.eu/news/en/press-room/20260306IPR37511/protecting-copyrighted-work-and-the-eu-s-creative-sector-in-the-age-of-ai
- Regulation (EU) 2024/1689 (AI Act), EUR-Lex: https://eur-lex.europa.eu/eli/reg/2024/1689/oj
- ITIF, comments to the European Commission on the copyright environment (24 June 2026): https://itif.org/publications/2026/06/24/comments-european-commission-regarding-copyright-environment-in-europe/
- YouGov, “Should consent be required for data used to train AI models?” (May 2024): https://yougov.com/en-us/articles/49867-americans-consent-be-required-data-used-to-train-ai-models-artificial-intelligence-poll
- Pew Research Center, “Many Americans think generative AI programs should credit the sources they rely on” (26 March 2024): https://www.pewresearch.org/short-reads/2024/03/26/many-americans-think-generative-ai-programs-should-credit-the-sources-they-rely-on/
- Longpre et al., “Consent in Crisis: The Rapid Decline of the AI Data Commons” (arXiv / NeurIPS 2024): https://arxiv.org/abs/2407.14933
- Cloudflare, “The crawl-to-click gap: Cloudflare data on AI bots, training, and referrals” (29 August 2025): https://blog.cloudflare.com/crawlers-click-ai-bots-training/
- Cloudflare press release, “Cloudflare just changed how AI crawlers scrape the internet at large” (1 July 2025): https://cloudflare.com/press-releases/2025/cloudflare-just-changed-how-ai-crawlers-scrape-the-internet-at-large
- Meta AI, “Introducing Meta Llama 3” (April 2024): https://ai.meta.com/blog/meta-llama-3/
- Epoch AI, “Will we run out of data? Limits of LLM scaling based on human-generated data”: https://epoch.ai/blog/will-we-run-out-of-data-limits-of-llm-scaling-based-on-human-generated-data
- NBC News, Reddit–Google AI content licensing deal (February 2024): https://www.nbcnews.com/tech/tech-news/reddit-strikes-60m-deal-allowing-google-train-ai-models-posts-unveils-rcna140168
- Engadget, OpenAI–News Corp deal reported at US$250 million (May 2024): https://www.engadget.com/openai-will-reportedly-pay-250-million-to-put-news-corps-journalism-in-chatgpt-214615249.html
- Wiley, fiscal 2025 results release: https://newsroom.wiley.com/press-releases/press-release-details/2025/Research-Growth-AI-Licensing-and-Cost-Reduction-Drive-Wileys-Fiscal-2025-Results/default.aspx
- CISAC, “Global economic study shows human creators’ future at risk from generative AI” (December 2024): https://www.cisac.org/Newsroom/news-releases/global-economic-study-shows-human-creators-future-risk-generative-ai
- European Writers’ Council, Society of Authors AI survey 2024: https://europeanwriterscouncil.eu/soa-survey-uk-ai-2024/
- Statement on AI Training: https://www.aitrainingstatement.org/
- US Copyright Office, Copyright and Artificial Intelligence: https://copyright.gov/ai/
- US Copyright Office, Copyright and Artificial Intelligence Part 3: Generative AI Training (pre-publication, May 2025): https://www.copyright.gov/ai/Copyright-and-Artificial-Intelligence-Part-3-Generative-AI-Training-Report-Pre-Publication-Version.pdf
- Cooper, Lemley et al., “Extracting memorized pieces of (copyrighted) books from open-weight language models” (arXiv): https://arxiv.org/abs/2505.12546v4
- Olin Business School, Washington University, release on Hui, Reshef & Zhou freelancer study: https://olin.washu.edu/about/news-and-media/news/2023/08/study-ai-tools-cause-a-decline-in-freelance-work-and-incomeat-least-in-the-short-run.php
- Brookings, “Is generative AI a job killer? Evidence from the freelance market”: https://www.brookings.edu/articles/is-generative-ai-a-job-killer-evidence-from-the-freelance-market
- The Bookseller, Taylor & Francis authors and the Microsoft AI deal (July 2024): https://thebookseller.com/news/academic-authors-shocked-after-taylor--francis-sells-access-to-their-research-to-microsoft-ai
- AIPPI, “Getty Images v Stability AI: UK High Court finds no secondary copyright infringement”: https://www.aippi.org/news/getty-images-v-stability-ai-uk-high-court-finds-no-secondary-copyright-infringement-in-landmark-genai-ruling/
- MLex, Getty v. Stability AI Court of Appeal hearing (November 2026): https://www.mlex.com/mlex/articles/2549525
- BCLP, Getty v. Stability AI appeal hearing note: https://www.bclplaw.com/en-US/events-insights-news/key-ai-appeal-court-hearing-getty-v-stability-ai-flags-ai-model-training-and-use-conflicts-and-uk-v-eu-v-us-differences.html
- GEMA, “Landmark ruling: GEMA against OpenAI” (November 2025): https://www.gema.de/en/w/landmark-ruling-gema-against-openai
- IRIS Merlin, Munich Regional Court GEMA v. OpenAI summary: https://merlin.obs.coe.int/article/10428
- Innovation and Policy Institute (IPI), President Trump’s comments on copyright and AI (excerpt, 23 July 2025): https://www.ipi.org/policy_blog/detail/president-trumps-comments-on-copyright-ai-excerpt
- OpenAI, response to OSTP request for information on the AI Action Plan (13 March 2025): https://cdn.openai.com/global-affairs/ostp-rfi/ec680b75-d539-4653-b297-8bcf6e5f7686/openai-response-ostp-nsf-rfi-notice-request-for-information-on-the-development-of-an-artificial-intelligence-ai-action-plan.pdf
- OpenAI, proposals for the US AI Action Plan (summary page): https://openai.com/global-affairs/openai-proposals-for-the-us-ai-action-plan/
- Authors Guild, “AG to Copyright Office: Require consent and compensation for AI training” (2 November 2023): https://authorsguild.org/news/ag-to-copyright-office-require-consent-and-compensation-for-ai-training/
- US Congress, S. 2367, AI Accountability and Personal Data Protection Act (text): https://www.congress.gov/119/bills/s2367/BILLS-119s2367is.htm
- Senator Josh Hawley, press release on the Hawley–Blumenthal bill (July 2025): https://www.hawley.senate.gov/hawley-blumenthal-unveil-bipartisan-bill-empowering-working-americans-to-sue-big-tech-ai-companies-for-stealing-creative-works/
- Electronic Frontier Foundation, “Copyright Kills Competition” (21 January 2026): https://www.eff.org/deeplinks/2026/01/copyright-kills-competition
- Electronic Frontier Foundation, “AI and Copyright: Expanding Copyright Hurts Everyone—Here’s What to Do Instead” (February 2025): https://eff.org/deeplinks/2025/02/ai-and-copyright-expanding-copyright-hurts-everyone-heres-what-do-instead
- Tony Blair Institute for Global Change, “Rebooting Copyright: How the UK Can Be a Global Leader in the Arts and AI” (April 2025; page returned 429 on fetch, content confirmed through The Register): https://institute.global/insights/tech-and-digitalisation/rebooting-copyright-how-the-uk-can-be-a-global-leader-in-the-arts-and-ai
- The Register, Tony Blair Institute AI copyright report (3 April 2025): https://theregister.com/2025/04/03/blair_institute_ai_copyright
- TechRepublic, “OpenAI and Google Reject UK Government’s AI Copyright Proposal”: https://www.techrepublic.com/article/news-openai-google-reject-uk-ai-copyright/
- DPIIT (India), Working Paper on Generative AI and Copyright, Part 1 (December 2025), copy hosted by Open Future: https://openfuture.eu/wp-content/uploads/2026/02/251208one_nation_one_license_one_payment.pdf
- Martin Senftleben, “Win-Win: How to Remove Copyright Obstacles to AI Training While Ensuring Author Remuneration,” Chicago-Kent Law Review 100(1), 2025: https://scholarship.kentlaw.iit.edu/cklawreview/vol100/iss1/5
- Authors Alliance, amicus brief in Thomson Reuters v. ROSS (30 September 2025): https://www.authorsalliance.org/2025/09/30/authors-alliance-files-amicus-brief-in-thomson-reuters-v-ross/
- Authors Guild, join page: https://authorsguild.org/join/
- EFF, donate page: https://supporters.eff.org/donate
- Cloudflare, AI Crawl Control documentation: https://developers.cloudflare.com/ai-crawl-control/
- ai.robots.txt, community list of AI crawlers: https://github.com/ai-robots-txt/ai.robots.txt
- Fairly Trained, certified models: https://www.fairlytrained.org/certified-models
- Creative Commons, CC signals (in development; public alpha planned for early 2027; not used as an action): https://creativecommons.org/ai-and-the-commons/cc-signals/
