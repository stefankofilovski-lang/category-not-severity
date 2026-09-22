"""Clarify labels in the original sensitivity figure without changing data."""
from pathlib import Path
import json
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]/'.deps'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
G=Path(__file__).resolve().parents[1]
B=G.parent/'revision-2026-09-22'
if not B.is_dir(): B=G.parent/'research'
data=json.loads((B/'results/summary.json').read_text(encoding='utf-8'))
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'pdf.fonttype':42})
fig,axes=plt.subplots(1,2,figsize=(7.0,2.15),gridspec_kw={'width_ratios':[1,1]})
ax=axes[0]
for i,c in enumerate(['naive','decomposed']):
    group=[x for x in data['full144']['direction'] if x['condition']==c and x['group'] in ['outside','inside']]
    for j,x in enumerate(group):
        ax.errorbar(x['mean'],j+(i-.5)*.18,xerr=[[x['mean']-x['lo']],[x['hi']-x['mean']]],fmt='o',capsize=3,
                    color=['#255978','#b05b35'][i],label=['Basic','Step-by-step'][i] if j==0 else None)
ax.axvline(0,color='#999999',lw=.8); ax.set_yticks([0,1],['Outside (109)','Inside (33)'])
ax.set_xlabel('Mean signed category difference'); ax.invert_yaxis(); ax.legend(frameon=False,fontsize=8)
ax.set_title('(a) Annex III; unclear excluded',fontsize=9)
ax=axes[1]
for j,key in enumerate(['full144','same130','no_driving','historical8']):
    x=data[key]['delta_paired_qwk']; v=x['value']; lo,hi=x['ci']
    ax.errorbar(v,j,xerr=[[v-lo],[hi-v]],fmt='o',capsize=3,color='#255978')
ax.axvline(0,color='#999999',lw=.8)
ax.set_yticks(range(4),['144 records','14 extra-source\ncases excluded','Driving excluded','8 earlier labels\nrestored'])
ax.invert_yaxis(); ax.set_xlabel('Paired panel mean change in QWK'); ax.set_title('(b) Sensitivity of prompt comparison',fontsize=9)
for ax in axes: ax.spines[['top','right']].set_visible(False)
fig.tight_layout(w_pad=1.8); fig.savefig(G/'paper/fig_revision.pdf',bbox_inches='tight'); plt.close(fig)
print('Figure wording refreshed from unchanged numerical results.')
