"""Offline revision analyses. No network, API key or model invocation.

Frozen inputs are copied from the submitted experiment. Missing predictions count
as nominal nonmatches; ordinal comparisons use explicit complete-case masks.
Bootstrap unit = incident; both prompts and the fixed model panel stay together.
"""
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]/'.deps'))
import ast
import hashlib
import json
import re
import warnings
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT.parents[1]
INP, OUT = ROOT/'inputs', ROOT/'results'
PAPER = ROOT/'paper'
SEED, B = 20260916, 10000
LABELS = ['minimal','transparency','high','prohibited','not_ai_system','insufficient_information']
ORD = {x:i for i,x in enumerate(LABELS[:4])}
NAMES = {'sonnet46':'Claude Sonnet 4.6','gpt52':'GPT-5.2','gemini3f':'Gemini 3 Flash',
 'gemma27b':'Gemma 3 27B','kimi25':'Kimi K2.5','haiku45':'Claude Haiku 4.5',
 'sonnet5':'Claude Sonnet 5','gemini37f':'Gemini 3.7 Flash','kimi3':'Kimi K3',
 'qwen38max':'Qwen 3.8 Max','qwen3827b':'Qwen 3.8 27B','gpt56sol':'GPT-5.6 Sol',
 'gpt56luna':'GPT-5.6 Luna','grok46':'Grok 4.6'}

def write_json(name, x):
    (OUT/name).write_text(json.dumps(x,indent=2,allow_nan=False),encoding='utf-8')

def ci(x):
    return np.nanpercentile(x,[2.5,97.5]).tolist()

def qwk(a,b,w):
    good=np.isfinite(a)&np.isfinite(b)
    n=w@good.astype(float)
    aa=np.where(good,a,0);bb=np.where(good,b,0)
    den=w@(aa*aa+bb*bb)/n-2*(w@aa/n)*(w@bb/n)
    with np.errstate(invalid='ignore',divide='ignore'):
        return 1-(w@((aa-bb)**2)/n)/den

def nominal(a,b,w):
    exact=w@(a==b).astype(float)/w.sum(axis=1)
    fs=[]
    for lab in LABELS:
        tp=w@((a==lab)&(b==lab)).astype(float)
        d=w@(a==lab).astype(float)+w@(b==lab).astype(float)
        fs.append(np.divide(2*tp,d,out=np.zeros_like(d),where=d>0))
    return exact,np.array(fs).mean(axis=0)

exp_all=pd.read_csv(INP/'expert_labels.csv').fillna('')
sample=pd.read_csv(INP/'sample_v1_frozen.csv').fillna('')
excluded=pd.read_csv(INP/'rubric_dev_exclusions.csv')
exp=exp_all[~exp_all.sample_id.isin(excluded.sample_id)].copy().sort_values('sample_id')
assert len(exp)==144 and exp.sample_id.is_unique
raw=pd.read_csv(INP/'model_outputs.csv').fillna('')
assert raw.pilot.isin([False,True]).all()
runs=raw[(raw.pilot==False)&(raw.run==1)&raw.sample_id.isin(exp.sample_id)].copy()
assert not runs.duplicated(['sample_id','condition','model']).any()
models=sorted(runs.model.unique())
assert len(models)==14 and len(runs)==4030
extra=exp[exp.consulted_full_page.eq('yes')].sample_id.tolist()
assert len(extra)==14
driving=exp[(exp.L3_annex_i_product=='yes') & exp.title.str.contains('Tesla|Uber|Autopilot|self-driving|autonomous|Cruise|Waymo|XPeng',case=False)].sample_id.tolist()
assert len(driving)==15
print('Driving candidates:',driving,flush=True)
exp[exp.sample_id.isin(driving)].to_csv(OUT/'automated_driving_exclusions.csv',index=False)
exp[exp.sample_id.isin(extra)].to_csv(OUT/'extra_evidence_exclusions.csv',index=False)

