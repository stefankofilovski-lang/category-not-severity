"""Apply Stefan's post-hoc rulings uniformly across both splits, with an audit trail.

Stefan labelled the dev split BEFORE revising his reading of Art. 5(1)(a), then revised
the held-out split. This script carries the revision back over dev so one rule governs
all 144 rows, and records every change in data/label_corrections.csv so the paper can
state exactly what was altered and why.

Nothing here is a fresh legal judgement: each change either applies a ruling Stefan made
on materially identical facts in the held-out split, or is entailed by the decision
procedure itself.
"""
import os
import pandas as pd

ROOT = r"F:\SkiDD paper"

# Third-party misuse of general-purpose generative tools. Stefan moved 28 held-out rows
# of this exact shape from prohibited to transparency; these are their dev twins.
MISUSE_TO_TRANSPARENCY = {
    "S045": "donation scam using generated disaster images - twin of S085/S122",
    "S076": "non-consensual deepfake pornography - twin of S063/S077/S149",
    "S079": "coordinated propaganda on a platform - moderation sits in the DSA (rubric Step 3)",
    "S083": "romance scam using a deepfake persona - twin of S091",
    "S084": "health-expert deepfakes selling supplements - twin of S125",
    "S089": "manipulated protest audio - twin of S096/S101/S134/S136",
    "S116": "doctor deepfakes selling fake health products - twin of S084/S125",
    "S137": "celebrity deepfake crypto scam - twin of S085/S128/S135",
}

# Purpose-built or configured systems: Stefan kept prohibited on S095 and S131 (assembled
# fraud operations) and asked for S106 back (a system configured by prompt to distort an
# assessment). These dev rows match those precedents rather than the misuse cluster.
KEEP_PROHIBITED = {
    "S069": "160-site fake-news network built by an identifiable operator - twin of S131",
    "S093": "avatars configured with fabricated medical credentials - twin of S106",
    "S123": "law-enforcement facial identification in public, apparently real time - Art. 5(1)(h), twin of S025",
}

# Stefan's explicit instruction after reviewing the held-out revision.
RESTORE = {"S106": "hidden prompts configuring AI reviewers to return positive reviews - Art. 5(1)(a) configuration test"}

# Entailed fix: S020 was moved out of Annex III, but transparency requires Art. 50 to fire.
FORCE_TIER = {"S020": ("minimal", "Annex III now 'none' and Art. 50 is 'no'; transparency has nothing to rest on")}


def apply(df):
    log = []

    def setrow(sid, col, val, why):
        m = df.sample_id == sid
        if not m.any():
            return
        old = df.loc[m, col].iloc[0]
        if str(old) == str(val):
            return
        df.loc[m, col] = val
        log.append({"sample_id": sid, "field": col, "from": old, "to": val, "reason": why})

    for sid, why in MISUSE_TO_TRANSPARENCY.items():
        setrow(sid, "FINAL_risk_tier", "transparency", why)
        setrow(sid, "L1_art5_prohibited", "no", why)
        setrow(sid, "L6_art50_transparency", "yes", why)
    for sid, why in KEEP_PROHIBITED.items():
        setrow(sid, "FINAL_risk_tier", "prohibited", why)
        setrow(sid, "L1_art5_prohibited", "yes", why)
    for sid, why in RESTORE.items():
        setrow(sid, "FINAL_risk_tier", "prohibited", why)
        setrow(sid, "L1_art5_prohibited", "yes", why)
    for sid, (tier, why) in FORCE_TIER.items():
        setrow(sid, "FINAL_risk_tier", tier, why)

    # entailed consequences
    n = (df.L2_annex_iii_domain == "none")
    for col in ("L4_art6_3_derogation", "L5_profiling_override"):
        bad = n & (df[col] != "not_applicable")
        for sid in df.loc[bad, "sample_id"]:
            setrow(sid, col, "not_applicable", "no Annex III area (entailed)")
    bad = df.FINAL_risk_tier.isin(["transparency", "minimal"]) & (df.L1_art5_prohibited == "yes")
    for sid in df.loc[bad, "sample_id"]:
        setrow(sid, "L1_art5_prohibited", "no", "tier is not prohibited (entailed)")
    return df, pd.DataFrame(log)


if __name__ == "__main__":
    df = pd.read_csv(os.path.join(ROOT, "data", "expert_labels.csv"), encoding="utf-8-sig")
    df, log = apply(df)
    df.to_csv(os.path.join(ROOT, "data", "expert_labels.csv"), index=False, encoding="utf-8-sig")
    log.to_csv(os.path.join(ROOT, "data", "label_corrections.csv"), index=False, encoding="utf-8-sig")
    done = df[df.FINAL_risk_tier.notna() & (df.FINAL_risk_tier != "")]
    print(f"{len(log)} field changes across {log.sample_id.nunique() if len(log) else 0} rows "
          f"-> data/label_corrections.csv")
    print(f"\nlabelled {len(done)}/{len(df)}  "
          f"(dev {(done.split=='dev').sum()}, heldout {(done.split=='heldout').sum()})")
    print(done.FINAL_risk_tier.value_counts().to_string())
