import pandas as pd, numpy as np
from scipy.stats import spearmanr, pearsonr
u=pd.read_pickle('u2.pkl'); A=pd.read_pickle('A.pkl')
d=u[u.exp14_A.notna()].copy(); d['gg']=d.cbo.str[0]
nm={'1':'Dirigentes','2':'Profissionais das ciências e artes','3':'Técnicos de nível médio','4':'Serviços administrativos','5':'Serviços e vendas','6':'Agropecuária','7':'Produção industrial (7)','8':'Produção industrial (8)','9':'Reparação e manutenção','0':'Forças armadas'}
tot=d.QTDE.sum()
rate=d.groupby('gg').apply(lambda x: np.average(x.exp14_A,weights=x.QTDE))
shareBR=d.groupby('gg').QTDE.sum()/tot
print(pd.DataFrame({'nome':pd.Series(nm),'share_BR':shareBR,'taxa_exp':rate,'contrib_BR':shareBR*rate}).round(4).to_string())
sh=d.groupby(['UF','gg']).QTDE.sum().unstack(fill_value=0); sh=sh.div(sh.sum(1),axis=0)
print('corr(exp14, share grupo 4)',pearsonr(A.exp14.reindex(sh.index),sh['4']),spearmanr(A.exp14.reindex(sh.index),sh['4']))
print('corr(exp14, share grupo 2)',pearsonr(A.exp14.reindex(sh.index),sh['2']))
# decomposition: state share diff * national group rate
dec=(sh-shareBR.reindex(sh.columns))*rate.reindex(sh.columns)
for uf in ['DF','PB','PI','SP','MS','AM','PA']:
    print(uf, 'diff vs BR', round(A.exp14[uf]-0.3515,4), dec.loc[uf].round(4).to_dict())
# within-group (rate) differences
print((sh.loc[['DF','MS']]).round(3))
# check largest occupations by exposure nationally
top=d.groupby(['cbo','isco88']).agg(q=('QTDE','sum'),e=('exp14_A','mean')).reset_index().sort_values('q',ascending=False).head(15)
print(top)
sh.to_pickle('sh.pkl')
# bootstrapless robustness: score
print(A[['exp14','exp34','score']].corr(method='spearman'))
