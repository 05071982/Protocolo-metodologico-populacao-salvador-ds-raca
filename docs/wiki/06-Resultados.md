# 6. Resultados

Arquivos em `resultados/`:

- `POP_SSA_DS_BAIRRO_RACA_2000_2026_v5.xlsx`, com as abas LEIAME, METODOLOGIA, LIMITACOES, DICIONARIO, TOTAIS, CHECAGENS, POP_DS, **POP_BAIRRO**, RECONCILIACAO_SESAB, VALIDACAO e SETORES;
- `populacao_salvador_bairro_ds_2000_2026.csv.gz`, a tabela oficial `ANO | DS | COD_BAIRRO | FXET | SEXO | RACA | FREQ` (947.700 linhas: 942.840 das 194 unidades bairro × DS mais 4.860 linhas zeradas do bairro 2 – Aeroporto, para que os 171 bairros estejam presentes);
- `populacao_bairro_idade_raca_por_ano.zip`, com um CSV por ano (idade detalhada, com nomes de DS e bairro), o dicionário (`DICIONARIO.xlsx` e `dicionario_bairros.csv`), `VALIDACAO_v4.csv` e `RECONCILIACAO_SESAB_2000_2025.csv`;
- `validacao_v5.csv` e `reconciliacao_sesab_2000_2025.csv`.

## 6.1 População por DS

| DS | 2000 | 2005 | 2010 | 2015 | 2022 | 2025 | 2026 |
|:--|--:|--:|--:|--:|--:|--:|--:|
| Centro Histórico | 72.262 | 75.435 | 71.678 | 72.294 | 52.741 | 53.178 | 52.187 |
| Itapagipe | 160.374 | 169.041 | 162.416 | 170.911 | 131.239 | 135.008 | 133.388 |
| São Caetano/Valéria | 227.858 | 254.280 | 259.426 | 273.318 | 215.362 | 223.205 | 221.089 |
| Liberdade | 183.647 | 189.344 | 178.640 | 183.510 | 137.381 | 139.899 | 137.744 |
| Brotas | 190.971 | 206.146 | 203.297 | 219.315 | 177.202 | 185.580 | 184.429 |
| Barra/Rio Vermelho | 330.697 | 350.154 | 338.299 | 368.102 | 298.671 | 313.420 | 311.683 |
| Boca do Rio | 104.447 | 120.524 | 126.950 | 144.068 | 124.113 | 133.793 | 134.258 |
| Itapuã | 199.307 | 233.688 | 250.230 | 302.018 | 300.070 | 339.632 | 346.342 |
| Cabula/Beiru | 335.138 | 375.384 | 384.060 | 409.709 | 327.120 | 341.917 | 339.775 |
| Pau da Lima | 194.950 | 216.957 | 220.498 | 243.832 | 203.224 | 216.085 | 215.839 |
| Subúrbio Ferroviário | 304.305 | 326.873 | 321.133 | 352.680 | 290.866 | 308.329 | 307.705 |
| Cajazeiras | 139.151 | 155.731 | 159.029 | 181.330 | 159.689 | 174.158 | 175.506 |
| **Salvador** | **2.443.107** | **2.673.557** | **2.675.656** | **2.921.087** | **2.417.678** | **2.564.204** | **2.559.945** |

2000, 2010 e 2022 têm total censitário; os demais anos têm total TCU/IBGE. Em 2000, o total de cada DS é o da tabela DS 2000; em 2010, a soma dos setores nos limites atuais (v5). A queda de 2009 para 2010 e o salto de 2006 para 2007 vêm de quebras nos totais TCU, não de variação real (use `FREQ_CENSO` para tendência).

## 6.2 Nova base × base antiga do TabNet (2025)

| DS | Antiga (razão fixa / Lagrange) | Nova | Diferença |
|:--|--:|--:|--:|
| Centro Histórico | 68.455 | 53.178 | −22,3% |
| Itapagipe | 154.698 | 135.008 | −12,7% |
| São Caetano/Valéria | 245.233 | 223.205 | −9,0% |
| Liberdade | 170.907 | 139.899 | −18,1% |
| Brotas | 193.641 | 185.580 | −4,2% |
| Barra/Rio Vermelho | 322.822 | 313.420 | −2,9% |
| Boca do Rio | 120.324 | 133.793 | +11,2% |
| **Itapuã** | 238.348 | 339.632 | **+42,5%** |
| Cabula/Beiru | 367.520 | 341.917 | −7,0% |
| Pau da Lima | 208.322 | 216.085 | +3,7% |
| Subúrbio Ferroviário | 306.816 | 308.329 | +0,5% |
| Cajazeiras | 151.474 | 174.158 | +15,0% |

