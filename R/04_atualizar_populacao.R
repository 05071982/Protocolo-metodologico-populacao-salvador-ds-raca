# =====================================================================
# 04_atualizar_populacao.R  (versão 5)
# Gera a base populacional de Salvador (ANO, DS, COD_BAIRRO, FXET, SEXO,
# RACA, FREQ) para todos os anos de dados/entrada/totais_municipais.csv.
#
# USO ANUAL (ex.: saiu o total de 2027) — só isto:
#   1. Acrescente uma linha ao final de dados/entrada/totais_municipais.csv:
#        2027,<total TCU/IBGE>,TCU/IBGE,0
#   2. Rode, nesta ordem: 04_atualizar_populacao.R, 05_idade_simples.R,
#      06_bairro_idade_raca.R e 07_exportar_por_ano.R.
#
# Estruturas prontas em dados/estrutura/ (194 unidades bairro × DS, limites atuais):
#   2000 (margens do Censo 2000), 2010 (setores censitários 2010) e 2022 (setores 2022),
#   todas calibradas ao IBGE (ver wiki, páginas 4 e 13).
# Método (Razão Censitária com razões variáveis):
#   - 2000, 2010, 2022: valores censitários calibrados (inteiros, prontos)
#   - 2001–2009 e 2011–2021: interpolação geométrica das participações de cada
#     célula unidade × sexo × faixa × raça entre os censos vizinhos
#   - 2023 em diante: tendência 2010→2022 nas células DS × sexo × faixa × raça,
#     repartida entre as unidades do DS pela proporção de 2022
#   Todo ano não censitário fecha no total de totais_municipais.csv.
# =====================================================================
rm(list = ls())
raiz <- getwd()          # abra o projeto .Rproj ou use setwd("C:/.../repositorio")
source(file.path(raiz, "R", "funcoes.R"))

totais <- read.csv(file.path(raiz, "dados/entrada/totais_municipais.csv"))
totais <- totais[order(totais$ANO), ]
stopifnot(!anyDuplicated(totais$ANO), all(totais$TOTAL > 0), min(totais$ANO) >= 2000)
le <- function(a) { d <- read.csv(file.path(raiz, "dados/estrutura", a)); d[order(d$UNIDADE, d$SEXO, d$FXET, d$RACA), ] }
e00 <- le("estrutura_2000_unidade.csv"); e10 <- le("estrutura_2010_unidade.csv"); e22 <- le("estrutura_2022_unidade.csv")
stopifnot(nrow(e10) == 194 * 180, nrow(e00) == nrow(e10), nrow(e22) == nrow(e10))
cel <- e10[, c("UNIDADE", "DS", "COD_BAIRRO", "SEXO", "FXET", "RACA")]
C00 <- e00$POP; C10 <- e10$POP; C22 <- e22$POP
censo <- list("2000" = C00, "2010" = C10, "2022" = C22)
part <- function(C, eps) (C + eps) / sum(C + eps)
s00 <- part(C00, 0.1); s10 <- part(C10, 0.1); s22 <- part(C22, 0.1)      # unidades

# --- extrapolação após 2022: células DS × sexo × faixa × raça (2.160)
chave_ds <- paste(cel$DS, cel$SEXO, cel$FXET, cel$RACA)
ds_cel <- unique(cel[order(cel$DS, cel$SEXO, cel$FXET, cel$RACA), c("DS", "SEXO", "FXET", "RACA")])
kds <- paste(ds_cel$DS, ds_cel$SEXO, ds_cel$FXET, ds_cel$RACA)
D10 <- as.numeric(tapply(C10, factor(chave_ds, levels = kds), sum))
D22 <- as.numeric(tapply(C22, factor(chave_ds, levels = kds), sum))
d10 <- part(D10, 0.5); d22 <- part(D22, 0.5)
D22u <- D22[match(chave_ds, kds)]
tot_u <- tapply(C22, cel$UNIDADE, sum); tot_dsu <- tapply(tot_u, tapply(cel$DS, cel$UNIDADE, `[`, 1), sum)
sh_fb <- as.numeric(tot_u[as.character(cel$UNIDADE)] / tot_dsu[as.character(cel$DS)])
SH <- ifelse(D22u > 0, C22 / ifelse(D22u > 0, D22u, 1), sh_fb)

