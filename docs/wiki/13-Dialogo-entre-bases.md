# 13. Diálogo entre bases: IBGE, SESAB e Município (versões 4 e 5)

Uma crítica frequente às estimativas municipais é a falta de diálogo entre a população do IBGE, a da SESAB e a do município. A versão 4 respondeu a essa crítica, e a versão 5 a completou com os setores de 2010, com uma **hierarquia explícita de fontes**: cada fonte manda no nível em que é a melhor informação disponível, e as diferenças que sobram são publicadas.

## 13.1 Por que alinhar não quebra o método dos setores

O método tem dois níveis independentes:

- **Quanto existe no município** (totais e margens): vem do IBGE.
- **Como a população se distribui dentro de Salvador** (DS, bairro e os cruzamentos de idade, sexo e raça): vem dos setores censitários.

O alinhamento é feito por **ajuste proporcional iterativo** (IPF/raking; Deming & Stephan, 1940). Entre todas as tabelas que respeitam as margens oficiais, o IPF escolhe a que **muda o mínimo possível** a tabela de partida, no sentido da informação de Kullback-Leibler (Ireland & Kullback, 1968). Na prática, as razões internas são preservadas: se o Cabula/Beiru tinha proporcionalmente mais jovens pretos que a Barra, isso continua valendo depois do ajuste. Só o nível muda. Na literatura, isso se chama *benchmarking* ou calibração hierárquica de estimativas para pequenas áreas (Swanson & Tayman, 2012).

## 13.2 Hierarquia de fontes

| Nível | Fonte que manda | Anos |
|---|---|---|
| 1. Total do município | Censo (IBGE) | 2000, 2010, 2022 |
| | Estimativa TCU/IBGE (2023 = RIPSA; 2025–2026 = IBGE Cidades) | demais anos |
| 2. Sexo × faixa etária do município | Censo 2000 e Censo 2022 (TabNet SESAB = Censo); universo 2010 (SIDRA 3175) | 2000, 2010, 2022 |
| | Idades simples 0–19 (2000 e 2022) e 0–100+ (2010) | 2000, 2010, 2022 |
| 3. Raça/cor do município | Censo 2000, amostra (SIDRA 136); universo 2010 por sexo e idade (SIDRA 3175); universo 2022 (setores) | 2000, 2010, 2022 |
| 4. Total por DS e por bairro | Tabela DS 2000 (mesmos limites atuais); setores 2010 (v5); setores 2022 e população por bairro do IBGE | 2000, 2010, 2022 |
| 5. Bairro e cruzamentos internos | Setores censitários 2010 e 2022, nos limites atuais | todos |
| Tabela SESAB por DS de 2010 (limites da época) | comparação: diferença máxima de 0,8% | 2010 |
| SESAB fora dos censos | **comparação publicada**, não ajuste | 2001–2009, 2011–2021, 2023–2025 |

"Sem declaração" de raça (2000: 16.749 pessoas; 2010: 402 no universo) foi redistribuída proporcionalmente entre as cinco categorias, dentro de cada sexo e idade em 2010 e no total em 2000.

## 13.3 Calibração de cada censo

**2010 (v5).** Ponto de partida: os 3.546 setores do universo agregados nas 195 unidades bairro × DS (ver [página 14](14-Versao-5-setores-2010)). Margens:

1. população de cada unidade por sexo = soma dos setores;
2. sexo × faixa × raça do município = universo SIDRA 3175.

Inteiros por arredondamento controlado com as duas margens exatas. Na v4, 2010 partia da tabela SESAB por DS (limites da época) e de um banco com 78% de cobertura.

**2022.** Ponto de partida: as unidades bairro × DS da v3 (194; a 195ª, Boa Vista do Lobato, é desmembrada depois da calibração), vindas dos setores. Margens:

1. total de cada unidade = total oficial IBGE do bairro;
2. unidade × raça = setores (raça do Censo 2022);
3. sexo × faixa do município = Censo 2022.

Os cruzamentos unidade × sexo × 11 faixas × raça dos setores mudaram no máximo 1,4%: o ajuste só corrigiu a abertura das 11 faixas censitárias nas 18 faixas.

**2000.** O Censo 2000 entra **apenas nas margens do município e dos DS**. A distribuição interna continua sendo a dos censos 2010 e 2022, conforme a regra do projeto. Ponto de partida: a estrutura calibrada de 2010. Margens:

1. total por DS = tabela DS 2000;
2. sexo × faixa = Censo 2000;
3. raça = SIDRA 136.

