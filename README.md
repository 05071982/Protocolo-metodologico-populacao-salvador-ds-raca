# Protocolo metodológico — População de Salvador por DS, bairro, sexo, idade e raça/cor (2000–2026)

[![DOI](https://zenodo.org/badge/1452138178.svg)](https://doi.org/10.5281/zenodo.24096844)

Base populacional oficial da **Sala de Situação em Saúde de Salvador (SDSS/SMS)** para o **TabNet Salvador**, o **Painel Sociodemográfico** e os painéis de BI com denominador populacional.

📘 **Documentação completa:** [Wiki do projeto](https://github.com/05071982/Protocolo-metodologico-populacao-salvador-ds-raca/wiki)

## Tabela principal

```
ANO | DS | COD_BAIRRO | FXET | SEXO | RACA | FREQ
```

- `resultados/populacao_salvador_bairro_ds_2000_2026.csv.gz` — 942.840 linhas (27 anos × 194 unidades bairro×DS × 2 × 18 × 5)
- `resultados/POP_SSA_DS_BAIRRO_RACA_2000_2026_v3.xlsx` — planilha com metodologia, dicionário, checagens, POP_DS, POP_BAIRRO e SETORES

- `resultados/populacao_salvador_ds_sexo_idade_2000_2026.csv.gz` e `POP_SSA_DS_SEXO_IDADE_SIMPLES_2000_2026.xlsx` — DS × sexo × idade simples (0–100+), 65.448 linhas, totais por faixa idênticos à base principal

- `resultados/populacao_salvador_bairro_ds_idade_raca_2000_2026.csv.gz` — `ANO | DS | COD_BAIRRO | IDADE | FXET | SEXO | RACA | FREQ` (3.116.090 linhas com FREQ > 0), coerente com as duas tabelas acima

## Método (resumo)

- **Totais municipais:** Censo (2000, 2010, 2022); TCU/IBGE nos demais anos (2023: RIPSA).
- **Distribuição interna:** Razão Censitária com razões variáveis entre os Censos 2010 e 2022, com IPF/raking para raça e idade e arredondamento pelo maior resto.
- 12 Distritos Sanitários · 171 bairros (inclui Aquarius, Lei 9.778/2024) · 18 faixas etárias · 5 categorias de raça/cor.

## Atualização anual (ex.: 2027)

1. Acrescente `2027,<total>,TCU/IBGE,0` em `dados/entrada/totais_municipais.csv`.
2. No R: `setwd("<pasta do repositório>"); source("R/04_atualizar_populacao.R")`.
3. Para idade simples: `source("R/05_idade_simples.R")`.
4. Use `resultados/populacao_salvador_bairro_ds_2000_2027.csv` e `populacao_salvador_ds_sexo_idade_2000_2027.csv`.

## Estrutura

```
R/            scripts R (01 chave setor-bairro-DS, 02 Aquarius, 03 estrutura base, 04 atualização anual, funcoes)
python/       implementação de referência que gerou a v3
dados/
  entrada/    totais municipais, SESAB 2010, raça 2010, chave setores, população IBGE por bairro
  estrutura/  estruturas 2010 (DS) e 2022 (DS e bairro×DS) — base da atualização anual
  dicionarios/ DS, FXET, SEXO, RACA, bairros
resultados/   base final, planilha v3, backtest de métodos
```

## Equipe

- Jessidenes Teixeira de Freitas Mendes Leal
- Rafaella Santiago Coutinho Santos

## Como citar

Leal JTFM, Santos RSC. Protocolo metodológico para estimativa populacional de Salvador por distrito sanitário, bairro, sexo, idade e raça/cor, 2000–2026 [Internet]. Salvador: Secretaria Municipal da Saúde de Salvador; 2026. doi:10.5281/zenodo.24096844

## Licença

Dados e documentação: CC BY 4.0. Código: MIT. Ver `LICENSE`.
