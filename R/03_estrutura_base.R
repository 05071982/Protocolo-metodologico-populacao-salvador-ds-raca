# =====================================================================
# 03_estrutura_base.R — Reconstrói a ESTRUTURA BASE (2010 e 2022)
# Só precisa ser rodado de novo se mudar algum insumo censitário
# (nova chave setor→bairro→DS, novo bairro, correção do IBGE etc.).
# Para atualização anual (novo total TCU) use 04_atualizar_populacao.R.
#
# Entradas:
#   pasta_censo/pop_*.csv     — 12 arquivos de setores 2022 por DS (Drive:
#                               "Pop DS - Censo 2022"; agregados IBGE de
#                               demografia + cor/raça + básico por setor)
#   dados/entrada/chave_setor_bairro_ds_2022.csv
#   dados/entrada/populacao_bairros_ibge_2022.csv
#   dados/entrada/sesab_2010_ds_sexo_fxet.csv
#   dados/entrada/raca_2010_ds_banco_parcial.csv
# Saídas:
#   dados/estrutura/estrutura_2010_ds.csv
#   dados/estrutura/estrutura_2022_ds.csv
#   dados/estrutura/estrutura_2022_bairro_ds.csv
#
# Implementação de referência (validada) em python/: s22.py, p2_s22.py,
# v3_model.py. Este script reproduz a mesma lógica em R.
# =====================================================================
rm(list = ls())
raiz <- getwd()
source(file.path(raiz, "R", "funcoes.R"))
pasta_censo <- "C:/Users/SEU_USUARIO/Documents/pop_ds/Pop DS - Censo 2022"   # <-- ajuste

R5  <- c("branco", "preto", "amarelo", "pardo", "indigena")
A11 <- c("0a4","5a9","10a14","15a19","20a24","25a29","30a39","40a49","50a59","60a69","70m")
arqs <- c(`1`="pop_centro.csv", `2`="pop_itapagipe.csv", `3`="pop_SCV.csv", `4`="pop_liberdade.csv",
          `5`="pop_brotas.csv", `6`="pop_barra.csv", `7`="pop_boca.csv", `8`="pop_itapua.csv",
          `9`="pop_cab.csv", `10`="pop_pl.csv", `11`="pop_suburbio.csv", `12`="pop_caj.csv")

# ---- 1. Setores 2022 (únicos) ----------------------------------------
lista <- lapply(arqs, function(f) read.csv(file.path(pasta_censo, f), colClasses = "character", check.names = FALSE))
s <- do.call(rbind, lapply(lista, function(d) d[, setdiff(names(d), "")]))
s <- s[!duplicated(s$CD_setor), ]                     # setores de fronteira apareciam em 2–3 arquivos
num <- function(v) suppressWarnings(as.numeric(ifelse(v == "X", NA, v)))   # "X" = sigilo IBGE
X <- as.data.frame(lapply(s[, setdiff(names(s), c("CD_setor", "Cod_municipio"))], num))
X$populacao[is.na(X$populacao)] <- X$moradores[is.na(X$populacao)]
X$moradores[is.na(X$moradores)] <- X$populacao[is.na(X$moradores)]

# Imputação do sigilo: o resíduo (total do bloco − soma conhecida) é dividido
# igualmente entre as células "X" do bloco.
preenche <- function(X, total, partes) {
  P <- as.matrix(X[, partes]); conhecido <- rowSums(P, na.rm = TRUE)
  nmiss <- rowSums(is.na(P)); res <- pmax(X[[total]] - conhecido, 0)
  val <- ifelse(nmiss > 0, res / nmiss, 0)
  for (p in partes) X[[p]] <- ifelse(is.na(X[[p]]), val, X[[p]])
  X
}
X$masculino <- ifelse(is.na(X$masculino), X$moradores - X$feminino, X$masculino)
X$feminino  <- ifelse(is.na(X$feminino),  X$moradores - X$masculino, X$feminino)
X <- preenche(X, "moradores", c("masculino", "feminino"))
X <- preenche(X, "masculino", paste0("m_", A11)); X <- preenche(X, "feminino", paste0("f_", A11))
X <- preenche(X, "moradores", R5)
X <- preenche(X, "masculino", paste0("m_", R5)); X <- preenche(X, "feminino", paste0("f_", R5))
for (sx in c("m", "f")) {
  tot <- if (sx == "m") "masculino" else "feminino"
  X[[paste0(sx, "_0a9")]] <- X[[paste0(sx, "_0a4")]] + X[[paste0(sx, "_5a9")]]
  X[[paste0(sx, "_10m")]] <- X[[tot]] - X[[paste0(sx, "_0a9")]]
  X <- preenche(X, paste0(sx, "_0a9"), paste0(sx, "_0a9_", R5))
  X <- preenche(X, paste0(sx, "_10m"), paste0(sx, "_10m_", R5))
}
age4 <- list(`0a4` = c("0a4","5a9","10a14"), `15a29` = c("15a19","20a24","25a29"),
             `30a59` = c("30a39","40a49","50a59"), `60m` = c("60a69","70m"))
