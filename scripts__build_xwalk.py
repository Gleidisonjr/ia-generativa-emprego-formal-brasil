import pandas as pd, pyreadr, numpy as np
P='dados_brutos/ocupacoesBR/data/'
def rd(n):
    r=pyreadr.read_r(P+n+'.rda'); return r[list(r)[0]]
c88=rd('cbo2002_isco88'); esc=rd('cbo2002_escada'); i88_08=rd('isco88_isco08'); i08_88=rd('isco08_isco88')
print(esc.head(), esc.nivel.value_counts().to_dict())
print(i88_08.n_alternativas.value_counts().to_dict())
print(i08_88.isco08.str.len().value_counts().to_dict())
ilo=pd.read_excel('dados_brutos/ilo/2025_GenAI_scores_ISCO08/Final_Scores_ISCO08_Gmyrek_et_al_2025.xlsx')
occ=ilo.drop_duplicates('ISCO_08')[['ISCO_08','Title','mean_score_2025','SD_2025','potential25']].copy()
occ['ISCO_08']=occ.ISCO_08.astype(str).str.zfill(4)
print(len(occ)); print(occ.potential25.value_counts())
print(occ.head())
occ.to_csv('dados_brutos/ilo_occ.csv',index=False)
