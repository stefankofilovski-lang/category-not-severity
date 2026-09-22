# Response to reviewers: submission 109

**Revised title:** Legal Categories from Incident Reports: Evaluating 14 LLMs under the EU AI Act

Thank you for the detailed comments. We have rewritten the paper, added paired uncertainty estimates and nominal measures, expanded the disagreement analysis, and completed a separate evidence comparison. The reference labels remain the first author's expert legal assessment. We explain below which requests have been completed and which require further human evaluation.

## Reviewer 1

### 1. Reliability of the expert reference

The abstract and Sections 3.1 and 5 now explain the reference directly: a lawyer developed the rubric and supplied his assessment of the legally correct categories under that interpretation and the available evidence. We have removed broader claims of independently established legal accuracy. The supplement preserves confidence ratings, notes and the correction log, including 19 field changes across ten incidents.

A second specialist was not available within the revision period. Independent annotation, agreement measurement and adjudication remain unperformed. Clearer disclosure and sensitivity analysis do not replace them. We ask the chairs to assess the narrower exploratory contribution with this request explicitly unmet.

### 2. Unequal evidence on 14 cases

We completed the reviewer's proposed exclusion analysis. Section 4.1 reports the remaining 130 cases alongside the full sample. Exact agreement is 71.7%/79.5%, and mean QWK is 0.379/0.469, for basic/checklist prompting. Nine excluded cases are high-risk, so we also disclose the changed class mix. The excluded IDs and results are in Supplement S6.

We additionally ran a separate comparison on the 14 cases. Every model received both the same short record and the same expanded evidence packet, under both prompts, with a fresh short-record baseline. All 784 calls were attempted once; 750 gave valid category answers. Model versions, provider settings, failures and usage are documented in Supplement S11. Thirteen canonical identifiers match the archive; the unavailable Qwen Max version has a disclosed replacement.

Among common valid pairs, the expanded records changed 18/187 basic-prompt labels and 26/179 checklist labels. Mean paired agreement changed by 0.18 percentage points [−3.53, 3.85] and −8.95 [−15.48, −3.23], respectively. The negative finding appears in the abstract and Section 4.2.

The original expert labels were retained as a fixed reference and were not reassessed against the new packets. Those packets were assembled for the follow-up and do not reconstruct the original annotation evidence. The analysis therefore measures how the evidence supplied to models changes their agreement with the existing reference. It does not establish expert–model evidence equivalence or independently verified legal corrections. Repeated-call variability remains unmeasured.

### 3. Uncertainty and paired analysis

Table 1 gives 95% incident-bootstrap intervals and scorable counts for all original QWK estimates. Figure 2 shows intervals for directional differences and paired prompt changes. We resample incidents while keeping both prompts and all models together, using 10,000 draws. Paired QWK uses records scorable under both prompts for each model; individual estimates use their stated available cases.

Exact agreement rises by 6.35 percentage points [2.93, 9.87]. The paired mean QWK change is 0.068 [−0.007, 0.143], whose interval includes zero. We make no universal-improvement or multiple-model significance claim. Supplement S5–S7 reports per-model comparisons and sensitivities, including exclusion of the 15 automated-driving cases. The intervals condition on fixed expert labels and model outputs.

Supplement S13 now also reports the paired macro-F1 change, −0.002 [−0.079, 0.081], and checks the original held-out partition. On those 102 records, exact agreement rises by 5.32 points [1.47, 9.31]; removing their 14 additional-source cases leaves 88 records. These are post-hoc checks, not claims of a prospectively untouched test set. Median model gain is 4.51 points; nine models improve and five decline. Leaving out one model at a time retains a positive panel mean gain, between 4.01 and 7.53 points. All fourteen models remain in the main analysis.

### 4. Development examples and independence

Section 3.1 names all six excluded examples. Supplement S2–S3 connects them to the saved development notes and explains their limited coverage. They do not validate every prohibition or the product route, and we do not describe their selection as random.

