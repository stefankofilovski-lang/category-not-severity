# Category, Not Severity — replication materials

Materials for *Category, Not Severity: How Large Language Models Misclassify AI
Incidents Under the EU AI Act Risk Taxonomy* (SiKDD 2026, Information Society
multiconference, Ljubljana).

## What this is

144 incidents from the AI Incident Database, classified under the EU AI Act risk
taxonomy by a lawyer working from a written rubric, and by 14 large language models
under two prompts (basic and step-by-step). The paper reports where the models and the expert disagree, and in
which direction.

## Files

| file | contents |
|---|---|
| `rubric.md` | The annotation rubric. Frozen 26 August 2026, before any incident was labelled, and not revised afterwards. The interpretive positions in it are the first author's. |
| `prompt_basic.txt` | The basic prompt — a minimal classification instruction, verbatim. |
| `prompt_step_by_step.txt` | The step-by-step prompt — the statutory test as an explicit procedure, verbatim. Derived from the rubric and written before any incident was labelled. |
| `expert_labels.csv` | The expert labels: one row per incident, each statutory step recorded separately, plus the final tier, a three-point confidence rating, whether the full AIID page was consulted, and a free-text note. |
| `label_corrections.csv` | Every field changed after labelling, with the reason. No entry is a fresh legal judgement: each either applies a ruling made on materially identical facts elsewhere in the sample, or is entailed by the decision procedure. |
| `rubric_dev_exclusions.csv` | Six incidents used while drafting the rubric, excluded from the evaluation set because the labels on them are not independent. |
| `sample_v1_frozen.csv` | The drawn sample, with the stratum used only to obtain variety in the draw. The stratum is a keyword proxy, is frequently wrong, and was withheld from the annotator. |
| `model_outputs.csv` | 4,198 model classifications: incident, condition (`naive` = basic prompt, `decomposed` = step-by-step prompt), model, run, tier, per-step record (step-by-step only), and the model's one-sentence rationale. |
| `08_analyze.py` | Agreement (quadratic weighted kappa with bootstrap intervals), self-consistency, error direction by Annex III membership, and step-level divergence. |
| `09_ingest_labels.py` | Reads the labelling workbooks and validates every value against the rubric's decision procedure. |
| `11_apply_corrections.py` | Applies the corrections in `label_corrections.csv` and records them. |

## Reproducing the analysis

```
pip install pandas numpy
python 08_analyze.py --split all
```

The scripts resolve paths relative to their own location, so no configuration is needed.

## A note on one classification decision

The treatment of third-party misuse of general-purpose generative systems — a fraudster
using an off-the-shelf voice cloner, for instance — is the single most consequential
judgement in the study. It is classified under Art. 50 rather than Art. 5, on the
reasoning set out in the rubric, and reversing it inverts the ranking of the models.
The per-step labels allow the alternative reading to be scored; the paper reports the
decision as a decision.

## Licence

Rubric, prompts and labels: CC BY 4.0. Analysis scripts: MIT. See `LICENSE`.
Incident text and metadata are from the AI Incident Database and remain subject to its
terms.

## Citation

```
S. Kofilovski. Category, Not Severity: How Large Language Models Misclassify AI
Incidents Under the EU AI Act Risk Taxonomy. Proceedings of the 28th International
Multiconference Information Society - SiKDD 2026, Ljubljana, October 2026.
```