for (g in names(age4)) {
  X[[paste0("tot_", g)]] <- Reduce(`+`, lapply(age4[[g]], function(a) X[[paste0("m_", a)]] + X[[paste0("f_", a)]]))
  X <- preenche(X, paste0("tot_", g), paste0(g, "_", R5))   # obs.: "0a4_*" no IBGE = 0 a 14 anos
}
X$CD_SETOR <- s$CD_setor

# ---- 2. Chave setor → bairro → DS e calibração ao total oficial do bairro ----
chave <- read.csv(file.path(raiz, "dados/entrada/chave_setor_bairro_ds_2022.csv"), colClasses = c(CD_SETOR = "character"))
X <- merge(X, chave[, c("CD_SETOR", "DS", "COD_BAIRRO")], by = "CD_SETOR")
X$COD_BAIRRO[is.na(X$COD_BAIRRO)] <- 0
of <- read.csv(file.path(raiz, "dados/entrada/populacao_bairros_ibge_2022.csv"))
off <- setNames(of$POP_IBGE_2022, of$COD_BAIRRO)
obs <- tapply(X$moradores, X$COD_BAIRRO, sum)
# Aquarius (171) foi desmembrado da Pituba (130): reparte o total oficial da Pituba
tp <- off["130"]; off["171"] <- tp * obs["171"] / (obs["171"] + obs["130"]); off["130"] <- tp - off["171"]
fac <- off[names(obs)] / obs; fac[is.na(fac)] <- 1
vars <- setdiff(names(X), c("CD_SETOR", "DS", "COD_BAIRRO"))
X[, vars] <- X[, vars] * fac[as.character(X$COD_BAIRRO)]
G <- aggregate(X[, vars], by = list(DS = X$DS, COD_BAIRRO = X$COD_BAIRRO), FUN = sum)
G <- G[order(G$DS, G$COD_BAIRRO), ]
cat("Total 2022:", round(sum(G$moradores)), " unidades bairro×DS:", nrow(G), "\n")

# ---- 3. IPF por unidade e abertura em 18 faixas ----------------------
S <- read.csv(file.path(raiz, "dados/entrada/sesab_2010_ds_sexo_fxet.csv"))
sesab <- function(ds, sx) S$POP[S$DS == ds & S$SEXO == sx][order(S$FXET[S$DS == ds & S$SEXO == sx])]
g4 <- c(1,1,1,2,2,2,3,3,3,4,4); g2 <- c(1,1,2,2,2,2,2,2,2,2,2)
sd <- function(a, b) ifelse(b > 0, a / ifelse(b > 0, b, 1), 0)

