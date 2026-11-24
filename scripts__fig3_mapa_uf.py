import geopandas as gpd, pandas as pd, numpy as np, matplotlib as mpl, matplotlib.pyplot as plt
mpl.rcParams['font.family']='Liberation Serif'
d=gpd.read_file('geo/mun_resultado.gpkg'); from shapely import make_valid
d['geometry']=d.geometry.apply(make_valid)
ufg=d.dissolve(by='uf_'); from shapely.geometry import Polygon
from shapely.ops import unary_union
def fill(g):
    ps=[p for p in (list(g.geoms) if g.geom_type in ('MultiPolygon','GeometryCollection') else [g]) if p.geom_type=='Polygon']
    return unary_union([Polygon(p.exterior) for p in ps])
ufg=ufg.to_crs(5880); ufg['geometry']=ufg.geometry.buffer(3000).buffer(-3000).apply(fill); ufg=ufg.to_crs(4674); ufg=ufg[['geometry']]
A=pd.read_pickle('A.pkl'); A.index.name='UF'
ufg['p14']=100*A.exp14.reindex(ufg.index); ufg['p34']=100*A.exp34.reindex(ufg.index)
print(ufg[['p14','p34']].describe().round(1).T)
ufg=ufg.to_crs(5880)
cm=mpl.colors.LinearSegmentedColormap.from_list('b',['#dbe7f3','#6a9bc9','#12385e'])
fig,ax=plt.subplots(1,2,figsize=(7.4,4.1),dpi=300)
off={'DF':(0.8e5,3.0e5),'SE':(3.2e5,-1.3e5),'AL':(3.2e5,-0.6e5),'PE':(3.2e5,0.1e5),'PB':(3.2e5,0.8e5),'RN':(3.2e5,1.5e5),'ES':(2.0e5,-0.5e5),'RJ':(1.5e5,-1.2e5)}
tx={'SP':(0.5e5,0.7e5),'MG':(0,0.3e5),'BA':(2.4e5,2.0e5)}
for a,col,t,vmin,vmax in [(ax[0],'p14','(a) Qualquer exposição (gradientes 1 a 4)',29,42),(ax[1],'p34','(b) Alta exposição (gradientes 3 e 4)',ufg.p34.min()-1,ufg.p34.max()+1)]:
    a.set_axis_off()
    ufg.plot(ax=a,column=col,cmap=cm,vmin=vmin,vmax=vmax,edgecolor='white',linewidth=0.6)
    for u,r in ufg.iterrows():
        c=r.geometry.representative_point(); x,y=c.x,c.y
        dx,dy=off.get(u,(0,0)); 
        if u in off and u in ('SE','AL','PE','PB','RN','ES','RJ','DF'):
            a.annotate('%s %s'%(u,('%.1f'%r[col]).replace('.',',')),(x,y),xytext=(x+dx,y+dy),fontsize=5.2,color='#222',ha='left',va='center',arrowprops=dict(arrowstyle='-',lw=0.3,color='#555'))
        else:
            rgb=cm((r[col]-vmin)/(vmax-vmin))[:3]; lum=0.299*rgb[0]+0.587*rgb[1]+0.114*rgb[2]; tc='white' if lum<0.50 else '#111'
            a.text(x+tx.get(u,(0,0))[0],y+tx.get(u,(0,0))[1],'%s\n%s'%(u,('%.1f'%r[col]).replace('.',',')),fontsize=5.2,ha='center',va='center',color=tc,linespacing=1.0)
    a.set_title(t,fontsize=7.5,loc='left',pad=2)
    a.set_xlim(ufg.total_bounds[0]-1e5,ufg.total_bounds[2]+5e5)
fig.text(0.01,0.985,'Como a exposição à IA generativa se distribui pelo território brasileiro?',fontsize=9.5,fontweight='bold',va='top')
fig.text(0.01,0.935,'Em cada estado, % dos empregos formais em ocupações cujas tarefas a IA generativa pode executar, em parte (a) ou em metade ou mais (b). O DF (41,9%),\na PB (38,9%) e o PI (37,7%) lideram; MS (29,6%), AM (30,9%) e PA (32,1%) têm os menores valores. Média do Brasil: 35,2% (a) e 17,5% (b).',fontsize=6.5,va='top',color='#333',linespacing=1.25)
fig.text(0.01,0.012,'Fonte: elaboração própria com dados de RAIS 2025 (Bartkevihi, 2026) e OIT (Gmyrek et al., 2025). Malha: IBGE via tbrugz/geodata-br (7 municípios criados após 2010 sem malha, 0,02% dos vínculos).',fontsize=5.1,color='#555')
plt.subplots_adjust(left=0.01,right=0.99,top=0.82,bottom=0.05,wspace=0.0)
fig.savefig('/home/claude/out/fig3.png')
