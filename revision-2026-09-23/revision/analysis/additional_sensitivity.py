"""Offline partition checks on unchanged archived labels and model answers.

These post-hoc checks do not turn the legacy split into a prospectively frozen
test set. No models are called and no expert label is changed.
"""
from pathlib import Path
import csv
import hashlib
import json
import re
import numpy as np

G = Path(__file__).resolve().parents[1]
B = G.parent / 'revision-2026-09-22'
if not B.is_dir():
    B = G.parent / 'research'
LABELS = ['minimal','transparency','high','prohibited','not_ai_system','insufficient_information']
ORD = {x:i for i,x in enumerate(LABELS[:4])}
def read(name):
    with (B/'inputs'/name).open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))
excluded = {x['sample_id'] for x in read('rubric_dev_exclusions.csv')}
expert = sorted([x for x in read('expert_labels.csv') if x['sample_id'] not in excluded], key=lambda x:x['sample_id'])
rows = [x for x in read('model_outputs.csv') if x['run']=='1' and x['pilot'].lower()=='false' and x['sample_id'] not in excluded]
models = sorted({x['model'] for x in rows})
lookup = {(x['sample_id'],x['condition'],x['model']):x['risk_tier'] for x in rows}
assert len(rows)==4030 and len(lookup)==4030 and len(models)==14 and len(expert)==144

def describe(a):
    finite = a[1:][np.isfinite(a[1:])]
    return {'estimate':float(a[0]), 'ci95':np.percentile(finite,[2.5,97.5]).tolist(), 'finite_draws':len(finite)}

def matrix_f1(reference,predictions):
    labs=LABELS+['__missing__']; idx={v:i for i,v in enumerate(labs)}
    matrix=np.zeros((7,7),dtype=float)
    for a,b in zip(reference,predictions): matrix[idx[a],idx[b]]+=1
    den=matrix.sum(axis=0)+matrix.sum(axis=1)
    return np.divide(2*matrix.diagonal(),den,out=np.zeros(7),where=den>0)[:6].mean()

def matrix_qwk(reference,predictions):
    matrix=np.zeros((4,4),dtype=float)
    for a,b in zip(reference,predictions): matrix[int(a),int(b)]+=1
    expected=np.outer(matrix.sum(axis=1),matrix.sum(axis=0))/matrix.sum()
    loss=(np.arange(4)[:,None]-np.arange(4)[None,:])**2
    return 1-(loss*matrix).sum()/(loss*expected).sum()

def analyse(records):
    n = len(records)
    ref = np.array([x['FINAL_risk_tier'] for x in records])
    y = np.array([ORD.get(x,np.nan) for x in ref])
    w = np.vstack([np.ones(n),np.random.default_rng(20260916).multinomial(n,np.full(n,1/n),size=10000)]).astype(float)
    def qwk(p,mask):
        a,b = np.where(mask,y,0),np.where(mask,p,0)
        count = w@mask.astype(float)
        with np.errstate(divide='ignore',invalid='ignore'):
            expected = (w@(a*a+b*b))/count-2*(w@a/count)*(w@b/count)
            return 1-(w@((a-b)**2)/count)/expected
    panel = {c:{k:[] for k in ['exact','macro_f1','qwk']} for c in ['naive','decomposed']}
    common_deltas=[]
    for model in models:
        ps=[]
        for condition in panel:
            p=np.array([lookup.get((r['sample_id'],condition,model),'__missing__') for r in records])
            exact=w@(ref==p).astype(float)/n
            fs=[]
            for label in LABELS:
                tp=w@((ref==label)&(p==label)).astype(float)
                denom=w@(ref==label).astype(float)+w@(p==label).astype(float)
                fs.append(np.divide(2*tp,denom,out=np.zeros_like(denom),where=denom>0))
            f1=np.mean(fs,axis=0)
            ordinal=np.array([ORD.get(x,np.nan) for x in p]); ps.append(ordinal)
            mask=np.isfinite(y)&np.isfinite(ordinal)
            k=qwk(ordinal,mask)
            assert abs(f1[0]-matrix_f1(ref,p))<1e-12
            assert abs(k[0]-matrix_qwk(y[mask],ordinal[mask]))<1e-12
            for name,v in [('exact',exact),('macro_f1',f1),('qwk',k)]: panel[condition][name].append(v)
        common=np.isfinite(y)&np.isfinite(ps[0])&np.isfinite(ps[1])
        common_deltas.append(qwk(ps[1],common)-qwk(ps[0],common))
    means={c:{k:np.mean(v,axis=0) for k,v in group.items()} for c,group in panel.items()}
    result={'n':n,'ids':[x['sample_id'] for x in records], 'class_counts':{lab:int((ref==lab).sum()) for lab in LABELS},
            'conditions':{c:{k:describe(v) for k,v in group.items()} for c,group in means.items()}}
    result['paired_changes']={k:describe(means['decomposed'][k]-means['naive'][k]) for k in ['exact','macro_f1']}
    result['paired_changes']['qwk']=describe(np.mean(common_deltas,axis=0))
    return result

