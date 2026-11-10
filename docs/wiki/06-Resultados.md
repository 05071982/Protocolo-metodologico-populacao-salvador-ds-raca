# 6. Resultados

Arquivos em `resultados/`:

- `POP_SSA_DS_BAIRRO_RACA_2000_2026_v3.xlsx`, com as abas LEIAME, METODOLOGIA, LIMITACOES, DICIONARIO, TOTAIS, CHECAGENS, POP_DS, **POP_BAIRRO** e SETORES;
- `populacao_salvador_bairro_ds_2000_2026.csv.gz`, a tabela oficial `ANO | DS | COD_BAIRRO | FXET | SEXO | RACA | FREQ` (942.840 linhas).

## 6.1 População por DS

| DS | 2000 | 2010 | 2015 | 2022 | 2025 | 2026 |
|:--|--:|--:|--:|--:|--:|--:|
| Centro Histórico | 73.042 | 71.870 | 72.230 | 52.744 | 53.004 | 51.940 |
| Itapagipe | 152.524 | 162.416 | 169.963 | 131.238 | 134.798 | 133.093 |
| São Caetano/Valéria | 264.961 | 257.463 | 272.350 | 215.363 | 223.594 | 221.589 |
| Liberdade | 199.959 | 179.428 | 182.814 | 137.380 | 139.713 | 137.504 |
| Brotas | 179.936 | 203.297 | 219.555 | 177.203 | 185.362 | 184.128 |
| Barra/Rio Vermelho | 294.122 | 338.921 | 367.615 | 298.673 | 313.273 | 311.463 |
| Boca do Rio | 99.810 | 126.328 | 143.475 | 124.116 | 133.863 | 134.343 |
| Itapuã | 175.606 | 250.230 | 308.342 | 300.064 | 340.034 | 346.923 |
| Cabula/Beiru | 353.818 | 385.852 | 410.031 | 327.117 | 342.030 | 339.955 |
| Pau da Lima | 195.479 | 218.706 | 241.900 | 203.228 | 216.545 | 216.463 |
| Subúrbio Ferroviário | 316.827 | 322.116 | 351.411 | 290.861 | 308.003 | 307.270 |
| Cajazeiras | 137.023 | 159.029 | 181.401 | 159.691 | 173.985 | 175.274 |
| **Salvador** | **2.443.107** | **2.675.656** | **2.921.087** | **2.417.678** | **2.564.204** | **2.559.945** |

2000, 2010 e 2022 têm total censitário; os demais anos têm total TCU/IBGE.

## 6.2 Nova base × base antiga do TabNet (2025)

| DS | Antiga (razão fixa / Lagrange) | Nova | Diferença |
|:--|--:|--:|--:|
| Centro Histórico | 68.455 | 53.004 | −22,6% |
| Itapagipe | 154.698 | 134.798 | −12,9% |
| São Caetano/Valéria | 245.233 | 223.594 | −8,8% |
| Liberdade | 170.907 | 139.713 | −18,3% |
| Brotas | 193.641 | 185.362 | −4,3% |
| Barra/Rio Vermelho | 322.822 | 313.273 | −3,0% |
| Boca do Rio | 120.324 | 133.863 | +11,3% |
| **Itapuã** | 238.348 | 340.034 | **+42,7%** |
| Cabula/Beiru | 367.520 | 342.030 | −6,9% |
| Pau da Lima | 208.322 | 216.545 | +3,9% |
| Subúrbio Ferroviário | 306.816 | 308.003 | +0,4% |
| Cajazeiras | 151.474 | 173.985 | +14,9% |

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

## 6.4 Estrutura etária, Salvador (%)

| Ano | 0–4 | 5–14 | 15–29 | 30–59 | 60+ |
|--:|--:|--:|--:|--:|--:|
| 2010 | 6,2 | 14,5 | 28,2 | 41,9 | 9,3 |
| 2022 | 5,1 | 11,7 | 20,7 | 45,9 | 16,6 |

Razão de sexo em 2022: 83,5 homens para cada 100 mulheres.

## 6.5 Bairros mais populosos, 2022

| Bairro | População |
|:--|--:|
| Itapuã | 60.965 |
| Pituba (sem Aquarius) | 53.066 |
| Pernambués | 52.567 |
| Paripe | 52.466 |
| Brotas | 51.305 |
| São Cristóvão | 47.417 |
| Fazenda Grande do Retiro | 41.057 |
| São Caetano | 40.310 |
| Boca do Rio | 39.261 |
| Beiru/Tancredo Neves | 38.340 |

Aquarius (171): 4.837 habitantes em 2022. 23 bairros têm território em mais de um DS.

## 6.6 Conferências automáticas (aba CHECAGENS)

| Conferência | Resultado |
|---|---|
| Total 2000, 2010 e 2022 = Censo | OK |
| Total 2014 = TCU (2.902.927); total 2025 = IBGE Cidades (2.564.204) | OK |
| DS 2010 = tabela SESAB (por DS, sexo e faixa) | OK |
| Soma dos bairros 2022 = IBGE (2.417.678) | OK |
| Soma POP_BAIRRO por DS = POP_DS (todos os anos) | OK |
| Valores negativos | nenhum |