extrapola <- function(ano, Tt) {
  w <- (ano - 2010) / 12
  s <- exp((1 - w) * log(d10) + w * log(d22)); s <- s / sum(s)
  Xd <- arred_maior_resto(s * Tt, round(Tt))
  X  <- Xd[match(chave_ds, kds)] * SH
  FL <- floor(X + 1e-9); FR <- X - FL
  o  <- order(chave_ds, -FR, cel$UNIDADE)              # maior resto dentro da célula do DS; desempate pela unidade
  falta <- Xd[match(chave_ds, kds)] - ave(FL, chave_ds, FUN = sum)
  pos <- integer(length(X)); pos[o] <- ave(seq_along(o), chave_ds[o], FUN = seq_along)
  as.integer(FL + (pos <= falta))
}

res <- vector("list", nrow(totais))
for (i in seq_len(nrow(totais))) {
  ano <- totais$ANO[i]; Tt <- totais$TOTAL[i]
  if (as.character(ano) %in% names(censo)) {
    Xi <- censo[[as.character(ano)]]
    if (sum(Xi) != round(Tt)) stop("Total de ", ano, " difere do censo: ", sum(Xi))
  } else if (ano > 2022) {
    Xi <- extrapola(ano, Tt)
  } else {
    Xi <- arred_maior_resto(composicao_ano(s00, s10, s22, ano) * Tt, round(Tt))
  }
  res[[i]] <- data.frame(ANO = ano, cel[, c("DS", "COD_BAIRRO", "FXET", "SEXO", "RACA")], FREQ = Xi)
}
pop <- do.call(rbind, res)

# Bairros oficiais sem população residente (ex.: 2 – Aeroporto): linhas com FREQ = 0
dic <- read.csv(file.path(raiz, "dados/dicionarios/bairros.csv"))
sem <- dic[!dic$COD_BAIRRO %in% pop$COD_BAIRRO, ]
if (nrow(sem) > 0) {
  z <- expand.grid(RACA = 1:5, FXET = 1:18, SEXO = 1:2, COD_BAIRRO = sem$COD_BAIRRO, ANO = totais$ANO)
  z$DS <- sem$DS_PRINCIPAL[match(z$COD_BAIRRO, sem$COD_BAIRRO)]; z$FREQ <- 0L
  pop <- rbind(pop, z[, names(pop)])
}
pop <- pop[order(pop$ANO, pop$DS, pop$COD_BAIRRO, pop$SEXO, pop$FXET, pop$RACA), ]
stopifnot(setequal(unique(pop$COD_BAIRRO), dic$COD_BAIRRO), all(pop$FREQ >= 0))
chk <- merge(aggregate(FREQ ~ ANO, pop, sum), totais[, c("ANO", "TOTAL")])
stopifnot(all(chk$FREQ == round(chk$TOTAL)))
print(chk)

dir.create(file.path(raiz, "resultados"), showWarnings = FALSE)
arq <- file.path(raiz, "resultados", sprintf("populacao_salvador_bairro_ds_%d_%d.csv", min(pop$ANO), max(pop$ANO)))
write.csv(pop, arq, row.names = FALSE, fileEncoding = "UTF-8")
pop_ds <- aggregate(FREQ ~ ANO + FXET + DS + SEXO + RACA, pop, sum)
write.csv(pop_ds[order(pop_ds$ANO, pop_ds$DS, pop_ds$SEXO, pop_ds$FXET, pop_ds$RACA), ],
          sub("bairro_ds", "ds", arq), row.names = FALSE, fileEncoding = "UTF-8")
cat("Arquivo gerado:", arq, "\nLinhas:", nrow(pop), "\n")
