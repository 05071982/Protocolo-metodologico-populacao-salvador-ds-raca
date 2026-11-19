# 6. Resultados

Arquivos em `resultados/`:

- `POP_SSA_DS_BAIRRO_RACA_2000_2026_v4.xlsx`, com as abas LEIAME, METODOLOGIA, LIMITACOES, DICIONARIO, TOTAIS, CHECAGENS, POP_DS, **POP_BAIRRO**, RECONCILIACAO_SESAB, VALIDACAO e SETORES;
- `populacao_salvador_bairro_ds_2000_2026.csv.gz`, a tabela oficial `ANO | DS | COD_BAIRRO | FXET | SEXO | RACA | FREQ` (947.700 linhas: 942.840 das 194 unidades bairro × DS mais 4.860 linhas zeradas do bairro 2 – Aeroporto, para que os 171 bairros estejam presentes);
- `populacao_bairro_idade_raca_por_ano.zip`, com um CSV por ano (idade detalhada, com nomes de DS e bairro), o dicionário (`DICIONARIO.xlsx` e `dicionario_bairros.csv`), `VALIDACAO_v4.csv` e `RECONCILIACAO_SESAB_2000_2025.csv`;
- `validacao_v4.csv` e `reconciliacao_sesab_2000_2025.csv`.

## 6.1 População por DS

| DS | 2000 | 2005 | 2010 | 2015 | 2022 | 2025 | 2026 |
|:--|--:|--:|--:|--:|--:|--:|--:|
| Centro Histórico | 72.262 | 75.489 | 71.870 | 72.216 | 52.741 | 53.026 | 51.968 |
| Itapagipe | 160.374 | 169.033 | 162.416 | 169.972 | 131.240 | 134.799 | 133.090 |
| São Caetano/Valéria | 227.858 | 253.347 | 257.463 | 272.388 | 215.362 | 223.558 | 221.541 |
| Liberdade | 183.647 | 189.849 | 179.427 | 182.825 | 137.381 | 139.706 | 137.504 |
| Brotas | 190.971 | 206.189 | 203.296 | 219.509 | 177.201 | 185.373 | 184.138 |
| Barra/Rio Vermelho | 330.697 | 350.407 | 338.921 | 367.552 | 298.671 | 313.383 | 311.646 |
| Boca do Rio | 104.447 | 120.294 | 126.328 | 143.437 | 124.113 | 133.907 | 134.385 |
| Itapuã | 199.307 | 233.681 | 250.230 | 308.340 | 300.070 | 340.056 | 346.940 |
| Cabula/Beiru | 335.138 | 376.227 | 385.854 | 410.048 | 327.120 | 341.983 | 339.910 |
| Pau da Lima | 194.950 | 216.035 | 218.706 | 241.906 | 203.224 | 216.524 | 216.437 |
| Subúrbio Ferroviário | 304.305 | 327.354 | 322.116 | 351.477 | 290.866 | 307.938 | 307.166 |
| Cajazeiras | 139.151 | 155.652 | 159.029 | 181.417 | 159.689 | 173.951 | 175.220 |
| **Salvador** | **2.443.107** | **2.673.557** | **2.675.656** | **2.921.087** | **2.417.678** | **2.564.204** | **2.559.945** |

2000, 2010 e 2022 têm total censitário; os demais anos têm total TCU/IBGE. Em 2000, o total de cada DS é o da tabela DS 2000 (v4). A queda de 2009 para 2010 e o salto de 2006 para 2007 vêm de quebras nos totais TCU, não de variação real (use `FREQ_CENSO` para tendência).

## 6.2 Nova base × base antiga do TabNet (2025)

