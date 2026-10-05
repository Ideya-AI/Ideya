# Encryption vs. Lawful Access — research

## Overview

End-to-end encryption scrambles a message on the sender’s device and unscrambles it only on the recipient’s, so the company carrying it cannot read it and cannot hand its contents to anyone else, including police holding a warrant. WhatsApp, Signal, iMessage, and since December 2023 Facebook Messenger work this way by default, which puts billions of people’s private conversations beyond the reach of the traditional wiretap. This topic covers the argument over whether governments should be able to get at the content of end-to-end encrypted communication: by requiring companies to build a way to decrypt on lawful demand (“exceptional” or “lawful” access), by requiring software to check messages on the device before they are encrypted (client-side scanning, the core of the European Union’s “chat control” fight), by hacking individual suspects’ phones, or not at all. It deliberately excludes surveillance in general — metadata collection, data retention, facial recognition, intelligence bulk collection, and the broader balance between privacy and security, which belong to Privacy vs. Surveillance — and touches encryption of stored data, such as locked phones and encrypted cloud backups, only where the same legal powers and arguments reach it. Content moderation of public posts belongs to Content Moderation & Free Speech.

Why now: on 29 September 2026 negotiators for the European Parliament, the Council and the Commission met in Brussels for a trilogue that the Council presidency described as “dedicated to reaching general political agreement on detection obligations and own-initiative searches” in the proposed EU regulation on child sexual abuse online, the file critics call chat control; it is the sixth political round since talks opened on 9 December 2025, and the outcome was not public when this was written (Council of the EU, note 13051/26 of 29 September 2026, https://data.consilium.europa.eu/doc/document/ST-13051-2026-INIT/en/pdf). [Correction 2026-10-05: the outcome is now known: at the 29 September 2026 round, negotiators agreed on detection orders for public content and the tasks of a new EU Centre, but not on scanning private messages (Agence Europe, 30 September 2026, https://agenceurope.eu/en/bulletin/article/13949/2/csam-regulation-co-legislators-agree-on-detection-of-public-content-and-tasks-of-eu-centre-for-child-protection).] Twelve days earlier, on 17 September 2026, the UK Investigatory Powers Tribunal heard argument over whether the Home Office may keep refusing to confirm or deny a reported order requiring Apple to give access to British users’ end-to-end encrypted iCloud data; Apple had withdrawn its Advanced Data Protection feature from the UK in February 2025 rather than comply with an earlier, worldwide version of the order, and filed a fresh challenge on 3 August 2026 (Computer Weekly, 17 September 2026, https://www.computerweekly.com/news/366650612/Home-Office-challenged-on-farcical-secrecy-over-Apple-backdoor-order). And in July 2026 the EU reinstated, until 3 April 2028, the temporary law that lets messaging and email providers voluntarily scan for child sexual abuse material, after a 111-day lapse, but only with an amendment excluding interpersonal communications protected by end-to-end encryption (Agence Europe, https://agenceurope.eu/en/bulletin/article/13915/9/eu-council-formally-adopts-extension-of-derogation-from-eprivacy-until-3-april-2028).

The debate is live because both sides’ worst cases have recently happened. Child-protection agencies watched reports of suspected abuse from Facebook fall by millions after Meta switched Messenger to default encryption; the US National Center for Missing & Exploited Children counted about 7 million fewer incidents reported to it in 2024 than in 2023 and named encryption as one cause. At the same time, Chinese state hackers known as Salt Typhoon broke into the wiretap systems US telephone carriers are required by law to maintain, which led the Cybersecurity and Infrastructure Security Agency in December 2024 to advise officials and others at high risk to use only end-to-end encrypted communications. The participants are police and interior ministries across the Five Eyes and the EU, Europol, child-protection organizations such as NCMEC, ECPAT, Thorn and the Internet Watch Foundation, messaging companies led by Apple, Meta and Signal, cryptographers and computer security researchers, digital-rights groups such as the Electronic Frontier Foundation and European Digital Rights, and legislators who have split within their own parties.

## Basics

Label: US wiretaps where investigators met encryption they could not decrypt
Value: 486
Unit: wiretaps (state and federal combined)
Viz: ranked
Series: 2015 11; 2018 192; 2020 383; 2022 441; 2024 533; 2025 486 (highlight)
Data year: 2025
Source label: Administrative Office of the US Courts, Wiretap Report 2025 (and the 2015, 2018, 2020, 2022 and 2024 reports)
Source URL: https://www.uscourts.gov/data-news/reports/statistical-reports/wiretap-reports/wiretap-report-2025
Note: In 2025, officials could not decipher the plain text in 217 state wiretaps and 269 federal wiretaps, 486 in all, against 1,735 wiretaps authorized that year.
Context: The US courts’ annual wiretap report is the only long-running official count of how often encryption stops a court-ordered interception. The figures here add the state wiretaps in which “officials were unable to decipher the plain text” to the federal wiretaps “reported as being encrypted” that “could not be decrypted”: 7 plus 4 in 2015, 134 plus 58 in 2018, 183 plus 200 in 2020, 179 plus 262 in 2022, 220 plus 313 in 2024, and 217 plus 269 in 2025. Over the same decade the total number of wiretaps authorized fell from 4,148 (2015) to 1,735 (2025), so encrypted intercepts went from a fraction of a percent to a large minority of the total. Two cautions apply to reading this as a share. The encryption counts are what was reported in a given year and can include wiretaps authorized earlier, so dividing one by the other gives only an approximation. And the report covers only real-time interception under Title III and state equivalents; it says nothing about stored messages, seized phones, cloud backups or cases where investigators never applied for a wiretap because they expected encryption. Law-enforcement agencies read the rise as evidence of “going dark”; critics note that the number of affected wiretaps each year remains in the hundreds.

Label: Reports of suspected child sexual exploitation to the US CyberTipline
Value: 21.3
Unit: million reports
Viz: ranked
Series: 2023 36.2; 2024 20.5; 2025 21.3 (highlight)
Data year: 2025
Source label: NCMEC, 2025 CyberTipline Report; NCMEC, 2024 CyberTipline Report
Source URL: https://www.missingkids.org/content/dam/missingkids/pdfs/2025-cybertipline-report.pdf
Note: NCMEC’s CyberTipline received 21.3 million reports in 2025, after 20.5 million in 2024 and 36.2 million in 2023.
Context: US-based online services must report child sexual abuse material to the National Center for Missing & Exploited Children when they become aware of it, and most reports come from companies that scan their own services. Part of the 2024 fall is a change of method: NCMEC introduced “bundling,” which lets a platform file one report for a viral image shared many times, and after adjusting for it NCMEC counted 29.2 million incidents in 2024, about 7 million fewer than 2023’s 36.2 million reports (2024 report, https://www.missingkids.org/content/dam/missingkids/pdfs/2024-cybertipline-report.pdf). NCMEC attributes the remaining decline to several causes, among them fewer reports from Google, X, Discord, Microsoft and Synchronoss, the removal of images that broke terms of service but did not meet the legal definition of child pornography, and “further implementation of end-to-end encryption.” The same year the REPORT Act added new categories companies must report, which NCMEC says should have raised the count. Reports are not the same as distinct victims or offenders; one report can cover many files, and many reports concern the same material.

Label: CyberTipline reports from Meta’s platforms
Value: 4,907,710
Unit: reports from Facebook
Viz: ranked
Series: Facebook 2023 17,838,422; Facebook 2024 8,590,357; Facebook 2025 4,907,710 (highlight); Instagram 2023 11,430,007; Instagram 2025 3,673,045; WhatsApp 2023 1,389,618; WhatsApp 2025 2,355,302
Data year: 2025
Source label: NCMEC, CyberTipline reports by electronic service provider, 2023, 2024 and 2025
Source URL: https://www.missingkids.org/content/dam/missingkids/pdfs/2025-reports-by-esp.pdf
Note: Facebook filed 4.9 million reports with NCMEC in 2025, down from 17.8 million in 2023, the year Meta began switching Messenger to default end-to-end encryption.
Context: Meta turned on end-to-end encryption by default for Messenger in December 2023 and, according to NCMEC, finished the rollout in summer 2024 (Meta, https://about.fb.com/news/2023/12/default-end-to-end-encryption-on-messenger/). NCMEC says that after adjusting for Facebook’s adoption of bundling and a change in what content it reports, Facebook filed about 6.9 million fewer reports in 2024 than in 2023, and it lists encryption as a contributing factor. The raw drop across 2023 to 2025 is larger than 6.9 million because it mixes in bundling and content changes, so it should not be read as the effect of encryption alone. Meta says it still reports more than any other company and uses signals other than message content, such as account behavior and user reports. WhatsApp, which has been end-to-end encrypted since 2016 and cannot scan message content, files reports from unencrypted surfaces such as profile photos and group descriptions and from user reports; its count rose over the same period. 2023 and 2024 figures: https://www.missingkids.org/content/dam/missingkids/pdfs/2023-reports-by-esp.pdf and https://www.missingkids.org/content/dam/missingkids/pdfs/2024-reports-by-esp.pdf.

Label: UK police referrals projected lost to default encryption
Value: 92
Unit: percent of Facebook child-abuse reports disseminated to UK police
Viz: ranked
Series: Facebook 92 (highlight); Instagram 85
Data year: 2023
Source label: National Crime Agency, response to Meta’s rollout of end-to-end encryption, 7 December 2023 (republished by WiredGov)
Source URL: https://wired-gov.net/wg/news.nsf/articles/NCA+response+to+Metas+rollout+of+endtoendencryption+07122023161500?open=
Note: The National Crime Agency estimated that default end-to-end encryption would cost “the vast majority of reports (92% from Facebook and 85% from Instagram)” of detected child abuse that reach UK police.
Context: This is a projection made when Meta announced the Messenger rollout, not a measured outcome. The NCA said industry reports, acted on by it and local police, were leading to “over 800 arrests and nearly 1,200 children being safeguarded” each month across all companies, not just Meta. Meta has not published a comparable figure for how many reports its encrypted services now generate from non-content signals. The NCMEC figures for Facebook above are the nearest measured series, with the caveats noted there. Instagram direct messages were not yet encrypted by default when the NCA made the estimate.

Label: Monthly users of WhatsApp
Value: 3,000,000,000
Unit: people per month
Viz: bar
Data year: 2025
Source label: TechCrunch, reporting Meta’s first-quarter 2025 earnings call, 1 May 2025
Source URL: https://techcrunch.com/2025/05/01/whatsapp-now-has-more-than-3-billion-users/
Note: Mark Zuckerberg said on 1 May 2025 that more than 3 billion people use WhatsApp each month; its personal messages are end-to-end encrypted by default.
Context: WhatsApp completed end-to-end encryption for all messages in 2016 using the Signal Protocol, the same design Signal uses, which made strong encryption the default for a large share of humanity rather than a tool for specialists. Apple’s iMessage is also end-to-end encrypted, and Messenger joined in 2023. Scale is the reason governments now treat encryption design as a policy question: a single company’s product choice decides whether several billion people’s messages can be reached by any warrant anywhere. It is also the reason security officials worry about adding an access mechanism, since any flaw in it would sit on the same several billion devices.

Label: Reach of the Salt Typhoon intrusion into telecom networks
Value: 80
Unit: countries targeted (FBI estimate)
Viz: bar
Data year: 2025
Source label: Nextgov/FCW, quoting FBI Cyber Division director Brett Leatherman, 27 August 2025
Source URL: https://www.nextgov.com/cybersecurity/2025/08/salt-typhoon-hackers-targeted-over-80-countries-fbi-says/407719/
Note: The FBI said the China-linked Salt Typhoon campaign targeted organizations in more than 80 countries and that it had notified at least 600 organizations of the group’s interest in their systems.
Context: Salt Typhoon matters to this debate because of where it got in. In November 2024 the FBI and CISA said the hackers had stolen call records, the private communications of a limited number of people in government and politics, and copies of “certain information that was subject to U.S. law enforcement requests pursuant to court orders,” meaning the systems carriers maintain to carry out wiretaps under the 1994 Communications Assistance for Law Enforcement Act (FBI and CISA joint statement, 13 November 2024, https://www.cisa.gov/news-events/news/joint-statement-fbi-and-cisa-peoples-republic-china-targeting-commercial-telecommunications-infrastructure; the page returned 403 to automated requests). In December 2024 CISA advised senior officials to “use only end-to-end encrypted communications” and named Signal as an example (https://www.cisa.gov/sites/default/files/2024-12/guidance-mobile-communications-best-practices.pdf; 403 to automated requests). Opponents of lawful-access mandates treat this as the clearest proof that an access point built for police will be found by someone else; supporters answer that telecom wiretap systems were poorly secured and that the lesson is to secure access systems properly, not to have none.

Label: Arrests from the hacking of EncroChat
Value: 6,558
Unit: arrests worldwide
Viz: bar
Data year: 2023
Source label: Europol, “Dismantling encrypted criminal EncroChat communications leads to over 6 500 arrests and close to EUR 900 million seized,” 27 June 2023
Source URL: https://www.europol.europa.eu/media-press/newsroom/news/dismantling-encrypted-criminal-encrochat-communications-leads-to-over-6-500-arrests-and-close-to-eur-900-million-seized
Note: Europol reported 6,558 arrests and close to 900 million euros seized from the French and Dutch operation that intercepted more than 115 million conversations among about 60,000 users of the EncroChat encrypted phone network.
Context: EncroChat sold modified phones with encrypted messaging, overwhelmingly to organized crime. In 2020 the French gendarmerie planted malware through the network’s servers onto the handsets, reading messages on the device before they were encrypted, and shared the take with partners across Europe (Wikipedia, https://en.wikipedia.org/wiki/EncroChat). Similar operations followed against Sky ECC in 2021. The case is cited by both sides. Supporters of stronger access powers say it shows how much serious crime hides behind encryption; opponents of mandates say it shows police can reach criminal encrypted networks through targeted hacking without weakening the apps ordinary people use. Defendants in several countries challenged the evidence, with mixed results in court.

Label: Messages collected through the FBI’s fake encrypted phone, ANOM
Value: 27,000,000
Unit: messages
Viz: bar
Data year: 2021
Source label: Wikipedia, Operation Trojan Shield (citing Europol and the FBI)
Source URL: https://en.wikipedia.org/wiki/Operation_Trojan_Shield
Note: The FBI and Australian Federal Police secretly ran the ANOM encrypted phone service from 2018 to 2021, distributing about 11,800 devices to criminal networks and collecting 27 million messages, which led to more than 800 arrests coordinated through Europol when it was revealed on 8 June 2021.
Context: ANOM was built by the FBI with a hidden function that copied every message to a server investigators could read, and was sold through criminal channels as a secure phone. Counting national operations, reported arrests exceeded 1,100 across 16 countries, with about 40 tonnes of drugs and 250 firearms seized (FBI announcement, https://www.fbi.gov/news/stories/fbi-global-partners-announce-results-of-operation-trojan-shield-060821; 403 to automated requests). It is evidence that police can penetrate encrypted criminal markets without changing mainstream apps, though it worked because the targets used a niche product sold to criminals, which mainstream-app users do not.

Label: Encrypted phones the FBI said it could not open in 2017
Value: 7,775
Unit: devices (as claimed)
Viz: ranked
Series: Figure given to Congress and the public 7,775 (highlight); FBI internal estimate after correction about 1,200
Data year: 2017
Source label: CSO Online, reporting the Washington Post, 23 May 2018
Source URL: https://www.csoonline.com/article/565476/fbi-going-dark-whopper-locked-out-of-only-1200-phones-not-7775.html
Note: FBI leaders told Congress and the public that encryption kept them out of 7,775 devices in fiscal 2017; the bureau later attributed the figure to “programming errors,” and an internal estimate put the real number closer to 1,200.
Context: The Washington Post reported in May 2018 that the FBI had counted phones repeatedly across three databases. Director Christopher Wray had called the 7,775 figure evidence of a major public-safety problem. The FBI never published a final corrected count. The episode is why skeptics of the “going dark” argument ask for independently audited numbers, and why the European Commission and Europol have since asked member states to gather documented cases of investigations frustrated by encryption. It concerns locked devices, not messages in transit, but the same agencies made both arguments.

Label: What Europeans say about scanning messages, depending on the question
Value:
Unit: percent of respondents
Viz: ranked
Series: Support detection in end-to-end encrypted services “in case of a significant risk of child sexual abuse on a specific platform” (Eurobarometer, 2023) 83 (highlight); Support detection of child sexual abuse in online messages (Eurobarometer, 2023) 87; Oppose “automatic searching of all personal electronic mail and messages of each citizen for presumed suspicious content” (YouGov for MEP Patrick Breyer, 2021) 72
Data year: 2023
Source label: European Commission, Eurobarometer on protection of children against online sexual abuse, 20 July 2023; Patrick Breyer, YouGov poll, 28 April 2021
Source URL: https://home-affairs.ec.europa.eu/news/strong-support-citizens-across-eu-prevent-and-combat-child-sexual-abuse-online-2023-07-20_en
Note: Asked about detecting child abuse where there is significant risk, 83 percent of EU respondents supported it even in encrypted services; asked about automatically searching everyone’s messages, 72 percent of respondents in ten EU countries opposed it.
Context: These are different questions and do not contradict each other; they show how much the answer depends on framing. The Eurobarometer, commissioned by the European Commission, also found that 96 percent saw detecting child abuse as equally or more important than online privacy and that 78 percent approved of the Commission’s proposal. The YouGov survey of 10,265 people in ten countries, commissioned by Pirate Party MEP Patrick Breyer, an opponent of the proposal, found 18 percent support (https://www.patrick-breyer.de/en/poll-72-of-citizens-oppose-eu-plans-to-search-all-private-messages-for-allegedly-illegal-material-and-report-to-the-police/). Each side has criticized the other’s wording: the Eurobarometer describes targeted detection under a risk condition, the YouGov question describes blanket searching of all messages. No poll found asks a question that matches the text actually under negotiation in 2026.

Label: Americans on whether Apple should unlock the San Bernardino iPhone
Value: 51
Unit: percent saying Apple should unlock it
Viz: ranked
Series: Apple should unlock the iPhone 51 (highlight); Apple should not unlock it 38; No opinion 11
Data year: 2016
Source label: Pew Research Center, 22 February 2016
Source URL: https://www.pewresearch.org/politics/2016/02/22/more-support-for-justice-department-than-for-apple-in-dispute-over-unlocking-iphone/
Note: In a February 2016 survey of 1,002 US adults, 51 percent said Apple should unlock the iPhone to assist the FBI investigation and 38 percent said it should not, to ensure the security of other users’ information.
Context: The survey was taken days after a federal magistrate ordered Apple to write software to help the FBI get into the work phone of one of the gunmen who killed 14 people in San Bernardino, California, in December 2015. Republicans (56 percent) and Democrats (55 percent) gave similar answers; the split ran more through independents. The FBI dropped the case in March 2016 after an outside firm, later reported to be Australia’s Azimuth Security, unlocked the phone (Wikipedia, https://en.wikipedia.org/wiki/FBI%E2%80%93Apple_encryption_dispute). The question concerned one named phone in a terrorism case, not encrypted messaging generally, and Pew has not repeated it; there is no recent US poll of similar quality on end-to-end encrypted messaging.

Label: Automated child-abuse referrals that Irish police found were not abuse material
Value: 471
Unit: referrals out of 4,192
Viz: ranked
Series: Referrals received from NCMEC 4,192; Not child abuse material 471 (highlight); Actionable 409
Data year: 2020
Source label: Irish Council for Civil Liberties, citing An Garda Síochána responses, 19 October 2022
Source URL: https://www.iccl.ie/news/an-garda-siochana-unlawfully-retains-files-on-innocent-people-who-it-has-already-cleared-of-producing-or-sharing-of-child-sex-abuse-material/
Note: Of 4,192 referrals Ireland’s police received from NCMEC in 2020, they marked 471 (11.2 percent) as not child abuse material and 409 (9.7 percent) as actionable.
Context: This is one of the few official, published breakdowns of what happens to reports generated largely by automated scanning. The Garda child-exploitation unit gave examples of material it would not pursue: “children playing on a beach, topless content, nudist, adult content, etc.” The source does not classify the remaining roughly 3,300 referrals, which may include genuine abuse material that could not be acted on, for example because the offender was abroad, so the 9.7 percent actionable figure should not be read as the share that was abuse. Opponents of mandatory scanning cite the false positives and the fact that Irish police kept data on people they had cleared; supporters note that most referrals were not false positives and that new laws would bring stricter accuracy standards. A widely circulated Swiss figure suggesting most machine-generated reports are not criminally relevant has been disputed by NCMEC and is not used here.

Label: Australian notices to help police get around encryption
Value: 58
Unit: technical assistance requests in 2024–25
Viz: ranked
Series: Technical assistance requests (voluntary) 58 (highlight); Technical assistance notices (compulsory, use existing capability) 0; Technical capability notices (compulsory, build new capability) 0
Data year: 2024–25
Source label: Australian Department of Home Affairs, Telecommunications (Interception and Access) Act 1979 and Part 15 of the Telecommunications Act 1997, Annual Report 2024–25
Source URL: https://www.homeaffairs.gov.au/criminal-justice/files/telecommunications-interception-and-access-reports/telecommunications-interception-access-act-1979-annual-report-24-25.pdf
Note: Five Australian interception agencies gave communications providers 58 voluntary technical assistance requests in 2024–25; no compulsory technical assistance notices or technical capability notices were issued.
Context: Australia’s Assistance and Access Act of 2018 lets agencies compel a communications company to use or build a capability to help them, though it bars requiring a “systemic weakness” in encryption. Its use so far has been mostly voluntary: 60 requests in 2023–24 and 58 in 2024–25, two compulsory assistance notices in 2023–24 and none in 2024–25, and, the report states, no capability notices in either year. Supporters say the power works as intended, by giving police leverage to reach voluntary agreements; critics say its secrecy makes it impossible to know what the voluntary requests achieved or cost. The UK’s equivalent, the technical capability notice under the Investigatory Powers Act 2016, is the power reportedly used against Apple.

Label: Scientists signing the 2025 open letter against chat control
Value: 807
Unit: signatories from 37 countries
Viz: bar
Data year: 2025
Source label: Joint statement of scientists and researchers on the EU’s proposed Child Sexual Abuse Regulation, 9 September 2025 (signatures closed 12 October 2025)
Source URL: https://csa-scientist-open-letter.org/Sep2025
Note: 807 scientists and researchers from 37 countries signed a September 2025 letter calling the EU plan to scan private messages technically infeasible and dangerous to security and democracy.
Context: It was the third such letter from the research community since 2023, with signatories concentrated among cryptographers and computer security researchers at European universities, the Max Planck Society and Fraunhofer. Press reports at different points gave 400, 500 or 600 signatories because the count kept growing; 807 is the letter’s own final figure. Supporters of the regulation respond that technical feasibility should be judged on accredited tools and independent testing rather than letters, and point to the UK government’s own technical experts, Ian Levy and Crispin Robinson of the National Cyber Security Centre and GCHQ, who argued in 2022 that on-device safety measures can be designed with meaningful safeguards (https://arxiv.org/abs/2207.09506).

Label: European Parliament civil liberties committee vote on the child sexual abuse regulation
Value: 51
Unit: votes in favor of the Parliament’s position
Viz: ranked
Series: In favor 51 (highlight); Against 2; Abstaining 1
Data year: 2023
Source label: European Parliament press release, 14 November 2023
Source URL: https://www.europarl.europa.eu/news/en/press-room/20231110IPR10118/child-sexual-abuse-online-effective-measures-no-mass-surveillance
Note: The civil liberties committee adopted the Parliament’s position by 51 votes to 2 with 1 abstention, excluding end-to-end encrypted communications from detection orders and limiting orders to targeted, court-approved measures of last resort.
Context: The vote crossed party lines, including the center-right rapporteur Javier Zarzalejos, and set the Parliament firmly against scanning of encrypted messages. The Council did not agree its own position until 26 November 2025, after Poland and then Denmark failed to find a majority for mandatory detection and Germany announced in October 2025 that it would not support the Danish text. The Council mandate dropped mandatory scanning in favor of risk-mitigation duties and made voluntary scanning permanent (Wikipedia, https://en.wikipedia.org/wiki/Chat_Control). The gap between the two institutions on detection and encryption is what the 29 September 2026 trilogue was convened to close.

Label: Criminal investigations in the EU that rely on electronic evidence
Value: 85
Unit: percent of criminal investigations
Viz: radial
Data year: 2025
Source label: European Commission, Roadmap for lawful and effective access to data for law enforcement, 24 June 2025
Source URL: https://home-affairs.ec.europa.eu/news/commission-presents-roadmap-effective-and-lawful-access-data-law-enforcement-2025-06-24_en
Note: The European Commission says 85 percent of criminal investigations now rely on electronic evidence.
Context: The figure is about electronic evidence of any kind, from phone records and cloud accounts to messages, not about encrypted evidence specifically, and the Commission has used it since its 2018 e-evidence proposals, so it describes investigations’ dependence on data rather than how often encryption blocks them. The June 2025 roadmap promised a “Technology Roadmap on encryption” in 2026 to “identify and evaluate solutions that enable lawful access to encrypted data,” and research so that Europol has next-generation decryption capabilities from 2030. The Commission also states that its measures “do not in any way prohibit, limit or weaken encryption” (https://home-affairs.ec.europa.eu/policies/internal-security/lawful-access-data/encryption_en). Publication of the encryption technology roadmap could not be confirmed as of 29 September 2026 [unverified].

Label: Days the EU went without a legal basis for voluntary abuse scanning
Value: 111
Unit: days (3 April to 23 July 2026)
Viz: bar
Data year: 2026
Source label: Agence Europe, “EU Council formally adopts extension of derogation from ePrivacy until 3 April 2028”
Source URL: https://agenceurope.eu/en/bulletin/article/13915/9/eu-council-formally-adopts-extension-of-derogation-from-eprivacy-until-3-april-2028
Note: The EU law allowing providers to scan messages voluntarily for child abuse material lapsed on 3 April 2026 and was reinstated by the Council on 23 July 2026, after 111 days, with end-to-end encrypted communications excluded.
Context: Since 2021 a temporary exception to the EU’s ePrivacy rules has allowed services such as Gmail, Messenger and Instagram to keep scanning for known abuse material while the permanent regulation was negotiated. The European Parliament declined to extend it in March 2026, and it expired; child-protection groups warned of “an alarming and unacceptable gap in child protection” (ECPAT, 1 April 2026, https://ecpat.org/this-is-no-april-fools-joke-europe-is-switching-its-detection-of-child-sexual-abuse-online-off/). The reinstatement passed Parliament under an urgent procedure on 9 July 2026 with an amendment excluding end-to-end encrypted interpersonal communications, which the Council accepted; it now runs to 3 April 2028 (Council press release, 23 July 2026, https://www.consilium.europa.eu/en/press/press-releases/2026/07/23/fighting-child-sexual-abuse-online-interim-measure-protecting-children-now-reinstated/; 403 to automated requests). Encrypted services were effectively outside the old regime anyway, since providers cannot scan what they cannot read; the amendment makes that exclusion explicit in law.

## Questions

Question: Can a way in for lawful authorities be built without creating a weakness others will exploit?
Tag: empirical
Poles: Safe access possible / Any access is a hole
Why contested: No government has published a working design for exceptional access to end-to-end encrypted messaging at scale, so the argument is about systems that do not yet exist. Cryptographers point to a long record of access mechanisms failing; officials point to other high-stakes keys, such as software-signing keys and payment systems, that companies already protect.
Case for safe access possible: Companies already guard secrets whose theft would be catastrophic: the keys that sign every software update to billions of phones, the keys that run cloud services, and the systems that process payments. A decryption capability held by the provider, used only on a court order, logged, split between several parties and audited, would be no harder to protect than those. The claim that access is mathematically impossible confuses the encryption algorithm, which no one proposes to weaken, with the surrounding system, which engineers design every day. The Salt Typhoon breach happened in decades-old telephone wiretap equipment that carriers never secured properly, not in a modern design built for the purpose. European police chiefs said in April 2024 that “technical solutions do exist; they simply require flexibility from industry as well as from governments” (Europol, https://www.europol.europa.eu/cms/sites/default/files/documents/EDOC-%231384205-v1-Joint_Declaration_of_the_European_Police_Chiefs.PDF). Absolute claims of impossibility have been made about many engineering problems that were later solved.
Case for any access is a hole: Every access mechanism tried so far has failed. The US government’s Clipper Chip in the 1990s was found to have a flaw that let users bypass it. In Greece in 2004 and 2005, unknown intruders used the lawful-intercept software in Vodafone’s network to tap the prime minister’s phone and many others. Salt Typhoon went into the wiretap systems US law required carriers to build, and the FBI later said the campaign reached more than 80 countries (Nextgov, https://www.nextgov.com/cybersecurity/2025/08/salt-typhoon-hackers-targeted-over-80-countries-fbi-says/407719/). A signing key is used rarely by a few people; a lawful-access key would be used thousands of times a year by many agencies in many countries, each use a chance for theft, insider abuse or error. In 2015 a group of leading cryptographers concluded that exceptional access would add complexity, concentrate targets and undo modern protections such as forward secrecy (“Keys Under Doormats,” https://dspace.mit.edu/handle/1721.1/97690). The burden of proof lies with whoever wants to deploy the design to billions of devices, and no one has met it.

Question: Is encryption leaving police unable to investigate serious crime, or do they have more evidence than ever?
Tag: empirical
Poles: Going dark / Golden age of surveillance
Why contested: The data are fragmentary and partly collected by interested parties. The FBI overstated its count of locked phones in 2017, and the US wiretap report shows rising encrypted intercepts but only in the hundreds. Meanwhile police have gained cloud data, location records and device forensics that did not exist twenty years ago, and nobody measures the cases that are never solved or never opened.
Case for going dark: The content of criminal communication is the best evidence there is, and it is disappearing. Encrypted wiretaps that US officials could not read rose from 11 in 2015 to 486 in 2025, against a falling total of wiretaps as prosecutors stop applying for intercepts they know will be useless (US Courts, https://www.uscourts.gov/data-news/reports/statistical-reports/wiretap-reports/wiretap-report-2025). Reports of child sexual abuse from Facebook to NCMEC fell by about 6.9 million in 2024 once Messenger was encrypted, by NCMEC’s adjusted count (https://www.missingkids.org/content/dam/missingkids/pdfs/2024-cybertipline-report.pdf). Metadata shows who talked to whom, not what they planned, and it rarely proves intent in court. Hacking devices is expensive, slow, unavailable to most local police forces and often defeated by the next software update. The European Commission says 85 percent of criminal investigations now depend on electronic evidence.
Case for golden age of surveillance: Police have never had more digital evidence. Phones generate location histories, cloud backups, contact lists, photos, payment records and metadata that investigators can obtain with ordinary legal process, and forensic tools sold by firms such as Cellebrite unlock many seized devices. A 2016 Harvard study, “Don’t Panic,” concluded that going dark was a problem in some corners but not the whole picture, because commercial incentives keep most data accessible to companies and therefore to warrants (https://cyber.harvard.edu/pubrelease/dont-panic/Dont_Panic_Making_Progress_on_Going_Dark_Debate.pdf). The biggest encrypted-crime cases of recent years, EncroChat, Sky ECC and ANOM, were broken without any access mandate and produced thousands of arrests. The FBI’s headline figure for inaccessible phones in 2017 was later found to be inflated by programming errors, roughly 7,775 against an internal estimate near 1,200 (CSO Online, https://www.csoonline.com/article/565476/fbi-going-dark-whopper-locked-out-of-only-1200-phones-not-7775.html). Until agencies publish audited counts of cases lost to encryption, claims of going dark are assertions.

Question: Does scanning messages on the phone before they are encrypted keep the protection end-to-end encryption promises?
Tag: empirical
Poles: Scanning preserves encryption / Scanning breaks encryption
Why contested: Client-side scanning leaves the encryption itself untouched but adds software that inspects content before it is sent. Whether that is a narrow safety check or a surveillance channel depends on how accurate it is, who controls the list of what it looks for, and whether it can be kept to its stated purpose, none of which can be observed from outside.
Case for scanning preserves encryption: The messages stay encrypted in transit and on the server; nobody gets a key. On-device matching against a list of already-known abuse images, the same hashing technique platforms have run on unencrypted services for over a decade, reveals nothing about any message that does not match. Ian Levy and Crispin Robinson, the technical directors of the UK’s National Cyber Security Centre and of GCHQ’s cryptanalysis work, argued in 2022 that such safeguards can be designed with human review, independent oversight and limits on what the system can report (https://arxiv.org/abs/2207.09506). The EU proposal would allow only technologies tested and approved by a new EU Centre, with detection orders issued by courts. Opposing all scanning means accepting that known abuse images can circulate freely on the largest messaging services in the world.
Case for scanning breaks encryption: The promise of end-to-end encryption is that only the sender and recipient can learn what a message says. Software that inspects every message and reports on it breaks that promise whether it runs before or after encryption, and Signal’s president Meredith Whittaker called it a means for “hackers and hostile nation states” to “piggyback on the access granted to the scanning system” (Signal, 3 October 2025, https://signal.org/blog/pdfs/germany-chat-control.pdf). A group of leading security researchers concluded in 2021 that client-side scanning creates serious security and privacy risks for everyone and can be repurposed by changing the list it matches against (“Bugs in Our Pockets,” https://arxiv.org/abs/2110.07450). Apple designed such a system for iCloud Photos in 2021 and abandoned it in 2022 after widespread criticism from security researchers, some of whom showed that its image-matching algorithm could be made to produce false matches. Detecting new images and grooming requires machine-learning classifiers whose error rates, multiplied across billions of messages, would flood police with innocent material; Irish police marked 471 of 4,192 automated NCMEC referrals in 2020 as not abuse material (ICCL, https://www.iccl.ie/news/an-garda-siochana-unlawfully-retains-files-on-innocent-people-who-it-has-already-cleared-of-producing-or-sharing-of-child-sex-abuse-material/).

Question: Should any private communication be beyond the reach of a lawful warrant?
Tag: value
Poles: No warrant-proof spaces / Some spaces stay private
Why contested: Legal traditions in democracies have always let a judge authorize search of a home, a letter or a phone line, and end-to-end encryption is the first technology to make that authorization unenforceable for ordinary communication at scale. Whether that is a loss of the rule of law or a restoration of the privacy that face-to-face conversation always had is a judgment about what the state is owed.
Case for no warrant-proof spaces: Democratic societies have never accepted places where the law cannot reach. When a judge finds probable cause, police may enter a locked house; Europol’s executive director Catherine De Bolle has argued that the same principle should apply to data “locked inside encryption” (Computer Weekly, 22 January 2025, https://www.computerweekly.com/news/366618230/Europol-seeks-evidence-of-encryption-on-crime-enforcement-as-it-steps-up-pressure-on-Big-Tech). A warrant is the product of democratic law, judicial oversight and individual suspicion, not arbitrary power. Letting private companies decide by product design that no warrant can ever be served transfers a decision about public safety from elected legislatures and courts to engineers, and the people who benefit most are those with the most to hide.
Case for some spaces stay private: For most of history the most private conversations, spoken face to face, were never recorded and could not be retrieved later by any warrant; the wiretap and the stored message are recent exceptions, not the baseline. Encryption restores that privacy for conversations that now happen by phone. The same property that protects a suspect protects a journalist’s source, a dissident abroad, a victim hiding from an abuser and an official discussing secrets, and it cannot be offered to one and withheld from another. The question is not whether the state may search, but whether everyone must be made less secure so that the state always can.

Question: Would access mandates catch serious criminals, or only expose ordinary users?
Tag: empirical
Poles: Mandates catch offenders / Offenders move elsewhere
Why contested: Encryption software is freely available and open source, so a determined offender can always use a tool beyond a government’s reach. Whether most offenders actually do, or whether they stay on mainstream apps out of convenience and carelessness, is an empirical question with little systematic evidence.
Case for mandates catch offenders: Most criminals are not sophisticated. Offenders who groom children go where children are, which is mainstream platforms, and much abuse material is traded on ordinary apps; tens of millions of reports a year from large platforms show that. Drug networks, fraudsters and extremists also use WhatsApp and iMessage because everyone does. Making mainstream services reachable would recover most of the lost evidence even if a few experts migrate. When offenders are pushed to niche tools, those tools become markers of criminality and targets for operations like EncroChat and ANOM.
Case for offenders move elsewhere: Strong encryption is published mathematics running in open-source code that anyone can compile, and it cannot be recalled. A law can compel Apple or Meta but not the maintainers of open-source software in another country, so the most dangerous people would switch and the law would fall on everyone else. Criminal markets already use custom tools, as EncroChat and Sky ECC showed. Mandates would also push dissidents, journalists and security-conscious users toward less audited apps, and would lead responsible companies such as Signal to withdraw from a market rather than comply, as Signal has said it would do in the EU (Signal, https://signal.org/blog/pdfs/germany-chat-control.pdf).

Question: Can an access power granted by democracies be kept from authoritarian governments and criminals?
Tag: empirical
Poles: Safeguards hold / Precedent spreads
Why contested: Messaging apps are global products, so a capability built for one government exists everywhere the product is sold. Whether companies can refuse other governments once they have complied with one, and whether judicial safeguards travel with the capability, is a prediction about politics as much as engineering.
Case for safeguards hold: Companies already comply with lawful demands in dozens of countries and refuse many others; they have legal teams, transparency reports and home-country laws that let them distinguish a judge’s order in a democracy from a request by a dictatorship. Access can be limited to cases authorized by law and subject to strong safeguards and independent oversight, as the Five Eyes governments, India and Japan proposed in their 2020 statement on end-to-end encryption (https://www.gov.uk/government/publications/international-statement-end-to-end-encryption-and-public-safety/international-statement-end-to-end-encryption-and-public-safety-accessible-version). Authoritarian states such as China and Russia already block or control the apps they dislike and do not wait for Western precedent. Refusing democracies what autocracies take anyway leaves democratic law enforcement worse off without protecting anyone.
Case for precedent spreads: Once a capability exists, the question becomes who can compel its use, and a company that has built it for the UK cannot credibly tell another government it is technically impossible. The UK’s 2025 order to Apple was itself a claim to reach users worldwide, and the US Director of National Intelligence, Tulsi Gabbard, called it a “clear and egregious violation of Americans’ privacy and civil liberties” (The Record, 26 February 2025, https://therecord.media/odni-gabbard-uk-apple-backdoor-request-grave-concern) before announcing in August 2025 that the UK had agreed to drop the demand as it affected Americans (Nextgov, https://www.nextgov.com/cybersecurity/2025/08/uk-agreed-drop-backdoor-encryption-demand-apple-dni-says/407556/); the UK then reportedly issued a narrower order covering British users. The Greek wiretap case and Salt Typhoon show lawful-intercept systems falling into the wrong hands. Laws written for child abuse have a history of expanding to other crimes, and systems that match content against a list can be pointed at political speech by changing the list.

Question: Should platforms search for child abuse proactively, or only when there is suspicion of a specific person?
Tag: value
Poles: Proactive detection / Targeted suspicion only
Why contested: Most child sexual abuse material is found today because platforms scan everything uploaded to unencrypted services, without any suspicion of the uploader. Encryption forces a choice between extending that practice into private messages and limiting searches to people a court has reason to suspect, which is the line the European Parliament drew in 2023 and the Council did not.
Case for proactive detection: Children who are being abused cannot report it, and the images of their abuse circulate for years; proactive detection is how millions of those images are found and how victims are identified and rescued. Suspicion-based searching cannot find what nobody has reported. Scanning for known images is narrow, automatic and reviewed by people before anything reaches police, which is less intrusive than the airport screening and bank monitoring everyone already accepts. The EU’s own survey found 83 percent support for detection even in encrypted services where a platform poses a significant risk (European Commission, https://home-affairs.ec.europa.eu/news/strong-support-citizens-across-eu-prevent-and-combat-child-sexual-abuse-online-2023-07-20_en). Leaving encrypted messaging outside detection creates exactly the safe haven offenders seek.
Case for targeted suspicion only: Searching everyone’s private messages without any suspicion is general surveillance, which European courts and constitutions have long rejected for any purpose. The European Parliament’s civil liberties committee voted 51 to 2 in 2023 for detection orders only against individuals or groups with reasonable grounds for suspicion, approved by a court, as a last resort, and never inside end-to-end encryption (European Parliament, https://www.europarl.europa.eu/news/en/press-room/20231110IPR10118/child-sexual-abuse-online-effective-measures-no-mass-surveillance). Germany’s justice minister Stefanie Hubig said on 8 October 2025 that “unprovoked chat monitoring must be taboo in a constitutional state. Private communication must never be under general suspicion” (heise online, https://www.heise.de/en/news/Minister-of-Justice-Chat-control-is-taboo-in-a-constitutional-state-10747560.html). Resources are better spent on child-protection services, on police capacity to act on existing reports and on prevention than on a system that treats every citizen as a suspect.

Question: Should the state hack individual suspects’ devices as an alternative to encryption mandates?
Tag: value
Poles: Hack the endpoint / Close every hole
Why contested: Targeted hacking leaves encryption intact for everyone else, but it depends on governments keeping software vulnerabilities secret rather than reporting them so they can be fixed, which leaves everyone exposed to the same flaws. Whether that trade is better or worse than a mandate is a judgment about which risk is more acceptable.
Case for hack the endpoint: Police should do the work of breaking into one suspect’s phone, under a warrant, rather than asking companies to weaken security for billions of people. Steven Bellovin, Matt Blaze, Sandy Clark and Susan Landau argued in 2014 that exploiting existing vulnerabilities is a better path than building wiretap interfaces into internet services, because it is costly and therefore naturally limited to serious cases (“Lawful Hacking,” https://scholarlycommons.law.northwestern.edu/njtip/vol12/iss1/1/). Germany has used this approach for years, with court-ordered source interception and online searches under narrow statutory rules. The largest successes against encrypted crime, EncroChat and ANOM, came from targeted operations, not mandates.
Case for close every hole: Government hacking depends on keeping vulnerabilities unpatched, and those same flaws are available to criminals and hostile states; the NSA’s EternalBlue exploit, stolen and leaked in 2017, powered the WannaCry and NotPetya attacks. The commercial spyware industry that serves government hacking, from NSO Group’s Pegasus onward, has been used against journalists, dissidents and politicians in democracies as well as autocracies. The Electronic Frontier Foundation calls for a public debate on whether governments should be allowed to “stockpile and exploit software flaws” at all (EFF, https://www.eff.org/issues/government-hacking-digital-security). Replacing backdoors with hacking changes who holds the risk, not whether it exists.

## Positions

Camp: Require encrypted services to give authorities access and detect abuse
Adherents:
- Europol and the European Police Chiefs (institution), whose April 2024 joint declaration calls on the technology industry “to build in security by design, to ensure they maintain the ability to both identify and report harmful and illegal activities, such as child sexual exploitation, and to lawfully and exceptionally act on a lawful authority,” and says “we do not accept that there need be a binary choice between cyber security or privacy on the one hand and public safety on the other”: https://www.europol.europa.eu/cms/sites/default/files/documents/EDOC-%231384205-v1-Joint_Declaration_of_the_European_Police_Chiefs.PDF
- US Department of Justice, Office of Legal Policy (institution): “Because of warrant-proof encryption, the government often cannot obtain the electronic evidence and intelligence necessary to investigate and prosecute threats to public safety and national security, even with a warrant or court order. This provides a ‘lawless space’ that criminals, terrorists, and other bad actors can exploit”: https://www.justice.gov/olp/lawful-access
- Catherine De Bolle, executive director of Europol, who told the Financial Times in January 2025 that technology companies have a “social responsibility” to give police access to encrypted messages, comparing encryption to a locked house police may enter with a warrant (reported by Computer Weekly): https://www.computerweekly.com/news/366618230/Europol-seeks-evidence-of-encryption-on-crime-enforcement-as-it-steps-up-pressure-on-Big-Tech
- National Center for Missing & Exploited Children (institution): “We oppose privacy measures that fail to address how the internet is used to entice children into sexually exploitive situations”: https://www.missingkids.org/theissues/end-to-end-encryption
- Also in this camp: the UK Home Office, which reportedly served Apple with technical capability notices in 2025 and holds a power under the Online Safety Act 2023 to require accredited scanning technology; the UK National Crime Agency and the Virtual Global Taskforce of 15 law-enforcement agencies (statement of 22 April 2024, https://www.nationalcrimeagency.gov.uk/statement-on-end-to-end-encryption); the governments that signed the October 2020 international statement on end-to-end encryption and public safety, the Five Eyes plus India and Japan (https://www.gov.uk/government/publications/international-statement-end-to-end-encryption-and-public-safety/international-statement-end-to-end-encryption-and-public-safety-accessible-version); the European Commission, whose 2022 proposal introduced detection orders and whose 2025 roadmap plans lawful access to encrypted data; ECPAT International, Thorn, the Internet Watch Foundation and the NSPCC.
Variation inside the camp: The camp wants two things that its own members distinguish. Police and interior ministries emphasize lawful access: the ability of a provider to hand over a named suspect’s messages in readable form when a court orders it, which for end-to-end encryption means redesigning the service so the provider can decrypt. Child-protection organizations and the European Commission emphasize proactive detection: automated scanning, including on the device before encryption, for known abuse images, new images and grooming, without a specific suspect. Some insist neither requires weakening encryption and prefer terms like “security by design” or “responsibly managed encryption”; others accept that a design change is needed and argue its risk is manageable. They also differ on means: the UK uses secret capability notices and regulator-approved technology, the EU is legislating detection orders through a new EU Centre, and the US has relied on pressure and proposed bills such as the 2020 Lawful Access to Encrypted Data Act, which never passed. The US government itself is divided: its Director of National Intelligence publicly opposed the UK’s order against Apple in 2025.
Case: For every other kind of evidence, society has settled the question: if a judge finds good reason, police may search a home, open a letter, tap a phone line or seize a bank record. End-to-end encryption as currently deployed abolishes that settlement for the main way people now communicate, not by any democratic decision but by the product choices of a few companies. The consequences are concrete. Offenders groom children on mainstream apps because children are there; abuse images circulate on the same services; drug networks, fraudsters and terrorists coordinate on WhatsApp and iMessage because everyone does. When Meta encrypted Messenger by default, millions of reports that used to reach child-protection agencies stopped. We are not asking to weaken the mathematics of encryption, to read everyone’s messages or to spy without a warrant. We are asking companies that have built some of the most sophisticated systems in the world to design their products so they can still respond to a lawful court order and still detect the worst material, as they already do on their unencrypted services. The claim that this is impossible is a policy preference presented as a technical fact.
Best evidence: NCMEC’s count of incidents reported by platforms fell by about 7 million from 2023 to 2024, and NCMEC names the further rollout of end-to-end encryption as a contributing factor, with Facebook alone filing about 6.9 million fewer reports after adjustment for bundling (NCMEC 2024 CyberTipline Report, https://www.missingkids.org/content/dam/missingkids/pdfs/2024-cybertipline-report.pdf). The UK National Crime Agency projected that default encryption would cost 92 percent of Facebook and 85 percent of Instagram child-abuse reports reaching UK police, at a time when industry reports were leading to over 800 arrests and nearly 1,200 children safeguarded each month (NCA, 7 December 2023). US wiretaps where officials could not read the plain text rose from 11 in 2015 to 486 in 2025 (US Courts). The EncroChat and Sky ECC operations showed how much organized crime runs on encrypted messaging once it can be read: 6,558 arrests from EncroChat alone. Most Europeans, asked by the EU’s Eurobarometer in 2023, supported detection of child abuse in messages, including 83 percent in encrypted services where a platform poses a significant risk.
Answer to the strongest objection: The strongest objection is that any access mechanism is a security hole that criminals and hostile states will find, as Salt Typhoon did with US telephone wiretap systems. But Salt Typhoon exploited old telecom equipment that carriers never adequately secured, and its lesson is to protect access systems as seriously as the other critical keys companies already guard, not to abolish lawful access. Companies protect signing keys that could compromise every phone they have sold; a capability used under court order, with auditing and oversight, can be protected to the same standard. Security is also not only about attacks on devices: a child being groomed in an encrypted chat is a security failure too. And the alternatives critics offer, from metadata to targeted hacking, are slower, costlier, out of reach for most police forces and useless against the scale of abuse that automated detection finds.

Camp: Keep end-to-end encryption closed to everyone but its users
Adherents:
- Signal Foundation (institution) and its president Meredith Whittaker, who wrote on 3 October 2025 that “encryption either works for everyone, or it doesn’t work for anyone; a backdoor in one part of a network is a vector into every other part,” and that “if we were given a choice between building a surveillance machine into Signal or leaving the market, we would leave the market”: https://signal.org/blog/pdfs/germany-chat-control.pdf
- Apple (institution), which withdrew Advanced Data Protection from UK users rather than comply with the UK order and states: “We have never built a backdoor or master key to any of our products or services and we never will”: https://support.apple.com/en-us/122234
- Electronic Frontier Foundation (institution): “you cannot build a backdoor that only lets in good guys and not bad guys” and “the system of special law enforcement access that was set up for the ‘good guys’ isn’t making us safer; it’s a dangerous security flaw” (Joe Mullin and Cindy Cohn, 9 October 2024): https://www.eff.org/deeplinks/2024/10/salt-typhoon-hack-shows-theres-no-security-backdoor-thats-only-good-guys
- Senator Ron Wyden and Representative Andy Biggs, a Democrat and a Republican, who asked the Director of National Intelligence in February 2025 to act against the UK’s order to Apple: https://www.wyden.senate.gov/imo/media/doc/wyden-biggs-letter-to-dni-re-uk-backdoors.pdf
- Also in this camp: the Global Encryption Coalition, which says it has over 400 members in 103 countries (https://www.globalencryption.org/); the 807 scientists and researchers who signed the September 2025 letter against chat control (https://csa-scientist-open-letter.org/Sep2025); Meta’s WhatsApp; European Digital Rights; Privacy International and Liberty, which are challenging the UK’s notices before the Investigatory Powers Tribunal; the Internet Society; Proton and Tuta; former MEP Patrick Breyer; the authors of “Keys Under Doormats” (2015) and “Bugs in Our Pockets” (2021).
Variation inside the camp: Members agree that no provider should be required to build decryption or scanning into end-to-end encrypted services, but differ on what else is acceptable. Some, including several of the cryptographers, accept targeted government hacking of individual suspects’ devices under warrant as the lesser evil; others, such as the Electronic Frontier Foundation, are critical of government hacking and the stockpiling of vulnerabilities as well. Meta defends encryption while using account behavior, metadata and user reports to find abuse on its encrypted services; Signal collects almost no metadata by design and treats that as part of the promise. Most accept voluntary scanning of unencrypted public content and cloud uploads; a minority oppose automated scanning generally. The US executive branch has joined this camp on the specific question of foreign orders against American companies, without renouncing lawful access at home.
Case: Encryption is how ordinary people, companies and governments protect themselves in a world of constant attack. It shields bank transfers, medical records, the messages of soldiers and diplomats, the sources of journalists and the plans of dissidents, and it protects children too, whose photos and locations are exactly what stalkers and extortionists want. There is no way to build a door that only the right people can open. Every access system ever built has eventually been abused or broken, from the Greek wiretapping scandal to Salt Typhoon, which went straight into the interception systems US law required, and led the government’s own cybersecurity agency to tell officials to use end-to-end encrypted apps. Scanning messages on the device before encryption is the same door by another name: once software reads every message and reports to an authority, the list of what it looks for can be changed by any government that can compel the company. The mathematics is public and open-source code cannot be recalled, so a mandate would push serious criminals to other tools and leave everyone else less secure. Child safety matters enormously, and it is better served by prevention, by resourcing police to act on the reports they already receive, by user reporting and by safety design than by a system that makes every conversation searchable.
Best evidence: Salt Typhoon compromised the systems US carriers use to carry out court-ordered wiretaps and, the FBI and CISA said, copied information “subject to U.S. law enforcement requests pursuant to court orders”; the FBI later said the campaign targeted more than 80 countries (Nextgov, https://www.nextgov.com/cybersecurity/2025/08/salt-typhoon-hackers-targeted-over-80-countries-fbi-says/407719/). In December 2024 CISA advised senior officials to “use only end-to-end encrypted communications.” Apple withdrew its 2021 on-device scanning design after sustained criticism, during which researchers showed that its matching algorithm could be made to produce false matches. The FBI’s claim of 7,775 phones it could not open in 2017 was overstated by programming errors, with an internal estimate near 1,200. EncroChat, Sky ECC and ANOM produced thousands of arrests without any encryption mandate. Irish police marked 11.2 percent of automated NCMEC referrals in 2020 as not abuse material and found 9.7 percent actionable (ICCL). The US wiretap report shows encryption blocking hundreds, not thousands, of intercepts a year.
Answer to the strongest objection: The strongest objection is that encryption without exceptions lets child abusers operate unseen and that reports have already fallen. Part of the fall in reports is an accounting change, bundling, that NCMEC itself adjusts for, and the rest is a real loss we do not deny. But reports are not rescues; police in many countries already cannot act on most of the reports they receive, and the measure that matters, children protected, depends on investigators, prevention and support services more than on report volume. Encrypted platforms can still act on user reports, unencrypted profile and group information, account behavior and metadata, and can design products that make it harder for strangers to reach children. Weakening encryption would not stop abuse; it would move offenders to other tools while exposing the private lives of billions of people, children among them, to anyone who breaks in.

Camp: Target individual suspects’ devices instead of mandating access
Adherents:
- German Federal Government (institution), whose cryptography policy since 1999 has been “security through encryption and security despite encryption”: it supports “developing, implementing and using strong encryption as a necessary means to protect fundamental rights” while holding that the legal powers of law enforcement “must not be undermined” despite encryption, and it has created narrowly limited powers for source telecommunications surveillance and online searches of suspects’ devices (Bundestag press service, 1 February 2021): https://www.bundestag.de/presse/hib/820140-820140. Justice Minister Stefanie Hubig said on 8 October 2025 that “unprovoked chat monitoring must be taboo in a constitutional state” and that Germany would not agree to such proposals at EU level (heise online): https://www.heise.de/en/news/Minister-of-Justice-Chat-control-is-taboo-in-a-constitutional-state-10747560.html
- European Parliament (institution), whose position on the child sexual abuse regulation, adopted in committee by 51 votes to 2 on 14 November 2023, allows detection orders only as a court-approved last resort, “targeted at individuals or groups” with reasonable grounds of suspicion, and excludes end-to-end encrypted communications: https://www.europarl.europa.eu/news/en/press-room/20231110IPR10118/child-sexual-abuse-online-effective-measures-no-mass-surveillance
- Steven Bellovin, Matt Blaze, Sandy Clark and Susan Landau, who argued in “Lawful Hacking: Using Existing Vulnerabilities for Wiretapping on the Internet” (2014) that exploiting existing vulnerabilities in suspects’ systems is a better path than mandating built-in wiretap interfaces: https://scholarlycommons.law.northwestern.edu/njtip/vol12/iss1/1/
- Also in this camp: the French and Dutch investigators behind the EncroChat operation and the FBI and Australian Federal Police behind ANOM, in practice if not in policy statements; Jens Spahn, leader of the CDU/CSU group in the Bundestag, who compared suspicionless chat monitoring to “opening all letters as a precautionary measure” (The Register, https://www.theregister.com/2025/10/08/germany_chat_control_opposition/).
Variation inside the camp: The shared idea is to go after the suspect rather than the service. Some emphasize government hacking of a named suspect’s phone under a warrant, as German law allows; some emphasize targeted, court-ordered detection limited to specific users of unencrypted services, as the European Parliament does; some emphasize infiltrating criminal encrypted networks, as in EncroChat and ANOM. Members differ on how far companies should be made to help: some would require providers to assist with a targeted operation short of changing encryption for everyone, as Australia’s voluntary and compulsory assistance notices allow; others want no provider involvement at all. A related position, set out by the Carnegie Endowment’s Encryption Working Group in 2019, would rule out access to encrypted messages in transit while continuing to study access to data on seized phones (https://carnegieendowment.org/research/2019/09/moving-the-encryption-policy-conversation-forward).
Case: The debate has been framed as a choice between weakening encryption for everyone and letting criminals go free, and both halves are wrong. Encryption protects the whole society and should stay strong on every device and service. But a warrant against a specific person still means something, and police can serve it on that person’s device, where messages are unencrypted to be read, rather than on the design of an app used by billions. Targeted hacking is expensive and slow, and that is a feature: it limits intrusion to serious cases a judge has approved, the same way physical surveillance always has. The biggest successes against encrypted crime, EncroChat, Sky ECC and ANOM, came this way and produced thousands of arrests. Suspicionless scanning of everyone’s messages, by contrast, is general surveillance of the kind European constitutions forbid, whatever its purpose.
Best evidence: EncroChat led to 6,558 arrests and close to 900 million euros seized after French investigators placed software on the network’s handsets (Europol, https://www.europol.europa.eu/media-press/newsroom/news/dismantling-encrypted-criminal-encrochat-communications-leads-to-over-6-500-arrests-and-close-to-eur-900-million-seized). ANOM gave investigators 27 million messages and more than 800 arrests coordinated through Europol without touching any mainstream app. Germany has operated under its “through and despite encryption” policy for over 25 years without mandating backdoors. Australia’s 2024–25 annual report shows agencies relying on 58 voluntary assistance requests and no compulsory capability notices (Home Affairs). The European Parliament’s targeted approach passed its civil liberties committee 51 to 2 across party lines.
Answer to the strongest objection: Two objections come from opposite sides. The first camp says targeted hacking does not scale: it is costly, local police cannot afford it, and it cannot find abuse nobody has reported. That is true, and it is the right trade: an investigative method that can be used against everyone at once is a surveillance system, and scale should come from more investigators and better cooperation, not from turning every phone into an informant. The second camp says government hacking depends on keeping vulnerabilities unpatched, leaving everyone exposed. That risk is real, but it is bounded: governments can be required to disclose most vulnerabilities they find, to use exploits only under judicial warrant and to report their use, and a flaw exploited quietly against a handful of suspects is a smaller danger than an access mechanism built into every copy of an app.

## Crux

Can any mechanism that lets authorities read end-to-end encrypted messages, whether by decrypting them on a court order or by scanning them on the device before they are encrypted, be built and run across billions of devices without creating a weakness that criminals, hostile states or abusive governments will eventually use, and if some risk remains, is what it buys for investigations and child protection worth that risk to everyone?

What evidence could settle: Whether a specific access or scanning design can survive sustained, independent attack; this could be tested by publishing designs and letting outside researchers try to break them, as has been done with encryption standards but never with an exceptional-access system at scale. How accurate on-device detection of known images, new images and grooming really is in live use, measured by independent testers rather than vendors. How many investigations and prosecutions end-to-end encryption actually defeats, and how many are solved by other means, which would need audited counts from police rather than the incomplete and sometimes inflated figures published so far. How many children are identified and protected, rather than reports filed, on encrypted and unencrypted services. Whether offenders move to niche tools when mainstream apps change, which could be studied where laws have already changed, such as in Australia and the UK.

What stays a value choice: How much residual risk to the security and privacy of everyone is acceptable in exchange for reaching a minority of offenders, when those who bear the risk and those who gain the benefit are different people. Whether a democratic society may allow any form of private communication that no warrant can reach, or whether the rule of law requires that a judge’s order be enforceable everywhere. Whether searching everyone’s messages for abuse without individual suspicion is ever proportionate, even when done by software and reviewed by people. Whose judgment should decide, legislatures and courts in each country or the companies and engineers who build products used worldwide.

## Actions

Kind: learn_more
Title: Read the National Academies’ framework for the encryption debate
What: A 2018 report by the US National Academies of Sciences, Engineering, and Medicine that sets out the questions any lawful-access proposal should answer, from effectiveness to security risk, without taking a side.
URL: https://nap.nationalacademies.org/catalog/25010/decrypting-the-encryption-debate-a-framework-for-decision-makers
Resolved: yes (200)
Serves: neutral

Kind: learn_more
Title: Read Congress’s researchers on the lawful access debate
What: A Congressional Research Service brief, updated January 2025, explaining the lawful access debate in the US, the law that governs it and the main proposals.
URL: https://www.everycrsreport.com/reports/IF11769.html
Resolved: yes (200; the congress.gov original at https://www.congress.gov/crs-product/IF11769 returned 403 to automated requests)
Serves: neutral

Kind: learn_more
Title: Follow the EU chat control negotiations
What: The European Parliament’s Legislative Train page tracks the proposed regulation to prevent and combat child sexual abuse, including the trilogue negotiations over detection and encryption.
URL: https://www.europarl.europa.eu/legislative-train/theme-promoting-our-european-way-of-life/file-combating-child-sexual-abuse-online
Resolved: yes (200)
Serves: neutral

Kind: learn_more
Title: Look at the US courts’ wiretap data
What: The annual Wiretap Reports from the Administrative Office of the US Courts count, among much else, how many court-ordered intercepts met encryption and how many could not be decrypted.
URL: https://www.uscourts.gov/data-news/reports/statistical-reports/wiretap-reports
Resolved: yes (200)
Serves: neutral

Kind: learn_more
Title: Read the case for lawful access from the US Justice Department
What: The Department of Justice’s lawful access page sets out its argument against “warrant-proof” encryption, with case examples and statements from US attorneys.
URL: https://www.justice.gov/olp/lawful-access
Resolved: yes (200)
Serves: Require encrypted services to give authorities access and detect abuse

Kind: policy
Title: Back ECPAT’s call for a permanent EU law on detecting child abuse
What: ECPAT International, a global network against the sexual exploitation of children, campaigns for a permanent EU legal framework guaranteeing continued detection of child sexual abuse online, and explains its case here.
URL: https://ecpat.org/this-is-no-april-fools-joke-europe-is-switching-its-detection-of-child-sexual-abuse-online-off/
Resolved: yes (200)
Serves: Require encrypted services to give authorities access and detect abuse

Kind: donate
Title: Support Thorn
What: A US nonprofit that builds detection technology used by platforms to find child sexual abuse material and advocates for stronger child-safety duties for online services.
URL: https://www.thorn.org/donate/
Resolved: yes (200)
Serves: Require encrypted services to give authorities access and detect abuse

Kind: policy
Title: Join the Global Encryption Coalition’s campaigns
What: A coalition of more than 400 organizations, companies and experts in 103 countries that lists current campaigns against laws and orders that would weaken encryption, with ways to take part.
URL: https://www.globalencryption.org/take-action/
Resolved: yes (200)
Serves: Keep end-to-end encryption closed to everyone but its users

Kind: donate
Title: Support the Electronic Frontier Foundation
What: A US digital-rights nonprofit that litigates and lobbies against encryption backdoors and client-side scanning mandates in the US and abroad.
URL: https://supporters.eff.org/donate
Resolved: yes (200)
Serves: Keep end-to-end encryption closed to everyone but its users

Kind: learn_more
Title: Use EFF’s Surveillance Self-Defense guide
What: A practical guide to choosing and using end-to-end encrypted tools, written for journalists, activists and ordinary users.
URL: https://ssd.eff.org/
Resolved: yes (200)
Serves: Keep end-to-end encryption closed to everyone but its users

Kind: learn_more
Title: Read the case for lawful hacking
What: The 2014 paper by Steven Bellovin, Matt Blaze, Sandy Clark and Susan Landau arguing that police should exploit existing vulnerabilities in targeted cases rather than require built-in access.
URL: https://scholarlycommons.law.northwestern.edu/njtip/vol12/iss1/1/
Resolved: yes (200)
Serves: Target individual suspects’ devices instead of mandating access

Kind: learn_more
Title: Read the Carnegie working group’s attempt at middle ground
What: A 2019 paper from a working group of former FBI, CIA and NSA officials, technologists and civil-liberties advocates that recommends setting aside access to encrypted messages in transit and focusing any debate on data stored on phones.
URL: https://carnegieendowment.org/research/2019/09/moving-the-encryption-policy-conversation-forward
Resolved: yes (200)
Serves: Target individual suspects’ devices instead of mandating access

## Sources

Council of the EU, note 13051/26, overview of legislative proposals under the Irish Presidency, 29 September 2026 — https://data.consilium.europa.eu/doc/document/ST-13051-2026-INIT/en/pdf — accessed 2026-09-29
Computer Weekly, Home Office challenged on “farcical” secrecy over Apple backdoor order, 17 September 2026 — https://www.computerweekly.com/news/366650612/Home-Office-challenged-on-farcical-secrecy-over-Apple-backdoor-order — accessed 2026-09-29
9to5Mac, Apple pushes UK court to lift secrecy around encryption backdoor order, 17 September 2026 — https://9to5mac.com/2026/09/17/apple-pushes-uk-court-to-lift-secrecy-around-encryption-backdoor-order/ — accessed 2026-09-29
Privacy International, PI Apple TCN challenge — https://privacyinternational.org/legal-action/pi-apple-tcn-challenge — accessed 2026-09-29
Law Gazette, Tribunal rejects government bid to keep data privacy row with Apple secret — https://www.lawgazette.co.uk/news/government-fails-to-keep-apple-legal-battle-secret/5122939.article — accessed 2026-09-29
Agence Europe, EU Council formally adopts extension of derogation from ePrivacy until 3 April 2028 — https://agenceurope.eu/en/bulletin/article/13915/9/eu-council-formally-adopts-extension-of-derogation-from-eprivacy-until-3-april-2028 — accessed 2026-09-29
Council of the EU press release, interim measure reinstated, 23 July 2026 (403 to automated requests) — https://www.consilium.europa.eu/en/press/press-releases/2026/07/23/fighting-child-sexual-abuse-online-interim-measure-protecting-children-now-reinstated/ — accessed 2026-09-29
Wikipedia, Chat Control — https://en.wikipedia.org/wiki/Chat_Control — accessed 2026-09-29
Wikipedia, Regulation to Prevent and Combat Child Sexual Abuse — https://en.wikipedia.org/wiki/Regulation_to_Prevent_and_Combat_Child_Sexual_Abuse — accessed 2026-09-29
ECPAT International, statement on the lapse of EU detection rules, 1 April 2026 — https://ecpat.org/this-is-no-april-fools-joke-europe-is-switching-its-detection-of-child-sexual-abuse-online-off/ — accessed 2026-09-29
US Courts, Wiretap Report 2025 — https://www.uscourts.gov/data-news/reports/statistical-reports/wiretap-reports/wiretap-report-2025 — accessed 2026-09-29
US Courts, Wiretap Report 2024 — https://www.uscourts.gov/data-news/reports/statistical-reports/wiretap-reports/wiretap-report-2024 — accessed 2026-09-29
US Courts, Wiretap Report 2022 — https://www.uscourts.gov/data-news/reports/statistical-reports/wiretap-reports/wiretap-report-2022 — accessed 2026-09-29
US Courts, Wiretap Report 2020 — https://www.uscourts.gov/data-news/reports/statistical-reports/wiretap-reports/wiretap-report-2020 — accessed 2026-09-29
US Courts, Wiretap Report 2018 — https://www.uscourts.gov/data-news/reports/statistical-reports/wiretap-reports/wiretap-report-2018 — accessed 2026-09-29
US Courts, Wiretap Report 2015 — https://www.uscourts.gov/data-news/reports/statistical-reports/wiretap-reports/wiretap-report-2015 — accessed 2026-09-29
US Courts, Wiretap Reports index — https://www.uscourts.gov/data-news/reports/statistical-reports/wiretap-reports — accessed 2026-09-29
NCMEC, 2025 CyberTipline Report — https://www.missingkids.org/content/dam/missingkids/pdfs/2025-cybertipline-report.pdf — accessed 2026-09-29
NCMEC, 2024 CyberTipline Report — https://www.missingkids.org/content/dam/missingkids/pdfs/2024-cybertipline-report.pdf — accessed 2026-09-29
NCMEC, NCMEC Releases New Data: 2024 in Numbers, 8 May 2025 — https://www.missingkids.org/blog/2025/ncmec-releases-new-data-2024-in-numbers — accessed 2026-09-29
NCMEC, 2023 CyberTipline reports by electronic service provider — https://www.missingkids.org/content/dam/missingkids/pdfs/2023-reports-by-esp.pdf — accessed 2026-09-29
NCMEC, 2024 CyberTipline reports by electronic service provider — https://www.missingkids.org/content/dam/missingkids/pdfs/2024-reports-by-esp.pdf — accessed 2026-09-29
NCMEC, 2025 CyberTipline reports by electronic service provider — https://www.missingkids.org/content/dam/missingkids/pdfs/2025-reports-by-esp.pdf — accessed 2026-09-29
NCMEC, End-to-End Encryption position — https://www.missingkids.org/theissues/end-to-end-encryption — accessed 2026-09-29
NBC News, Child exploitation watchdog says Meta encryption led to sharp decrease in tips, 8 May 2025 — https://www.nbcnews.com/tech/security/child-exploitation-watchdog-says-meta-encryption-led-sharp-decrease-ti-rcna205548 — accessed 2026-09-29
Meta, Launching default end-to-end encryption on Messenger, December 2023 — https://about.fb.com/news/2023/12/default-end-to-end-encryption-on-messenger/ — accessed 2026-09-29
National Crime Agency response to Meta’s rollout of end-to-end encryption, 7 December 2023 (WiredGov) — https://wired-gov.net/wg/news.nsf/articles/NCA+response+to+Metas+rollout+of+endtoendencryption+07122023161500?open= — accessed 2026-09-29
National Crime Agency, Virtual Global Taskforce statement on end-to-end encryption, 22 April 2024 — https://www.nationalcrimeagency.gov.uk/statement-on-end-to-end-encryption — accessed 2026-09-29
TechCrunch, WhatsApp now has more than 3 billion users a month, 1 May 2025 — https://techcrunch.com/2025/05/01/whatsapp-now-has-more-than-3-billion-users/ — accessed 2026-09-29
Nextgov/FCW, Salt Typhoon hackers targeted over 80 countries, FBI says, 27 August 2025 — https://www.nextgov.com/cybersecurity/2025/08/salt-typhoon-hackers-targeted-over-80-countries-fbi-says/407719/ — accessed 2026-09-29
FBI and CISA joint statement on PRC targeting of commercial telecommunications infrastructure, 13 November 2024 (403 to automated requests) — https://www.cisa.gov/news-events/news/joint-statement-fbi-and-cisa-peoples-republic-china-targeting-commercial-telecommunications-infrastructure — accessed 2026-09-29
CISA, Mobile Communications Best Practice Guidance, December 2024 (403 to automated requests) — https://www.cisa.gov/sites/default/files/2024-12/guidance-mobile-communications-best-practices.pdf — accessed 2026-09-29
EFF, Salt Typhoon Hack Shows There’s No Security Backdoor That’s Only For The “Good Guys,” 9 October 2024 — https://www.eff.org/deeplinks/2024/10/salt-typhoon-hack-shows-theres-no-security-backdoor-thats-only-good-guys — accessed 2026-09-29
EFF, Government Hacking and Subversion of Digital Security — https://www.eff.org/issues/government-hacking-digital-security — accessed 2026-09-29
Europol, EncroChat results press release, 27 June 2023 — https://www.europol.europa.eu/media-press/newsroom/news/dismantling-encrypted-criminal-encrochat-communications-leads-to-over-6-500-arrests-and-close-to-eur-900-million-seized — accessed 2026-09-29
Wikipedia, EncroChat — https://en.wikipedia.org/wiki/EncroChat — accessed 2026-09-29
Wikipedia, Operation Trojan Shield — https://en.wikipedia.org/wiki/Operation_Trojan_Shield — accessed 2026-09-29
FBI, results of Operation Trojan Shield, 8 June 2021 (403 to automated requests) — https://www.fbi.gov/news/stories/fbi-global-partners-announce-results-of-operation-trojan-shield-060821 — accessed 2026-09-29
CSO Online, FBI “going dark” figure: locked out of only 1,200 phones, not 7,775, 23 May 2018 — https://www.csoonline.com/article/565476/fbi-going-dark-whopper-locked-out-of-only-1200-phones-not-7775.html — accessed 2026-09-29
EFF, FBI admits it inflated number of supposedly unhackable devices, May 2018 — https://www.eff.org/deeplinks/2018/05/fbi-admits-it-inflated-number-supposedly-unhackable-devices — accessed 2026-09-29
European Commission, Eurobarometer on protection of children against online sexual abuse, 20 July 2023 — https://home-affairs.ec.europa.eu/news/strong-support-citizens-across-eu-prevent-and-combat-child-sexual-abuse-online-2023-07-20_en — accessed 2026-09-29
Patrick Breyer, Poll: 72% of citizens oppose EU plans to search all private messages, 28 April 2021 — https://www.patrick-breyer.de/en/poll-72-of-citizens-oppose-eu-plans-to-search-all-private-messages-for-allegedly-illegal-material-and-report-to-the-police/ — accessed 2026-09-29
Pew Research Center, More Support for Justice Department Than for Apple in Dispute Over Unlocking iPhone, 22 February 2016 — https://www.pewresearch.org/politics/2016/02/22/more-support-for-justice-department-than-for-apple-in-dispute-over-unlocking-iphone/ — accessed 2026-09-29
Wikipedia, Apple–FBI encryption dispute — https://en.wikipedia.org/wiki/FBI%E2%80%93Apple_encryption_dispute — accessed 2026-09-29
Irish Council for Civil Liberties, An Garda Síochána unlawfully retains files on innocent people, 19 October 2022 — https://www.iccl.ie/news/an-garda-siochana-unlawfully-retains-files-on-innocent-people-who-it-has-already-cleared-of-producing-or-sharing-of-child-sex-abuse-material/ — accessed 2026-09-29
Australian Department of Home Affairs, TIA Act and Part 15 Telecommunications Act Annual Report 2024–25 — https://www.homeaffairs.gov.au/criminal-justice/files/telecommunications-interception-and-access-reports/telecommunications-interception-access-act-1979-annual-report-24-25.pdf — accessed 2026-09-29
Joint statement of scientists and researchers on the proposed CSA Regulation, September 2025 — https://csa-scientist-open-letter.org/Sep2025 — accessed 2026-09-29
Levy and Robinson, Thoughts on child safety on commodity platforms, 2022 — https://arxiv.org/abs/2207.09506 — accessed 2026-09-29
Abelson et al., Bugs in Our Pockets: The Risks of Client-Side Scanning, 2021 — https://arxiv.org/abs/2110.07450 — accessed 2026-09-29
Abelson et al., Keys Under Doormats, MIT CSAIL, 2015 — https://dspace.mit.edu/handle/1721.1/97690 — accessed 2026-09-29
Berkman Center, Don’t Panic: Making Progress on the “Going Dark” Debate, 2016 — https://cyber.harvard.edu/pubrelease/dont-panic/Dont_Panic_Making_Progress_on_Going_Dark_Debate.pdf — accessed 2026-09-29
European Parliament press release, Child sexual abuse online: effective measures, no mass surveillance, 14 November 2023 — https://www.europarl.europa.eu/news/en/press-room/20231110IPR10118/child-sexual-abuse-online-effective-measures-no-mass-surveillance — accessed 2026-09-29
European Commission, Commission presents Roadmap for effective and lawful access to data for law enforcement, 24 June 2025 — https://home-affairs.ec.europa.eu/news/commission-presents-roadmap-effective-and-lawful-access-data-law-enforcement-2025-06-24_en — accessed 2026-09-29
European Commission, Encryption (lawful access to data) — https://home-affairs.ec.europa.eu/policies/internal-security/lawful-access-data/encryption_en — accessed 2026-09-29
Europol, Joint Declaration of the European Police Chiefs, April 2024 — https://www.europol.europa.eu/cms/sites/default/files/documents/EDOC-%231384205-v1-Joint_Declaration_of_the_European_Police_Chiefs.PDF — accessed 2026-09-29
US Department of Justice, Office of Legal Policy, Lawful Access — https://www.justice.gov/olp/lawful-access — accessed 2026-09-29
Computer Weekly, Europol seeks evidence of encryption on crime enforcement, 22 January 2025 — https://www.computerweekly.com/news/366618230/Europol-seeks-evidence-of-encryption-on-crime-enforcement-as-it-steps-up-pressure-on-Big-Tech — accessed 2026-09-29
UK Government, International statement: End-to-end encryption and public safety, October 2020 — https://www.gov.uk/government/publications/international-statement-end-to-end-encryption-and-public-safety/international-statement-end-to-end-encryption-and-public-safety-accessible-version — accessed 2026-09-29
Signal, For a future with privacy, not mass surveillance, 3 October 2025 — https://signal.org/blog/pdfs/germany-chat-control.pdf — accessed 2026-09-29
Apple Support, Advanced Data Protection unavailable in the UK — https://support.apple.com/en-us/122234 — accessed 2026-09-29
Wyden and Biggs letter to the Director of National Intelligence, 13 February 2025 — https://www.wyden.senate.gov/imo/media/doc/wyden-biggs-letter-to-dni-re-uk-backdoors.pdf — accessed 2026-09-29
The Record, Gabbard: UK demand to Apple for backdoor access is “grave concern,” 26 February 2025 — https://therecord.media/odni-gabbard-uk-apple-backdoor-request-grave-concern — accessed 2026-09-29
Nextgov/FCW, UK “agreed to drop” backdoor encryption demand for Apple, DNI says, August 2025 — https://www.nextgov.com/cybersecurity/2025/08/uk-agreed-drop-backdoor-encryption-demand-apple-dni-says/407556/ — accessed 2026-09-29
Global Encryption Coalition — https://www.globalencryption.org/ — accessed 2026-09-29
Deutscher Bundestag, hib 141/2021, Quellen-TKÜ oder Online-Durchsuchung, 1 February 2021 — https://www.bundestag.de/presse/hib/820140-820140 — accessed 2026-09-29
heise online, Minister of Justice: “Chat control is taboo in a constitutional state,” 8 October 2025 — https://www.heise.de/en/news/Minister-of-Justice-Chat-control-is-taboo-in-a-constitutional-state-10747560.html — accessed 2026-09-29
The Register, Germany slams brakes on EU’s Chat Control, 8 October 2025 — https://www.theregister.com/2025/10/08/germany_chat_control_opposition/ — accessed 2026-09-29
Bellovin, Blaze, Clark and Landau, Lawful Hacking, Northwestern Journal of Technology and Intellectual Property, 2014 — https://scholarlycommons.law.northwestern.edu/njtip/vol12/iss1/1/ — accessed 2026-09-29
Carnegie Endowment Encryption Working Group, Moving the Encryption Policy Conversation Forward, September 2019 — https://carnegieendowment.org/research/2019/09/moving-the-encryption-policy-conversation-forward — accessed 2026-09-29
Landau, testimony to the House Judiciary Committee, 5 June 2025 — https://www.congress.gov/119/meeting/house/118335/witnesses/HHRG-119-JU08-Wstate-LandauS-20250605.pdf — accessed 2026-09-29
National Academies, Decrypting the Encryption Debate, 2018 — https://nap.nationalacademies.org/catalog/25010/decrypting-the-encryption-debate-a-framework-for-decision-makers — accessed 2026-09-29
Congressional Research Service, Law Enforcement and Technology: The “Lawful Access” Debate (IF11769) — https://www.everycrsreport.com/reports/IF11769.html — accessed 2026-09-29
European Parliament Legislative Train, Combating child sexual abuse online — https://www.europarl.europa.eu/legislative-train/theme-promoting-our-european-way-of-life/file-combating-child-sexual-abuse-online — accessed 2026-09-29
Thorn, donate — https://www.thorn.org/donate/ — accessed 2026-09-29
Global Encryption Coalition, take action — https://www.globalencryption.org/take-action/ — accessed 2026-09-29
EFF, donate — https://supporters.eff.org/donate — accessed 2026-09-29
EFF, Surveillance Self-Defense — https://ssd.eff.org/ — accessed 2026-09-29
