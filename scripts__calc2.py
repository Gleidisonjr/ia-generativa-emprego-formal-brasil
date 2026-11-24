import pandas as pd, numpy as np, pyreadr
from scipy.stats import spearmanr
u=pd.read_pickle('u.pkl'); occ=pd.read_pickle('occ.pkl')
i08_88=pyreadr.read_r('ocupacoesBR/data/isco08_isco88.rda'); i08_88=i08_88[list(i08_88)[0]]
i88=pyreadr.read_r('ocupacoesBR/data/isco88_isco08.rda'); i88=i88[list(i88)[0]]
s=dict(zip(i88.isco88,i88.isco08))
alt=i08_88.groupby('isco88').isco08.apply(list).to_dict()
cat={'Exposed: Gradient 1':1,'Exposed: Gradient 2':2,'Exposed: Gradient 3':3,'Exposed: Gradient 4':4}
occ['g']=occ.potential25.map(cat).fillna(0).astype(int)
codes=occ.ISCO_08.tolist()
def desc(d):
    """ILO 4-digit codes under a (possibly aggregated) ISCO-08 code"""
    p=d.rstrip('0') or d[:1]
    while p:
        m=[c for c in codes if c.startswith(p)]
        if m: return m
        p=p[:-1]
    return []
def feat(lst):
    lst=[c for c in lst if c in set(codes)] if False else lst
    sub=occ[occ.ISCO_08.isin(lst)]
    n=len(sub)
    return dict(exp14=(sub.g>=1).mean(), exp34=(sub.g>=3).mean(), g4=(sub.g==4).mean(), score=sub.mean_score_2025.mean())
# primary: single dest + descendants
cache={}
def primary(i88c):
    if i88c is None or i88c!=i88c: return None
    d=s.get(i88c)
    if d is None: return None
    if d not in cache: cache[d]=feat(desc(d))
    return cache[d]
cacheB={}
def altern(i88c):
    if i88c is None or i88c!=i88c: return None
    if i88c not in alt: return None
    if i88c not in cacheB:
        lst=[]
        for d in alt[i88c]: lst+=desc(d)
        cacheB[i88c]=feat(lst) if lst else None
    return cacheB[i88c]
for name,fn in (('A',primary),('B',altern)):
    f=u.isco88.map(fn)
    ok=f.notna()
    for k in ('exp14','exp34','g4','score'):
        u[f'{k}_{name}']=[x[k] if x else np.nan for x in f]
tot=u.QTDE.sum(); okA=u.exp14_A.notna(); okB=u.exp14_B.notna()
print('cov A',u[okA].QTDE.sum()/tot,'cov B',u[okB].QTDE.sum()/tot)
reg={'RO':'Norte','AC':'Norte','AM':'Norte','RR':'Norte','PA':'Norte','AP':'Norte','TO':'Norte','MA':'Nordeste','PI':'Nordeste','CE':'Nordeste','RN':'Nordeste','PB':'Nordeste','PE':'Nordeste','AL':'Nordeste','SE':'Nordeste','BA':'Nordeste','MG':'Sudeste','ES':'Sudeste','RJ':'Sudeste','SP':'Sudeste','PR':'Sul','SC':'Sul','RS':'Sul','MS':'Centro-Oeste','MT':'Centro-Oeste','GO':'Centro-Oeste','DF':'Centro-Oeste'}
u['reg']=u.UF.map(reg); assert u.reg.notna().all()
def agg(df,by,sfx):
    d=df[df[f'exp14_{sfx}'].notna()]
    g=d.groupby(by)
    out=pd.DataFrame({'emp_map':g.QTDE.sum()})
    for k in ('exp14','exp34','g4','score'):
        out[k]=g.apply(lambda x: np.average(x[f'{k}_{sfx}'],weights=x.QTDE))
    out['emp_tot']=df.groupby(by).QTDE.sum()
    out['cob']=out.emp_map/out.emp_tot
    return out
for sfx in 'AB':
    br=agg(u.assign(b='BR'),'b',sfx); print(sfx,'BR\n',br.round(4).to_string())
A=agg(u,'UF',  'A'); B=agg(u,'UF','B'); RA=agg(u,'reg','A'); RB=agg(u,'reg','B')
print(A.sort_values('exp14',ascending=False).round(4).to_string())
print(RA.sort_values('exp14',ascending=False).round(4).to_string())
print('spearman A vs B exp14',spearmanr(A.exp14,B.exp14), 'exp34',spearmanr(A.exp34,B.exp34))
print('regions B\n',RB.round(4).to_string())
u.to_pickle('u2.pkl'); A.to_pickle('A.pkl'); B.to_pickle('B.pkl'); RA.to_pickle('RA.pkl'); RB.to_pickle('RB.pkl')
