# 14. Versão 5: setores censitários de 2010 e bairros com tendência própria

## 14.1 O que mudou

Até a versão 4, só 2022 era construído setor a setor. Em 2010 a base usava:

- a tabela da SESAB por DS, sexo e faixa etária, nos limites de DS **da época**;
- um "banco 2010 por DS" com raça/cor e idade simples que cobria só cerca de 78% da população.

Consequência: os bairros repetiam, em todos os anos, a proporção de 2022 dentro do DS.

Na versão 5, 2010 é construído **do mesmo jeito que 2022**: a partir dos agregados por setor censitário do universo do Censo 2010, nos **limites atuais** de bairro e DS.

| Item | v4 | v5 |
|---|---|---|
| Fonte de 2010 | tabela SESAB por DS + banco parcial | agregados por setor do IBGE (3.546 setores com moradores) |
| Cobertura da raça/cor em 2010 | ≈ 78% (proporções) | 100% (universo, setor a setor) |
| Limites dos DS em 2010 | da época | atuais |
| Bairros em 2010 | proporção de 2022 dentro do DS | soma dos setores de cada bairro |
| Bairros entre os censos | seguiam o DS | **cada bairro com tendência própria** (2001–2021) |
| Idade simples por DS em 2010 | banco parcial | setores (Pessoa11 e Pessoa12), 100% |

## 14.2 Por que a cobertura era de 78%

O script original (`Pop_DS_2010_20260324.R`) cruzava os **códigos** dos setores de 2010 com o shapefile de setores de **2022**. Setores divididos ou recodificados em 2022 não encontravam par e ficavam de fora. Com a malha de setores de 2010 (`29SEE250GC_SIR`), todos os setores com moradores entram.

## 14.3 Insumos

- `Basico_BA`, `Pessoa03_BA` (raça × sexo × grupos etários de 5 anos ou mais), `Pessoa05_BA` (raça × sexo, 0 a 4 anos), `Pessoa11_BA` e `Pessoa12_BA` (idade simples por sexo), da pasta Agregados por Setores Censitários do Censo 2010 (IBGE).
- Malha de setores de 2010 do IBGE recortada para Salvador (3.592 polígonos).
- Malha oficial de bairros (`delimitacao_de_bairros_oficial`) e de DS (`DISTRITO_SANITARIO`).

Conferências: a soma do Pessoa03 é **2.675.656**, igual ao Censo, e os 3.546 setores com dados estão todos na malha. Nove setores com sigilo têm só o total por sexo (475 pessoas).

## 14.4 Chave setor 2010 → bairro × DS

`R/01b_chave_setor2010.R` cruza cada setor com as unidades bairro × DS e guarda a fração de área de cada interseção. A escolha final (`python/v5_harmoniza_chave.py`) segue esta ordem:

1. **Mesmo código em 2022 (2.874 setores):** usa-se a unidade da chave de 2022, desde que o polígono de 2010 tenha ao menos 25% da área nela. Isso mantém a definição de bairro do IBGE usada em 2022.
2. **Demais (669 setores):** unidade de maior área de interseção.
3. **Sem interseção (3 setores costeiros de Paripe, 2.897 pessoas):** Paripe (DS Subúrbio Ferroviário), como os setores vizinhos.

Em 96% da população, o critério do código e o do polígono dão o mesmo bairro. Setores cuja maior área cai no Aeroporto (sem moradores em 2022) ou em pedaços de bairro sem população em 2022 vão para a unidade vizinha com população. Arquivo final: `dados/entrada/chave_setor_bairro_ds_2010.csv`.

O **Aquarius** (criado em 2024) aparece em 2010 com a população que morava na área do seu polígono atual: 3.248 pessoas (4.839 em 2022).

## 14.5 Estrutura de 2010 por bairro × DS

Para cada unidade:

1. sexo × idade simples = soma dos setores (Pessoa11/12) → sexo × 18 faixas;
2. raça × sexo × grupo etário = soma dos setores (Pessoa05 para 0–4; Pessoa03 para 5–9, 10–14, …, 55–59, 60–69 e 70+);
3. semente = população da faixa × proporção de raça no grupo; IPF com margens unidade × sexo × faixa, unidade × sexo × grupo × raça e sexo × faixa × raça do município (universo, SIDRA 3175);
4. arredondamento controlado: população de cada unidade por sexo e sexo × faixa × raça do município exatas.

## 14.6 Resultados que mudam

- **DS de 2010 nos limites atuais × tabela SESAB (limites da época):** diferença máxima de **0,8%** (São Caetano/Valéria e Pau da Lima). A mudança de limites era pequena; o padrão de ganho e perda entre DS de 2010 a 2022 se mantém (Itapuã +20% a +39% acima da média da cidade em todas as coortes; Liberdade −10% a −18%).
- **Validação retrospectiva** (todos os anos nos limites atuais): erro médio da razão variável de **5,8%** (antes 5,7%); razão fixa 9,8%; Lagrange 23,5%.
- **Bairros:** a variação 2010→2022 vai de −26% (percentil 10) a +30% (percentil 90), com mediana de −12%. Manter a proporção de 2010 fixa até 2022 erraria os bairros em 16% em média. Bairros de expansão: Jardim das Margaridas (4.592 → 20.637), Areia Branca (2.594 → 9.205), Patamares (6.156 → 21.086). Perdas maiores: Nazaré, Santa Mônica e Chame-Chame (−35% a −36%).
- **Após 2022:** a tendência é aplicada no nível do DS e repartida pelos bairros na proporção de 2022. Extrapolar célula a célula de bairro levaria Jardim das Margaridas a 37 mil habitantes em 2026 (+80% em quatro anos), o que não é plausível.

## 14.7 Validação da versão 5

Todas as 20 conferências de `resultados/validacao_v5.csv` passaram:

- totais oficiais em todos os anos;
- margens do IBGE em 2000, 2010 e 2022;
- bairros de 2010 iguais à soma dos setores e de 2022 iguais ao IBGE;
- tabelas por bairro, por idade simples e por DS iguais em todas as células;
- 171 bairros presentes;
- nenhum valor negativo.

A réplica do R reproduziu as 942.840 células da base e as 65.448 da idade simples, também com um ano 2027 de teste.
