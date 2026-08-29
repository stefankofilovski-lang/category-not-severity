"""Read the expert labels out of the labelling workbooks (or CSV exports).

Accepts .xlsx or .csv downloaded from Google Sheets, maps the friendly column
headers back to canonical field names, validates every value, drops the six
rubric-development incidents, and writes data/expert_labels.csv.

It also runs consistency checks against the rubric's own decision procedure and
prints anything that looks like a slip. It never silently fixes a label -- the
labels are the study's reference data, so every correction is the annotator's call.

Usage:
    python analysis/09_ingest_labels.py                    # both splits, default paths
    python analysis/09_ingest_labels.py path1.xlsx path2.csv
"""
import glob
import json
import os
import sys
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get("PAPER_ROOT", HERE)
OUT = os.path.join(ROOT, "expert_labels.csv")

LABELS = {
    "L1_art5_prohibited":    {"no", "yes", "unclear"},
    "L3_annex_i_product":    {"no", "yes", "unclear"},
    "L2_annex_iii_domain":   {"none", "biometrics", "critical_infrastructure", "education",
                              "employment", "essential_services", "law_enforcement",
                              "migration", "justice_democracy", "unclear"},
    "L4_art6_3_derogation":  {"not_applicable", "applies", "does_not_apply", "unclear"},
    "L5_profiling_override": {"not_applicable", "yes", "no", "unclear"},
    "L6_art50_transparency": {"no", "yes", "unclear"},
    "FINAL_risk_tier":       {"prohibited", "high", "transparency", "minimal",
                              "not_ai_system", "insufficient_information"},
    "confidence_1to3":       {"1", "2", "3"},
    "consulted_full_page":   {"no", "yes"},
}

HEADER_MAP = {
    "sample_id": "sample_id", "id": "sample_id",
    "1. art.5 banned?": "L1_art5_prohibited",
    "2. annex i product?": "L3_annex_i_product",
    "3. annex iii area": "L2_annex_iii_domain",
    "4. derogation 6(3)": "L4_art6_3_derogation",
    "5. profiling?": "L5_profiling_override",
    "6. art.50?": "L6_art50_transparency",
    "==> final tier": "FINAL_risk_tier",
    "final tier": "FINAL_risk_tier",
    "unnamed: 11": "FINAL_risk_tier",
    "sure? 3=yes": "confidence_1to3",
    "opened link?": "consulted_full_page",
    "notes": "notes",
}
for k in LABELS:
    HEADER_MAP[k.lower()] = k


def load(path):
    if path.lower().endswith(".csv"):
        df = pd.read_csv(path, dtype=str, encoding="utf-8-sig")
    else:
        df = pd.read_excel(path, sheet_name="LABEL HERE", dtype=str)
    ren, keep = {}, []
    for c in df.columns:
        key = str(c).strip().lower()
        if key in HEADER_MAP:
            ren[c] = HEADER_MAP[key]
            keep.append(HEADER_MAP[key])
    df = df.rename(columns=ren)[keep]
    df = df[df["sample_id"].notna()]
    df = df[df["sample_id"].astype(str).str.match(r"^S\d+$", na=False)]
    for c in df.columns:
        df[c] = df[c].astype(str).str.strip().replace({"nan": "", "None": ""})
    return df