Inteiros com as três margens exatas.

## 13.4 O que isso muda na série

- **2001–2009 passam a ser interpolação, não extrapolação.** Antes, esses anos eram a tendência 2010–2022 prolongada para trás. Isso produzia 21% a menos de crianças de 0 a 4 anos e 50% a mais de adultos de 25 a 29 em 2000, comparado ao Censo 2000. Agora, $s_c(t) \propto (s_c^{2000})^{1-w}(s_c^{2010})^{w}$, com $w=(t-2000)/10$, e a raça também é interpolada.
- **2011 em diante:** mesma fórmula da v3 (2010→2022). As diferenças para a v3 ficaram abaixo de 0,05% por DS, por causa do ajuste fino de 2010 e 2022.
- **Anos censitários:** fecham exatamente com o IBGE em todas as margens listadas acima.

## 13.5 Reconciliação com a SESAB (`resultados/reconciliacao_sesab_2000_2025.csv`)

A dissimilaridade é o percentual da população que teria de mudar de célula sexo × faixa para a estrutura da base ficar igual à da SESAB (0 = idênticas).

| Período | Total | Dissimilaridade | Interpretação |
|---|---|---|---|
| 2000, 2010, 2022 | igual | **0%** | ambos são o Censo |
| 2001–2006 | igual, exceto ±200 pessoas em 2001–2002 (arquivo TCU) | 1% a 6,5% | a SESAB repete a estrutura de 2000 e não incorpora o envelhecimento |
| 2007 | base 5% maior | 3,2% | a SESAB usa a projeção UNFPA/IBGE (2.754.946); a base usa o TCU (2.892.625) |
| 2008–2009 | igual | ≈3,3% | projeções UNFPA/IBGE |
| 2011–2019 | igual (±10 pessoas) | 1% a 10% | a SESAB repete a estrutura de 2010 |
| 2020–2021 | igual | 3,5% a 4,4% | estrutura SESAB mais recente |
| 2023 | base 7% maior | 1,2% | a SESAB repete o Censo 2022; a base usa a RIPSA (2.589.296) |
| 2024–2025 | igual | 2,4% a 3,6% | |

Fora dos censos, **forçar a base a seguir a SESAB pioraria a qualidade**. A estrutura etária da SESAB fica quase parada entre censos e se afasta até 10% em 2019, e mesmo assim a base reencontra o Censo 2022 quando ele chega. Por isso a SESAB é usada como comparação, não como total. Quem precisar dos números da SESAB tem a tabela de reconciliação ano a ano.

## 13.6 Validação (`resultados/validacao_v5_1.csv`)

| Conferência | Resultado |
|---|---|
| Total de cada ano = total oficial | OK |
| 2000: DS = tabela DS 2000; sexo × faixa = Censo 2000; raça = SIDRA 136; idades 0–19 = Censo 2000 | OK |
| 2010: sexo × faixa × raça e idade simples 0–100+ = SIDRA 3175; bairros × DS por sexo = soma dos setores | OK |
| 2022: sexo × faixa e idades 0–19 = Censo 2022; bairros = IBGE (origens do 172 somadas à parte transferida) | OK |
| 2022: Boa Vista do Lobato (172) = parte transferida (5.519 + 501 + 199 = 6.219) | OK |
| Tabela detalhada (idade) = POP_BAIRRO = DS × idade, em todas as células | OK |
| 172 bairros no dicionário e nas bases (2 – Aeroporto com FREQ = 0) | OK |
| Valores negativos | nenhum |
| R (04 e 05) reproduz a referência Python, inclusive com um ano 2027 de teste | 0 células diferentes (v5 e v5.1) |

## 13.7 Referências desta página

- Deming WE, Stephan FF. On a least squares adjustment of a sampled frequency table when the expected marginal totals are known. Ann Math Stat. 1940;11(4):427-44.
- Ireland CT, Kullback S. Contingency tables with given marginals. Biometrika. 1968;55(1):179-88.
- Swanson DA, Tayman J. Subnational population estimates. Dordrecht: Springer; 2012.
- Instituto Brasileiro de Geografia e Estatística. Censo Demográfico 2000 e 2010: tabelas 136 e 3175 [Internet]. Rio de Janeiro: IBGE. Disponível em: https://sidra.ibge.gov.br
- Bahia. Secretaria da Saúde. População residente estimada por sexo e faixa etária, Salvador, 2000–2025 [TabNet]. Salvador: SESAB/SUVISA/DIVEP; 2025.
