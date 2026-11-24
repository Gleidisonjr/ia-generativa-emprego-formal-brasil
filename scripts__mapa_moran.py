import pandas as pd, numpy as np, geopandas as gpd, json
from libpysal.weights import Queen, KNN
from esda.moran import Moran, Moran_Local
g=pd.read_csv('mun_exposicao.csv',dtype={'ID_MUNICIPIO':str})
geo=gpd.read_file('geo/mun.json'); geo=geo.rename(columns={'id':'ID_MUNICIPIO'})
print(len(geo), geo.ID_MUNICIPIO.nunique(), 'sem geo:',len(set(g.ID_MUNICIPIO)-set(geo.ID_MUNICIPIO)),'sem dado:',len(set(geo.ID_MUNICIPIO)-set(g.ID_MUNICIPIO)))
d=geo.merge(g,on='ID_MUNICIPIO',how='inner').to_crs(5880)
d['uf_']=d.uf
np.random.seed(42)
w=Queen.from_dataframe(d,use_index=False); 
print('islands',len(w.islands))
if w.islands:
    w=KNN.from_dataframe(d,k=4)
w.transform='r'
y=d.p14.values
mi=Moran(y,w,permutations=999); print('Moran I=%.3f p=%.4f'%(mi.I,mi.p_sim))
y2=d.p34.values; mi2=Moran(y2,w,permutations=999); print('Moran I alta=%.3f p=%.4f'%(mi2.I,mi2.p_sim))
lm=Moran_Local(y,w,permutations=999,seed=42)
q=lm.q; sig=lm.p_sim<0.05
lab=np.where(~sig,'ns',np.select([q==1,q==2,q==3,q==4],['HH','LH','LL','HL'],default='ns'))
d['lisa']=lab
print(pd.Series(lab).value_counts())
# robustez: municipios com >=1000 vinculos
big=d.tot>=1000
print('n>=1000:',big.sum())
d.to_file('geo/mun_resultado.gpkg',driver='GPKG')
d.drop(columns='geometry').to_csv('mun_lisa.csv',index=False)
json.dump({'I14':mi.I,'p14':mi.p_sim,'I34':mi2.I,'p34':mi2.p_sim,'n':len(d)},open('moran.json','w'))
print(d.groupby('lisa').agg(n=('tot','size'),emp=('tot','sum')))
print(d[d.lisa=='HH'].groupby('uf').size().sort_values(ascending=False).head(8))
print(d[d.lisa=='LL'].groupby('uf').size().sort_values(ascending=False).head(8))
print(d.p14.describe().round(1))