def analyse(name, e):
    ids=e.sample_id.tolist(); n=len(ids)
    w=np.vstack([np.ones(n),np.random.default_rng(SEED).multinomial(n,np.full(n,1/n),size=B)]).astype(float)
    ref=e.FINAL_risk_tier.to_numpy()
    er=np.array([ORD.get(x,np.nan) for x in ref])
    pred={c:runs[runs.condition.eq(c)].pivot(index='sample_id',columns='model',values='risk_tier').reindex(index=ids,columns=models).fillna('__missing__').to_numpy() for c in ['naive','decomposed']}
    table=[];panel={c:{'exact':[],'macro_f1':[],'qwk':[]} for c in pred}
    paired=[];classes=[];conf=[]
    for j,m in enumerate(models):
        pa=[]
        for c in pred:
            p=pred[c][:,j];pord=np.array([ORD.get(x,np.nan) for x in p]);pa.append(pord)
            acc,f=nominal(ref,p,w); k=qwk(er,pord,w)
            for metric,v in [('exact',acc),('macro_f1',f),('qwk',k)]:panel[c][metric].append(v)
            table.append(dict(model=m,name=NAMES[m],condition=c,n=n,answered=int((p!='__missing__').sum()),auxiliary=int(np.isin(p,LABELS[4:]).sum()),n_ordinal=int((np.isfinite(er)&np.isfinite(pord)).sum()),exact=float(acc[0]),exact_lo=ci(acc[1:])[0],exact_hi=ci(acc[1:])[1],macro_f1=float(f[0]),f1_lo=ci(f[1:])[0],f1_hi=ci(f[1:])[1],qwk=float(k[0]),qwk_lo=ci(k[1:])[0],qwk_hi=ci(k[1:])[1]))
            for lab in LABELS:
                tp=int(((ref==lab)&(p==lab)).sum());support=int((ref==lab).sum());npred=int((p==lab).sum())
                classes.append(dict(model=m,condition=c,label=lab,support=support,predicted=npred,tp=tp,precision=tp/npred if npred else 0.,recall=tp/support if support else 0.,f1=2*tp/(npred+support) if npred+support else 0.))
            for a in LABELS:
                for b in LABELS+['__missing__']:
                    conf.append(dict(model=m,condition=c,reference=a,prediction=b,count=int(((ref==a)&(p==b)).sum())))
        common=np.isfinite(er)&np.isfinite(pa[0])&np.isfinite(pa[1])
        aa=np.where(common,er,np.nan)
        k0=qwk(aa,pa[0],w);k1=qwk(aa,pa[1],w);dk=k1-k0;paired.append(dk)
        table[-2].update(common_n=int(common.sum()),paired_qwk=float(k0[0]),delta_qwk=float(dk[0]),delta_lo=ci(dk[1:])[0],delta_hi=ci(dk[1:])[1])
        table[-1].update(common_n=int(common.sum()),paired_qwk=float(k1[0]),delta_qwk=float(dk[0]),delta_lo=ci(dk[1:])[0],delta_hi=ci(dk[1:])[1])
    summary={'n':n,'class_counts':e.FINAL_risk_tier.value_counts().to_dict(),'majority_label':'transparency','majority_exact':float((ref=='transparency').mean()),'majority_macro_f1':float(nominal(ref,np.full(n,'transparency'),w[:1])[1][0])}
    for c in pred:
        summary[c]={}
        for metric in panel[c]:
            v=np.mean(panel[c][metric],axis=0);summary[c][metric]={'value':float(v[0]),'ci':ci(v[1:])}
    for metric in ['exact','macro_f1']:
        dv=np.mean(panel['decomposed'][metric],axis=0)-np.mean(panel['naive'][metric],axis=0)
        summary['delta_'+metric]={'value':float(dv[0]),'ci':ci(dv[1:])}
    dk=np.mean(paired,axis=0);summary['delta_paired_qwk']={'value':float(dk[0]),'ci':ci(dk[1:])}
    directions=[]
    groups={'outside':e.L2_annex_iii_domain.eq('none').to_numpy(),'inside':~e.L2_annex_iii_domain.isin(['none','unclear']).to_numpy(),'unclear':e.L2_annex_iii_domain.eq('unclear').to_numpy()}
    for c in pred:
        pr=np.array([[ORD.get(x,np.nan) for x in row] for row in pred[c]])
        delta=pr-er[:,None]
        for g,mask in groups.items():
            good=np.isfinite(delta)&mask[:,None]; totals=good.sum(axis=1);sums=np.where(good,delta,0).sum(axis=1)
            if not totals.sum():continue
            with np.errstate(invalid='ignore',divide='ignore'):dv=(w@sums)/(w@totals)
            directions.append(dict(condition=c,group=g,incidents=int(mask.sum()),pairs=int(good.sum()),mean=float(dv[0]),lo=ci(dv[1:])[0],hi=ci(dv[1:])[1],up_pct=float(100*((delta>0)&good).sum()/good.sum()),down_pct=float(100*((delta<0)&good).sum()/good.sum())))
        for lab in LABELS[:4]:
            mask=ref==lab; good=np.isfinite(delta)&mask[:,None]
            if not good.any():continue
            directions.append(dict(condition=c,group='reference_'+lab,incidents=int(mask.sum()),pairs=int(good.sum()),mean=float(delta[good].mean()),lo=None,hi=None,up_pct=float(100*((delta>0)&good).sum()/good.sum()),down_pct=float(100*((delta<0)&good).sum()/good.sum())))
    summary['direction']=directions
    pd.DataFrame(table).to_csv(OUT/f'{name}_metrics.csv',index=False)
    pd.DataFrame(classes).to_csv(OUT/f'{name}_class_metrics.csv',index=False)
    pd.DataFrame(conf).to_csv(OUT/f'{name}_confusions.csv',index=False)
    pd.DataFrame(directions).to_csv(OUT/f'{name}_direction.csv',index=False)
    print(name,json.dumps(summary),flush=True)
    return summary,pd.DataFrame(table),pred

