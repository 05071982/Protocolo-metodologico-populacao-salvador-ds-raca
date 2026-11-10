# 4. Método passo a passo

O método tem duas partes independentes:

- **Estrutura** (calculada uma vez, a partir dos censos): como a população se distribui entre bairros, DS, sexo, idade e raça em **2010** e em **2022**.
- **Série** (recalculada a cada novo total): como essa distribuição evolui ano a ano e se encaixa no total municipal oficial.

```
                ┌──────────────────────────── ESTRUTURA (03_estrutura_base.R) ─────────────────────────────┐
 Setores 2022 ──► imputação "X" ──► chave setor→bairro→DS ──► calibração no total do bairro ──► IPF raça ──► 18 faixas
 SESAB 2010  ──────────────────────────────────────────────────────────────────────────────► IPF raça 2010
                └───────────────────────────────────────────────────────────────────────────────────────────┘
                                                    │
 Totais TCU/Censo ──► SÉRIE (04_atualizar_populacao.R): razão censitária com razões variáveis ──► arredondamento
                                                    │
                                       ANO | DS | COD_BAIRRO | FXET | SEXO | RACA | FREQ
```

---

## 4.1 Chave setor → bairro → DS

Cada um dos 4.542 setores de 2022 recebe:

- o **bairro** IBGE (`NM_BAIRRO`), com os nomes padronizados para o Livro código;
- o **DS de maior área de interseção**:

$$
DS(i) = \arg\max_{d}\; \text{área}(\text{setor}_i \cap DS_d)
$$

O **Aquarius** (171) recebe os setores da Pituba com mais de 50% da área no seu polígono oficial (7 setores).

## 4.2 Imputação do sigilo ("X")

O IBGE suprime células com contagens muito pequenas. Para cada bloco de variáveis com total conhecido $T$ (por exemplo, homens por faixa etária, cuja soma é o total de homens do setor):

$$
x_{\text{suprimida}} = \frac{\max\left(T - \sum_{\text{conhecidas}} x,\; 0\right)}{n_{\text{suprimidas}}}
$$

Os blocos, nesta ordem, são: sexo; sexo × idade; raça; sexo × raça; (0–9, 10+) × sexo × raça; (0–14, 15–29, 30–59, 60+) × raça.

## 4.3 Unidades bairro × DS e calibração

Os setores são somados em **194 unidades** (bairro × DS). Em cada bairro $b$, todas as variáveis são multiplicadas por

$$
f_b = \frac{P_b^{\text{IBGE 2022}}}{\sum_{i \in b} \text{moradores}_i}
$$

Com isso cada bairro fecha no total oficial e o município fecha em 2.417.678. O fator mediano foi 1,000; ele compensa os setores sem dados. Para o Aquarius e a Pituba, o total oficial da Pituba é repartido na proporção da população recenseada dos seus setores.

## 4.4 Raça e idade em 2022: ajuste proporcional iterativo (IPF)

O censo não publica o cruzamento completo **sexo × idade × raça**. Ele é estimado em cada unidade por **IPF / raking** (Deming & Stephan, 1940). Parte-se de uma matriz $X^{(0)}=1$ (2 × 11 × 5) e ela é ajustada iterativamente às quatro margens publicadas:

| Margem | Dimensão |
|---|---|
| $M_1$ | sexo × 11 faixas |
| $M_2$ | sexo × raça |
| $M_3$ | 4 faixas largas (0–14, 15–29, 30–59, 60+) × raça |
| $M_4$ | sexo × (0–9, 10+) × raça |

Em cada iteração, e para cada margem $M_k$:

$$
X \leftarrow X \cdot \frac{M_k}{\sum_{\text{dims fora de }k} X}
$$

O IPF converge para a matriz de **máxima entropia** (mínima informação adicional) compatível com todas as margens (Bishop, Fienberg & Holland, 1975).

## 4.5 Abertura das 11 faixas do censo em 18 faixas

| Faixa do censo | Faixas de saída | Regra |
|---|---|---|
| 0–4 | < 1, 1–4 | proporção de 2010 no mesmo DS e sexo (SESAB) |
| 30–39, 40–49, 50–59, 60–69 | quinquenais | **método das coortes** |
| 70+ | 70–74, 75–79, 80+ | proporção de 2010 no mesmo DS e sexo |

