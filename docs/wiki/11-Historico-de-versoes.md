# 11. Histórico de versões

| Versão | Data | Mudanças |
|---|---|---|
| até 2023 | — | `pop14` e séries do TabNet: razão censitária fixa (estrutura SESAB 2010) e extrapolação de Lagrange sobre totais TCU |
| v1 | 09/11/2026 | Primeira base DS × bairro × sexo × 18 faixas × raça; setores de fronteira divididos 1/k; bairros com a estrutura do DS |
| v2 | 09/11/2026 | Chave setor → bairro → DS por maior área; unidades bairro × DS; estrutura própria de cada bairro |
| **v5.1** | 22/11/2026 | **Bairro 172 – Boa Vista do Lobato** (Lei 9.919/2025): delimitado pelos endereços do CNEFE 2022 nos 34 logradouros da lei; cada setor repartido pela fração de domicílios nessas ruas; desmembrado do Lobato, Alto do Cabrito e Boa Vista de São Caetano (DS 11); presente em toda a série nos limites atuais. Dicionário com `LEI_CRIACAO` e `BAIRRO_ORIGEM`. **Prefeitura-Bairro** (10 PBs): PB de cada bairro no dicionário, colunas nos arquivos por ano e série por PB ([página 16](16-Prefeituras-Bairro)). 195 unidades bairro × DS. Página [Bairros criados por lei](15-Bairros-criados-por-lei) |
| **v5** | 22/11/2026 | **Setores censitários de 2010**: 2010 construído setor a setor (3.546 setores, agregados do universo e malha do IBGE) nos limites atuais de bairro e DS, com raça/cor do universo em 100% dos setores; chave 2010 harmonizada com a de 2022; cada bairro com tendência própria entre os censos; após 2022, tendência por DS repartida pelos bairros na proporção de 2022; bairros 2010 = soma dos setores e 2022 = IBGE (exatos). Página [Versão 5](14-Versao-5-setores-2010) |
| v4 | 19/11/2026 | **Calibração censitária**: 2000, 2010 e 2022 fecham exatamente com o IBGE (sexo × faixa; idades simples 0–19 em 2000/2022 e 0–100+ em 2010; raça SIDRA 136/3175; DS 2000; bairros 2022). 2001–2009 interpolados entre 2000 e 2010 (antes: retroprojeção). Reconciliação publicada com o TabNet SESAB. Dicionário de bairros com DS; bairro 2 (Aeroporto) com FREQ = 0 em todas as bases. Script `07_exportar_por_ano.R` (zip por ano). Página [Diálogo entre bases](13-Dialogo-entre-bases) |
| v3.2 | 13/11/2026 | Tabela ANO × DS × bairro × idade simples × sexo × raça (CSV, arredondamento com duas margens); abas tabuladas 2010/2022 (DS × idade e DS × faixa, por sexo); script `06_bairro_idade_raca.R` |
| v3.1 | 12/11/2026 | Tabela complementar DS × sexo × idade simples (0–100+), compatível com as faixas da base principal; script `05_idade_simples.R` |
| **v3** | 10/11/2026 | Totais Censo + TCU/IBGE (2023 RIPSA; 2025–2026 IBGE Cidades); série `FREQ_CENSO`; **Aquarius (171)**; aba SETORES; scripts R para atualização anual |

## Publicação no Zenodo (DOI)

[![DOI](https://zenodo.org/badge/1452138178.svg)](https://doi.org/10.5281/zenodo.24096844)

**DOI:** [10.5281/zenodo.24096844](https://doi.org/10.5281/zenodo.24096844). Release v3.0.0 publicada em 10/11/2026. Para a v5.1, crie a release `v5.1.0`; o Zenodo gera um DOI de versão próprio.

### Como gerar uma nova versão

1. Entre em https://zenodo.org com a conta do GitHub (**Log in → GitHub**).
2. Em **Account → GitHub**, ative o repositório `Protocolo-metodologico-populacao-salvador-ds-raca`.
3. No GitHub, crie uma *release*: **Releases → Draft a new release**, tag `v5.1.0`, título "v5.1 – bairro 172 Boa Vista do Lobato".
4. O Zenodo arquiva a release e gera o DOI. Os metadados (autoras, título, licença, palavras-chave) vêm do arquivo `.zenodo.json` do repositório.
5. Copie o selo do DOI para o `README.md` e para a página [Home](Home).

A cada atualização anual (nova release), o Zenodo cria um DOI de versão, ligado a um DOI conceito que sempre aponta para a versão mais recente.
