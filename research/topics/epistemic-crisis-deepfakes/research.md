# Deepfakes & Shared Truth — research

## Overview

This topic is about synthetic media — AI-generated or AI-altered images, video, audio and text that can pass as real — and what it does to a society’s ability to agree on basic facts. It covers deepfakes of politicians and public figures, voice-cloned scams, AI content farms and chatbot answers that blend true and false, nonconsensual sexual deepfakes as the largest documented category of harm, the “liar’s dividend” by which real evidence is waved away as fake, and the responses on offer: labeling and watermark mandates, provenance standards such as Content Credentials, detection tools, likeness rights, election deepfake laws, criminal penalties, and media literacy. It deliberately excludes platform moderation rules — what a given platform takes down or ranks, Section 230 reform as a general matter, and the broader fight over online speech governance — which belong to Content Moderation & Free Speech. It also sets aside AI training on copyrighted work (AI, Copyright & Training Data), the economics of journalism (Collapse of Local News), and trust in science specifically (The Replication Crisis & Trust in Science), touching each only where synthetic media is the mechanism.

Why now: on 2 August 2026 the European Union’s AI Act transparency obligations under Article 50 began to apply, the first binding regime at continental scale requiring that AI-generated content be machine-detectably marked and that deepfakes be labeled for the people who see them, with a deferral to 2 December 2026 for marking by generative systems already on the market (European Commission, https://digital-strategy.ec.europa.eu/en/policies/code-practice-ai-generated-content). [Correction 2026-10-05: the 2 December 2026 deferral for generators already on the market comes from the AI Omnibus agreed in May 2026, not from the cited Commission page, which states no grace period.] The Commission published the final voluntary Code of Practice on Transparency of AI-generated Content on 10 June 2026 and reports that about 190 companies and organizations had signed it by the end of July. The United States is moving the other way in its courts as its own midterm campaign runs: the Wesleyan Media Project counted at least 164 AI-generated or AI-enhanced political ads this cycle as of 4 September 2026, 69 percent of them without an AI disclaimer (https://mediaproject.wesleyan.edu/releases-090426/), and in mid-September 2026 U.S. District Judge Susan Watters preliminarily enjoined Montana’s 2025 election deepfake disclosure law as likely viewpoint discrimination, for the named plaintiffs only (Daily Montanan, 18 September 2026, https://dailymontanan.com/2026/09/18/federal-judge-says-ai-deepfake-election-law-violates-first-amendment/). Federal courts had already struck down California’s two 2024 election deepfake laws in August 2025 and permanently blocked Hawaii’s in January 2026.

The debate is live because the tools have become cheap, fast and good — people now perform barely above chance at telling high-quality fakes from real media — while the measured damage to elections has so far been smaller than predicted, which lets serious people draw opposite conclusions from the same record. Those who favor regulation point to nonconsensual imagery at industrial scale (the Grok “undressing” episode of January 2026), multimillion-dollar voice and video fraud, and growing public anxiety about what is real; those skeptical of the crisis framing point out that most misinformation is low-tech, that audiences consume little of it, and that the deeper problem is distrust and partisanship that predates generative AI. The participants are legislators and regulators (the European Commission, U.S. states, Congress on the NO FAKES Act), AI developers and the provenance coalition around C2PA, election-integrity and consumer advocates such as Public Citizen, digital forensics researchers, civil liberties groups such as FIRE and EFF that have won most of the U.S. court fights so far, human rights documentarians such as WITNESS, and communication scholars who argue the panic outruns the evidence.

## Basics

Label: Human accuracy at detecting high-quality deepfakes
Value: 55.54
Unit: percent correct (pooled accuracy; chance is 50)
Viz: ranked
Series: Audio 62.08; Video 57.31; All formats 55.54 (highlight); Images 53.16; Text 52.00
Data year: 2024
Source label: Diel, Lalgi, Schröter, MacDorman, Teufel & Bäuerle, Human performance in detecting deepfakes: A systematic review and meta-analysis of 56 papers, Computers in Human Behavior Reports 16 (2024)
Source URL: https://doi.org/10.1016/j.chbr.2024.100538
Note: Pooling 56 studies with 86,155 participants, people identified high-quality deepfakes correctly 55.54 percent of the time, and the confidence interval for that figure crosses the 50 percent chance line.
Context: This is the first meta-analysis of human deepfake detection, and its headline is that ordinary viewers cannot reliably tell. The 95 percent confidence interval on overall accuracy runs from 48.87 to 62.10 percent, and the authors report that overall detection sensitivity was not significantly above chance. Audio was the easiest format and text and images the hardest, though the audio estimate rests on only eight effects and has a very wide interval. Training with feedback, AI assistance and exaggerated “caricatured” deepfakes raised accuracy to 65.14 percent, so detection is learnable to a degree, but not to the level a juror, editor or voter would want. The studies used deliberately high-quality fakes; much real-world deceptive content is cruder, which is one reason those skeptical of the crisis framing say lab detection rates overstate the practical problem.

Label: Listeners judging real speech as real, then and now
Value: 64.1
Unit: percent of genuine audio samples correctly judged real
Viz: ranked
Series: Real speech, 2021 baseline 72.7; Real speech, 2026 64.1 (highlight); Fake speech, 2021 baseline 72.9; Fake speech, 2026 71.2
Data year: 2026
Source label: Müller & Choong, Eroding Trust in Real Speech: A Large-Scale Study of Human Audio Deepfake Perception, arXiv:2605.26136 (preprint, 21 May 2026)
Source URL: https://arxiv.org/abs/2605.26136
Note: Compared with a 2021 baseline, listeners were about as good at catching fake audio (72.9 to 71.2 percent) but markedly worse at recognizing real audio as real (72.7 to 64.1 percent).
Context: This is the largest listening study of audio deepfakes to date — 35,532 judgments from 1,768 participants across 138 speech-synthesis and voice-conversion systems — and it is a preprint, not yet peer reviewed. Its finding is what the authors call a skepticism shift: people are not getting worse at spotting synthesis artifacts, they are increasingly distrusting authentic speech. That is the mechanism behind the liar’s dividend, measured rather than argued. Audio from commercial and language-model-based systems was the hardest to catch (61.3 to 65.9 percent accuracy). A machine-learning detector used as a reference point stayed above 94.5 percent accuracy in every condition, which supporters of technical detection cite and skeptics answer by pointing to how detectors degrade on content they were not trained on.

Label: Concern about what is real and fake online
Value: 62
Unit: percent of online news users concerned
Viz: radial
Data year: 2026
Source label: Reuters Institute for the Study of Journalism, Digital News Report 2026, executive summary
Source URL: https://reutersinstitute.politics.ox.ac.uk/digital-news-report/2026/dnr-executive-summary
Note: Across 48 markets, 62 percent of respondents said they were concerned about what is real and what is fake online, up 4 percentage points from 2025.
Context: The Digital News Report asks roughly 2,000 people in each of 48 markets whether they agree that, thinking about online news, they are concerned about what is real and what is fake on the internet; the 2026 executive summary describes the result as concern about fake news online and reports a rise to 62 percent, with jumps of more than 5 points in 11 markets. Concern rose by at least 4 points in every Western European market, including 7 in Norway, 8 in the Netherlands and 9 in Belgium, and the report links the rise to worry about deepfakes, AI slop and politically motivated misinformation; Brazil was the one market where it fell. Nigeria and Kenya were highest. The previous year’s figure was 58 percent, which the World Economic Forum’s Global Risks Report 2026 also cites, noting it reached 73 percent in Africa and the United States. Concern is not the same as exposure or harm: the measure records anxiety, which those skeptical of the crisis framing argue may itself be partly a product of alarmed coverage.

Label: Trust in news and in AI chatbot answers
Value: 37
Unit: percent who trust news most of the time
Viz: ranked
Series: News overall, 2015–2025 typical 40; News overall, global 2026 37 (highlight); News overall, United States 2026 25; Answers from AI chatbots, global 2026 20
Data year: 2026
Source label: Reuters Institute for the Study of Journalism, Digital News Report 2026, executive summary
Source URL: https://reutersinstitute.politics.ox.ac.uk/digital-news-report/2026/dnr-executive-summary
Note: Trust in news fell to 37 percent globally in 2026, the lowest since the Reuters Institute began measuring in 2015; in the United States it was 25 percent, and trust in AI chatbot answers was 20 percent.
Context: Global trust in news had held at 40 percent for three years before falling to 37 percent. Meanwhile weekly use of AI chatbots such as ChatGPT, Perplexity and Gemini for news rose from 7 to 10 percent year on year, so a growing share of people are getting news through a channel they trust even less than journalism. The two figures frame the topic’s central dispute. Those who favor regulating synthetic media read falling trust as the damage generative AI is accelerating; those who think the crisis is overstated note that trust in news was falling long before generative AI, and argue that the causal arrow runs from distrust to the appeal of fakes, not the other way around.

Label: Opponents of a scandal-hit politician after a false “fake news” claim
Value: 32–34
Unit: percent of respondents opposing the politician
Viz: ranked
Series: No response from politician (text scandal) 44; Politician falsely claims misinformation (text scandal) 32–34 (highlight)
Data year: 2021
Source label: Schiff, Jackson Schiff & Bueno, The Liar’s Dividend: Can Politicians Claim Misinformation to Evade Accountability?, American Political Science Review 119(1), 2025
Source URL: https://doi.org/10.1017/S0003055423001454
Note: In a February 2021 experiment with 2,503 Americans, a politician’s false claim that a real text-reported scandal was misinformation cut the share of respondents opposing that politician from about 44 percent to about 32–34 percent.
Context: Across five survey experiments with more than 15,000 American adults, the authors found that falsely crying “fake news” raised support for politicians caught in real scandals by roughly 0.15 to 0.24 standard deviations, more than apologizing or staying silent, and across partisan subgroups. A replication in November 2022 found the share of opponents falling from 58 to about 49 percent. The finding most relevant to deepfakes cuts the other way: falsely claiming that a real video was a deepfake was largely ineffective in the 2021 study, apparently because people still believe video, though in the 2022 replication a claim framed to rally the politician’s partisans did work against video. Awareness of deepfakes rose between the two studies — 22 percent had not heard of them in 2021, 8 percent in 2022 — and the authors flag rising familiarity as one possible reason the video protection weakened. The false claims did not reduce general trust in media.

Label: Deceptive share of AI use in 2024 elections
Value: 50
Unit: percent of documented cases
Viz: radial
Data year: 2024
Source label: Kapoor & Narayanan, We Looked at 78 Election Deepfakes. Political Misinformation Is Not an AI Problem., Knight First Amendment Institute, 13 December 2024
Source URL: https://knightcolumbia.org/blog/we-looked-at-78-election-deepfakes-political-misinformation-is-not-an-ai-problem
Note: Of 78 instances of AI use in 2024 elections worldwide collected by the WIRED AI Elections Project, 39 were deceptive and 39 were not.
Context: The authors estimated that every one of the 39 deceptive cases could have been produced without AI for no more than a few hundred dollars, and cite a News Literacy Project finding that “cheap fakes” — conventionally edited or miscaptioned media — were used seven times more often than AI-generated content in the 2024 U.S. election. Their argument is that the bottleneck for a disinformation campaign is distribution and audience demand, not the cost of making the content. The Alan Turing Institute’s Centre for Emerging Technology and Security reached a compatible conclusion for Europe in 2024, identifying 16 viral AI-enabled disinformation cases in the UK general election and 11 across the EU and French elections and finding no evidence they changed results, while noting they amplified harmful narratives (CETaS, https://cetas.turing.ac.uk/publications/ai-enabled-influence-operations-threat-analysis-2024-uk-and-european-elections; page blocks automated retrieval, figures taken from the institute’s published summary). Those who favor regulation reply that a collection of known cases cannot capture targeted or private deception, and that 2024 measured the tools of 2024.

Label: AI political ads without an AI disclaimer, 2026 U.S. cycle
Value: 69
Unit: percent of identified AI ads
Viz: radial
Data year: 2026
Source label: Wesleyan Media Project, At Least $80 Million Spent on AI Ads This Cycle, 4 September 2026
Source URL: https://mediaproject.wesleyan.edu/releases-090426/
Note: Of at least 164 political ads generated or enhanced with AI tools in the 2026 election cycle, 69 percent of the ads and 78 percent of the spending carried no AI disclaimer.
Context: The ads identified represent just under $80 million in spending across broadcast television, connected TV and digital venues. Eighty percent of the ads and 83 percent of the spending came from Republican candidates or pro-Republican groups, and 11 percent of the ads (14 percent of spending) from Democratic sponsors. Wesleyan calls its count a minimum, because it found AI ads through news coverage, ads that self-disclosed, and its own review for AI visuals, and because there is no federal requirement that political ads disclose AI use. The count includes all AI-generated or AI-enhanced ads, not only deceptive deepfakes of opponents, so it measures how normal AI has become in campaigning rather than how much of it deceives.

Label: U.S. states with laws regulating election deepfakes
Value: 30
Unit: states
Viz: bar
Data year: 2026
Source label: Public Citizen, 30 States Now Have Laws to Regulate Election Deepfakes, 13 May 2026
Source URL: https://www.citizen.org/news/30-states-now-have-laws-to-regulate-election-deepfakes/
Note: Maryland became the 30th state with a law regulating deepfakes in elections in May 2026, according to Public Citizen, which tracks and advocates for such laws.
Context: Public Citizen’s tracker (https://www.citizen.org/article/tracker-legislation-on-deepfakes-in-elections/) lists further enactments since, including Louisiana in June 2026. Most of these laws require a disclosure on deceptive AI depictions of candidates within a window before an election; a few prohibit some such content outright. Their record in court is the counterweight. A federal judge struck down California’s AB 2655 on 20 August 2025 as preempted by Section 230 and its AB 2839 on 29 August 2025 as unconstitutional, writing that the antidote in political expression is counter speech and fact-checking rather than stifling content creation (Georgetown Free Speech Project, https://freespeechproject.georgetown.edu/tracker-entries/federal-judge-strikes-down-california-law-targeting-misinformation/). A federal court permanently blocked Hawaii’s Act 191 on 30 January 2026 in a case brought by The Babylon Bee, and Montana’s law was preliminarily enjoined for the plaintiffs in September 2026. There is no federal statute on political deepfakes.

Label: Deepfake detector performance lost on real-world content
Value: 50
Unit: percent decrease in AUC versus academic benchmarks
Viz: ranked
Series: Video detectors 50 (highlight); Audio detectors 48; Image detectors 45
Data year: 2024
Source label: Chandra et al., Deepfake-Eval-2024: A Multi-Modal In-the-Wild Benchmark of Deepfakes Circulated in 2024, arXiv:2503.02857
Source URL: https://arxiv.org/abs/2503.02857
Note: Open-source deepfake detectors lost about half their discriminating power — AUC fell 50 percent for video, 48 percent for audio and 45 percent for images — when tested on deepfakes actually circulating in 2024 rather than on academic datasets.
Context: The benchmark collected 45 hours of video, 56.5 hours of audio and 1,975 images from social media and detection-platform users in 2024, spanning 88 websites and 52 languages. AUC measures how well a classifier separates real from fake, where 0.5 is a coin toss; the drop moved many off-the-shelf models close to that line. Commercial systems and models fine-tuned on the new data did better, but the authors report they still do not match trained deepfake forensic analysts. The result is the core of the case that detecting fakes is an arms race defenders lose, and the reason the provenance camp argues for authenticating real content instead.

Label: Platforms that surfaced provenance data on an AI video
Value: 1
Unit: platforms out of 8 tested
Viz: bar
Data year: 2025
Source label: The Washington Post, Tests show top social platforms don’t disclose markers on AI videos, 22 October 2025
Source URL: https://www.washingtonpost.com/technology/2025/10/22/ai-deepfake-sora-platforms-c2pa/
Note: When The Washington Post uploaded an AI-generated video carrying Content Credentials to eight major platforms, only YouTube disclosed anything about its origin, inside the expanded description, and none kept the credentials attached or let users view them.
Context: Content Credentials, built on the C2PA standard, attach a signed record of how a file was made and edited, and they are the main industry answer to deepfakes. Adoption on the generating side is large: Google said in May 2025 that more than 10 billion pieces of content had been watermarked with its SynthID system (https://blog.google/innovation-and-ai/products/google-synthid-ai-content-detector/), and TikTok said in July 2026 that it had labeled more than 3 billion pieces of content as AI-generated using Content Credentials and invisible watermarking (C2PA, https://www.prnewswire.com/news-releases/c2pa-welcomes-tiktok-to-steering-committee-advancing-the-adoption-of-content-credentials-at-a-global-scale-302836730.html). The Post’s test shows the weak link is distribution: if the platforms where people see content strip or ignore the record, the record does not reach the viewer. Advocates of provenance read this as an implementation gap that standards and the EU’s new marking rules will close; skeptics read it as evidence that metadata is too easy to lose.

Label: Americans who want to be able to tell AI content from human content
Value: 76
Unit: percent saying it is extremely or very important
Viz: ranked
Series: Extremely or very important to be able to tell 76 (highlight); Not too or not at all confident they can tell 53; Highly confident they can tell 12
Data year: 2025
Source label: Pew Research Center, How Americans View AI and Its Impact on People and Society, 17 September 2025
Source URL: https://www.pewresearch.org/science/2025/09/17/how-americans-view-ai-and-its-impact-on-people-and-society/
Note: Seventy-six percent of U.S. adults said it is extremely or very important to be able to tell whether pictures, videos and text were made by AI or by people, while 53 percent said they were not too or not at all confident they could.
Context: The survey of 5,023 U.S. adults on Pew’s American Trends Panel was conducted from 9 to 15 June 2025. The two numbers answer different questions — one asks how much detection matters, the other how confident people are in their own ability — and the gap between them is the public demand that labeling mandates and provenance systems are both trying to meet. Twelve percent described themselves as highly confident. Confidence is not accuracy: the meta-analytic evidence suggests even confident viewers perform near chance on high-quality fakes.

Label: Accuracy at telling AI-generated faces from real ones
Value: 48.2
Unit: percent correct (chance is 50)
Viz: ranked
Series: Untrained participants 48.2 (highlight); Participants given training and feedback 59.0
Data year: 2022
Source label: Nightingale & Farid, AI-synthesized faces are indistinguishable from real faces and more trustworthy, PNAS 119(8), 2022
Source URL: https://pmc.ncbi.nlm.nih.gov/articles/PMC8872790/
Note: 315 participants classified StyleGAN2-generated and real faces with 48.2 percent accuracy, slightly below chance; with training and trial-by-trial feedback, 219 participants reached 59.0 percent.
Context: In a third experiment, 223 participants rated the synthetic faces 7.7 percent more trustworthy than the real ones (mean 4.82 against 4.48 on a seven-point scale), a statistically significant difference. Feedback improved accuracy overall but participants did not improve over the course of the trials. The study used still faces from a 2020-era generator; image and video generators have improved substantially since, so the authors’ conclusion that synthetic faces had passed through the “uncanny valley” is, if anything, more true now. Hany Farid, a coauthor, is among the most prominent advocates of legal liability for deepfake harms.

Label: Trust in U.S. mass media
Value: 28
Unit: percent with a great deal or fair amount of trust
Viz: ranked
Series: 2020 40; 2024 31; 2025 28 (highlight)
Data year: 2025
Source label: Gallup, Trust in Media at New Low of 28% in U.S., 2 October 2025
Source URL: https://news.gallup.com/poll/695762/trust-media-new-low.aspx
Note: Twenty-eight percent of Americans said they trust newspapers, television and radio to report the news fully, accurately and fairly, the lowest Gallup has recorded.
Context: Trust fell from 31 percent a year earlier and from 40 percent five years earlier. Among Republicans it was 8 percent, the first single-digit reading; among independents 27 percent, matching the previous year’s low; and among Democrats 51 percent, tying their 2016 low. Americans 65 and older were the most trusting at 43 percent. The decline predates generative AI by decades — Gallup recorded trust of 68 to 72 percent in the 1970s — which is the central empirical point for those who argue that synthetic media is a symptom of a trust problem rather than its cause. Those who favor regulation reply that a low-trust public is exactly the environment in which cheap fabrication and the liar’s dividend do the most damage.

Label: Sexualized images generated by Grok on X in 11 days
Value: 3,000,000
Unit: estimated images
Viz: bar
Data year: 2026
Source label: Center for Countering Digital Hate, Grok floods X with sexualized images of women and children, 22 January 2026
Source URL: https://counterhate.com/research/grok-floods-x-with-sexualized-images/
Note: CCDH estimated that Grok’s image-editing feature produced about 3 million sexualized images, including about 23,000 that appeared to depict children, between 29 December 2025 and 8 January 2026.
Context: The estimate is extrapolated from a random sample of 20,000 of the 4.6 million images Grok produced in the period, classified with AI assistance and manual review; CCDH is an advocacy organization that campaigns for platform accountability. It works out to about 190 sexualized images a minute, and one apparently depicting a child every 41 seconds. As of 15 January, 29 percent of the sexualized images of children in the sample were still publicly accessible. The episode triggered an Ofcom investigation of X under the UK Online Safety Act, temporary blocks of X in Malaysia and Indonesia, and inquiries elsewhere, and is the most-cited recent case for regulating generation tools themselves rather than only the people who post their output.

Label: Sexual deepfake videos hosted on one site
Value: 43,000
Unit: videos
Viz: bar
Data year: 2023
Source label: Han, Li, Kumar & Durumeric, Characterizing the MrDeepFakes Sexual Deepfake Marketplace, USENIX Security Symposium 2025
Source URL: https://www.usenix.org/system/files/usenixsecurity25-han.pdf
Note: As of November 2023, MrDeepFakes hosted about 43,000 sexual deepfake videos depicting about 3,800 people, viewed more than 1.5 billion times.
Context: Among the 1,942 most commonly targeted individuals, who account for 95 percent of the site’s videos, 95.3 percent were women; most were actors and musicians, but the researchers found hundreds of targets with little or no public presence despite the site’s celebrity-only rule. Only 43 of those individuals, 2.21 percent, were geopolitical figures, which illustrates a recurring point in the debate: the deepfakes that have done the most documented harm are sexual and personal rather than political. Nonconsensual intimate deepfakes are the one area where U.S. federal law now acts directly: the TAKE IT DOWN Act, whose platform removal duties took effect on 19 May 2026, requires covered platforms to remove reported nonconsensual intimate images within 48 hours (FTC, https://www.ftc.gov/news-events/news/press-releases/2026/05/ftc-begins-enforcing-take-it-down-act).

Label: Loss in a single deepfake video-call fraud
Value: 200,000,000
Unit: Hong Kong dollars
Viz: bar
Data year: 2024
Source label: The Guardian, UK engineering firm Arup falls victim to £20m deepfake scam, 17 May 2024
Source URL: https://www.theguardian.com/technology/article/2024/may/17/uk-engineering-arup-deepfake-scam-hong-kong-ai-video
Note: An employee in engineering firm Arup’s Hong Kong office transferred HK$200 million (about £20 million, or roughly US$25.6 million at the time) to fraudsters after a video call in which AI-generated likenesses posed as senior colleagues.
Context: Hong Kong police reported the case in February 2024 without naming the company; Arup confirmed in May that it was the victim and that fake voices and images were used, adding that its financial stability and operations were not affected. The case became the standard illustration that deepfakes can defeat the most intuitive human check — seeing and hearing a known colleague live. It also shows a dimension of the shared-truth problem that is not about politics at all: when face and voice stop being proof of identity, organizations and families have to fall back on codewords, callbacks and other out-of-band verification.

Label: U.S. fraud losses enabled by generative AI, projected
Value: 40
Unit: billion U.S. dollars per year (projection for 2027)
Viz: ranked
Series: 2023 estimate 12.3; 2027 projection 40 (highlight)
Data year: 2024
Source label: Deloitte Center for Financial Services, Generative AI is expected to magnify the risk of deepfakes and other fraud in banking, 29 May 2024
Source URL: https://www.deloitte.com/us/en/insights/industry/financial-services/deepfake-banking-fraud-risk-on-the-rise.html
Note: Deloitte projected that generative AI could enable U.S. fraud losses to reach $40 billion by 2027, up from $12.3 billion in 2023, a compound annual growth rate of 32 percent.
Context: This is a model-based projection by a consultancy, not a measured total, and it covers fraud categories enabled or amplified by generative AI broadly — deepfake impersonation, business email compromise, synthetic identities — rather than deepfakes alone. It is included because it is the most widely cited estimate of the scale, and because measured totals do not exist: neither the FBI nor most national statistics bodies separate AI-enabled fraud in their loss figures. A reader should treat it as an order of magnitude from an interested industry analyst, not as a count.

Label: AI content farm websites identified
Value: 3,006
Unit: websites
Viz: bar
Data year: 2026
Source label: NewsGuard, NewsGuard Launches Real-time “AI Content Farm” Detection Datastream, 12 March 2026
Source URL: https://www.newsguardtech.com/press/newsguard-launches-real-time-ai-content-farm-detection-datastream-to-counter-onslaught-of-ai-slop-in-news/
Note: NewsGuard had identified 3,006 websites that publish mostly AI-generated content presented as human-written news, a number it says more than doubled over the previous year.
Context: NewsGuard classifies a site as an AI content farm when a substantial share of its content is AI-generated, it does not disclose this, and its appearance could mislead an average reader into thinking humans wrote it. It reports new sites appearing at 300 to 500 a month. NewsGuard is a commercial company that sells reliability ratings, which those wary of centralized credibility judgments note. Most such sites exist for advertising revenue rather than persuasion, which supports the demand-side argument that their main effect is noise rather than belief change; the worry on the other side is that they feed the training data and retrieval sources of AI chatbots.

Label: AI chatbots repeating false claims about the news
Value: 35
Unit: percent of responses to prompts based on false claims
Viz: ranked
Series: August 2024 18; August 2025 35 (highlight)
Data year: 2025
Source label: NewsGuard, One-Year AI Audit Progress Report, 4 September 2025
Source URL: https://www.newsguardtech.com/press/newsguard-one-year-ai-audit-progress-report-finds-that-ai-models-spread-falsehoods-in-the-news-35-of-the-time/
Note: In August 2025 the ten leading AI chatbots repeated false claims in 35 percent of responses to news prompts built on known falsehoods, up from 18 percent a year earlier.
Context: The rise came with a change in behavior: a year earlier the chatbots often declined to answer, and in August 2025 they answered every prompt, so the combined rate of false or non-answers fell from 49 to 35 percent while the false-claim rate itself roughly doubled. The tools tested included ChatGPT, Grok, Copilot, Meta AI, Claude, Gemini and Perplexity. The audit uses prompts deliberately built around circulating falsehoods, including some seeded by state influence networks, so it measures vulnerability on contested news rather than average accuracy. It matters to this topic because chatbots are becoming a news source: the Reuters Institute found weekly use for news at 10 percent in 2026.

Label: Global risk ranking of misinformation and disinformation
Value: 2
Unit: rank among global risks, two-year horizon
Viz: ranked
Series: Geoeconomic confrontation 1; Misinformation and disinformation 2 (highlight); Societal polarization 3; Extreme weather events 4; State-based armed conflict 5
Data year: 2026
Source label: World Economic Forum, Global Risks Report 2026
Source URL: https://reports.weforum.org/docs/WEF_Global_Risks_Report_2026.pdf
Note: More than 1,300 experts surveyed by the World Economic Forum ranked misinformation and disinformation the second most severe global risk over the next two years and fourth over ten years.
Context: The ranking comes from the Global Risks Perception Survey, which asks respondents to estimate the likely severity of each risk over two and ten years. Adverse outcomes of AI technologies ranked fifth on the ten-year horizon. The report ties the concern to the growing difficulty of distinguishing authentic from synthetic video, audio and text. It is a survey of elite perception, not a measurement of harm, and those who think the crisis is overstated cite rankings like this as evidence of how far concern has run ahead of evidence; those who favor action cite it as a consensus of people paid to anticipate risk.

## Questions

Question: Is synthetic media changing what people believe, or mostly confirming what they already thought?
Tag: empirical
Poles: Deceives at scale / Preaches to converted
Why contested: The documented record so far shows many deepfakes and little measurable effect on election outcomes, but the record only captures what was found, and the tools improve every few months.
Case for “Deceives at scale”: People cannot reliably tell high-quality fakes from real media — pooled accuracy of about 55 percent, near chance — and synthetic faces are rated more trustworthy than real ones. A fake does not need to persuade a majority to matter: the Slovak audio clip released days before the 2023 election, the Biden voice robocall before the 2024 New Hampshire primary, and the Arup video call all worked on the few people they reached at the moment it counted. Targeted, private and last-minute deception is exactly what public case collections and post-election studies are worst at catching. And the 2024 elections tested the tools of 2024; audio and video generators released since are markedly better, while AI political ads went from novelty to routine in the 2026 U.S. cycle with most carrying no disclosure.
Case for “Preaches to converted”: Decades of research on misinformation find that the average person consumes very little of it, that consumption is concentrated among people who are already highly partisan or distrustful, and that the bottleneck is reaching an audience, not producing content. Of 78 documented AI uses in 2024 elections, half were not deceptive at all and every deceptive one could have been made cheaply without AI; cheap fakes outnumbered AI fakes seven to one in the U.S. election. Studies of the UK, EU, French and U.S. elections in 2024 found no evidence that AI content changed results. On this reading, deepfakes mostly give committed audiences what they already wanted to see.

Question: Is the bigger danger that people believe fakes, or that they stop believing real evidence?
Tag: empirical
Poles: Fakes fool us / Truth gets doubted
Why contested: The two dangers call for different remedies — catching fakes versus shoring up authentic evidence — and the evidence on the liar’s dividend is newer and more mixed than the evidence on deception.
Case for “Fakes fool us”: The concrete, countable harms today are deceptions: nonconsensual sexual images of real people, scams that use a cloned voice or face, fabricated statements by candidates, and fake news sites. These have identifiable victims and measurable losses. The liar’s dividend is real but bounded: in the largest experiments, false claims that a real video was a deepfake were largely ineffective, because people still believe video. Policy should focus on the harms that are happening, not on a second-order effect that may stay small.
Case for “Truth gets doubted”: The largest listening study to date found that, compared with 2021, people were no worse at catching fake audio but markedly worse at accepting real audio as real — 72.7 percent correct in 2021, 64.1 percent in 2026. Experiments show politicians gain support by falsely calling real reports fake, and the protection video offered weakened as awareness of deepfakes grew. A world where any recording can be dismissed favors the powerful, who can deny, over the documented, who must prove. WITNESS, which runs a rapid-response force for disputed footage, handles claims that authentic evidence is AI-generated as well as actual deepfakes, and warns that hyper-realistic fakes lead people to dismiss reality.

Question: Can provenance and watermarking work at internet scale?
Tag: empirical
Poles: Workable at scale / Easily stripped
Why contested: Billions of items are now marked at creation, but marks can be removed, many generators will never comply, and the platforms where people actually see content have been slow to display the information.
Case for “Workable at scale”: Content Credentials and watermarks are already on billions of items — more than 10 billion from Google’s SynthID by May 2025 and more than 3 billion labeled on TikTok by July 2026 — and the C2PA standard is backed by Adobe, Google, Microsoft, Meta, OpenAI, Sony, TikTok and major news organizations. The EU now requires providers to mark AI output in machine-readable form and to offer detection, with about 190 signatories to the implementing code. The goal is not to label every fake but to let authentic capture — from cameras, newsrooms, campaigns — prove itself, so that unverified content is treated with appropriate caution. HTTPS worked the same way: it did not stop fake websites, but it changed what users could verify.
Case for “Easily stripped”: Metadata disappears with a screenshot or re-encode, and watermarks can be removed or forged by determined actors; open-source generators run by bad actors will never add them. The Washington Post found in October 2025 that of eight major platforms only one showed anything about an AI video’s provenance and none preserved the credentials. A system that marks only the compliant can create false reassurance — unmarked fakes look more trustworthy — and pressure to sign all authentic capture raises privacy risks for journalists, dissidents and witnesses who need anonymity.

Question: Should the law require labels on AI-generated political content?
Tag: value
Poles: Mandatory disclosure / Protected expression
Why contested: Disclosure is the lightest form of regulation and polls well, but in the United States courts have repeatedly found these laws unconstitutional when applied to political speech and satire.
Case for “Mandatory disclosure”: Voters have a right to know when an image of a candidate saying or doing something was manufactured, and disclosure is the least restrictive tool available — it bans nothing. Thirty U.S. states had enacted election deepfake laws by May 2026, mostly disclosure requirements in the weeks before an election, because last-minute fakes leave no time for correction. The EU now requires deepfakes to be labeled for viewers, with narrow allowances for evidently artistic or satirical work. With most AI political ads carrying no disclaimer even where states require one, the case for a clear rule is stronger, not weaker.
Case for “Protected expression”: Political speech is the core of what free speech protects, and the government deciding which depictions of candidates are “deceptive” invites selective enforcement. Labels destroy satire and parody, which depend on the audience getting the joke unprompted, and a mandated AI label can itself mislead by implying an ad is false. Courts have agreed: California’s laws were struck down in August 2025, Hawaii’s in January 2026, and Montana’s was enjoined in September 2026 as likely viewpoint discrimination for covering only content that harms a candidate. Fraud, voter suppression and defamation are already illegal whatever tool is used.

Question: Who should be liable when a deepfake causes harm — the person who makes it, the platform that spreads it, or the company whose tool generated it?
Tag: value
Poles: Toolmakers answer / Users answer
Why contested: Liability placed on tools and platforms can actually be enforced but sweeps in lawful uses; liability placed on individual creators protects innovation but is often unenforceable against anonymous or foreign actors.
Case for “Toolmakers answer”: The companies that build and host generators are the only actors positioned to prevent harm at scale, and they profit from the product. Hany Farid argues that a company that ships a product it knew or should have known would cause harm should face liability as it would in the physical world, and that platform immunity for user posts does not cover output a company’s own model creates. The Grok episode — an estimated 3 million sexualized images in 11 days from a single built-in feature — showed what happens when guardrails are a business choice. Victims cannot sue thousands of anonymous users; they can sue one company.
Case for “Users answer”: Generative tools, like cameras, editors and word processors, have overwhelmingly lawful uses, and making their makers liable for every misuse would push development toward a few large firms able to absorb legal risk and toward pre-emptive censorship of legitimate output. The person who chooses to deceive, defraud or harass is the wrongdoer, and existing law on fraud, defamation, harassment and impersonation already reaches that person. Narrow statutes aimed at specific harms, such as nonconsensual intimate images, can target the conduct without regulating the tool.

Question: Should people own their face and voice as a property right?
Tag: value
Poles: Likeness as property / Privacy, not property
Why contested: Performers and victims want an enforceable right against unauthorized digital replicas; civil liberties groups fear a takedown regime that will be abused against commentary and signed away in contracts.
Case for “Likeness as property”: Without a clear right, a person’s voice or face can be cloned for ads, songs, scams or pornography with little recourse beyond a patchwork of state publicity laws. The NO FAKES Act, advanced unanimously by the Senate Judiciary Committee in June 2026, would create a federal right in one’s voice and visual likeness with a notice-and-removal system and exceptions for news, commentary, satire and parody. Denmark has prepared amendments to its copyright act requiring a person’s consent before realistic digital imitations of their appearance or voice are made available, with satire and parody in principle excluded; the European Parliamentary Research Service reported in January 2026 that they were expected to take effect in July 2026 (https://www.europarl.europa.eu/RegData/etudes/ATAG/2026/782611/EPRS_ATA(2026)782611_EN.pdf). [Correction 2026-10-05: July 2026 passed without adoption; the Afterlife.ai likeness-law tracker reported on 2 October 2026 that the Danish parliament had not yet adopted the amendments.] Performers’ unions and the music industry support this because it gives individuals something enforceable.
Case for “Privacy, not property”: A transferable property right will be signed over to studios and labels in standard contracts, protecting the companies rather than the people. A notice-and-takedown system modeled on copyright invites abuse: anyone claiming to be depicted could force removal of criticism, satire or news, and platforms will over-filter to avoid liability. EFF argues the real interest at stake is privacy and dignity, which a narrower privacy law could protect without creating a new speech-suppression tool.

Question: Will detection keep pace with generation?
Tag: empirical
Poles: Detectors catch up / Generators stay ahead
Why contested: Detection tools post excellent results on familiar data and much worse ones on content in the wild, and each new generator resets the contest.
Case for “Detectors catch up”: Detectors fine-tuned on current real-world data recover much of their lost performance, and a reference detector in the 2026 audio study kept above 94.5 percent accuracy in every condition. Trained forensic analysts still outperform both the public and automated tools, and combining automated screening with expert review and provenance gives a layered defense. Detection does not need to be perfect to be valuable; it needs to be available quickly to the journalists, election officials and courts who face disputed content.
Case for “Generators stay ahead”: The structural advantage belongs to the generator: any detector can be used to train a better fake. Off-the-shelf detectors lost about half their accuracy on deepfakes circulating in 2024, and many fell to near-random performance. Detection also fails asymmetrically for the people who most need it — less common languages, low-quality phone footage, communities without access to commercial tools — and a false positive on authentic evidence does the liar’s work. That is why the provenance camp argues the burden must shift to proving what is real.

Question: Is the root problem the supply of fabricated content or the demand for it?
Tag: empirical
Poles: Supply drives harm / Demand drives harm
Why contested: The answer decides whether regulating generators and content can work, and the evidence for each side comes from different kinds of studies — measures of what the tools can do versus measures of who consumes falsehood and why.
Case for “Supply drives harm”: Generative AI collapsed the cost and skill required to fabricate convincing media and to flood an environment with plausible text, and supply creates its own demand when content is engineered for engagement. More than 3,000 AI content farms have appeared in a few years, chatbots repeated false claims in 35 percent of tested news prompts in 2025, and an estimated 3 million sexualized images came from one feature in under two weeks. Cheap abundance also has a cumulative effect that individual-exposure studies miss: when fakes are everywhere, doubt about everything rises.
Case for “Demand drives harm”: People seek out and share falsehoods that fit their identity, and they do so with low-tech material as readily as with deepfakes. Trust in U.S. media fell from about 70 percent in the 1970s to 28 percent in 2025, long before generative AI. If distrust and polarization create the demand, then cutting supply of one kind of content will be routed around, and the effective interventions are rebuilding trusted institutions, strengthening journalism, and teaching verification habits.

## Positions

Camp: Require labels and liability for synthetic media
Adherents: European Commission, which enforces the AI Act’s Article 50 duties to mark AI output and label deepfakes, framed as addressing “risks of deception and manipulation” and “fostering the integrity of the information ecosystem” (https://digital-strategy.ec.europa.eu/en/policies/code-practice-ai-generated-content); Public Citizen, which tracks and campaigns for state election deepfake laws, its democracy organizing manager Ilana Beller saying states are “protecting constituents from the threat of generative AI deceiving voters and undermining elections” (https://www.citizen.org/news/30-states-now-have-laws-to-regulate-election-deepfakes/); Hany Farid, UC Berkeley digital forensics professor, who argues that a company that knowingly ships a harmful product should be sued “back to the dark ages” and that platform immunity does not cover AI output a company itself creates (Scientific American, 17 February 2026, https://www.scientificamerican.com/article/deepfakes-are-getting-faster-than-fact-checks-says-digital-forensics-expert/).
Case: When anyone can fabricate a convincing video of anyone else in seconds, a society cannot rely on viewers to sort real from fake — the evidence says they perform near chance — and it cannot rely on companies to police themselves, because the companies have shown what they do when guardrails cost engagement. The answer is rules with teeth, built in layers. AI providers should be required to mark what their systems generate in ways machines can detect, and anyone deploying a realistic deepfake should have to tell the people who see it. Election deepfakes of candidates should carry clear disclosure in the window before a vote, when there is no time for correction. Nonconsensual sexual deepfakes and AI impersonation for fraud should be crimes with fast removal duties. And the companies that build and host generation tools should be liable when they knew or should have known their product would be used to harm people, as any manufacturer would be. Disclosure bans nothing; it restores a fact the viewer is entitled to know. The point is not to stop synthetic media but to put the cost of its harms on the people who profit from it rather than on its victims.
Evidence: Human detection accuracy of about 55 percent across 56 studies, and synthetic faces rated more trustworthy than real ones. An estimated 3 million sexualized images, including about 23,000 apparently of children, from one Grok feature in 11 days. A HK$200 million fraud by video call. Most AI political ads in the 2026 U.S. cycle carrying no disclaimer, which shows voluntary disclosure does not happen on its own. Only one of eight platforms surfacing provenance data in The Washington Post’s test, which shows that industry standards without obligations do not reach the viewer. Strong public demand: 76 percent of Americans say it is important to be able to tell AI content from human content.
Variation: Within the camp, emphasis varies. The EU model is horizontal: marking and labeling duties on all providers and deployers. U.S. states have focused on election windows and on nonconsensual imagery, and the federal TAKE IT DOWN Act on removal of intimate images. A likeness-rights wing, including the bipartisan sponsors of the NO FAKES Act and performers’ unions, wants individuals to hold an enforceable right in their own voice and face, the route Denmark has taken through amendments to its copyright act. Some, after the Grok episode, want to restrict nudification tools outright rather than label their output.
Answer to objections: To the free-speech objection, this camp answers that disclosure is the least restrictive tool there is, that the EU and well-drafted state laws exempt evident satire and parody, and that courts striking down particular drafts have objected to their wording — viewpoint selectivity, vagueness, burdens on platforms — rather than to the idea that voters can be told what is synthetic. To the claim that demand, not supply, is the problem, it answers that both matter and only one is within a legislature’s reach this year; the people harmed by nonconsensual images and fraud are not harmed by their own partisanship. To the provenance camp, it answers that voluntary standards are welcome but have not reached viewers, and obligations are what make standards stick.

Camp: Build provenance that proves what is real
Adherents: Coalition for Content Provenance and Authenticity (C2PA), the standards body behind Content Credentials whose steering committee includes Adobe, Google, Microsoft, Meta, OpenAI, Sony and, since July 2026, TikTok, its chair Clement Wolf saying TikTok’s implementation “demonstrates how provenance can deliver meaningful value in real-world environments” (https://www.prnewswire.com/news-releases/c2pa-welcomes-tiktok-to-steering-committee-advancing-the-adoption-of-content-credentials-at-a-global-scale-302836730.html); Andy Parsons, senior director of Adobe’s Content Authenticity Initiative, who describes Content Credentials as a “nutrition label” that lets people “find out for themselves” where content came from, while calling it “not a silver bullet” (DPReview, https://www.dpreview.com/interviews/3215783269/adobe-max-2024-content-credentials-authenticity-initiative/); WITNESS, the human rights video organization led by Sam Gregory, which participates in C2PA and argues for privacy-protecting, opt-in provenance alongside equitable access to detection (https://www.gen-ai.witness.org/).
Case: Chasing fakes is a race the defenders lose: every detector becomes training data for a better generator, and off-the-shelf detectors already lose half their accuracy on content in the wild. The durable fix runs the other way — make authentic media able to prove itself. Cameras, editing software, newsrooms, campaigns and AI generators can attach a cryptographically signed record of where a file came from and what was done to it, and platforms can show that record to viewers. Once authentic capture routinely carries credentials, unverified content earns appropriate caution without anyone having to rule on what is true. This is an open, interoperable standard, built across competitors and news organizations, that informs rather than censors; it puts the judgment in the viewer’s hands. Laws can help by requiring generators to mark output and platforms to preserve and display credentials, but the system has to be built by the ecosystem, not decreed content by content.
Evidence: More than 10 billion items watermarked with SynthID by May 2025; more than 3 billion items labeled on TikTok using Content Credentials by July 2026; a standard backed by the largest AI developers, camera makers and news organizations. The EU’s marking rules, which took effect in August 2026, rely on precisely the techniques this camp built — metadata plus watermarking — and about 190 organizations signed the implementing code. Deepfake-Eval-2024’s finding that detectors degrade badly on real-world content, which is the core argument for authenticating the real instead of detecting the fake.
Variation: Industry members tend to favor voluntary adoption with light legal backing; WITNESS and other human rights participants press for opt-in signing, protections for anonymity, and attention to the people and places that provenance will not reach. Some members, including Adobe and Microsoft, have also supported targeted laws on impersonation and nonconsensual imagery.
Answer to objections: To the objection that metadata is easily stripped, this camp answers that durable watermarks now travel with the content alongside the metadata, that stripping is an implementation gap platforms are closing under regulatory pressure, and that the system does not need to catch every fake to work — it needs authentic material from trusted sources to be verifiable, as HTTPS made websites verifiable without eliminating fake ones. To the regulation camp, it answers that labeling fakes asks the least trustworthy actors to label themselves, while provenance asks the trustworthy ones to sign their work. To the demand-side camp, it agrees that technology cannot make people want the truth, but argues that people who do want it currently have no reliable way to check.

Camp: Address the demand for falsehood, not the supply of fakes
Adherents: Knight First Amendment Institute at Columbia University, which published Sayash Kapoor and Arvind Narayanan’s analysis concluding that improving the information environment “depends on structural and institutional changes rather than on curbing AI-generated content” (https://knightcolumbia.org/blog/we-looked-at-78-election-deepfakes-political-misinformation-is-not-an-ai-problem); Felix M. Simon, Sacha Altay and Hugo Mercier, communication and cognitive scientists, who argue that “fears about the impact of generative AI on misinformation are overblown” because misinformation is “mostly limited by demand and not by supply” (Harvard Kennedy School Misinformation Review, 2023, https://misinforeview.hks.harvard.edu/article/misinformation-reloaded-fears-about-the-impact-of-generative-ai-on-misinformation-are-overblown/).
Case: The “epistemic crisis” framing gets the causation backward. People did not stop sharing a common reality because deepfakes arrived; deepfakes find audiences because trust in institutions had already collapsed and politics had already sorted people into hostile camps. Most people consume very little misinformation, the people who consume most of it go looking for it, and they share low-tech falsehoods just as readily as sophisticated fakes — cheap fakes outnumbered AI fakes seven to one in the 2024 U.S. election, and every deceptive AI case studied could have been made for a few hundred dollars without AI. The real constraint on a disinformation campaign is distribution and receptive audiences, not production cost, so cutting production cost changes less than it seems. Treating synthetic media as the cause has its own costs: it licenses speech restrictions that will not work, it hands politicians a ready excuse to dismiss real evidence, and alarm about fakes can itself erode trust in genuine information. The effective work is slower — rebuilding trusted journalism, supporting fact-checkers, teaching verification habits, and addressing the polarization that creates the demand.
Evidence: Of 78 documented AI uses in 2024 elections worldwide, 39 were not deceptive at all. Studies of the 2024 UK, EU, French and U.S. elections found no evidence AI content changed results; viral cases mostly reached people who already agreed. Trust in U.S. media fell from about 70 percent in the 1970s to 28 percent in 2025, long before generative AI. The liar’s dividend experiments found that false claims that real video was a deepfake were largely ineffective, and that false “fake news” claims did not reduce general trust in media.
Variation: Some in this camp reject the crisis framing outright; others, including media literacy organizations such as the News Literacy Project, accept that synthetic media is a real and growing problem but share the view that the lever with the most reach is the audience’s habits and the health of trusted institutions. Most accept targeted laws against concrete harms such as nonconsensual intimate images and fraud, which they distinguish from the shared-truth question.
Answer to objections: To the objection that the 2024 record measured old tools, this camp answers that the demand-side constraints — limited attention, motivated reasoning, the cost of distribution — do not change when the fakes get better, and that past media panics, from Photoshop to “cheap fakes,” predicted collapses that did not come. To the point that nonconsensual imagery and fraud are real harms, it agrees, and notes those harms are personal and criminal rather than a collapse of shared facts, and are best handled by laws aimed at them. To the provenance camp, it answers that a label is only as good as the trust in whoever issues it, and that people who distrust institutions will distrust their credentials too.

Camp: Protect synthetic speech and punish concrete harms
Adherents: Foundation for Individual Rights and Expression (FIRE), which argues that AI parodies of political figures have the same First Amendment protection as political cartoons, that “a mandatory disclaimer for parody or satire would kill the joke,” and that fraud, voter suppression and defamation are already punishable (FIRE, 29 July 2026, https://www.fire.org/news/how-does-first-amendment-apply-deepfakes); Electronic Frontier Foundation (EFF), which opposes the NO FAKES Act because it “targets speech, tools, and innovation instead of focusing on the real concern posed by these replicas: privacy” and would create a takedown regime easy to abuse against commentary and satire (EFF, 9 June 2026, https://www.eff.org/deeplinks/2026/06/tell-congress-just-say-no-no-fakes).
Case: A new medium does not create a new exception to free speech. Altered images of politicians are as old as political cartoons and darkroom retouching, and ridicule of the powerful is the speech the First Amendment protects most. What makes a deepfake wrong is not the technology but a specific harm — fraud, defamation, voter suppression, harassment, sexual exploitation — and the law already punishes those harms whatever tool produced them. Election deepfake laws that single out content “intended to injure” a candidate are viewpoint discrimination by design; mandatory labels kill satire and may lead voters to treat any labeled ad as false; and broad takedown systems for “digital replicas” will be used by the powerful against critics while platforms over-filter to avoid liability. Courts have agreed again and again. Where there is a gap, fill it with narrow, harm-specific law, such as remedies for nonconsensual intimate images, and with privacy protections for ordinary people — not with rules that make the government or platforms the arbiter of which depictions of public figures may circulate.
Evidence: The court record: California’s two election deepfake laws struck down in August 2025 (one as unconstitutional, one as preempted by Section 230), Hawaii’s permanently blocked in January 2026, Montana’s enjoined in September 2026 as likely viewpoint-based. The Hawaii court pointed to digital literacy, counter speech and enforcement of existing defamation and fraud law as less restrictive alternatives. The Biden robocall case was pursued under existing law: the FCC fined the consultant who commissioned the calls $6 million and he faced state criminal charges, though a New Hampshire jury acquitted him in June 2025. The Knight Institute’s finding that deceptive election content is cheap to make without AI suggests AI-specific rules target the tool rather than the conduct.
Variation: FIRE concentrates on election and satire laws; EFF on likeness-rights and takedown regimes, preferring privacy law as the vehicle for protecting individuals. Libertarian scholars make overlapping arguments: the Cato Institute has published commentary warning that state deepfake laws with vague terms, criminal penalties and no exemption for parody threaten free speech (https://www.cato.org/commentary/deepfake-crackdowns-threaten-free-speech).
Answer to objections: To the claim that disclosure is harmless, this camp answers that compelled speech is still a speech burden, that courts have found these particular disclosures overbroad and selective, and that a label requirement enforced by officials in the weeks before an election hands incumbents a weapon. To the regulation camp’s point about nonconsensual imagery and fraud, it agrees those are harms, notes that they are already crimes or torts in most places, and supports narrowly drawn laws aimed at them. To the claim that existing law is too slow for viral fakes, it answers that speed is an argument for counter speech, fact-checking and platform choices, not for prior restraint by the state.

## Crux

The question under the others: is the erosion of shared truth driven mainly by how cheap and convincing fabrication has become, or mainly by distrust and partisan demand that would find falsehood with or without AI? If the supply of synthetic media is the main driver, then marking, provenance, liability and labeling can restore a working baseline of what can be checked, and their costs to speech are a price worth weighing. If demand is the main driver, those measures mostly burden expression and give a false sense of security, and the effort belongs in institutions, journalism and the habits of audiences. Most people on the page agree that nonconsensual imagery and fraud are real harms that warrant targeted law; the disagreement is about whether a society’s capacity to agree on facts is being damaged by the tools themselves.

What evidence could settle: whether exposure to synthetic media changes beliefs and votes beyond what equivalent low-tech misinformation does, measured in field settings rather than labs and in the 2026 cycle rather than 2024; whether the skepticism shift — people rejecting authentic audio and video — keeps growing as generators improve and awareness spreads, and whether it shows up in real disputes over evidence; whether provenance labels, where they actually reach viewers, change what people believe or share; and whether disclosure laws reduce deceptive political content without chilling satire, as the next round of court cases and state experience will show.

What is a value choice: how much risk to political expression, parody and anonymous speech is acceptable in exchange for how much protection against deception; who should be trusted to certify what is authentic — governments, platforms, a consortium of technology companies, or no one; whether the burden of proof should fall on the makers of fakes or on the makers of authentic records; and whether individuals should own their likeness as property or be protected through privacy. No study closes these, because they turn on whose mistakes a society would rather live with: unlabeled fakes that deceive, or rules and credentials that can be misused against legitimate speech.

## Actions

Kind: learn_more
Title: Read the International AI Safety Report 2026
What: The independent, government-backed scientific review led by Yoshua Bengio, with chapters on AI-generated content, manipulation, fraud and nonconsensual imagery and on what the evidence does and does not show.
URL: https://internationalaisafetyreport.org/publication/international-ai-safety-report-2026
Resolved: yes
Serves: neutral

Kind: learn_more
Title: Explore the Reuters Institute Digital News Report 2026
What: The largest annual survey of news use and trust, covering 48 markets, with data on concern about what is real online, trust in news, and use of AI chatbots for news.
URL: https://reutersinstitute.politics.ox.ac.uk/digital-news-report/2026/dnr-executive-summary
Resolved: yes
Serves: neutral

Kind: learn_more
Title: Check an image for Content Credentials
What: A free tool from the Content Authenticity Initiative that reads any provenance record attached to an image or video and shows how it was made and edited.
URL: https://contentcredentials.org/verify
Resolved: yes
Serves: Build provenance that proves what is real

Kind: local
Title: Look up your state’s election deepfake law
What: Public Citizen’s tracker lists which U.S. states regulate deepfakes in elections, what each law requires, and bills pending, so you can see what applies where you vote.
URL: https://www.citizen.org/article/tracker-legislation-on-deepfakes-in-elections/
Resolved: yes
Serves: Require labels and liability for synthetic media

Kind: learn_more
Title: Get a nonconsensual intimate image removed
What: StopNCII.org lets adults create a digital fingerprint of an intimate image on their own device so participating platforms can block it, without the image being uploaded; NCMEC’s Take It Down does the same for images of minors.
URL: https://stopncii.org/
Resolved: yes
Serves: neutral

Kind: policy
Title: Follow the NO FAKES Act in the Senate
What: The bipartisan bill, advanced by the Senate Judiciary Committee in June 2026, would create a federal right in one’s voice and visual likeness with a notice-and-removal system; GovTrack shows its text, status and sponsors so you can contact your senators.
URL: https://www.govtrack.us/congress/bills/119/s4591
Resolved: yes
Serves: Require labels and liability for synthetic media

Kind: policy
Title: Join EFF’s campaign against NO FAKES
What: The Electronic Frontier Foundation’s explainer and action asking Congress to reject the NO FAKES Act in favor of privacy-based protections it argues would not chill speech.
URL: https://www.eff.org/deeplinks/2026/06/tell-congress-just-say-no-no-fakes
Resolved: yes
Serves: Protect synthetic speech and punish concrete harms

Kind: learn_more
Title: Read “We Looked at 78 Election Deepfakes”
What: Sayash Kapoor and Arvind Narayanan’s analysis for the Knight First Amendment Institute arguing that political misinformation is a demand problem, not an AI problem.
URL: https://knightcolumbia.org/blog/we-looked-at-78-election-deepfakes-political-misinformation-is-not-an-ai-problem
Resolved: yes
Serves: Address the demand for falsehood, not the supply of fakes

Kind: volunteer
Title: Practice verification with RumorGuard
What: The News Literacy Project’s free site that walks through viral claims and images, including AI fakes, and teaches the checks that work on any of them.
URL: https://www.rumorguard.org/
Resolved: yes
Serves: Address the demand for falsehood, not the supply of fakes

Kind: learn_more
Title: Use WITNESS’s guidance on AI and video evidence
What: Resources from the human rights video organization on provenance, detection access and responding to both deepfakes and false claims that real footage is fake.
URL: https://www.gen-ai.witness.org/
Resolved: yes
Serves: Build provenance that proves what is real

Kind: donate
Title: Support Public Citizen’s democracy work
What: The consumer advocacy group that drafts model election deepfake legislation, tracks state laws and petitions federal regulators for rules on AI in political ads.
URL: https://www.citizen.org/donate/
Resolved: yes
Serves: Require labels and liability for synthetic media

Kind: donate
Title: Support FIRE
What: The free speech organization that litigates and campaigns against laws it considers unconstitutional restrictions on political speech and satire, including election deepfake laws.
URL: https://www.fire.org/donate
Resolved: yes
Serves: Protect synthetic speech and punish concrete harms

## Sources

European Commission, Code of Practice on Transparency of AI-generated Content — https://digital-strategy.ec.europa.eu/en/policies/code-practice-ai-generated-content — accessed 2026-10-02
Paul, Weiss, EU Finalises Transparency Rules for AI-Generated Content (dates of Article 50 deferrals) — https://www.paulweiss.com/insights/client-memos/eu-finalises-transparency-rules-for-ai-generated-content — accessed 2026-10-02
Wesleyan Media Project, At Least $80 Million Spent on AI Ads This Cycle, 4 September 2026 — https://mediaproject.wesleyan.edu/releases-090426/ — accessed 2026-10-02
Daily Montanan, Federal judge says AI deepfake election law violates First Amendment, 18 September 2026 — https://dailymontanan.com/2026/09/18/federal-judge-says-ai-deepfake-election-law-violates-first-amendment/ — accessed 2026-10-02
Georgetown Free Speech Project, Federal judge strikes down California law targeting misinformation (Kohls v. Bonta) — https://freespeechproject.georgetown.edu/tracker-entries/federal-judge-strikes-down-california-law-targeting-misinformation/ — accessed 2026-10-02
Courthouse News, Hawaii’s deepfake law struck down over free speech concerns (30 January 2026) — https://courthousenews.com/hawaiis-deepfake-law-struck-down-over-free-speech-concerns/ — accessed 2026-10-02
Diel et al., Human performance in detecting deepfakes: A systematic review and meta-analysis of 56 papers, Computers in Human Behavior Reports, 2024 — https://doi.org/10.1016/j.chbr.2024.100538 — accessed 2026-10-02
Müller & Choong, Eroding Trust in Real Speech, arXiv:2605.26136 (preprint) — https://arxiv.org/abs/2605.26136 — accessed 2026-10-02
Reuters Institute, Digital News Report 2026, executive summary — https://reutersinstitute.politics.ox.ac.uk/digital-news-report/2026/dnr-executive-summary — accessed 2026-10-02
Schiff, Jackson Schiff & Bueno, The Liar’s Dividend, American Political Science Review, 2025 — https://doi.org/10.1017/S0003055423001454 — accessed 2026-10-02
Kapoor & Narayanan, We Looked at 78 Election Deepfakes, Knight First Amendment Institute, 13 December 2024 — https://knightcolumbia.org/blog/we-looked-at-78-election-deepfakes-political-misinformation-is-not-an-ai-problem — accessed 2026-10-02
Alan Turing Institute CETaS, AI-Enabled Influence Operations: Threat Analysis of the 2024 UK and European Elections (page blocks automated retrieval; figures from the institute’s published summary) — https://cetas.turing.ac.uk/publications/ai-enabled-influence-operations-threat-analysis-2024-uk-and-european-elections — accessed 2026-10-02
Public Citizen, 30 States Now Have Laws to Regulate Election Deepfakes, 13 May 2026 — https://www.citizen.org/news/30-states-now-have-laws-to-regulate-election-deepfakes/ — accessed 2026-10-02
Public Citizen, Tracker: State Legislation on Deepfakes in Elections — https://www.citizen.org/article/tracker-legislation-on-deepfakes-in-elections/ — accessed 2026-10-02
Chandra et al., Deepfake-Eval-2024, arXiv:2503.02857 — https://arxiv.org/abs/2503.02857 — accessed 2026-10-02
The Washington Post, Tests show top social platforms don’t disclose markers on AI videos, 22 October 2025 (paywalled; finding read from the article’s published summary) — https://www.washingtonpost.com/technology/2025/10/22/ai-deepfake-sora-platforms-c2pa/ — accessed 2026-10-02
Google, SynthID Detector announcement, 20 May 2025 — https://blog.google/innovation-and-ai/products/google-synthid-ai-content-detector/ — accessed 2026-10-02
C2PA, C2PA Welcomes TikTok to Steering Committee, 28 July 2026 — https://www.prnewswire.com/news-releases/c2pa-welcomes-tiktok-to-steering-committee-advancing-the-adoption-of-content-credentials-at-a-global-scale-302836730.html — accessed 2026-10-02
Pew Research Center, How Americans View AI and Its Impact on People and Society, 17 September 2025 — https://www.pewresearch.org/science/2025/09/17/how-americans-view-ai-and-its-impact-on-people-and-society/ — accessed 2026-10-02
Nightingale & Farid, AI-synthesized faces are indistinguishable from real faces and more trustworthy, PNAS, 2022 — https://pmc.ncbi.nlm.nih.gov/articles/PMC8872790/ — accessed 2026-10-02
Gallup, Trust in Media at New Low of 28% in U.S., 2 October 2025 — https://news.gallup.com/poll/695762/trust-media-new-low.aspx — accessed 2026-10-02
Center for Countering Digital Hate, Grok floods X with sexualized images of women and children, 22 January 2026 — https://counterhate.com/research/grok-floods-x-with-sexualized-images/ — accessed 2026-10-02
Ofcom, Ofcom launches investigation into X over Grok sexualised imagery — https://www.ofcom.org.uk/online-safety/illegal-and-harmful-content/ofcom-launches-investigation-into-x-over-grok-sexualised-imagery — accessed 2026-10-02
NBC News, International pressure builds on X and Musk over Grok deepfakes of women and children — https://www.nbcnews.com/tech/tech-news/international-pressure-builds-x-musk-grok-deepfakes-rcna253639 — accessed 2026-10-02
Han, Li, Kumar & Durumeric, Characterizing the MrDeepFakes Sexual Deepfake Marketplace, USENIX Security 2025 — https://www.usenix.org/system/files/usenixsecurity25-han.pdf — accessed 2026-10-02
Federal Trade Commission, FTC Begins Enforcing the TAKE IT DOWN Act, May 2026 — https://www.ftc.gov/news-events/news/press-releases/2026/05/ftc-begins-enforcing-take-it-down-act — accessed 2026-10-02
The Guardian, UK engineering firm Arup falls victim to £20m deepfake scam, 17 May 2024 — https://www.theguardian.com/technology/article/2024/may/17/uk-engineering-arup-deepfake-scam-hong-kong-ai-video — accessed 2026-10-02
Deloitte Center for Financial Services, Generative AI is expected to magnify the risk of deepfakes and other fraud in banking, 29 May 2024 — https://www.deloitte.com/us/en/insights/industry/financial-services/deepfake-banking-fraud-risk-on-the-rise.html — accessed 2026-10-02
NewsGuard, Real-time AI Content Farm Detection Datastream, 12 March 2026 — https://www.newsguardtech.com/press/newsguard-launches-real-time-ai-content-farm-detection-datastream-to-counter-onslaught-of-ai-slop-in-news/ — accessed 2026-10-02
NewsGuard, One-Year AI Audit Progress Report, 4 September 2025 — https://www.newsguardtech.com/press/newsguard-one-year-ai-audit-progress-report-finds-that-ai-models-spread-falsehoods-in-the-news-35-of-the-time/ — accessed 2026-10-02
World Economic Forum, Global Risks Report 2026 (PDF) — https://reports.weforum.org/docs/WEF_Global_Risks_Report_2026.pdf — accessed 2026-10-02
Scientific American, Deepfakes are getting faster than fact-checks, says digital forensics expert Hany Farid, 17 February 2026 — https://www.scientificamerican.com/article/deepfakes-are-getting-faster-than-fact-checks-says-digital-forensics-expert/ — accessed 2026-10-02
DPReview, Adobe Content Credentials check-in (interview with Andy Parsons) — https://www.dpreview.com/interviews/3215783269/adobe-max-2024-content-credentials-authenticity-initiative/ — accessed 2026-10-02
WITNESS, Generative AI and deepfakes program — https://www.gen-ai.witness.org/ — accessed 2026-10-02
Simon, Altay & Mercier, Misinformation reloaded? Fears about the impact of generative AI on misinformation are overblown, HKS Misinformation Review, 2023 — https://misinforeview.hks.harvard.edu/article/misinformation-reloaded-fears-about-the-impact-of-generative-ai-on-misinformation-are-overblown/ — accessed 2026-10-02
FIRE, How does the First Amendment apply to “deepfakes”?, 29 July 2026 — https://www.fire.org/news/how-does-first-amendment-apply-deepfakes — accessed 2026-10-02
EFF, Tell Congress: Just Say No to NO FAKES, 9 June 2026 — https://www.eff.org/deeplinks/2026/06/tell-congress-just-say-no-no-fakes — accessed 2026-10-02
Cato Institute, Deepfake Crackdowns Threaten Free Speech (blocks automated retrieval; characterized from search excerpt) — https://www.cato.org/commentary/deepfake-crackdowns-threaten-free-speech — accessed 2026-10-02
NHPR, Political operative who admitted to creating fake Biden robocalls found not guilty, 13 June 2025 — https://www.nhpr.org/nh-news/2025-06-13/political-operative-fake-biden-robocalls-nh-primary-found-not-guilty — accessed 2026-10-02
European Parliamentary Research Service, The Danish approach to copyright and deepfakes, January 2026 — https://www.europarl.europa.eu/RegData/etudes/ATAG/2026/782611/EPRS_ATA(2026)782611_EN.pdf — accessed 2026-10-02
GovTrack, S. 4591 NO FAKES Act of 2026 — https://www.govtrack.us/congress/bills/119/s4591 — accessed 2026-10-02
International AI Safety Report 2026 — https://internationalaisafetyreport.org/publication/international-ai-safety-report-2026 — accessed 2026-10-02
Content Credentials Verify — https://contentcredentials.org/verify — accessed 2026-10-02
StopNCII.org — https://stopncii.org/ — accessed 2026-10-02
NCMEC Take It Down — https://takeitdown.ncmec.org/ — accessed 2026-10-02
News Literacy Project, RumorGuard — https://www.rumorguard.org/ — accessed 2026-10-02
Public Citizen, Donate — https://www.citizen.org/donate/ — accessed 2026-10-02
FIRE, Donate — https://www.fire.org/donate — accessed 2026-10-02
