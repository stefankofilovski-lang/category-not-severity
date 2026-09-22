# Paper 109: revised manuscript and replication companion

The four-page revision was resubmitted to EasyChair as paper 109, version 3, on 23 September 2026. This directory contains the paper and its research companion; the conference chairs determine final acceptance. The paper retains the original expert reference. The audit followed the model runs: AI selected and prepared cases, while the author made the three recorded case judgments. No AI-derived reference replaces the expert labels in the reported results.

## Contents

- `revision/paper/sikdd2026-revised.pdf`: current four-page manuscript.
- `revision/supplement.md`: S1–S15, including original results and new diagnostics.
- `revision/review/response-to-reviewers.md`: current response, distinguishing completed work and unmet independent validation.
- `research/inputs/`: original submitted v2, both executed prompts, rubric, labels, corrections, original model answers and sampling sources.
- `research/results/`: preserved numerical results, including all 784 follow-up cells and failure statuses.
- `research/rerun/followup/`: exact frozen requests, added evidence, source notes and provider/model settings. Its public manifest distinguishes the pre-run preparation record from the completed execution.
- `research/rerun/execution-methods.md`: scheduling, failed-answer handling and the boundary of public reproduction.
- `revision/results/`: held-out, legal-version and fraud-family sensitivities; per-value rule support; model-gain heterogeneity.
- `MANIFEST.sha256.json`: hashes of every included file other than the manifest itself.

Original-research relative paths in S1–S11 resolve under `research/`. New S13–S15 result paths resolve under `revision/`. S12 records the three author confirmations and the boundary between preparation and research decisions. The detailed confirmation record is `revision/review/guided-author-review.md`; the archived `research/review/` sample represents its earlier preparation state. The current paper and response are only under `revision/`.

## Offline reproduction

Use Python 3.12 and the versions in `requirements.txt`. Installing packages needs network access; the commands below make no network requests and require no credentials. Work on a copy if you want to preserve the extracted file hashes after regeneration.

From the extracted archive root:

```text
python revision/analysis/verify_companion.py .
python revision/analysis/additional_sensitivity.py
```

The first command verifies the manifest, recomputes the original 28 exact/F1/QWK combinations with contingency matrices, and reproduces follow-up panel/paired estimates and bootstrap intervals from the parsed labels. The second recomputes all added diagnostics using the archived data; its output is saved under `revision/`.

To regenerate the original tables, figure, confusion matrices and paired bootstrap results:

```text
python research/analysis/revise_analysis.py
```

That script writes under `research/`. To regenerate only the current figure's clearer labels:

```text
python revision/analysis/refresh_figure.py
```

Build the current paper from `revision/paper/` with a working LaTeX installation: pdflatex, biber, pdflatex twice. No font-size overrides are required.

## Provenance and privacy boundary

Research inputs, historical numerical outputs, frozen request bodies, evidence packets and model bindings retain their original bytes. The public follow-up manifest omits administrative spending controls and adds an explicit execution summary; it is not presented as the original pre-run file. Later diagnostics do not replace the archived reference or imply new model calls. The fourteen-case follow-up used one attempt per cell, with 750 valid answers and 34 failures.

Personal correspondence, internal working instructions, administrative records, credentials and raw provider-response envelopes are excluded. Numerical reproduction uses parsed cell labels. This companion cannot independently repeat raw-response parsing or authenticate provider charges; `research/rerun/execution-methods.md` explains that boundary.

The historical model explanations and public incident evidence are research data. Proposed new legal judgments are provided separately to the author and are not silently included as accepted annotations. Independent specialist validation, controlled model legal-version choice and repeated-call uncertainty remain unperformed.
