# 11. Histórico de versões

| Versão | Data | Mudanças |
|---|---|---|
| até 2023 | — | `pop14` e séries do TabNet: razão censitária fixa (estrutura SESAB 2010) e extrapolação de Lagrange sobre totais TCU |
| v1 | 09/11/2026 | Primeira base DS × bairro × sexo × 18 faixas × raça; setores de fronteira divididos 1/k; bairros com a estrutura do DS |
| v2 | 09/11/2026 | Chave setor → bairro → DS por maior área; unidades bairro × DS; estrutura própria de cada bairro |
| v3.1 | 12/11/2026 | Tabela complementar DS × sexo × idade simples (0–100+), compatível com as faixas da base principal; script `05_idade_simples.R` |
| **v3** | 10/11/2026 | Totais Censo + TCU/IBGE (2023 RIPSA; 2025–2026 IBGE Cidades); série `FREQ_CENSO`; **Aquarius (171)**; aba SETORES; scripts R para atualização anual |

## Publicação no Zenodo (DOI)

[![DOI](https://zenodo.org/badge/1452138178.svg)](https://doi.org/10.5281/zenodo.24096844)

**DOI:** [10.5281/zenodo.24096844](https://doi.org/10.5281/zenodo.24096844). Release v3.0.0 publicada em 10/11/2026.

### Como gerar uma nova versão

1. Entre em https://zenodo.org com a conta do GitHub (**Log in → GitHub**).
2. Em **Account → GitHub**, ative o repositório `Protocolo-metodologico-populacao-salvador-ds-raca`.
3. No GitHub, crie uma *release*: **Releases → Draft a new release**, tag `v3.0.0`, título "v3 – base 2000–2026".
4. O Zenodo arquiva a release e gera o DOI. Os metadados (autoras, título, licença, palavras-chave) vêm do arquivo `.zenodo.json` do repositório.
5. Copie o selo do DOI para o `README.md` e para a página [Home](Home).

A cada atualização anual (nova release), o Zenodo cria um DOI de versão, ligado a um DOI conceito que sempre aponta para a versão mais recente.
