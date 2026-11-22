# 2. Fontes de dados

Todos os insumos estão na pasta **População por DS** do Drive da SDSS. Os que entram no cálculo estão versionados neste repositório em `dados/`.

## 2.1 Insumos censitários

| Insumo | Origem | Uso no protocolo |
|---|---|---|
| Agregados por setores — **básico**, **demografia**, **cor ou raça**, **características dos domicílios** (Censo 2022) | IBGE | Sexo × 11 faixas, raça por sexo e por faixas largas, por setor |
| `BA_setores_CD2022.shp` | IBGE (malha de setores 2022) | Geometria dos 4.542 setores de Salvador e bairro IBGE (`NM_BAIRRO`) |
| `pop_*.csv` (12 arquivos, pasta "Pop DS - Censo 2022") | SDSS (R, mar/2026) | Variáveis por setor já selecionadas e renomeadas (Livro código) |
| Tabela SESAB/SUVISA/DIS 2010 (aba "2010" do arquivo `POPULAÇÃO_INTERPOLAÇÃO_COM_BASE_CENSO_2010_Atual_10_11_2016.xlsx`) | SESAB | DS × sexo × 18 faixas, total 2.675.656 (limites da época); na v5, só comparação |
| `(Censo 2010) Banco de dados por DS_.xlsx` | SDSS | Usado até a v4 (raça/cor por DS, cobertura ≈ 78%); substituído pelos setores na v5 |
| Agregados por setores do Censo 2010, universo: `Basico_BA`, `Pessoa03_BA`, `Pessoa05_BA`, `Pessoa11_BA`, `Pessoa12_BA` | IBGE | Idade simples por sexo e raça por sexo e grupo etário, por setor (v5) |
| Malha de setores censitários 2010 (`29SEE250GC_SIR`, recorte de Salvador) | IBGE | Chave setor 2010 → bairro × DS nos limites atuais (v5) — `dados/entrada/chave_setor_bairro_ds_2010.csv` |
| `Bairros_2022.csv` | IBGE (população por bairro) | Total oficial de cada bairro em 2022 (soma 2.417.678) |
| SIDRA **tabela 3175** (Censo 2010, universo): cor ou raça × sexo × idade, Salvador | IBGE | Margem sexo × idade × raça de 2010 (v4) — `dados/entrada/sidra_3175_salvador_2010_sexo_idade_raca.csv` |
| SIDRA **tabela 136** (Censos 2000 e 2010): cor ou raça, Salvador | IBGE | Margem de raça de 2000 (amostra) (v4) — `dados/entrada/sidra_136_salvador_raca_2000_2010.csv` |
| TabNet SESAB: população por sexo e faixa etária detalhada, Salvador, 2000–2025 | SESAB/SUVISA/DIVEP | 2000 e 2022 (= Censo): margens sexo × faixa e idades 0–19 (v4); demais anos: só reconciliação — `dados/entrada/sesab_tabnet_*.csv` |
| Totais por DS de 2000 (mesmos limites atuais) | SMS (`pop_TCU.csv`, ano 2000) | Margem por DS de 2000 (v4) — `dados/entrada/ds_2000_totais.csv` |

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

> O bairro **2 – Aeroporto** consta no dicionário, mas não tem população residente no Censo 2022 e por isso não aparece nas tabelas de população: elas trazem **170 bairros com moradores** dos 171 oficiais.
