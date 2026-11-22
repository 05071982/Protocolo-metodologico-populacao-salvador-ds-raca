# 5. Comparação entre métodos

São três candidatos para estimar a população dos DS fora dos anos censitários.

| | Extrapolação de Lagrange | Razão Censitária fixa | **Razão Censitária com razões variáveis** |
|---|---|---|---|
| Ideia | polinômio que passa pelos pontos conhecidos | participação de 2010 × total do ano | participação interpolada/extrapolada entre 2010 e 2022 × total do ano |
| Fórmula | $P(t)=\sum_j P(t_j)\,L_j(t)$, com $L_j(t)=\prod_{k\neq j}\frac{t-t_k}{t_j-t_k}$ | $P_c(t)=T(t)\cdot s_c^{2010}$ | $P_c(t)=T(t)\cdot s_c(t)$, $s_c(t)\propto (s_c^{2010})^{1-w}(s_c^{2022})^{w}$ |
| Referência | Burden & Faires (2008) | Siegel & Swanson (2004) | Siegel & Swanson (2004); Smith, Tayman & Swanson (2013) |
| Soma = total oficial? | **não** | sim | sim |
| Valores negativos? | **sim** | não | não |
| Capta migração entre DS? | parcialmente (instável) | **não** | sim |
| Capta envelhecimento? | parcialmente | **não** | sim |
| Capta mudança de raça/cor? | — | **não** | sim |
| Funciona com 2.160 células e 194 unidades? | **não** (oscila) | sim | sim |

## 5.1 Teste fora da amostra: prever 2022 usando só dados até 2010

Fingimos que estamos em 2010 e tentamos prever a população de cada DS em 2022. Comparamos com o observado pelos setores do Censo 2022.

- **Razão fixa:** participação de 2010 × total de 2022.
- **Lagrange (2 pontos: 2000 e 2010):** polinômio de grau 1 extrapolado até 2022.
- **Lagrange calibrado:** o mesmo, reescalado para somar o total de 2022.
- **Razão variável:** participações de 2000 e 2010 interpoladas e extrapoladas até 2022 (w = 2,2) × total de 2022.

| DS | Observado 2022 | Razão fixa | Lagrange | Lagrange calibrado | **Razão variável** |
|---|---:|---:|---:|---:|---:|
| Centro Histórico | 52.741 | 64.767 | 70.977 | 58.077 | **57.110** |
| Itapagipe | 131.239 | 146.756 | 164.866 | 134.901 | **132.672** |
| São Caetano/Valéria | 215.362 | 234.413 | 297.308 | 243.270 | **243.888** |
| Liberdade | 137.381 | 161.416 | 172.632 | 141.255 | **139.037** |
| Brotas | 177.202 | 183.696 | 218.088 | 178.449 | **176.313** |
| Barra/Rio Vermelho | 298.671 | 305.681 | 347.421 | 284.276 | **279.707** |
| Boca do Rio | 124.113 | 114.710 | 153.954 | 125.972 | **129.085** |
| Itapuã | 300.070 | 226.104 | 311.338 | 254.750 | **264.531** |
| Cabula/Beiru | 327.120 | 347.030 | 442.766 | 362.291 | **363.887** |
| Pau da Lima | 203.224 | 199.238 | 251.156 | 205.507 | **205.655** |
| Subúrbio Ferroviário | 290.866 | 290.170 | 341.327 | 279.288 | **275.609** |
| Cajazeiras | 159.689 | 143.696 | 182.883 | 149.643 | **150.183** |
| **Soma** | **2.417.678** | 2.417.677 | **2.954.716** | 2.417.679 | 2.417.677 |

| Métrica | Razão fixa | Lagrange | Lagrange calibrado | **Razão variável** |
|---|---:|---:|---:|---:|
| Erro percentual absoluto médio (MAPE) | 9,8% | 23,5% | 6,1% | **5,8%** |
| Maior erro absoluto | 24,6% | 38,1% | 15,1% | **13,2%** |
| RMSE (pessoas) | 25.240 | 52.632 | 19.534 | **18.633** |

