# Annotation Rubric — EU AI Act Risk-Tier Classification of AI Incidents

*Frozen 26 August 2026, before any incident was labelled. The results reported in
"Category, Not Severity" (SiKDD 2026) are scored against this version; it was not
revised afterwards. Written by a lawyer; the interpretive positions are the author's.*

## Purpose and framing

This rubric operationalizes the EU AI Act's risk-classification test (Regulation (EU) 2024/1689) for application to short incident records from the AI Incident Database. It answers a **counterfactual classification question**:

> *If the AI system involved in this incident were placed on the EU market or put into service today (August 2026), which risk tier would it fall under?*

Two framing rules:
1. **Classify the system, not the harm.** The Act's tiers attach to a system's intended purpose and context of use — not to how bad the incident's outcome was. A fatal crash of a system outside Annex III is not thereby "high-risk"; a mundane-sounding CV-screening tool inside Annex III is. This distinction is applied strictly throughout.
2. **Jurisdiction is hypothetical.** Most incidents occurred outside the EU or before the Act. Treat the Act as applicable; ignore territorial and temporal scope (Art. 2 questions are out of scope; note in `notes` if this feels distortive for a given incident).

## Evidence rules

- Label primarily from the provided fields: `title`, `description`, `deployer`, `developer`, `harmed`, `year`.
- You MAY open the `aiid_url` page to resolve ambiguity about what the system is or does. If you do, set `consulted_full_page = yes`. (The models see only the provided fields; this asymmetry is disclosed in the paper.)
- If even the full page does not let you identify the system's function and deployment context well enough to run the test, set `FINAL_risk_tier = insufficient_information` and stop.

## Threshold gate — is it an AI system at all? (Art. 3(1))

Before applying any step below, ask whether the thing described is an "AI system"
within Article 3(1): *"a machine-based system that is designed to operate with
varying levels of autonomy and that may exhibit adaptiveness after deployment, and
that, for explicit or implicit objectives, infers, from the input it receives, how
to generate outputs such as predictions, content, recommendations, or decisions that
can influence physical or virtual environments."* This definition must be passed
through before any of the risk-tier steps are reached. Where the record shows a
purely deterministic, rule-based process with no inferential element, record
`FINAL_risk_tier = not_ai_system` and stop. Where there is not enough information to
determine whether the system can be subsumed under this definition, mark `unclear`
in the relevant step. Given that the definition is quite broad, I do not expect a
significant number of such cases.

## Decision procedure

Apply steps in order. The first tier triggered wins, with the profiling override at Step 5. Record each step in its labelled column even after the tier is determined, so we can analyze where models diverge.

### Step 1 — Prohibited practices, Art. 5 → `L1_art5_prohibited`
Does the system, as used in the incident, constitute a practice prohibited by Art. 5(1)? Checklist of categories (a)–(h):
- (a) subliminal / purposefully manipulative or deceptive techniques materially distorting behaviour, causing significant harm
- (b) exploitation of vulnerabilities (age, disability, social/economic situation)
- (c) social scoring by public or private actors leading to detrimental treatment
- (d) risk assessment predicting criminal offences based solely on profiling/personality traits
- (e) untargeted scraping of facial images for facial-recognition databases
- (f) emotion recognition in workplace or education institutions (health/safety exceptions)
- (g) biometric categorisation inferring sensitive attributes
- (h) real-time remote biometric identification in publicly accessible spaces for law enforcement (with exceptions)

