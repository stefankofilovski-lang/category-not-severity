"""OpenRouter classification harness for the SiKDD 2026 paper.

Modes:
  probe                       verify all panel slugs exist + show live prices (no key needed)
  run --condition naive --split dev --models all --runs 1 [--limit N]
                              classify incidents; per-incident calls; resumable
  report                      summarize spend so far from usage_log.csv

Key: file F:\\SkiDD paper\\.openrouter_key (one line) or env OPENROUTER_API_KEY.
Output: results/raw/{condition}_{modelkey}_run{r}_{split}.json  (+ .jsonl partial for resume)
Spend log: results/usage_log.csv
"""
import argparse
import csv
import json
import os
import re
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import pandas as pd
import requests

ROOT = r"F:\SkiDD paper"
API = "https://openrouter.ai/api/v1/chat/completions"
VALID = {"prohibited", "high", "transparency", "minimal", "not_ai_system",
         "insufficient_information"}

# Panel: MIT replication set (6) + new-generation extension (7). Keys must be [a-z0-9]+
MODELS = {
    # --- MIT June 2026 panel (the four below-chance models + top performer + Haiku) ---
    "sonnet46": "anthropic/claude-sonnet-4.6",
    "gpt52": "openai/gpt-5.2",
    "gemini3f": "google/gemini-3-flash-preview",
    "gemma27b": "google/gemma-3-27b-it",
    "kimi25": "moonshotai/kimi-k2.5",
    "haiku45": "anthropic/claude-haiku-4.5",
    # --- new-generation extension ---
    "sonnet5": "anthropic/claude-sonnet-5",
    "gemini37f": "google/gemini-3.7-flash",
    "kimi3": "moonshotai/kimi-k3",
    "qwen38max": "qwen/qwen3.8-max",
    "qwen3827b": "qwen/qwen3.8-27b",
    "gpt56sol": "openai/gpt-5.6-sol",
    "gpt56luna": "openai/gpt-5.6-luna",
    "grok46": "x-ai/grok-4.6",
}

_lock = threading.Lock()


def get_key():
    p = os.path.join(ROOT, ".openrouter_key")
    if os.path.exists(p):
        return open(p).read().strip()
    k = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if not k:
        sys.exit("No API key: create F:\\SkiDD paper\\.openrouter_key or set OPENROUTER_API_KEY")
    return k


def probe():
    cat = requests.get("https://openrouter.ai/api/v1/models", timeout=60).json()["data"]
    by_id = {m["id"]: m for m in cat}
    print(f"{'key':12s} {'slug':40s} {'$in/M':>8s} {'$out/M':>8s}  ok")
    for k, slug in MODELS.items():
        m = by_id.get(slug)
        if m:
            p = m["pricing"]
            pin = float(p["prompt"]) * 1e6
            pout = float(p["completion"]) * 1e6
            print(f"{k:12s} {slug:40s} {pin:8.3f} {pout:8.3f}  YES")
        else:
            print(f"{k:12s} {slug:40s} {'-':>8s} {'-':>8s}  MISSING!")


def load_incidents(split, limit):
    df = pd.read_csv(os.path.join(ROOT, "data", "sample_v1_frozen.csv"))
    if split != "all":
        df = df[df["split"] == split]
    df = df.sort_values("sample_id")
    if limit:
        df = df.head(limit)
    recs = []
    for _, r in df.iterrows():
        recs.append({
            "sample_id": r["sample_id"],
            "year": int(r["year"]),
            "title": r["title"],
            "description": r["description"],
            "deployer": r["deployer"] if pd.notna(r["deployer"]) else "",
            "developer": r["developer"] if pd.notna(r["developer"]) else "",
            "harmed": r["harmed"] if pd.notna(r["harmed"]) else "",
        })
    return recs


def parse_json_reply(text):
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.S)
    m = re.search(r"\{.*\}", text, flags=re.S)
    if not m:
        raise ValueError("no JSON object found")
    return json.loads(m.group(0))


def classify_one(key, slug, instruction, incident, is_decomposed):
    body = {
        "model": slug,
        "messages": [
            {"role": "system", "content": instruction},
            {"role": "user", "content": "Incident record:\n" + json.dumps(incident, ensure_ascii=False)},
        ],
        "max_tokens": 4096,
        "usage": {"include": True},
    }
    last_err = None
    for attempt in range(4):
        try:
            r = requests.post(API, timeout=180, json=body,
                              headers={"Authorization": f"Bearer {key}"})
            if r.status_code == 429 or r.status_code >= 500:
                time.sleep(5 * (attempt + 1))
                last_err = f"HTTP {r.status_code}"
                continue
            r.raise_for_status()
            data = r.json()
            if "error" in data:
                last_err = str(data["error"])
                time.sleep(3)
                continue
            content = data["choices"][0]["message"]["content"] or ""
            obj = parse_json_reply(content)
            if obj.get("risk_tier") not in VALID:
                last_err = f"invalid tier {obj.get('risk_tier')!r}"
                continue
            obj["sample_id"] = incident["sample_id"]  # trust our id, not the echo
            if is_decomposed and not isinstance(obj.get("steps"), dict):
                obj["steps"] = {}
            usage = data.get("usage", {}) or {}
            return obj, usage
        except Exception as e:
            last_err = repr(e)
            time.sleep(3)
    return ({"sample_id": incident["sample_id"], "risk_tier": "ERROR",
             "rationale": str(last_err)[:300]}, {})


