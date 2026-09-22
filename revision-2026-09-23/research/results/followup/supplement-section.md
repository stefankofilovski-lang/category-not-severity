# S11. Expanded-evidence follow-up, 22 September 2026

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
