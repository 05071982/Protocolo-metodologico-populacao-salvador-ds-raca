# 16. Prefeituras-Bairro

Salvador organiza a gestão administrativa em **10 Prefeituras-Bairro (PB)**, criadas pela Lei Municipal nº 8.376/2012. A base usa essa configuração de 10 PBs, conforme o shapefile da Prefeitura (`Prefeituras_Bairro.shp`, 2018). Ela é a mesma do mapa da Fundação Mário Leal Ferreira (FMLF) de 2022.

| COD_PB | PB | Bairros | Pop. 2022 | % negra 2022 | % 60+ 2022 | Pop. 2026 |
|---|---|---|---|---|---|---|
| 1 | I – Centro / Brotas | 23 | 239.424 | 75,7 | 20,7 | 246.826 |
| 2 | II – Subúrbio / Ilhas | 19 | 261.006 | 91,0 | 14,0 | 275.439 |
| 3 | III – Cajazeiras | 17 | 192.680 | 89,9 | 13,9 | 210.713 |
| 4 | IV – Itapuã / Ipitanga | 17 | 388.097 | 80,1 | 14,8 | 441.337 |
| 5 | V – Cidade Baixa | 15 | 149.149 | 87,8 | 18,5 | 152.339 |
| 6 | VI – Barra / Pituba | 23 | 323.924 | 64,8 | 23,5 | 339.457 |
| 7 | VII – Liberdade / São Caetano | 19 | 296.545 | 90,2 | 16,7 | 302.770 |
| 8 | VIII – Cabula / Tancredo Neves | 22 | 317.923 | 87,2 | 14,2 | 330.326 |
| 9 | IX – Pau da Lima | 13 | 173.172 | 87,5 | 12,3 | 183.261 |
| 10 | X – Valéria | 4 | 75.758 | 89,7 | 11,9 | 77.477 |

## 16.1 Chave bairro → PB

`R/01c_chave_bairro_prefeitura_bairro.R` cruza o polígono de cada bairro oficial com as PBs.

- **Resultado:** todo bairro tem **93% ou mais da área** em uma única PB, e nenhum tem mais de **3% em outra**. O maior valor é o da Lapinha, com 2,6%.
- **Por que as sobras são pequenas:** são diferenças de traçado entre as duas malhas, a de PB (2018) e a de bairros. Também há áreas de costa fora dos polígonos de PB. Não são bairros realmente divididos.
- **Decisão:** cada bairro pertence **inteiro** à PB que contém sua maior área. Por isso a PB é só um atributo do bairro e não muda nenhum cálculo da base.
- **Boa Vista do Lobato (172):** a malha de bairros ainda não tem o bairro. Ele segue o Lobato e fica na PB V – Cidade Baixa, onde estão cerca de 89% dos seus moradores; o restante vem do Alto do Cabrito e da Boa Vista de São Caetano, que são da PB VII. Revisar quando a Prefeitura definir a PB do bairro.

As frações de área estão em `dados/entrada/chave_bairro_prefeitura_bairro.csv`.

## 16.2 Onde a PB aparece

- **Dicionário de bairros** (`dados/dicionarios/bairros.csv`): colunas `COD_PB`, `PB_ROMANO`, `NOME_PB` e `PROP_AREA_PB`.
- **Dicionário de PBs:** `dados/dicionarios/prefeituras_bairro.csv`.
- **Arquivos por ano (idade detalhada):** colunas `COD_PB` e `NOME_PB`.
- **Série por PB:** `resultados/populacao_salvador_prefeitura_bairro_2000_2026.csv.gz` e aba POP_PB da planilha, no formato `ANO | COD_PB | FXET | SEXO | RACA | FREQ`.
- **Tabela oficial** (`ANO | DS | COD_BAIRRO | FXET | SEXO | RACA | FREQ`): **não muda**, para não quebrar o TabNet. Para obter a PB, basta ligar `COD_BAIRRO` ao dicionário.

**Validação:** todo bairro tem uma PB (de 1 a 10), e a soma das 10 PBs é igual ao total de cada ano.

## 16.3 Atualização

Na atualização anual, o `07_exportar_por_ano.R` já gera as colunas de PB e a série por PB. Se a configuração mudar (por exemplo, com a PB do Centro Histórico ou a das Ilhas), siga estes passos:

1. Rode o `01c` com o novo shapefile.
2. Atualize `COD_PB` no dicionário.
3. Rode o `07`.
