# 8. Códigos R

Todos os scripts estão em [`R/`](https://github.com/05071982/Protocolo-metodologico-populacao-salvador-ds-raca/tree/main/R) no repositório.

| Script | Quando rodar | Entrada | Saída |
|---|---|---|---|
| `funcoes.R` | carregado pelos demais | — | `arred_maior_resto()`, `ipf_2d()`, `composicao_ano()` |
| `01_chave_setor_bairro_ds.R` | nova malha, novo DS ou novo bairro | `BA_setores_CD2022.shp`, `DISTRITO_SANITARIO.shp` | `chave_setor_bairro_DS_2022.csv` |
| `01b_chave_setor2010.R` | nova malha de 2010 ou novos limites (v5) | malha de setores 2010 de Salvador, `DISTRITO_SANITARIO.shp`, `delimitacao_de_bairros_oficial.shp` | `chave_setor2010_bairro_ds.csv` (todas as interseções com fração de área) |
| `02_aquarius.R` | criação de bairro desmembrado | setores + `delimitacao_de_bairros_oficial.shp` | `setores_pituba_aquarius.csv` |
| `03_estrutura_base.R` | mudança na estrutura censitária | `pop_*.csv` 2022 + `dados/entrada/` | estruturas-semente 2010 e 2022 (v3) |
| *estruturas e calibração (v5)* | mudança na estrutura censitária | setores 2010 e 2022 + margens IBGE em `dados/entrada/` | `dados/estrutura/estrutura_{2000,2010,2022}_unidade.csv`, idade simples (referência: `python/v5_*.py`) |
| **`04_atualizar_populacao.R`** | **todo ano** | `dados/estrutura/estrutura_*_unidade.csv` + `totais_municipais.csv` | `resultados/*.csv` |
| **`05_idade_simples.R`** | **todo ano, depois do 04** | saída do 04 + `proporcao_idade_simples_na_faixa.csv` + `idade_simples_censos_ds.csv` | `populacao_salvador_ds_sexo_idade_*.csv` |
| **`06_bairro_idade_raca.R`** | todo ano, depois do 05 | saídas do 04 e do 05 | `populacao_salvador_bairro_ds_idade_raca_*.csv` |
| **`07_exportar_por_ano.R`** | todo ano, depois do 06 | saída do 06 + `dados/dicionarios/` | `populacao_bairro_idade_raca_por_ano.zip` |

Pacotes: `sf` e `dplyr` (só nos scripts 01 e 02); `zip` e, opcionalmente, `openxlsx` (script 07). Os scripts 03 a 06 usam apenas o R base.

## 8.1 Núcleo do método (`funcoes.R`)

```r
# Arredondamento pelo maior resto (Hamilton), desempate estável
arred_maior_resto <- function(x, total) {
  fl  <- floor(x)
  rem <- as.integer(round(total - sum(fl)))
  if (rem > 0) {
    ordem <- order(-(x - fl), seq_along(x))
    fl[ordem[seq_len(rem)]] <- fl[ordem[seq_len(rem)]] + 1
  }
  as.integer(fl)
}

# Razão Censitária com razões variáveis, ancorada em três censos (v4)
composicao_ano <- function(s00, s10, s22, ano) {
  if (ano < 2010) { w <- (ano - 2000) / 10; s <- exp((1 - w) * log(s00) + w * log(s10)) }
  else            { w <- (ano - 2010) / 12; s <- exp((1 - w) * log(s10) + w * log(s22)) }
  s / sum(s)
}
```

## 8.2 Atualização anual (trecho central do `04`)

```r
part <- function(C) (C + 0.5) / sum(C + 0.5)
s00 <- part(C00); s10 <- part(C10); s22 <- part(C22)       # estruturas calibradas aos censos
for (i in seq_len(nrow(totais))) {
  ano <- totais$ANO[i]; Tt <- totais$TOTAL[i]
  if (as.character(ano) %in% names(censo)) {
    Xi <- censo[[as.character(ano)]]                         # 2000, 2010, 2022: valores censitários
  } else {
    Xi <- arred_maior_resto(composicao_ano(s00, s10, s22, ano) * Tt, round(Tt))
  }
  ...
}
# v5: as células são unidade bairro × DS × sexo × faixa × raça (34.920).
# Após 2022: tendência por DS × sexo × faixa × raça, repartida entre os bairros
# na proporção de 2022, com maior resto dentro de cada célula do DS.
```

## 8.3 Validação

Não havia R no ambiente em que os scripts foram escritos. O `04` e o `05` foram validados por uma réplica linha a linha em Python (`python/v5_espelho_R.py`) que lê os mesmos CSV do repositório. A réplica reproduziu **as 942.840 células da base e as 65.448 da idade simples da v5 sem nenhuma diferença**, também com um ano 2027 de teste acrescentado.

Ao rodar no R pela primeira vez, confira:

```r
pop <- read.csv("resultados/populacao_salvador_bairro_ds_2000_2026.csv")
ref <- read.csv(gzfile("resultados/populacao_salvador_bairro_ds_2000_2026.csv.gz"))
m <- merge(pop, ref, by = c("ANO","DS","COD_BAIRRO","FXET","SEXO","RACA"))
sum(m$FREQ.x != m$FREQ.y)   # esperado: 0
```

O `03_estrutura_base.R` é a tradução para R dos scripts de referência em `python/` (`s22.py`, `p2_s22.py`, `v3_model.py`). Pequenas diferenças de ponto flutuante no IPF podem mudar o arredondamento em ±1 em células isoladas.

## 8.4 Implementação de referência (Python)

Os scripts em `python/` geraram as versões publicadas. Ordem de execução:

- **Sementes (v3):** `geo.py` → `bds.py` → `p1_sesab2010.py` → `s22.py` → `p2_s22.py` → `v3_model.py` → `v3_series.py` → `v3_series_censo.py`
- **v4:** `v4_inputs.py` (lê e confere SIDRA 136/3175, SESAB e DS 2000) → `v4_model.py` (calibração censitária) → `v4_series.py` → `v4_idade.py` → `v4_bairro_idade.py` → `v4_validar.py` → `v4_export.py` → `v4_repo_estrutura.py` → `v4_excel.py`, `v4_idade_tabs.py`
- **v5:** `v5_setores2010.py` (lê setores 2010 e chave) → `v5_harmoniza_chave.py` → `v5_estrutura2010.py` → `v5_model.py` (calibração e série por unidade) → `v5_idade.py` → `v5_bairro_idade.py` → `v5_validar.py` → `v5_backtest.py` → `v5_export.py` → `v5_repo_estrutura.py` → `v5_excel.py`, `v5_idade_tabs.py`; conferência do R: `v5_espelho_R.py`
- **Conferência do R:** `v4_espelho_R.py`