I would interpret Article 5(1)(a) narrowly because it is a prohibitive norm. Its effect is the highlight here because it encompasses both subliminal and purposeful techniques as the means to the prohibited negative outcome or objective. The prohibited negative outcome or objective is *materially* distorting the behavior of a person or group of persons by *appreciably* impairing their ability to make an informed decision, thereby causing them to take a decision that they would otherwise not have taken that either causes or would reasonably likely cause them or other persons *significant* harm. From this framing, a chain of action is immediately noticeable from this provision. A person's or group of persons behavior would be materially distorted only if their ability to make an informed decision would be appreciably impaired, and this should result or be reasonably likely to result in significant harm being done to a person or group thereof. This would be the case where a model would be trained or configured (through a system prompt for example) to use a subliminal or purposeful technique to lead to the prohibited outcome. Intent to cause harm is not required, the effect or objective would satisfy the provision. However, it is important to discern regular hallucinations and genuine model limits from an architectural and technical standpoint from (un)intentional techniques leading to the prohibited behavior. An interesting edge case would be emergently manipulative systems, like engagement optimized-recommenders that were never designed to but learned to manipulate. I would mark these edge-cases as "unclear". 

Article 5(1)(b) is straightforward. The term vulnerability must not be construed to merely the physical or psychological aspects, but rather the entire circumstances of the person's position must be taken into account. The term exploit also must be interpreted more broadly in favor of the victim, and in this sense, to exploit would also mean to take action that may not necessarily cause direct harm to the person, but may benefit the company. For example, exploitation is also the case where a company is to collect personal data related to a vulnerability and use that data for anything other than the person's interest without him knowing and consenting to it.

Article 5(1)(c) addresses what is commonly known as social scoring. This provision is to be interpreted especially carefully because there it is not completely prohibiting social scoring. It does not outright prohibit building models that conduct social scoring, instead, it merely prohibits using already an existing social scoring analysis made by a model for an unrelated social context or disproportionally negatively treating particular persons to their social score and its respective gravity. 

Article 5(1)(d) is once again another peculiar provision. Here, the Act prohibits AI systems that exist to predict the risk of a person committing a crime based solely on personality traits or psychological profiling. It does not, however, prohibit a model to assist human analysts to profile based on actual pre-existing crimes or current suspected crimes with objective and verifiable evidence directly linked to the suspected criminal activity. 

Article 5(1)(e) is another straightforward provision. It prohibits the untargeted scraping by AI of facial images from the internet or CCTV footage targeted to expand or create databases. 

Article 5(1)(f) is a only a seemingly straightforward provision. It prohibits the use of AI to infer emotions from natural persons in areas of workplace and education institutions. However, this is exempt for medical and safety reasons. The medical and safety reasons in question must be interpreted in a strict sense, favorable to the person's emotional privacy. The institution running the AI that emotionally profiles these persons in such places must have clear medical institutional backing, and doing such profiling for a legitimate cause in order for it to be exempt from the prohibition. The same applies for the institution running the AI for safety reasons. There must be a clear and legitimate goal for the exemption, based on one or multiple verifiable facts.

Article 5(1)(g) is put in place to protect individual sensitive data tied to the natural person: race, political opinions, trade union membership, religious or philosophical beliefs, sex life or sexual orientation. This list is exhaustive. It, does not however prohibit the filtering or labeling lawfully acquired biometric datasets; or categorizing biometric data in the area of law enforcement. The provision is explicit when it states words such as "filtering", "labeling" and "categorizing" of "biometric datasets" and "biometric data" such as "images". This means that the non-biometric sensitive attributes of the natural person are in any case and always protected, while the lawfully acquired biometric data can only be filtered and labelled, as well as categorized in the area of law enforcement but not processed in other means. I would interpret law enforcement as the official state run law enforcement and trusted private subcontractors and partners. 

The last provision, Article 5(1)(h) is also quite straightforward. It prohibits the use of 'real-time' remote biometric identification systems in publicly accessible spaces (note: not just public spaces, but also publicly accessible, meaning potentially even private property if left publicly accessible given the circumstances) for the purposes of law enforcement, unless strictly necessary for either: target searching victims of abduction, human trafficking, sexual exploitation as well as missing persons; for the prevention of a genuine, specific and imminent threat to life or physical safety of natural persons, as well as for the prevention of a present terrorist attack or foreseeable threat of such; and locating or identifying a suspect wanted for specific serious crimes punishable by a prison sentence of at least four years.