**Impacto nos indicadores:** as taxas do Centro Histórico e da Liberdade vão **subir**, porque o denominador antigo estava inflado. As de Itapuã, Cajazeiras e Boca do Rio vão **cair**: Itapuã tinha 100 mil habitantes a menos no denominador.

## 6.3 Composição por raça/cor, 2022 (%)

| DS | Branca | Preta | Amarela | Parda | Indígena | **Negra** |
|:--|--:|--:|--:|--:|--:|--:|
| Centro Histórico | 24,2 | 28,2 | 0,2 | 47,1 | 0,4 | 75,2 |
| Itapagipe | 12,7 | 34,0 | 0,1 | 53,1 | 0,2 | 87,1 |
| São Caetano/Valéria | 9,4 | 38,2 | 0,0 | 52,2 | 0,1 | 90,4 |
| Liberdade | 10,2 | 39,5 | 0,0 | 50,1 | 0,2 | 89,6 |
| Brotas | 24,0 | 30,6 | 0,1 | 45,0 | 0,2 | 75,7 |
| Barra/Rio Vermelho | 33,3 | 25,9 | 0,2 | 40,5 | 0,2 | 66,3 |
| Boca do Rio | 28,5 | 22,4 | 0,2 | 48,6 | 0,3 | 71,0 |
| Itapuã | 18,6 | 31,6 | 0,1 | 49,5 | 0,2 | 81,1 |
| Cabula/Beiru | 12,2 | 37,2 | 0,3 | 50,0 | 0,4 | 87,1 |
| Pau da Lima | 11,7 | 37,2 | 0,1 | 50,8 | 0,2 | 88,0 |
| Subúrbio Ferroviário | 8,6 | 39,4 | 0,1 | 51,8 | 0,1 | 91,2 |
| Cajazeiras | 9,6 | 39,0 | 0,1 | 51,2 | 0,2 | 90,1 |
| **Salvador** | **16,6** | **34,1** | **0,1** | **49,0** | **0,2** | **83,1** |

### Raça/cor em 2010 (universo, setores censitários) e 2000 (amostra, SIDRA 136), %

**2010**

| DS | Branca | Preta | Amarela | Parda | Indígena | **Negra** |
|:--|--:|--:|--:|--:|--:|--:|
| Centro Histórico | 29,5 | 20,2 | 1,1 | 48,8 | 0,4 | 68,9 |
| Itapagipe | 15,7 | 26,1 | 0,8 | 57,2 | 0,2 | 83,3 |
| São Caetano/Valéria | 12,1 | 31,1 | 1,4 | 55,1 | 0,3 | 86,2 |
| Liberdade | 13,7 | 32,1 | 1,3 | 52,6 | 0,3 | 84,7 |
| Brotas | 23,8 | 25,5 | 1,1 | 49,2 | 0,3 | 74,8 |
| Barra/Rio Vermelho | 35,5 | 21,6 | 1,0 | 41,5 | 0,3 | 63,2 |
| Boca do Rio | 29,3 | 20,7 | 1,2 | 48,4 | 0,3 | 69,2 |
| Itapuã | 20,6 | 26,4 | 1,3 | 51,4 | 0,3 | 77,7 |
| Cabula/Beiru | 14,6 | 30,2 | 1,5 | 53,5 | 0,3 | 83,7 |
| Pau da Lima | 14,7 | 30,3 | 1,6 | 53,1 | 0,3 | 83,5 |
| Subúrbio Ferroviário | 11,4 | 31,0 | 1,8 | 55,6 | 0,2 | 86,6 |
| Cajazeiras | 13,1 | 31,0 | 1,5 | 54,2 | 0,3 | 85,1 |
| **Salvador** | **18,9** | **27,8** | **1,3** | **51,7** | **0,3** | **79,5** |

**2000**

