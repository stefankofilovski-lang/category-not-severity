"""Analysis for the SiKDD 2026 paper.

Compares the expert labels against every model/condition/run and produces:
  1. agreement.csv        QWK + exact agreement per condition x model (with bootstrap CI)
  2. consistency.csv      self-consistency across repeated runs per condition x model
  3. error_direction.csv  over/under-classification split by Annex III domain
  4. step_divergence.csv  (decomposed only) which statutory step the models fumble

The tier scale is ordinal: minimal < transparency < high < prohibited. The two
off-scale answers (not_ai_system, insufficient_information) cannot enter a weighted
kappa, so they are excluded from QWK and reported as coverage instead.

Usage: python analysis/08_analyze.py [--split heldout] [--boot 2000]
"""
import argparse
import json
import os
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get("PAPER_ROOT", HERE)
RES = ROOT
ORD = {"minimal": 0, "transparency": 1, "high": 2, "prohibited": 3}
OFFSCALE = {"not_ai_system", "insufficient_information"}
RNG = np.random.default_rng(2026)


def qwk(a, b, k=4):
    """Quadratic weighted kappa on a fixed 0..k-1 scale."""
    a, b = np.asarray(a, int), np.asarray(b, int)
    if len(a) == 0:
        return np.nan
    O = np.zeros((k, k))
    for i, j in zip(a, b):
        O[i, j] += 1
    w = (np.arange(k)[:, None] - np.arange(k)[None, :]) ** 2 / (k - 1) ** 2
    ha = np.bincount(a, minlength=k)
    hb = np.bincount(b, minlength=k)
    E = np.outer(ha, hb) / len(a)
    den = (w * E).sum()
    if den == 0:
        return np.nan
    return 1 - (w * O).sum() / den


def boot_ci(a, b, n):
    if len(a) < 5 or n <= 0:
        return np.nan, np.nan
    a, b = np.asarray(a), np.asarray(b)
    vals = []
    for _ in range(n):
        idx = RNG.integers(0, len(a), len(a))
        v = qwk(a[idx], b[idx])
        if not np.isnan(v):
            vals.append(v)
    if not vals:
        return np.nan, np.nan
    return float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))


def load(split):
    exp = pd.read_csv(os.path.join(ROOT, "expert_labels.csv"), encoding="utf-8-sig")
    exp = exp[exp["FINAL_risk_tier"].notna() & (exp["FINAL_risk_tier"] != "")]
    runs = pd.read_csv(os.path.join(ROOT, "model_outputs.csv"), encoding="utf-8-sig")
    runs = runs[~runs["pilot"].fillna(False).astype(bool)]
    if split != "all":
        exp = exp[exp["split"] == split]
    exp = exp.rename(columns={"FINAL_risk_tier": "expert_tier",
                              "L2_annex_iii_domain": "expert_domain",
                              "confidence_1to3": "expert_conf"})
    cols = ["sample_id", "split", "expert_tier", "expert_domain", "expert_conf",
            "L1_art5_prohibited", "L3_annex_i_product", "L4_art6_3_derogation",
            "L5_profiling_override", "L6_art50_transparency"]
    cols = [c for c in cols if c in exp.columns]
    return exp[cols].merge(runs, on="sample_id", how="inner", suffixes=("", "_run"))


def agreement(df, nboot):
    rows = []
    for (cond, model), g in df.groupby(["condition", "model"]):
        g1 = g[g["run"] == g["run"].min()]          # one run per model for the headline
        n_all = len(g1)
        on = g1[~g1.expert_tier.isin(OFFSCALE) & ~g1.risk_tier.isin(OFFSCALE)]
        a = [ORD[t] for t in on.expert_tier]
        b = [ORD[t] for t in on.risk_tier]
        k = qwk(a, b)
        lo, hi = boot_ci(a, b, nboot)
        rows.append({
            "condition": cond, "model": model, "n": n_all, "n_scored": len(on),
            "qwk": round(k, 3) if not np.isnan(k) else np.nan,
            "ci_lo": round(lo, 3) if not np.isnan(lo) else np.nan,
            "ci_hi": round(hi, 3) if not np.isnan(hi) else np.nan,
            "exact_pct": round(100 * (g1.expert_tier == g1.risk_tier).mean(), 1),
            "model_offscale_pct": round(100 * g1.risk_tier.isin(OFFSCALE).mean(), 1),
        })
    return pd.DataFrame(rows).sort_values(["condition", "qwk"], ascending=[True, False])


