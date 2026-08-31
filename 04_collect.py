"""Collect and validate the raw classification outputs into one tidy CSV.

Reads results/raw/{condition}_{model}_run{r}_{split}.json (as written by 06_classify.py),
checks every sample_id against the frozen sample and every answer against the label
space, and writes results/all_runs.csv -- the file released here as model_outputs.csv.

Usage: python 04_collect.py
"""
import json
import os
import re
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get("PAPER_ROOT", HERE)
RAW = os.path.join(ROOT, "results", "raw")
OUT = os.path.join(ROOT, "results", "all_runs.csv")
VALID_TIERS = {"prohibited", "high", "transparency", "minimal", "not_ai_system",
               "insufficient_information"}
PAT = re.compile(r"^(pilot_)?(?P<condition>[a-z]+)_(?P<model>[a-z0-9]+)_run(?P<run>\d+)_(?P<split>[a-z]+)")

if not os.path.isdir(RAW):
    raise SystemExit(f"No raw results at {RAW} - run 06_classify.py first.")

sample = pd.read_csv(os.path.join(ROOT, "sample_v1_frozen.csv"))
known_ids = set(sample["sample_id"])

rows, problems = [], []
for fname in sorted(os.listdir(RAW)):
    if not fname.endswith(".json"):
        continue
    m = PAT.match(fname)
    if not m:
        problems.append(f"{fname}: unrecognized filename pattern, skipped")
        continue
    meta = m.groupdict()
    meta["pilot"] = bool(m.group(1))
    try:
        data = json.load(open(os.path.join(RAW, fname), encoding="utf-8"))
    except json.JSONDecodeError as e:
        problems.append(f"{fname}: JSON parse error: {e}")
        continue
    for item in data:
        sid = item.get("sample_id")
        tier = item.get("risk_tier")
        if sid not in known_ids:
            problems.append(f"{fname}: unknown sample_id {sid!r}")
            continue
        if tier not in VALID_TIERS:
            problems.append(f"{fname}: invalid tier {tier!r} for {sid}")
            continue
        rows.append({
            "sample_id": sid,
            "condition": meta["condition"],
            "model": meta["model"],
            "run": int(meta["run"]),
            "steps": json.dumps(item.get("steps", {}), ensure_ascii=False) if item.get("steps") else "",
            "pilot": meta["pilot"],
            "risk_tier": tier,
            "rationale": item.get("rationale", ""),
            "source_file": fname,
        })

df = pd.DataFrame(rows)
if not df.empty:
    dupes = df.duplicated(subset=["sample_id", "condition", "model", "run"], keep=False)
    if dupes.any():
        problems.append(f"{dupes.sum()} duplicate (sample_id, condition, model, run) rows")
    df = df.merge(sample[["sample_id", "split", "sampling_stratum"]], on="sample_id", how="left")
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    df.to_csv(OUT, index=False, encoding="utf-8-sig")
    print(f"Wrote {OUT}: {len(df)} classifications")
    print("\nCompleteness (non-pilot) - classifications per condition/model/run:")
    main = df[~df["pilot"]]
    if not main.empty:
        print(main.groupby(["condition", "model", "run"]).size().to_string())
    else:
        print("  (no non-pilot runs yet)")

print(f"\n{len(problems)} problems:")
for p in problems:
    print(" -", p)