groups={'full144':expert,'legacy_heldout102':[x for x in expert if x['split']=='heldout'],
        'legacy_heldout_same_record':[x for x in expert if x['split']=='heldout' and x['consulted_full_page']!='yes']}
assert len(groups['legacy_heldout102'])==102
intimate={'S035','S063','S064','S076','S077','S149'}
# Broad, descriptive flag: all historical product-positive records, both
# industrial robots, hotel robots, crash-detection device and medical model.
# A flag is not a finding that a new legal provision changes the final label.
product={x['sample_id'] for x in expert if x['L3_annex_i_product']=='yes'}|{'S001','S029','S040','S058','S110'}
assert len(product)==20 and len(intimate)==6 and not intimate&product
groups['excluding_intimate_material']=[x for x in expert if x['sample_id'] not in intimate]
groups['excluding_version_sensitive_flags']=[x for x in expert if x['sample_id'] not in intimate|product]
records_by_id={x['sample_id']:x for x in read('sample_v1_frozen.csv')}
fraud_flags={x['sample_id'] for x in expert if x['FINAL_risk_tier']=='transparency' and
             re.search(r'scam|fraud|phish',records_by_id[x['sample_id']]['title']+' '+records_by_id[x['sample_id']]['description'],re.I)}
assert len(fraud_flags)==22
groups['excluding_flagged_transparency_fraud']=[x for x in expert if x['sample_id'] not in fraud_flags]
results={name:analyse(records) for name,records in groups.items()}
baseline=json.loads((B/'results/summary.json').read_text(encoding='utf-8'))['full144']
for metric in ['exact','macro_f1']:
    assert abs(results['full144']['paired_changes'][metric]['estimate']-baseline['delta_'+metric]['value'])<1e-12
    assert np.allclose(results['full144']['paired_changes'][metric]['ci95'],baseline['delta_'+metric]['ci'],atol=1e-12)
out={'analysis':'Post-hoc legacy-partition sensitivity with fixed historical expert labels', 'bootstrap':{'unit':'incident shared across models and prompts','draws':10000,'seed':20260916},
     'limitations':'The legacy heldout designation predates later annotation revisions; this is not a newly established untouched test set. These selected sensitivity checks do not support additional confirmatory significance claims.',
     'input_sha256':{name:hashlib.sha256((B/'inputs'/name).read_bytes()).hexdigest() for name in ['expert_labels.csv','model_outputs.csv','rubric_dev_exclusions.csv']},
     'version_flags':{'intimate_material':sorted(intimate),'product_related':sorted(product),'status':'Assistant-defined broad diagnostic flags; not author-adjudicated amended-law labels'},
     'reference_family_flags':{'ids':sorted(fraud_flags),'rule':'Historical transparency label and case-insensitive scam|fraud|phish in original title or description',
                               'status':'Broad automated screen, not a legal finding or an exhaustive Article 5 audit'},
     'independent_point_checks':'Macro-F1 and QWK independently matched contingency-matrix implementations for every model, condition and subset.', 'subsets':results}
(G/'results/additional-sensitivity.json').write_text(json.dumps(out,indent=2,allow_nan=False),encoding='utf-8')
lines=['## S13. Additional checks on the archived evaluation','',
       'These post-hoc analyses keep the original labels and model answers. They exclude the 42 records bearing the legacy development designation, then additionally exclude records for which the expert consulted extra sources. The remaining split is not a newly established untouched test set: rubric development and annotation history remain as described in S3. No additional model calls were made.','',
       'Each interval uses 10,000 shared incident resamples (seed 20260916), keeping the fixed model panel and prompt pairs together. Macro-F1 always uses the same six classes, with zero for an undefined class F1. QWK differences use common scorable records.','',
       '| Sample | n | Exact agreement B/S | Paired change, pp [95% interval] | Macro-F1 B/S | Paired F1 change [95% interval] | Paired QWK change [95% interval] |',
       '|---|---:|---|---|---|---|---|']
for name,r in results.items():
    a,b=r['conditions']['naive'],r['conditions']['decomposed']
    def delta(metric,scale=1,decimals=3):
        d=r['paired_changes'][metric]; return f"{scale*d['estimate']:.{decimals}f} [{scale*d['ci95'][0]:.{decimals}f}, {scale*d['ci95'][1]:.{decimals}f}]"
    lines.append(f"| {name} | {r['n']} | {100*a['exact']['estimate']:.2f}/{100*b['exact']['estimate']:.2f} | {delta('exact',100,2)} | {a['macro_f1']['estimate']:.3f}/{b['macro_f1']['estimate']:.3f} | {delta('macro_f1')} | {delta('qwk')} |")