full,metrics,preds=analyse('full144',exp)
equal,_,_=analyse('same130',exp[~exp.sample_id.isin(extra)])
nodrive,_,_=analyse('no_driving',exp[~exp.sample_id.isin(driving)])
corr=pd.read_csv(INP/'label_corrections.csv')
changed=corr[(corr.field=='FINAL_risk_tier')&(corr['from']=='prohibited')&(corr.to=='transparency')].sample_id.tolist()
assert len(changed)==8
alternate=exp.copy();alternate.loc[alternate.sample_id.isin(changed),'FINAL_risk_tier']='prohibited'
history,hm,_=analyse('historical8',alternate)
corr[corr.sample_id.isin(changed)].to_csv(OUT/'historical8_definition.csv',index=False)

# Step comparisons describe recorded outputs; they are not independent legal reviews.
stepmap=[('art5','L1_art5_prohibited'),('annex_i','L3_annex_i_product'),('annex_iii','L2_annex_iii_domain'),('derogation','L4_art6_3_derogation'),('profiling','L5_profiling_override'),('art50','L6_art50_transparency')]
joined=runs.merge(exp,on='sample_id',suffixes=('','_expert'))
step_rows=[];first_rows=[]
for m,g in joined[joined.condition.eq('decomposed')].groupby('model'):
    first_count={x:0 for x,_ in stepmap};first_count.update(no_recorded_mismatch=0,missing_step=0)
    for _,r in g.iterrows():
        s=json.loads(r.steps) if r.steps else {};first=None
        for k,col in stepmap:
            got=str(s.get(k,''));want=str(r[col]);missing=not got
            step_rows.append(dict(model=m,sample_id=r.sample_id,step=k,reference=want,prediction=got,missing=missing,match=(got==want and not missing),final_match=r.risk_tier==r.FINAL_risk_tier))
            if first is None and (missing or got!=want):first='missing_step' if missing else k
        first_count[first or 'no_recorded_mismatch']+=1
        first_rows.append(dict(model=m,sample_id=r.sample_id,first_recorded_mismatch=first or 'none',final_match=r.risk_tier==r.FINAL_risk_tier))
