import pandas as pd, numpy as np, matplotlib as mpl, matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
mpl.rcParams['font.family']='Liberation Serif'
d=pd.read_csv('cnae/cnae_fechado.csv'); d=d[d.uf!='IGNORADO']
P=d.pivot(index='uf',columns='sec',values='tot').fillna(0); S=P.div(P.sum(1),axis=0)
S=S[[c for c in S.columns if S[c].mean()>=0.004]]
ex=d.groupby('uf')[['mp','s14']].sum(); p14=100*ex.s14/ex.mp; tot=P.sum(1)
Z=StandardScaler().fit_transform(S); p=PCA(2).fit(Z); sc=p.transform(Z); sc[:,1]*=-1  # PC2 invertido: cima = mais administração pública
Ld=p.components_.T.copy(); Ld[:,1]*=-1
nm={'O':'Adm. pública','J':'Informação e\ncomunicação','K':'Finanças','G':'Comércio','C':'Indústria','A':'Agropecuária'}
lp={'O':(-1.9,2.05,'center'),'J':(1.55,1.1,'left'),'K':(1.6,-0.25,'left'),'G':(-0.45,-1.75,'right'),'C':(0.15,-1.75,'left'),'A':(-0.7,-1.3,'right')}
fig,ax=plt.subplots(figsize=(7.2,5.0),dpi=300)
sz=40+260*np.sqrt(tot/tot.max())
cmap=mpl.colors.LinearSegmentedColormap.from_list('b',['#dbe7f3','#6a9bc9','#12385e'])
sca=ax.scatter(sc[:,0],sc[:,1],s=sz,c=p14.values,cmap=cmap,vmin=29,vmax=42,edgecolor='#12385e',linewidth=0.5,zorder=3)
off={'RJ':(6,-7),'DF':(6,5),'SP':(6,5),'MT':(-4,6),'MS':(6,-3),'RN':(5,5),'PB':(6,-8),'PI':(-4,8),'AC':(-12,-9),'RR':(-6,-11),'TO':(-12,6),'AP':(-14,-8),'RO':(-14,6),'MA':(-12,-10),'PA':(-8,8),'AL':(-4,-12),'SE':(-4,-12),'ES':(6,4),'MG':(-16,6),'GO':(5,-9),'PR':(8,6),'SC':(6,4),'RS':(-14,-10),'BA':(7,-9),'PE':(6,5),'CE':(6,-9),'AM':(6,-9)}
for i,u in enumerate(S.index):
    ax.annotate(u,(sc[i,0],sc[i,1]),xytext=off.get(u,(5,4)),textcoords='offset points',fontsize=6.5,zorder=4)
k=4.0
for s_ in nm:
    j=list(S.columns).index(s_)
    ax.annotate('',xy=(Ld[j,0]*k*1.0,Ld[j,1]*k*1.0),xytext=(0,0),arrowprops=dict(arrowstyle='->',color='#d98c2b',lw=0.9),zorder=2)
    ax.text(lp[s_][0],lp[s_][1],nm[s_],fontsize=6.3,color='#9a5b0f',ha=lp[s_][2],va='center',zorder=2)
ax.axhline(0,color='#bbb',lw=0.5,zorder=1); ax.axvline(0,color='#bbb',lw=0.5,zorder=1)
ax.set_xlabel('Eixo 1 (%.0f%% da variação): menos ← → mais serviços privados avançados (informação, finanças, artes)'%(100*p.explained_variance_ratio_[0]),fontsize=7)
ax.set_ylabel('Eixo 2 (%.0f%%): estrutura produtiva ← → administração pública'%(100*p.explained_variance_ratio_[1]),fontsize=7)
ax.tick_params(labelsize=6.5)
for s_ in ['top','right']: ax.spines[s_].set_visible(False)
cb=fig.colorbar(sca,ax=ax,fraction=0.03,pad=0.01); cb.set_label('% de vínculos em ocupações expostas',fontsize=7); cb.ax.tick_params(labelsize=6.5)
fig.text(0.01,0.985,'O que diferencia a estrutura do emprego formal dos estados — e a sua exposição?',fontsize=9.5,fontweight='bold',va='top')
fig.text(0.01,0.945,'Cada ponto é um estado, posicionado pela composição setorial do emprego formal (tamanho = nº de vínculos). Não há grupos nítidos de estados:\nhá um contínuo. Os estados mais expostos são os de peso grande da administração pública (PB, DF) ou de serviços avançados (DF, RJ, SP).',fontsize=6.6,va='top',color='#333',linespacing=1.25)
fig.text(0.01,0.008,'Fonte: elaboração própria com dados de RAIS 2025 (Bartkevihi, 2026) e OIT (Gmyrek et al., 2025). Análise de componentes principais da participação de 17 seções da CNAE 2.0 no emprego.',fontsize=5.3,color='#555')
plt.subplots_adjust(left=0.08,right=0.93,top=0.86,bottom=0.11)
fig.savefig('/home/claude/out/fig4.png')
