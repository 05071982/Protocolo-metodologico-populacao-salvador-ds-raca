# Protocolo Metodológico para estimativa populacional de Salvador

*Documento-síntese. O detalhamento de cada etapa está nas páginas numeradas da [Home](Home).*

**Equipe:** Jessidenes Teixeira de Freitas Mendes Leal · Rafaella Santiago Coutinho Santos
**Instituição:** Sala de Situação em Saúde de Salvador (SDSS), Secretaria Municipal da Saúde de Salvador
**Versão:** v5 (22/11/2026) · **Cobertura:** 2000–2026, atualizável

---

## 1. Problema

O TabNet Salvador estimava a população dos 12 Distritos Sanitários aplicando a **estrutura fixa de 2010** ao total municipal de cada ano (Razão Censitária fixa), com trechos extrapolados por **Lagrange**. O Censo 2022 mostrou que essa premissa não se sustenta:

- a população municipal caiu de 2,68 milhões (2010) para 2,42 milhões (2022), enquanto as estimativas TCU indicavam cerca de 2,9 milhões;
- Itapuã cresceu cerca de 20%, enquanto Centro Histórico e Liberdade perderam mais de 23%;
- a população de 60 anos ou mais quase dobrou em participação (9,3% → 16,6%);
- a autodeclaração preta subiu de 27,6% para 34,1%.

Além disso, não existia base por **bairro** nem por **raça/cor**, essenciais para o Painel Sociodemográfico e para a análise de equidade.

## 2. Produto

Uma tabela única, usada no TabNet Salvador e no Painel Sociodemográfico:

```
ANO | DS | COD_BAIRRO | FXET | SEXO | RACA | FREQ
27 anos × 194 unidades bairro×DS × 2 sexos × 18 faixas × 5 raças = 942.840 linhas
```

**Novidade da versão 5:** 2010 passa a ser construído setor a setor (3.546 setores do Censo 2010) nos limites atuais, e cada bairro segue a própria tendência entre os censos ([página 14](14-Versao-5-setores-2010)).

## 3. Método em 7 passos

| # | Passo | Técnica | Detalhe |
|---|---|---|---|
| 1 | Chave setor → bairro → DS (2010 e 2022, limites atuais) | maior área de interseção (R/`sf`); 2010 harmonizado com a chave de 2022 | [4.1](04-Metodo-passo-a-passo#41-chave-setor--bairro--ds) |
| 2 | Sigilo "X" do IBGE | imputação pelo resíduo do bloco | [4.2](04-Metodo-passo-a-passo#42-imputação-do-sigilo-x) |
| 3 | Calibração | fecha no total oficial IBGE de cada bairro | [4.3](04-Metodo-passo-a-passo#43-unidades-bairro--ds-e-calibração) |
| 4 | Sexo × idade × raça | IPF / raking com 4 margens | [4.4–4.6](04-Metodo-passo-a-passo#44-raça-e-idade-em-2022-ajuste-proporcional-iterativo-ipf) |
| 5 | Série 2000–2026 | **Razão Censitária com razões variáveis** | [4.7](04-Metodo-passo-a-passo#47-série-anual-razão-censitária-com-razões-variáveis) |
| 6 | Calibração aos censos 2000, 2010 e 2022 | IPF com margens do IBGE (sexo × idade, raça, DS, bairros) | [4.6](04-Metodo-passo-a-passo#46-estruturas-de-2000-2010-e-2022-calibração-censitária) e [13](13-Dialogo-entre-bases) |
| 7 | Inteiros | arredondamento controlado (maior resto; várias margens nos censos) | [4.9](04-Metodo-passo-a-passo#49-arredondamento-controlado-maior-resto) |

**Fórmula central:**

$$
P_c(t)=T(t)\cdot\frac{\left(s_c^{2010}\right)^{1-w}\left(s_c^{2022}\right)^{w}}{\sum_{c'}\left(s_{c'}^{2010}\right)^{1-w}\left(s_{c'}^{2022}\right)^{w}},\qquad w=\frac{t-2010}{12}\quad(t\ge 2010)
$$

Em 2001–2009 a mesma fórmula usa os censos 2000 e 2010: $(s_c^{2000})^{1-w}(s_c^{2010})^{w}$, com $w=(t-2000)/10$.

- $T(t)$: total oficial (Censo em 2000, 2010 e 2022; TCU/IBGE nos demais anos);
- $s_c$: participação da célula $c$ (bairro × DS × sexo × faixa × raça) no total do município. Após 2022, a tendência é aplicada por DS e repartida pelos bairros na proporção de 2022.

## 4. Por que este método

| Critério | Lagrange | Razão fixa | **Razão variável** |
|---|---|---|---|
| Erro médio ao prever 2022 com dados até 2010 | 23,5% | 9,8% | **5,8%** |
| Maior erro por DS | 38,1% | 24,6% | **13,2%** |
| Soma igual ao total oficial | não | sim | **sim** |
| Células negativas (2026) | 401 de 2.160 | 0 | **0** |
| Capta envelhecimento e mudança de raça | parcial | não | **sim** |

Detalhes em [Comparação entre métodos](05-Comparacao-entre-metodos).

## 5. Atualização

Todo ano, quando o IBGE publicar o novo total: acrescente uma linha em `dados/entrada/totais_municipais.csv` e rode `R/04` a `R/07` (o `07` gera o zip com um arquivo por ano e o dicionário). Ver [Como atualizar](07-Como-atualizar-a-base).

## 6. Principais resultados (2022)

- **Mais populosos:** Cabula/Beiru (327 mil), Itapuã (300 mil) e Barra/Rio Vermelho (299 mil).
- **Menos populoso:** Centro Histórico (53 mil).
- **População negra:** 83,1% em Salvador, variando de 66,3% (Barra/Rio Vermelho) a 91,2% (Subúrbio Ferroviário).
- **Aquarius (bairro 171):** 4.839 habitantes (3.248 em 2010, na área atual).
- **Alinhamento com o IBGE:** 2000, 2010 e 2022 fecham exatamente com os censos em sexo × idade, raça e DS; diferenças com a SESAB fora dos censos estão publicadas ([página 13](13-Dialogo-entre-bases)).

Tabelas completas em [Resultados](06-Resultados).

## 7. Limitações principais

Setores divididos entre bairros (imprecisão em bairros pequenos); raça de 2000 vem da amostra e a estrutura interna de 2000 é a de 2010; bairros fora de 2022 seguem a dinâmica do seu DS; quebras metodológicas nos totais TCU. Ver [Limitações](09-Limitacoes).