steps=pd.DataFrame(step_rows);steps.to_csv(OUT/'step_comparisons.csv',index=False)
steps.groupby(['model','step']).agg(n=('match','size'),matches=('match','sum'),missing=('missing','sum')).reset_index().to_csv(OUT/'step_agreement_by_model.csv',index=False)
pd.DataFrame(first_rows).to_csv(OUT/'first_recorded_mismatch.csv',index=False)
steps.groupby('step').agg(n=('match','size'),matches=('match','sum'),missing=('missing','sum')).reset_index().to_csv(OUT/'step_agreement_panel.csv',index=False)

# Fixed stratified review sample: up to three greatest-disagreement cases per
# reference class plus one best-agreement control per class. Ties by sample ID.
case=exp[['sample_id','title','FINAL_risk_tier','confidence_1to3','notes']].copy()
ref=exp.FINAL_risk_tier.to_numpy()
case['disagreements']=sum((p!=ref[:,None]).sum(axis=1) for p in preds.values())
chosen=[]
for lab,g in case.groupby('FINAL_risk_tier',sort=True):
    errors=g[g.disagreements>0].sort_values(['disagreements','sample_id'],ascending=[False,True]).head(3)
    chosen.extend([(sid,'disagreement') for sid in errors.sample_id])
    controls=g[~g.sample_id.isin(errors.sample_id)].sort_values(['disagreements','sample_id']).head(1)
    chosen.extend([(sid,'agreement_control' if int(controls.iloc[0].disagreements)==0 else 'lowest_disagreement_control') for sid in controls.sample_id])
selection=pd.DataFrame(chosen,columns=['sample_id','selection_role']).merge(case,on='sample_id')
review_fields={'author_review_status':'pending','author_error_code':'','author_reason':'','author_name':'','reviewed_at':'','reference_decision':''}
for k,v in review_fields.items():selection[k]=v
review_path=ROOT/'review/author_review_sample.csv'
if review_path.exists():
    prior=pd.read_csv(review_path).fillna('').set_index('sample_id')
    for i,row in selection.iterrows():
        if row.sample_id in prior.index:
            old=prior.loc[row.sample_id]
            if old.get('author_review_status','pending') not in ['','pending']:
                assert old.FINAL_risk_tier==row.FINAL_risk_tier, 'Reference changed for reviewed case; reconcile author review explicitly.'
            for k in review_fields:
                if k in old.index and str(old[k]).strip():selection.at[i,k]=old[k]
selection.to_csv(review_path,index=False)
joined[joined.sample_id.isin(selection.sample_id)].merge(sample[['sample_id','description','aiid_url']],on='sample_id').to_csv(ROOT/'review/author_review_outputs.csv',index=False)
case.to_csv(OUT/'incident_disagreement_counts.csv',index=False)

# Dataset provenance and descriptions from the actual source export.
population=pd.read_excel(INP/'AIID_Excel_Export-20260810.xlsx',sheet_name='Incidents',header=2)
valid=population[population.title.notna()&population.description.notna()]
ev=sample[sample.sample_id.isin(exp.sample_id)]
dataset=dict(export_date='2026-08-10',export_rows=len(population),eligible_rows=len(valid),sample_n=len(sample),evaluation_n=len(exp),seed=2026,legacy_splits=sample.split.value_counts().to_dict(),evaluation_legacy_splits=ev.split.value_counts().to_dict(),year_min=int(ev.year.min()),year_max=int(ev.year.max()),description_median_chars=float(ev.description.str.len().median()),description_min_chars=int(ev.description.str.len().min()),description_max_chars=int(ev.description.str.len().max()),strata=ev.sampling_stratum.value_counts().to_dict(),domains=exp.L2_annex_iii_domain.value_counts().to_dict(),confidence=exp.confidence_1to3.value_counts().to_dict(),correction_fields=len(corr),correction_incidents=int(corr.sample_id.nunique()),driving_ids=driving,extra_evidence_ids=extra,review_selection_n=len(selection))
write_json('dataset.json',dataset)
summary=dict(seed=SEED,resamples=B,full144=full,same130=equal,no_driving=nodrive,historical8=history,dataset=dataset)
write_json('summary.json',summary)