The sample flow is 150 sampled records minus six examples, leaving 144. The historical 44/106 development/held-out split becomes 42/102 after exclusion. The first author confirms that he revised the legal labels before seeing any model answers. We now distinguish this author-reported timing from facts recoverable from archived files. The pooled evaluation includes development records and is not described as an untouched test set. We have removed the assertion that all rubric decisions preceded annotation; the exact early selection process remains incompletely documented.

### 5. Severity substitution

The revised title, abstract and conclusions describe agreement with an expert reference. We did not independently measure severity, so classification by perceived harm remains a possible explanation. Section 4.3 and Supplement S6 explain category composition and the limits of the imposed scale: prohibited cannot be over-classified and minimal cannot be under-classified. We do not claim that the directional pattern identifies a reasoning mechanism.

## Reviewer 2

### 1. Measures and human evaluation

Section 3.2 defines exact agreement and six-label macro-F1, and the supplement reports precision, recall and confusion matrices. Missing answers count as nonmatches and false negatives. The always-transparency baseline is 53.5% exact agreement and 0.116 macro-F1.

QWK is retained for comparison, with an explicit warning that its category distances are not a statutory harm scale. The unrelated MIT human score is context, not a human-performance threshold. Mean macro-F1 is almost unchanged, 0.606/0.604, despite the exact-agreement gain.

A new independent human evaluation of model explanations has not been completed. The case audit took place after the model runs. AI assisted with case selection and preparation; the author made the recorded legal judgments. The author has explicitly accepted the presented case summaries and reasons for S014, S024 and S140, retaining their labels. AI-generated recommendations for the remaining cases are prepared for the author’s final review and have not changed the expert reference or the reported model scores. Supplement S12 records the scope: the author assessed the summaries and stated rationale examples presented in the conversation, not every individual model explanation. This does not replace independent annotation or a completed 20-case evaluation.

### 2. Depth of disagreement analysis

Section 4.3 and Supplement S6–S9 now cover all-record confusions, six recorded rule fields, per-model comparisons, first recorded differences and seven paired case dossiers. The dossiers include the source record, expert note, both prompts' labels, stored explanations and unresolved facts. The paper discusses S058, S011 and S024 as examples of product assumptions, evidential thresholds and the AI-system definition. A recorded disagreement is not automatically a model error.

We also restore eight documented earlier labels in a separate sensitivity check. The paired QWK change becomes 0.036 [−0.034, 0.107]. This tests dependence on the annotation history without endorsing either interpretation. Section 5 flags the Article 5 tension in S083. The original reference is preserved while the author considers the prepared recommendation. The three completed author judgments concern the AI-system gate and unsupported factual assumptions; they do not establish a completed human evaluation of the full sample.

Supplement S13 adds a reproducible 22-case fraud-family exclusion to examine whether the exact-agreement gain depends entirely on those historically transparency-labelled cases. The remaining 122 cases give a 4.57-point gain [0.94, 8.43], while paired QWK and macro-F1 intervals include zero. This is a stress test of unchanged labels, not a finding that all flagged cases should be prohibited. The prepared review material contains draft suggestions, not additional human annotations; no AI-derived reference replaces the expert labels in this paper.

Supplement S14 reports all six rule fields by reference value, including negatives, unclear and not-applicable answers. Article 5 agreement is 51/140 (36.4%) on positive-reference cases, compared with 76.6% across all records. All fifteen positive product-route records concern automated driving; the 95.3% overall product-field agreement does not establish broad legal competence on other products.

Section 3.2 also identifies two limits in the archived checklist: its abstention instruction differs from the basic prompt, and its Article 5(1)(b) summary omits the material-distortion and significant-harm thresholds. The original prompts are preserved, so reported results describe the actual experiment. A revised instruction is not presented as if it generated the archived answers.

