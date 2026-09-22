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