# Check every original point estimate independently against the prior saved table.
orig=pd.read_csv(INP/'agreement_all.csv')
check=metrics.merge(orig[['condition','model','qwk']],on=['condition','model'],suffixes=('_new','_published'))
assert len(check)==28 and ((check.qwk_new-check.qwk_published).abs()<=.00051).all()
assert all(len(p)==144 for p in preds.values())
hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(INP.iterdir()) if p.is_file()}
write_json('input_hashes.json',hashes)

# Compact manuscript table with uncertainty; primary nominal measures beside QWK.
lines=[r'\begin{table}[!ht]',r'\centering',r'\caption{Agreement with the expert legal reference on 144 incidents. B: basic; S: step-by-step. Exact agreement (\%) and six-label macro-F1 include all records. $n_o$: scorable ordinal pairs for QWK; brackets show 95\% incident-bootstrap intervals.}',r'\label{tab:agreement}',r'\setlength{\tabcolsep}{4pt}',r'\small',r'\begin{tabular}{@{}lrrrll@{}}',r'\toprule',r'& Exact B/S & F1 B/S & $n_o$ B/S & QWK B [95\% CI] & QWK S [95\% CI] \\',r'\midrule']
for m in models:
    a=metrics[(metrics.model==m)&(metrics.condition=='naive')].iloc[0];b=metrics[(metrics.model==m)&(metrics.condition=='decomposed')].iloc[0]
    lines.append(f"{NAMES[m]} & {100*a.exact:.1f}/{100*b.exact:.1f} & {a.macro_f1:.2f}/{b.macro_f1:.2f} & {a.n_ordinal}/{b.n_ordinal} & {a.qwk:.2f} [{a.qwk_lo:.2f}, {a.qwk_hi:.2f}] & {b.qwk:.2f} [{b.qwk_lo:.2f}, {b.qwk_hi:.2f}] " + r'\\')
lines += [r'\bottomrule',r'\end{tabular}',r'\end{table}']
# The table spans both columns to preserve readable type.
lines=[x.replace(r'\begin{table}',r'\begin{table*}').replace(r'\end{table}',r'\end{table*}') for x in lines]
(PAPER/'tab_agreement.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')

plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'pdf.fonttype':42})
fig,axes=plt.subplots(1,2,figsize=(7.0,2.15),gridspec_kw={'width_ratios':[1,1]})
ax=axes[0]
for i,c in enumerate(['naive','decomposed']):
    data=[x for x in full['direction'] if x['condition']==c and x['group'] in ['outside','inside']]
    for j,x in enumerate(data):
        y=j+(i-.5)*.18
        ax.errorbar(x['mean'],y,xerr=[[x['mean']-x['lo']],[x['hi']-x['mean']]],fmt='o',capsize=3,color=['#255978','#b05b35'][i],label=['Basic','Step-by-step'][i] if j==0 else None)
ax.axvline(0,color='#999999',lw=.8);ax.set_yticks([0,1],['Outside (109)','Inside (33)']);ax.set_xlabel('Mean signed category difference');ax.invert_yaxis();ax.legend(frameon=False,fontsize=8);ax.set_title('(a) Annex III; unclear kept separate',fontsize=9)
ax=axes[1]
for j,(name,s) in enumerate([('144 records',full),('130 same-record',equal),('Without driving',nodrive),('8 historical labels',history)]):
    x=s['delta_paired_qwk'];v=x['value'];lo,hi=x['ci'];ax.errorbar(v,j,xerr=[[v-lo],[hi-v]],fmt='o',capsize=3,color='#255978')
ax.axvline(0,color='#999999',lw=.8);ax.set_yticks(range(4),['144 records','130 same-record','Without driving','8 historical labels']);ax.invert_yaxis();ax.set_xlabel('Paired panel mean change in QWK');ax.set_title('(b) Sensitivity of prompt comparison',fontsize=9)
for ax in axes:
    ax.spines[['top','right']].set_visible(False)
fig.tight_layout(w_pad=2);fig.savefig(PAPER/'fig_revision.pdf',bbox_inches='tight');plt.close(fig)
print('PASS: all 28 original QWK estimates reproduced; offline outputs complete.',flush=True)
