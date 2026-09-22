# Expanded-evidence follow-up

The 22 September 2026 experiment attempted all 784 intended calls once: 750 valid category answers and 34 unsuccessful or nonconforming answers. Reported inference charges total $4.893542, including unsuccessful attempts. Charge estimates and their verification limits are described in Supplement S11 and `execution-methods.md`.

This separate comparison gives each current model short and expanded evidence on the 14 pre-identified cases. It does not replace the original 144-case results. The historical expert reference remains unchanged and has not been reassessed against the new factual packets.

## Published files

- `followup/requests.jsonl`: the 784 exact frozen requests.
- `followup/packets.json`: incident records and source-linked factual expansions.
- `followup/model-bindings.json`: model and provider settings.
- `followup/manifest.json`: public research metadata, original input hashes and a separately identified execution summary.
- `followup/source-review.md`: source-access notes and evidence limitations.
- `audit/model-availability.json` and `audit/model-comparison.json`: the model-identifier and endpoint comparisons.
- `../results/followup/`: all parsed cells, denominators, class scores, confusions, paired changes and uncertainty estimates.
- `execution-methods.md`: scheduling and failed-answer handling.

## Reproduce the reported statistics

From the companion root (`revision-2026-09-23/`), run:

```text
python revision/analysis/verify_companion.py .
```

This verifies the file manifest and recomputes the original and follow-up statistics from published parsed labels. It makes no network requests or paid model calls. Package requirements and the remaining analysis commands are in the companion README. Raw provider-response envelopes and private account records are not part of this public package.

## Scope

Every model receives a fresh short-record baseline and the expanded record under both original prompts. Qwen3.8 Max 0902 explicitly replaces the unavailable August version. The other 13 canonical identifiers match the archive, without guaranteeing immutable serving infrastructure. Provider fallback is disabled. Sampling and reasoning use the pinned endpoint's defaults; the requested 4,096-token limit did not uniformly cap reported reasoning and completion usage. No failed or successful call was repeated.

The factual expansions were assembled on 22 September and are not claimed to reconstruct the exact pages the author originally consulted. They have not undergone a new author verification or reference-label reassessment. The selected 14-case set cannot establish general legal reliability.
