import pandas as pd, numpy as np, matplotlib as mpl, matplotlib.pyplot as plt
mpl.rcParams['font.family']='Liberation Serif'
n=pd.read_parquet('rais/niveis.parquet'); f=n[n.NIVEL=='UF'].copy()
u=pd.read_pickle('u2.pkl'); x=u.drop_duplicates('cbo')[['cbo','exp14_A','exp34_A']]
f['cbo']=f.CBO2002.astype(str); f=f.merge(x,on='cbo',how='left'); f=f[f.exp14_A.notna()].copy(); f['q']=f.QTDE
f=f.sort_values('MEDIA'); cq=f.q.cumsum()/f.q.sum(); f['dec']=np.minimum((cq*10).astype(int),9)+1
g=f.groupby('dec').apply(lambda d:pd.Series({'wage':(d.q*d.MEDIA).sum()/d.q.sum(),'alta':100*(d.q*d.exp34_A).sum()/d.q.sum(),'exp':100*(d.q*d.exp14_A).sum()/d.q.sum()}),include_groups=False)
g['media']=g.exp-g.alta
print(g.round(1)); 
us=f.groupby('UF').apply(lambda d:pd.Series({'wage':(d.q*d.MEDIA).sum()/d.q.sum(),'exp':100*(d.q*d.exp14_A).sum()/d.q.sum(),'wexp':(d.q*d.exp14_A*d.MEDIA).sum()/(d.q*d.exp14_A).sum(),'wnot':(d.q*(1-d.exp14_A)*d.MEDIA).sum()/(d.q*(1-d.exp14_A)).sum()}),include_groups=False)
us['prem']=100*(us.wexp/us.wnot-1); print(us.round(1).sort_values('prem').to_string())
r=np.corrcoef(us.wage,us.exp)[0,1]; print('corr UF wage x exposure %.2f'%r, 'corr decile wage x exp (dec)',np.corrcoef(g.wage,g.exp)[0,1])
us.to_csv('salario_uf.csv'); g.to_csv('salario_decil.csv')
fig,ax=plt.subplots(1,2,figsize=(7.4,3.9),dpi=300,gridspec_kw={'width_ratios':[1.15,1]})
a=ax[0]; xx=np.arange(1,11)
a.bar(xx,g.alta,color='#12385e',width=0.75,label='Alta exposição (IA pode fazer metade ou mais das tarefas)')
a.bar(xx,g.media,bottom=g.alta,color='#a9c6e3',width=0.75,label='Exposição baixa ou média')
for i,(v,w) in enumerate(zip(g.exp,g.wage)): a.text(i+1,v+0.8,'%.0f%%'%v,ha='center',fontsize=6.3)
a.set_xticks(xx); a.set_xticklabels([('%.1f'%(w/1000)).replace('.',',')+' mil' if w<10000 else '%.0f mil'%(w/1000) for w in g.wage],fontsize=5.6,rotation=0)
a.set_xlabel('Remuneração média mensal em R\\$ (cada barra = 10% dos vínculos, do menor ao maior salário)',fontsize=6.2)
a.set_ylabel('% dos vínculos em ocupações expostas',fontsize=6.8); a.tick_params(axis='y',labelsize=6.5)
a.axhline(35.2,color='black',ls='--',lw=0.7,label='Média do Brasil (35,2%)')
a.set_ylim(0,60); a.legend(fontsize=5.8,frameon=False,loc='upper left',bbox_to_anchor=(0,1.02))
a.set_title('(a) Exposição por faixa de remuneração',fontsize=7.5,loc='left')
for s in ['top','right']: a.spines[s].set_visible(False)
b=ax[1]
us=us.sort_values('prem'); yy=np.arange(len(us)); 
b.hlines(yy,0,us.prem,color='#a9c6e3',lw=1.2,zorder=2)
b.scatter(us.prem,yy,s=16,color=np.where(us.prem>=0,'#d98c2b','#12385e'),zorder=3)
b.axvline(0,color='black',lw=0.6)
b.set_yticks(yy); b.set_yticklabels(us.index,fontsize=5.6); b.tick_params(axis='x',labelsize=6.3)
b.set_xlabel('Remuneração média em ocupações expostas vs. não expostas (%)',fontsize=6.4)
b.set_title('(b) Diferença salarial dentro de cada estado',fontsize=7.5,loc='left')
for s_ in ['top','right','left']: b.spines[s_].set_visible(False)
b.grid(axis='x',color='#e5e5e5',lw=0.5); b.set_axisbelow(True)
fig.text(0.01,0.985,'Quem está mais exposto à IA generativa: quem ganha menos ou quem ganha mais?',fontsize=9.5,fontweight='bold',va='top')
fig.text(0.01,0.935,'No Brasil, ocupações expostas pagam em média o mesmo que as demais (R\\$ 4.090 vs. R\\$ 4.098), e a exposição não cresce nem cai com a faixa salarial.\nDentro dos estados o quadro é misto: em 24 dos 27 pagam menos (até -26% em RR, PI e AP); só em SP, SC e DF pagam mais.',fontsize=6.5,va='top',color='#333',linespacing=1.25)
fig.text(0.01,0.008,'Fonte: elaboração própria com dados de RAIS 2025 (Bartkevihi, 2026) e OIT (Gmyrek et al., 2025). Faixas calculadas sobre a remuneração média de cada ocupação por estado; vínculos mapeados.',fontsize=5.1,color='#555')
plt.subplots_adjust(left=0.07,right=0.99,top=0.80,bottom=0.17,wspace=0.28)
fig.savefig('/home/claude/out/fig6.png')
