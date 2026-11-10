# Protocolo Metodológico para estimativa populacional de Salvador

*Documento-síntese. O detalhamento de cada etapa está nas páginas numeradas da [Home](Home).*

**Equipe:** Jessidenes Teixeira de Freitas Mendes Leal · Rafaella Santiago Coutinho Santos
**Instituição:** Sala de Situação em Saúde de Salvador (SDSS), Secretaria Municipal da Saúde de Salvador
**Versão:** v3 (10/11/2026) · **Cobertura:** 2000–2026, atualizável

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

## 3. Método em 6 passos

| # | Passo | Técnica | Detalhe |
|---|---|---|---|
| 1 | Chave setor → bairro → DS | maior área de interseção (R/`sf`) | [4.1](04-Metodo-passo-a-passo#41-chave-setor--bairro--ds) |
| 2 | Sigilo "X" do IBGE | imputação pelo resíduo do bloco | [4.2](04-Metodo-passo-a-passo#42-imputação-do-sigilo-x) |
| 3 | Calibração | fecha no total oficial IBGE de cada bairro | [4.3](04-Metodo-passo-a-passo#43-unidades-bairro--ds-e-calibração) |
| 4 | Sexo × idade × raça | IPF / raking com 4 margens | [4.4–4.6](04-Metodo-passo-a-passo#44-raça-e-idade-em-2022-ajuste-proporcional-iterativo-ipf) |
| 5 | Série 2000–2026 | **Razão Censitária com razões variáveis** | [4.7](04-Metodo-passo-a-passo#47-série-anual-razão-censitária-com-razões-variáveis) |
| 6 | Inteiros | arredondamento pelo maior resto | [4.9](04-Metodo-passo-a-passo#49-arredondamento-controlado-maior-resto) |

**Fórmula central:**

$$
P_c(t)=T(t)\cdot\frac{\left(s_c^{2010}\right)^{1-w}\left(s_c^{2022}\right)^{w}}{\sum_{c'}\left(s_{c'}^{2010}\right)^{1-w}\left(s_{c'}^{2022}\right)^{w}},\qquad w=\frac{t-2010}{12}
$$

- $T(t)$: total oficial (Censo em 2000, 2010 e 2022; TCU/IBGE nos demais anos);
- $s_c$: participação da célula $c$ (DS × sexo × faixa × raça) no total do município.

## 4. Por que este método

| Critério | Lagrange | Razão fixa | **Razão variável** |
|---|---|---|---|
| Erro médio ao prever 2022 com dados até 2010 | 23,4% | 9,9% | **5,7%** |
| Maior erro por DS | 36,6% | 24,6% | **12,4%** |
| Soma igual ao total oficial | não | sim | **sim** |
| Células negativas (2026) | 401 de 2.160 | 0 | **0** |
| Capta envelhecimento e mudança de raça | parcial | não | **sim** |

Detalhes em [Comparação entre métodos](05-Comparacao-entre-metodos).

## 5. Atualização

Todo ano, quando o IBGE publicar o novo total: acrescente uma linha em `dados/entrada/totais_municipais.csv` e rode `R/04_atualizar_populacao.R`. Ver [Como atualizar](07-Como-atualizar-a-base).

## 6. Principais resultados (2022)

- **Mais populosos:** Cabula/Beiru (327 mil), Itapuã (300 mil) e Barra/Rio Vermelho (299 mil).
- **Menos populoso:** Centro Histórico (53 mil).
- **População negra:** 83,1% em Salvador, variando de 66,3% (Barra/Rio Vermelho) a 91,2% (Subúrbio Ferroviário).
- **Aquarius (bairro 171):** 4.837 habitantes.

Tabelas completas em [Resultados](06-Resultados).

## 7. Limitações principais

Mudança dos limites dos DS entre 2010 e 2022; raça de 2010 estimada a partir de um banco parcial; bairros fora de 2022 seguem a dinâmica do seu DS; quebras metodológicas nos totais TCU. Ver [Limitações](09-Limitacoes).