def consistency(df):
    rows = []
    for (cond, model), g in df.groupby(["condition", "model"]):
        runs = sorted(g["run"].unique())
        if len(runs) < 2:
            continue
        wide = g.pivot_table(index="sample_id", columns="run", values="risk_tier",
                             aggfunc="first")
        pairs, agree = 0, 0
        for i in range(len(runs)):
            for j in range(i + 1, len(runs)):
                both = wide[[runs[i], runs[j]]].dropna()
                pairs += len(both)
                agree += (both[runs[i]] == both[runs[j]]).sum()
        unan = wide.dropna().nunique(axis=1).eq(1).mean() if len(wide.dropna()) else np.nan
        rows.append({"condition": cond, "model": model, "n_runs": len(runs),
                     "pairwise_agree_pct": round(100 * agree / pairs, 1) if pairs else np.nan,
                     "unanimous_pct": round(100 * unan, 1) if not np.isnan(unan) else np.nan})
    if not rows:
        return pd.DataFrame()
    return pd.DataFrame(rows).sort_values(["condition", "pairwise_agree_pct"],
                                          ascending=[True, False])


def error_direction(df):
    d = df[~df.expert_tier.isin(OFFSCALE) & ~df.risk_tier.isin(OFFSCALE)].copy()
    d = d[d["run"] == d["run"].min()]
    d["delta"] = d.risk_tier.map(ORD) - d.expert_tier.map(ORD)
    d["inside_annex_iii"] = np.where(d.expert_domain.isin(["none", "unclear"]),
                                     "outside", "inside")
    out = []
    for keys, g in d.groupby(["condition", "inside_annex_iii"]):
        out.append({"condition": keys[0], "group": keys[1], "n": len(g),
                    "over_pct": round(100 * (g.delta > 0).mean(), 1),
                    "under_pct": round(100 * (g.delta < 0).mean(), 1),
                    "exact_pct": round(100 * (g.delta == 0).mean(), 1),
                    "mean_delta": round(g.delta.mean(), 3)})
    by_dom = []
    for keys, g in d.groupby(["condition", "expert_domain"]):
        by_dom.append({"condition": keys[0], "group": keys[1], "n": len(g),
                       "over_pct": round(100 * (g.delta > 0).mean(), 1),
                       "under_pct": round(100 * (g.delta < 0).mean(), 1),
                       "exact_pct": round(100 * (g.delta == 0).mean(), 1),
                       "mean_delta": round(g.delta.mean(), 3)})
    return pd.DataFrame(out + by_dom)


def step_divergence(df):
    """For the decomposed condition, compare each recorded statutory step to the annotator's."""
    pairs = [("art5", "L1_art5_prohibited"), ("annex_i", "L3_annex_i_product"),
             ("annex_iii", "expert_domain"), ("derogation", "L4_art6_3_derogation"),
             ("profiling", "L5_profiling_override"), ("art50", "L6_art50_transparency")]
    d = df[(df.condition == "decomposed") & df.steps.notna() & (df.steps != "")].copy()
    if d.empty:
        return pd.DataFrame()
    d = d[d["run"] == d["run"].min()]
    parsed = d.steps.apply(lambda s: json.loads(s) if isinstance(s, str) and s else {})
    rows = []
    for model, idx in d.groupby("model").groups.items():
        sub = d.loc[idx]
        p = parsed.loc[idx]
        rec = {"model": model, "n": len(sub)}
        for step, col in pairs:
            if col not in sub.columns:
                continue
            got = p.apply(lambda o: str(o.get(step, "")).strip())
            want = sub[col].astype(str).str.strip()
            both = (got != "") & (want != "")
            rec[step] = round(100 * (got[both] == want[both]).mean(), 1) if both.any() else np.nan
        rows.append(rec)
    return pd.DataFrame(rows).sort_values("model")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--split", default="heldout", choices=["dev", "heldout", "all"])
    ap.add_argument("--boot", type=int, default=2000)
    a = ap.parse_args()

    df = load(a.split)
    if df.empty:
        raise SystemExit("No overlap between expert labels and model runs yet.")
    print(f"split={a.split}  {df.sample_id.nunique()} incidents  "
          f"{df.model.nunique()} models  {sorted(df.condition.unique())}\n")

    for name, tbl in [("agreement", agreement(df, a.boot)),
                      ("consistency", consistency(df)),
                      ("error_direction", error_direction(df)),
                      ("step_divergence", step_divergence(df))]:
        path = os.path.join(RES, f"{name}_{a.split}.csv")
        if tbl.empty:
            print(f"--- {name}: nothing to report yet ---\n")
            continue
        tbl.to_csv(path, index=False, encoding="utf-8-sig")
        print(f"--- {name} ---")
        print(tbl.to_string(index=False))
        print(f"-> {path}\n")