ajusta_unidade <- function(g, ds) {
  N <- g$moradores
  if (N <= 0) return(array(0, c(2, 18, 5)))
  nz <- function(M) if (sum(M) > 0) M * N / sum(M) else array(N / length(M), dim(M))
  M1 <- nz(rbind(unlist(g[paste0("m_", A11)]), unlist(g[paste0("f_", A11)])))                    # sexo × idade
  M2 <- nz(rbind(unlist(g[paste0("m_", R5)]),  unlist(g[paste0("f_", R5)])))                     # sexo × raça
  M3 <- nz(t(sapply(names(age4), function(q) unlist(g[paste0(q, "_", R5)]))))                    # idade4 × raça
  M4 <- array(0, c(2, 2, 5))                                                                    # sexo × idade2 × raça
  for (i in 1:2) for (j in 1:2) M4[i, j, ] <- unlist(g[paste0(c("m","f")[i], "_", c("0a9","10m")[j], "_", R5)])
  M4 <- nz(M4)
  A <- array(1, c(2, 11, 5))
  for (it in 1:200) {
    A <- A * array(sd(M1, apply(A, c(1, 2), sum)), c(2, 11, 5))
    A <- A * aperm(array(sd(M2, apply(A, c(1, 3), sum)), c(2, 5, 11)), c(1, 3, 2))
    B3 <- matrix(0, 4, 5); for (i in 1:11) B3[g4[i], ] <- B3[g4[i], ] + colSums(A[, i, ])
    f3 <- sd(M3, B3); for (i in 1:11) A[, i, ] <- sweep(A[, i, ], 2, f3[g4[i], ], `*`)
    B4 <- array(0, c(2, 2, 5)); for (i in 1:11) B4[, g2[i], ] <- B4[, g2[i], ] + A[, i, ]
    f4 <- sd(M4, B4); for (i in 1:11) A[, i, ] <- A[, i, ] * f4[, g2[i], ]
  }
  A <- A * N / sum(A)
  Y <- array(0, c(2, 18, 5))
  for (si in 1:2) {
    s10 <- sesab(ds, si); r2 <- function(a, b) c(a, b) / (a + b)
    sp <- list(list(s10[1:2] / sum(s10[1:2]), 1:2), list(1, 3), list(1, 4), list(1, 5), list(1, 6), list(1, 7),
               list(r2(.4*s10[5] + .6*s10[6],  .4*s10[6] + .6*s10[7]),   8:9),     # 30–39 por coortes
               list(r2(.4*s10[7] + .6*s10[8],  .4*s10[8] + .6*s10[9]),   10:11),   # 40–49
               list(r2(.4*s10[9] + .6*s10[10], .4*s10[10] + .6*s10[11]), 12:13),   # 50–59
               list(r2(.4*s10[11] + .6*s10[12], .4*s10[12] + .6*s10[13]), 14:15),  # 60–69
               list(s10[16:18] / sum(s10[16:18]), 16:18))                          # 70+ (período 2010)
    for (i in 1:11) for (j in seq_along(sp[[i]][[2]]))
      Y[si, sp[[i]][[2]][j], ] <- Y[si, sp[[i]][[2]][j], ] + sp[[i]][[1]][j] * A[si, i, ]
  }
  Y
}

U <- lapply(seq_len(nrow(G)), function(i) ajusta_unidade(G[i, ], G$DS[i]))
longo <- function(A, extra) {
  idx <- expand.grid(RACA = 1:5, FXET = 1:18, SEXO = 1:2)[, 3:1]
  cbind(extra, idx, POP = A[cbind(idx$SEXO, idx$FXET, idx$RACA)])
}
e22u <- do.call(rbind, lapply(seq_along(U), function(i)
  longo(U[[i]], data.frame(UNIDADE = i, DS = G$DS[i], COD_BAIRRO = G$COD_BAIRRO[i]))))
e22 <- aggregate(POP ~ DS + SEXO + FXET + RACA, e22u, sum)

# ---- 4. Estrutura 2010: IPF com margens SESAB (sexo×faixa) e raça do DS ----
r10 <- read.csv(file.path(raiz, "dados/entrada/raca_2010_ds_banco_parcial.csv"))
e10 <- list()
for (ds in 1:12) {
  M <- rbind(sesab(ds, 1), sesab(ds, 2)); N <- sum(M)
  rr <- r10$POP_BANCO2010[r10$DS == ds][order(r10$RACA[r10$DS == ds])]; rr <- rr / sum(rr) * N
  Z <- array(0, c(2, 18, 5)); sub <- e22[e22$DS == ds, ]
  Z[cbind(sub$SEXO, sub$FXET, sub$RACA)] <- sub$POP; Z <- Z + 0.01         # semente = estrutura 2022
  for (it in 1:300) {
    Z <- Z * array(M / apply(Z, c(1, 2), sum), c(2, 18, 5))
    Z <- Z * aperm(array(rr / apply(Z, 3, sum), c(5, 2, 18)), c(2, 3, 1))
  }
  e10[[ds]] <- longo(Z, data.frame(DS = ds))
}
e10 <- do.call(rbind, e10)

ord <- function(d) d[order(d$DS, d$SEXO, d$FXET, d$RACA), ]
write.csv(ord(e10), file.path(raiz, "dados/estrutura/estrutura_2010_ds.csv"), row.names = FALSE)
write.csv(ord(e22), file.path(raiz, "dados/estrutura/estrutura_2022_ds.csv"), row.names = FALSE)
write.csv(e22u[order(e22u$UNIDADE, e22u$SEXO, e22u$FXET, e22u$RACA), ],
          file.path(raiz, "dados/estrutura/estrutura_2022_bairro_ds.csv"), row.names = FALSE)
cat("Estrutura base salva. Totais 2010:", round(sum(e10$POP)), " 2022:", round(sum(e22$POP)), "\n")
