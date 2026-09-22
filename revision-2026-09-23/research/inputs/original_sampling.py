"""Build the stratified labeling sample from the AIID export.

Strata are keyword-based *candidate* Annex III domains used ONLY to balance the
sample across domains; they are not labels and are excluded from model inputs.
Fixed seed for reproducibility. Output: data/sample_v1.xlsx (labeling workbook)
and data/sample_v1_frozen.csv (immutable record of the draw).
"""
import re
import pandas as pd
import numpy as np
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

SEED = 2026
TOTAL = 150
DEV_FRACTION = 0.27  # ~40 dev incidents
PATH = r"F:\SkiDD paper\data\AIID_Excel_Export-20260810.xlsx"
OUT_XLSX = r"F:\SkiDD paper\data\sample_v1.xlsx"
OUT_CSV = r"F:\SkiDD paper\data\sample_v1_frozen.csv"

# Candidate strata: the eight Annex III areas + off-Annex control.
# Keyword lists deliberately favor precision over recall; unmatched incidents
# fall into the general pool from which the control group is drawn.
STRATA = {
    "biometrics": [
        "facial recognition", "face recognition", "biometric", "emotion recognition",
        "fingerprint", "iris scan", "gait recognition", "face-scanning", "face scan",
    ],
    "critical_infrastructure": [
        "power grid", "electricity", "water supply", "traffic light", "traffic control",
        "energy grid", "utility", "pipeline", "air traffic", "railway", "power plant",
    ],
    "education": [
        "school", "student", "exam", "teacher", "university", "grading", "proctor",
        "admission", "essay scoring", "education",
    ],
    "employment": [
        "hiring", "recruit", "resume", "job applicant", "job candidate", "employee",
        "worker", "workplace", "interview", "promotion", "fired", "deactivat",
        "gig ", "scheduling software", "productivity monitoring",
    ],
    "essential_services": [
        "credit scor", "loan", "insurance", "welfare", "benefits", "social security",
        "mortgage", "food stamp", "medicaid", "medicare", "emergency call", "911",
        "housing application", "tenant screening", "fraud detection",
    ],
    "law_enforcement": [
        "police", "policing", "arrest", "law enforcement", "gunshot", "surveillance",
        "crime prediction", "predictive policing", "suspect", "shoplifting detection",
        "license plate", "licence plate",
    ],
    "migration": [
        "border", "immigration", "asylum", "visa", "migrant", "passport", "customs",
        "refugee", "deportation",
    ],
    "justice_democracy": [
        "court", "judge", "sentencing", "bail", "parole", "recidivism", "judicial",
        "election", "voting", "voter", "democratic", "legal advice", "lawsuit filing",
    ],
}
CANONICAL_ORDER = list(STRATA.keys())

# Per-stratum quotas; shortfalls flow into the control group.
QUOTA = {k: 13 for k in CANONICAL_ORDER}  # 8 x 13 = 104

inc = pd.read_excel(PATH, sheet_name="Incidents", header=2, engine="openpyxl")
inc = inc[inc["description"].notna() & inc["title"].notna()].copy()

def assign_stratum(row) -> str:
    text = " ".join(
        str(row[c]) for c in ("title", "description", "deployer", "developer", "harmed")
        if pd.notna(row[c])
    ).lower()
    scores = {}
    for stratum, kws in STRATA.items():
        hits = sum(1 for kw in kws if kw in text)
        if hits:
            scores[stratum] = hits
    if not scores:
        return "control_pool"
    best = max(scores.values())
    for stratum in CANONICAL_ORDER:  # deterministic tie-break
        if scores.get(stratum) == best:
            return stratum
    return "control_pool"

inc["sampling_stratum"] = inc.apply(assign_stratum, axis=1)
print("Stratum pool sizes:")
print(inc["sampling_stratum"].value_counts().to_string())

