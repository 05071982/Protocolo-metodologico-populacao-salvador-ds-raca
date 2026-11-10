# 2. Fontes de dados

Todos os insumos estão na pasta **População por DS** do Drive da SDSS. Os que entram no cálculo estão versionados neste repositório em `dados/`.

## 2.1 Insumos censitários

| Insumo | Origem | Uso no protocolo |
|---|---|---|
| Agregados por setores — **básico**, **demografia**, **cor ou raça**, **características dos domicílios** (Censo 2022) | IBGE | Sexo × 11 faixas, raça por sexo e por faixas largas, por setor |
| `BA_setores_CD2022.shp` | IBGE (malha de setores 2022) | Geometria dos 4.542 setores de Salvador e bairro IBGE (`NM_BAIRRO`) |
| `pop_*.csv` (12 arquivos, pasta "Pop DS - Censo 2022") | SDSS (R, mar/2026) | Variáveis por setor já selecionadas e renomeadas (Livro código) |
| Tabela SESAB/SUVISA/DIS 2010 (aba "2010" do arquivo `POPULAÇÃO_INTERPOLAÇÃO_COM_BASE_CENSO_2010_Atual_10_11_2016.xlsx`) | SESAB | DS × sexo × 18 faixas, total 2.675.656 |
| `(Censo 2010) Banco de dados por DS_.xlsx` | SDSS | Proporção de raça/cor por DS em 2010 |
| `Bairros_2022.csv` | IBGE (população por bairro) | Total oficial de cada bairro em 2022 (soma 2.417.678) |

## 2.2 Insumos geográficos

| Insumo | Origem | Uso |
|---|---|---|
| `DISTRITO_SANITARIO.shp` (2023) | SMS | Limites dos 12 DS |
| `delimitacao_de_bairros_oficial.shp` | Prefeitura de Salvador | 171 bairros, incluindo o Aquarius |

## 2.3 Totais municipais

| Anos | Fonte | Arquivo |
|---|---|---|
| 2000, 2010, 2022 | Censo Demográfico (IBGE) | — |
| 2001–2009, 2011–2021, 2024 | Estimativas TCU/IBGE | `pop_TCU.csv` (linha Total) |
| 2023 | RIPSA | `pop_TCU.csv` |
| 2025, 2026 | IBGE Cidades (estimativas TCU) | — |

Os totais estão em `dados/entrada/totais_municipais.csv`.

> **Importante:** do `pop_TCU.csv` foi usada **apenas a linha Total**. A distribuição por DS desse arquivo vinha da Razão fixa e de Lagrange e foi **substituída** pelo método deste protocolo.

## 2.4 Dicionário de códigos

**DS** (numeração SESAB, igual ao `pop14`)

| DS | Nome | DS | Nome |
|---|---|---|---|
| 1 | Centro Histórico | 7 | Boca do Rio |
| 2 | Itapagipe | 8 | Itapuã |
| 3 | São Caetano/Valéria | 9 | Cabula/Beiru |
| 4 | Liberdade | 10 | Pau da Lima |
| 5 | Brotas | 11 | Subúrbio Ferroviário |
| 6 | Barra/Rio Vermelho | 12 | Cajazeiras |

**FXET**

| FXET | Faixa | FXET | Faixa | FXET | Faixa |
|---|---|---|---|---|---|
| 1 | < 1 ano | 7 | 25–29 | 13 | 55–59 |
| 2 | 1–4 | 8 | 30–34 | 14 | 60–64 |
| 3 | 5–9 | 9 | 35–39 | 15 | 65–69 |
| 4 | 10–14 | 10 | 40–44 | 16 | 70–74 |
| 5 | 15–19 | 11 | 45–49 | 17 | 75–79 |
| 6 | 20–24 | 12 | 50–54 | 18 | 80 e mais |

**SEXO:** 1 Masculino · 2 Feminino
**RACA:** 1 Branca · 2 Preta · 3 Amarela · 4 Parda · 5 Indígena ("Negra" = 2 + 4)
**COD_BAIRRO:** ordem alfabética do Livro código (1 = Acupe … 170 = Águas Claras) e **171 = Aquarius**. A lista completa está em `dados/dicionarios/bairros.csv`.
