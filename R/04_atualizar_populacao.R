# =====================================================================
# 04_atualizar_populacao.R
# Gera a base populacional de Salvador (ANO, DS, COD_BAIRRO, FXET, SEXO,
# RACA, FREQ) para todos os anos de dados/entrada/totais_municipais.csv.
#
# USO ANUAL (ex.: saiu o total de 2027):
#   1. Acrescente uma linha em dados/entrada/totais_municipais.csv:
#        2027,<total TCU/IBGE>,TCU/IBGE,0
#   2. Rode este script (Ctrl+Shift+S no RStudio).
#   3. Resultado em resultados/populacao_salvador_bairro_ds_<ano_ini>_<ano_fim>.csv
#
# Não é preciso reprocessar os censos: a estrutura de 2010 e 2022
# (dados/estrutura/) já está calculada (ver 03_estrutura_base.R).
# Método: Razão Censitária com razões variáveis (ver wiki).
# =====================================================================

rm(list = ls())

# ---- Pasta do repositório (ajuste se necessário) --------------------
raiz <- getwd()          # abra o projeto .Rproj ou use setwd("C:/.../repositorio")
source(file.path(raiz, "R", "funcoes.R"))

# ---- Entradas --------------------------------------------------------
totais <- read.csv(file.path(raiz, "dados/entrada/totais_municipais.csv"))
e10 <- read.csv(file.path(raiz, "dados/estrutura/estrutura_2010_ds.csv"))
e22 <- read.csv(file.path(raiz, "dados/estrutura/estrutura_2022_ds.csv"))
u22 <- read.csv(file.path(raiz, "dados/estrutura/estrutura_2022_bairro_ds.csv"))

# Ordem canônica das 2.160 células: DS > SEXO > FXET > RACA (RACA varia mais rápido)
ordena <- function(d) d[order(d$DS, d$SEXO, d$FXET, d$RACA), ]
e10 <- ordena(e10); e22 <- ordena(e22)
stopifnot(nrow(e10) == 2160, nrow(e22) == 2160)
celula <- e10[, c("DS", "SEXO", "FXET", "RACA")]
grupo_dsa <- interaction(celula$DS, celula$SEXO, celula$FXET, drop = TRUE, lex.order = TRUE)

C10 <- e10$POP; C22 <- e22$POP
s10 <- (C10 + 0.5) / sum(C10 + 0.5)   # pseudo-contagem 0,5 evita log(0)
s22 <- (C22 + 0.5) / sum(C22 + 0.5)
pr_raca_2010 <- C10 / ave(C10, grupo_dsa, FUN = sum)       # P(raça | DS, sexo, faixa) em 2010
pr_raca_2010[is.nan(pr_raca_2010)] <- 0

# ---- 1. Série por DS × sexo × faixa × raça ---------------------------
serie_ds <- vector("list", nrow(totais))
for (i in seq_len(nrow(totais))) {
  ano <- totais$ANO[i]; Tt <- totais$TOTAL[i]
  s <- composicao_ano(s10, s22, ano)
  if (ano < 2010) {                       # antes de 2010: raça congelada na distribuição de 2010
    s <- ave(s, grupo_dsa, FUN = sum) * pr_raca_2010
    s <- s / sum(s)
  }
  if (ano == 2010) {                      # censo 2010: fecha exatamente em cada DS × sexo × faixa (SESAB)
    Xi <- integer(length(C10))
    for (g in levels(grupo_dsa)) {
      k <- which(grupo_dsa == g)
      Xi[k] <- arred_maior_resto(C10[k], round(sum(C10[k])))
    }
  } else if (ano == 2022) {
    Xi <- arred_maior_resto(C22, round(Tt))
  } else {
    Xi <- arred_maior_resto(s * Tt, round(Tt))
  }
  serie_ds[[i]] <- cbind(ANO = ano, celula, FREQ_DS = Xi)
}
serie_ds <- do.call(rbind, serie_ds)

# ---- 2. Repartição de cada célula do DS entre os bairros (proporção de 2022) ----
u22 <- u22[order(u22$UNIDADE, u22$SEXO, u22$FXET, u22$RACA), ]
u22 <- merge(u22, setNames(e22, c("DS", "SEXO", "FXET", "RACA", "C22_DS")),
             by = c("DS", "SEXO", "FXET", "RACA"), sort = FALSE)
tot_u  <- tapply(u22$POP, u22$UNIDADE, sum)
tot_ds <- tapply(tot_u, tapply(u22$DS, u22$UNIDADE, `[`, 1), sum)
u_ds   <- tapply(u22$DS, u22$UNIDADE, `[`, 1)
share_fallback <- (tot_u / tot_ds[as.character(u_ds)])[as.character(u22$UNIDADE)]
u22$SH <- ifelse(u22$C22_DS > 0, u22$POP / u22$C22_DS, share_fallback)

resultado <- vector("list", nrow(totais))
for (i in seq_len(nrow(totais))) {
  ano <- totais$ANO[i]
  d <- merge(u22[, c("UNIDADE", "DS", "COD_BAIRRO", "SEXO", "FXET", "RACA", "SH")],
             serie_ds[serie_ds$ANO == ano, ], by = c("DS", "SEXO", "FXET", "RACA"))
  d$X  <- d$FREQ_DS * d$SH
  d$FL <- floor(d$X)
  d$FR <- d$X - d$FL
  d$CH <- interaction(d$DS, d$SEXO, d$FXET, d$RACA, drop = TRUE)
  d <- d[order(d$CH, -d$FR, d$UNIDADE), ]                          # maior resto; desempate estável
  falta <- d$FREQ_DS - ave(d$FL, d$CH, FUN = sum)                  # unidades a distribuir na célula
  pos   <- ave(seq_len(nrow(d)), d$CH, FUN = seq_along)             # posição no ranking da célula
  d$FREQ <- as.integer(d$FL + (pos <= falta))
  resultado[[i]] <- d[, c("ANO", "DS", "COD_BAIRRO", "FXET", "SEXO", "RACA", "FREQ")]
}
pop <- do.call(rbind, resultado)
pop <- pop[order(pop$ANO, pop$DS, pop$COD_BAIRRO, pop$SEXO, pop$FXET, pop$RACA), ]

# ---- 3. Conferências -------------------------------------------------
chk <- aggregate(FREQ ~ ANO, pop, sum)
chk <- merge(chk, totais[, c("ANO", "TOTAL")])
stopifnot(all(chk$FREQ == round(chk$TOTAL)))
stopifnot(all(pop$FREQ >= 0))
print(chk)

# ---- 4. Saída --------------------------------------------------------
dir.create(file.path(raiz, "resultados"), showWarnings = FALSE)
arq <- file.path(raiz, "resultados",
                 sprintf("populacao_salvador_bairro_ds_%d_%d.csv", min(pop$ANO), max(pop$ANO)))
write.csv(pop, arq, row.names = FALSE, fileEncoding = "UTF-8")
cat("Arquivo gerado:", arq, "\nLinhas:", nrow(pop), "\n")

# Versão agregada por DS (formato pop14 / TabNet)
pop_ds <- aggregate(FREQ ~ ANO + FXET + DS + SEXO + RACA, pop, sum)
write.csv(pop_ds[order(pop_ds$ANO, pop_ds$DS, pop_ds$SEXO, pop_ds$FXET, pop_ds$RACA), ],
          sub("bairro_ds", "ds", arq), row.names = FALSE, fileEncoding = "UTF-8")