If yes → `FINAL_risk_tier = prohibited`.

### Step 2 — Annex I product-safety route, Art. 6(1) → `L3_annex_i_product`
Is the AI a product or safety component covered by Union harmonisation legislation in Annex I (machinery, toys, lifts, medical devices, in-vitro diagnostics, vehicles, aviation, marine, rail, pressure equipment, PPE, gas appliances, cableways) that undergoes third-party conformity assessment?

Pursuant to Article 6(1) of the EU AI Act, an AI system can be considered "high-risk" if it is a product/safety component covered by the Union harmonisation legislation in Annex I and pursuant to this, is required to undergo a third-party conformity assessment. It is very hard to qualify some edge cases and reports to identify whether the product is required to undergo a third-party conformity assessment in accordance with Union harmonisation legislation in Annex I because of vague or inconclusive reports, which would lead to many "unclear" labels. A rule of thumb that can reasonably be applied here is to classify products *normally* requiring third-party conformity assessment as such, unless the record proves otherwise. Argumentum a contrario, if the product type normally self-certifies, they should be classified as such that do not require third-party conformity assessment, unless the record proves otherwise. Finally, if we cannot even reasonably tell what the product is from the perspective of a third reasonable person, they should be labelled as "unclear".

Normally third-party assessed are:
- Motor vehicles and trailers, Reg. (EU) 2018/858 [driver-assistance, autopilot,
    robotaxis, automatic emergency braking]
  - Two- and three-wheel vehicles and quadricycles, Reg. (EU) 168/2013 [motorcycle
    ABS and stability control, e-scooter speed governors]
  - Agricultural and forestry vehicles, Reg. (EU) 167/2013 [autonomous tractors,
    self-steering harvesters]
  - Aircraft and aviation products, Reg. (EU) 2018/1139 [autopilot, flight control,
    collision avoidance, certified-category drones]
  - Rail subsystems, Dir. (EU) 2016/797 [automatic train operation, signalling,
    train protection systems]
  - Marine equipment, Dir. 2014/90/EU [shipboard navigation, radar, collision
    avoidance]
  - Lifts and lift safety components, Dir. 2014/33/EU [AI overload detection or
    dispatch acting as a safety component]
  - Cableway installations, Reg. (EU) 2016/424 [ski-lift and gondola control and
    braking systems]
  - Appliances burning gaseous fuels, Reg. (EU) 2016/426 [smart boiler burner control]
  - Medical devices Class IIa, IIb, III, Reg. (EU) 2017/745 [AI diagnostic imaging,
    triage and early-warning systems, patient monitoring, surgical robots]
  - In vitro diagnostics Class B, C, D, Reg. (EU) 2017/746 [AI interpretation of lab
    assays, cancer screening]
  - PPE Categories II and III, Reg. (EU) 2016/425 [smart helmets, connected
    fall-arrest harnesses, powered respirators]
  - Pressure equipment Categories II–IV, Dir. 2014/68/EU [AI control of industrial
    boilers and pressure vessels]
  - ATEX equipment Categories 1 and 2, Dir. 2014/34/EU [sensing and control equipment
    in explosive atmospheres, e.g. refineries, mines]
    
Normally self-certified are:
- General industrial machinery, Reg. (EU) 2023/1230 [warehouse and picking robots,
    robotic arms, CNC machines, packaging lines] — but see the ML carve-out below
  - Toys, Dir. 2009/48/EC, where harmonised standards are fully applied [AI talking
    dolls, companion robot pets, interactive learning toys]
  - Radio equipment, Dir. 2014/53/EU, where harmonised standards are fully applied
    [smart speakers, smartphones, smartwatches, consumer IoT cameras]
  - Medical devices Class I, non-sterile, non-measuring, non-reusable-surgical, MDR
    [wellness and fitness apps making no diagnostic claim]
  - In vitro diagnostics Class A, non-sterile, IVDR [general laboratory instruments]
  - PPE Category I, Reg. (EU) 2016/425 [sunglasses, gardening gloves]
  - Pressure equipment Category I, Dir. 2014/68/EU [low-hazard vessels]
  - ATEX Category 3, Dir. 2014/34/EU [zone 2 equipment]
  
  
