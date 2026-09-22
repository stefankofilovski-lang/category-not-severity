# Execution of the expanded-evidence follow-up

The 22 September 2026 follow-up attempted each of its 784 frozen requests once. There were 750 valid category answers and 34 unsuccessful or nonconforming answers. The archived request bodies, evidence packets, model bindings and historical reference were unchanged during execution.

## Scheduling

The first 24 requests used batches of four workers. Subsequent requests used up to eight concurrent workers, refilling a slot when a request finished. All 56 requests for an incident finished before the next incident began. This scheduling change did not alter request bodies, endpoints, sampling defaults, requested output limits or the analysis plan.

The requested completion limit was 4,096 tokens. Provider-reported reasoning and completion usage sometimes exceeded that value. The experiment holds evidence and within-model request settings constant; it does not establish equal realised computational effort across models.

## Failed answers and reported usage

The 34 unsuccessful answers comprise 10 invalid-JSON responses, one invalid-schema response, 16 missing-content responses, four provider content-filter refusals and three transport timeouts. No failed or successful call was repeated. Missing answers remain explicit in `../results/followup/cells.csv` and in the reported denominators.

Two transport timeouts have provider-reported charges and token counts recovered from generation metadata, but no recovered category answer. The third has no observed charge or matching generation record at the recorded checks; its token usage is unavailable. Content-filter refusals retain the original requests and remain missing answers.

## Reproduction boundary

The public companion reproduces the numerical results from the published parsed labels, prompts, reference and metadata. Raw response envelopes and private account records are not distributed. Consequently, this companion does not independently repeat raw-response parsing or authenticate provider charges. Supplement S11 reports the completion counts, usage limitations and results.
