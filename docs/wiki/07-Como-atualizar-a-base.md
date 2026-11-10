# 7. Como atualizar a base (ex.: total de 2027)

A atualização anual **não** exige reprocessar o Censo. A estrutura de 2010 e 2022 já está pronta em `dados/estrutura/`. Basta informar o novo total.

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
source("R/04_atualizar_populacao.R")
```

Não precisa instalar pacotes: o script usa só o R base.

**4. Confira o console.** O script para com erro se:

- a soma de algum ano diferir do total informado;
- surgir algum valor negativo.

**5. Pegue os resultados em `resultados/`:**

| Arquivo | Uso |
|---|---|
| `populacao_salvador_bairro_ds_2000_2027.csv` | TabNet Salvador e Painel Sociodemográfico (`ANO, DS, COD_BAIRRO, FXET, SEXO, RACA, FREQ`) |
| `populacao_salvador_ds_2000_2027.csv` | versão agregada por DS (formato `pop14`) |

**6. Registre a versão.** Faça commit com a mensagem `Atualização total 2027` e crie uma *release* no GitHub. O Zenodo gera um novo DOI automaticamente (ver [Histórico de versões](11-Historico-de-versoes)).

## 7.2 O que acontece com os anos anteriores?

Nada muda. Cada ano depende só do seu total $T(t)$ e da fórmula $s_c(t)$, que é fixa enquanto a estrutura de 2010 e 2022 for a mesma. Acrescentar 2027 **não altera** 2000–2026.

## 7.3 Quando é preciso rodar `03_estrutura_base.R`

Só quando mudar a estrutura:

- um **novo censo** (substituir 2010 por 2022 e 2022 pelo novo, e ajustar a fórmula $w$);
- um **novo bairro** oficial (como o Aquarius);
- uma mudança nos **limites dos DS**;
- uma correção dos agregados do IBGE.

Nesses casos: rode `01_chave_setor_bairro_ds.R` (e `02_aquarius.R` ou um equivalente para o novo bairro), depois `03_estrutura_base.R` e por fim `04_atualizar_populacao.R`.

## 7.4 Se o total de algum ano for revisado

Edite o valor em `totais_municipais.csv` e rode o `04` de novo. Só aquele ano muda.