def run(args):
    key = get_key()
    cond = args.condition
    prompt_path = os.path.join(ROOT, "analysis", "prompts", f"{cond}_v1.txt")
    if not os.path.exists(prompt_path):
        sys.exit(f"Prompt file missing (not frozen yet?): {prompt_path}")
    instruction = open(prompt_path, encoding="utf-8").read()
    incidents = load_incidents(args.split, args.limit)
    model_keys = list(MODELS) if args.models == "all" else args.models.split(",")
    for mk in model_keys:
        if mk not in MODELS:
            sys.exit(f"Unknown model key {mk!r}. Known: {', '.join(MODELS)}")
    raw_dir = os.path.join(ROOT, "analysis", "results", "raw")
    os.makedirs(raw_dir, exist_ok=True)
    usage_path = os.path.join(ROOT, "analysis", "results", "usage_log.csv")
    new_usage_file = not os.path.exists(usage_path)

    jobs = []       # (model_key, run_idx, incident)
    partials = {}   # (mk, run) -> {sample_id: obj}
    for mk in model_keys:
        for ri in range(1, args.runs + 1):
            tag = f"{cond}_{mk}_run{ri}_{args.split}"
            jl = os.path.join(raw_dir, tag + ".jsonl")
            done = {}
            if os.path.exists(jl):
                for line in open(jl, encoding="utf-8"):
                    try:
                        o = json.loads(line)
                        if o.get("risk_tier") in VALID:
                            done[o["sample_id"]] = o
                    except json.JSONDecodeError:
                        pass
            partials[(mk, ri)] = done
            for inc in incidents:
                if inc["sample_id"] not in done:
                    jobs.append((mk, ri, inc))
    print(f"{len(jobs)} calls to make ({len(incidents)} incidents x {len(model_keys)} models "
          f"x {args.runs} runs, minus resumed)")

    ucsv = open(usage_path, "a", newline="", encoding="utf-8")
    uw = csv.writer(ucsv)
    if new_usage_file:
        uw.writerow(["ts", "condition", "model", "run", "sample_id",
                     "prompt_tokens", "completion_tokens", "cost_usd"])

    def work(job):
        mk, ri, inc = job
        obj, usage = classify_one(key, MODELS[mk], instruction, inc, cond == "decomposed")
        with _lock:
            tag = f"{cond}_{mk}_run{ri}_{args.split}"
            with open(os.path.join(raw_dir, tag + ".jsonl"), "a", encoding="utf-8") as f:
                f.write(json.dumps(obj, ensure_ascii=False) + "\n")
            uw.writerow([int(time.time()), cond, mk, ri, inc["sample_id"],
                         usage.get("prompt_tokens", ""), usage.get("completion_tokens", ""),
                         usage.get("cost", "")])
            ucsv.flush()
            if obj["risk_tier"] in VALID:
                partials[(mk, ri)][inc["sample_id"]] = obj
        return mk, ri, obj["risk_tier"]

    n_err = 0
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futures = [ex.submit(work, j) for j in jobs]
        for i, fut in enumerate(as_completed(futures), 1):
            mk, ri, tier = fut.result()
            if tier == "ERROR":
                n_err += 1
            if i % 25 == 0 or i == len(jobs):
                print(f"  {i}/{len(jobs)} done ({n_err} errors)")
    ucsv.close()

    # finalize arrays for the collector (04_collect_results.py)
    want = {inc["sample_id"] for inc in incidents}
    for (mk, ri), done in partials.items():
        tag = f"{cond}_{mk}_run{ri}_{args.split}"
        arr = [done[sid] for sid in sorted(done) if sid in want]
        with open(os.path.join(raw_dir, tag + ".json"), "w", encoding="utf-8") as f:
            json.dump(arr, f, indent=1, ensure_ascii=False)
        missing = want - set(done)
        status = "COMPLETE" if not missing else f"missing {len(missing)}: {sorted(missing)[:5]}"
        print(f"{tag}.json: {len(arr)} results — {status}")


def report():
    p = os.path.join(ROOT, "analysis", "results", "usage_log.csv")
    if not os.path.exists(p):
        print("no usage yet")
        return
    df = pd.read_csv(p)
    df["cost_usd"] = pd.to_numeric(df["cost_usd"], errors="coerce")
    g = df.groupby(["condition", "model"]).agg(
        calls=("sample_id", "count"),
        ptok=("prompt_tokens", "sum"),
        ctok=("completion_tokens", "sum"),
        usd=("cost_usd", "sum"))
    print(g.to_string())
    print(f"\nTOTAL SPEND: ${df['cost_usd'].sum():.2f}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["probe", "run", "report"])
    ap.add_argument("--condition", default="naive", choices=["naive", "decomposed"])
    ap.add_argument("--split", default="dev", choices=["dev", "heldout", "all"])
    ap.add_argument("--models", default="all")
    ap.add_argument("--runs", type=int, default=1)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--workers", type=int, default=6)
    a = ap.parse_args()
    if a.mode == "probe":
        probe()
    elif a.mode == "report":
        report()
    else:
        run(a)
