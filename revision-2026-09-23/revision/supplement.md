# Supplement: Legal Categories from Incident Reports

Submission 109; revision completed 23 September 2026. This supplement preserves the original experiment and reports the separately identified expanded-evidence follow-up in S11. Neither analysis establishes independent expert validation.


## S1. Scope, evidence and reproducibility

The original v2 manuscript, rubric, prompts, reference labels, outputs and correction log are preserved under `research/inputs/` in the companion archive. Original-research relative paths below are resolved from `research/`; new S13–S15 paths are resolved from `revision/`. The legal reference is the first author's expert assessment under that interpretation and available evidence. Model disagreement is not by itself proof of a legal mistake. The nominal measures use all 144 records and six labels; missing outputs count as nonmatches. The separate 22 September model-only follow-up is reported in S11. The expert has not reassessed the historical reference against its new evidence packets.

In the companion archive, `research/` contains the archived inputs, outputs and original analysis scripts. Run `python analysis/revise_analysis.py` from that directory with numpy, pandas, openpyxl and matplotlib installed to reproduce the original numerical analysis. Run `python analysis/additional_sensitivity.py` from `revision/` for the added diagnostics. The archive README identifies all paths; do not run these commands from the reading-only extract. No network or credentials are used. `results/input_hashes.json` identifies the source bytes. `results/*_metrics.csv`, `*_class_metrics.csv`, `*_confusions.csv` and `*_direction.csv` provide unrounded results and denominators. All 28 submitted QWK point estimates are reproduced within 0.00051 of the rounded original values.

The revised four-page manuscript was resubmitted to EasyChair as paper 109, version 3, on 23 September 2026. The paper and companion are published in the accompanying repository. Final conference acceptance remains a decision for the chairs.


## S2. Dataset and sampling

The official AIID workbook dated 2026-08-10 has 1,618 incident rows; all 1,618 have a title and description. The stored script matches keywords in title, description, developer, deployer and harmed-party fields. The stratum with most keyword matches wins, with a fixed domain ordering for ties. A NumPy random generator with seed 2026 samples up to 13 records per domain; unfilled places enter the control sample. This is an enriched draw, not a population-prevalence design.

150 sampled - 6 documented development examples = 144 evaluated. The original workflow split was 44 `dev` and 106 `heldout`; after exclusions it is 42 and 102. The evaluation years are 2012–2026; description lengths are 64–599 characters, median 358. Party fields and year supplement that text. Keyword strata are absent from the model request and must not be treated as legal labels.

Class counts: transparency: 77, high: 44, prohibited: 10, minimal: 9, not_ai_system: 2, insufficient_information: 2. Expert confidence (1–3): {'3': 96, '2': 47, '1': 1}. Confidence is self-assessment, not externally calibrated correctness.

| Evaluation keyword bucket | Incidents |
| --- | --- |
| control_pool | 45 |
| employment | 13 |
| biometrics | 13 |
| justice_democracy | 13 |
| education | 12 |
| migration | 12 |
| essential_services | 12 |
| critical_infrastructure | 12 |
| law_enforcement | 12 |

| Reference Annex III area | Incidents |
| --- | --- |
| none | 109 |
| biometrics | 13 |
| migration | 7 |
| essential_services | 6 |
| law_enforcement | 3 |
| employment | 2 |
| unclear | 2 |
| education | 1 |
| justice_democracy | 1 |

The two unclear-domain records have auxiliary reference labels and contribute no ordinal pairs to the directional contrasts. Their absence from that plot must not be interpreted as zero uncertainty. Fourteen model answers on a single education incident are still one incident.


## S3. Development history and coverage

The six exclusions are documented in `rubric_dev_exclusions.csv`. Original notes explicitly discuss S019, S026, S041, S059 and S067; they also discuss the Home Office sham-marriage case matching S028 without giving that ID. These examples concentrate on Annex III boundaries. They are not a representative validation sample and do not demonstrate coverage of every prohibition, the product route or the full insufficient-evidence gate.

The saved files do not establish a prospectively random selection procedure. Early planning notes proposed prompt iteration on a 44-record development split. Later manuscript text describes six examples, while the archived rubric says it was frozen before any annotation. The correction script explicitly documents a subsequent change in the author's Article 5 interpretation and propagation to earlier labels. We therefore remove claims of preregistration, complete blinding, an untouched pooled test set or an immutable interpretation throughout annotation. The first author now confirms that he revised the labels before seeing any model answers. This author-reported timing does not reconstruct the full early selection procedure or establish an untouched pooled test set; see S12.

| Case | Documented topic | Boundary discussed |
| --- | --- | --- |
| S019 | Employment; work-related relationships | Whether gig-platform pay decisions fall within Annex III 4(b). |
| S026 | Outside Annex III; product recommendations | Distinguishing recommendations from a listed use; consumer-law context does not by itself settle AI Act status. |
| S028 | Migration versus law enforcement | Identify the intended administrative purpose of sham-marriage screening. |
| S041 | Outside Annex III; content moderation | Distinguish content-moderation harm from a listed use; DSA applicability is not a universal AI Act exclusion. |
| S059 | Essential public services; fraud review | Benefit suspension/recovery and whether human review makes the system merely preparatory. |
| S067 | Electoral purpose versus general voice cloning | Distinguish the described use, intended purpose and operator role. |

The archived first-page “frozen” wording is preserved as evidence, not repeated as a verified methodological claim. Nineteen fields on ten records were changed in the published correction log; earlier workbook revisions are not necessarily exhausted by that log. No new reference labels have been written during this revision.


## S4. Legal map and version boundary

The benchmark is explicitly scoped to the original July 2024 framework, not “the law today in August 2026”. This is an analytical scope correction that preserves the experiment; it does not assert that every annotator or model reasoned exclusively from that version. The original Act has 113 numbered articles, 13 chapters and 13 annexes. The later consolidated text contains additional provisions and an Annex XIV.