Método das coortes: quem tinha 30–34 anos em 2022 tinha 18–22 anos em 2010 (12 anos antes). Interpolando linearmente as faixas quinquenais de 2010:

$$
c_{30\text{–}34} = 0{,}4\,P^{2010}_{15\text{–}19} + 0{,}6\,P^{2010}_{20\text{–}24},\qquad
c_{35\text{–}39} = 0{,}4\,P^{2010}_{20\text{–}24} + 0{,}6\,P^{2010}_{25\text{–}29}
$$

$$
P^{2022}_{30\text{–}34} = P^{2022}_{30\text{–}39}\cdot\frac{c_{30\text{–}34}}{c_{30\text{–}34}+c_{35\text{–}39}}
$$

O mesmo vale para 40–49, 50–59 e 60–69. A raça de cada subfaixa segue a da faixa-mãe.

## 4.6 Estrutura de 2010

A tabela SESAB fornece **DS × sexo × 18 faixas** (total 2.675.656). A raça de 2010 é estimada por IPF com:

- semente: a estrutura sexo × idade × raça do **mesmo DS em 2022**, que preserva as interações observadas;
- margem 1: sexo × faixa (SESAB);
- margem 2: distribuição de raça do DS (banco 2010, só como proporção).

## 4.7 Série anual: Razão Censitária com razões variáveis

Seja $c$ uma célula (DS × sexo × faixa × raça; 2.160 células) e $s_c^{2010}$, $s_c^{2022}$ as suas participações no total municipal:

$$
s_c^{a} = \frac{P_c^{a} + 0{,}5}{\sum_c \left(P_c^{a} + 0{,}5\right)}\qquad a\in\{2010, 2022\}
$$

(A pseudo-contagem 0,5 evita $\log 0$.) Para qualquer ano $t$:

$$
w = \frac{t-2010}{12},\qquad
\tilde s_c(t) = \left(s_c^{2010}\right)^{1-w}\left(s_c^{2022}\right)^{w},\qquad
s_c(t) = \frac{\tilde s_c(t)}{\sum_c \tilde s_c(t)}
$$

$$
\boxed{\;P_c(t) = T(t)\cdot s_c(t)\;}
$$

em que $T(t)$ é o total municipal oficial do ano.

- $0<w<1$ (2011–2021): **interpolação** geométrica entre os censos.
- $w>1$ (2023 em diante): **extrapolação** da tendência 2010–2022.
- $w<0$ (2000–2009): **retroprojeção** de DS × sexo × idade. A raça fica congelada na distribuição de 2010 dentro de cada DS × sexo × faixa, para não extrapolar para trás a mudança de autodeclaração.
- $t=2010$ e $t=2022$: valores observados do censo.

Isso equivale a interpolar **linearmente o logaritmo da razão** de cada célula. É a forma multiplicativa do método da razão (*ratio method*; Siegel & Swanson, 2004; Smith, Tayman & Swanson, 2013), com razões que variam no tempo em vez de fixas.

## 4.8 Do DS para o bairro

Cada célula do DS no ano $t$ é repartida entre os bairros (unidades $u$) do DS na proporção observada em 2022:

$$
P_{u,c}(t) = P_{DS(u),c}(t)\cdot\frac{P_{u,c}^{2022}}{P_{DS(u),c}^{2022}}
$$

## 4.9 Arredondamento controlado (maior resto)

Para obter inteiros sem perder os totais, usa-se o método do maior resto (Hamilton; Balinski & Young, 1982):

1. arredonda-se tudo para baixo;
2. os $k$ inteiros que faltam vão para as células com as maiores partes fracionárias (empate: ordem estável).

Esse procedimento é aplicado ao total municipal de cada ano, a cada DS × sexo × faixa em 2010 e a cada célula do DS na repartição entre bairros. Assim:

- $\sum$ FREQ de cada ano $= T(t)$ exatamente;
- $\sum$ bairros de um DS $=$ DS exatamente;
- bairros em 2022 $=$ IBGE ± 19 pessoas (efeito do arredondamento).
