# Legal Categories from Incident Reports

Replication materials for **Legal Categories from Incident Reports: Evaluating 14 LLMs under the EU AI Act**, by Stefan Kofilovski and Georgi Trajkov, SiKDD / Information Society 2026, submission 109.

## Revised paper and companion

The revised four-page paper was resubmitted to EasyChair as version 3 on 23 September 2026. The paper and companion are in [`revision-2026-09-23/`](revision-2026-09-23/). Final conference acceptance remains a decision for the chairs.

- [Four-page paper](revision-2026-09-23/revision/paper/sikdd2026-revised.pdf)
- [Supplement, S1–S15](revision-2026-09-23/revision/supplement.md)
- [Response to reviewers](revision-2026-09-23/revision/review/response-to-reviewers.md)
- [Reproduction instructions and file manifest](revision-2026-09-23/README.md)

The paper compares 14 models with one lawyer's legal assessments of 144 AI incident records under two prompts. Exact agreement increases from 73.2% to 79.5%; the paired gain is 6.35 percentage points with a 95% incident-bootstrap interval of 2.93–9.87. Macro-F1 is almost unchanged. The paired QWK interval includes zero. These are agreement results, not independent validation of legal accuracy.

The separate 14-case evidence follow-up attempted 784 calls: 750 valid answers and 34 failures. Its short and expanded inputs, model/provider settings, parsed results and uncertainty calculations are included. No repeated-call variability or second-specialist annotation is claimed.

## Provenance

The original files at the repository root are preserved. They document the executed prompts, rubric, labels, corrections and model outputs, including limitations identified during revision. The earlier README's claim that the rubric never changed during annotation is superseded: the correction log records 19 field changes across ten incidents. The author states that these changes preceded his inspection of model answers. Six development examples are excluded from the 144-record evaluation.

The later audit took place after the model runs. AI selected and prepared cases; the author made the three recorded case judgments. Draft AI recommendations did not replace the expert labels or generate the paper's reported results. Independent specialist validation remains unperformed. The study interprets results against the July 2024 framework; the executed prompts did not uniformly fix a legal version.

## Reproduce the revised results

Use the requirements and commands in the [companion README](revision-2026-09-23/README.md). Numerical reproduction uses archived inputs and predictions, makes no new model calls and requires no API credentials. The original root scripts are retained as historical research material; use the revision's scripts for its reported calculations.

## Licence

Rubric, prompts and labels: CC BY 4.0. Analysis scripts: MIT. See [LICENSE](LICENSE). Incident text and metadata originate from the AI Incident Database and remain subject to its terms.

## Citation

Stefan Kofilovski and Georgi Trajkov. 2026. Legal Categories from Incident Reports: Evaluating 14 LLMs under the EU AI Act. Information Society 2026, SiKDD, Ljubljana. DOI: [10.70314/is.2026.sikdd.109](https://doi.org/10.70314/is.2026.sikdd.109).
