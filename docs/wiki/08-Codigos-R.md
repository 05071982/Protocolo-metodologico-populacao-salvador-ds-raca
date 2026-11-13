# 8. Códigos R

Todos os scripts estão em [`R/`](https://github.com/05071982/Protocolo-metodologico-populacao-salvador-ds-raca/tree/main/R) no repositório.

| Script | Quando rodar | Entrada | Saída |
|---|---|---|---|
| `funcoes.R` | carregado pelos demais | — | `arred_maior_resto()`, `ipf_2d()`, `composicao_ano()` |
| `01_chave_setor_bairro_ds.R` | nova malha, novo DS ou novo bairro | `BA_setores_CD2022.shp`, `DISTRITO_SANITARIO.shp` | `chave_setor_bairro_DS_2022.csv` |
| `02_aquarius.R` | criação de bairro desmembrado | setores + `delimitacao_de_bairros_oficial.shp` | `setores_pituba_aquarius.csv` |
| `03_estrutura_base.R` | mudança na estrutura censitária | `pop_*.csv` 2022 + `dados/entrada/` | `dados/estrutura/*.csv` |
| **`04_atualizar_populacao.R`** | **todo ano** | `dados/estrutura/` + `totais_municipais.csv` | `resultados/*.csv` |
| **`06_bairro_idade_raca.R`** | todo ano, depois do 05 | saídas do 04 e do 05 | `populacao_salvador_bairro_ds_idade_raca_*.csv` |
| **`05_idade_simples.R`** | **todo ano, depois do 04** | saída do 04 + `proporcao_idade_simples_na_faixa.csv` | `populacao_salvador_ds_sexo_idade_*.csv` |

Pacotes: `sf` e `dplyr` (só nos scripts 01 e 02). Os scripts 03 e 04 usam apenas o R base.

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

# Razão Censitária com razões variáveis
composicao_ano <- function(s10, s22, ano) {
  w <- (ano - 2010) / 12
  s <- exp((1 - w) * log(s10) + w * log(s22))
  s / sum(s)
}
```

## 8.2 Atualização anual (trecho central do `04`)

```r
s10 <- (C10 + 0.5) / sum(C10 + 0.5)
s22 <- (C22 + 0.5) / sum(C22 + 0.5)
for (i in seq_len(nrow(totais))) {
  ano <- totais$ANO[i]; Tt <- totais$TOTAL[i]
  s <- composicao_ano(s10, s22, ano)
  if (ano < 2010) s <- ave(s, grupo_dsa, FUN = sum) * pr_raca_2010   # raça congelada antes de 2010
  Xi <- arred_maior_resto(s / sum(s) * Tt, round(Tt))               # DS × sexo × faixa × raça
  ...
}
# Depois: cada célula do DS é repartida entre os bairros na proporção de 2022,
# com arredondamento de maior resto dentro de cada célula.
```

## 8.3 Validação

Não havia R no ambiente em que os scripts foram escritos. O `04_atualizar_populacao.R` foi validado por uma réplica linha a linha em Python que lê os mesmos CSV do repositório. A réplica reproduziu **as 942.840 células da v3 sem nenhuma diferença**.

Ao rodar no R pela primeira vez, confira:

```r
pop <- read.csv("resultados/populacao_salvador_bairro_ds_2000_2026.csv")
ref <- read.csv(gzfile("resultados/populacao_salvador_bairro_ds_2000_2026.csv.gz"))
m <- merge(pop, ref, by = c("ANO","DS","COD_BAIRRO","FXET","SEXO","RACA"))
sum(m$FREQ.x != m$FREQ.y)   # esperado: 0
```

O `03_estrutura_base.R` é a tradução para R dos scripts de referência em `python/` (`s22.py`, `p2_s22.py`, `v3_model.py`). Pequenas diferenças de ponto flutuante no IPF podem mudar o arredondamento em ±1 em células isoladas.

## 8.4 Implementação de referência (Python)

Os scripts em `python/` são os que geraram a v3. Ordem de execução:

`geo.py` → `bds.py` → `p1_sesab2010.py` → `s22.py` → `p2_s22.py` → `v3_model.py` → `v3_series.py` → `v3_series_censo.py` → `v3_units.py` → `v3_excel.py`
