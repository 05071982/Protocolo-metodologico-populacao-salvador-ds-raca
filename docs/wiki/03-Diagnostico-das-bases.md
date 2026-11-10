# 3. Diagnóstico das bases existentes

Antes de estimar, todas as construções da pasta foram auditadas. Os problemas encontrados explicam várias escolhas do método.

## 3.1 Banco 2010 por DS: cobertura incompleta

| Verificação | Resultado |
|---|---|
| Soma da população no banco 2010 por DS | **2.082.781** |
| Censo 2010 (Salvador) | **2.675.656** |
| Cobertura | **≈ 78%** |

O cruzamento dos setores de 2010 com a malha perdeu muitos setores (o *Diário* registra, por exemplo, Itapuã com 235 de 543 setores).
**Decisão:** o banco 2010 é usado apenas para a **proporção de cor/raça** de cada DS. Sexo × idade de 2010 vêm da tabela SESAB, completa.

## 3.2 Banco 2022 por DS: dupla contagem nas fronteiras

| Verificação | Resultado |
|---|---|
| Soma da população nos 12 arquivos por DS | **2.649.519** |
| Censo 2022 | **2.417.678** |
| Linhas × setores únicos | 4.778 linhas para 4.371 setores |
| Setores em 2 ou 3 DS | **386** |

A função `st_intersection` coloca um setor de fronteira em todos os DS que ele toca.
**Decisão:** criar uma **chave única**, em que cada setor recebe o DS de maior área de interseção (script `01_chave_setor_bairro_ds.R`). Resultado: 4.542 setores, nenhum sem DS e só 60 com menos de 90% da área no DS escolhido.

## 3.3 Bancos de bairros: merge quebrado

Em `Bairros_2022.csv` e `pop_bairros2022.xlsx`, **apenas população e domicílios estão corretos** (a soma bate exatamente 2.417.678). As colunas de idade, sexo e raça repetem os valores de **um único setor** por bairro.
**Decisão:** usar só o total oficial de cada bairro e reconstruir a estrutura a partir dos setores.

## 3.4 Bairros × DS

Bairros não se encaixam em DS: **23 bairros** têm setores em mais de um DS. Atribuir um bairro inteiro ao DS do seu centróide gera erros grandes. Com centróides, o Centro Histórico teria 84 mil habitantes em 2022, contra 53 mil pelos setores.
**Decisão:** a unidade de cálculo é a interseção **bairro × DS** (194 unidades).

## 3.5 Limitações dos agregados do Censo 2022

| Limitação | Tratamento |
|---|---|
| Idade só em 11 faixas (30–39, 40–49, 50–59, 60–69, 70+) | Abertura em 18 faixas (seção 4.4) |
| Raça cruzada só com sexo e com faixas largas (0–14, 15–29, 30–59, 60+; 0–9/10+ por sexo) | Raking/IPF (seção 4.3) |
| Sigilo "X" (≈5% das células de idade; ≈28% das de indígena) | Imputação pelo resíduo do bloco (seção 4.2) |
| ≈171 setores sem dados demográficos | Calibração pelo total oficial do bairro |

## 3.6 Inconsistência dos totais ao longo do tempo

| Ano | Total TCU/Censo | Observação |
|---|---|---|
| 2009 | 2.998.058 | projeção baseada no Censo 2000 |
| 2010 | 2.675.656 | Censo |
| 2021 | 2.900.319 | projeção baseada no Censo 2010 |
| 2022 | 2.417.678 | Censo |
| 2023 | 2.589.296 | RIPSA, com correção de cobertura |

Os saltos são **metodológicos**, não demográficos. Por isso o arquivo traz também a série `FREQ_CENSO`, calculada só com os totais dos censos.

## 3.7 Bairro Aquarius

Criado em jan/2024 (Lei 9.778/2024) a partir da Pituba. O IBGE não tem setor "Aquarius", porque em 2022 a área era Pituba.
**Decisão:** cruzar os setores da Pituba com o polígono oficial (`02_aquarius.R`). Os **7 setores** com mais de 50% da área no Aquarius formam o bairro 171.
