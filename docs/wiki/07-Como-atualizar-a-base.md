# 7. Como atualizar a base (ex.: total de 2027)

A atualização anual **não** exige reprocessar o Censo. As estruturas calibradas de 2000, 2010 e 2022 (por bairro × DS) já estão prontas em `dados/estrutura/`. **Basta informar o novo total.**

## 7.1 Passo a passo

**1. Baixe (ou atualize) o repositório**

```bash
git clone https://github.com/05071982/Protocolo-metodologico-populacao-salvador-ds-raca.git
```

Ou, no GitHub: **Code → Download ZIP**.

**2. Acrescente o novo ano em `dados/entrada/totais_municipais.csv`**

```csv
ANO,TOTAL,FONTE,CENSITARIO
...
2026,2559945,IBGE Cidades,0
2027,<total TCU/IBGE de 2027>,TCU/IBGE,0
```

O valor sai do IBGE Cidades ou da publicação das estimativas TCU no Diário Oficial (agosto de cada ano).

**3. Abra o R/RStudio na pasta do repositório e rode**

```r
setwd("C:/caminho/Protocolo-metodologico-populacao-salvador-ds-raca")
source("R/04_atualizar_populacao.R")   # base principal (bairro × DS × faixa × sexo × raça)
source("R/05_idade_simples.R")         # DS × sexo × idade simples
source("R/06_bairro_idade_raca.R")     # bairro × DS × idade × sexo × raça
source("R/07_exportar_por_ano.R")      # zip: um CSV por ano + dicionário
```

Os scripts 04 a 06 usam só o R base. O 07 usa o pacote `zip` (recomendado: `install.packages(c("zip", "openxlsx"))`). Sem `zip` ele tenta o `utils::zip`, que no Windows depende do Rtools; sem `openxlsx` o dicionário sai só em CSV.

**4. Confira o console.** O script para com erro se:

- a soma de algum ano diferir do total informado;
- surgir algum valor negativo;
- o total informado para 2000, 2010 ou 2022 diferir do censo;
- faltar algum dos 172 bairros do dicionário.

**5. Pegue os resultados em `resultados/`:**

| Arquivo | Uso |
|---|---|
| `populacao_salvador_bairro_ds_2000_2027.csv` | TabNet Salvador e Painel Sociodemográfico (`ANO, DS, COD_BAIRRO, FXET, SEXO, RACA, FREQ`) |
| `populacao_salvador_ds_2000_2027.csv` | versão agregada por DS (formato `pop14`) |
| `populacao_salvador_ds_sexo_idade_2000_2027.csv` | DS × sexo × idade simples (TabNet, idade detalhada) |
| `populacao_salvador_bairro_ds_idade_raca_2000_2027.csv` | tabela completa com idade (passa do limite do Excel) |
| `populacao_bairro_idade_raca_por_ano.zip` | um CSV por ano (abre no Excel), com nomes de DS e bairro, e o dicionário |

O bairro 2 (Aeroporto), sem população residente, aparece com FREQ = 0 em todas as saídas.

**6. Registre a versão.** Faça commit com a mensagem `Atualização total 2027` e crie uma *release* no GitHub. O Zenodo gera um novo DOI automaticamente (ver [Histórico de versões](11-Historico-de-versoes)).

## 7.2 O que acontece com os anos anteriores?

Nada muda. Cada ano depende só do seu total $T(t)$ e da fórmula $s_c(t)$, que é fixa enquanto as estruturas de 2000, 2010 e 2022 forem as mesmas. Acrescentar 2027 **não altera** 2000–2026. (Teste feito: com um total fictício de 2027, as 942.840 células de 2000–2026 ficaram idênticas.)

## 7.3 Quando é preciso rodar `03_estrutura_base.R`

Só quando mudar a estrutura:

- um **novo censo** (substituir 2010 por 2022 e 2022 pelo novo, e ajustar a fórmula $w$);
- um **novo bairro** oficial (como o Aquarius);
- uma mudança nos **limites dos DS**;
- uma correção dos agregados do IBGE.

Nesses casos: rode `01_chave_setor_bairro_ds.R` e `01b_chave_setor2010.R` (e `02_aquarius.R` quando houver polígono oficial, ou `02b_boa_vista_lobato_cnefe.R` quando a lei listar logradouros), depois `03_estrutura_base.R`, refaça a calibração censitária (implementação de referência em `python/v5_*.py`; ver [página 13](13-Dialogo-entre-bases)) e por fim os scripts 04 a 07.

## 7.4 Se o total de algum ano for revisado

Edite o valor em `totais_municipais.csv` e rode o `04` de novo. Só aquele ano muda.