| DS | Antiga (razão fixa / Lagrange) | Nova | Diferença |
|:--|--:|--:|--:|
| Centro Histórico | 68.455 | 53.026 | −22,5% |
| Itapagipe | 154.698 | 134.799 | −12,9% |
| São Caetano/Valéria | 245.233 | 223.558 | −8,8% |
| Liberdade | 170.907 | 139.706 | −18,3% |
| Brotas | 193.641 | 185.373 | −4,3% |
| Barra/Rio Vermelho | 322.822 | 313.383 | −2,9% |
| Boca do Rio | 120.324 | 133.907 | +11,3% |
| **Itapuã** | 238.348 | 340.056 | **+42,7%** |
| Cabula/Beiru | 367.520 | 341.983 | −6,9% |
| Pau da Lima | 208.322 | 216.524 | +3,9% |
| Subúrbio Ferroviário | 306.816 | 307.938 | +0,4% |
| Cajazeiras | 151.474 | 173.951 | +14,8% |

**Impacto nos indicadores:** as taxas do Centro Histórico e da Liberdade vão **subir**, porque o denominador antigo estava inflado. As de Itapuã, Cajazeiras e Boca do Rio vão **cair**: Itapuã tinha 100 mil habitantes a menos no denominador.

## 6.3 Composição por raça/cor, 2022 (%)

| DS | Branca | Preta | Amarela | Parda | Indígena | **Negra** |
|:--|--:|--:|--:|--:|--:|--:|
| Centro Histórico | 24,2 | 28,1 | 0,2 | 47,0 | 0,4 | 75,2 |
| Itapagipe | 12,7 | 34,0 | 0,1 | 53,1 | 0,2 | 87,0 |
| São Caetano/Valéria | 9,4 | 38,2 | 0,1 | 52,2 | 0,1 | 90,4 |
| Liberdade | 10,2 | 39,5 | 0,0 | 50,1 | 0,2 | 89,6 |
| Brotas | 24,0 | 30,6 | 0,1 | 45,0 | 0,2 | 75,6 |
| Barra/Rio Vermelho | 33,3 | 25,9 | 0,2 | 40,4 | 0,2 | 66,3 |
| Boca do Rio | 28,5 | 22,4 | 0,2 | 48,6 | 0,3 | 71,0 |
| Itapuã | 18,6 | 31,6 | 0,1 | 49,5 | 0,2 | 81,1 |
| Cabula/Beiru | 12,1 | 37,1 | 0,3 | 50,0 | 0,4 | 87,1 |
| Pau da Lima | 11,7 | 37,2 | 0,1 | 50,8 | 0,2 | 88,0 |
| Subúrbio Ferroviário | 8,6 | 39,4 | 0,1 | 51,8 | 0,1 | 91,2 |
| Cajazeiras | 9,6 | 39,0 | 0,1 | 51,2 | 0,2 | 90,1 |
| **Salvador** | **16,6** | **34,1** | **0,1** | **49,0** | **0,2** | **83,1** |

### Raça/cor em 2010 (universo, SIDRA 3175) e 2000 (amostra, SIDRA 136), %

**2010**

| DS | Branca | Preta | Amarela | Parda | Indígena | **Negra** |
|:--|--:|--:|--:|--:|--:|--:|
| Centro Histórico | 28,6 | 20,9 | 1,1 | 49,0 | 0,4 | 69,9 |
| Itapagipe | 14,9 | 27,0 | 0,8 | 57,1 | 0,2 | 84,1 |
| São Caetano/Valéria | 11,8 | 31,4 | 1,5 | 55,0 | 0,3 | 86,4 |
| Liberdade | 13,4 | 32,2 | 1,2 | 52,9 | 0,3 | 85,1 |
| Brotas | 22,4 | 26,8 | 1,1 | 49,3 | 0,3 | 76,2 |
| Barra/Rio Vermelho | 36,0 | 21,1 | 1,1 | 41,6 | 0,3 | 62,7 |
| Boca do Rio | 28,8 | 20,9 | 1,2 | 48,8 | 0,3 | 69,7 |
| Itapuã | 21,4 | 25,9 | 1,5 | 51,0 | 0,2 | 76,9 |
| Cabula/Beiru | 15,6 | 29,3 | 1,5 | 53,4 | 0,2 | 82,7 |
| Pau da Lima | 14,9 | 30,0 | 1,5 | 53,4 | 0,3 | 83,4 |
| Subúrbio Ferroviário | 11,1 | 31,2 | 1,7 | 55,6 | 0,3 | 86,9 |
| Cajazeiras | 12,9 | 31,5 | 1,4 | 53,9 | 0,3 | 85,4 |
| **Salvador** | **18,9** | **27,8** | **1,3** | **51,7** | **0,3** | **79,5** |

