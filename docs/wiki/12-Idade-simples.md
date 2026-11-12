# 12. População por idade simples (DS × sexo × idade 0 a 100+)

Tabela complementar para o **TabNet Salvador** (idade detalhada), **compatível** com a base principal: em todos os anos, somando as idades de cada faixa obtém-se exatamente o valor de FXET da base `ANO | DS | COD_BAIRRO | FXET | SEXO | RACA | FREQ`.

```
ANO | DS | SEXO | IDADE | FXET | FREQ        (IDADE 100 = 100 anos e mais)
27 anos × 12 DS × 2 sexos × 101 idades = 65.448 linhas
```

Arquivos: `resultados/POP_SSA_DS_SEXO_IDADE_SIMPLES_2000_2026.xlsx` e `resultados/populacao_salvador_ds_sexo_idade_2000_2026.csv.gz`.

## 12.1 O problema

| Ano | Idade simples por DS disponível? |
|---|---|
| 2010 | **sim**: o banco Censo 2010 por DS tem idades de 0 a 100+ (cobertura de 78%, usada só como proporção) |
| 2022 | **não**: os agregados por setor só trazem 11 faixas (0–4 … 25–29, 30–39 … 60–69, 70+) |
| outros anos | não há dado: precisa ser estimado |

## 12.2 Método

A população de cada faixa já está estimada na base principal. Basta repartir cada faixa entre as suas idades:

$$
P_{\text{idade}}(t)=P_{\text{faixa}}(t)\cdot p(\text{idade}\mid\text{faixa},t)
$$

**Proporção em 2010 (observada).** É a participação de cada idade dentro da sua faixa, por DS e sexo, tirada do banco 2010.

**Proporção em 2022 (estimada por Sprague).** As faixas quinquenais de 2022 (0–4, 5–9, …, 75–79) de cada DS × sexo são desagregadas pela **interpolação osculatória de Sprague** (Siegel & Swanson, 2004, cap. 22). Esse método ajusta um polinômio suave passando pelas faixas vizinhas e preserva exatamente o total de cada faixa:

$$
\begin{pmatrix}P_{x}\\\vdots\\P_{x+4}\end{pmatrix}=\mathbf{M}\begin{pmatrix}N_{g-2}\\N_{g-1}\\N_{g}\\N_{g+1}\\N_{g+2}\end{pmatrix}
$$

$\mathbf{M}$ é a matriz de multiplicadores de Sprague: painel central para as faixas internas, painéis próprios para as duas primeiras e as duas últimas.

- Idade 0 = faixa "< 1 ano". As idades 1–4 recebem a faixa "1–4" na proporção dos multiplicadores.
- As idades 80 a 100+ seguem a forma observada em 2010, porque o Censo 2022 por setor só tem 70+.
- Valores negativos ocasionais dos multiplicadores são truncados em zero e a faixa é renormalizada.

**Demais anos: razão variável dentro da faixa.** É a mesma lógica da base principal:

$$
p(\text{idade}\mid\text{faixa},t)\propto p_{2010}^{\,1-w}\;p_{2022}^{\,w},\qquad w=\frac{t-2010}{12}
$$

**Arredondamento.** Inteiros pelo maior resto **dentro de cada faixa**, o que garante a soma exata.

## 12.3 Validação

Aplicamos Sprague às faixas de 2010 e comparamos com as idades **observadas** em 2010, por DS e sexo, nas idades de 1 a 79:

| Métrica | Resultado |
|---|---|
| Erro absoluto total | **4,1%** |
| Erro percentual médio por idade | 4,8% |

Parte desse erro é a **preferência digital** do censo, isto é, a concentração de declarações em idades terminadas em 0 e 5, que o método suaviza.

Conferências automáticas:
- soma por faixa = base principal em **todos** os 324 conjuntos ano × DS × sexo;
- nenhum valor negativo;
- total anual = TCU/Censo.

## 12.4 Como atualizar

Depois de rodar `04_atualizar_populacao.R`:

```r
source("R/05_idade_simples.R")
```

Gera `resultados/populacao_salvador_ds_sexo_idade_<ano_ini>_<ano_fim>.csv`.

## 12.5 Cuidados de uso

- Idade simples por DS tem mais flutuação que as faixas. Para taxas, agrupe idades sempre que possível.
- Esta tabela não tem raça nem bairro. Para esses recortes, use a base principal com FXET.
