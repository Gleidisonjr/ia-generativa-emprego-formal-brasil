# Exposição do emprego formal à IA generativa nos estados brasileiros

Trabalho da disciplina *Metodologia e Técnicas de Pesquisa em Economia II* (Ciências Econômicas, UFMT, 2026). Integrantes: Eduardo Melo, Gleidison Jr., Guilherme Rocha e Nicolas Ferreira. Professora: Carla Cristina Rosa de Almeida.

**Pergunta:** quais estados e regiões do Brasil concentram mais empregos formais expostos à IA generativa?

**Resposta curta:** 35,2% dos vínculos formais estão em profissões expostas (17,5% em alta exposição). O Distrito Federal tem o maior valor (41,9%) e Mato Grosso do Sul, o menor (29,6%).

## Como foi feito

1. **Nota por profissão.** A OIT (Gmyrek et al., 2025, *ILO Working Paper 140*) dá a cada ocupação da ISCO-08 uma nota de 1 a 4. "Exposta" = nota 1 a 4; "alta exposição" = nota 3 ou 4.
2. **Empregos.** RAIS 2025, vínculos ativos em 31/12/2025, por estado, profissão (CBO-2002) e setor (CNAE), consultados no BigQuery (Base dos Dados).
3. **Ligação entre as listas.** CBO-2002 → ISCO-88 → ISCO-08 pela tabela de correspondência do Ministério do Trabalho (pacote `ocupacoesBR`). Cobriu cerca de 93% dos vínculos.
4. **Cálculo.** Percentual de vínculos expostos por estado, região e setor; decomposição das diferenças entre estados; análise espacial por município; comparação com remuneração.

## Arquivos

O GitHub (envio pelo navegador) não aceita pastas, então o prefixo do nome indica o grupo de cada arquivo:

| Prefixo | Conteúdo |
|---|---|
| `dados__` | Tabelas já tratadas (ver abaixo) |
| `sql__` | Consultas rodadas no BigQuery |
| `scripts__` | Código Python usado nos cálculos e nas figuras |
| `figuras__` | Figuras 1 a 6 |
| `docs__` | Versão em PDF do trabalho |

### Principais tabelas (`dados__`)

- `dados__uf_resumo.csv`: vínculos analisados, % expostos (`exp14`), % em alta exposição (`exp34`) e cobertura, por UF.
- `dados__uf_setor.csv` e `dados__uf_setor_bigquery.csv`: vínculos por UF e seção da CNAE.
- `dados__uf_cbo_exposicao.csv`: vínculos, remuneração média e exposição por UF e profissão (títulos em `dados__cbo_titulos.csv`).
- `dados__oit_escores_isco08.csv`: notas da OIT por ocupação.
- `dados__decomposicao_uf.csv`: quanto da diferença de cada estado vem do setor e quanto vem da profissão dentro do setor.
- `dados__mun_exposicao.csv` e `dados__mun_lisa.csv`: exposição por município e agrupamentos espaciais.
- `dados__salario_uf.csv` e `dados__salario_decil.csv`: remuneração e exposição.

## Limitações

- A nota mede potencial técnico de a IA executar tarefas, não perda de emprego.
- A RAIS cobre só o emprego formal; a informalidade fica de fora.
- Cerca de 7% dos vínculos não tiveram correspondência entre as listas de profissões. Tratando-os como não expostos, o total nacional cai para 32,7%; conforme a hipótese, varia de 30,4% a 35,2%.

## Reprodução

Os scripts `scripts__*` foram escritos com caminhos do ambiente de trabalho original (`/home/claude/...`); ajuste os caminhos antes de rodar. Os microdados brutos da RAIS e os arquivos da OIT e do `ocupacoesBR` **não** estão aqui; baixe-os nas fontes abaixo.

## Fontes

- GMYREK, P. et al. *Generative AI and jobs: a refined global index of occupational exposure*. Genebra: OIT, 2025. (ILO Working Paper 140).
- BASE DOS DADOS. RAIS: microdados de vínculos (`basedosdados.br_me_rais.microdados_vinculos`). https://basedosdados.org
- Pacote `ocupacoesBR` (tabelas CBO-2002 ↔ ISCO).
- DUQUE, D. *Inteligência artificial generativa e mercado de trabalho no Brasil*. Blog do IBRE/FGV, 27 abr. 2026.
