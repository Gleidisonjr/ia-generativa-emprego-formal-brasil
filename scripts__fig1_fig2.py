import pandas as pd, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
plt.rcParams['font.family']='Liberation Serif'
d=pd.read_pickle('/home/claude/data/cnae/cnae.pkl')
g=d.groupby('uf')[['mp','e14','e34']].sum(); g['e']=100*g.e14/g.mp; g['h']=100*g.e34/g.mp
reg={'RO':'Norte','AC':'Norte','AM':'Norte','RR':'Norte','PA':'Norte','AP':'Norte','TO':'Norte','MA':'Nordeste','PI':'Nordeste','CE':'Nordeste','RN':'Nordeste','PB':'Nordeste','PE':'Nordeste','AL':'Nordeste','SE':'Nordeste','BA':'Nordeste','MG':'Sudeste','ES':'Sudeste','RJ':'Sudeste','SP':'Sudeste','PR':'Sul','SC':'Sul','RS':'Sul','MS':'Centro-Oeste','MT':'Centro-Oeste','GO':'Centro-Oeste','DF':'Centro-Oeste'}
g['reg']=g.index.map(reg); g=g.sort_values('e',ascending=False)
col={'Norte':'#2a78d6','Nordeste':'#eb6834','Sudeste':'#1baf7a','Sul':'#6250d6','Centro-Oeste':'#e87ba4'}
rg=d.assign(r=d.uf.map(reg)).groupby('r')[['mp','e14','e34']].sum(); rg['e']=100*rg.e14/rg.mp; rg['h']=100*rg.e34/rg.mp
nat=d[['mp','e14','e34']].sum(); ne=100*nat.e14/nat.mp
fig=plt.figure(figsize=(6.1,3.0),dpi=300)
ax=fig.add_axes([0.065,0.17,0.57,0.68]); bx=fig.add_axes([0.80,0.17,0.19,0.68])
x=np.arange(len(g))
ax.bar(x,g.e,color=[col[r] for r in g.reg],width=0.72,zorder=2)
ax.scatter(x,g.h,s=11,color='#111',edgecolor='white',linewidth=0.5,zorder=3)
ax.axhline(ne,color='#444',lw=0.8,ls='--',zorder=4)
ax.set_xticks(x); ax.set_xticklabels(g.index,fontsize=6.3,rotation=90)
ax.set_ylim(0,52); ax.set_yticks([0,10,20,30,40,50]); ax.set_xlim(-0.7,26.7); ax.tick_params(axis='y',labelsize=6.5,length=2); ax.tick_params(axis='x',length=0)
ax.yaxis.grid(True,color='#ddd',lw=0.5,zorder=0); [ax.spines[s].set_visible(False) for s in ['top','right']]
ax.set_ylabel('% dos vínculos',fontsize=7)
ax.set_title('(a) UFs: barra = expostos; ponto = alta exposição; tracejado = Brasil (35,1%)',fontsize=6.8,loc='left',pad=8)
for u in ['DF','PB','PI','MS','AM']:
    i=list(g.index).index(u); ax.text(i,g.e[u]+0.8,f'{g.e[u]:.1f}'.replace('.',','),ha='center',fontsize=5.6)
hs=[Patch(color=col[r],label=f"{r}: {rg.e[r]:.1f} | {rg.h[r]:.1f}".replace('.',',')) for r in ['Norte','Nordeste','Sudeste','Sul','Centro-Oeste']]
ax.legend(handles=hs,fontsize=5.5,frameon=False,loc='upper right',ncol=2,title='Região: % expostos | % alta exposição',title_fontsize=5.6,borderpad=0.1,labelspacing=0.25,handlelength=1,columnspacing=0.8)
names={'G':'Comércio','O':'Adm. pública','N':'Adm. e serv. compl.','C':'Ind. transformação','Q':'Saúde','M':'Ativ. profissionais','J':'Informação','K':'Finanças'}
s=d.groupby('sec')[['e14','e34']].sum()/nat.mp*100; s=s.loc[list(names)]
y=np.arange(len(s))[::-1]
bx.barh(y,s.e34,color='#2a78d6',height=0.65,zorder=2,label='Alta exposição')
bx.barh(y,s.e14-s.e34,left=s.e34,color='#a9c8ee',height=0.65,zorder=2,label='Demais expostos')
bx.set_yticks(y); bx.set_yticklabels([names[k] for k in s.index],fontsize=6)
for yi,v in zip(y,s.e14): bx.text(v+0.2,yi,f'{v:.1f}'.replace('.',','),va='center',fontsize=5.8)
bx.set_xlim(0,14.8); bx.tick_params(axis='x',labelsize=6,length=2); bx.tick_params(axis='y',length=0)
bx.xaxis.grid(True,color='#ddd',lw=0.5,zorder=0); [bx.spines[k].set_visible(False) for k in ['top','right']]
bx.set_xlabel('p.p. da exposição nacional',fontsize=6.5)
bx.set_title('(b) Contribuição setorial',fontsize=6.8,loc='right',pad=8)
bx.legend(fontsize=5.5,frameon=False,loc='lower right',borderpad=0.1,handlelength=1,labelspacing=0.2)
fig.savefig('fig1.png',dpi=300,facecolor='white',bbox_inches='tight',pad_inches=0.04)
