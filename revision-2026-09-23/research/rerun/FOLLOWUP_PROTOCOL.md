# Expanded-evidence follow-up protocol

Scientific design recorded before the 22 September 2026 model runs. This public description retains the research design and reporting rules; administrative instructions are omitted. Exact model request bodies, evidence packets and model bindings are distributed separately without changes.

## Question and scope

Do current instances of the 14-model panel change their classifications when the 14 pre-identified unequal-evidence cases are supplied with additional, source-linked facts? This is a small exploratory follow-up. It cannot independently validate the author's legal reference or recover the exact historical information available to him.

The original 144-case experiment, original prompts, original expert reference and 130-case exclusion analysis remain intact. New results must be reported separately. Newly assembled factual paraphrases are not described as the author's original full sources. They contain no reference labels, legal annotations, AIID taxonomy classifications or model outputs. Source-access limitations are recorded for each packet.

## Frozen design

- The case set is the exact 14 cases recorded as receiving additional-source consultation in the historical reference. It is not chosen using new predictions.
- Each case receives both historical prompts and both evidence conditions (original short record and short record plus factual expansion) for every model: 14 × 14 × 2 × 2 = 784 intended calls.
- A fresh short-record baseline is included for all models. Thirteen current catalog canonical identifiers match the archived identifiers. Qwen3.8 Max 0902 replaces the unavailable August version and is explicitly a different snapshot. No new result is substituted into the original 144-case table.
- Endpoint, quantization where disclosed, price ceilings, canonical identifier, exact requests and source packets are frozen and hashed. Within each model, endpoint and request settings are identical across evidence conditions. Provider fallbacks are disabled.
- Standard service endpoints are selected, favouring the model developer where available. For Kimi K2.5 and Gemma 3 the pinned endpoints are Novita and Novita/bf16 respectively. Kimi K3's first-party endpoint declares mxfp4 quantization; this is disclosed rather than assuming full precision.
- The original system prompts and 4,096-token completion limit are retained, including historical rubric limitations. Sampling and reasoning settings use the selected endpoint's defaults. This compares two information conditions under the historical rubric; it is not an updated-law experiment.
- Incident and request order use the recorded fixed seed. Each incident's 56 cells are scheduled before the next incident.
- One attempt is retained per intended cell. Refusals, malformed outputs, truncation and transport failures remain visible. There is no selective retry based on correctness and no silent model/provider substitution. Any separately authorized retry must be reported as a new attempt.

## Reference and reporting

The historical expert labels are frozen before the follow-up, but have not been reassessed against these new packets. Report **agreement with the historical expert reference**, not measured legal accuracy. Class changes themselves do not establish corrections. Source packets remain marked as prepared by the research assistant and not author-verified. Any later expert reassessment requires a dated, separately versioned label file and disclosure of whether new predictions had been seen.

Report completion and parsing coverage, all six-label confusion counts, class support, exact agreement, macro-F1 and the direction of within-model changes. Compute paired differences only on explicitly identified common completed cells; additionally count missing intended answers as nonmatches. Bootstrap the 14 incidents as clusters while retaining all models and conditions together. With only 14 purposively identified cases, intervals are exploratory and cannot support general claims about all incidents. QWK is secondary and may be undefined for degenerate subsets; report undefined values and denominators rather than replacing them with zero.

## Execution record

All 784 intended requests were attempted once. There were 750 valid category answers and 34 unsuccessful or nonconforming answers. See `execution-methods.md` for scheduling changes and failed-answer handling, and `../results/followup/cells.csv` for the complete parsed result set. The preparation record alone is not evidence of completed execution.
