"""Offline verification of the distributable archive; no credentials or API calls.

Verifies file hashes, original metrics and follow-up estimates from published
parsed cell labels. Raw provider-envelope parsing/charging is a separate private
audit, not reproducible from this deliberately minimised companion.
"""
from pathlib import Path
import csv
import hashlib
import json
import sys
import numpy as np

ROOT=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path(__file__).resolve().parents[2]
R=ROOT/'research'
assert R.is_dir(), 'Give the extracted companion root as the argument.'
manifest=json.loads((ROOT/'MANIFEST.sha256.json').read_text(encoding='utf-8'))
for name,value in manifest.items():
    assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==value,name
def csvrows(path):
    with path.open(encoding='utf-8-sig',newline='') as f: return list(csv.DictReader(f))
LABELS=['minimal','transparency','high','prohibited','not_ai_system','insufficient_information']
idx={x:i for i,x in enumerate(LABELS+['__missing__'])}
excluded={x['sample_id'] for x in csvrows(R/'inputs/rubric_dev_exclusions.csv')}
expert={x['sample_id']:x for x in csvrows(R/'inputs/expert_labels.csv') if x['sample_id'] not in excluded}
runs=[x for x in csvrows(R/'inputs/model_outputs.csv') if x['sample_id'] in expert and x['run']=='1' and x['pilot'].lower()=='false']
lookup={(x['sample_id'],x['condition'],x['model']):x['risk_tier'] for x in runs}
assert len(expert)==144 and len(runs)==len(lookup)==4030
verified=0
for metric in csvrows(R/'results/full144_metrics.csv'):
    matrix=np.zeros((6,7),dtype=float)
    for sid,e in expert.items(): matrix[idx[e['FINAL_risk_tier']],idx[lookup.get((sid,metric['condition'],metric['model']),'__missing__')]]+=1
    exact=np.trace(matrix[:,:6])/144
    den=matrix.sum(axis=1)+matrix[:,:6].sum(axis=0)
    f1=np.divide(2*matrix[:,:6].diagonal(),den,out=np.zeros(6),where=den>0).mean()
    m=matrix[:4,:4]; expected=np.outer(m.sum(axis=1),m.sum(axis=0))/m.sum()
    loss=(np.arange(4)[:,None]-np.arange(4)[None,:])**2
    qwk=1-(loss*m).sum()/(loss*expected).sum()
    assert np.allclose([exact,f1,qwk],[float(metric[k]) for k in ['exact','macro_f1','qwk']],atol=1e-12,rtol=0)
    verified+=1
assert verified==28
cells=csvrows(R/'results/followup/cells.csv')
summary=json.loads((R/'results/followup/summary.json').read_text(encoding='utf-8'))
assert len(cells)==784 and len({x['request_id'] for x in cells})==784
assert sum(x['prediction']!='__missing__' for x in cells)==750
ids=sorted({x['sample_id'] for x in cells}); models=sorted({x['model'] for x in cells})
assert len(ids)==len(models)==14
ref=np.array([expert[sid]['FINAL_risk_tier'] for sid in ids])
cellmap={(x['sample_id'],x['model'],x['prompt'],x['evidence']):x['prediction'] for x in cells}
w=np.vstack([np.ones(14),np.random.default_rng(20260922).multinomial(14,np.full(14,1/14),size=10000)])

def distributions(p,mask):
    # Weighted contingency tables, independently of the original moment formula.
    matrix=np.zeros((len(w),6,7),dtype=float)
    for a in LABELS:
        for b in LABELS+['__missing__']:
            matrix[:,idx[a],idx[b]]=w@((ref==a)&(p==b)&mask).astype(float)
    n=matrix.sum(axis=(1,2))
    diag=matrix[:,:,:6].diagonal(axis1=1,axis2=2)
    exact=np.divide(diag.sum(axis=1),n,out=np.full(len(w),np.nan),where=n>0)
    den=matrix.sum(axis=2)+matrix[:,:,:6].sum(axis=1)
    f1=np.divide(2*diag,den,out=np.zeros_like(den),where=den>0).mean(axis=1); f1[n==0]=np.nan
    small=matrix[:,:4,:4]; ns=small.sum(axis=(1,2))
    with np.errstate(divide='ignore',invalid='ignore'):
        expected=small.sum(axis=2)[:,:,None]*small.sum(axis=1)[:,None,:]/ns[:,None,None]
        loss=(np.arange(4)[:,None]-np.arange(4)[None,:])**2
        expected_loss=(expected*loss).sum(axis=(1,2))
        qwk=1-(small*loss).sum(axis=(1,2))/expected_loss
    qwk[(ns==0)|(expected_loss<=0)|~np.isfinite(qwk)]=np.nan
    return {'exact':exact,'macro_f1':f1,'qwk':qwk}
def compare(values,expected):
    assert abs(values[0]-expected['value'])<1e-12
    finite=values[1:][np.isfinite(values[1:])]
    assert len(finite)==expected['defined_bootstrap_draws']
    assert np.allclose(np.percentile(finite,[2.5,97.5]),expected['ci95'],atol=1e-12,rtol=0)
for prompt in ['naive','decomposed']:
    regular={ev:{k:[] for k in ['exact','macro_f1','qwk']} for ev in ['short','expanded']}
    paired={k:[] for k in ['exact','macro_f1','qwk']}; pairs=0
    for model in models:
        pp={ev:np.array([cellmap[sid,model,prompt,ev] for sid in ids]) for ev in regular}
        mask=(pp['short']!='__missing__')&(pp['expanded']!='__missing__'); pairs+=int(mask.sum())
        for ev in regular:
            d=distributions(pp[ev],np.ones(14,dtype=bool))
            for k in d: regular[ev][k].append(d[k])
        # Paired QWK additionally holds the ordinal-scoring mask common.
        a=distributions(pp['short'],mask); b=distributions(pp['expanded'],mask)
        ordinal=mask&np.isin(ref,LABELS[:4])&np.isin(pp['short'],LABELS[:4])&np.isin(pp['expanded'],LABELS[:4])
        a['qwk']=distributions(pp['short'],ordinal)['qwk']; b['qwk']=distributions(pp['expanded'],ordinal)['qwk']
        for k in paired: paired[k].append(b[k]-a[k])
    means={ev:{k:np.mean(v,axis=0) for k,v in ds.items()} for ev,ds in regular.items()}
    for ev in means:
        for k,v in means[ev].items(): compare(v,summary['panel'][prompt+'_'+ev][k])
    target=summary['expanded_minus_short'][prompt]
    assert pairs==target['common_valid_pairs']
    for k,values in paired.items(): compare(np.mean(values,axis=0),target['common_'+k+'_delta'])
    compare(means['expanded']['exact']-means['short']['exact'],target['intended_exact_delta'])
print(json.dumps({'manifest_files_verified':len(manifest),'original_model_prompt_combinations':verified,
                  'followup_cells':len(cells),'valid_followup_answers':750,
                  'followup_verification':'All exact/F1/QWK panel estimates and intervals and paired changes reproduced from parsed cells',
                  'new_model_calls':0},indent=2))
