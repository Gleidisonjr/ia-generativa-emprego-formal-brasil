import pandas as pd, pyreadr, numpy as np
P='/home/claude/data/ocupacoesBR/data/'
def rd(n):
    r=pyreadr.read_r(P+n+'.rda'); return r[list(r)[0]]
c88=rd('cbo2002_isco88'); esc=rd('cbo2002_escada'); i88=rd('isco88_isco08'); i08_88=rd('isco08_isco88')
occ=pd.read_csv('ilo_occ.csv',dtype={'ISCO_08':str})
r=pd.read_parquet('rais/niveis.parquet')
print(r.columns.tolist(), r.NIVEL.value_counts().to_dict())
u=r[r.NIVEL=='UF'].copy(); u['cbo']=u.CBO2002.astype(str).str.zfill(6)
print('UF total',u.QTDE.sum(), 'BR total', r[r.NIVEL=='BRASIL'].QTDE.sum())
# CBO->ISCO88 with ladder
m6=dict(zip(c88.cbo2002,c88.isco88))
lad={ (int(a),b):c for a,b,c in zip(esc.nivel,esc.prefixo,esc.isco88)}
def cbo2isco88(c):
    if c in m6: return m6[c],6
    for k in (4,3,2):
        v=lad.get((k,c[:k]))
        if isinstance(v,str) and v==v: return v,k
    return None,0
cb=pd.DataFrame({'cbo':u.cbo.unique()})
res=cb.cbo.map(cbo2isco88); cb['isco88']=[x[0] for x in res]; cb['nivel']=[x[1] for x in res]
u=u.merge(cb,on='cbo')
tot=u.QTDE.sum()
print((u.groupby('nivel').QTDE.sum()/tot).round(4).to_dict())
# ISCO88->ISCO08 (single, as the package) and set of alternatives (inverse of isco08_isco88)
s=dict(zip(i88.isco88,i88.isco08))
alt=i08_88.groupby('isco88').isco08.apply(list).to_dict()
sc=occ.set_index('ISCO_08')
def score_single(i88c):
    d=s.get(i88c); 
    return d if d in sc.index else None
u['isco08']=u.isco88.map(lambda x: s.get(x) if x else None)
print('isco08 dest in ILO 4d:', (u[u.isco08.isin(sc.index)].QTDE.sum()/tot).round(4))
print('has isco88:', (u[u.isco88.notna()].QTDE.sum()/tot).round(4))
u.to_pickle('u.pkl'); occ.to_pickle('occ.pkl')
bad=u[u.isco88.notna() & ~u.isco08.isin(sc.index)]
print(bad.groupby('isco08').QTDE.sum().sort_values(ascending=False).head(15))
print(u[u.isco88.isna()].groupby('cbo').QTDE.sum().sort_values(ascending=False).head(10))