Arquivo: `resultados/backtest_metodos_ds_2022.csv`.

**Leitura:**

1. Lagrange puro erra o total em +537 mil pessoas (+22%), porque não respeita o total oficial.
2. A Razão fixa respeita o total, mas não acompanha a dinâmica: subestima Itapuã em 25% e superestima Liberdade e Centro Histórico em 18–23%.
3. A Razão variável tem o **menor erro em todas as métricas**. Mesmo comparada ao Lagrange recalibrado, que é uma melhoria que o método antigo não fazia, ela tem erro máximo menor e, sobretudo, as vantagens estruturais dos itens 5.2 e 5.3.

*Desde a v5*, os três anos estão nos **limites atuais** dos DS (2000: tabela DS 2000; 2010 e 2022: setores censitários). Os erros quase não mudaram em relação à versão anterior, em que 2010 seguia os limites da época, o que confirma que a mudança de limites tinha efeito pequeno.

## 5.2 Teste nas células: valores negativos

Extrapolando linearmente (Lagrange de 2 pontos, 2010 e 2022) cada uma das 2.160 células DS × sexo × faixa × raça:

| Ano | Células negativas (Lagrange) | Soma dos negativos | Razão variável |
|---|---:|---:|---|
| 2000 | 76 | −5.413 | 0 negativas |
| 2026 | 405 | −7.900 | 0 negativas |
| 2030 | 500 | −19.111 | 0 negativas |

No nível de bairro × DS (34.920 células), a extrapolação linear até 2026 gera 5.937 células negativas.

Isso acontece porque uma célula que diminuiu entre 2010 e 2022 continua diminuindo linearmente até passar de zero. Na forma geométrica, a participação nunca fica negativa e as células sempre somam 100%.

Com mais pontos (polinômio de grau maior), o problema piora: polinômios de grau alto oscilam nas bordas do intervalo (fenômeno de Runge; Runge, 1901), e as bordas são justamente os anos que queremos extrapolar.

## 5.3 Teste de estrutura: envelhecimento e raça

| Indicador (Salvador) | 2010 observado | 2022 observado | Razão fixa usada em 2022 | Razão variável em 2022 |
|---|---:|---:|---:|---:|
| % 60 anos ou mais | 9,3% | 16,6% | 9,3% | **16,6%** |
| % 0–4 anos | 6,2% | 5,1% | 6,2% | **5,1%** |
| % preta | 27,6% | 34,1% | 27,6% | **34,1%** |

Na razão variável os valores de 2022 coincidem com o observado **por construção**, porque 2022 é âncora. O ponto é o contrário: a Razão fixa, que era o método em uso, teria continuado aplicando a estrutura de 2010 até 2022 e depois. Ela congela a estrutura de 2010. Taxas de mortalidade por idade calculadas com esse denominador ficariam viesadas: a população idosa de 2022 estaria subestimada em 44% (9,3% contra 16,6% do total).

## 5.4 Por que razão variável e não outro método demográfico

| Alternativa | Por que não |
|---|---|
| Componentes demográficos (nascimentos, óbitos, migração por DS) | não há migração intramunicipal medida |
| Hamilton-Perry (razões de coorte; Hamilton & Perry, 1962) | exige estrutura etária fina em dois censos com a mesma geografia, o que 2010 não oferece por bairro |
| Regressão / razão-correlação (registros administrativos) | caminho para versões futuras, combinando a base com SIM/SINASC/CNES/cadastros (ver [Limitações](09-Limitacoes)) |

A razão variável usa **todo** o dado disponível (dois censos completos), é **coerente por construção** com os totais oficiais, **não produz negativos** e é **simples de atualizar**: basta acrescentar o total do novo ano.