Two counter-intuitive refinements however are:
- Machinery in which the AI is with fully or partially self-evolving behaviour using machine-learning approaches that perform safety functions, and machinery embedding such systems. Where the AI *is* the safety function.
- Medical software, which is rarely self-certified. Step counters and basic medical systems are self-certified, but systems like for example melanoma detectors which scan warts, are almost certainly requiring third party assessment.

If yes → `FINAL_risk_tier = high` (skip Step 4; the Art. 6(3) derogation does not apply to the Annex I route).

### Step 3 — Annex III area, Art. 6(2) → `L2_annex_iii_domain`
Does the system's use in the incident fall within one of the eight Annex III areas? Use these values:
1. `biometrics` — remote biometric ID, biometric categorisation, emotion recognition (insofar as not prohibited)
2. `critical_infrastructure` — safety components in management/operation of critical digital infrastructure, road traffic, water/gas/heating/electricity supply
3. `education` — access/admission, learning-outcome evaluation, level assessment, cheating monitoring
4. `employment` — recruitment/selection (targeted ads, screening, evaluating candidates), and decisions on promotion/termination, task allocation, monitoring/evaluation
5. `essential_services` — eligibility for public assistance benefits/services; creditworthiness (except financial-fraud detection); risk assessment/pricing in life & health insurance; emergency-call triage/dispatch
6. `law_enforcement` — victim-risk assessment, polygraphs, evidence-reliability evaluation, offending/re-offending risk (not solely profiling), profiling in investigations
7. `migration` — polygraphs, risk assessments, examination of asylum/visa/residence applications, identification of persons (border context)
8. `justice_democracy` — assisting judicial authorities in researching/interpreting facts and law, alternative dispute resolution with legal effect, influencing elections/voting behaviour

There can be many edge cases where certain incidents can be labelled in multiple areas or can be both labelled none and in a certain area. One of those is when cartels or criminals use AI for criminal activities. It is easy to mislabel this use as if belonging to the law enforcement area, however, this would be a mistake. Even though it is a matter of law enforcement activities, the provision assumes that the AI is intended to be used by the law enforcement organizations themselves. If a cartel or criminal organization could obtain such a system, that still would not be sufficient to label it as belonging to the law enforcement area, because the intent of AI system was to be used by law enforcement organizations themselves. The proper label here would be to label this edge case as belonging to none of these areas.

In cases such as S059, where there is a suspension of universal credit over suspected benefit fraud, they naturally fall into the category of essential services. 5(a) is quite broad and includes AI systems that to "grant, reduce, revoke, or reclaim" an essential service as high risk. Suspension of an essential service no doubt falls into this category.

In regards to Home Office algorithms flagging sham marriages, I believe that this should be under the migration category if the Office runs the algorithm precisely to detect sham marriages for regulating migration. It should not, however, fall into the category of law enforcement since the under Annex III if the aforementioned purpose is correct. Technically Home Offices can qualify as law enforcement in the functional sense of the definition that Annex III provides for law enforcement, all the more given if migration is a criminal offense. However, I believe that the migration area is the closest related field because of the underlying purpose of detecting sham marriages -- to stop illegal migration.

For S067 and similar occurrences, the correct area is justice and democracy because of the mere intent to influence election outcomes/voting behavior. This, however, should not apply to AI systems that are not designed by their creators to influence election outcomes and/or voting behavior because if this were correct, a large plethora of AI systems could fall into the same category merely given the use case. The intent should be assessed based on how the system was built and put into service. A general voice cloning tool, built not for the purpose of meddling in elections and voter decisions would be clear of a high risk label, however, if the party building or deploying it built it for this purpose, then it would constitute as such.

For S041, S026 and similar cases, despite the obvious risky nature, they do not fall under any area because moderation is in the DSA area and product recommendation is regulated by consumer law.