**2000**

| DS | Branca | Preta | Amarela | Parda | Indígena | **Negra** |
|:--|--:|--:|--:|--:|--:|--:|
| Centro Histórico | 33,4 | 15,1 | 0,3 | 50,4 | 0,9 | 65,4 |
| Itapagipe | 18,5 | 20,0 | 0,2 | 60,9 | 0,5 | 80,8 |
| São Caetano/Valéria | 15,2 | 23,5 | 0,3 | 60,1 | 0,9 | 83,6 |
| Liberdade | 17,0 | 24,2 | 0,3 | 57,6 | 0,9 | 81,8 |
| Brotas | 27,4 | 19,7 | 0,2 | 51,9 | 0,9 | 71,5 |
| Barra/Rio Vermelho | 41,5 | 15,1 | 0,2 | 42,4 | 0,8 | 57,5 |
| Boca do Rio | 34,2 | 14,8 | 0,2 | 49,8 | 0,9 | 64,7 |
| Itapuã | 26,0 | 18,9 | 0,3 | 54,1 | 0,7 | 73,0 |
| Cabula/Beiru | 19,7 | 21,7 | 0,3 | 57,5 | 0,7 | 79,2 |
| Pau da Lima | 18,9 | 22,2 | 0,3 | 57,7 | 0,8 | 80,0 |
| Subúrbio Ferroviário | 14,5 | 23,5 | 0,4 | 60,9 | 0,7 | 84,4 |
| Cajazeiras | 16,6 | 23,5 | 0,3 | 58,7 | 0,8 | 82,3 |
| **Salvador** | **23,2** | **20,5** | **0,3** | **55,2** | **0,8** | **75,7** |

Em Salvador, a população negra passou de 75,7% (2000) para 79,5% (2010) e 83,1% (2022). A autodeclaração preta subiu de 20,5% para 27,8% e 34,1%. A distribuição por DS em 2000 usa a interação DS × raça de 2010, ajustada ao total de raça de 2000.

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
| Itapuã | 60.966 |
| Pituba (sem Aquarius) | 53.057 |
| Pernambués | 52.570 |
| Paripe | 52.461 |
| Brotas | 51.300 |
| São Cristóvão | 47.417 |
| Fazenda Grande do Retiro | 41.050 |
| São Caetano | 40.313 |
| Boca do Rio | 39.258 |
| Beiru/Tancredo Neves | 38.338 |

Aquarius (171): 4.835 habitantes em 2022. Aeroporto (2): sem população residente, presente nas bases com FREQ = 0. 23 bairros têm território em mais de um DS.

## 6.6 Conferências automáticas (aba CHECAGENS)

| Conferência | Resultado |
|---|---|
| Total 2000, 2010 e 2022 = Censo | OK |
| Total 2014 = TCU (2.902.927); total 2025 = IBGE Cidades (2.564.204) | OK |
| DS 2010 = tabela SESAB (por DS, sexo e faixa), tolerância 2 pessoas | OK |
| 2000 e 2022: sexo × faixa = Censo; 2000: DS = tabela DS 2000 | OK |
| Soma dos bairros 2022 = IBGE (2.417.678) | OK |
| Soma POP_BAIRRO por DS = POP_DS (todos os anos) | OK |
| Valores negativos | nenhum |


A lista completa de conferências da v4 (raça, idades simples, 171 bairros, consistência entre tabelas) está em [Diálogo entre bases](13-Dialogo-entre-bases#136-validação-da-versão-4-resultadosvalidacao_v4csv).
