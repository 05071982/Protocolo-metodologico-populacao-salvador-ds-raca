# 1. Contexto e objetivos

## 1.1 Por que precisamos de um denominador próprio

A Análise de Situação de Saúde (ASIS) depende de taxas: mortalidade, incidência, cobertura vacinal, cobertura de pré-natal. Toda taxa tem um **denominador populacional**. Se ele estiver errado, o indicador também estará, e um DS pode parecer pior (ou melhor) do que realmente é.

O IBGE publica população por município. A SMS planeja e executa ações em uma escala menor: **12 Distritos Sanitários** e **171 bairros**. O IBGE não publica estimativas anuais nessas escalas, e as fronteiras dos DS não coincidem com as dos bairros nem com as divisões do IBGE. Por isso a SMS precisa produzir as próprias estimativas.

## 1.2 Como era feito até 2023

A base do TabNet Salvador (arquivos `pop14`, `POPULAÇÃO_INTERPOLAÇÃO_COM_BASE_CENSO_2010`) usava:

1. a **tabela SESAB/SUVISA/DIS de 2010** com a população de cada DS por sexo e 18 faixas etárias (total = Censo 2010 = 2.675.656);
2. o **total municipal TCU/IBGE** de cada ano;
3. a **Razão Censitária fixa**: participação de cada DS × sexo × faixa em 2010 multiplicada pelo total do ano;
4. para algumas séries, **extrapolação de Lagrange** (polinômio interpolador; Burden & Faires, 2008).

A premissa central era que **a distribuição da população entre os DS permaneceu igual à de 2010**. Essa premissa não captura:

- **migração interna**: crescimento de Itapuã, Cajazeiras, Boca do Rio e esvaziamento do Centro Histórico e da Liberdade;
- **envelhecimento**: a população de 60 anos ou mais passou de 9,3% (2010) para 16,6% (2022);
- **mudança na autodeclaração de cor/raça**: a população preta passou de 27,6% para 34,1%.

## 1.3 O que mudou em 2022

- O **Censo 2022** encontrou **2.417.678** habitantes em Salvador, menos que em 2010 (2.675.656). As estimativas TCU anteriores (~2,9 milhões) estavam superestimadas.
- O Ministério da Saúde questionou a cobertura do Censo (Nota Técnica nº 41/2024-CGIAE/DAENT/SVSA/MS).
- O IBGE publicou os **agregados por setor censitário** de 2022, com idade, sexo e cor/raça. Isso permitiu, pela primeira vez, montar a estrutura por DS e por bairro com dados de 2022.
- Salvador passou a ter **171 bairros** oficiais com a criação do **Aquarius** (Lei 9.778/2024), desmembrado da Pituba.

## 1.4 Objetivos do protocolo

**Geral:** produzir uma base populacional anual de Salvador por DS, bairro, sexo, faixa etária e raça/cor, com método reprodutível, documentado e atualizável.

**Específicos:**

1. Diagnosticar as bases existentes e corrigir suas inconsistências.
2. Construir a chave setor censitário → bairro → DS para 2022.
3. Estimar a estrutura sexo × idade × raça de cada bairro e de cada DS em 2010 e em 2022.
4. Gerar a série 2000–2026 coerente com os totais oficiais (Censo e TCU/IBGE).
5. Comparar o método adotado com o método anterior (Razão fixa e Lagrange).
6. Disponibilizar códigos em R para atualizar a base a cada novo total anual (2027 em diante).
