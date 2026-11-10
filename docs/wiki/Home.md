# Protocolo Metodológico para estimativa populacional de Salvador

**Base populacional de Salvador por Distrito Sanitário (DS), bairro, sexo, faixa etária e raça/cor — 2000 a 2026**

Sala de Situação em Saúde de Salvador (SDSS) · Secretaria Municipal da Saúde de Salvador (SMS)

---

## Para que serve

Esta base é o **denominador populacional** do **TabNet Salvador**, do **Painel Sociodemográfico/Socioambiental** e de todos os painéis de BI da SMS que calculam taxas, coberturas e incidências. Ela responde a uma necessidade antiga: ter, em um único arquivo e com método documentado, a população de Salvador desagregada por

| Dimensão | Categorias |
|---|---|
| Ano | 2000 a 2026 (atualizável a cada nova estimativa) |
| Distrito Sanitário | 12 DS |
| Bairro | 171 bairros oficiais (Lei 9.278/2017 e alterações, incluindo o Aquarius, Lei 9.778/2024) |
| Sexo | Masculino, Feminino |
| Faixa etária | 18 faixas (as mesmas do antigo `pop14`) |
| Raça/cor | Branca, Preta, Amarela, Parda, Indígena (códigos IBGE/SIM/SINASC) |

A tabela oficial tem o layout:

```
ANO | DS | COD_BAIRRO | FXET | SEXO | RACA | FREQ
```

## Em uma frase

Os **totais municipais** vêm do Censo nos anos censitários (2000, 2010, 2022) e das estimativas oficiais **TCU/IBGE** nos demais anos. A **distribuição interna** (DS × bairro × sexo × idade × raça) vem dos Censos 2010 e 2022 pelo **Método da Razão Censitária com razões variáveis**, uma evolução do método usado até 2023 no TabNet Salvador.

## Navegação

1. [Contexto e objetivos](01-Contexto-e-objetivos)
2. [Fontes de dados](02-Fontes-de-dados)
3. [Diagnóstico das bases existentes](03-Diagnostico-das-bases)
4. [Método passo a passo](04-Metodo-passo-a-passo)
5. [Comparação entre métodos: Lagrange × Razão fixa × Razão variável](05-Comparacao-entre-metodos)
6. [Resultados](06-Resultados)
7. [Como atualizar a base (ex.: total de 2027)](07-Como-atualizar-a-base)
8. [Códigos R](08-Codigos-R)
9. [Limitações](09-Limitacoes)
10. [Referências](10-Referencias)
11. [Histórico de versões](11-Historico-de-versoes)

Documento-síntese: [Protocolo Metodológico para estimativa populacional de Salvador](Protocolo-Metodológico-para-estimativa-populacional-de-Salvador)

## Equipe

- **Jessidenes Teixeira de Freitas Mendes Leal**
- **Rafaella Santiago Coutinho Santos**

## Como citar

> Leal JTFM, Santos RSC. Protocolo metodológico para estimativa populacional de Salvador por distrito sanitário, bairro, sexo, idade e raça/cor, 2000–2026. Salvador: Secretaria Municipal da Saúde de Salvador; 2026. Disponível em: https://github.com/05071982/Protocolo-metodologico-populacao-salvador-ds-raca

(Um DOI será atribuído via Zenodo; ver [Histórico de versões](11-Historico-de-versoes).)
