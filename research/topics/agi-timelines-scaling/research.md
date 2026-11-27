# AGI Timelines — research

## Overview

AGI timelines is the question of when, if ever, AI systems will be able to do most of the cognitive work humans do, and of what will get them there. It covers capability forecasts (the dates that lab leaders, researchers, superforecasters and forecasting communities give for AI matching or surpassing human professionals, and the definitions those dates depend on), the scaling hypothesis (the bet that more compute, more data and more reinforcement learning on today’s architectures will keep producing more general capability, against the view that new ideas are needed), and the feedback loop in which AI systems take over the work of improving AI, insofar as it moves the date. It deliberately excludes whether such systems would be safe or controllable, which belongs to AI Existential Risk and AI Alignment, how governments should regulate them, which belongs to Frontier AI Regulation, what they will do to jobs, which belongs to AI and the Future of Work, and whether they could be conscious, which belongs to AI Consciousness. It touches takeoff speed only where the speed of AI-driven research is the reason someone gives the date they do.

Why now: on November 5, 2026 METR, the independent evaluator, published an assessment from inside Anthropic estimating that the company was improving model capabilities on well-specified tasks about 1.9 times as fast as it had from March 2024 to October 2025 (95 percent interval 1.5 to 2.8), and guessing that about 80 percent of the acceleration came from Anthropic’s own use of AI in its research (METR, https://metr.org/blog/2026-11-05-anthropic-ai-rd-acceleration-assessment/). Five days later the AI Futures Project, the group behind the AI 2027 scenario, published “Q3.5 Timelines Update: Looks Like the Intelligence Explosion Will Happen in 2027 After All,” in which all its forecasters said a Superhuman AI Researcher “will likely arrive at some point in 2027,” assuming no deliberate slowdown; Daniel Kokotajlo moved his median from December 2028 to May 2027 (AI Futures Project, https://blog.aifutures.org/p/q35-timelines-update-looks-like-the). On November 20 METR’s quarterly update put the length of task the best public agents finish half the time at about 40 hours of skilled human work, doubling roughly every 3.6 months (METR, https://metr.org/blog/2026-11-20-q4-2026-capability-update/). The backdrop is OpenAI’s September 3 launch of GPT-6 Astra, at which its president, Greg Brockman, said “It’s not unreasonable to feel that we are now in the AGI era” (Fortune, https://www.fortune.com/2026/09/03/openai-debuts-gpt-6-astra-computer-use-greg-brockman-says-start-of-agi/), while the ARC Prize Foundation, whose benchmark OpenAI featured, wrote “we are not claiming that it is AGI” (ARC Prize, https://arcprize.org/blog/astra).

The debate is live because the forecasts now disagree by decades about something that may be a few years away. The heads of the leading labs speak of one to three years: Anthropic’s Dario Amodei said in February 2026 that models amounting to “a country of geniuses in the data center” could come “in one to two years” (Dwarkesh Podcast, https://www.dwarkesh.com/p/dario-amodei-2), and Google DeepMind’s Demis Hassabis was reported in October 2026 to expect AGI within two to three years (Free Press Journal, citing The Wall Street Journal, https://www.freepressjournal.in/tech/its-soon-ai-mastermind-demis-hassabis-now-expects-agi-within-three-years). A broad panel of experts surveyed by the Forecasting Research Institute in April and May 2026 gave a median of 2050 for a demanding definition of AGI, and superforecasters 2047 (https://leap.forecastingresearch.org/reports/wave8). In a 2025 survey by the Association for the Advancement of Artificial Intelligence, 76 percent of 475 respondents said scaling up current approaches was unlikely or very unlikely to yield AGI (AAAI, https://aaai.org/wp-content/uploads/2025/03/AAAI-2025-PresPanel-Report-FINAL.pdf). The participants are the frontier labs and the forecasters who extrapolate their trends, researchers who think scaling must be joined by a few more breakthroughs, those who think large language models are the wrong road altogether (Yann LeCun, Gary Marcus, Richard Sutton), economists and forecasters who expect automation to arrive over decades, and those who think “AGI” is the wrong thing to be dating at all (Arvind Narayanan and Sayash Kapoor, Microsoft’s Satya Nadella). Hundreds of billions of dollars a year in data center spending rest on the answer.

## Basics

Label: Length of task frontier AI agents complete half the time
Value: 40
Unit: hours of skilled human working time
Viz: ranked
Series: GPT-4 (2023) 0.06; Claude 3.7 Sonnet (2025) 1.0; o3 (2025) 2.0; GPT-5 (2025) 3.6; Claude Opus 4.5 (2025) 5.3; GPT-6 Astra (2026) 40 (highlight). All in hours. Rows differ in task suite: the first five are METR’s Time Horizon 1.1 estimates (3.5, 60, 121, 214 and 320 minutes); the 2026 row is METR’s November 2026 estimate on its pooled original and harder (TH1.1 plus TH2) suites.
Data year: 2026
Source label: METR, Time Horizon 1.1 (January 29, 2026) and Q4 2026 capability update (November 20, 2026)
Source URL: https://metr.org/blog/2026-11-20-q4-2026-capability-update/ (earlier rows: https://metr.org/blog/2026-1-29-time-horizon-1-1/)
Note: The best public AI agents in November 2026 finished, half the time, software and research tasks that take a skilled human about 40 hours; in 2023 the figure was about three and a half minutes.
Context: METR’s “time horizon” is the length of task, measured by how long it takes skilled human professionals, at which an AI agent succeeds 50 percent of the time. It has become the most cited single trend in the timelines debate because it measures something like autonomy rather than knowledge. In METR’s November 2026 update GPT-6 Astra’s estimate is 40 hours with a 95 percent interval of 13 to 2,645 hours, and Opus 5.5’s 39 hours (12 to 1,253); the intervals are wide because few tasks are that long. The doubling time across both suites is about 3.6 months (95 percent interval 2.08 to 4.94), against 130.8 days since 2023 and 196.5 days since 2019 on the earlier suite. Models saturated the original suite, which includes tasks up to 30 hours, within about a year, which is why METR built a harder one; METR notes that naive extrapolation would reach its longest task threshold, 200 hours, around July 2027. METR writes that “current public evidence is insufficient to rule out drastic AI R&D acceleration in the next couple of years,” while also finding no strong acceleration across public frontier models on its composite capability index. Those who expect long timelines point out that these are well-specified, automatically scored tasks, and that success at 50 percent is far from the reliability real jobs require.

Label: Expert and superforecaster median year for AGI
Value: 2050
Unit: year (median forecast, experts)
Viz: ranked
Series: Superforecasters 2047; Experts 2050 (highlight); Public 2055
Data year: 2026
Source label: Forecasting Research Institute, Longitudinal Expert AI Panel (LEAP), Wave 8 (surveyed April 20 to May 11, 2026)
Source URL: https://leap.forecastingresearch.org/reports/wave8
Note: Asked in spring 2026 when a majority of the panel would agree a commercially available AI system meets a demanding definition of AGI, the median expert said 2050 and the median superforecaster 2047.
Context: The Forecasting Research Institute’s panel mixes computer scientists, industry researchers, economists and think-tank staff (205 experts in this wave, 44, 37, 49 and 75 respectively), with 52 superforecasters and 601 members of the public. The bar is high: an AI that can outperform the 90th-percentile professional in every primarily non-physical occupation, on at least 90 percent of the economically useful tasks they perform, at no more than five times the cost of human labor. The year is conditional on that happening before 2100, which the median expert and the median superforecaster each put at 80 percent and the median member of the public at 65 percent. The experts’ middle half runs from 2039 to 2065, and a quarter of superforecasters’ probability falls before 2036. The same wave’s median expert expected AI to reach 80 percent success on software tasks of eight hours or more by about 2030, and the median superforecaster by 2028. The institute’s interim accuracy review in September 2026, as reported by The Decoder, found the panel’s experts had significantly underestimated recent benchmark progress, which short-timeline forecasters read as a reason to discount panel medians and the panel’s defenders read as a miss on benchmarks rather than on general capability.

Label: AI researchers’ 50 percent year for machines outperforming humans at every task
Value: 2047
Unit: year (aggregate forecast)
Viz: ranked
Series: 2022 survey 2060; 2023 survey 2047 (highlight)
Data year: 2023
Source label: Grace et al., Thousands of AI Authors on the Future of AI (AI Impacts, 2,778 respondents), arXiv:2401.02843
Source URL: https://arxiv.org/abs/2401.02843
Note: Surveyed in late 2023, published AI researchers put a 50 percent chance on unaided machines outperforming humans in every possible task by 2047, thirteen years earlier than the same survey found a year before.
Context: The Expert Survey on Progress in AI asked people who had published at six top machine learning venues, and is the largest survey of its kind. The aggregate forecast gave a 10 percent chance of machines outperforming humans at every task by 2027 and 50 percent by 2047, assuming science continues undisrupted. Asked instead when all human occupations would become fully automatable, the same respondents gave 10 percent by 2037 and 50 percent by 2116, down from 2164 a year earlier. The gap of about seventy years between the two framings of nearly the same question is itself the most quoted finding: researchers’ answers depend heavily on wording, which those skeptical of survey forecasts take as evidence that the respondents have no stable model, and others take as a sign that “every task” and “every job” are read very differently. The survey was fielded in late 2023, before reasoning models and capable agents.

Label: Stated arrival dates from leading figures
Value:
Unit: approximate year implied (each person’s own definition)
Viz: ranked
Series: Sam Altman, OpenAI (August 2026) 2026; Daniel Kokotajlo, AI Futures Project (November 2026) 2027; Dario Amodei, Anthropic (February 2026) 2027 to 2028; Shane Legg, Google DeepMind (November 2026) 2027 to 2028; Demis Hassabis, Google DeepMind (October 2026) 2028 to 2029; Ilya Sutskever, Safe Superintelligence (November 2025) 2030 to 2045; Ege Erdil, Mechanize (April 2025) about 2045. Rows differ in source, date and definition.
Data year: 2025 to 2026
Source label: Each row’s own source (TIME via The Decoder; AI Futures Project; Dwarkesh Podcast; University of Auckland; Free Press Journal citing The Wall Street Journal; Dwarkesh Podcast; Epoch AI Gradient Updates)
Source URL: https://blog.aifutures.org/p/q35-timelines-update-looks-like-the ; https://www.dwarkesh.com/p/dario-amodei-2 ; https://www.auckland.ac.nz/en/news/2026/11/11/shane-legg-google-university-auckland-business-school.html ; https://www.freepressjournal.in/tech/its-soon-ai-mastermind-demis-hassabis-now-expects-agi-within-three-years ; https://www.dwarkesh.com/p/ilya-sutskever-2 ; https://epoch.ai/gradient-updates/the-case-for-multi-decade-ai-timelines ; https://the-decoder.com/sam-altman-says-openai-will-have-agi-by-the-end-of-2026-if-you-accept-his-definition/
Note: Leading figures’ stated dates for AGI or its near equivalents run from the end of 2026 to about 2045, and each uses a different definition.
Context: Sam Altman told TIME in August 2026 that OpenAI was “not quite yet” at AGI but expected an internal system he would call AGI by the end of the year (as reported by The Decoder). Kokotajlo’s row is his median for a Superhuman AI Researcher, a system a lab would rather keep than its best human researchers; his median for AI that dominates top experts at all white-collar work is September 2027. Amodei said in February 2026 that “a country of geniuses in the data center” could come “in one to two years,” called one to three years roughly a 50/50 matter, and put 90 percent on it within ten years. Legg, Google DeepMind’s co-founder, has given 50 percent for human-level machine intelligence by 2028 since 2009 and said in November 2026 “I think we’re getting very close and will probably reach this next year or the year after,” with a minimal bar of an AI that can do all the cognitive tasks people can typically do. Hassabis, after years of saying five to ten years, was reported by The Wall Street Journal in October 2026 to expect AGI within two to three years. Sutskever’s “5 to 20” years is for a system that learns as well as a human. Erdil’s roughly 20 years is for full automation of remote work. Yann LeCun gives no year but said in January 2026 that human-level AI is “not going to happen next year or two years from now.”

Label: Speed-up in Anthropic’s capability progress attributed largely to AI doing its research
Value: 1.9
Unit: times the March 2024 to October 2025 rate
Viz: bar
Data year: 2026
Source label: METR, Independent Assessment of AI R&D Acceleration at Anthropic in October 2026 (November 5, 2026)
Source URL: https://metr.org/blog/2026-11-05-anthropic-ai-rd-acceleration-assessment/
Note: METR estimated that in October 2026 Anthropic was improving its models on well-specified tasks about 1.9 times as fast as it had from March 2024 to October 2025, and guessed about 80 percent of that acceleration came from Anthropic’s own use of AI.
Context: This is the first outside measurement of the feedback loop at the center of short timelines: AI systems speeding up the work of building better AI systems. METR staff worked inside Anthropic from August 12 to October 29, 2026. Its benchmark-based estimate is 1.9 times (95 percent interval 1.5 to 2.8), and METR says it would not be surprised by a true figure closer to 1.3 or 3; alternative analysis choices gave 1.1 to 2.9 times, and using only non-Anthropic models about 1.4. METR reported “signs of life” for fully autonomous AI contributions to research and a significant risk of even faster acceleration over the coming year. The limits are stated in the report: Anthropic redacted most of the evidence METR found most informative, METR lacked staff-level access, Anthropic’s own staff did not agree on how much of the speed-up was due to AI, and the benchmarks used are saturating. The AI Futures Project cited this report as the main reason it moved its forecasts into 2027; those expecting longer timelines note it covers one company, rests on judgment the public cannot check, and measures well-specified tasks.

Label: AI researchers who doubt scaling current approaches will yield AGI
Value: 76
Unit: percent of respondents
Viz: radial
Data year: 2025
Source label: AAAI 2025 Presidential Panel on the Future of AI Research, community survey (475 respondents), p. 66
Source URL: https://aaai.org/wp-content/uploads/2025/03/AAAI-2025-PresPanel-Report-FINAL.pdf
Note: Of 475 respondents to the Association for the Advancement of Artificial Intelligence’s 2025 survey, 76 percent said “scaling up current AI approaches” to yield AGI is “unlikely” or “very unlikely” to succeed.
Context: The survey accompanied a report by 24 AI researchers convened by AAAI, the field’s oldest professional society, and was answered mostly by academics (67 percent; 19 percent from corporate research; about 20 percent students). It is the cleanest measure of how the broader research community, as opposed to frontier labs, views the scaling hypothesis. In the same AGI section 77 percent said they prioritize designing AI systems with an acceptable risk-benefit profile over directly pursuing AGI. The survey was fielded in late 2024 and early 2025, before reasoning-model and agent gains through 2026, and scaling proponents argue that “scaling up current approaches” now includes reinforcement learning and inference-time compute that many respondents did not have in mind. Skeptics of scaling answer that the result describes the people who build and study these systems for a living outside the labs that sell them.

Label: Growth in training compute for frontier language models
Value: 5
Unit: times per year (since 2020)
Viz: bar
Data year: 2026
Source label: Epoch AI, Trends in Artificial Intelligence (updated November 5, 2026)
Source URL: https://epoch.ai/trends
Note: The computing power used to train frontier language models has grown about fivefold each year since 2020, a doubling roughly every five months.
Context: Epoch AI, which tracks the inputs to AI, puts the 90 percent interval at 4 to 6 times a year. Compute is the core input of the scaling hypothesis: the empirical scaling laws of 2020 to 2022 showed predictable gains in model performance as compute, parameters and data grew together. Epoch’s summary lists Grok 4, at roughly 5 times 10 to the 26th power floating point operations, as the largest known training run (https://epoch.ai/llms.txt); GPT-4 in 2023 is estimated at about 2 times 10 to the 25th, roughly 25 times less. Epoch also reports that AI chip performance per dollar has grown 49 percent a year since 2023 and that the largest AI data center, SpaceXAI’s Colossus 2 in Memphis, holds an estimated 1.1 million H100-equivalent chips. Whether compute keeps growing this fast through 2030 depends on power, chips and money; whether more compute keeps buying general capability is the scaling question itself.

Label: GPT-6 Astra on ARC-AGI-3 under two test setups
Value: 62.7
Unit: percent of environments solved (standard harness)
Viz: ranked
Series: Standard harness 62.7 (highlight); OpenAI’s provider adapter harness 99.9; Humans 100
Data year: 2026
Source label: ARC Prize Foundation, GPT-6 Astra on ARC-AGI-3 (September 3, 2026)
Source URL: https://arcprize.org/blog/astra
Note: On ARC-AGI-3, a test of solving unfamiliar interactive puzzles that humans can solve, GPT-6 Astra scored 62.7 percent under the benchmark’s standard setup and 99.9 percent with the memory and tooling OpenAI designed for it.
Context: The ARC Prize Foundation, founded by François Chollet and Mike Knoop, builds tests meant to measure the ability to learn new skills efficiently rather than recall knowledge; it says humans can solve all of ARC-AGI-3’s environments. OpenAI’s launch post headlined the 99.9 percent provider adapter score at high reasoning effort ($18,817 for the run); the provider-neutral standard harness gave 62.7 percent at maximum effort ($26,098). ARC Prize wrote that Astra “represents meaningful progress towards generalization” but that “we are not claiming that it is AGI,” noting the benchmark consists of closed, deterministic worlds. With its own harness Astra used fewer actions than the human baseline on 96 percent of levels. The 37-point gap between the two setups is itself contested: those who see scaling as on track read the adapter score as the real capability of the system as deployed, and those who doubt it read the standard score as the fairer measure of general learning.

Label: Freelance projects AI agents complete as well as a professional
Value: 15.8
Unit: percent of projects (automation rate)
Viz: ranked
Series: Gemini 3 Pro 1.25; Grok 4 2.08; GPT-5.2 2.50; Opus 4.6 (Claude Cowork) 4.17; GPT-5.5 6.3; Opus 4.8 8.3; Fable 5 15.8 (highlight)
Data year: 2026
Source label: Center for AI Safety and Scale AI, Remote Labor Index update (July 1, 2026)
Source URL: https://safe.ai/blog/significant-increase-in-digital-labor-automation
Note: On the Remote Labor Index, real paid freelance projects judged by humans against a professional’s deliverable, the best AI agent in July 2026 matched or beat the professional on 15.8 percent of projects, up from a field best of 2.5 percent when the benchmark was released in October 2025.
Context: The Remote Labor Index, built by the Center for AI Safety and Scale AI, uses whole projects from freelance platforms, such as design, video, data and writing jobs, rather than tasks written for AI. It is the most direct measure of the gap between benchmark scores and economically complete work. The automation rate is the share of projects where human evaluators judged the AI’s work as good as or better than the professional’s; agents had up to 24 hours and a budget of $50 per project ($150 for Fable 5). The authors found an AI judge overstated the newest models (17.9 percent for GPT-5.5 against 6.25 percent by human judges), so they keep human evaluation. Short-timeline forecasters point to the sixfold rise in nine months; long-timeline forecasters point out that the best agent still fails about five projects in six. Scores for models released after July 2026 were not found.

Label: How fast the compute needed for a given language model performance falls
Value: 8
Unit: months to halve
Viz: bar
Data year: 2024
Source label: Epoch AI, Algorithmic Progress in Language Models (March 12, 2024)
Source URL: https://epoch.ai/blog/algorithmic-progress-in-language-models
Note: Better algorithms cut the compute needed to reach a given language model performance in half roughly every eight months between 2012 and 2023.
Context: Epoch AI’s estimate has a 95 percent interval of 5 to 14 months, meaning algorithmic improvements alone multiply effective compute severalfold a year on top of the growth in physical compute. The same analysis attributes about 60 to 95 percent of performance gains over the period to more compute and data, and 5 to 40 percent to algorithms. The number matters to both sides: scaling proponents count algorithmic progress as part of “scaling” and the main input that AI researchers could themselves accelerate, while those expecting long timelines point out that most of the historical gain came from spending more, which is limited by power, chips and capital.

Label: Capital spending by the largest AI infrastructure companies
Value: 803 to 828
Unit: billion US dollars (2026, forecast)
Viz: bar
Data year: 2026
Source label: Hargreaves Lansdown (Business Insider), AI hyperscalers are expected to finish the year spending $828 billion on capex (October 30, 2026)
Source URL: https://www.hl.co.uk/news/ai-hyperscalers-are-expected-to-finish-the-year-spending-a-whopping-828-billion-on-capex
Note: After third-quarter earnings, Amazon, Alphabet, Meta, Microsoft and SpaceX were forecast to spend $803 billion to $828 billion on capital in 2026, mostly on AI data centers.
Context: The figure tallies company guidance after October 2026 earnings: Amazon kept about $220 billion in cash capital spending, Microsoft guided to about $170 billion for the calendar year, and SpaceX, which now includes xAI, about $48.1 billion; the five spent about $227 billion in the third quarter alone. The International Energy Agency noted in June 2026 that capital spending by five technology companies, largely on data centers, now exceeds global investment in oil and gas production (IEA, Key questions on energy and AI, https://asiacleanenergyforum.adb.org/wp-content/uploads/2026/06/Key-questions-on-energy-and-AI.pdf). Epoch AI separately counts more than $370 billion raised by frontier AI labs and OpenAI’s annualized revenue growing 3.2 times a year since 2024 (https://epoch.ai/trends). The spending is a bet that scaling continues; whether revenue keeps pace decides whether it can be sustained, and Gary Marcus argued in June 2026 that the race to amass computing power will eventually hit a wall (Fortune, https://fortune.com/2026/06/29/hyperscalers-data-centers-gary-marcus-airlines-small-margins-intense-competition-high-expenses/).

Label: Largest training run Epoch AI judges feasible by 2030
Value: 2 × 10^29
Unit: floating point operations
Viz: bar
Data year: 2024
Source label: Epoch AI, Can AI Scaling Continue Through 2030? (August 20, 2024)
Source URL: https://epoch.ai/blog/can-ai-scaling-continue-through-2030
Note: Epoch AI estimated that training runs of 2 × 10^29 operations, about 10,000 times GPT-4’s, will likely be feasible by the end of the decade.
Context: The analysis checked four constraints. Power is the most likely to bind first: single campuses of 1 to 5 gigawatts could support runs of about 10^28 to 3 × 10^29 operations, and training spread across sites more. Chip manufacturing could supply around 100 million H100-equivalents for training (range 20 to 400 million). Data, counting text, images, video and audio, would allow runs of roughly 6 × 10^28 to 2 × 10^32, and the minimum time to process each batch sets a ceiling of about 3 × 10^30 to 10^32. Epoch stresses this is feasibility, not a prediction that anyone will spend the money. The scale-up from GPT-2 to GPT-4 was of similar size, which is why scaling proponents read the estimate as room for another jump of that kind before any physical wall.

Label: Growth in the cost to train frontier language models
Value: 3.5
Unit: times per year (since 2020)
Viz: bar
Data year: 2026
Source label: Epoch AI, Trends in Artificial Intelligence (updated November 5, 2026)
Source URL: https://epoch.ai/trends
Note: The cost of training the most advanced language models has grown about three and a half times a year since 2020, doubling roughly every seven months.
Context: Cost grows more slowly than compute because chips get cheaper per operation, about 49 percent better performance per dollar each year since 2023 by Epoch’s estimate. Epoch puts a gigawatt-scale data center at about $38 billion in up-front capital and about two years to build. At these rates the largest single training runs move from billions toward tens of billions of dollars before 2030, which is why the question of whether scaling can continue is partly a question of whether AI revenue grows fast enough to fund it.

Label: Stock of human-written public text usable for training
Value: 300
Unit: trillion tokens
Viz: range
Data year: 2024
Source label: Epoch AI, Will We Run Out of Data? Limits of LLM Scaling Based on Human-Generated Data (June 6, 2024)
Source URL: https://epoch.ai/blog/will-we-run-out-of-data-limits-of-llm-scaling-based-on-human-generated-data
Note: Epoch AI estimates the effective stock of public human-written text at around 300 trillion tokens, which frontier models would fully use between 2026 and 2032 if trends continued.
Context: Data was the scaling constraint most discussed in 2024: if model size and data must grow together, a finite internet sets a limit. The answers since have come from outside human text: reinforcement learning on problems with checkable answers, synthetic data generated by models, multimodal data, and training agents in simulated work environments, which companies including Mechanize now build. Scaling proponents say these have already replaced the data wall; skeptics say text was the cheap fuel and the substitutes are costlier and narrower.

Label: Electricity used by data centers worldwide
Value: 415
Unit: terawatt hours (2024)
Viz: ranked
Series: 2024 415 (highlight); 2030 projection (Base Case) 945
Data year: 2024
Source label: International Energy Agency, Energy and AI (April 2025)
Source URL: https://www.iea.org/reports/energy-and-ai/executive-summary
Note: Data centers used about 415 terawatt hours of electricity in 2024, around 1.5 percent of the world’s total, and the IEA’s base case has that roughly doubling to about 945 by 2030.
Context: The IEA expects AI-optimized data centers to drive most of the growth, with China and the United States accounting for nearly 80 percent of it; its range for 2035 runs from 700 to 1,700 terawatt hours. In a June 2026 briefing the agency said data center electricity demand grew by almost 20 percent in 2025, and that its 2030 outlook remains close to its 2025 trajectory because bottlenecks in gas turbines, transformers, grid connections, memory and advanced packaging constrain the near term (IEA, Key questions on energy and AI, https://asiacleanenergyforum.adb.org/wp-content/uploads/2026/06/Key-questions-on-energy-and-AI.pdf). The IEA’s 2026 update reportedly puts 2025 use at 485 terawatt hours rising to 950 by 2030 [unverified]. For timelines, power is the physical input that cannot be accelerated by better algorithms, which is why those expecting slower progress cite it.

Label: Metaculus community forecast for the date of general AI
Value: 2030 [unverified]
Unit: year (community median)
Viz: bar
Data year: 2026
Source label: Metaculus, When will the first general AI system be devised, tested, and publicly announced?
Source URL: https://www.metaculus.com/questions/5121/date-of-artificial-general-intelligence/
Note: The Metaculus forecasting community’s median for the first general AI system is around 2030 [unverified].
Context: Metaculus questions are the most widely cited crowd forecasts on AGI. The live value could not be read: the page returned 403 to automated fetching, and secondary trackers gave conflicting snapshots for late 2026 (around September 2030 in early November 2026 by one tracker; earlier snapshots in 2025 and early 2026 ranged from 2031 to 2033). The question’s criteria combine an adversarial Turing test, general robotic manipulation and expert-level performance on broad knowledge and coding tests [unverified: from memory of the question page]. Include only if the editor can read the current median off the page.

## Questions

Question: Will scaling up today’s methods reach AGI, or does it need ideas nobody has yet?
Tag: empirical
Poles: Scaling suffices / New ideas needed
Why contested: The scaling hypothesis is an extrapolation from regularities that have held for a decade: more compute, data and training reliably bought more capability. Whether that continues to general intelligence, or levels off short of it, is the question every forecast rests on, and the two sides read the same 2024 to 2026 record in opposite ways.
Case for scaling suffices: Every wall predicted for scaling has been crossed by scaling something. When pretraining gains slowed in 2024, reinforcement learning on checkable problems and more thinking time at inference took over, and the result was reasoning models, a mathematical olympiad gold medal in 2025 and agents whose time horizon now doubles in under four months. None of this needed a new architecture; it needed more compute applied in new places, which is what Richard Sutton’s “bitter lesson” predicted: general methods that use computation beat clever designs. The data wall was answered by synthetic data and simulated work environments. The compute is still coming, at five times a year, with room for runs ten thousand times larger than GPT-4 before 2030. The people inside the labs, who see the next systems before anyone else, are the ones with the shortest timelines.
Case for new ideas needed: Scaling laws describe how prediction error falls with compute, not how close a system is to general intelligence, and the capabilities that matter most are the ones that have not scaled. Systems still cannot learn continually after deployment, plan over long periods or behave consistently, the three gaps Google DeepMind’s Demis Hassabis named in February 2026; they generalize “dramatically worse than people,” in Ilya Sutskever’s words; and the best agent completed about one freelance project in six to professional standard in July 2026. Each recent advance that is called scaling was in fact a new idea: reasoning models needed new training methods, not just more chips. In a 2025 survey 76 percent of AAAI respondents said scaling current approaches was unlikely to yield AGI. A curve that has bent before can bend again, and an extrapolation that has worked for ten years says nothing about what lies past the edge of the data.

Question: Will AI that does its own research compress the path to AGI into a few years?
Tag: empirical
Poles: Compounding loop / Bottlenecked progress
Why contested: The shortest timelines depend less on any single model than on a feedback loop: once AI systems do much of the work of improving AI, the number of researchers is set by compute rather than hiring, and progress compounds. In 2026 the loop moved from theory to measurement, and the first measurements are contested.
Case for compounding loop: The loop is visible. METR measured Anthropic improving its models about 1.9 times as fast in October 2026 as in the eighteen months before, and guessed about 80 percent of that came from AI doing the work. OpenAI said in September 2026 it had built an automated research intern and is aiming for a fully automated AI researcher by March 2028. AI systems can be copied without limit, run faster than people, work without rest, and improve the algorithms that already halve the compute needed for a given result about every eight months. If even part of AI research can be handed to AI, each generation shortens the time to the next; that is why the AI Futures Project, after the METR report, expects a superhuman AI researcher in 2027 and why METR says a drastic acceleration cannot be ruled out in the next couple of years.
Case for bottlenecked progress: Research is gated by experiments, and experiments are gated by compute and real-world data that AI cannot conjure. Automating AI research is likely as hard as automating remote work in general, Ege Erdil argues, so a software-only intelligence explosion is unlikely before AI has transformed the economy that pays for the chips. The METR assessment covers one company, relies on evidence Anthropic mostly redacted, and found Anthropic’s own staff disagreeing about how much of the speed-up was due to AI; METR’s quarterly update found no strong acceleration across public frontier models. Gigawatt data centers still take about two years to build, and the International Energy Agency reports turbines, transformers and grid connections constraining the buildout. Coding faster is not the same as discovering faster.

Question: Do benchmark gains measure progress toward general intelligence?
Tag: empirical
Poles: Real progress signal / Narrow test-taking
Why contested: Almost all the evidence for rapid progress comes from benchmarks, and benchmarks are being saturated within months of release. Whether rising scores track the abilities that matter in open-ended work, or reflect training aimed at the tests, determines how much the trend lines should move anyone.
Case for real progress signal: The benchmarks that matter have been designed to resist gaming and to look like real work: METR’s tasks are drawn from software and research jobs and measured in human hours, FrontierMath problems are new and written by research mathematicians, ARC-AGI-3 uses games no model has seen, and the Remote Labor Index uses paid freelance projects. Progress shows up on all of them at once, and in the market: OpenAI’s revenue has grown about 3.2 times a year since 2024 by Epoch AI’s count, which is hard to explain if the systems cannot do useful work. Every time a skeptic has named a task AI cannot do, the next generation has done it.
Case for narrow test-taking: When a measure becomes a target it stops being a good measure, and frontier labs now train against the benchmarks the field watches. Scores depend on the test setup: GPT-6 Astra scored 99.9 percent on ARC-AGI-3 with OpenAI’s harness and 62.7 percent with the standard one. The tasks that saturate fastest are well specified and automatically scored, while open-ended work lags: the best agent matched a professional on about 16 percent of freelance projects, and 80,000 Hours’ Rob Wiblin described AI-run shops losing money in 2026 trials. Systems that solve olympiad problems still make elementary errors when a question is rephrased, the “jaggedness” Hassabis says a general system should not have. A benchmark measures the benchmark.

Question: Can compute, power and money keep growing at current rates through 2030?
Tag: empirical
Poles: Buildout continues / Physical limits bind
Why contested: The scaling path assumes training compute keeps growing about fivefold a year. That requires chips, electricity and capital at a scale no industry has raised this fast, and each input has its own bottleneck and its own skeptics.
Case for buildout continues: The money is already committed: the largest AI infrastructure companies were forecast to spend $803 billion to $828 billion in 2026, more than the world invests in oil and gas production, and frontier labs have raised more than $370 billion. Epoch AI found runs of 2 × 10^29 operations, about ten thousand times GPT-4, likely feasible by 2030 on power, chips, data and latency. Chips get about 49 percent more performance per dollar each year, and revenue is growing fast enough that the spending is being paid for by customers, not only investors. The constraints are engineering problems with known solutions: build power plants, spread training across sites, add fabs.
Case for physical limits bind: Each input is hitting real limits. The IEA reports gas turbines, transformers, grid connections, memory and advanced packaging all constraining data center deployment, and its 2030 outlook has barely moved despite the spending boom. The cost of the largest training runs grows about 3.5 times a year, so a few more doublings put single runs in the tens of billions of dollars, which only works if revenue keeps compounding. Gary Marcus compares the hyperscalers to airlines: heavy capital, similar products, thin margins. If the investment cycle turns, the trend line that every short timeline extrapolates turns with it.

Question: Whose forecasts deserve more weight: people at the frontier, or broad panels with track records?
Tag: empirical
Poles: Frontier insiders / Broad panels
Why contested: The people building the systems give dates in the late 2020s; broad panels of experts and superforecasters give medians around 2047 to 2050. Both groups have been wrong before, in opposite directions, and choosing between them is most of what a reader is doing when they form a view.
Case for frontier insiders: Insiders see systems months before anyone else and watch the internal metrics that drive their forecasts. Outsiders have been too slow, repeatedly: the Forecasting Research Institute’s own interim review in September 2026 found its expert panel had significantly underestimated benchmark progress, and the researcher survey’s median for machines beating humans at every task moved thirteen years earlier between 2022 and 2023. Shane Legg has forecast 2028 since 2009 and looks closer to right every year. A panel median averages many people who are not watching closely; the trend lines are public, and those who extrapolate them have been right more often than those who expected them to break.
Case for broad panels: Insiders have every incentive to say AGI is near, because it raises money and attracts talent, and the people who believe it are the ones who choose to work at labs. AI has a long record of confident near-term predictions by its leading figures, from the 1950s onward, that did not come true. Broad panels of experts and superforecasters, who are scored on accuracy and have no stake in a particular company, still put the median decades out after seeing the same trends. The insiders’ own dates also keep shifting with the definition: OpenAI’s president said “AGI era” in September 2026 while its chief executive said “not quite yet” a week earlier. Aggregated, independent judgment beats the most confident individual.

Question: Is AGI a meaningful threshold to put a date on?
Tag: value
Poles: Meaningful milestone / Misleading concept
Why contested: Every forecast depends on a definition, and the definitions differ by decades: an AI that can do typical cognitive tasks, one that beats the 90th-percentile professional at nearly everything at comparable cost, one that can do the job of the best AI researcher, one that adds 10 percent a year to world growth. Whether “AGI” names a real point worth forecasting or a moving label is a choice about what to measure.
Case for meaningful milestone: There is a real difference between tools that help people do cognitive work and systems that can do nearly all of it, including improving themselves, and that difference is what matters for everything downstream. Definitions can be made precise and checked: the Forecasting Research Institute, Metaculus and the AI Futures Project each publish operational criteria. A fuzzy threshold can still be important, as a pandemic or a recession is; arguing about the edges does not make the middle disappear. Refusing to name the milestone leaves people unprepared for exactly the change they most need to see coming.
Case for misleading concept: Within eight days in 2026 OpenAI’s chief executive said OpenAI was “not quite yet” at AGI, its president welcomed the “AGI era,” and the benchmark it cited said it was not claiming AGI. A term that can mean all of those things measures nothing. Arvind Narayanan and Sayash Kapoor argue AGI “is not a milestone because it is not actionable” and can only be identified in hindsight, Satya Nadella calls self-declared AGI milestones “nonsensical benchmark hacking,” and the contractual AGI trigger between Microsoft and OpenAI was replaced in April 2026 by payments “independent of OpenAI’s technology progress.” AI capability is jagged, rising on some tasks and stalling on others, so there is no single crossing to date; what can be measured is particular capabilities and their adoption.

Question: Once AI can do most cognitive tasks, how quickly will it change what the economy produces?
Tag: empirical
Poles: Within years / Over decades
Why contested: Many definitions of AGI are economic (most valuable work, full automation, a jump in growth), so the speed of adoption is part of the date, not only a consequence of it. Software spreads instantly, but organizations, laws and habits do not.
Case for within years: Digital work needs no factories: a system that can do a job can be copied to every computer that pays for it. AI adoption and revenue have grown faster than any previous technology, and AI systems that can run a business, write software and manage other AI systems remove the human bottlenecks that slowed earlier technologies. Once AI does AI research, the capability gains compound faster than any adoption lag, so the economy will be pulled along whether institutions are ready or not.
Case for over decades: Diffusion “occurs at human (and societal) timescales,” as Narayanan and Kapoor put it, and every general-purpose technology so far, from electricity to computing, took decades to show up in productivity. Daron Acemoglu has said he does not expect any occupation that exists today to be eliminated in five or ten years. Most work involves physical tasks, regulation, liability, trust and coordination that capability alone does not solve, and AI-run businesses in 2026 trials still lost money. The date when a system could do a job and the date when the job is done by systems are far apart.

Question: When credible forecasts range from 2027 to 2050, which end should people plan around?
Tag: value
Poles: Prepare for early / Plan on the median
Why contested: No evidence will settle the date before it arrives, so individuals, companies and institutions have to choose now how much weight to give the early end of the range. This is a question about the costs of different kinds of error, not about the forecasts themselves.
Case for prepare for early: The costs are lopsided. Preparing for an arrival that comes late wastes some effort; failing to prepare for one that comes early could mean the most important transition in history arrives with institutions, careers and plans built for a world that no longer exists. Even the cautious panels give real probability to the near term: a quarter of superforecasters’ probability falls before 2036, and lab leaders put near-even odds on the next few years. Planning on the median when the distribution is this wide is planning to be surprised.
Case for plan on the median: Planning around the earliest claims has a cost too: it moves money into an investment bubble, steers students away from careers that will still exist, and spends public attention on a forecast that has been wrong for seventy years. Overreacting to the most confident voices rewards the people with the most to gain from being believed. A sound plan works across the range, building flexible skills and institutions that adapt as evidence arrives, rather than betting on a date that the people offering it cannot agree on.

## Positions

Camp: Expect AGI within a few years from scaling and AI-built AI
Adherents: the AI Futures Project, authors of the AI 2027 scenario, whose forecasters wrote on November 10, 2026 that a Superhuman AI Researcher “will likely arrive at some point in 2027,” assuming no substantial deliberate slowdown, with Daniel Kokotajlo’s median at May 2027 — https://blog.aifutures.org/p/q35-timelines-update-looks-like-the ; Anthropic, which told the White House Office of Science and Technology Policy in March 2025 that “we expect powerful AI systems will emerge in late 2026 or early 2027” (https://www.anthropic.com/news/anthropic-s-recommendations-ostp-u-s-ai-action-plan), and whose chief executive Dario Amodei said in February 2026 that “we could have models that are a country of geniuses in the data center in one to two years” — https://www.dwarkesh.com/p/dario-amodei-2 ; also OpenAI, whose chief executive Sam Altman wrote in January 2025 “We are now confident we know how to build AGI as we have traditionally understood it” (https://blog.samaltman.com/reflections) and told TIME in August 2026 he expected an internal system he would call AGI by the end of the year (The Decoder, https://the-decoder.com/sam-altman-says-openai-will-have-agi-by-the-end-of-2026-if-you-accept-his-definition/); and Google DeepMind co-founder Shane Legg, who said in November 2026 of human-level machine intelligence “I think we’re getting very close and will probably reach this next year or the year after” (University of Auckland, https://www.auckland.ac.nz/en/news/2026/11/11/shane-legg-google-university-auckland-business-school.html).
Variation inside the camp: The AI Futures Project rests its dates on AI automating AI research, and its forecasters’ medians for AI that dominates top experts at all white-collar work run from September 2027 to September 2028. Anthropic speaks of a “country of geniuses” and Amodei puts 90 percent on it within ten years, with one to three years about even odds. OpenAI’s leaders differ in wording, its president saying in September 2026 that it is “not unreasonable” to feel the AGI era has begun and its chief executive that OpenAI is “not quite yet” there. Legg separates “minimal” AGI, an AI that can do the cognitive tasks people typically can, from a later full AGI.
The case in the camp’s own voice: Look at the curves, not the headlines. For ten years, more compute has reliably bought more capability, and every time someone named a wall, whether data, reasoning or the end of pretraining gains, the field found another way to turn compute into intelligence. The length of task an AI agent can complete has gone from minutes in 2023 to about 40 hours of skilled work in 2026, doubling every few months. And now the decisive step has started: AI is doing a large share of the work of building the next AI. METR measured one lab improving its models about twice as fast as before, mostly because of its own AI. Once AI researchers can be copied by the thousand, run day and night and improve the algorithms that make the next generation cheaper, progress stops being limited by how many people can be hired. We do not claim certainty; we claim that the most likely outcome, if nobody deliberately slows down, is AI that can do nearly all cognitive work, including AI research, before the end of the decade, and possibly within a year or two. The people who have been closest to these systems have been right about their pace more often than the people furthest from them.
Best evidence: METR’s time horizon of about 40 hours in November 2026 with a doubling time of about 3.6 months; METR’s finding that Anthropic’s capability progress ran about 1.9 times its earlier rate in October 2026, perhaps 80 percent due to AI; OpenAI’s announcement in September 2026 of an automated research intern, on schedule against a goal set in October 2025, with a fully automated AI researcher targeted for March 2028; GPT-6 Astra’s 99.9 percent on ARC-AGI-3 with OpenAI’s harness; the sixfold rise in nine months on the Remote Labor Index; training compute growing five times a year and spending forecast at more than $800 billion in 2026; and the Forecasting Research Institute’s interim finding that its expert panel significantly underestimated benchmark progress.
Answer to the strongest objection: The objection is that we have a stake in saying this, that the evidence is benchmarks rather than real work, and that the decisive METR report rests on evidence the public cannot see. The stake is real, which is why we point to outside measurement: METR, ARC Prize and the Remote Labor Index are independent, and the AI Futures Project is not a lab. Benchmarks are not the economy, but the gap between benchmark and real work has been closing on every measure that tracks it, and revenue growing several times a year is the economy’s own verdict. The redactions in the METR report are a reason for humility about the exact multiplier, not for assuming the multiplier is one. If we are wrong, the evidence will show it within two years: time horizons will stall, AI research will stop accelerating, and we will say so.

Camp: Expect AGI soon, but only after breakthroughs beyond scaling
Adherents: Google DeepMind, which wrote in April 2025 that AGI “could be here within the coming years” (https://deepmind.google/discover/blog/taking-a-responsible-path-to-agi/), and whose chief executive Demis Hassabis named in February 2026 three capabilities still missing from current systems, continual learning after deployment, long-term planning and consistency across tasks (Business Insider Japan, https://www.businessinsider.jp/article/2602-deepmind-ceo-demis-hassabis-agi-real-intelligence-gap/), while saying in October 2026 “It’s soon. I’m updating nearer and nearer” (Free Press Journal, citing The Wall Street Journal, https://www.freepressjournal.in/tech/its-soon-ai-mastermind-demis-hassabis-now-expects-agi-within-three-years) ; Ilya Sutskever, co-founder of Safe Superintelligence and formerly OpenAI’s chief scientist, who said in November 2025 that the field is “back to the age of research again, just with big computers,” that current models “generalize dramatically worse than people,” and that a system that learns as well as a human is “like 5 to 20” years away — https://www.dwarkesh.com/p/ilya-sutskever-2 ; also Andrej Karpathy, who said in October 2025 that “It will take about a decade to work through all of those issues,” naming continual learning and cognitive gaps (https://www.dwarkesh.com/p/andrej-karpathy).
Variation inside the camp: The camp agrees that scaling is necessary and not sufficient, and disagrees about how close the missing pieces are. Hassabis has moved from five to ten years to two to three and treats the gaps as research problems Google DeepMind is already working on; Sutskever’s range of 5 to 20 years puts the weight on an unsolved problem of reliable generalization; Karpathy’s decade, given before the agent gains of late 2025 and 2026, is the longest.
The case in the camp’s own voice: Scaling has been the most productive idea in the history of AI, and it is not finished. But scale alone has never been the whole story, and it will not be the last step. Today’s systems are frozen at the moment training ends; they cannot keep learning from experience the way a new employee does. They can win an olympiad medal and then fail an elementary question phrased differently. They plan well over hours and poorly over months. Those are not gaps more compute will simply fill; they are research problems, and they look tractable. The reason our timelines are short is that the field now has enormous computers, thousands of the best researchers, and AI tools that make research faster, all aimed at a short list of known problems. Expect AGI within years, not decades, but expect it to arrive through a few genuine breakthroughs layered on scale, and expect the date to depend on when those breakthroughs land, which no trend line can tell you.
Best evidence: The pattern of the last two years: reasoning models came from a new training method, not from a bigger pretraining run, and the jump in agent capability came from new reinforcement learning techniques; the persistent gaps that benchmarks reveal, such as GPT-6 Astra’s 62.7 percent on ARC-AGI-3 under the standard harness, against 99.9 percent with OpenAI’s purpose-built memory and tooling, and the best agent completing about one freelance project in six to professional standard; Hassabis’s example of olympiad-level systems that still make elementary errors depending on phrasing; and Epoch AI’s finding that algorithmic improvements, not just hardware, accounted for a substantial share of language model progress from 2012 to 2023.
Answer to the strongest objection: From one side the objection is that the breakthroughs are already happening through scaling, so the distinction is empty; from the other, that if breakthroughs are needed, nobody can say they will come in two or three years. To the first: the distinction matters because it decides what to build and what to watch. If continual learning and reliable generalization are solved by more compute, the trend lines are the forecast; if they need new ideas, the forecast is the research pipeline. To the second: research breakthroughs are not random when the problems are well defined and the effort is enormous. We are not guessing that a miracle will happen; we are judging that a few specific, well-studied problems are close to solved, and saying plainly that the date moves if they are not.

Camp: Expect human-level AI only from new architectures, not language models
Adherents: AMI Labs, the company Yann LeCun founded after leaving Meta, which states that “real intelligence does not start in language. It starts in the world” (https://amilabs.xyz/), and LeCun, who said in January 2026 “The breakthroughs are not going to come from scaling up LLMs” and that human-level AI is “not going to happen next year or two years from now” — https://www.technologyreview.com/2026/01/22/1131661/yann-lecuns-new-venture-ami-labs/ ; Gary Marcus, who predicted in December 2025 “We won’t get to AGI in 2026 (or 7)” and that “Work on new approaches such as world models and neurosymbolic will escalate” — https://garymarcus.substack.com/p/six-or-seven-predictions-for-ai-2026 ; also Richard Sutton, the Turing Award-winning pioneer of reinforcement learning, who said in September 2025 of the large language model perspective “I don’t think it’s a good perspective,” and that “Large language models are trying to get by without having a goal or a sense of better or worse” (https://www.dwarkesh.com/p/richard-sutton).
Variation inside the camp: The camp agrees that language models are the wrong foundation and disagrees about the right one. LeCun and AMI Labs build world models that learn abstract representations of sensor data and plan in them; Marcus argues for neurosymbolic hybrids that combine neural networks with explicit symbols and reasoning; Sutton argues for agents that learn continually from their own experience through reinforcement learning. LeCun expects human-level AI eventually and says it will take a while; Marcus said in May 2026 that the remaining challenges, among them building world models and inducing structured representations from raw data, will take at least a decade to solve (Antithesis Bug Bash, https://antithesis.com/bugbash/talks/gary-marcus-in-conversation/).
The case in the camp’s own voice: Language models are a remarkable technology and the wrong road to human-level intelligence. They learn to predict text, and text is a thin, secondhand record of a world they have never touched. A four-year-old has taken in more of the world through its eyes than any model has read, and learns from a handful of examples what a model needs millions to approximate. That is why the same failures persist through every generation: confident errors, brittle reasoning when a problem is rephrased, no model of cause and effect, no ability to learn after training. The labs keep covering these gaps with more data, more compute and more tools, and the benchmarks rise, but the architecture underneath has not changed and neither have its limits. Real intelligence needs systems that model the world, plan toward goals and learn from experience. Those systems are being built now, and they will get there, but not by scaling a next-word predictor, and not on the dates the people selling those predictors announce.
Best evidence: The 2025 AAAI survey, in which 76 percent of 475 respondents said scaling current approaches was unlikely or very unlikely to yield AGI; the jaggedness that even scaling’s proponents acknowledge, with systems at olympiad level failing elementary problems depending on phrasing; the persistence of fabricated answers across model generations; the gap between benchmark scores and complete work on the Remote Labor Index; the slowing of returns to pretraining in 2024 that sent labs to reinforcement learning and tools; and the fact that many of the largest recent gains came from attaching code interpreters, search and other symbolic tools to language models, which Marcus reads as evidence for hybrids.
Answer to the strongest objection: The objection is that we have said for years what language models could not do, and they keep doing it. Some of that is fair, and we update on it. But look at how they do it: with tools that run code, search engines, memory systems and scaffolds built by engineers, on top of oceans of data and compute no brain needs. That is evidence that the language model on its own is not enough, and that the progress comes from adding the things we said were missing. Passing more tests is not the same as understanding the world. When a system can learn a new physical task from a few tries, keep learning after deployment and plan over months, we will agree it is close; that system will not be a scaled-up chatbot.

Camp: Expect no AGI moment, only gradual measurable change
Adherents: Arvind Narayanan and Sayash Kapoor of Princeton, authors of “AI as Normal Technology,” published by the Knight First Amendment Institute at Columbia University (https://knightcolumbia.org/content/ai-as-normal-technology), who argue that “AGI is not a milestone because it is not actionable” and that “Diffusion occurs at human (and societal) timescales, not at the speed of tech development” — https://www.normaltech.ai/p/agi-is-not-a-milestone ; Microsoft, whose chief executive Satya Nadella said in February 2025 “Us self-claiming some AGI milestone, that’s just nonsensical benchmark hacking to me” and “The real benchmark is: the world growing at 10%” — https://www.dwarkesh.com/p/satya-nadella ; also Borhane Blili-Hamelin, Margaret Mitchell and co-authors, whose ICML 2025 position paper argues the research community should stop treating “AGI” as the north-star goal of AI research (https://arxiv.org/abs/2502.03689). Narayanan reaffirmed the view in October 2026: “For us, there is going to be no milestone, no threshold where the impacts are sudden” (The Ezra Klein Show transcript, https://dnyuz.com/2026/10/09/what-if-a-i-is-just-a-normal-technology/).
Variation inside the camp: Narayanan and Kapoor reject AGI as a discontinuity and expect impact through slow diffusion; Nadella keeps the ambition but wants it judged by economic growth rather than by labs’ declarations; Blili-Hamelin, Mitchell and co-authors object to AGI as a research goal because it hides disagreements about what the field should build and for whom.
The case in the camp’s own voice: The question “when will AGI arrive?” has no answer, because AGI is not a thing that arrives. There is no capability threshold past which the world changes overnight; there are particular systems that get better at particular tasks, unevenly, and are adopted at the pace of organizations, regulation and trust. The term is used for whatever its speaker needs: a fundraising pitch, a contract trigger, a warning. Within eight days in 2026 OpenAI’s chief executive said it was not quite here and its president said its era had begun. A declaration of AGI would change nothing a business, a government or a researcher actually does. What matters is measurable: which jobs AI does well enough to be used for, how fast it is adopted, whether it shows up in productivity and growth. Track those, and the debate about dates becomes a debate about evidence. Keep forecasting a mythical moment, and every benchmark becomes a referendum on the end of the world.
Best evidence: The spread of definitions behind published forecasts, which differ by decades for questions that sound alike; the AI researchers’ survey, in which “every task” and “every occupation” framings of nearly the same milestone came out about seventy years apart; ARC Prize’s statement that GPT-6 Astra is not AGI on the same day OpenAI’s president said the AGI era had begun; the April 2026 rewrite of the Microsoft–OpenAI agreement, under which payments continue “independent of OpenAI’s technology progress”; the jagged profile of current systems, superhuman on some tasks and unreliable on others; and the historical record of general-purpose technologies such as electricity and computing taking decades to show up in productivity statistics.
Answer to the strongest objection: The objection is that refusing to name a milestone is a way of not noticing it, and that a system able to do most cognitive work is a real and dated event whatever it is called. We do not deny that AI can become very capable; we say capability is not impact, and that the date that matters, when the world actually changes, will be set by adoption, not by a lab’s announcement. Nor are we unfalsifiable: Narayanan has said evidence that a profession could be automated wholesale, or that a lab could teach a model to cure cancer, would falsify the view. Until then, tracking real-world change is the more honest forecast.

Camp: Expect full automation over decades, not years
Adherents: Mechanize, the company founded by Ege Erdil, Tamay Besiroglu and Matthew Barnett to build the environments and data for “the full automation of the economy” (https://www.mechanize.work/announcing-mechanize-inc/), whose co-founders Erdil and Besiroglu set out the case on the April 2025 episode titled “AGI is Still 30 Years Away” (https://www.dwarkesh.com/p/ege-tamay), and Erdil, who wrote in April 2025 that his median is about 20 years until full automation of remote work — https://epoch.ai/gradient-updates/the-case-for-multi-decade-ai-timelines ; Daron Acemoglu, the Nobel-winning MIT economist, who said in 2025 “I don’t expect any occupation that we have today to have been eliminated in five or 10 years’ time” — https://www.businesstoday.in/latest/economy/story/dont-be-taken-by-the-hype-mit-economist-says-ai-likely-to-impact-just-5-of-jobs-485407-2025-07-20.
Variation inside the camp: Mechanize’s founders accept that scaling compute is the road and expect explosive economic growth once automation is broad; they argue only that it will take decades, and are working to make it come sooner. Acemoglu expects modest productivity effects for at least a decade and doubts the transformative endpoint. No statement from Mechanize revising its 2025 timelines was found.
The case in the camp’s own voice: AI will eventually be able to do nearly all the work people do, and it will be the biggest economic change since the industrial revolution. It will not happen in two years. The short timelines rest on a single mechanism, a software feedback loop in which AI improves AI faster and faster, and that mechanism is weaker than it looks. Research is bottlenecked by experiments, experiments by compute, and compute by chips, power plants and capital that take years to build. Automating AI research is about as hard as automating remote work in general, because it needs the same breadth: judgment, coordination, taste, long projects with unclear goals. AI is getting more capable fast, but also slower and more expensive per task as it takes on agentic, multimodal work. The forecasting record of the field’s leaders is not encouraging, and the trend lines they extrapolate come from narrow, clean tasks. Expect a long, compute-driven buildout that automates work piece by piece over decades, and plan for that.
Best evidence: The Forecasting Research Institute’s 2026 panel, whose median expert put AGI at 2050 and median superforecaster at 2047 under a demanding definition; the AI researchers’ 2023 survey, which put a 50 percent chance on full automation of occupations only by 2116; the IEA’s report that turbines, transformers and grid connections constrain data center growth, and Epoch AI’s estimate that a gigawatt data center takes about two years to build; the Remote Labor Index, on which the best agent still failed about five projects in six in July 2026; METR’s own finding of no strong acceleration across public frontier models; and the decades it took earlier general-purpose technologies to transform production.
Answer to the strongest objection: The objection is that 2026 has already broken the case: time horizons near 40 hours, AI accelerating research inside a lab, systems doing work that was supposed to be years away. We take that seriously, and Erdil’s own forecast gave about 30 percent to full remote-work automation within a decade. But the evidence is from well-specified tasks that are automatically scored; it is from one lab, with most of the evidence withheld; and it does not show the breadth that replacing a remote worker or a research team requires. Faster coding is not a faster economy. If agents start completing most real freelance projects and AI-run firms start turning profits, we will shorten our timelines; until then, decades remains the better bet.

## Crux

The crux is whether AI systems will soon be able to do the work of improving AI broadly and reliably enough that progress compounds, or whether the remaining gaps and physical limits will keep each step waiting on human breakthroughs and new infrastructure.

Nearly every disagreement on the page runs through it. If AI research can be largely handed to AI in the next few years, the scaling camp’s dates follow almost mechanically, the breakthroughs the hybrid camp is waiting for would be found faster than any human team could find them, the new architectures the language-model skeptics want could be invented by the systems they doubt, and the bottlenecks the decades camp points to would be worked around at machine speed. If instead automating AI research turns out to be as hard as automating any other broad, open-ended profession, gated by experiments, compute and power that cannot be hurried, then progress stays roughly as fast as the money and the buildout allow, the dates spread back out over decades, and the gap between what systems can do on tests and what they do in the world becomes the main story, as the camp that rejects the AGI milestone argues. Even that camp has named the wholesale automation of a profession as the kind of evidence that would change its view, and AI research is a profession.

The empirical half is unusually close to being tested. The measurements exist and are arriving every few months: METR’s estimates of how much faster labs improve their models with AI help, now one lab at about 1.9 times with most evidence redacted; whether the length of task agents complete keeps doubling in under four months once tasks become long, messy and judged by people rather than scripts; how agents do on whole projects such as those in the Remote Labor Index; whether OpenAI’s target of a fully automated AI researcher by March 2028 is met; and whether chips, power and capital keep growing at the rates the trend requires. Within two years most camps expect the evidence to have moved them, and several have said in advance what would.

The value half is what counts as arriving, and no measurement settles it. One view holds that the threshold that matters is capability: once systems can do most cognitive work, including their own improvement, the world has crossed a line whether or not anyone has adopted them yet, and the prudent forecast is the one that does not miss it. The other holds that the threshold that matters is change in people’s lives and in what the economy produces, which comes through adoption at the pace of institutions, and that dating a capability nobody can define the same way twice invites both hype and complacency. Beneath both sits a choice about which mistake is worse while the evidence comes in: being caught unprepared by an early arrival, or reorganizing careers, investment and attention around a date that does not come.

## Actions

Kind: learn_more
Title: METR, AI R&D-relevant model capabilities are improving rapidly and are getting harder to measure
What it is: METR’s November 2026 quarterly update on how long a task the best AI agents can complete, with the doubling time, the confidence intervals, the limits of the measurement and METR’s own reading of whether AI research is accelerating.
URL: https://metr.org/blog/2026-11-20-q4-2026-capability-update/
Resolved: yes
Serves: neutral

Kind: learn_more
Title: Epoch AI, Trends in Artificial Intelligence
What it is: A regularly updated dashboard of the inputs behind scaling, training compute, cost, chip performance, data center size, investment and revenue, each with its method and data, from the research group that tracks them.
URL: https://epoch.ai/trends
Resolved: yes
Serves: neutral

Kind: learn_more
Title: Forecasting Research Institute, Longitudinal Expert AI Panel
What it is: A standing panel of computer scientists, industry researchers, economists, policy experts and superforecasters who forecast AI progress every few months, with published question wording, results by group and accuracy checks as questions resolve.
URL: https://leap.forecastingresearch.org/
Resolved: yes
Serves: neutral

Kind: volunteer
Title: Forecast the date of AGI on Metaculus
What it is: The longest-running public forecasting question on when the first general AI system will be devised, tested and announced, with explicit resolution criteria; anyone can register, submit a forecast and see how the community’s median has moved.
URL: https://www.metaculus.com/questions/5121/date-of-artificial-general-intelligence/
Resolved: blocked (403 to automated fetch; the site is live)
Serves: neutral

Kind: learn_more
Title: Thousands of AI Authors on the Future of AI
What it is: The largest survey of AI researchers on when machines will match humans at every task and every occupation, with every question and distribution published, so readers can see how much the answers depend on wording.
URL: https://arxiv.org/abs/2401.02843
Resolved: yes
Serves: neutral

Kind: learn_more
Title: AI Futures Project, Q3.5 Timelines Update
What it is: The November 2026 update from the authors of AI 2027, setting out why each of their forecasters now expects a superhuman AI researcher in 2027, with their medians, models and stated doubts.
URL: https://blog.aifutures.org/p/q35-timelines-update-looks-like-the
Resolved: yes
Serves: Expect AGI within a few years from scaling and AI-built AI

Kind: learn_more
Title: Ilya Sutskever on the Dwarkesh Podcast
What it is: The November 2025 interview in which Safe Superintelligence’s co-founder argues that the age of scaling has given way to a new age of research, explains why current models generalize worse than people, and gives his range of 5 to 20 years.
URL: https://www.dwarkesh.com/p/ilya-sutskever-2
Resolved: yes
Serves: Expect AGI soon, but only after breakthroughs beyond scaling

Kind: learn_more
Title: Yann LeCun on his new venture, AMI Labs
What it is: MIT Technology Review’s January 2026 interview in which LeCun explains why he thinks scaling language models will not produce human-level intelligence and what world models are meant to do instead.
URL: https://www.technologyreview.com/2026/01/22/1131661/yann-lecuns-new-venture-ami-labs/
Resolved: yes
Serves: Expect human-level AI only from new architectures, not language models

Kind: learn_more
Title: Arvind Narayanan and Sayash Kapoor, AI as Normal Technology
What it is: The essay, published by the Knight First Amendment Institute, arguing that AI’s effects will arrive through gradual diffusion rather than a sudden threshold, with its companion piece “AGI is not a milestone.”
URL: https://knightcolumbia.org/content/ai-as-normal-technology
Resolved: yes (redirects to https://knightcolumbia.org/research/ai-as-normal-technology)
Serves: Expect no AGI moment, only gradual measurable change

Kind: learn_more
Title: Ege Erdil, The Case for Multi-Decade AI Timelines
What it is: The April 2025 essay by Mechanize’s co-founder setting out why he expects full automation of remote work around 20 years out, and why he doubts a software-only intelligence explosion.
URL: https://epoch.ai/gradient-updates/the-case-for-multi-decade-ai-timelines
Resolved: yes
Serves: Expect full automation over decades, not years

Kind: learn_more
Title: AAAI 2025 Presidential Panel on the Future of AI Research
What it is: The report of 24 AI researchers convened by the field’s oldest professional society, with a community survey of 475 members on AGI, scaling and research priorities.
URL: https://aaai.org/wp-content/uploads/2025/03/AAAI-2025-PresPanel-Report-FINAL.pdf
Resolved: yes (the PDF; the landing page https://aaai.org/about-aaai/presidential-panel-on-the-future-of-ai-research/ returned 403 to automated fetch)
Serves: neutral

Kind: donate
Title: Support Epoch AI
What it is: Donations fund Epoch AI’s public data on compute, cost, chips, data and benchmarks, the measurements that every side of the timelines debate cites.
URL: https://epoch.ai/about/donate
Resolved: yes
Serves: neutral

No policy or local action is listed: the topic’s scope is forecasts and the scaling hypothesis, not regulation, and no timelines-specific policy target was found that would not belong to Frontier AI Regulation.

## Sources

METR, Independent Assessment of AI R&D Acceleration at Anthropic in October 2026 (5 November 2026) — https://metr.org/blog/2026-11-05-anthropic-ai-rd-acceleration-assessment/ — accessed 2026-11-25
METR, AI R&D-relevant model capabilities are improving rapidly and are getting harder to measure (Q4 2026 capability update, 20 November 2026) — https://metr.org/blog/2026-11-20-q4-2026-capability-update/ — accessed 2026-11-25
METR, Time Horizon 1.1 (29 January 2026) — https://metr.org/blog/2026-1-29-time-horizon-1-1/ — accessed 2026-11-25
AI Futures Project, Q3.5 Timelines Update: Looks Like the Intelligence Explosion Will Happen in 2027 After All (10 November 2026) — https://blog.aifutures.org/p/q35-timelines-update-looks-like-the — accessed 2026-11-25
Alignment Forum linkpost of the AI Futures Project Q3.5 update — https://alignmentforum.org/posts/f9PajMLmBYzmWzyDv/aifp-looks-like-the-intelligence-explosion-will-happen-in — accessed 2026-11-25
AI Futures Project, home page — https://www.aifutures.org/ — accessed 2026-11-25
Fortune, OpenAI debuts GPT-6 Astra; Greg Brockman says start of AGI (3 September 2026) — https://www.fortune.com/2026/09/03/openai-debuts-gpt-6-astra-computer-use-greg-brockman-says-start-of-agi/ — accessed 2026-11-25
Axios, “Welcome to the AGI era,” OpenAI says as GPT-6 Astra debuts (3 September 2026; 403 to automated fetch) — https://axios.com/2026/09/03/openai-astra-gpt-6-agi-brockman — accessed 2026-11-25
Implicator.ai, GPT-6 Astra Launches as OpenAI Declares the AGI Era (finding aid) — https://www.implicator.ai/openai-gpt-6-astra-agi-era-launch/ — accessed 2026-11-25
OpenAI, GPT-6 Astra — https://openai.com/index/gpt-6-astra/ — accessed 2026-11-25
ARC Prize Foundation, GPT-6 Astra on ARC-AGI-3 (Greg Kamradt, 3 September 2026) — https://arcprize.org/blog/astra — accessed 2026-11-25
The Decoder, Sam Altman says OpenAI will have AGI by the end of 2026 if you accept his definition (26 August 2026) — https://the-decoder.com/sam-altman-says-openai-will-have-agi-by-the-end-of-2026-if-you-accept-his-definition/ — accessed 2026-11-25
Sam Altman, Reflections (January 2025) — https://blog.samaltman.com/reflections — accessed 2026-11-25
Engadget, OpenAI says it reached its goal of creating an automated research intern (6 September 2026) — https://www.engadget.com/2251859/openai-says-it-reached-its-goal-of-creating-an-automated-research-intern/ — accessed 2026-11-25
OpenAI, The next phase of the Microsoft partnership (27 April 2026) — https://openai.com/index/next-phase-of-microsoft-partnership — accessed 2026-11-25
Dwarkesh Podcast, Dario Amodei (13 February 2026) — https://www.dwarkesh.com/p/dario-amodei-2 — accessed 2026-11-25
Anthropic, Anthropic’s recommendations to OSTP for the U.S. AI Action Plan (6 March 2025) — https://www.anthropic.com/news/anthropic-s-recommendations-ostp-u-s-ai-action-plan — accessed 2026-11-25
University of Auckland, Google DeepMind founder returns to campus (Shane Legg, 11 November 2026) — https://www.auckland.ac.nz/en/news/2026/11/11/shane-legg-google-university-auckland-business-school.html — accessed 2026-11-25
Free Press Journal, ‘It’s Soon’: AI Mastermind Demis Hassabis Now Expects AGI Within Three Years (22 October 2026, citing The Wall Street Journal) — https://www.freepressjournal.in/tech/its-soon-ai-mastermind-demis-hassabis-now-expects-agi-within-three-years — accessed 2026-11-25
Computerworld, DeepMind CEO: AGI could be here in three years (28 May 2026) — https://www.computerworld.com/article/4178398/deepmind-ceo-agi-could-be-here-in-three-years.html — accessed 2026-11-25
Business Insider Japan, Hassabis on the gaps between AGI systems and real intelligence (5 March 2026) — https://www.businessinsider.jp/article/2602-deepmind-ceo-demis-hassabis-agi-real-intelligence-gap/ — accessed 2026-11-25
Google DeepMind, Taking a responsible path to AGI (2 April 2025) — https://deepmind.google/discover/blog/taking-a-responsible-path-to-agi/ — accessed 2026-11-25
Dwarkesh Podcast, Ilya Sutskever (25 November 2025) — https://www.dwarkesh.com/p/ilya-sutskever-2 — accessed 2026-11-25
Dwarkesh Podcast, Andrej Karpathy (October 2025) — https://www.dwarkesh.com/p/andrej-karpathy — accessed 2026-11-25
Dwarkesh Podcast, Richard Sutton (26 September 2025) — https://www.dwarkesh.com/p/richard-sutton — accessed 2026-11-25
Dwarkesh Podcast, Satya Nadella (19 February 2025) — https://www.dwarkesh.com/p/satya-nadella — accessed 2026-11-25
Dwarkesh Podcast, AGI is Still 30 Years Away: Ege Erdil and Tamay Besiroglu (April 2025) — https://www.dwarkesh.com/p/ege-tamay — accessed 2026-11-25
MIT Technology Review, Yann LeCun’s new venture, AMI Labs (22 January 2026) — https://www.technologyreview.com/2026/01/22/1131661/yann-lecuns-new-venture-ami-labs/ — accessed 2026-11-25
AMI Labs, home page — https://amilabs.xyz/ — accessed 2026-11-25
Gary Marcus, Six (or seven) predictions for AI 2026 (20 December 2025) — https://garymarcus.substack.com/p/six-or-seven-predictions-for-ai-2026 — accessed 2026-11-25
Antithesis Bug Bash, Gary Marcus in conversation with Will Wilson (13 May 2026) — https://antithesis.com/bugbash/talks/gary-marcus-in-conversation/ — accessed 2026-11-25
Fortune, Gary Marcus on hyperscalers and airlines (29 June 2026) — https://fortune.com/2026/06/29/hyperscalers-data-centers-gary-marcus-airlines-small-margins-intense-competition-high-expenses/ — accessed 2026-11-25
Sayash Kapoor and Arvind Narayanan, AGI is not a milestone (1 May 2025) — https://www.normaltech.ai/p/agi-is-not-a-milestone — accessed 2026-11-25
Knight First Amendment Institute, AI as Normal Technology — https://knightcolumbia.org/content/ai-as-normal-technology — accessed 2026-11-25
The Ezra Klein Show, What if A.I. is just a normal technology? (transcript repost, 9 October 2026) — https://dnyuz.com/2026/10/09/what-if-a-i-is-just-a-normal-technology/ — accessed 2026-11-25
Blili-Hamelin et al., Position: Stop Treating ‘AGI’ as the North-star Goal of AI Research (ICML 2025), arXiv:2502.03689 — https://arxiv.org/abs/2502.03689 — accessed 2026-11-25
Mechanize, Announcing Mechanize, Inc. (17 April 2025) — https://www.mechanize.work/announcing-mechanize-inc/ — accessed 2026-11-25
Ege Erdil, The case for multi-decade AI timelines (Epoch AI Gradient Updates, 26 April 2025) — https://epoch.ai/gradient-updates/the-case-for-multi-decade-ai-timelines — accessed 2026-11-25
Business Today, Don’t be taken by the hype: MIT economist says AI likely to impact just 5% of jobs (20 July 2025) — https://www.businesstoday.in/latest/economy/story/dont-be-taken-by-the-hype-mit-economist-says-ai-likely-to-impact-just-5-of-jobs-485407-2025-07-20 — accessed 2026-11-25
MIT Technology Review, Three things in AI to watch, according to a Nobel-winning economist (11 May 2026) — https://www.technologyreview.com/2026/05/11/1137090/three-things-in-ai-to-watch-according-to-a-nobel-winning-economist/ — accessed 2026-11-25
Forecasting Research Institute, LEAP Wave 8 report — https://leap.forecastingresearch.org/reports/wave8 — accessed 2026-11-25
Forecasting Research Institute, Experts and Superforecasters Update Their AI Timelines (LEAP Wave 8, 2 June 2026) — https://forecastingresearch.substack.com/p/leap-wave-8-ai-timelines — accessed 2026-11-25
Forecasting Research Institute, LEAP home — https://leap.forecastingresearch.org/ — accessed 2026-11-25
The Decoder, Top AI experts badly underestimated how fast the field is moving, study finds (24 September 2026; figures behind paywall) — https://the-decoder.com/top-ai-experts-badly-underestimated-how-fast-the-field-is-moving-study-finds/ — accessed 2026-11-25
Grace et al., Thousands of AI Authors on the Future of AI, arXiv:2401.02843 — https://arxiv.org/abs/2401.02843 — accessed 2026-11-25
AAAI, 2025 Presidential Panel on the Future of AI Research (report PDF, survey results p. 66) — https://aaai.org/wp-content/uploads/2025/03/AAAI-2025-PresPanel-Report-FINAL.pdf — accessed 2026-11-25
Epoch AI, Trends in Artificial Intelligence (updated 5 November 2026) — https://epoch.ai/trends — accessed 2026-11-25
Epoch AI, llms.txt site summary (largest known training run, Grok 4) — https://epoch.ai/llms.txt — accessed 2026-11-25
Epoch AI, Algorithmic Progress in Language Models (12 March 2024) — https://epoch.ai/blog/algorithmic-progress-in-language-models — accessed 2026-11-25
Epoch AI, Can AI Scaling Continue Through 2030? (20 August 2024) — https://epoch.ai/blog/can-ai-scaling-continue-through-2030 — accessed 2026-11-25
Epoch AI, Will We Run Out of Data? (6 June 2024) — https://epoch.ai/blog/will-we-run-out-of-data-limits-of-llm-scaling-based-on-human-generated-data — accessed 2026-11-25
Epoch AI, GDPval benchmark page (no scores listed; not used for a figure) — https://epoch.ai/benchmarks/gdpval — accessed 2026-11-25
Epoch AI, donate — https://epoch.ai/about/donate — accessed 2026-11-25
Center for AI Safety, A Significant Increase in Digital Labor Automation (Remote Labor Index update, 1 July 2026) — https://safe.ai/blog/significant-increase-in-digital-labor-automation — accessed 2026-11-25
Hargreaves Lansdown (Business Insider), AI hyperscalers are expected to finish the year spending $828 billion on capex (30 October 2026) — https://www.hl.co.uk/news/ai-hyperscalers-are-expected-to-finish-the-year-spending-a-whopping-828-billion-on-capex — accessed 2026-11-25
International Energy Agency, Energy and AI, executive summary (April 2025; 403 to automated fetch, figures read from IEA text in search index) — https://www.iea.org/reports/energy-and-ai/executive-summary — accessed 2026-11-25
International Energy Agency, Key questions on energy and AI (Natalie Kauf, 11 June 2026, slides hosted by the Asian Development Bank) — https://asiacleanenergyforum.adb.org/wp-content/uploads/2026/06/Key-questions-on-energy-and-AI.pdf — accessed 2026-11-25
International Energy Agency, Key questions on energy and AI, executive summary (403 to automated fetch; 485 and 950 TWh figures unverified) — https://iea.org/reports/key-questions-on-energy-and-ai/executive-summary — accessed 2026-11-25
Metaculus, Date of Artificial General Intelligence (403 to automated fetch) — https://www.metaculus.com/questions/5121/date-of-artificial-general-intelligence/ — accessed 2026-11-25
80,000 Hours Podcast, What the hell happened with AGI timelines in 2026? (Rob Wiblin, 4 August 2026) — https://80000hours.org/podcast/episodes/2026-agi-timelines/ — accessed 2026-11-25
METR, donate — https://metr.org/donate — accessed 2026-11-25
AI 2027 — https://ai-2027.com/ — accessed 2026-11-25