| DS | Branca | Preta | Amarela | Parda | Indígena | **Negra** |
|:--|--:|--:|--:|--:|--:|--:|
| Centro Histórico | 34,2 | 14,4 | 0,3 | 50,0 | 1,1 | 64,4 |
| Itapagipe | 19,4 | 19,2 | 0,2 | 60,6 | 0,6 | 79,9 |
| São Caetano/Valéria | 15,7 | 23,2 | 0,3 | 60,0 | 0,8 | 83,2 |
| Liberdade | 17,5 | 24,1 | 0,3 | 57,2 | 0,8 | 81,3 |
| Brotas | 28,7 | 18,6 | 0,2 | 51,6 | 0,8 | 70,2 |
| Barra/Rio Vermelho | 40,9 | 15,6 | 0,2 | 42,5 | 0,8 | 58,1 |
| Boca do Rio | 34,6 | 14,8 | 0,3 | 49,5 | 0,8 | 64,3 |
| Itapuã | 25,1 | 19,4 | 0,3 | 54,5 | 0,7 | 73,9 |
| Cabula/Beiru | 18,4 | 22,5 | 0,3 | 58,0 | 0,8 | 80,5 |
| Pau da Lima | 18,7 | 22,6 | 0,4 | 57,5 | 0,8 | 80,1 |
| Subúrbio Ferroviário | 14,8 | 23,3 | 0,4 | 60,8 | 0,7 | 84,1 |
| Cajazeiras | 16,9 | 23,1 | 0,3 | 58,9 | 0,7 | 82,0 |
| **Salvador** | **23,2** | **20,5** | **0,3** | **55,2** | **0,8** | **75,7** |

Em Salvador, a população negra passou de 75,7% (2000) para 79,5% (2010) e 83,1% (2022). A autodeclaração preta subiu de 20,5% para 27,8% e 34,1%. Desde a v5, a raça de 2010 por DS vem do universo, setor a setor. A distribuição por DS em 2000 usa a interação bairro × raça de 2010, ajustada ao total de raça de 2000.

## 6.4 Estrutura etária, Salvador (%)

| Ano | 0–4 | 5–14 | 15–29 | 30–59 | 60+ |
|--:|--:|--:|--:|--:|--:|
| 2000 | 8,5 | 17,6 | 32,1 | 35,0 | 6,8 |
| 2010 | 6,2 | 14,5 | 28,2 | 41,9 | 9,3 |
| 2022 | 5,1 | 11,7 | 20,7 | 46,0 | 16,5 |

Os três anos são idênticos aos censos. Razão de sexo: 89,0 (2000), 87,5 (2010) e 83,8 (2022) homens para cada 100 mulheres.

## 6.5 Bairros mais populosos, 2022

| Bairro | População |
|:--|--:|
| Itapuã | 60.968 |
| Pituba | 53.055 |
| Pernambués | 52.564 |
| Paripe | 52.469 |
| Brotas | 51.296 |
| São Cristóvão | 47.408 |
| Fazenda Grande do Retiro | 41.056 |
| São Caetano | 40.303 |
| Boca do Rio | 39.262 |
| Beiru/Tancredo Neves | 38.329 |

Aquarius (171): 3.248 habitantes em 2010 (área atual do bairro) e 4.839 em 2022. Aeroporto (2): sem população residente, presente nas bases com FREQ = 0. 23 bairros têm território em mais de um DS.

## 6.6 Conferências automáticas (aba CHECAGENS)

| Conferência | Resultado |
|---|---|
| Total 2000, 2010 e 2022 = Censo | OK |
| Total 2014 = TCU (2.902.927); total 2025 = IBGE Cidades (2.564.204) | OK |
| Bairros 2010 = soma dos setores censitários; DS 2010 × tabela SESAB (limites da época): até 0,8% | OK |
| 2000 e 2022: sexo × faixa = Censo; 2000: DS = tabela DS 2000 | OK |
| Soma dos bairros 2022 = IBGE (2.417.678) | OK |
| Soma POP_BAIRRO por DS = POP_DS (todos os anos) | OK |
| Valores negativos | nenhum |


A lista completa de conferências da v5 (raça, idades simples, 171 bairros, consistência entre tabelas) está em [Diálogo entre bases](13-Dialogo-entre-bases#136-validação-da-versão-4-resultadosvalidacao_v4csv).