def check(df, excluded):
    problems, blank = [], []
    df = df.fillna("")
    for _, r in df.iterrows():
        sid = r["sample_id"]
        if sid in excluded:
            continue
        missing = [c for c in LABELS if str(r.get(c, "")).strip() in ("", "nan")]
        if missing:
            blank.append((sid, missing))
            continue
        for c, allowed in LABELS.items():
            if r[c] not in allowed:
                problems.append(f"{sid}: {c} = {r[c]!r} is not an allowed value")

        f, a5 = r["FINAL_risk_tier"], r["L1_art5_prohibited"]
        ai, a3 = r["L3_annex_i_product"], r["L2_annex_iii_domain"]
        der, pro, a50 = r["L4_art6_3_derogation"], r["L5_profiling_override"], r["L6_art50_transparency"]

        if a5 == "yes" and f != "prohibited":
            problems.append(f"{sid}: step 1 is 'yes' but FINAL is {f!r}, not 'prohibited'")
        if f == "prohibited" and a5 != "yes":
            problems.append(f"{sid}: FINAL is 'prohibited' but step 1 is {a5!r}")
        if ai == "yes" and f not in ("high", "prohibited"):
            problems.append(f"{sid}: Annex I product but FINAL is {f!r}, not 'high'")
        if a3 == "none" and der != "not_applicable":
            problems.append(f"{sid}: no Annex III area but derogation is {der!r}, "
                            f"expected 'not_applicable'")
        if a3 == "none" and pro != "not_applicable":
            problems.append(f"{sid}: no Annex III area but profiling is {pro!r}, "
                            f"expected 'not_applicable'")
        if (a3 not in ("none", "unclear") and ai != "yes" and a5 != "yes"
                and (der == "does_not_apply" or pro == "yes") and f != "high"):
            problems.append(f"{sid}: Annex III {a3!r} with no working derogation "
                            f"(derogation={der!r}, profiling={pro!r}) but FINAL is {f!r}, "
                            f"expected 'high'")
        if f == "transparency" and a50 != "yes":
            problems.append(f"{sid}: FINAL is 'transparency' but Art. 50 is {a50!r}")
        if f == "minimal" and a50 == "yes":
            problems.append(f"{sid}: Art. 50 is 'yes' but FINAL is 'minimal', "
                            f"expected 'transparency' unless something higher fired")
        if f == "minimal" and a3 not in ("none", "unclear"):
            problems.append(f"{sid}: FINAL is 'minimal' but the system is in Annex III area "
                            f"{a3!r} -- only a derogation with no profiling gets there")
    return problems, blank


if __name__ == "__main__":
    paths = sys.argv[1:] or [p for p in
                             glob.glob(os.path.join(ROOT, "LABEL_*.xlsx"))
                             + glob.glob(os.path.join(ROOT, "LABEL_*.csv"))
                             if "frozen" not in p.lower()]
    if not paths:
        sys.exit("No LABEL_*.xlsx / LABEL_*.csv found in data/")

    exc = pd.read_csv(os.path.join(ROOT, "rubric_dev_exclusions.csv"),
                      encoding="utf-8-sig")
    excluded = set(exc["sample_id"])

    frames = []
    for p in paths:
        d = load(p)
        print(f"read {os.path.basename(p):24s} {len(d)} rows")
        frames.append(d)
    df = pd.concat(frames, ignore_index=True).drop_duplicates("sample_id", keep="last")
    df = df[~df.sample_id.isin(excluded)]

    sample = pd.read_csv(os.path.join(ROOT, "sample_v1_frozen.csv"), encoding="utf-8-sig")
    sample = sample[~sample.sample_id.isin(excluded)]
    df = sample[["sample_id", "split", "year", "title"]].merge(df, on="sample_id", how="left")

    # Normalisations strictly entailed by the rubric's own decision procedure.
    # These are mechanical consequences of a ruling, never new judgements.
    n1 = (df.FINAL_risk_tier.isin(["transparency", "minimal"])) & (df.L1_art5_prohibited == "yes")
    df.loc[n1, "L1_art5_prohibited"] = "no"
    n2 = (df.L2_annex_iii_domain == "none") & (df.L4_art6_3_derogation != "not_applicable")
    df.loc[n2, "L4_art6_3_derogation"] = "not_applicable"
    n3 = (df.L2_annex_iii_domain == "none") & (df.L5_profiling_override != "not_applicable")
    df.loc[n3, "L5_profiling_override"] = "not_applicable"
    if n1.sum() or n2.sum() or n3.sum():
        print("normalised (entailed, not judged): %d rows L1 yes->no; %d derogation and %d profiling -> not_applicable" % (n1.sum(), n2.sum(), n3.sum()))
    problems, blank = check(df, excluded)
    done = df[df["FINAL_risk_tier"].notna() & (df["FINAL_risk_tier"] != "")]
    print(f"\nlabelled {len(done)}/{len(df)}   "
          f"(dev {(done.split == 'dev').sum()}/{(df.split == 'dev').sum()}, "
          f"heldout {(done.split == 'heldout').sum()}/{(df.split == 'heldout').sum()})")

    if len(done):
        print("\nyour tier distribution:")
        print(done["FINAL_risk_tier"].value_counts().to_string())
        if (done["confidence_1to3"] != "").any():
            print("\nconfidence:", done["confidence_1to3"].value_counts().to_dict())

    if blank:
        print(f"\n{len(blank)} rows still incomplete (first 10):")
        for sid, cols in blank[:10]:
            print(f"  {sid}: missing {', '.join(c.split('_')[0] for c in cols)}")
    print(f"\n{len(problems)} consistency flags:")
    for p in problems:
        print("  -", p)

    df.to_csv(OUT, index=False, encoding="utf-8-sig")
    print(f"\nwrote {OUT}")