Supplement S15 audits the remaining instruction assumptions, including the trained/configured prerequisite in Article 5(1)(a), the product-type presumptions, incomplete exception wording and the distinction between creating political content and developing a system. The abstract now states the exact-agreement finding without implying that the checklist has been validated as a complete legal test.

### 3. Dataset and legal framework

Sections 2–3 explain the Act before the experiment, then describe the export, population, sampling, input fields, date range, text lengths, class counts and exclusions. Sampling buckets are distinct from legal labels. Sparse domain counts are stated in Section 4.3.

We interpret the benchmark against the July 2024 Act with 113 numbered articles, 13 chapters and 13 annexes. Supplement S4 maps them and explains the July 2026 amendment boundary. The archived rubric and checklist refer to classification “today”; a common historical legal version was not explicitly fixed for all participants. Section 2 now states that this is an interpretive scope, not a uniformly controlled legal-version experiment. The original predictions are not presented as an updated-law evaluation. Transparency duties may overlap with high-risk status; minimal does not mean harmless or free of duties. General-purpose use does not establish a blanket Article 5 exemption.

Section 2 restores the hypothetical EU-placement/use task and explains that the rubric/checklist set aside territorial and temporal applicability, while the basic prompt does not repeat that assumption. These labels are not retrospective findings of liability for historical or non-EU incidents. Supplement S13 flags six synthetic-intimate-material records and a broader set of twenty product-related records. Excluding all 26 leaves an exact-agreement gain of 4.66 points [0.97, 8.29], without a clear macro-F1 or QWK gain. This non-exhaustive diagnostic does not establish which legal version each model used. The new intimate-material prohibitions' December 2026 application date is distinguished from the amendment's entry into force.

### 4. Language and organisation

We rewrote the full manuscript in shorter, direct sentences. It now moves from the problem to the law, records, comparison, findings and limits. The abstract starts with the missing-facts problem. The methods explain each measure, and separate results subsections answer what the checklist changed, whether more evidence helped and where answers differed. Awkward expressions and repeated defensive qualifications have been removed. The acknowledgements retain disclosure of LLM assistance.

### 5. Single-annotator limitation

The abstract, reference description and discussion state the limitation and the first author's role in both rubric construction and annotation. His legal assessment is retained, while broader reliability claims are qualified. Independent specialist validation remains unperformed, as explained in response 1.1.

### 6. Figure and table placement

Figure 1 gives a compact overview on page 1. Table 1 appears on page 3, following its first discussion on page 2; Figure 2 appears on page 4 after its discussion on page 3. Its labels now say that unclear cases are excluded and identify the extra-source exclusion and restored earlier labels. Captions explain the evidence conditions, exclusions and uncertainty. The manuscript keeps the template font sizes and fits four pages including references. Every final rendered page is checked before delivery.

## Chairs' instructions

The paper includes DOI `10.70314/is.2026.sikdd.109` in the first-page footnote, uses title case and has no page numbers. The author-approved four-page PDF was resubmitted to EasyChair as paper 109, version 3, on 23 September 2026. Final conference acceptance remains a decision for the chairs.

The public companion contains the unchanged research inputs and outputs under `research/` and the current manuscript and new diagnostics under `revision/`. It supplies both verbatim prompts, the rubric, labels and correction history, parsed predictions, source-linked expanded inputs, model/provider metadata, analysis scripts and a SHA-256 manifest. Its README gives reproducible offline commands. Personal correspondence, internal working instructions, administrative records, credentials and raw provider-response envelopes are excluded.

The follow-up result is explicitly the unweighted mean of model-specific changes on common valid pairs. Counting failed answers as nonmatches preserves the directions (+0.51 and −7.14 points). Supplement S11 and the added packet-size note document the source-selection approach and passage lengths. All calculations and editorial changes described here are complete. The paper preserves the original expert reference and the three recorded post-run author confirmations. Draft AI recommendations remain author-review material, not adopted research decisions.