rng = np.random.default_rng(SEED)
picked_parts = []
shortfall = 0
for stratum in CANONICAL_ORDER:
    pool = inc[inc["sampling_stratum"] == stratum]
    n = min(QUOTA[stratum], len(pool))
    shortfall += QUOTA[stratum] - n
    idx = rng.choice(pool.index.to_numpy(), size=n, replace=False)
    picked_parts.append(inc.loc[idx])

control_n = TOTAL - sum(len(p) for p in picked_parts)
control_pool = inc[inc["sampling_stratum"] == "control_pool"]
idx = rng.choice(control_pool.index.to_numpy(), size=control_n, replace=False)
picked_parts.append(inc.loc[idx])

sample = pd.concat(picked_parts).copy()
print(f"\nSampled {len(sample)} incidents "
      f"({control_n} control, shortfall redistributed: {shortfall})")

# Stratified dev/held-out split
sample["split"] = "heldout"
for stratum, grp in sample.groupby("sampling_stratum"):
    n_dev = max(1, round(DEV_FRACTION * len(grp)))
    dev_idx = rng.choice(grp.index.to_numpy(), size=n_dev, replace=False)
    sample.loc[dev_idx, "split"] = "dev"
print(sample["split"].value_counts().to_string())

sample = sample.sort_values("Incident ID").reset_index(drop=True)
sample.insert(0, "sample_id", [f"S{i+1:03d}" for i in range(len(sample))])
sample["aiid_url"] = "https://incidentdatabase.ai/cite/" + sample["Incident ID"].astype(int).astype(str)

KEEP = ["sample_id", "Incident ID", "aiid_url", "year", "title", "description",
        "deployer", "developer", "harmed", "sampling_stratum", "split"]
out = sample[KEEP].rename(columns={"Incident ID": "incident_id"})

# Labeling columns (aligned with the rubric in notes/rubric_v1.md)
LABEL_COLS = {
    "L1_art5_prohibited": ["no", "yes", "unclear"],
    "L2_annex_iii_domain": ["none"] + CANONICAL_ORDER + ["unclear"],
    "L3_annex_i_product": ["no", "yes", "unclear"],
    "L4_art6_3_derogation": ["not_applicable", "applies", "does_not_apply", "unclear"],
    "L5_profiling_override": ["not_applicable", "yes", "no", "unclear"],
    "L6_art50_transparency": ["no", "yes", "unclear"],
    "FINAL_risk_tier": ["prohibited", "high", "transparency", "minimal", "insufficient_information"],
    "confidence_1to3": ["1", "2", "3"],
    "consulted_full_page": ["no", "yes"],
    "notes": None,
}
for col, _ in LABEL_COLS.items():
    out[col] = ""

out.to_csv(OUT_CSV, index=False, encoding="utf-8-sig")

with pd.ExcelWriter(OUT_XLSX, engine="openpyxl") as writer:
    out.to_excel(writer, sheet_name="labeling", index=False)
    ws = writer.sheets["labeling"]
    ws.freeze_panes = "A2"
    widths = {"A": 9, "B": 11, "C": 34, "D": 6, "E": 45, "F": 60, "G": 18, "H": 18,
              "I": 18, "J": 20, "K": 9}
    for col, w in widths.items():
        ws.column_dimensions[col].width = w
    first_label_col = len(KEEP) + 1
    for offset, (col, options) in enumerate(LABEL_COLS.items()):
        letter = get_column_letter(first_label_col + offset)
        ws.column_dimensions[letter].width = 22
        if options:
            dv = DataValidation(type="list", formula1='"' + ",".join(options) + '"',
                                allow_blank=True, showDropDown=False)
            ws.add_data_validation(dv)
            dv.add(f"{letter}2:{letter}{len(out)+1}")

print(f"\nWrote {OUT_XLSX} and {OUT_CSV}")
print("\nFinal sample by stratum and split:")
print(out.groupby(["sampling_stratum", "split"]).size().to_string())