S019 in my opinion however is covered by 4(b), the act does not mandate an employment contract to exist, but rather uses the broad term "work-related relationships".

If none apply → `L2 = none`, go to Step 6.

### Step 4 — Art. 6(3) derogation → `L4_art6_3_derogation`
The system is in an Annex III area, but is it nonetheless *not* high-risk because it does not pose a significant risk of harm to health, safety or fundamental rights, including by not materially influencing decision outcomes? The derogation applies where any of the four conditions holds:
- (a) narrow procedural task
- (b) improving the result of a previously completed human activity
- (c) detecting decision-making patterns or deviations, not meant to replace/influence the completed human assessment without proper review
- (d) preparatory task to an assessment relevant for Annex III use cases

When it comes to flagging for human investigation, there are usually two arguments which can be made pro et contra for determining whether the AI is exempt under 6(3)(c) or not. The first argument, pro exemption merely states that the AI does the flagging and humans are the ones making the decisions, but the opposite, not unreasonable counter argument states that the AI is actually the one making the decision of who gets flagged, therefore indirectly deciding the outcome by materially influencing the decision making process. However, if we examine the wording closely of 6(3)(c), it states that the system  "is not meant to replace or *influence* the previously completed human assessment without proper human review". This generous framing contra exemption leads to flagging generally being considered as not exempt. In addition, this argumentation may also be unnecessary for the simple reason that flagging people's reliability and behavior from personal data constitutes profiling under GDPR 4(4), which is automatically considered as high-risk. Of course, this depends on the type of flagging being done, and it is not to say that every type of flagging represents profiling and that certain flagging cannot be exempt. A diligent review of the concrete situation is necessary for correct judgement.

Finally, a pressing question that will no doubt be most common is what would happen when the record is silent about the system's role or is vague enough that the system role cannot be classified with the necessary confidence. In that case, I suggest the exemptions only applying if there is concrete evidence in the record that the system performs as the provision exemptions declare, but where the system appears to drive decisions or select decisions and the record is silent, the natural conclusion would be that the exemptions do not apply. Last but not least, where the system's role cannot be identified at all, the natural choice is to mark the scenario as unclear. 

### Step 5 — Profiling override, Art. 6(3) 2nd subpara → `L5_profiling_override`
Regardless of Step 4: does the system perform profiling of natural persons (Art. 3(52) → GDPR Art. 4(4) definition)? If yes, it is always high-risk when in an Annex III area.

If (Annex III area) AND (derogation does not apply OR profiling) → `FINAL_risk_tier = high`.

### Step 6 — Transparency obligations, Art. 50 → `L6_art50_transparency`
Record `yes` if the system is subject to Art. 50 transparency duties (record even for high/prohibited systems — the column is independent):
- AI systems intended to interact directly with natural persons (chatbots)
- Synthetic audio/image/video/text generation (deep fakes; AI-generated content marking)
- Emotion recognition / biometric categorisation systems (disclosure duty)

If the FINAL tier is not yet set and `L6 = yes` → `FINAL_risk_tier = transparency`.

### Step 7 — Default
Nothing triggered → `FINAL_risk_tier = minimal`.

## Confidence and notes
- `confidence_1to3`: 3 = another EU-law practitioner would very likely agree; 2 = defensible but contestable; 1 = genuine coin-flip after full analysis. (We report the distribution and analyze disagreement by confidence band.)
- `notes`: one short line on the deciding factor, especially for confidence 1–2 and for `insufficient_information`. These notes feed the paper's qualitative examples.

## Sources (verify wording against the Official Journal text)
- Regulation (EU) 2024/1689, EUR-Lex CELEX 32024R1689: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32024R1689
- Convenient article navigation: https://artificialintelligenceact.eu/article/5/ , /article/6/ , /article/50/ , /annex/1/ , /annex/3/
- Commission Guidelines on prohibited practices (Feb 2025) and on high-risk classification
