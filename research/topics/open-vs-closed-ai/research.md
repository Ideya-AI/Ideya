# Open vs. Closed AI — research

## Overview

This topic covers the release decision itself: whether the developers of capable AI models should publish the trained weights so anyone can download, run, modify and redistribute the model, or keep the weights on their own servers and offer the model only through a controlled interface (an app or an API) that they can monitor, restrict, update and withdraw. It includes the range between those poles: open weights under restrictive licenses, staged release, vetted researcher access, releasing smaller models openly while keeping the flagship closed, and the fuller “open source” that also publishes training data and code. It covers the arguments that drive the choice: misuse and the ease of stripping safeguards, irreversibility, cyber offense and defense, whether withholding weights slows rivals or merely cedes the field, concentration of power, transparency and research access, and dependence on a few vendors. It deliberately excludes government regulation of AI as such (licensing, mandatory testing, preemption, liability), which belongs to Frontier AI Regulation; export controls and proposed bans on using Chinese models appear only where they bear on what developers release. Technical alignment methods belong to AI Alignment and rules for agents to Governing Autonomous Agents.

Why now: on 4 November 2026 Moonshot AI published the full weights of Kimi K3.1 Pro on Hugging Face, a 2.8-trillion-parameter mixture-of-experts model with about 104 billion parameters active per token (TechNode, 5 November 2026, https://technode.com/2026/11/05/moonshot-ai-releases-kimi-k3-1-pro-model-weights/); it tops the open-weight list on Artificial Analysis’s Intelligence Index (https://artificialanalysis.ai/models/open-source). It came three weeks after two other release-policy moves. On 15 October 2026 Meta, whose first Muse Spark model in April had been its first frontier model without open weights, released the weights of Muse Spark Open (816 billion parameters, 42 billion active) under a custom license, saying “We’re sharing this work because we want everyone to have access to the best models” (Meta, https://research.meta.ai/blog/muse-spark-open), while its more capable Muse Wonder stays closed (Implicator, https://www.implicator.ai/meta-releases-muse-spark-open-an-816b-model-that-trails-chinese-rivals-at-coding/). On 16 October China’s commerce and science ministries proposed export controls covering large models with at least 2 trillion parameters or a global top-10 ranking, under which already-public open weights are exempt and open-sourcing a restricted model would get an automatic license (The Next Web, https://thenextweb.com/news/china-ai-export-controls-draft; ChinaTalk, https://www.chinatalk.media/p/mofcoms-new-ai-rules). Suggested one-source why_now: “On November 4, 2026, Moonshot AI published the weights of Kimi K3.1 Pro, a 2.8-trillion-parameter model and the most capable open-weight release to date, weeks after Meta released an open version of its Muse Spark model and kept its most capable model closed.” If the editor wants a single source for every clause, the TechNode piece supports the Kimi date and size only; the Meta clause needs the Meta blog.

The debate is live because the gap has narrowed while the evidence of misuse potential has sharpened. Epoch AI estimates the best open-weight models have trailed the closed frontier by about four months on average in 2026 (https://epoch.ai/data-insights/open-closed-eci-gap), and the leading open models are now Chinese, which has turned a safety argument into a geopolitical one. In July 2026 more than 270 companies and organizations, led by Microsoft and Nvidia and later joined by OpenAI and Google, signed “Open Weights and American AI Leadership,” arguing “the right response to this risk is not to prohibit open weights” (https://www.microsoft.com/en-us/corporate-responsibility/topics/open-weight/); Anthropic answered that it has never called for a ban but that open-weight models carry higher risk and that all sufficiently capable models should be tested (https://www.anthropic.com/news/position-open-weights-models). Since then Anthropic’s red team reported that GLM-5.3 was released “without meaningful safeguards” and that simple techniques got it to engage with overtly harmful cyber requests up to 100 percent of the time (https://www.anthropic.com/research/glm-5-3-and-the-spread-of-advanced-cyber-capabilities), and Epoch AI used the same open model to turn public Firefox security fixes into working exploits for about 1,000 dollars per release (https://epoch.ai/publications/open-weight-models-patch-gap). On the other side, the June 2026 US directive that forced Anthropic to switch off two of its models for every customer at a few hours’ notice became the open camp’s favorite example of what dependence on a closed provider means (Al Jazeera, https://www.aljazeera.com/economy/2026/6/14/us-orders-anthropic-to-disable-ai-models-for-all-foreign-nationals). The participants are the frontier labs (which mostly keep their best models closed and release smaller ones), Meta, Nvidia (which agreed in September 2026 to buy Hugging Face for about 12.9 billion dollars, https://semafor.com/article/09/03/2026/nvidia-to-buy-hugging-face-for-nearly-13-billion), Chinese labs that release their flagships openly, cloud and enterprise buyers, safety researchers and evaluators, security researchers, academics who need weights to do science, open-source and public-interest groups, and governments in Washington and Beijing that each treat open models as strategic.

## Basics

Label: How far the best open-weight models trail the closed frontier
Value: 4
Unit: months (average lag, general capability)
Viz: bar
Data year: 2026
Source label: Epoch AI, Open models lag state-of-the-art closed models by 4 months, Data Insight, 29 May 2026
Source URL: https://epoch.ai/data-insights/open-closed-eci-gap
Note: Since January 2026, the most capable open-weight models have matched closed frontier models from about four months earlier, an average gap of 8 points on Epoch’s Capabilities Index.
Context: Epoch says the 8-point gap is similar to the gap between GPT-5 and GPT-5.5. Its earlier analysis, covering January 2023 to October 2025, put the average lag at about three months (Epoch AI topic page, https://epoch.ai/topics/open-models), and a November 2024 Epoch report had put it at “about one year,” with a range of 5 to 22 months across benchmarks (https://epoch.ai/blog/open-models-report), so the lag has shrunk from about a year to a season. The figure is an average across model pairs with wide, often overlapping confidence intervals, and some recent open releases lacked enough benchmark results to be scored. The lag is the single most cited number in the debate because both sides use it: those who favor open release say a few months of delay makes withholding US weights pointless, and those who favor keeping the frontier closed say a few months is exactly the window defenders need.

Label: Open-weight share of AI tokens versus closed-model share of spending on OpenRouter
Value: 73
Unit: percent of spending going to closed-weight models (second week of September 2026)
Viz: ranked
Series: Open-weight share of tokens, peak in early July 2026 79; Chinese labs’ share of tokens, week of 14 September 2026 69; Open-weight share of tokens, floor since July 2026 62; Closed-weight share of spending, week of 5 January 2026 89; Closed-weight share of spending, second week of September 2026 73 (highlight)
Data year: 2026
Source label: OpenRouter, The Token State of Play (Inferred newsletter), 22 September 2026
Source URL: https://openrouter.ai/data/newsletter/the-token-state-of-play
Note: On OpenRouter, open-weight models have processed more than 62 percent of tokens every week since July 2026, peaking at 79 percent, while closed models still took 73 percent of the money spent in mid-September.
Context: The two halves tell different stories: open models win on volume because they are far cheaper per token, and closed models win on revenue because the most demanding work still goes to them. The 62 percent row is a floor (“has held above 62% since”), not a weekly value. OpenRouter is a marketplace that routes requests among many providers and handles only a small slice of global AI traffic; its users choose it precisely to switch between models, so it overstates open-model use relative to the whole market, and the figures exclude resellers. A 2025 study by Frank Nagle and Daniel Yue of the same platform found closed models then took close to 80 percent of tokens and nearly 96 percent of revenue between May and September 2025 (Linux Foundation, https://www.linuxfoundation.org/blog/revealing-the-hidden-economics-of-open-models-in-the-ai-era), which shows how fast the volume side has moved.

Label: Chinese-developed models’ share of open-model downloads on Hugging Face
Value: 41
Unit: percent of downloads, past year (2025 into early 2026)
Viz: radial
Data year: 2025
Source label: Hugging Face, State of Open Source on Hugging Face: Spring 2026, 17 March 2026
Source URL: https://huggingface.co/blog/huggingface/state-of-os-hf-spring-2026
Note: Chinese models accounted for a plurality, 41 percent, of downloads on Hugging Face over the past year, and China has passed the United States in both monthly and overall downloads.
Context: The report attributes the shift to Alibaba’s Qwen family above all; Alibaba alone has more derivative models than Google and Meta combined, and Hugging Face’s Summer 2026 report counts 151,448 Qwen derivative repositories on the Hub, 4.7 times the number of Llama repositories (https://huggingface.co/blog/state-of-open-models-summer-2026). The Spring report also found independent developers’ share of downloads rose from 17 to 39 percent while industry’s fell from about 70 percent before 2022 to about 37 percent in 2025. Coverage of the report gives the US share as 36.5 percent, but the Hugging Face page itself does not state it [US share unverified on the primary]. This is the number behind the American argument that the country is losing the open ecosystem to China: the 2025 US AI Action Plan says “We need to ensure America has leading open models founded on American values” (https://www.whitehouse.gov/wp-content/uploads/2025/07/Americas-AI-Action-Plan.pdf).

Label: How often an open-weight model’s safeguards were bypassed on harmful cyber requests
Value: 100
Unit: percent of overtly harmful cyber requests the model engaged with (after abliteration)
Viz: ranked
Series: GLM-5.3 after abliteration (refusal removed from the weights) 100 (highlight); GLM-5.3 with prefilled reasoning 92; GLM-5.3 with a cover story 64; Safeguarded Claude models, same tests 0
Data year: 2026
Source label: Anthropic Frontier Red Team, GLM-5.3 and the spread of advanced cyber capabilities, 29 September 2026
Source URL: https://www.anthropic.com/research/glm-5-3-and-the-spread-of-advanced-cyber-capabilities
Note: Anthropic found simple techniques got Z.ai’s open-weight GLM-5.3 to engage with overtly harmful cyber requests 64 to 100 percent of the time; its safeguarded Claude models engaged 0 percent of the time in the same tests.
Context: Anthropic says GLM-5.3 “is unlike other frontier models in that it has been released without meaningful safeguards to limit misuse” and that “a critical threshold in freely accessible capabilities has now been crossed.” On ExploitBench (410 attempts on Chrome V8 bugs) GLM-5.3 produced 50 end-to-end exploits against 56 for Claude Mythos Preview; on Anthropic’s internal binary exploitation benchmark it achieved full control-flow hijacks in 4 percent of 100 tasks, against 6 percent for Mythos Preview and none for Claude Opus 4.6 or GLM-5.2. The comparison is between a downloadable model and API-served models that sit behind monitoring and classifiers; the Claude results reflect those system safeguards, not only the model. Anthropic is a competitor of Z.ai and a party to the open-weights dispute, which supporters of open release point out; the report cites NIST’s CAISI as independently finding GLM-5.3 the most cyber-capable open-weight model to date, about four months behind the US frontier.

Label: Firefox releases an open-weight model turned into working exploits from public fixes
Value: 6
Unit: Firefox releases (156.0 to 158.0.1)
Viz: bar
Data year: 2026
Source label: Epoch AI, AI can turn security fixes into working exploits before users receive an update, 29 October 2026
Source URL: https://epoch.ai/publications/open-weight-models-patch-gap
Note: Epoch researchers used Z.ai’s open-weight GLM 5.3 to build working one-click exploits for six Firefox releases from security fixes that were public before users got the update, at about 1,000 dollars in API cost per release.
Context: The releases came out between 17 September and 26 October 2026; the fastest successful attempt took 12 hours, and total research spending exceeded 100,000 dollars. The authors write: “Our central finding is that widely available open-weight models can now do much, or even all, of this work on their own,” and report that they “did not trigger any safeguards or refusals from any provider, including Z.ai.” The model was used through Z.ai’s and third-party APIs in an offline sandbox, not self-hosted. The exploits chained the patch gap with a separate unpublished flaw and achieved file reads, not arbitrary code execution; attacks on Chrome had not succeeded after about 100,000 dollars of spending. Mozilla patched the flaw in Firefox 159.0 on 27 October. The authors’ suggested fixes are on the software side (keep fixes private until release, ship faster), which is part of the open camp’s argument that the answer to cheap offense is faster defense.

Label: How far an open-weight model got through a simulated 32-step network attack
Value: 17
Unit: steps reached on average, of 32 (Kimi K3)
Viz: ranked
Series: Most cyber-capable US closed models 28.5; Kimi K3 17 (highlight); GLM-5.2 11
Data year: 2026
Source label: UK AI Security Institute and NIST CAISI, Preliminary assessment of Kimi K3’s cyber capabilities, 23 July 2026 (updated 28 August 2026)
Source URL: https://www.nist.gov/news-events/news/2026/07/uk-aisi-caisi-preliminary-assessment-kimi-k3s-cyber-capabilities
Note: On the “The Last Ones” cyber range, Moonshot’s open-weight Kimi K3 reached step 17 of 32 on average and solved it once in 10 attempts; the most capable US closed models reached 28.5 steps and had solved it 6 and 7 times in 10.
Context: On ExploitBench’s 41 tasks Kimi K3 scored 32 percent against 24 percent for GLM-5.2, and achieved arbitrary code execution on none of 41 samples, against an average of 20 of 41 for the most cyber-capable models. The evaluators found “Kimi K3’s safeguards did not prevent it from attempting cyber exploit development or offensive cyber operations.” The US closed models were tested with their system-level safeguards disabled, while the public versions keep them on; the assessment is labeled preliminary and rests on a small set of benchmarks. Kimi K3 was released on 16 July and its weights posted on 27 July 2026. Both camps cite the result: as proof the capability gap is real and worth keeping, and as proof that the safeguard gap is the larger problem.

Label: How far open-weight models trail the closed frontier on cyber capabilities
Value: 6–7
Unit: months
Viz: bar
Data year: 2026
Source label: Epoch AI, Open-weight models trail closed models in cyber capabilities by 6–7 months, Data Insight, 16 October 2026
Source URL: https://epoch.ai/data-insights/open-closed-cyber-eci-gap
Note: Z.ai’s GLM-5.3, the top open-weight model on Epoch’s Cyber Capabilities Index, scores where the closed frontier stood 6 to 7 months earlier.
Context: GLM-5.3 scores about 160 on the Cyber ECI, above GPT-5.4 (March 2026) and below Claude Mythos Preview (April 2026); Claude Opus 5.5 and GPT-6 Astra score about 171. GLM-5.3’s score rests on three CAISI benchmark results, and Epoch had to infer which US models CAISI tested. The UK AI Security Institute, measuring separately in July 2026, found open models GLM-5.2 and DeepSeek V4-Pro performed like closed models released 4 to 7 months earlier, narrower than the 6 to 10 months it measured in 2025, and concluded: “This implies cyber defenders have a short window to prepare before today’s frontier cyber capabilities may become accessible without the same safeguards” (https://www.aisi.gov.uk/work/how-far-behind-the-frontier-are-leading-open-weight-models-on-cyber). AISI also found the open models far cheaper per task: 6.12 dollars for GLM-5.2 against 15.17 for Claude Opus 4.6 on tasks both solved every time.

Label: Cost to remove safety training from an open-weight model
Value: 1,200
Unit: US dollars (estimated, about 600 GPU hours, experienced team, GLM-5.3)
Viz: ranked
Series: Llama 2-Chat 13B, full safety removal by fine-tuning (2023) under 200; GLM-5.3 abliteration, experienced team starting fresh (2026 estimate) 1,200 (highlight); GLM-5.3 abliteration, Anthropic’s actual spend including exploration (2026) 4,400
Data year: 2026
Source label: Anthropic Frontier Red Team, GLM-5.3 and the spread of advanced cyber capabilities, 29 September 2026; Gade, Lermen, Rogers-Smith and Ladish, BadLlama, arXiv:2311.00117 (Llama 2 row)
Source URL: https://www.anthropic.com/research/glm-5-3-and-the-spread-of-advanced-cyber-capabilities
Note: Anthropic estimates an experienced team could strip GLM-5.3’s refusals in about 600 GPU hours, roughly 1,200 dollars, cutting refusal rates from above 90 percent to between 2 and 12 percent with little loss of capability.
Context: The rows come from different studies and models: the Llama 2 figure is from BadLlama (2023, https://arxiv.org/abs/2311.00117), which removed safety fine-tuning from Llama 2-Chat 13B for under 200 dollars; a 2024 follow-up did the same to Llama 3 8B in minutes on one GPU (Volkov, https://arxiv.org/abs/2407.01376). Anthropic’s own team spent about 2,200 GPU hours, roughly 4,400 dollars, mostly on exploration. The point that matters for release policy is not the exact price but the ratio: removing a safeguard costs a tiny fraction of training the model, so for a downloadable model, safety training is a default the user can undo. The 2026 International AI Safety Report makes the same point, that open-weight models cannot be recalled and their safeguards are easier to remove (https://internationalaisafetyreport.org/). Those who favor open release reply that closed models also leak capability through jailbreaks, distillation and fine-tuning APIs, and that the relevant question is marginal risk.

Label: Claude exchanges Anthropic attributed to distillation by three Chinese labs
Value: 16
Unit: million exchanges (through about 24,000 fraudulent accounts)
Viz: ranked
Series: MiniMax 13 (highlight); Moonshot AI 3.4; DeepSeek 0.15
Data year: 2026
Source label: Anthropic, Detecting and preventing distillation attacks, 23 February 2026
Source URL: https://anthropic.com/news/detecting-and-preventing-distillation-attacks
Note: Anthropic says DeepSeek, Moonshot and MiniMax generated more than 16 million exchanges with Claude through about 24,000 fraudulent accounts to train their own models on its outputs.
Context: Series values are “over” figures in millions: MiniMax over 13 million, Moonshot over 3.4 million, DeepSeek over 150,000. Anthropic argues “Illicitly distilled models lack necessary safeguards” and “If distilled models are open-sourced, this risk multiplies.” The figures and attributions are Anthropic’s own; the three labs had not responded when NBC News reported them, and no independent verification was found. In a 10 June 2026 letter to Senators Tim Scott and Elizabeth Warren, Anthropic alleged a further campaign by operators connected to Alibaba’s Qwen lab of about 25,000 accounts and more than 28.8 million exchanges, which Alibaba disputes (as reported by the Cloud Security Alliance, https://labs.cloudsecurityalliance.org/research/csa-research-note-open-weight-concentration-risk-rift-202608/) [Alibaba figures secondary]. Distillation cuts both ways in this debate: it suggests keeping weights closed does not stop capability from leaking, and it suggests some open models owe their capability to closed ones.

Label: Signers of the “Open Weights and American AI Leadership” letter
Value: 270
Unit: companies and organizations (more than, as of 3 August 2026)
Viz: bar
Data year: 2026
Source label: Microsoft, Open Weights and American AI Leadership (letter dated 24 July 2026)
Source URL: https://www.microsoft.com/en-us/corporate-responsibility/topics/open-weight/
Note: More than 270 companies and organizations had signed the July 2026 letter defending open-weight models by 3 August 2026.
Context: The letter launched with about 25 signers, among them Nvidia, Microsoft, Meta, Mistral, Palantir, IBM, Andreessen Horowitz, Hugging Face, Mozilla and the Linux Foundation (The Next Web, https://thenextweb.com/news/open-weights-american-ai-leadership-letter-huang-nvidia-openai-absent); OpenAI and Google added their names afterward (eWeek, https://www.eweek.com/news/nvidia-microsoft-open-weight-ai-letter/), and Anthropic did not sign. It concedes “Once released, the weights are beyond the original developer’s control” but argues “the right response to this risk is not to prohibit open weights” and that “defenders need access to models with comparable capabilities.” It came a week after Axios reported the administration was weighing steps against Chinese open models after the Kimi K3 release (https://axios.com/2026/07/20/ai-us-china-open-source-kimi). Several signers keep their own most capable models closed, so signing marks opposition to restricting open release, not a commitment to release.

Label: Share of Hugging Face downloads by model size
Value: 83
Unit: percent of all-time downloads going to models under 1 billion parameters
Viz: ranked
Series: Models under 1 billion parameters 83 (highlight); Models above 100 billion parameters 1
Data year: 2026
Source label: Hugging Face, State of Open Models: Summer 2026 (January to August 2026)
Source URL: https://huggingface.co/blog/state-of-open-models-summer-2026
Note: Among models that declare a parameter count, those under 1 billion parameters account for 83 percent of all-time Hugging Face downloads; those above 100 billion account for 1 percent.
Context: Most open-model use is small models embedded in products, search, speech and classification, far from the frontier-scale models the safety argument is about; the most downloaded single model in the report is a sentence-embedding model, all-MiniLM-L6-v2, at 1.55 billion downloads in seven months. Large models are concentrated among a few labs: 88 percent of Moonshot’s 2026 downloads are of models above 70 billion parameters. Downloads overall are highly concentrated: “1.5% of repositories account for 99.2% of all downloads,” and about 85.6 percent of models have fewer than 200 lifetime downloads. Those who favor open release read the size split as evidence that restrictions aimed at frontier models would barely touch the bulk of open use; those who want the frontier closed read it the same way, as evidence that a narrow rule would not harm the ecosystem.

Label: Public model repositories on Hugging Face
Value: 2.96
Unit: million (August 2026)
Viz: ranked
Series: January 2026 2.43; August 2026 2.96 (highlight)
Data year: 2026
Source label: Hugging Face, State of Open Models: Summer 2026
Source URL: https://huggingface.co/blog/state-of-open-models-summer-2026
Note: Public model repositories on Hugging Face grew from 2.43 million to 2.96 million between January and August 2026.
Context: The count includes fine-tunes, quantized copies and experiments, not three million distinct base models; the Qwen family alone has 151,448 derivatives. Hugging Face is the main distribution point for open weights, and in September 2026 Nvidia agreed to buy it for about 12.9 billion dollars, with Jensen Huang writing that it “will remain an open platform for the entire AI ecosystem” (Semafor, https://semafor.com/article/09/03/2026/nvidia-to-buy-hugging-face-for-nearly-13-billion). Coverage reported the public count passing 3 million in late August 2026 [secondary; the report’s own figure is 2.96 million].

Label: Transparency scores of AI developers, 2025 Foundation Model Transparency Index
Value: 41
Unit: average score out of 100 (13 developers)
Viz: ranked
Series: IBM 95; Average of 13 developers 41 (highlight); DeepSeek 32; Alibaba 26; xAI 14; Midjourney 14
Data year: 2025
Source label: Stanford CRFM, The 2025 Foundation Model Transparency Index, December 2025
Source URL: https://crfm.stanford.edu/fmti/December-2025
Note: The average transparency score across 13 developers was 41 of 100; the index found “The 5 open-weight developers outscore the 8 closed-weight developers overall and on every domain.”
Context: The index scores what developers disclose about data, compute, risks, access and downstream use. Open release correlates with transparency as a group, but not reliably: IBM set the highest score in the index’s history at 95 while DeepSeek, also an open-weight developer, scored 32, and Stanford HAI’s coverage says major open developers such as DeepSeek and Meta are quite opaque. Meta’s score fell 29 points from 2024, and the overall average fell sharply. The page gives scores for only five companies; the others are reported as changes. This is the evidence behind both the claim that openness enables scrutiny and the reply that releasing weights is not the same as disclosing how a model was made.

Label: Size of the largest open-weight releases against China’s proposed export-control trigger
Value: 2,800
Unit: billion parameters (Kimi K3.1 Pro)
Viz: ranked
Series: Moonshot Kimi K3.1 Pro (weights released 4 November 2026) 2,800 (highlight); China’s draft export-control trigger for large models 2,000; Meta Muse Spark Open (weights released 15 October 2026) 816
Data year: 2026
Source label: TechNode on Kimi K3.1 Pro, 5 November 2026; The Next Web on China’s draft controls, 16 October 2026; Meta on Muse Spark Open, 15 October 2026
Source URL: https://technode.com/2026/11/05/moonshot-ai-releases-kimi-k3-1-pro-model-weights/
Note: Kimi K3.1 Pro, 2.8 trillion parameters, was released openly weeks after Beijing proposed controls on models of 2 trillion parameters or more; Meta’s largest open release, Muse Spark Open, has 816 billion.
Context: Rows come from three sources: the Kimi figure from TechNode, the 2,000 trigger from The Next Web (https://thenextweb.com/news/china-ai-export-controls-draft), and Muse Spark Open from Meta (https://research.meta.ai/blog/muse-spark-open). These are mixture-of-experts models, so far fewer parameters are active per token (about 104 billion for Kimi K3.1 Pro, 42 billion for Muse Spark Open). The Chinese draft, open for comment until 15 November 2026, also triggers on 10^26 operations of training compute or a top-10 global ranking; per MOFCOM’s Q&A as reported by ChinaTalk, already-public open weights are excluded and open-sourcing a restricted model counts as an export that receives an automatic license (https://www.chinatalk.media/p/mofcoms-new-ai-rules). Running the full Kimi model takes a server cluster, not a laptop: the Cloud Security Alliance estimated about 64 high-end GPUs across eight servers for Kimi K3. Both licenses are custom. Under Meta’s Muse Model License, companies with more than 20 million dollars in revenue must notify Meta and sign a separate agreement before offering the model as a hosted service, and military and critical-infrastructure uses are barred (Implicator); Moonshot’s license is reported to carry a similar 20-million-dollar threshold for hosted services [Kimi license term secondary, unverified on the model card].

Label: Estimated annual savings if AI users shifted to open models
Value: 24.8
Unit: billion US dollars per year (2025 estimate)
Viz: bar
Data year: 2025
Source label: Linux Foundation, Revealing the Hidden Economics of Open Models in the AI Era (Nagle and Yue, The Latent Role of Open Models in the AI Economy)
Source URL: https://www.linuxfoundation.org/blog/revealing-the-hidden-economics-of-open-models-in-the-ai-era
Note: Frank Nagle and Daniel Yue estimated users would save about 24.8 billion dollars a year, within a range of 20 to 48 billion, if they picked models purely on price and performance, because open models are much cheaper for similar benchmark results.
Context: The authors tracked OpenRouter usage from May to September 2025, when closed models took close to 80 percent of tokens and nearly 96 percent of revenue on the platform, and found open models routinely reach 90 percent or more of closed models’ benchmark performance. The estimate extrapolates from a platform that handles about 1 percent of global inference spending and ignores switching costs, reliability and support, which is why defenders of closed models say users who pay more are buying something real. Nagle is the Linux Foundation’s advising chief economist, and an earlier Linux Foundation survey on open-source AI was commissioned by Meta, which those skeptical of the finding note.

Label: Distinct attack vectors against stored model weights
Value: 38
Unit: attack vectors
Viz: bar
Data year: 2024
Source label: RAND, Securing AI Model Weights: Preventing Theft and Misuse of Frontier Models (Nevo et al.), May 2024
Source URL: https://www.rand.org/pubs/research_reports/RRA2849-1.html
Note: RAND identified 38 meaningfully distinct ways attackers could steal a frontier model’s weights and defined five security levels for defending against them.
Context: The closed case depends on weights staying closed, and RAND’s report is the standard reference for how hard that is: the higher security levels are meant to hold off increasingly capable attackers, up to well-resourced state operations. Those who favor open release use this to argue that a determined adversary can get closed weights anyway, so secrecy mostly denies access to ordinary users; those who favor keeping the frontier closed argue it shows labs must raise security, not give up on it. The 2026 distillation campaigns are a cheaper route to the same end that needs no theft at all.

Label: Downloads of Meta’s Llama models
Value: 1.2
Unit: billion downloads (as of April 2025)
Viz: bar
Data year: 2025
Source label: TechCrunch, Meta says its Llama AI models have been downloaded 1.2B times, 29 April 2025
Source URL: https://techcrunch.com/2025/04/29/meta-says-its-llama-ai-models-have-been-downloaded-1-2b-times/
Note: Meta said its open-weight Llama models had been downloaded 1.2 billion times by April 2025, up from 1 billion in March and 650 million in December 2024.
Context: Llama was the model family that made open weights a mainstream strategy after Mark Zuckerberg’s July 2024 essay “Open Source AI Is the Path Forward” (https://about.fb.com/news/2024/07/open-source-ai-is-the-path-forward/). The count is Meta’s own and includes repeated and automated downloads. Meta then released its first Muse Spark model in April 2026 with closed weights (DeepLearning.AI, https://www.deeplearning.ai/the-batch/with-muse-spark-meta-pivots-away-from-its-open-weights-llama-strategy), and Qwen has since overtaken Llama in derivatives and local downloads, which makes the figure a marker of where the open-weight movement started rather than where it is. Llama’s license also excluded companies with more than 700 million monthly users without a separate agreement [license term from memory, unverified on a fetched page], one reason the Open Source Initiative has said Llama is not open source [OSI statement not fetched for this page].

Label: US voters on open-sourcing powerful AI models
Value: 47
Unit: percent opposed (23 percent in support)
Viz: ranked
Series: Oppose 47 (highlight); Support 23
Data year: 2023
Source label: AI Policy Institute poll conducted by YouGov, 1,118 voters, 2 to 6 September 2023
Source URL: https://theaipi.org/poll-shows-voters-oppose-open-sourcing-ai-models-support-regulatory-representation-on-boards-and-say-ai-risks-outweigh-benefits/
Note: In a 2023 poll, 47 percent of US voters opposed open-sourcing powerful AI models and 23 percent supported it.
Context: This is the only national poll found that asks directly about open release, and it is old and limited: it predates every model in the current debate, the pollster simplified the question for respondents unfamiliar with weights and does not publish the wording on the release page, the unsure share is not reported, and the sponsor advocates a cautious path on AI. No 2025 or 2026 national poll on open-weight release was found. The editor should use this tile only with the date and the sponsor visible, or drop it.

## Questions

Question: Does releasing a capable model’s weights give attackers meaningful help they could not already get?
Tag: empirical
Poles: Little added risk / Real added uplift
Why contested: The debate turns on marginal risk, the harm open release adds over what a determined attacker could already do with the internet, existing tools and closed models. The US Commerce Department’s 2024 review found “not sufficient evidence on the marginal risks” to justify restricting open weights at the time (NTIA, https://www.ntia.gov/programs-and-initiatives/artificial-intelligence/open-model-weights-report/policy-approaches-recommendations/recommendations). The 2026 evidence is much stronger in cyber than in biology: open models are now building working exploits and running multi-step attacks in tests, but the evaluations cited on this page report laboratory results, not a real-world attack attributed to an open model.
Case for little added risk: The question is not whether a model can help with a harmful task but whether it changes what attackers can do. Sophisticated attackers, especially states, already have skilled staff, stolen tools and their own models; unsophisticated ones are limited far more by access to materials, targets and operational skill than by information. The Kimi K3 evaluation found the open model far behind US closed models on actual exploitation (no arbitrary code execution in 41 tries against an average of 20 for the best closed models), and the Firefox exploits Epoch built also depended on a separate unpublished flaw, which Mozilla patched once Epoch disclosed it. Every capability in today’s open models existed in closed models four to seven months earlier and did not produce the predicted wave of attacks. The marginal-risk framework set out by Sayash Kapoor and 24 co-authors in 2024 (https://arxiv.org/abs/2403.07918) asks for evidence of added harm before restriction, and that standard has not been met.
Case for real added uplift: The marginal-risk argument assumed open models would stay well behind; they no longer do. Open models in 2026 have turned public security fixes into working browser exploits for about 1,000 dollars, matched closed models on end-to-end exploit generation, and engaged with overtly harmful requests once their refusals were removed for about 1,200 dollars. What open release adds is not knowledge but labor: an attacker who could never hire an exploit team now has one that does not refuse, cannot be monitored, and cannot be cut off. Attackers adopt new tools faster than defenders patch, and a downloaded model is permanent. Waiting for proof of a real-world attack means the evidence arrives only after the weights are everywhere.

Question: Does keeping American weights closed slow rivals, or only cede the open ecosystem to them?
Tag: empirical
Poles: Withholding buys time / Capability spreads anyway
Why contested: The leading open-weight models in 2026 are Chinese (Kimi, GLM, Qwen, DeepSeek), Chinese models took the largest share of Hugging Face downloads, and the open-closed gap is measured in months. Each side reads those facts as proof of its case.
Case for withholding buys time: The strongest Chinese open models are still months behind the US frontier, and the evaluations show the gap is widest where it matters most, in real exploitation. Some of their progress is alleged to come from distilling US closed models through tens of thousands of fraudulent accounts, which is evidence that US closed weights are worth protecting rather than giving away. Releasing a US frontier model’s weights would hand every rival the result of billions of dollars of training at no cost and erase the lead that chip export controls are meant to preserve. A few months matters: it is the window in which defenders can patch what the frontier can find.
Case for capability spreads anyway: The lead in open models has already passed to China, not because US labs released too much but because they released too little. Developers worldwide build on what they can download and adapt, which is why Qwen has more derivatives than Google and Meta combined and why US companies including Airbnb, DoorDash and the maker of Cursor build on Chinese models (Reuters via bdnews24, https://bdnews24.com/world/americas/nz7l0a0g1i). Closed weights do not stop diffusion, which happens through distillation, theft, talent and independent research within months. Withholding only decides whose models, values and technical standards the world’s developers adopt; the 2025 US AI Action Plan itself says open models “have geostrategic value.”

Question: Does open release spread power over AI, or reinforce the firms that already hold it?
Tag: empirical
Poles: Openness distributes power / Openness entrenches incumbents
Why contested: Openness is defended as the antidote to concentration, yet the largest open releases come from trillion-dollar companies and state-backed labs, the main distribution hub is being bought by the dominant chip maker, and the compute needed to train frontier models is held by a handful of firms.
Case for openness distributes power: Open weights let anyone run, inspect, fine-tune and deploy a capable model without asking permission or paying rent, which closed APIs never allow. The effect is visible: independent developers’ share of Hugging Face downloads rose from 17 to 39 percent, open models carry most tokens on OpenRouter, and a startup or government can host its own model on its own hardware with its own data. Competition among open models has pushed prices down across the market, including for closed models. A world with three closed providers is one where three companies, and the governments that can lean on them, decide what everyone else may do with AI.
Case for openness entrenches incumbents: Releasing weights distributes the product, not the power to make it. The ability to train frontier models depends on compute, data and capital that open release does not share, and firms release weights when it serves their strategy: to commoditize a rival’s product, attract developers to their platform, or sell the chips and clouds open models run on. Meta closed its weights when it thought it had a lead and reopened a lesser version later; Alibaba kept its best Qwen model API-only before returning to open weights with commercial restrictions. As David Gray Widder, Meredith Whittaker and Sarah Myers West argued in Nature in 2024, openness by itself does not shift concentration in AI, which is why they say it must be paired with antitrust and privacy protections (https://ui.adsabs.harvard.edu/abs/2024Natur.635..827W).

Question: Do open models help cyber defenders more than attackers?
Tag: empirical
Poles: Defenders gain more / Attackers gain more
Why contested: Cyber is where the 2026 evidence is concentrated. The same capability that writes exploits finds and fixes vulnerabilities, and the open-weights letter and the safety camp make opposite claims about which side benefits.
Case for defenders gain more: Defenders vastly outnumber attackers, and most of them (hospitals, utilities, small firms, governments abroad) cannot send sensitive code and logs to a foreign company’s API or afford frontier prices. Open models let them scan their own systems at scale, privately and cheaply; open models were reportedly used to analyze the July 2026 agent attack on Hugging Face quickly (CNAS, https://www.cnas.org/publications/cnas-insights/cnas-insights-a-closing-door-on-open-weights-implications-for-ai-sovereignty). The letter’s argument is that “defenders need access to models with comparable capabilities.” Attackers who matter already have capable tools; it is defenders who are left without them when the best models are locked away or switched off.
Case for attackers gain more: Offense needs one working exploit; defense needs to patch everything, and patches take weeks to reach users. Epoch’s Firefox result is that gap in action: public fixes became working exploits before users updated. Defenders can be given closed frontier models through vetted access programs, as Anthropic did with Mythos 5, offered to government agencies and selected companies to harden their systems (Al Jazeera, https://www.aljazeera.com/economy/2026/6/14/us-orders-anthropic-to-disable-ai-models-for-all-foreign-nationals), while a downloaded model cannot be given to defenders alone. The UK AI Security Institute’s reading of its own results is that defenders have “a short window to prepare” before frontier cyber capabilities become available “without the same safeguards,” which only makes sense if open availability favors offense.

Question: Is depending on a few closed providers a bigger risk than putting capable models in everyone’s hands?
Tag: value
Poles: Concentration is the risk / Proliferation is the risk
Why contested: Both sides argue from security. The open camp points to single points of failure; the closed camp points to irreversible misuse. The June 2026 order that made Anthropic disable two models for every customer gave the first argument a concrete case (Al Jazeera, https://www.aljazeera.com/economy/2026/6/14/us-orders-anthropic-to-disable-ai-models-for-all-foreign-nationals).
Case for concentration is the risk: When a few companies hold every capable model, an outage, a policy change, a commercial dispute or a government directive in one country can cut off businesses, hospitals and governments everywhere at once. That happened in June 2026, when an export-control directive led Anthropic to switch off Fable 5 and Mythos 5 for all customers at short notice. Concentration also puts the judgment about what billions of people may ask an AI in a few private hands, and a closed system can fail or be breached “in ways that outsiders cannot detect,” as the open-weights letter puts it (The Next Web, https://thenextweb.com/news/open-weights-american-ai-leadership-letter-huang-nvidia-openai-absent). Countries building their own capacity cannot rely on a foreign API.
Case for proliferation is the risk: Concentration can be governed: providers can be regulated, audited, sued and made to share access, and a provider that can switch a model off can also stop a misuse in progress. Proliferation cannot be undone. Once a model that can write exploits or assist with a pathogen is downloaded, every copy is permanent and unmonitored, and no later discovery about its capabilities can be acted on. The June 2026 episode shows closed control working as designed, however clumsily: a government that thought a capability was dangerous could act on it. A resilience problem has resilience solutions (multiple providers, contracts, local deployment of less capable models); a proliferation problem has none.

Question: How much catastrophic risk justifies withholding a model’s benefits from everyone?
Tag: value
Poles: Precaution first / Access first
Why contested: Even with full agreement on the evidence, the choice weighs a small chance of severe, irreversible harm against large, certain, widely shared benefits, and people differ on how to weigh those and who should bear the risk.
Case for precaution first: Some harms are bad enough that a small probability dominates the calculation: mass-casualty biological attacks, crippling attacks on infrastructure. Open release is the one AI decision that can never be reversed, so it should require the most confidence, not the least. Benefits withheld are delayed, not lost: smaller and older models can be opened, frontier capability can be offered through APIs and vetted programs, and the decision can be revisited as safeguards and evidence improve. The burden of proof belongs on the side that cannot take its decision back.
Case for access first: Withholding has costs as real as misuse, though harder to see: researchers who cannot study the systems shaping society, poorer countries and small firms priced out or cut off, users who must accept one company’s rules, and the security gained from many eyes. Treating every capable model as a potential weapon would leave general-purpose technology in the hands of a few firms indefinitely, since there will always be a speculative worst case. Harm should be addressed where it occurs, through laws against the conduct and defenses at the target, as with every other dual-use technology from cryptography to chemistry.

Question: Does opening a model to outside inspection make AI safer than keeping it under its developer’s control?
Tag: empirical
Poles: Scrutiny makes safer / Control makes safer
Why contested: Openness and control offer different kinds of safety. Open weights let independent researchers study, red-team and interpret models; closed deployment lets the developer monitor use, detect misuse and patch problems. Both are real, and the dispute is over which matters more for capable models.
Case for scrutiny makes safer: Independent research depends on access to real models: interpretability, red-teaming and replication of the labs’ own safety claims all need weights, and the 2025 Foundation Model Transparency Index found open-weight developers outscored closed ones on every domain. OpenAI said it released gpt-oss partly to “help accelerate safety training and alignment research across the industry” (https://openai.com/index/introducing-gpt-oss/). Safety that only the developer can check is a promise, and the agent incidents of 2026 at closed labs show what closed development can hide until disclosure.
Case for control makes safer: The safeguards that work in practice are system-level: monitoring, classifiers, account bans, rate limits and the ability to update a model after a problem is found. That is how Anthropic detected and blocked the distillation campaigns. A downloaded model has none of these; its safety training can be removed for about a thousand dollars. Researchers can be given deep access to closed models through structured programs without giving the same access to everyone. Transparency about how a model was made is valuable and can be required of closed developers without publishing the weights.

Question: Should “open” mean the weights alone, or the data and code that made them too?
Tag: value
Poles: Weights are enough / Open the whole stack
Why contested: Almost every model called open in 2026 releases weights under a custom license and withholds training data and code. The Open Source Initiative’s Open Source AI Definition (https://opensource.org/ai/open-source-ai-definition) requires much more, and few major models meet it.
Case for weights are enough: Weights are what users need to run, adapt, fine-tune and deploy a model independently, which is the freedom that matters to almost everyone who uses open models. Releasing training data is often impossible because of copyright, privacy and licensing, and insisting on it would leave almost no capable open models at all. Licenses that require a separate deal from the largest hosting companies are a reasonable way to fund the work while keeping it free for nearly everyone else.
Case for open the whole stack: Without the data, code and training recipe a model cannot be reproduced, audited for what it learned, or improved at the root; as Stanford HAI’s James Landay put it, “That’s not an open model. That’s open distribution” (https://hai.stanford.edu/news/open-weight-models-arent-enough-we-need-truly-open-source-ai-models-for-science-and-society). Custom licenses with revenue thresholds, attribution requirements and use bans give the releasing company control the word “open” implies it has given up. Models released with far more of the stack, such as Ai2’s OLMo and Switzerland’s publicly built Apertus, which Nathan Sanders and Bruce Schneier describe as fully open, show it can be done, and only that kind of release lets science check what a model is.

## Positions

Name: Release openly only below a tested danger line
Adherents: Anthropic, whose 27 July 2026 statement says “Anthropic has never advocated for a ban on open-weights models,” calls open models without dangerous capabilities a public good, and says “All sufficiently capable models, open and closed, should go through mandatory safety testing” — https://www.anthropic.com/news/position-open-weights-models ; SaferAI, whose executive director Henry Papadatos said after testing GLM-5.2 that “we shouldn’t just accept that dangerous capabilities are easily accessible by anyone anywhere” and that “The objective should clearly be that the good capabilities — the safe ones — are accessible to anyone” (TechCrunch) — https://techcrunch.com/2026/08/04/open-weight-ai-models-are-catching-up-to-the-frontier-the-safety-gap-remains/ ; OpenAI, which released gpt-oss only after adversarially fine-tuned versions “were unable to reach high capability levels” under its Preparedness Framework, while keeping its frontier models closed — https://openai.com/index/introducing-gpt-oss/ ; also Bengüsu Özcan, Alex Petropoulos and Max Reddel’s “Beyond the Binary,” which argues openness should be “determined by rigorous risk assessment and demonstrated safety rather than ideology or commercial pressure” (https://arxiv.org/abs/2602.19682); Georgetown’s Mark MacCarthy, who argues open and closed models should face the same pre-release review (https://techpolicy.press/us-governments-ai-risk-review-should-apply-to-open-weight-models); and CNAS’s Vivek Chilukuri, who writes “Open-weight models have no durable guardrails” (https://www.cnas.org/publications/cnas-insights/cnas-insights-a-closing-door-on-open-weights-implications-for-ai-sovereignty). In practice Google (closed Gemini, open Gemma) and Meta (closed Muse Wonder, open Muse Spark Open) follow the same pattern of a closed flagship and open models a step behind, under their own risk frameworks.
The case in the camp’s own voice: Open models below the danger line are one of the best things in AI: cheap, adaptable, private, essential for research and for countries that cannot rely on a foreign API. We want more of them. But a model’s weights, once published, can never be recalled, and its safety training can be stripped for about a thousand dollars. For most models that does not matter. For a model that can find and chain software vulnerabilities, or give real help toward a biological weapon, it is the whole question, because the safeguards that make such a model safe to offer — monitoring, classifiers, the ability to cut off an abuser or patch a flaw — exist only while the developer holds the weights. So the line should be drawn by testing, not ideology: evaluate every sufficiently capable model, open or closed, American or Chinese, for the specific dangerous capabilities, release openly what passes, and keep behind controlled access what does not until safeguards or defenses catch up. That is not a ban, and it is not protectionism: it applies to us as much as to anyone.
Best evidence: The 2026 cyber results are the core. Anthropic found GLM-5.3, released without meaningful safeguards, produced 50 end-to-end browser exploits in 410 attempts against 56 for Claude Mythos Preview, and engaged with overtly harmful cyber requests 64 to 100 percent of the time under simple techniques, against 0 for safeguarded Claude models. Epoch AI used the same open model to turn public Firefox fixes into working exploits for six releases at about 1,000 dollars each, without a single refusal. The UK AI Security Institute and CAISI found Kimi K3’s safeguards did not stop exploit development. Removing refusals costs about 1,200 dollars, a negligible fraction of training. The International AI Safety Report 2026 notes open models cannot be recalled and their safeguards are easier to remove. SaferAI found GLM-5.2 refused none of its offensive cyber or biology tasks and that Z.ai published no safety framework.
Variation inside the camp: Members differ on who should draw the line and how. Anthropic, MacCarthy and SaferAI want testing that is independent and, for Anthropic, mandatory and global for every sufficiently capable model; OpenAI, Google and Meta apply their own frameworks to their own releases, and Meta has said it will not release a model its framework rates high risk until mitigations bring it to moderate (TechCrunch, https://techcrunch.com/2025/02/03/meta-says-it-may-stop-development-of-ai-systems-it-deems-too-risky). Some, including the “Beyond the Binary” authors, favor a graded ladder between open and closed (staged release, licensed access to weights, vetted research programs) rather than a single line; Anthropic and CNAS favor expanding access to closed frontier models for vetted defenders and trusted countries. Members also differ on whether the line has already been crossed: Anthropic says “a critical threshold in freely accessible capabilities has now been crossed,” while OpenAI and Google signed the July 2026 letter against restricting open weights.
Answer to the strongest objection: The objection is that capability spreads within months anyway, so withholding only cedes ground to China and to companies that release without testing. The camp’s answer is that months are what defense runs on: a vulnerability found by a closed model can be patched before the same capability is downloadable, and the AI Security Institute describes that gap as a “short window to prepare.” Testing every capable model, wherever it is made, is the opposite of a unilateral sacrifice, and the camp does not ask the United States to stop releasing open models, only to release ones that pass. Distillation and theft are reasons to secure weights better and act against abuse, not reasons to publish them.

Name: Release frontier models openly
Adherents: The more than 270 companies and organizations behind “Open Weights and American AI Leadership,” including Nvidia, Microsoft, Meta, Hugging Face, Mistral, IBM, Andreessen Horowitz, Mozilla and the Linux Foundation, which argues US leadership “will be judged not by one frontier AI model, but by whether the United States builds a strong, open ecosystem” and that “the right response to this risk is not to prohibit open weights” — https://www.microsoft.com/en-us/corporate-responsibility/topics/open-weight/ ; Nvidia’s Jensen Huang, who shared the letter saying “The world needs both frontier closed models and frontier open models” (The Next Web) — https://thenextweb.com/news/open-weights-american-ai-leadership-letter-huang-nvidia-openai-absent ; Meta, which released Muse Spark Open saying “We’re sharing this work because we want everyone to have access to the best models” — https://research.meta.ai/blog/muse-spark-open ; also Hugging Face’s Clem Delangue, who said open models “can now help defend against millions of cyberattacks every day” (TechCrunch, https://techcrunch.com/2026/08/04/open-weight-ai-models-are-catching-up-to-the-frontier-the-safety-gap-remains/); Yann LeCun, who left Meta to found AMI Labs and argues AI platforms tend toward open source (MIT Technology Review, https://www.technologyreview.com/2026/01/22/1131661/yann-lecuns-new-venture-ami-labs/); Arvind Narayanan and Sayash Kapoor, whose “AI as Normal Technology” argues for regulating uses rather than development and against nonproliferation (https://knightcolumbia.org/content/ai-as-normal-technology); and in practice Moonshot AI, Z.ai, DeepSeek and Alibaba, which release their flagship models’ weights, with Xi Jinping telling the July 2026 World AI Conference “We must … encourage open source and openness, cooperation and sharing” (Tech Policy Press, https://techpolicy.press/will-china-crack-down-on-open-weight-models).
The case in the camp’s own voice: Open source built the internet, the cloud and nearly every piece of software the world runs on, and it did so because anyone could inspect, fix and build on it. AI is following the same path. Open weights let a hospital keep patient data on its own servers, a startup build without paying rent to a competitor, a researcher check a safety claim, a country run AI under its own laws, and a defender use the same tools as the attacker. Closed frontier models are single points of failure: they can be breached, misused or switched off in ways outsiders cannot see, as their own customers learned this year. The risks of open release are real, and the letter says so, but they are marginal: every capability in an open model existed in a closed one months earlier, the attackers who matter already have tools, and the harms are already crimes. Answer misuse by going after the misuse — distillation that breaks the law, attacks, fraud — and by giving defenders the best models, not by locking the most important technology of the century inside three companies.
Best evidence: The gap is months, not years (four months on average in 2026 by Epoch’s measure), and the camp points out that the cyber evidence against open models comes from laboratory tests, with no real-world attack yet attributed to an open model that closed models had not already made possible. Open models now carry most tokens on OpenRouter because users find them good enough at a fraction of the price, and Nagle and Yue estimated about 24.8 billion dollars a year in forgone savings from not using them more. The 2025 Foundation Model Transparency Index found open-weight developers outscore closed ones on every domain. The June 2026 directive that shut off two Anthropic models for every customer at a few hours’ notice showed what dependence on a closed provider means. The Kimi K3 evaluation found the best Chinese open model achieved arbitrary code execution in none of 41 tries, against an average of 20 for the best closed models. And withholding has not stopped diffusion: China leads open-model downloads at 41 percent.
Variation inside the camp: The camp splits on motive and on how far openness should go. US industry signers frame open weights as a pillar of American leadership against China, as does the ATOM Project (American Truly Open Models), whose main essay is by Nathan Lambert and which calls for multiple US labs training open models on 10,000 or more leading-edge GPUs (https://www.atomproject.ai/), and the 2025 US AI Action Plan, which says the release decision “is fundamentally up to the developer” but that government “should create a supportive environment for open models.” Others defend openness as a public good regardless of nationality. Some members release everything (DeepSeek under the MIT license, OpenAI’s gpt-oss under Apache 2.0); others release under custom licenses with revenue thresholds and use bans (Meta’s Muse Model License, Moonshot’s Kimi license). Several prominent signers keep their own best models closed and join the camp only in opposing restrictions on others’ open releases.
Answer to the strongest objection: The objection is irreversibility: once a model that can build exploits is downloaded, no safeguard can ever be applied. The camp’s answer is that the same capability reaches the world within months whether or not any given model is opened — through rivals’ releases, distillation, theft or independent research — so a lab that withholds weights delays very little while denying defenders, researchers and smaller countries the same tools. Closed safeguards are also weaker than claimed: models are jailbroken, distilled through fraudulent accounts and shut off by governments. The durable defense is hardening the targets, as Mozilla did by patching the flaw Epoch disclosed before the report was even published, and that defense needs capable open models in defenders’ hands.

Name: Build public AI instead of relying on company releases
Adherents: Stanford HAI’s James Landay, who argues open weights are “not an open model” but “open distribution,” says “A closed frontier model behind an API is the ultimate walled garden,” and calls for universities to build open frontier systems with code, data and tooling released — https://hai.stanford.edu/news/open-weight-models-arent-enough-we-need-truly-open-source-ai-models-for-science-and-society ; the Public AI Network, a coalition that treats AI as public infrastructure like utilities or libraries and argues “AI systems are growing in power and should reflect society’s values, not the values of shareholders” — https://publicai.network/ ; Mozilla, whose “Creating a public counterpoint for AI” says “We can’t just rely on a few companies to build everything our society needs from AI” and calls for “a whole parallel AI ecosystem that can run on non-commercial incentives” — https://blog.mozilla.org/mozilla/ai/public-ai-counterpoint/ ; also Nathan Sanders and Bruce Schneier, who hold up Switzerland’s fully open, publicly built Apertus model as “an alternative to corporate AI” (https://www.schneier.com/essays/archives/2026/02/rewiring-democracy-now-switzerland-shows-us-an-alternative-to-corporate-ai.html); and David Gray Widder, Meredith Whittaker and Sarah Myers West, whose 2024 Nature paper argues openness alone does not shift concentration of power in AI (https://ui.adsabs.harvard.edu/abs/2024Natur.635..827W).
The case in the camp’s own voice: The open-versus-closed fight is being held on the companies’ terms. Whether Meta, Moonshot or OpenAI publishes a given set of weights is a business decision those firms make for their own reasons, and they reverse it when their reasons change: Meta closed its frontier model in April and opened a lesser one in October, Alibaba held back its best Qwen and then reopened it with commercial strings. A downloadable file under a custom license is not openness; you cannot see what it was trained on, reproduce it or fix it at the root, and the power to make the next one stays with whoever owns the chips, the data and the capital. Closing everything would be worse, but waiting for corporate generosity is not a strategy. The answer is public capacity: models built by universities and public institutions with code, data and methods fully released, public compute to train them, and competition and privacy law to keep the private platforms honest. The question is not whether weights are open but who builds AI and for whom.
Best evidence: Release policies at the largest developers have shifted with commercial strategy within a single year (Meta’s closed Muse Spark in April 2026 and open Muse Spark Open in October with its most capable Muse Wonder still closed; Alibaba’s Qwen 3.6 top model API-only, then Qwen 3.8 weights with restrictions on outside hosts, per Graham Webster, https://techpolicy.press/will-china-crack-down-on-open-weight-models). The 2025 Foundation Model Transparency Index found open developers such as DeepSeek and Meta still opaque about how their models were built. Hugging Face’s Summer 2026 report found 1.5 percent of repositories take 99.2 percent of downloads, and the hub itself is being acquired by Nvidia. Openly released, publicly built models exist and work: Apertus (70 billion parameters, trained on 15 trillion tokens, Apache 2.0, built at ETH Zurich and EPFL on Swiss public supercomputers, per Sanders and Schneier) and Ai2’s OLMo, released with its training data and code.
Variation inside the camp: Some members, such as Landay and the Open Source Initiative, stress full openness (weights, data, code) wherever models are built; others, such as the Public AI Network and Mozilla, stress public institutions and funding; the Nature authors stress antitrust and privacy enforcement over model release altogether. Most members also oppose restricting open weights: Landay agrees with the industry letter on that point, and Mozilla signed it.
Answer to the strongest objection: The objection is that public projects cannot match the frontier: Apertus has 70 billion parameters while the companies train models with trillions, so public AI is a footnote to the real choice. The camp’s answer is that most useful AI is far from the frontier — models under 1 billion parameters account for 83 percent of Hugging Face downloads — and that public infrastructure does not need to win the frontier race to change who controls the technology everyone actually uses, any more than public libraries needed to outsell publishers. Where frontier capability matters, public compute and university labs are how the public gets a seat at the table instead of waiting to see what companies decide to release.

## Crux

The disagreement under the others is whether publishing the weights of a near-frontier model adds enough irreversible harm, beyond what attackers could already get or would get within months anyway, to outweigh what openness gives everyone else.

What evidence could settle: three empirical questions, each now being measured. First, marginal uplift: does an open model at today’s level actually change what attackers accomplish, in cyber and in biology, compared with the closed models, tools and skills they already have? The 2026 evaluations show capable open models will attempt offensive work and can produce exploits in laboratory settings; they do not yet show whether that changes real-world attack rates. Second, the speed of diffusion: how long does a closed-frontier capability stay out of reach when weights are withheld, given rivals’ releases, distillation and theft, and does that window, now four to seven months, stay steady or keep shrinking? Third, the value of control: how much misuse do closed providers’ monitoring, classifiers and account bans actually stop, and how much gets through by jailbreak or distillation? If open release turns out to add little and the window keeps closing, the case for withholding weakens; if open models measurably enable attacks that closed ones prevent, and withholding reliably buys time defenders use, it strengthens.

What no data can close: how to weigh a small chance of severe, permanent harm against large, diffuse and certain benefits; whether it is worse to have the most capable technology of the era controlled by a few companies and the governments that can direct them, or available to anyone including those who would misuse it; and who should carry the burden of proof, those who want to release or those who want to withhold. People who agree on every measurement can still answer these differently.

## Actions

Kind: learn_more
Title: Epoch AI’s open-weight model research
What it is: Epoch AI’s collected data and reports on open-weight models, including how far they trail the closed frontier on general and cyber capability and the October 2026 report on turning Firefox security fixes into exploits, with charts and methods a reader can check.
URL: https://epoch.ai/topics/open-models
Resolved: yes
Serves: neutral

Kind: learn_more
Title: How far behind the frontier are open-weight models on cyber?
What it is: The UK AI Security Institute’s July 2026 measurement of leading open models against closed ones on 70 cyber tasks and a simulated network attack, including costs per task and what the gap means for defenders.
URL: https://www.aisi.gov.uk/work/how-far-behind-the-frontier-are-leading-open-weight-models-on-cyber
Resolved: yes
Serves: neutral

Kind: learn_more
Title: International AI Safety Report 2026
What it is: The scientific assessment of general-purpose AI chaired by Yoshua Bengio, written by more than 100 experts and backed by more than 30 countries, with a section on the benefits and risks of open-weight models and a summary for policymakers.
URL: https://internationalaisafetyreport.org/
Resolved: yes
Serves: neutral

Kind: learn_more
Title: NTIA report on AI models with widely available weights
What it is: The US Commerce Department’s 2024 review of the benefits and risks of open model weights, which concluded the evidence did not then justify restrictions and set out what to monitor and when restrictions might become appropriate.
URL: https://www.ntia.gov/programs-and-initiatives/artificial-intelligence/open-model-weights-report
Resolved: yes
Serves: neutral

Kind: learn_more
Title: Anthropic’s position on open-weight models
What it is: Anthropic’s July 2026 statement that it opposes a ban on open weights but wants every sufficiently capable model, open or closed, safety-tested, with its reasoning on irreversibility, distillation and authoritarian misuse.
URL: https://www.anthropic.com/news/position-open-weights-models
Resolved: yes
Serves: Release openly only below a tested danger line

Kind: learn_more
Title: SaferAI’s Frontier Risk Management Tracker
What it is: An independent nonprofit’s ratings of how a dozen AI developers, including Meta and Nvidia, identify, analyze and manage the risks of their models, with the practices it says are missing across the industry.
URL: https://tracker.safer-ai.org/
Resolved: yes (redirects from ratings.safer-ai.org)
Serves: Release openly only below a tested danger line

Kind: learn_more
Title: On the Societal Impact of Open Foundation Models
What it is: The 2024 paper by Sayash Kapoor, Rishi Bommasani and 23 co-authors that set out the benefits of open models and the marginal-risk framework now used to judge whether a release adds harm beyond existing tools.
URL: https://arxiv.org/abs/2403.07918
Resolved: yes
Serves: Release frontier models openly

Kind: local
Title: Run an open-weight model on your own computer
What it is: Ollama is a free tool for downloading and running open-weight models locally, so a reader can see what open release means in practice: a capable model working offline, with no account and no one monitoring the conversation.
URL: https://ollama.com/
Resolved: yes
Serves: Release frontier models openly

Kind: learn_more
Title: Read the “Open Weights and American AI Leadership” letter
What it is: The July 2026 letter from more than 270 companies and organizations, hosted by Microsoft, setting out the industry case for open weights and against restricting them, with the full signatory list.
URL: https://www.microsoft.com/en-us/corporate-responsibility/topics/open-weight/
Resolved: yes (loads in a browser and through a fetch tool; returns 403 to bare command-line requests)
Serves: Release frontier models openly

Kind: volunteer
Title: Get involved with the Public AI Network
What it is: A coalition working to build AI as public infrastructure, with a newsletter, a Slack community, a seminar series, an editable public wiki and open roles for people who want to help.
URL: https://publicai.network/
Resolved: yes
Serves: Build public AI instead of relying on company releases

Kind: policy
Title: Endorse the Open Source AI Definition
What it is: The Open Source Initiative’s standard for what counts as open-source AI, requiring access to weights, code and detailed information about training data; organizations and individuals can add their endorsement.
URL: https://opensource.org/ai/endorsements
Resolved: yes
Serves: Build public AI instead of relying on company releases

Kind: learn_more
Title: Try a fully open model: Ai2 OLMo
What it is: The Allen Institute for AI’s OLMo models, released with weights, training data, code and training logs, which show what “open the whole stack” looks like in practice.
URL: https://allenai.org/olmo
Resolved: yes
Serves: Build public AI instead of relying on company releases

## Sources

Moonshot AI releases Kimi K3.1 Pro model weights, TechNode, 5 November 2026 — https://technode.com/2026/11/05/moonshot-ai-releases-kimi-k3-1-pro-model-weights/ — accessed 2026-11-23
Artificial Analysis, open-weight models leaderboard — https://artificialanalysis.ai/models/open-source — accessed 2026-11-23
Meta, Muse Spark Open announcement, 15 October 2026 — https://research.meta.ai/blog/muse-spark-open — accessed 2026-11-23
Implicator, Meta releases Muse Spark Open, an 816B model that trails Chinese rivals at coding — https://www.implicator.ai/meta-releases-muse-spark-open-an-816b-model-that-trails-chinese-rivals-at-coding/ — accessed 2026-11-23
DeepLearning.AI The Batch, With Muse Spark, Meta pivots away from its open-weights Llama strategy, 17 April 2026 — https://www.deeplearning.ai/the-batch/with-muse-spark-meta-pivots-away-from-its-open-weights-llama-strategy — accessed 2026-11-23
The Next Web, China proposes export controls on its advanced AI models and chip designs, 16 October 2026 — https://thenextweb.com/news/china-ai-export-controls-draft — accessed 2026-11-23
ChinaTalk, MOFCOM’s new AI rules — https://www.chinatalk.media/p/mofcoms-new-ai-rules — accessed 2026-11-23
Epoch AI, Open models lag state-of-the-art closed models by 4 months, 29 May 2026 — https://epoch.ai/data-insights/open-closed-eci-gap — accessed 2026-11-23
Epoch AI, Open-weight models topic page — https://epoch.ai/topics/open-models — accessed 2026-11-23
Epoch AI, Open-weight models trail closed models in cyber capabilities by 6–7 months, 16 October 2026 — https://epoch.ai/data-insights/open-closed-cyber-eci-gap — accessed 2026-11-23
Epoch AI, AI can turn security fixes into working exploits before users receive an update, 29 October 2026 — https://epoch.ai/publications/open-weight-models-patch-gap — accessed 2026-11-23
UK AI Security Institute, How far behind the frontier are leading open-weight models on cyber?, 17 July 2026 — https://www.aisi.gov.uk/work/how-far-behind-the-frontier-are-leading-open-weight-models-on-cyber — accessed 2026-11-23
UK AISI and NIST CAISI, Preliminary assessment of Kimi K3’s cyber capabilities, 23 July 2026 — https://www.nist.gov/news-events/news/2026/07/uk-aisi-caisi-preliminary-assessment-kimi-k3s-cyber-capabilities — accessed 2026-11-23
Anthropic Frontier Red Team, GLM-5.3 and the spread of advanced cyber capabilities, 29 September 2026 — https://www.anthropic.com/research/glm-5-3-and-the-spread-of-advanced-cyber-capabilities — accessed 2026-11-23
Anthropic, Our position on open-weights models, 27 July 2026 — https://www.anthropic.com/news/position-open-weights-models — accessed 2026-11-23
Anthropic, Detecting and preventing distillation attacks, 23 February 2026 — https://anthropic.com/news/detecting-and-preventing-distillation-attacks — accessed 2026-11-23
Microsoft, Open Weights and American AI Leadership (letter of 24 July 2026, signatories as of 3 August 2026) — https://www.microsoft.com/en-us/corporate-responsibility/topics/open-weight/ — accessed 2026-11-23
The Next Web, The AI giants just broke with OpenAI and Anthropic on open weights, July 2026 — https://thenextweb.com/news/open-weights-american-ai-leadership-letter-huang-nvidia-openai-absent — accessed 2026-11-23
eWeek, Nvidia, Microsoft back open-weight AI models, 27 July 2026 — https://www.eweek.com/news/nvidia-microsoft-open-weight-ai-letter/ — accessed 2026-11-23
Axios, The secret Trump administration battle to fight Chinese AI, 20 July 2026 — https://axios.com/2026/07/20/ai-us-china-open-source-kimi — accessed 2026-11-23 (search result only; page returned 403 to fetch)
Cloud Security Alliance, The Open-Weight Rift: Concentration Risk vs. National Security, 4 August 2026 — https://labs.cloudsecurityalliance.org/research/csa-research-note-open-weight-concentration-risk-rift-202608/ — accessed 2026-11-23
TechTarget, Calls for AI slowdown raise new challenges for open-weight models, 17 September 2026 — https://www.techtarget.com/ai/news/366650514/Calls-for-AI-slowdown-raise-new-challenges-for-open-weight-models — accessed 2026-11-23
CNAS, A Closing Door on Open Weights? Implications for AI Sovereignty (Vivek Chilukuri), 26 October 2026 — https://www.cnas.org/publications/cnas-insights/cnas-insights-a-closing-door-on-open-weights-implications-for-ai-sovereignty — accessed 2026-11-23
Tech Policy Press, US government’s AI risk review should apply to open-weight models (Mark MacCarthy), 13 August 2026 — https://techpolicy.press/us-governments-ai-risk-review-should-apply-to-open-weight-models — accessed 2026-11-23
Tech Policy Press, Will China crack down on open-weight models? (Graham Webster), 17 August 2026 — https://techpolicy.press/will-china-crack-down-on-open-weight-models — accessed 2026-11-23
TechCrunch, Open-weight AI models are catching up to the frontier; the safety gap remains, 4 August 2026 — https://techcrunch.com/2026/08/04/open-weight-ai-models-are-catching-up-to-the-frontier-the-safety-gap-remains/ — accessed 2026-11-23
Reuters via bdnews24, US weighs rule requiring companies to disclose use of Chinese AI models, 18 November 2026 — https://bdnews24.com/world/americas/nz7l0a0g1i — accessed 2026-11-23
Al Jazeera, US orders Anthropic to disable AI models for all foreign nationals, June 2026 — https://www.aljazeera.com/economy/2026/6/14/us-orders-anthropic-to-disable-ai-models-for-all-foreign-nationals — accessed 2026-11-23
Semafor, Nvidia to buy Hugging Face for nearly 13 billion dollars, 3 September 2026 — https://semafor.com/article/09/03/2026/nvidia-to-buy-hugging-face-for-nearly-13-billion — accessed 2026-11-23
OpenRouter, The Token State of Play, 22 September 2026 — https://openrouter.ai/data/newsletter/the-token-state-of-play — accessed 2026-11-23
Hugging Face, State of Open Source on Hugging Face: Spring 2026, 17 March 2026 — https://huggingface.co/blog/huggingface/state-of-os-hf-spring-2026 — accessed 2026-11-23
Hugging Face, State of Open Models: Summer 2026 — https://huggingface.co/blog/state-of-open-models-summer-2026 — accessed 2026-11-23
Stanford CRFM, The 2025 Foundation Model Transparency Index — https://crfm.stanford.edu/fmti/December-2025 — accessed 2026-11-23
Linux Foundation, Revealing the Hidden Economics of Open Models in the AI Era (Nagle and Yue) — https://www.linuxfoundation.org/blog/revealing-the-hidden-economics-of-open-models-in-the-ai-era — accessed 2026-11-23
RAND, Securing AI Model Weights (Nevo et al.), May 2024 — https://www.rand.org/pubs/research_reports/RRA2849-1.html — accessed 2026-11-23
Gade, Lermen, Rogers-Smith and Ladish, BadLlama, arXiv:2311.00117 — https://arxiv.org/abs/2311.00117 — accessed 2026-11-23
Epoch AI, How far behind are open models?, 4 November 2024 — https://epoch.ai/blog/open-models-report — accessed 2026-11-23
Volkov, Badllama 3, arXiv:2407.01376 — https://arxiv.org/abs/2407.01376 — accessed 2026-11-21 (verified in the AI Alignment refresh)
TechCrunch, Meta says its Llama AI models have been downloaded 1.2B times, 29 April 2025 — https://techcrunch.com/2025/04/29/meta-says-its-llama-ai-models-have-been-downloaded-1-2b-times/ — accessed 2026-11-23
Meta, Open Source AI Is the Path Forward (Mark Zuckerberg), July 2024 — https://about.fb.com/news/2024/07/open-source-ai-is-the-path-forward/ — accessed 2026-11-23
TechCrunch, Meta says it may stop development of AI systems it deems too risky, 3 February 2025 — https://techcrunch.com/2025/02/03/meta-says-it-may-stop-development-of-ai-systems-it-deems-too-risky — accessed 2026-11-23
AI Policy Institute, Poll shows voters oppose open-sourcing AI models, 13 September 2023 — https://theaipi.org/poll-shows-voters-oppose-open-sourcing-ai-models-support-regulatory-representation-on-boards-and-say-ai-risks-outweigh-benefits/ — accessed 2026-11-23
NTIA, Dual-Use Foundation Models with Widely Available Model Weights, report and recommendations, July 2024 — https://www.ntia.gov/programs-and-initiatives/artificial-intelligence/open-model-weights-report/policy-approaches-recommendations/recommendations — accessed 2026-11-23
The White House, America’s AI Action Plan, July 2025 — https://www.whitehouse.gov/wp-content/uploads/2025/07/Americas-AI-Action-Plan.pdf — accessed 2026-11-23
OpenAI, Introducing gpt-oss, 5 August 2025 — https://openai.com/index/introducing-gpt-oss/ — accessed 2026-11-23
International AI Safety Report 2026 — https://internationalaisafetyreport.org/ — accessed 2026-11-23
Kapoor, Bommasani et al., On the Societal Impact of Open Foundation Models, arXiv:2403.07918 — https://arxiv.org/abs/2403.07918 — accessed 2026-11-23
Narayanan and Kapoor, AI as Normal Technology, Knight First Amendment Institute — https://knightcolumbia.org/content/ai-as-normal-technology — accessed 2026-09-24 (verified in the Frontier AI Regulation research)
Özcan, Petropoulos and Reddel, Beyond the Binary: A nuanced path for open-weight advanced AI, arXiv:2602.19682 — https://arxiv.org/abs/2602.19682 — accessed 2026-11-23
Stanford HAI, Open-weight models aren’t enough (James Landay), 4 August 2026 — https://hai.stanford.edu/news/open-weight-models-arent-enough-we-need-truly-open-source-ai-models-for-science-and-society — accessed 2026-11-23
Public AI Network — https://publicai.network/ — accessed 2026-11-23
Mozilla, Creating a public counterpoint for AI, 30 September 2024 — https://blog.mozilla.org/mozilla/ai/public-ai-counterpoint/ — accessed 2026-11-23
Sanders and Schneier, Rewiring Democracy Now: Switzerland shows us an alternative to corporate AI, 21 February 2026 — https://www.schneier.com/essays/archives/2026/02/rewiring-democracy-now-switzerland-shows-us-an-alternative-to-corporate-ai.html — accessed 2026-11-23
Widder, Whittaker and West, Why “open” AI systems are actually closed, and why this matters, Nature 635 (2024), abstract — https://ui.adsabs.harvard.edu/abs/2024Natur.635..827W — accessed 2026-11-23
MIT Technology Review, Yann LeCun’s new venture AMI Labs, 22 January 2026 — https://www.technologyreview.com/2026/01/22/1131661/yann-lecuns-new-venture-ami-labs/ — accessed 2026-11-23
The ATOM Project (American Truly Open Models) — https://www.atomproject.ai/ — accessed 2026-11-23
Open Source Initiative, Open Source AI Definition — https://opensource.org/ai/open-source-ai-definition — accessed 2026-11-23
Open Source Initiative, OSAID endorsements — https://opensource.org/ai/endorsements — accessed 2026-11-23
SaferAI, Frontier Risk Management Tracker — https://tracker.safer-ai.org/ — accessed 2026-11-23
Ai2 OLMo — https://allenai.org/olmo — accessed 2026-11-23
Ollama — https://ollama.com/ — accessed 2026-11-23
