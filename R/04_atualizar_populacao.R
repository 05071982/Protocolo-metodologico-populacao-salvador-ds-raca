# =====================================================================
# 04_atualizar_populacao.R  (versão 4)
# Gera a base populacional de Salvador (ANO, DS, COD_BAIRRO, FXET, SEXO,
# RACA, FREQ) para todos os anos de dados/entrada/totais_municipais.csv.
#
# USO ANUAL (ex.: saiu o total de 2027) — só isto:
#   1. Acrescente uma linha ao final de dados/entrada/totais_municipais.csv:
#        2027,<total TCU/IBGE>,TCU/IBGE,0
#   2. Rode, nesta ordem: 04_atualizar_populacao.R, 05_idade_simples.R,
#      06_bairro_idade_raca.R e 07_exportar_por_ano.R.
#   3. Resultados em resultados/ (CSV completos e zip com um arquivo por ano).
#
# Não é preciso reprocessar os censos: as estruturas calibradas de 2000,
# 2010 e 2022 já estão em dados/estrutura/ (ver wiki, página 13).
# Método: Razão Censitária com razões variáveis, ancorada em três censos.
#   - 2000, 2010, 2022: valores censitários calibrados (inteiros, prontos)
#   - 2001–2009: interpolação geométrica 2000→2010
#   - 2011–2021: interpolação geométrica 2010→2022
#   - 2023 em diante: extrapolação da tendência 2010→2022 (w > 1)
#   Todo ano não censitário fecha no total de totais_municipais.csv.
# =====================================================================

rm(list = ls())

# ---- Pasta do repositório (ajuste se necessário) --------------------
raiz <- getwd()          # abra o projeto .Rproj ou use setwd("C:/.../repositorio")
source(file.path(raiz, "R", "funcoes.R"))

# ---- Entradas --------------------------------------------------------
totais <- read.csv(file.path(raiz, "dados/entrada/totais_municipais.csv"))
totais <- totais[order(totais$ANO), ]
stopifnot(!anyDuplicated(totais$ANO), all(totais$TOTAL > 0))
le <- function(a) read.csv(file.path(raiz, "dados/estrutura", a))
e00 <- le("estrutura_2000_ds.csv"); e10 <- le("estrutura_2010_ds.csv"); e22 <- le("estrutura_2022_ds.csv")
u22 <- le("estrutura_2022_bairro_ds.csv")

# Ordem canônica das 2.160 células: DS > SEXO > FXET > RACA (RACA varia mais rápido)
ordena <- function(d) d[order(d$DS, d$SEXO, d$FXET, d$RACA), ]
e00 <- ordena(e00); e10 <- ordena(e10); e22 <- ordena(e22)
stopifnot(nrow(e00) == 2160, nrow(e10) == 2160, nrow(e22) == 2160)
celula <- e10[, c("DS", "SEXO", "FXET", "RACA")]

C00 <- e00$POP; C10 <- e10$POP; C22 <- e22$POP          # inteiros calibrados aos censos
censo <- list("2000" = C00, "2010" = C10, "2022" = C22)
part <- function(C) (C + 0.5) / sum(C + 0.5)             # pseudo-contagem 0,5 evita log(0)
s00 <- part(C00); s10 <- part(C10); s22 <- part(C22)

# ---- 1. Série por DS × sexo × faixa × raça ---------------------------
serie_ds <- vector("list", nrow(totais))
for (i in seq_len(nrow(totais))) {
  ano <- totais$ANO[i]; Tt <- totais$TOTAL[i]
  if (as.character(ano) %in% names(censo)) {
    Xi <- censo[[as.character(ano)]]
    if (sum(Xi) != round(Tt)) stop("Total de ", ano, " difere do censo: ", sum(Xi))
  } else {
    if (ano < 2000) stop("Anos anteriores a 2000 não são suportados")
    Xi <- arred_maior_resto(composicao_ano(s00, s10, s22, ano) * Tt, round(Tt))
  }
  serie_ds[[i]] <- cbind(ANO = ano, celula, FREQ_DS = Xi)
}
serie_ds <- do.call(rbind, serie_ds)

# ---- 2. Repartição de cada célula do DS entre os bairros (proporção de 2022) ----
u22 <- u22[order(u22$UNIDADE, u22$SEXO, u22$FXET, u22$RACA), ]
c22u <- aggregate(POP ~ DS + SEXO + FXET + RACA, u22, sum)          # soma das unidades no DS
names(c22u)[5] <- "C22_DS"
u22 <- merge(u22, c22u, by = c("DS", "SEXO", "FXET", "RACA"), sort = FALSE)
tot_u  <- tapply(u22$POP, u22$UNIDADE, sum)
u_ds   <- tapply(u22$DS, u22$UNIDADE, `[`, 1)
tot_ds <- tapply(tot_u, u_ds, sum)
share_fallback <- (tot_u / tot_ds[as.character(u_ds)])[as.character(u22$UNIDADE)]
u22$SH <- ifelse(u22$C22_DS > 0, u22$POP / u22$C22_DS, share_fallback)

resultado <- vector("list", nrow(totais))
for (i in seq_len(nrow(totais))) {
  ano <- totais$ANO[i]
  d <- merge(u22[, c("UNIDADE", "DS", "COD_BAIRRO", "SEXO", "FXET", "RACA", "SH")],
             serie_ds[serie_ds$ANO == ano, ], by = c("DS", "SEXO", "FXET", "RACA"))
  d$X  <- d$FREQ_DS * d$SH
  d$FL <- floor(d$X + 1e-9)
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

# ---- 2b. Bairros oficiais sem população residente (ex.: 2 – Aeroporto): linhas com FREQ = 0
dic <- read.csv(file.path(raiz, "dados/dicionarios/bairros.csv"))
sem <- dic[!dic$COD_BAIRRO %in% pop$COD_BAIRRO, ]
if (nrow(sem) > 0) {
  z <- expand.grid(RACA = 1:5, FXET = 1:18, SEXO = 1:2, COD_BAIRRO = sem$COD_BAIRRO, ANO = totais$ANO)
  z$DS <- sem$DS_PRINCIPAL[match(z$COD_BAIRRO, sem$COD_BAIRRO)]
  z$FREQ <- 0L
  pop <- rbind(pop, z[, names(pop)])
  pop <- pop[order(pop$ANO, pop$DS, pop$COD_BAIRRO, pop$SEXO, pop$FXET, pop$RACA), ]
}
stopifnot(setequal(unique(pop$COD_BAIRRO), dic$COD_BAIRRO))     # os 171 bairros em todos os anos

# ---- 3. Conferências -------------------------------------------------
chk <- aggregate(FREQ ~ ANO, pop, sum)
chk <- merge(chk, totais[, c("ANO", "TOTAL")])
stopifnot(all(chk$FREQ == round(chk$TOTAL)), all(pop$FREQ >= 0))
chk_ds <- merge(aggregate(FREQ ~ ANO + DS + SEXO + FXET + RACA, pop, sum), serie_ds)
stopifnot(all(chk_ds$FREQ == chk_ds$FREQ_DS))
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