lines+=['','The saved JSON includes every subset ID and class count. Separate contingency-matrix implementations reproduced all model-level F1 and QWK point estimates. The full-sample results and intervals match the earlier analysis exactly. The sensitivities describe this archive and do not repair the prompt, legal-version or single-reference limitations.']
lines+=['','### Legal-version diagnostic','',
        'The intimate-material flag covers six records: '+', '.join(sorted(intimate))+'. The broader flag also covers 20 product-related records: '+', '.join(sorted(product))+'. These include all 15 historical product-positive automated-driving records and five records concerning industrial robots, hotel robots, a crash-detection device or a medical model. The flag is deliberately broad; it does not assert that an amended provision changes every label. S033 (identifying abuse victims) and S061 (a later assault following facial misidentification) are not synthetic-intimate-material cases.','',
        'The flags were selected from record content and statutory subject matter after the original study. The amended text adds intimate-material provisions and changes the safety-component/product framework. The new intimate-material prohibitions apply from 2 December 2026, distinct from the amendment’s entry into force. Since the historical checklist instructed models to ignore temporal scope while also saying “today”, neither subset becomes a controlled comparison of legal versions. The screen is not an exhaustive audit of every amendment. No relabelling or attribution of individual disagreements to legal-version choice is claimed.','',
        'Source: [Regulation (EU) 2026/1744, Article 1(4), (7), (40) and (41)](https://eur-lex.europa.eu/eli/reg/2026/1744/oj), checked 22 September 2026.']
lines+=['','### Related reference-family check','',
        'A separate, reproducible screen excludes all 22 historically transparency-labelled records whose original title or description contains scam, fraud or phish (case-insensitive): '+', '.join(sorted(fraud_flags))+'. This broad check tests whether the exact-agreement result depends entirely on that reference family. It is not a corrected-label score or a finding that every excluded case is prohibited. It includes some cases, such as manipulation of software rather than a person, that may remain transparency. It can miss related cases without these words and does not replace an element-by-element legal review.']
(G/'review/additional-sensitivity.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('\n'.join(x for x in lines if x.startswith('|')))

# Exact per-value rule support prevents all-negative agreement from being read
# as competence on the rare positive/applicable branch.
with (B/'results/step_comparisons.csv').open(encoding='utf-8-sig',newline='') as f:
    steps=list(csv.DictReader(f))
support=[]; confusion=[]
for rule in sorted({x['step'] for x in steps}):
    rr=[x for x in steps if x['step']==rule]
    assert len(rr)==2016
    for value in sorted({x['reference'] for x in rr}):
        vv=[x for x in rr if x['reference']==value]
        matches=sum(x['match'].lower()=='true' for x in vv)
        support.append({'rule':rule,'reference_value':value,'incidents':len({x['sample_id'] for x in vv}),
                        'pairs':len(vv),'matches':matches,'agreement':matches/len(vv)})
        for predicted in sorted({x['prediction'] or '__missing__' for x in vv}):
            confusion.append({'rule':rule,'reference_value':value,'prediction':predicted,
                              'count':sum((x['prediction'] or '__missing__')==predicted for x in vv)})
for name,rs in [('rule-reference-support.csv',support),('rule-value-confusions.csv',confusion)]:
    with (G/'results'/name).open('w',encoding='utf-8',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rs[0])); writer.writeheader(); writer.writerows(rs)
rule_lines=['## S14. Rule agreement by reference value','',
            'These descriptive checklist comparisons use the historical six rule fields. They are literal field matches, not independent judgments of legal correctness. Each incident contributes fourteen model answers; therefore the pairs are not independent observations. Negatives, unclear, missing and not-applicable values are shown separately. No basic-prompt rule answers are inferred from its short explanations.','',
            '| Rule | Reference value | Incidents | Matched / model–incident pairs | Agreement |','|---|---|---:|---:|---:|']
for r in support: rule_lines.append(f"| {r['rule']} | {r['reference_value']} | {r['incidents']} | {r['matches']} / {r['pairs']} | {100*r['agreement']:.1f}% |")
rule_lines+=['','All 15 positive product-route records belong to the automated-driving family. High agreement on the full product question therefore does not demonstrate broad positive-route coverage. `results/rule-value-confusions.csv` includes every observed reference/predicted-value combination.']
(G/'review/rule-support.md').write_text('\n'.join(rule_lines)+'\n',encoding='utf-8')

gains=[]
for model in models:
    exact={c:sum(lookup.get((r['sample_id'],c,model))==r['FINAL_risk_tier'] for r in expert)/144 for c in ['naive','decomposed']}
    gains.append({'model':model,'change_pp':100*(exact['decomposed']-exact['naive'])})
values=np.array([x['change_pp'] for x in gains]); largest=int(values.argmax())
heterogeneity={'individual_gains':gains,'mean_pp':float(values.mean()),'median_pp':float(np.median(values)),
    'positive_models':int((values>0).sum()),'negative_models':int((values<0).sum()),'unchanged_models':int((values==0).sum()),
    'largest_gain':gains[largest],'largest_share_of_sum':float(values[largest]/values.sum()),
    'leave_one_model_out_mean_range_pp':[float(np.min([(values.sum()-v)/13 for v in values])),float(np.max([(values.sum()-v)/13 for v in values]))],
    'interpretation':'Descriptive fixed-panel heterogeneity; not a model-population confidence interval or a reason to remove any model.'}
(G/'results/model-gain-heterogeneity.json').write_text(json.dumps(heterogeneity,indent=2),encoding='utf-8')
print('Rule-value breakdown saved. Model-gain heterogeneity:',json.dumps(heterogeneity))
