# 4. Método passo a passo

O método tem duas partes independentes:

- **Estrutura** (calculada uma vez, a partir dos censos): como a população se distribui entre bairros, DS, sexo, idade e raça em **2010** e em **2022** (setores censitários, limites atuais), e as margens censitárias de **2000**.
- **Série** (recalculada a cada novo total): como essa distribuição evolui ano a ano e se encaixa no total municipal oficial.

```
                ┌──────────────────────────── ESTRUTURA (03_estrutura_base.R) ─────────────────────────────┐
 Setores 2022 ──► imputação "X" ──► chave setor→bairro→DS ──► calibração no total do bairro ──► IPF raça ──► 18 faixas
 Setores 2010 ──► chave setor→bairro×DS (limites atuais) ──► idade×sexo e raça×sexo×grupo ──► IPF ──► 18 faixas (v5)
 Margens IBGE 2000/2010/2022 (sexo×idade, raça, DS) ──────────────────────► calibração censitária (v4)
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

## 4.6 Estruturas de 2000, 2010 e 2022 (calibração censitária)

### Estrutura de 2010 a partir dos setores (v5)

Desde a versão 5, 2010 é construído **setor a setor**, como 2022:

- **Dados:** agregados por setor do universo do Censo 2010 (3.546 setores com moradores, soma = 2.675.656): idade simples por sexo (Pessoa11 e Pessoa12) e raça/cor por sexo e grupo etário (Pessoa03 para 5 anos ou mais; Pessoa05 para 0 a 4 anos). Nove setores com sigilo (475 pessoas) têm só o total por sexo; idade e raça vêm da própria unidade.
- **Chave:** a malha de setores de 2010 foi cruzada com a malha oficial de bairros e DS (`R/01b_chave_setor2010.R`). Para 2.874 setores com o mesmo código em 2022, usa-se a unidade da chave de 2022, desde que o polígono de 2010 tenha ao menos 25% da área nela; para os demais 669, a unidade de maior área; 3 setores costeiros de Paripe sem interseção foram atribuídos a Paripe. Em 96% da população, os dois critérios dão o mesmo bairro.
- **IPF por unidade:** semente = idade do setor × proporção de raça no grupo etário; margens = unidade × sexo × faixa (setores), unidade × sexo × grupo × raça (setores) e sexo × faixa × raça do município (universo, SIDRA 3175).

Resultado: os DS de 2010 nos **limites atuais** diferem da tabela SESAB (limites da época) em no máximo 0,8%. A mudança de limites dos DS entre 2010 e 2022 era, portanto, pequena.

### Calibração censitária

| Ano | Semente | Margens exatas |
|---|---|---|
| 2010 | setores 2010 por unidade bairro × DS | população de cada unidade por sexo (setores); sexo × faixa × raça do município (SIDRA 3175) |
| 2022 | setores 2022 por unidade bairro × DS | total de cada unidade (IBGE por bairro); sexo × faixa do município (Censo 2022) |
| 2000 | estrutura de 2010 por unidade | total por DS (tabela DS 2000); sexo × faixa (Censo 2000); raça (SIDRA 136, sem declaração redistribuída) |

O IPF altera o mínimo possível a semente (Ireland & Kullback, 1968). Por isso a distribuição entre DS e bairros, e seus cruzamentos de idade e raça, continua vindo dos setores. Detalhes e validação em [Diálogo entre bases](13-Dialogo-entre-bases) e [Versão 5](14-Versao-5-setores-2010).

## 4.7 Série anual: Razão Censitária com razões variáveis

Seja $c$ uma célula (desde a v5, **unidade bairro × DS × sexo × faixa × raça**; 34.920 células) e $s_c^{2010}$, $s_c^{2022}$ as suas participações no total municipal:

$$
s_c^{a} = \frac{P_c^{a} + \varepsilon}{\sum_c \left(P_c^{a} + \varepsilon\right)}\qquad a\in\{2000, 2010, 2022\}
$$

(A pseudo-contagem $\varepsilon$ evita $\log 0$: 0,1 nas células de bairro e 0,5 nas de DS.) Para qualquer ano $t$:

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
- $w>1$ (2023 em diante): **extrapolação** da tendência 2010–2022, feita no nível **DS × sexo × faixa × raça** (2.160 células) e repartida entre os bairros do DS na proporção de 2022. Extrapolar célula a célula de bairro amplificaria crescimentos pontuais (ex.: bairros de expansão recente).
- 2001–2009: **interpolação** geométrica entre os Censos 2000 e 2010, $\tilde s_c(t)=(s_c^{2000})^{1-w}(s_c^{2010})^{w}$, $w=(t-2000)/10$, inclusive para raça. Na v3 esses anos eram retroprojeção ($w<0$), com raça congelada em 2010.
- $t=2000$, $2010$ e $2022$: valores censitários calibrados.

Isso equivale a interpolar **linearmente o logaritmo da razão** de cada célula. É a forma multiplicativa do método da razão (*ratio method*; Siegel & Swanson, 2004; Smith, Tayman & Swanson, 2013), com razões que variam no tempo em vez de fixas.

## 4.8 Bairros com tendência própria (v5)

Entre 2001 e 2021, a interpolação é feita diretamente nas células de cada unidade bairro × DS. Cada bairro segue, portanto, a sua própria trajetória entre os censos (antes da v5, os bairros repetiam a proporção de 2022 dentro do DS). Depois de 2022:

$$
P_{u,c}(t) = P_{DS(u),c}(t)\cdot\frac{P_{u,c}^{2022}}{P_{DS(u),c}^{2022}}
$$

## 4.9 Arredondamento controlado (maior resto)

Para obter inteiros sem perder os totais, usa-se o método do maior resto (Hamilton; Balinski & Young, 1982):

1. arredonda-se tudo para baixo;
2. os $k$ inteiros que faltam vão para as células com as maiores partes fracionárias (empate: ordem estável).

Esse procedimento é aplicado ao total municipal de cada ano (células de bairro) e, após 2022, a cada célula do DS na repartição entre bairros. Nos anos censitários usa-se um **arredondamento controlado com várias margens**: os inteiros vão para as células de maior parte fracionária cujas margens (DS, sexo × faixa, raça, conforme o ano) ainda têm déficit, de modo que todas as margens do item 4.6 fecham exatamente. Assim:

- $\sum$ FREQ de cada ano $= T(t)$ exatamente;
- $\sum$ bairros de um DS $=$ DS exatamente;
- bairros em 2022 $=$ IBGE e bairros em 2010 $=$ soma dos setores, exatamente.