Sources: [original Act](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng); [27 July 2026 consolidation](https://eur-lex.europa.eu/eli/reg/2024/1689/2026-07-27/eng); [amending Regulation 2026/1744](https://eur-lex.europa.eu/eli/reg/2026/1744/oj). These describe the legal text, not a legal adjudication of the incidents.

| Chapter | Original articles | Subject |
| --- | --- | --- |
| I | 1–4 | Scope, definitions and general provisions |
| II | 5 | Prohibited practices |
| III | 6–49 | High-risk classification, requirements, operators and conformity |
| IV | 50 | Transparency duties for specified systems |
| V | 51–56 | General-purpose AI models and systemic risk |
| VI | 57–63 | Innovation, sandboxes and testing |
| VII | 64–70 | Governance and authorities |
| VIII | 71 | EU database |
| IX | 72–94 | Monitoring, market surveillance and enforcement |
| X | 95–96 | Codes of conduct and guidelines |
| XI | 97–98 | Delegated powers and committee procedure |
| XII | 99–101 | Penalties |
| XIII | 102–113 | Amendments, transitional and final provisions |

| Original annex | Subject |
| --- | --- |
| I | Product legislation for the high-risk product route |
| II | Offences relevant to an exception for remote biometric identification |
| III | Listed high-risk use cases |
| IV | Technical documentation for high-risk systems |
| V | EU declaration of conformity |
| VI | Conformity assessment based on internal control |
| VII | Quality-management and technical-documentation assessment |
| VIII | Registration information |
| IX | Information for real-world testing registration |
| X | EU large-scale IT systems |
| XI | General-purpose model technical documentation |
| XII | Information for downstream integration of general-purpose models |
| XIII | Criteria for general-purpose models with systemic risk |

Targeted amendment audit: the 2026 regulation changes the safety-component definition and adds Article 6(1a)–(1c) product-route qualifications; adds Article 5 prohibitions for specified non-consensual intimate material and child sexual-abuse material; moves machinery legislation within Annex I; adds Annex XIV; and changes application dates and some transparency provisions. These changes are potentially consequential for this dataset and are not silently incorporated into the old labels or prompts. An updated-law benchmark would require a new rubric version and case-level reassessment. In particular, “13 annexes” is qualified as a description of the original text.

The original Article 5 already covers use, not only placing a system on the market. [Commission guidance, section 2.7, paragraphs 39–40](https://digital-strategy.ec.europa.eu/en/library/commission-publishes-guidelines-prohibited-artificial-intelligence-ai-practices-defined-ai-act) applies the prohibitions to general-purpose systems and their deployers. Therefore the manuscript no longer justifies all fraud-related transparency labels by calling the perpetrator a user rather than a provider. Each potentially prohibited practice requires evidence for its elements. Whether the recorded reference labels survive that assessment remains an author legal-review task.

Article 6(1) requires both relevant product/safety conditions and the appropriate conformity-assessment condition; a fatal outcome, or the generic word “robot”, cannot resolve that test. Article 6(3) has a risk-of-harm condition and specified circumstances, with a profiling override. Article 50 may apply alongside higher categories. Other legal regimes, including consumer law and the DSA, can coexist with the AI Act. “Minimal” is not a declaration of lawfulness or absence of duties.


## S5. Metrics, denominators and paired inference

Six-label macro-F1 gives each reference category equal weight; an undefined class F1 is assigned zero. We report precision and recall per model and class in CSV, rather than hiding rare labels inside an aggregate. The majority-label baseline is defined descriptively from the observed reference sample; it is not trained on a separate development set. QWK assigns scores 0,1,2,3 to the four ordinal categories. There is no legally established equal distance between those categories.

For each bootstrap draw, n incidents are sampled with replacement, carrying their reference label and every model/prompt output together. The panel statistic is the unweighted mean across the fixed 14 models. Ordinal auxiliary or missing pairs are masked explicitly. A paired QWK difference uses a common mask within each model and each draw; hence the mean paired change differs from the difference of the separately available-case means. Missing predictions are nonmatches for nominal measures. The seed 20260916 and 10,000 draws retain the convention used in the earlier diagnostic audit. All intervals are percentile intervals; no confirmatory significance or winner claims are made from 14 comparisons.

Rare classes have only two records each. Bootstrap samples can omit such classes, making fixed-six-class macro-F1 intervals unstable and asymmetric. Treat them descriptively and inspect the underlying supports. The bootstrap does not measure reference-label correctness, inter-expert variation, the effect of repeated model calls, changes in provider snapshots or all event-family dependence.


### naive coverage and nominal results

| name | n | answered | auxiliary | n_ordinal | common_n | exact | macro_f1 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Gemini 3.7 Flash | 144 | 144 | 3 | 140 | 140 | 86.81% | 0.773 |
| Gemini 3 Flash | 144 | 142 | 1 | 138 | 138 | 82.64% | 0.539 |
| Gemma 3 27B | 144 | 144 | 0 | 140 | 140 | 68.75% | 0.289 |
| GPT-5.2 | 144 | 144 | 4 | 139 | 139 | 81.25% | 0.688 |
| GPT-5.6 Luna | 144 | 144 | 7 | 137 | 137 | 81.25% | 0.728 |
| GPT-5.6 Sol | 144 | 144 | 5 | 139 | 139 | 79.17% | 0.757 |
| Grok 4.6 | 144 | 144 | 5 | 139 | 139 | 79.17% | 0.741 |
| Claude Haiku 4.5 | 144 | 144 | 9 | 134 | 132 | 38.89% | 0.367 |
| Kimi K2.5 | 144 | 144 | 4 | 139 | 139 | 75.69% | 0.682 |
| Kimi K3 | 144 | 144 | 2 | 139 | 138 | 76.39% | 0.532 |
| Qwen 3.8 27B | 144 | 144 | 5 | 138 | 138 | 77.78% | 0.647 |
| Qwen 3.8 Max | 144 | 144 | 4 | 140 | 140 | 79.17% | 0.779 |
| Claude Sonnet 4.6 | 144 | 144 | 4 | 137 | 137 | 54.17% | 0.384 |
| Claude Sonnet 5 | 144 | 144 | 6 | 137 | 137 | 63.19% | 0.577 |

### decomposed coverage and nominal results

| name | n | answered | auxiliary | n_ordinal | common_n | exact | macro_f1 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Gemini 3.7 Flash | 144 | 144 | 2 | 140 | 140 | 89.58% | 0.686 |
| Gemini 3 Flash | 144 | 144 | 1 | 140 | 138 | 83.33% | 0.511 |
| Gemma 3 27B | 144 | 144 | 0 | 140 | 140 | 66.67% | 0.332 |
| GPT-5.2 | 144 | 144 | 1 | 140 | 139 | 77.78% | 0.569 |
| GPT-5.6 Luna | 144 | 144 | 2 | 139 | 137 | 72.22% | 0.527 |
| GPT-5.6 Sol | 144 | 144 | 3 | 140 | 139 | 72.92% | 0.749 |
| Grok 4.6 | 144 | 144 | 1 | 140 | 139 | 87.50% | 0.612 |
| Claude Haiku 4.5 | 144 | 144 | 4 | 138 | 132 | 75.69% | 0.516 |
| Kimi K2.5 | 144 | 144 | 2 | 140 | 139 | 87.50% | 0.656 |
| Kimi K3 | 144 | 144 | 2 | 139 | 138 | 74.31% | 0.583 |
| Qwen 3.8 27B | 144 | 144 | 3 | 140 | 138 | 85.42% | 0.787 |
| Qwen 3.8 Max | 144 | 144 | 3 | 140 | 140 | 85.42% | 0.786 |
| Claude Sonnet 4.6 | 144 | 144 | 1 | 140 | 137 | 76.39% | 0.511 |
| Claude Sonnet 5 | 144 | 144 | 2 | 140 | 137 | 78.47% | 0.623 |

### Paired QWK changes by model

| name | common_n | delta_qwk | delta_lo | delta_hi |
| --- | --- | --- | --- | --- |
| Gemini 3.7 Flash | 140 | 0.058 | -0.0918 | 0.2073 |
| Gemini 3 Flash | 138 | -0.0398 | -0.2679 | 0.1632 |
| Gemma 3 27B | 140 | 0.0309 | -0.1681 | 0.237 |
| GPT-5.2 | 139 | -0.1066 | -0.2922 | 0.0804 |
| GPT-5.6 Luna | 137 | -0.2685 | -0.4344 | -0.1153 |
| GPT-5.6 Sol | 139 | -0.1272 | -0.288 | 0.0327 |
| Grok 4.6 | 139 | 0.1879 | 0.0485 | 0.3363 |
| Claude Haiku 4.5 | 132 | 0.5656 | 0.3463 | 0.7793 |
| Kimi K2.5 | 139 | 0.1902 | -0.0335 | 0.4011 |
| Kimi K3 | 138 | -0.1303 | -0.3137 | 0.0494 |
| Qwen 3.8 27B | 138 | 0.0925 | -0.0961 | 0.2756 |
| Qwen 3.8 Max | 140 | 0.192 | 0.0184 | 0.362 |
| Claude Sonnet 4.6 | 137 | 0.1547 | -0.0707 | 0.3721 |
| Claude Sonnet 5 | 137 | 0.1584 | -0.0065 | 0.3218 |

## S6. Sensitivity analyses

The full 144-record analysis remains primary. All exclusions and alternative labels are specified in the companion CSVs. None creates independently validated reference labels.

| Analysis | n | Mean QWK B/S | Exact % B/S | Paired QWK change [95% CI] |
| --- | --- | --- | --- | --- |
| Full sample | 144 | 0.424/0.498 | 73.16/79.51 | 0.068 [-0.007, 0.143] |
| No extra-source cases | 130 | 0.379/0.469 | 71.70/79.45 | 0.083 [0.001, 0.166] |
| No driving family | 129 | 0.395/0.460 | 70.04/77.13 | 0.059 [-0.020, 0.137] |
| Eight documented earlier labels | 144 | 0.393/0.437 | 71.38/76.54 | 0.036 [-0.034, 0.107] |

Excluded extra-source IDs: S005, S006, S007, S008, S009, S010, S011, S013, S014, S015, S016, S018, S020, S021. Nine high, two minimal, one prohibited, one not-AI and one transparency record are removed; the remaining composition differs. This implements the exclusion option requested by reviewer 1, while the separate model-only evidence comparison is reported in S11.

Driving-family IDs: S008, S009, S016, S030, S037, S042, S050, S052, S062, S070, S071, S090, S138, S142, S146. All 15 recorded product-route cases are automated-driving reports. This is a family exclusion, not a claim that the other incidents are independent.

The historical-label analysis restores only the eight final labels explicitly logged as prohibited → transparency (S045, S076, S079, S083, S084, S089, S116, S137). Their primary labels remain untouched. The subset was selected from the pre-existing correction log, not from which relabelling improves a score. This sensitivity neither reclassifies every fraud nor asserts that the earlier labels are legally correct. The manuscript's unsupported general claim that changing the fraud interpretation “inverts the ranking” is removed.


### Direction conditional on reference category

| condition | group | incidents | pairs | up_pct | down_pct |
| --- | --- | --- | --- | --- | --- |
| naive | reference_minimal | 9 | 114 | 38.6 | 0.0 |
| naive | reference_transparency | 77 | 1069 | 24.42 | 6.83 |
| naive | reference_high | 44 | 615 | 4.55 | 3.58 |
| naive | reference_prohibited | 10 | 138 | 0.0 | 50.72 |
| decomposed | reference_minimal | 9 | 124 | 20.97 | 0.0 |
| decomposed | reference_transparency | 77 | 1076 | 16.26 | 1.86 |
| decomposed | reference_high | 44 | 616 | 3.73 | 6.98 |
| decomposed | reference_prohibited | 10 | 140 | 0.0 | 63.57 |
At the bottom category, only upward errors are possible; at the top, only downward errors are possible. These structural constraints and class mixtures prevent inferring a severity-reasoning mechanism from signed averages.


## S7. Confusions and recorded-rule analysis

Confusion cells count model–incident outputs; they are not independent incident counts. Row sums equal class support × 14 for each prompt, including missing outputs. Stored steps are compared literally, preserving not-applicable and unclear answers. Missing step fields count as nonmatches. The first differing recorded step is descriptive, not a reconstructed causal chain. A mismatch at one stage may propagate; totals across stages must not be added as independent errors.


### naive confusion matrix

| reference | __missing__ | high | insufficient_information | minimal | not_ai_system | prohibited | transparency |
| --- | --- | --- | --- | --- | --- | --- | --- |
| high | 0 | 565 | 0 | 9 | 1 | 28 | 13 |
| insufficient_information | 0 | 1 | 16 | 2 | 0 | 5 | 4 |
| minimal | 0 | 43 | 3 | 70 | 9 | 0 | 1 |
| not_ai_system | 0 | 6 | 0 | 0 | 21 | 0 | 1 |
| prohibited | 0 | 17 | 0 | 5 | 2 | 68 | 48 |
| transparency | 2 | 61 | 1 | 73 | 6 | 200 | 735 |

### decomposed confusion matrix

| reference | __missing__ | high | insufficient_information | minimal | not_ai_system | prohibited | transparency |
| --- | --- | --- | --- | --- | --- | --- | --- |
| high | 0 | 550 | 0 | 26 | 0 | 23 | 17 |
| insufficient_information | 0 | 1 | 4 | 4 | 0 | 2 | 17 |
| minimal | 0 | 20 | 1 | 98 | 1 | 1 | 5 |
| not_ai_system | 0 | 8 | 0 | 1 | 19 | 0 | 0 |
| prohibited | 0 | 22 | 0 | 5 | 0 | 51 | 62 |
| transparency | 0 | 49 | 2 | 20 | 0 | 126 | 881 |

### Step agreement by model (%)

| model | annex_i | annex_iii | art5 | art50 | derogation | profiling |
| --- | --- | --- | --- | --- | --- | --- |
| gemini37f | 97.9 | 93.1 | 90.3 | 95.1 | 93.1 | 87.5 |
| gemini3f | 95.1 | 75.0 | 89.6 | 85.4 | 88.2 | 83.3 |
| gemma27b | 74.3 | 70.8 | 68.8 | 84.7 | 76.4 | 47.2 |
| gpt52 | 97.2 | 86.1 | 73.6 | 93.1 | 91.0 | 88.9 |
| gpt56luna | 98.6 | 86.1 | 72.2 | 95.8 | 92.4 | 89.6 |
| gpt56sol | 98.6 | 93.8 | 73.6 | 97.9 | 91.0 | 91.0 |
| grok46 | 97.9 | 93.8 | 90.3 | 96.5 | 90.3 | 90.3 |
| haiku45 | 92.4 | 61.1 | 38.2 | 85.4 | 81.9 | 84.0 |
| kimi25 | 97.2 | 90.3 | 89.6 | 93.8 | 92.4 | 91.7 |
| kimi3 | 97.2 | 93.8 | 77.8 | 95.1 | 91.7 | 88.2 |
| qwen3827b | 97.9 | 89.6 | 84.7 | 98.6 | 91.7 | 86.1 |
| qwen38max | 98.6 | 93.1 | 76.4 | 97.9 | 93.8 | 91.7 |
| sonnet46 | 95.8 | 83.3 | 63.9 | 87.5 | 88.2 | 81.9 |
| sonnet5 | 95.1 | 81.9 | 83.3 | 94.4 | 91.0 | 82.6 |

### First recorded mismatch (six stored rule fields)

| model | annex_i | annex_iii | art5 | art50 | derogation | missing_step | none | profiling |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gemini37f | 2 | 7 | 14 | 2 | 0 | 0 | 112 | 7 |
| gemini3f | 4 | 27 | 14 | 7 | 0 | 2 | 88 | 2 |
| gemma27b | 30 | 11 | 45 | 0 | 2 | 0 | 47 | 9 |
| gpt52 | 2 | 14 | 38 | 6 | 1 | 0 | 80 | 3 |
| gpt56luna | 2 | 17 | 40 | 3 | 2 | 0 | 74 | 6 |
| gpt56sol | 2 | 7 | 38 | 1 | 4 | 0 | 90 | 2 |
| grok46 | 2 | 7 | 14 | 1 | 3 | 0 | 115 | 2 |
| haiku45 | 9 | 22 | 89 | 2 | 1 | 0 | 17 | 4 |
| kimi25 | 3 | 9 | 15 | 3 | 2 | 0 | 109 | 3 |
| kimi3 | 2 | 6 | 32 | 2 | 1 | 0 | 95 | 6 |
| qwen3827b | 2 | 10 | 22 | 1 | 1 | 0 | 101 | 7 |
| qwen38max | 2 | 7 | 34 | 1 | 1 | 0 | 96 | 3 |
| sonnet46 | 6 | 13 | 52 | 5 | 1 | 0 | 64 | 3 |
| sonnet5 | 5 | 16 | 24 | 3 | 1 | 0 | 84 | 11 |

The AI-system gate was not an independent annotation column. Gate-related examples are discussed through final not-AI labels and stored model answers; an inter-expert gate agreement statistic cannot be manufactured from them.


## S8. Paired case dossiers

The following purposive examples expand the original expert notes and compare all model outputs. These are revision diagnostics prepared with AI assistance, not a newly completed human coding study. Existing expert notes are quoted as stored and can contain tensions with subsequently corrected labels. “Author review required” means a substantive question is unresolved; the original reference data remain unchanged.


### S058: Product route and missing technical facts

**Stacking robot fatally crushes employee in South Korea** ([AIID](https://incidentdatabase.ai/cite/599)).

Input description: An industrial robot is reported to have crushed a man to death in South Korea when it failed to differentiate the man from the boxes of produce it was handling.

Reference: **minimal**; confidence 3/3; additional sources: no.

Stored expert note: A general industrial stacking robot is normally self-certifying; the record does not show a self-evolving AI safety function requiring third-party assessment.

Diagnostic assessment: The existing expert note assumes ordinary stacking machinery does not require the relevant third-party assessment. Some model rationales treat the hazardous machinery role as sufficient for high risk. The record does not itself establish conformity-assessment details; agreement with the supplied instruction cannot validate that assumption.

| model | decomposed | naive |
| --- | --- | --- |
| gemini37f | minimal | high |
| gemini3f | high | high |
| gemma27b | high | high |
| gpt52 | minimal | high |
| gpt56luna | minimal | not_ai_system |
| gpt56sol | minimal | high |
| grok46 | minimal | high |
| haiku45 | high | high |
| kimi25 | minimal | high |
| kimi3 | minimal | high |
| qwen3827b | minimal | high |
| qwen38max | minimal | high |
| sonnet46 | high | not_ai_system |
| sonnet5 | minimal | high |

Stored GPT-5.6 Sol naive rationale (illustrative, not selected as the definitive answer): “The robot’s AI-based differentiation of people from produce directly governed hazardous industrial machinery, making it a safety-related system covered by the Act’s high-risk framework.”

Stored GPT-5.6 Sol decomposed rationale (illustrative, not selected as the definitive answer): “The produce-stacking robot used inferential perception to distinguish people from boxes, but it was general industrial machinery rather than a normally third-party-assessed product or an Annex III employment system, and no prohibited practice or Article 50 function is indicated.”


### S011: Evidence threshold for prohibited scraping

**PimEyes's Facial Recognition AI Allegedly Lacked Safeguards to Prevent Itself from Being Abused** ([AIID](https://incidentdatabase.ai/cite/109)).

Input description: PimEyes offered its subscription-based AI service to anyone in the public to search for matching facial images across the internet, which critics said lacked public oversight and government rules to prevent itself from misuse such as stalking women.

Reference: **high**; confidence 3/3; additional sources: yes.

Stored expert note: The record shows facial search, but not the untargeted scraping needed to establish Article 5(1)(e).

Diagnostic assessment: The reference note says untargeted scraping is not established. Several model rationales infer it from internet facial-image search. The expert had consulted additional sources here; the original comparison is therefore evidence-asymmetric and this case is excluded from the 130-record analysis.

| model | decomposed | naive |
| --- | --- | --- |
| gemini37f | prohibited | prohibited |
| gemini3f | transparency | prohibited |
| gemma27b | high | high |
| gpt52 | prohibited | high |
| gpt56luna | high | prohibited |
| gpt56sol | prohibited | prohibited |
| grok46 | prohibited | prohibited |
| haiku45 | prohibited | high |
| kimi25 | prohibited | prohibited |
| kimi3 | prohibited | prohibited |
| qwen3827b | prohibited | prohibited |
| qwen38max | prohibited | prohibited |
| sonnet46 | high | high |
| sonnet5 | prohibited | prohibited |

Stored GPT-5.6 Sol naive rationale (illustrative, not selected as the definitive answer): “PimEyes uses facial recognition to match people against facial images gathered across the internet, constituting the prohibited creation or expansion of a facial-recognition database through untargeted scraping.”

Stored GPT-5.6 Sol decomposed rationale (illustrative, not selected as the definitive answer): “The facial-recognition service relied on untargeted internet facial-image collection to enable public matching searches, falling within the prohibition on creating or expanding facial-recognition databases through untargeted scraping.”


### S024: AI-system gate

**Dartmouth's Geisel School of Medicine Reportedly Used Canvas Activity Logs to Accuse Students of Cheating** ([AIID](https://incidentdatabase.ai/cite/302)).

Input description: Dartmouth's Geisel School of Medicine reportedly used Canvas learning-management activity logs and an internal analysis process to investigate remote-exam cheating during the 2020–2021 academic year. Seventeen medical students were charged after the school inferred that they accessed course materials during exams, but students and outside technical reviewers said automated Canvas activity may have been misread as intentional misconduct. Dartmouth later dropped the charges.

Reference: **not_ai_system**; confidence 2/3; additional sources: no.

Stored expert note: The record identifies Canvas activity logs and a human internal analysis, but no system that inferred an output; the students' intent was inferred by people.

Diagnostic assessment: The expert and some models read the record as activity logging plus human analysis. Others classify a high-risk educational system. The report must identify inferential system output before an AI Act category is assigned; the models did not all agree on that factual gate.

| model | decomposed | naive |
| --- | --- | --- |
| gemini37f | not_ai_system | not_ai_system |
| gemini3f | high | high |
| gemma27b | high | high |
| gpt52 | high | not_ai_system |
| gpt56luna | high | not_ai_system |
| gpt56sol | not_ai_system | not_ai_system |
| grok46 | high | not_ai_system |
| haiku45 | high | high |
| kimi25 | not_ai_system | not_ai_system |
| kimi3 | high | high |
| qwen3827b | not_ai_system | not_ai_system |
| qwen38max | not_ai_system | not_ai_system |
| sonnet46 | high | high |
| sonnet5 | not_ai_system | high |

Stored GPT-5.6 Sol naive rationale (illustrative, not selected as the definitive answer): “The incident describes the use and possible misinterpretation of activity logs and an internal analysis process, without identifying an AI system as defined by the EU AI Act.”

Stored GPT-5.6 Sol decomposed rationale (illustrative, not selected as the definitive answer): “The record describes deterministic Canvas activity logging followed by an internal or human analysis, without evidence that a system itself inferred cheating predictions, recommendations, or decisions from the logs.”


### S072: Insufficient evidence

**Cartels Reportedly Using AI to Expand Operations into Financial Fraud and Human Trafficking** ([AIID](https://incidentdatabase.ai/cite/725)).

Input description: The Jalisco New Generation Cartel is reportedly using AI to expand its financial fraud and human trafficking operations, coercing individuals into illegal activities under the guise of legitimate jobs. INTERPOL warns that this integration of AI into criminal enterprises is a growing trend among cartels across Europe, Asia, and Africa as well.

Reference: **insufficient_information**; confidence 1/3; additional sources: no.

Stored expert note: The row refers generally to cartels using AI but does not identify a concrete system, inferential function, or deployment context.

Diagnostic assessment: The original expert note says a concrete system and function are not identified. Some models nevertheless infer a prohibited or transparency use from a general account of criminal AI use. The basic rationale cannot show an unreported decision chain.

| model | decomposed | naive |
| --- | --- | --- |
| gemini37f | transparency | insufficient_information |
| gemini3f | transparency | prohibited |
| gemma27b | high | high |
| gpt52 | prohibited | minimal |
| gpt56luna | prohibited | insufficient_information |
| gpt56sol | insufficient_information | insufficient_information |
| grok46 | minimal | insufficient_information |
| haiku45 | insufficient_information | insufficient_information |
| kimi25 | transparency | prohibited |
| kimi3 | transparency | prohibited |
| qwen3827b | insufficient_information | prohibited |
| qwen38max | insufficient_information | insufficient_information |
| sonnet46 | minimal | prohibited |
| sonnet5 | minimal | insufficient_information |

Stored GPT-5.6 Sol naive rationale (illustrative, not selected as the definitive answer): “The record alleges generic use of AI by criminal organizations but does not identify a specific AI system or describe its functionality sufficiently to classify it under the Act.”

Stored GPT-5.6 Sol decomposed rationale (illustrative, not selected as the definitive answer): “The record states only that criminal groups use AI to support fraud and trafficking, without identifying the system’s function, intended purpose, product context, or outputs sufficiently to classify it.”


### S083: Interpretation and reference-note tension

**Romance Scammer 'Alla Morgan' Allegedly Exploits Deepfake Technology to Defraud Victim of £17,000** ([AIID](https://incidentdatabase.ai/cite/878)).

Input description: A scammer, or scammers, reportedly used AI-generated deepfake videos and documents to impersonate a fictitious person named "Alla Morgan," allegedly convincing a 77-year-old woman, Nikki MacLeod, to send £17,000 through various payment methods. The deepfakes were allegedly used in establishing credibility so as to enable fraud under the pretense of an online romantic relationship.

Reference: **transparency**; confidence 3/3; additional sources: no.

Stored expert note: The deepfake persona deliberately deceived a 77-year-old victim, exploiting age vulnerability and causing substantial financial harm.

Diagnostic assessment: The stored expert note itself describes deliberate deception, exploitation of age vulnerability and substantial financial harm. The later transparency label was propagated in the correction script. Article 5 can apply to deployer use of general-purpose systems; the author must specify the element not established, or revise the assessment with reasons. We do not assert that every prohibited output is an error.

| model | decomposed | naive |
| --- | --- | --- |
| gemini37f | transparency | transparency |
| gemini3f | transparency | transparency |
| gemma27b | prohibited | transparency |
| gpt52 | transparency | transparency |
| gpt56luna | prohibited | prohibited |
| gpt56sol | prohibited | prohibited |
| grok46 | transparency | transparency |
| haiku45 | transparency | prohibited |
| kimi25 | transparency | transparency |
| kimi3 | prohibited | prohibited |
| qwen3827b | prohibited | prohibited |
| qwen38max | transparency | prohibited |
| sonnet46 | transparency | prohibited |
| sonnet5 | prohibited | prohibited |

Stored GPT-5.6 Sol naive rationale (illustrative, not selected as the definitive answer): “The deepfake system used purposefully deceptive techniques to impersonate a fictitious person, materially distort the victim’s decisions, and cause significant financial harm.”

Stored GPT-5.6 Sol decomposed rationale (illustrative, not selected as the definitive answer): “The AI-generated deepfakes were deliberately deployed as deceptive impersonation techniques to impair the victim’s informed decision-making and induce financially harmful payments, while also generating synthetic content subject to Article 50 transparency duties.”


### S106: Interpretation and significant-harm threshold

**Preprints Reportedly from Researchers from Multiple Universities Allegedly Contain Covert AI Prompts** ([AIID](https://incidentdatabase.ai/cite/1135)).

Input description: Hidden prompts reportedly were discovered in at least 17 academic preprints on arXiv that purportedly instructed AI tools to deliver only positive peer reviews. The lead authors are reportedly affiliated with 14 institutions in eight countries, including Waseda University, KAIST, Peking University, and the University of Washington. The alleged concealed instructions, some of which were reportedly embedded using white text or tiny fonts, were purportedly intended to influence any reviewers who rely on AI tools.

Reference: **prohibited**; confidence 2/3; additional sources: no.

Stored expert note: Hidden prompts deliberately configured AI review tools to produce favourable assessments, a deceptive technique capable of materially distorting academic decisions.

Diagnostic assessment: The expert records hidden prompts as prohibited manipulation. Most models assign other categories. The author must explain whether the evidence establishes the required impairment and significant harm, rather than assuming that deceptive intent alone meets Article 5.

| model | decomposed | naive |
| --- | --- | --- |
| gemini37f | transparency | minimal |
| gemini3f | high | transparency |
| gemma27b | minimal | transparency |
| gpt52 | transparency | minimal |
| gpt56luna | transparency | not_ai_system |
| gpt56sol | transparency | minimal |
| grok46 | transparency | transparency |
| haiku45 | high | high |
| kimi25 | transparency | transparency |
| kimi3 | transparency | prohibited |
| qwen3827b | transparency | transparency |
| qwen38max | transparency | minimal |
| sonnet46 | high | not_ai_system |
| sonnet5 | transparency | minimal |

Stored GPT-5.6 Sol naive rationale (illustrative, not selected as the definitive answer): “The described use of large language models to assist academic peer review is identifiable AI use but does not fall within a prohibited or high-risk category or clearly trigger a specified transparency obligation under the EU AI Act.”

Stored GPT-5.6 Sol decomposed rationale (illustrative, not selected as the definitive answer): “The general-purpose language model generates text for peer review, is not shown to have been configured to manipulate reviewers, and academic manuscript review is outside Annex III, but its direct interaction and synthetic-text generation trigger Article 50 transparency duties.”


### S006: Agreement control with an unresolved factual gate

**Australian Automated Debt Assessment System Issued False Notices to Thousands** ([AIID](https://incidentdatabase.ai/cite/57)).

Input description: Australian Department of Human Services (DHS)’s automated debt assessment system issued false or incorrect debt notices to hundreds of thousands of people, resulting in years-long lawsuits and damages to welfare recipients.

Reference: **high**; confidence 3/3; additional sources: yes.

Stored expert note: No free-text note recorded.

Diagnostic assessment: All 28 outputs match the high reference label. This checks observed agreement only: the dataset description does not itself establish the technical inference mechanism, and a unanimous classification does not validate the AI-system gate. The expert consulted additional sources; new source-linked evidence is documented separately in S11 and the follow-up packet file, without claiming reconstruction of the historical consultation.

| model | decomposed | naive |
| --- | --- | --- |
| gemini37f | high | high |
| gemini3f | high | high |
| gemma27b | high | high |
| gpt52 | high | high |
| gpt56luna | high | high |
| gpt56sol | high | high |
| grok46 | high | high |
| haiku45 | high | high |
| kimi25 | high | high |
| kimi3 | high | high |
| qwen3827b | high | high |
| qwen38max | high | high |
| sonnet46 | high | high |
| sonnet5 | high | high |

Stored GPT-5.6 Sol naive rationale (illustrative, not selected as the definitive answer): “The automated system assessed alleged debts affecting welfare recipients, making it a high-risk system used by a public authority in connection with access to essential public benefits and services.”

Stored GPT-5.6 Sol decomposed rationale (illustrative, not selected as the definitive answer): “The system assessed welfare recipients’ economic circumstances and drove public-benefit debt-recovery decisions, placing it in Annex III essential services with no derogation and with profiling.”


## S9. Further author-led evaluation and codebook

`review/author_review_sample.csv` fixes a 20-incident review set: up to three greatest-disagreement incidents per reference class, plus one best-agreement remaining control when available, with ties broken by sample ID. For the two two-record auxiliary classes there is no remaining control. This is purposive error discovery using observed outputs, not a blinded or representative estimate of error prevalence. `author_review_outputs.csv` contains the original evidence and paired outputs for every selected case.

Codebook: GATE (AI-system identification); ART5 (prohibition elements); PRODUCT (product/safety/conformity route); PURPOSE (Annex III mapping); EXCEPTION (Art. 6(3)); PROFILING (override); TRANSPARENCY (Art. 50); EVIDENCE (unsupported inference or justified abstention); CONSISTENCY (contradiction between reported steps and final category); INTERPRETATION (defensible competing reading); REFERENCE_REVIEW (recorded reference or explanation needs reconsideration). A case can have one primary and additional secondary codes, but report denominators and avoid counting propagated effects as independent errors.

For each coded disagreement, quote only what the output actually says, cite the input fact and legal provision, and distinguish a factual omission from a disputed legal assessment. Do not infer hidden reasoning from a one-sentence basic rationale. Record the author's name/date, whether the reference is retained and reasons. The archived preparation pack began with all author-review cells pending. The guided working copy now records only explicit author replies; S12 records the three completed author confirmations and the scope of the remaining prepared material. No inter-annotator score or independent specialist replication is claimed.


## S10. Model identifiers and execution record

These are the requested model identifiers and earliest/latest positive-usage log timestamps for evaluation records, including retained and repeated attempts. They do not prove immutable provider snapshots or exact retention times. The historical harness did not pin providers or explicit sampling/reasoning settings; defaults may differ between models and dates.

| Model key | Requested OpenRouter ID | First logged UTC | Last logged UTC |
| --- | --- | --- | --- |
| sonnet46 | anthropic/claude-sonnet-4.6 | 2026-08-26T18:48:39+00:00 | 2026-08-29T06:56:04+00:00 |
| gpt52 | openai/gpt-5.2 | 2026-08-26T18:48:37+00:00 | 2026-08-29T06:23:19+00:00 |
| gemini3f | google/gemini-3-flash-preview | 2026-08-26T18:51:22+00:00 | 2026-08-28T20:32:10+00:00 |
| gemma27b | google/gemma-3-27b-it | 2026-08-26T18:48:36+00:00 | 2026-08-28T20:34:09+00:00 |
| kimi25 | moonshotai/kimi-k2.5 | 2026-08-26T18:51:59+00:00 | 2026-08-28T20:48:30+00:00 |
| haiku45 | anthropic/claude-haiku-4.5 | 2026-08-26T18:54:14+00:00 | 2026-08-29T06:57:42+00:00 |
| sonnet5 | anthropic/claude-sonnet-5 | 2026-08-26T18:55:13+00:00 | 2026-08-28T22:05:17+00:00 |
| gemini37f | google/gemini-3.7-flash | 2026-08-26T18:56:21+00:00 | 2026-08-29T06:14:27+00:00 |
| kimi3 | moonshotai/kimi-k3 | 2026-08-26T18:57:06+00:00 | 2026-08-28T22:59:51+00:00 |
| qwen38max | qwen/qwen3.8-max | 2026-08-26T18:58:48+00:00 | 2026-08-29T07:47:16+00:00 |
| qwen3827b | qwen/qwen3.8-27b | 2026-08-26T19:02:10+00:00 | 2026-08-29T07:31:52+00:00 |
| gpt56sol | openai/gpt-5.6-sol | 2026-08-26T19:06:00+00:00 | 2026-08-29T06:58:12+00:00 |
| gpt56luna | openai/gpt-5.6-luna | 2026-08-26T19:07:23+00:00 | 2026-08-29T06:57:45+00:00 |
| grok46 | x-ai/grok-4.6 | 2026-08-26T18:48:52+00:00 | 2026-08-29T07:02:32+00:00 |


The original Qwen3.8 Max alias was unavailable for the September follow-up. S11 explicitly uses the September replacement and fresh short-record and expanded-record calls under the same accessible snapshot. All other models also receive fresh baselines. No follow-up result is substituted into the original model panel.


## S11. Expanded-evidence follow-up, 22 September 2026

All **784 intended requests were attempted once**, with **750 valid category answers** and **34 unsuccessful or nonconforming answers**. Reported inference charges total **$4.893542**, including unsuccessful attempts. No original reference label or original retained model output was replaced. The original 144-case and 130-case analyses remain separate.

Each of the 14 pre-identified additional-source cases was given to all 14 current models under both original prompts and both short/expanded evidence conditions. Fresh short-record baselines control the contemporaneous evidence comparison. Thirteen requested canonical identifiers match the archived catalog; Qwen3.8 Max 0902 is an explicit replacement for the unavailable August version. Matching names do not prove immutable serving infrastructure.

The new factual packets were assembled with research-assistant support from accessible primary or attributable reporting, with source-access limits recorded per packet. They were frozen before new outputs and contain no expert label or legal-review note. They are not claimed to reproduce the exact sources the expert previously read. The historical expert reference has not been reassessed against the new packets. Greater agreement is therefore not independent evidence of greater legal correctness.

The original prompts, sampling/reasoning defaults and requested `max_tokens=4096` are retained; providers are pinned and fallback is disabled. Actual reasoning-token consumption differs between providers and sometimes exceeds that request parameter. This controls evidence and within-model request settings, not realised compute. Empty or truncated answers remain failures rather than being selectively regenerated. Scheduling and failed-answer handling are documented in `rerun/execution-methods.md`; no failed or successful call was repeated.

| Prompt | Common valid pairs | Changed labels | Paired agreement change, pp [95% CI] | All intended agreement change, pp [95% CI] | Paired six-label macro-F1 change | Paired QWK change |
| --- | --- | --- | --- | --- | --- | --- |
| Basic | 187 | 18/187 | 0.18 [-3.53, 3.85] | 0.51 [-4.08, 4.59] | 0.007 [-0.015, 0.031] | 0.062 [-0.006, 0.130] |
| Step-by-step | 179 | 26/179 | -8.95 [-15.48, -3.23] | -7.14 [-13.78, -1.02] | -0.072 [-0.085, -0.015] | -0.108 [-0.169, -0.039] |

Intervals use 10,000 shared incident resamples, seed 20260922. The fixed panel mean gives each model equal weight. Complete-case paired metrics explicitly identify their denominators; the intended-cell analysis treats every missing answer as a nonmatch. With one attempt per cell, repeated-call variability is not separately measured; intervals condition on the retained outputs and reference labels. Undefined QWK values and bootstrap-draw counts are retained in the machine-readable outputs. A panel QWK is undefined if any model in the fixed panel has an undefined value. No multiple-comparison winner or generalisation claim is made.

## Model-level comparison

| Model | Prompt | Valid short/expanded, each out of 14 | Exact agreement % short/expanded | Common pairs | Changed | Paired agreement change, pp [95% CI] |
| --- | --- | --- | --- | --- | --- | --- |
| gemini37f | naive | 14/14 | 92.9/92.9 | 14 | 0 | 0.00 [0.00, 0.00] |
| gemini3f | naive | 14/14 | 100.0/92.9 | 14 | 1 | -7.14 [-21.43, 0.00] |
| gemma27b | naive | 14/14 | 78.6/78.6 | 14 | 0 | 0.00 [0.00, 0.00] |
| gpt52 | naive | 14/14 | 100.0/85.7 | 14 | 2 | -14.29 [-35.71, 0.00] |
| gpt56luna | naive | 14/14 | 78.6/78.6 | 14 | 0 | 0.00 [0.00, 0.00] |
| gpt56sol | naive | 14/14 | 78.6/71.4 | 14 | 5 | -7.14 [-35.71, 21.43] |
| grok46 | naive | 14/14 | 78.6/71.4 | 14 | 3 | -7.14 [-28.57, 14.29] |
| haiku45 | naive | 14/14 | 78.6/78.6 | 14 | 0 | 0.00 [0.00, 0.00] |
| kimi25 | naive | 14/14 | 71.4/85.7 | 14 | 2 | 14.29 [0.00, 35.71] |
| kimi3 | naive | 13/13 | 78.6/85.7 | 13 | 1 | 7.69 [0.00, 25.00] |
| qwen3827b | naive | 13/14 | 71.4/78.6 | 13 | 2 | 0.00 [-23.08, 23.08] |
| qwen38max | naive | 11/11 | 71.4/71.4 | 10 | 0 | 0.00 [0.00, 0.00] |
| sonnet46 | naive | 14/14 | 92.9/100.0 | 14 | 1 | 7.14 [0.00, 21.43] |
| sonnet5 | naive | 12/12 | 71.4/78.6 | 11 | 1 | 9.09 [0.00, 30.00] |
| gemini37f | decomposed | 14/14 | 78.6/64.3 | 14 | 2 | -14.29 [-35.71, 0.00] |
| gemini3f | decomposed | 14/14 | 92.9/92.9 | 14 | 0 | 0.00 [0.00, 0.00] |
| gemma27b | decomposed | 14/14 | 92.9/85.7 | 14 | 1 | -7.14 [-21.43, 0.00] |
| gpt52 | decomposed | 13/14 | 78.6/71.4 | 13 | 2 | -15.38 [-38.46, 0.00] |
| gpt56luna | decomposed | 14/14 | 71.4/50.0 | 14 | 4 | -21.43 [-42.86, 0.00] |
| gpt56sol | decomposed | 14/14 | 78.6/57.1 | 14 | 3 | -21.43 [-42.86, 0.00] |
| grok46 | decomposed | 14/14 | 64.3/78.6 | 14 | 2 | 14.29 [0.00, 35.71] |
| haiku45 | decomposed | 13/14 | 78.6/64.3 | 13 | 4 | -23.08 [-46.15, 0.00] |
| kimi25 | decomposed | 14/14 | 85.7/71.4 | 14 | 4 | -14.29 [-42.86, 14.29] |
| kimi3 | decomposed | 11/13 | 71.4/71.4 | 11 | 0 | 0.00 [0.00, 0.00] |
| qwen3827b | decomposed | 13/13 | 78.6/64.3 | 13 | 3 | -15.38 [-38.46, 0.00] |
| qwen38max | decomposed | 10/10 | 71.4/64.3 | 8 | 0 | 0.00 [0.00, 0.00] |
| sonnet46 | decomposed | 14/14 | 100.0/92.9 | 14 | 1 | -7.14 [-21.43, 0.00] |
| sonnet5 | decomposed | 11/12 | 50.0/64.3 | 9 | 0 | 0.00 [0.00, 0.00] |

## All case changes

| Case | Historical expert label | Common model/prompt pairs, out of 28 | Changed labels | Toward reference | Away from reference |
| --- | --- | --- | --- | --- | --- |
| S005 | high | 24 | 4 | 0 | 2 |
| S006 | high | 28 | 6 | 1 | 5 |
| S007 | high | 26 | 5 | 1 | 4 |
| S008 | high | 27 | 1 | 0 | 0 |
| S009 | high | 27 | 0 | 0 | 0 |
| S010 | prohibited | 24 | 0 | 0 | 0 |
| S011 | high | 27 | 6 | 1 | 5 |
| S013 | high | 26 | 8 | 4 | 4 |
| S014 | not_ai_system | 28 | 0 | 0 | 0 |
| S015 | minimal | 26 | 5 | 3 | 2 |
| S016 | high | 26 | 0 | 0 | 0 |
| S018 | transparency | 27 | 1 | 1 | 0 |
| S020 | minimal | 24 | 2 | 1 | 1 |
| S021 | high | 26 | 6 | 0 | 6 |

Changes toward or away from the historical reference do not identify which interpretation is legally correct. The source-review file supplies the factual expansion and legal questions for every case. `classification_changes.csv` contains all paired labels; `confusions.csv` and `class_metrics.csv` preserve every class and denominator.

## Coverage and paid token usage

| Model | Attempts | Valid answers | Prompt tokens | Billed completion tokens | Reported reasoning tokens | Calls above 4096 billed completion tokens | Cost USD | Failures |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gemini37f | 56 | 56 | 73042 | 23950 | 18797 | 0 | 0.144594 | {} |
| gemini3f | 56 | 56 | 73042 | 5179 | 0 | 0 | 0.052058 | {} |
| gemma27b | 56 | 56 | 73644 | 5435 | 0 | 0 | 0.009851 | {} |
| gpt52 | 56 | 55 | 70526 | 15191 | 9933 | 0 | 0.261704 | {'invalid_json': 1} |
| gpt56luna | 56 | 56 | 70526 | 17671 | 12957 | 0 | 0.026092 | {} |
| gpt56sol | 56 | 56 | 70526 | 15025 | 10391 | 0 | 0.199115 | {} |
| grok46 | 56 | 56 | 82912 | 126047 | 120756 | 9 | 0.907706 | {} |
| haiku45 | 56 | 55 | 77496 | 8038 | 0 | 0 | 0.117686 | {'invalid_schema': 1} |
| kimi25 | 56 | 56 | 71150 | 144229 | 138880 | 6 | 0.433276 | {} |
| kimi3 | 56 | 50 | 70456 | 50152 | 44123 | 2 | 0.844762 | {'missing_content': 1, 'transport_TimeoutError': 1, 'provider_content_filter': 4} |
| qwen3827b | 56 | 53 | 75551 | 155684 | 150735 | 14 | 0.418412 | {'missing_content': 3} |
| qwen38max | 56 | 42 | 74659 | 117717 | 113980 | 0 | 0.758852 | {'missing_content': 12, 'transport_TimeoutError': 2} |
| sonnet46 | 56 | 56 | 77552 | 6719 | 0 | 0 | 0.333441 | {} |
| sonnet5 | 56 | 47 | 112162 | 16167 | 8945 | 0 | 0.385994 | {'invalid_json': 9} |

Failure types across all intended calls: invalid_json: 10, invalid_schema: 1, missing_content: 16, provider_content_filter: 4, transport_TimeoutError: 3. Provider content-filter refusals retain the original prompt and count as missing answers. No charge was observed for those refusals at the recorded verification time. Private account records are outside the public reproduction package.

Reasoning-token fields are provider-reported and may be incomplete; absent fields are not evidence of no internal reasoning. Two transport timeouts retain missing category answers; their charges and native token counts were recovered through a read-only generation-metadata lookup. Another timeout had no observed charge or matching generation record at the recorded checks; its token usage is unavailable. Reported charges reflect those observations and do not establish that a later charge was impossible. Original response and ledger files are retained privately; public reproduction uses the parsed cells and cannot independently authenticate provider charges. A completed HTTP response is not automatically a valid category answer. The frozen request hash is `ec8f5dafda1c3feefa15b1b37c35db2c4f680867310c03dfe8ab56f9044cdb0a`; the response ledger hash used for this analysis is `226fbcc5c2030cc6d09993b065ecfd1e5144e2a03f758870df4597fba17d2958`.


## S12. Post-run case review and decision authority

The audit was conducted after the model runs. AI assisted with selecting and preparing review cases, including summaries and draft recommendations. The author made the recorded legal judgments. These must be distinguished from the earlier annotation revisions, which the author states preceded his inspection of model answers.

The fixed diagnostic sample contains 20 cases. The author explicitly confirmed the presented summaries and reasons for S014 and S024 as not-AI, and S140 as insufficient information. These are three retained original labels, not an exhaustive human evaluation of every model explanation. The original sample selection remains fixed; S083 was separately flagged, and later consistency checks do not redefine that sample.

All 144 records now have prepared review material. Suggested changes in that material are AI-generated proposals for the author's final judgment. They have not been adopted as research labels, do not change the original expert reference, and are not used for any results reported in this paper. The author's direction to finish the preparation is not recorded as approval of individual suggestions. No second specialist annotation, inter-annotator agreement or complete human error coding is claimed.

The original reference remains the first author's legal assessment under the archived rubric and available evidence. The three post-run confirmations support the stated case interpretations only. They do not independently validate the reference or establish broad model legal accuracy.

| Case | Recorded author judgment | Reason accepted by the author |
|---|---|---|
| S014 | Retain not-AI | The record specifies simple keyword lists; contrary categorisation skips the AI-definition gate. |
| S024 | Retain not-AI | The described process combines activity logs with human inference; an AI component is not identified. |
| S140 | Retain insufficient information | Citation errors suggest possible AI use, but the system and extent of involvement are expressly unconfirmed. |

The supplied companion preserves the fixed sample, archived explanations and recorded three-case status. Private draft recommendations and exploratory AI-reference calculations are kept in a separate author-review package. They are not part of the submission's evidential reference.

## S13. Additional checks on the archived evaluation

These post-hoc analyses keep the original labels and model answers. They exclude the 42 records bearing the legacy development designation, then additionally exclude records for which the expert consulted extra sources. The remaining split is not a newly established untouched test set: rubric development and annotation history remain as described in S3. No additional model calls were made.

Each interval uses 10,000 shared incident resamples (seed 20260916), keeping the fixed model panel and prompt pairs together. Macro-F1 always uses the same six classes, with zero for an undefined class F1. QWK differences use common scorable records.

| Sample | n | Exact agreement B/S | Paired change, pp [95% interval] | Macro-F1 B/S | Paired F1 change [95% interval] | Paired QWK change [95% interval] |
|---|---:|---|---|---|---|---|
| full144 | 144 | 73.16/79.51 | 6.35 [2.93, 9.87] | 0.606/0.604 | -0.002 [-0.079, 0.081] | 0.068 [-0.007, 0.143] |
| legacy_heldout102 | 102 | 74.02/79.34 | 5.32 [1.47, 9.31] | 0.646/0.639 | -0.007 [-0.080, 0.075] | 0.074 [-0.017, 0.167] |
| legacy_heldout_same_record | 88 | 72.00/79.22 | 7.22 [3.00, 11.53] | 0.482/0.480 | -0.002 [-0.069, 0.092] | 0.097 [-0.015, 0.207] |
| excluding_intimate_material | 138 | 73.08/78.83 | 5.75 [2.28, 9.32] | 0.607/0.602 | -0.005 [-0.082, 0.082] | 0.061 [-0.015, 0.137] |
| excluding_version_sensitive_flags | 118 | 71.85/76.51 | 4.66 [0.97, 8.29] | 0.628/0.589 | -0.039 [-0.105, 0.047] | 0.026 [-0.047, 0.097] |
| excluding_flagged_transparency_fraud | 122 | 77.34/81.91 | 4.57 [0.94, 8.43] | 0.641/0.626 | -0.015 [-0.090, 0.072] | 0.040 [-0.041, 0.124] |

The saved JSON includes every subset ID and class count. Separate contingency-matrix implementations reproduced all model-level F1 and QWK point estimates. The full-sample results and intervals match the earlier analysis exactly. The sensitivities describe this archive and do not repair the prompt, legal-version or single-reference limitations.

### Legal-version diagnostic

The intimate-material flag covers six records: S035, S063, S064, S076, S077, S149. The broader flag also covers 20 product-related records: S001, S008, S009, S016, S029, S030, S037, S040, S042, S050, S052, S058, S062, S070, S071, S090, S110, S138, S142, S146. These include all 15 historical product-positive automated-driving records and five records concerning industrial robots, hotel robots, a crash-detection device or a medical model. The flag is deliberately broad; it does not assert that an amended provision changes every label. S033 (identifying abuse victims) and S061 (a later assault following facial misidentification) are not synthetic-intimate-material cases.

The flags were selected from record content and statutory subject matter after the original study. The amended text adds intimate-material provisions and changes the safety-component/product framework. The new intimate-material prohibitions apply from 2 December 2026, distinct from the amendment’s entry into force. Since the historical checklist instructed models to ignore temporal scope while also saying “today”, neither subset becomes a controlled comparison of legal versions. The screen is not an exhaustive audit of every amendment. No relabelling or attribution of individual disagreements to legal-version choice is claimed.

Source: [Regulation (EU) 2026/1744, Article 1(4), (7), (40) and (41)](https://eur-lex.europa.eu/eli/reg/2026/1744/oj), checked 22 September 2026.

### Related reference-family check

A separate, reproducible screen excludes all 22 historically transparency-labelled records whose original title or description contains scam, fraud or phish (case-insensitive): S045, S078, S083, S084, S085, S086, S087, S088, S091, S102, S103, S104, S108, S113, S114, S115, S116, S118, S121, S122, S135, S137. This broad check tests whether the exact-agreement result depends entirely on that reference family. It is not a corrected-label score or a finding that every excluded case is prohibited. It includes some cases, such as manipulation of software rather than a person, that may remain transparency. It can miss related cases without these words and does not replace an element-by-element legal review.


## S14. Rule agreement by reference value

These descriptive checklist comparisons use the historical six rule fields. They are literal field matches, not independent judgments of legal correctness. Each incident contributes fourteen model answers; therefore the pairs are not independent observations. Negatives, unclear, missing and not-applicable values are shown separately. No basic-prompt rule answers are inferred from its short explanations.

| Rule | Reference value | Incidents | Matched / model–incident pairs | Agreement |
|---|---|---:|---:|---:|
| annex_i | no | 126 | 1705 / 1764 | 96.7% |
| annex_i | unclear | 3 | 7 / 42 | 16.7% |
| annex_i | yes | 15 | 209 / 210 | 99.5% |
| annex_iii | biometrics | 13 | 111 / 182 | 61.0% |
| annex_iii | education | 1 | 14 / 14 | 100.0% |
| annex_iii | employment | 2 | 28 / 28 | 100.0% |
| annex_iii | essential_services | 6 | 82 / 84 | 97.6% |
| annex_iii | justice_democracy | 1 | 12 / 14 | 85.7% |
| annex_iii | law_enforcement | 3 | 28 / 42 | 66.7% |
| annex_iii | migration | 7 | 76 / 98 | 77.6% |
| annex_iii | none | 109 | 1365 / 1526 | 89.4% |
| annex_iii | unclear | 2 | 0 / 28 | 0.0% |
| art5 | no | 129 | 1481 / 1806 | 82.0% |
| art5 | unclear | 5 | 12 / 70 | 17.1% |
| art5 | yes | 10 | 51 / 140 | 36.4% |
| art50 | no | 55 | 687 / 770 | 89.2% |
| art50 | unclear | 2 | 5 / 28 | 17.9% |
| art50 | yes | 87 | 1182 / 1218 | 97.0% |
| derogation | applies | 1 | 2 / 14 | 14.3% |
| derogation | does_not_apply | 29 | 320 / 406 | 78.8% |
| derogation | not_applicable | 112 | 1482 / 1568 | 94.5% |
| derogation | unclear | 2 | 0 / 28 | 0.0% |
| profiling | no | 14 | 101 / 196 | 51.5% |
| profiling | not_applicable | 113 | 1428 / 1582 | 90.3% |
| profiling | unclear | 2 | 0 / 28 | 0.0% |
| profiling | yes | 15 | 176 / 210 | 83.8% |

All 15 positive product-route records belong to the automated-driving family. High agreement on the full product question therefore does not demonstrate broad positive-route coverage. `results/rule-value-confusions.csv` includes every observed reference/predicted-value combination.


## S15. Audit of the executed legal instructions

The basic and checklist prompts in `inputs/` are the exact archived instructions. They have not been silently corrected. The table below identifies limits in those instructions. It is an assistant-prepared comparison with primary legal sources, not a second specialist's validation. A result favouring the checklist measures agreement with the historical reference under the complete prompt package; it does not establish that each instruction is legally sound.

| Topic | Executed instruction or assumption | Consequence for interpretation |
|---|---|---|
| Scope and date | The rubric/checklist posit EU placement or use and disregard territorial/temporal scope; the basic prompt does not repeat that framing. The rubric says August 2026 and the checklist says “today”, without freezing a statutory version. | Differences can reflect framing or legal version as well as rule use. The revision interprets an archived taxonomy; it does not establish uniform historical-law or current-law accuracy. |
| Article 5(1)(a) | The checklist requires evidence that the system was trained or configured to use a technique and labels some emergent manipulation unclear. | The statute does not impose a universal trained/configured prerequisite. Assess the technique, impairment of informed decision-making, material behavioural distortion, causation and significant harm or its reasonable likelihood. Intent to harm is not required. General-purpose use is not an exemption. |
| Article 5(1)(b) | Its summary discusses exploitation without direct harm but omits the material-distortion and significant-harm thresholds. | Actual injury is unnecessary, but benefit to an operator or vulnerability alone is insufficient. The full prohibition requires the statutory causal and harm conditions. |
| Article 5(1)(e) | The checklist summarises untargeted facial-image scraping without fully specifying the regulated acts. | The test includes use of a qualifying system, not only personal scraping by the incident deployer. The record must still establish the relevant database-building facts. |
| Article 5(1)(h) | Its short suspect-search exception gives a four-year penalty threshold without naming Annex II and all authorisation safeguards. | This is not a complete legal test for the exception. A serious offence alone does not establish lawful real-time remote biometric identification. |
| Article 6(1) | Product-type rules of thumb stand in for facts about the actual product, safety function and conformity-assessment route. | These are rubric assumptions. Where decisive technical facts are absent, a minimal/high decision is conditional and must not be presented as settled product classification. |
| Article 6(3) | The checklist lists the four limited-role routes but does not fully state the overarching absence-of-significant-risk condition. | A listed role alone is not a complete derogation analysis. Profiling prevents this derogation. |
| Election purpose | A same-actor development/deployment rule is used to distinguish election-specific systems from general-purpose tools. | Producing media does not itself prove development of an AI system. Identify the system's intended purpose and any purpose-changing deployment; apply Annex III 8(b) to the actual facts. |
| Sector overlap | The prompt assigns moderation to the DSA and recommendation to consumer law. | Other legislation does not displace the AI Act. Such functions are not automatically Annex III uses, but a concrete system can independently meet an Article 5, 6 or 50 condition. |
| Article 50 | The instruction uses broad interaction/generation/biometric flags. | These are summary fields, not a full duty-and-exception assessment. Separate provider marking/detectability from deployer disclosure, and identify the system and relevant operator. |
| Abstention | The basic prompt restricts insufficient-information answers to an unidentified system; the checklist uses a broader function/context threshold. | Auxiliary-answer rates and downstream scores can change because the permitted abstention rule changes. Neither prompt comparison isolates reasoning alone. |

The amendment-sensitive exclusions in S13 and the original 130-case evidence exclusion address different questions. Neither repairs the wording used in completed calls. Corrected instructions would constitute a new experimental condition. The archive therefore preserves the executed instructions, with this audit alongside them.

Primary sources checked on 22 September 2026: [original Regulation (EU) 2024/1689, Articles 2–6, 50 and Annexes II–III](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng); [Regulation (EU) 2026/1744](https://eur-lex.europa.eu/eli/reg/2026/1744/oj); [Commission guidelines C(2025) 5052 final, especially sections 2.7 and 3.2](https://ai-act-service-desk.ec.europa.eu/sites/default/files/2025-08/guidelines_on_prohibited_artificial_intelligence_practices_established_by_regulation_eu_20241689_ai_act_english_ied3r5nwo50xggpcfmwckm3nuc_112367-1.PDF). The guidelines assist interpretation and are not binding judicial determinations.


### Model-panel heterogeneity

Exact agreement rises for 9 models and falls for 5. The median gain is 4.51 percentage points. Claude Haiku 4.5 contributes 41.4% of the sum of model gains, with its own gain of 36.81 points. Leaving out one model at a time gives panel mean gains from 4.01 to 7.53 points. All fourteen models remain in the main result; these are descriptive checks, not model-population inference. See `results/model-gain-heterogeneity.json`.

### Follow-up packet size

The fourteen added factual passages range from 114 to 435 characters, with median 362, excluding their source URLs and the unchanged original record. The passages were chosen to clarify the system's function, deployment or incident circumstances from accessible primary or attributable reporting, with access failures recorded. Selection was not a systematic review of every linked article. Exact expanded inputs, sources, frozen request bodies and provider settings are supplied in `rerun/followup/packets.json`, `requests.jsonl` and `model-bindings.json`. Historical label/note fields in the preparation file were not sent to models; the request bodies show the actual evidence they received.

