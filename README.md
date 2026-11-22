# Protocolo metodológico — População de Salvador por DS, bairro, sexo, idade e raça/cor (2000–2026)

[![DOI](https://zenodo.org/badge/1452138178.svg)](https://doi.org/10.5281/zenodo.24096844)

Base populacional oficial da **Sala de Situação em Saúde de Salvador (SDSS/SMS)** para o **TabNet Salvador**, o **Painel Sociodemográfico** e os painéis de BI com denominador populacional.

📘 **Documentação completa:** [Wiki do projeto](https://github.com/05071982/Protocolo-metodologico-populacao-salvador-ds-raca/wiki)

## Tabela principal

```
ANO | DS | COD_BAIRRO | FXET | SEXO | RACA | FREQ
```

- `resultados/populacao_salvador_bairro_ds_2000_2026.csv.gz` — 952.560 linhas (27 anos × 195 unidades bairro×DS × 2 × 18 × 5, mais o bairro 2 – Aeroporto com FREQ = 0)
- `resultados/POP_SSA_DS_BAIRRO_RACA_2000_2026_v5_1.xlsx` — planilha com metodologia, dicionário, checagens, POP_DS, POP_BAIRRO, reconciliação com a SESAB, validação e SETORES
- `resultados/populacao_salvador_ds_sexo_idade_2000_2026.csv.gz` e `POP_SSA_DS_SEXO_IDADE_SIMPLES_2000_2026_v5_1.xlsx` — DS × sexo × idade simples (0–100+), 65.448 linhas, totais por faixa idênticos à base principal
- `resultados/populacao_salvador_bairro_ds_idade_raca_2000_2026.csv.gz` — `ANO | DS | COD_BAIRRO | IDADE | FXET | SEXO | RACA | FREQ` (3.131.625 linhas com FREQ > 0), coerente com as duas tabelas acima
- `resultados/populacao_bairro_idade_raca_por_ano.zip` — a mesma tabela, um CSV por ano (abre no Excel), com nomes e dicionário
- `resultados/validacao_v5_1.csv` e `reconciliacao_sesab_2000_2025.csv`

## Método (resumo, versão 5)

- **Totais municipais:** Censo (2000, 2010, 2022); TCU/IBGE nos demais anos (2023: RIPSA; 2025–2026: IBGE Cidades).
- **Calibração censitária:** 2000, 2010 e 2022 fecham exatamente com o IBGE em sexo × idade, raça (SIDRA 136 e 3175), DS (2000) e bairros (2022).
- **Distribuição interna:** setores censitários de 2010 e 2022 nos limites atuais de bairro e DS (cada bairro com tendência própria); Razão Censitária com razões variáveis (2001–2009 entre 2000 e 2010; depois entre 2010 e 2022), IPF/raking e arredondamento controlado.
- **Diálogo com a SESAB:** iguais nos anos de censo; diferenças nos demais anos publicadas ano a ano.
- 12 Distritos Sanitários · 172 bairros (inclui Aquarius, Lei 9.778/2024, e Boa Vista do Lobato, Lei 9.919/2025) · 18 faixas etárias e idade simples · 5 categorias de raça/cor.

## Atualização anual (ex.: 2027)

1. Acrescente `2027,<total>,TCU/IBGE,0` em `dados/entrada/totais_municipais.csv`.
2. No R: `setwd("<pasta do repositório>")` e rode, em ordem, `R/04_atualizar_populacao.R`, `R/05_idade_simples.R`, `R/06_bairro_idade_raca.R` e `R/07_exportar_por_ano.R`.
3. Use `resultados/populacao_salvador_bairro_ds_2000_2027.csv` (TabNet/BI) e `resultados/populacao_bairro_idade_raca_por_ano.zip` (um arquivo por ano + dicionário).

## Estrutura

```
R/            scripts R (01/01b chaves setor-bairro-DS 2022/2010, 02 Aquarius, 03 estrutura base, 04–07 atualização anual, funcoes)
python/       implementação de referência (v3 a v5.1) e réplica de conferência do R
dados/
  entrada/    totais municipais, chaves de setores 2010 e 2022, SESAB 2010 e TabNet 2000–2025, SIDRA 136 e 3175, DS 2000, raça 2010, chave setores, população IBGE por bairro
  estrutura/  estruturas calibradas 2000, 2010 e 2022 por bairro × DS e idade simples — base da atualização anual
  dicionarios/ DS, FXET, SEXO, RACA, bairros
resultados/   base final, planilhas v5.1, zip por ano, validação, reconciliação SESAB, backtest
```

## Equipe

- Jessidenes Teixeira de Freitas Mendes Leal
- Rafaella Santiago Coutinho Santos

## Como citar

Leal JTFM, Santos RSC. Protocolo metodológico para estimativa populacional de Salvador por distrito sanitário, bairro, sexo, idade e raça/cor, 2000–2026 [Internet]. Salvador: Secretaria Municipal da Saúde de Salvador; 2026. doi:10.5281/zenodo.24096844

## Licença

Dados e documentação: CC BY 4.0. Código: MIT. Ver `LICENSE`.
