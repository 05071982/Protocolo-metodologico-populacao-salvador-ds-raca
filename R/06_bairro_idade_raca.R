# =====================================================================
# 06_bairro_idade_raca.R — ANO | DS | COD_BAIRRO | IDADE | FXET | SEXO | RACA | FREQ
# Rode DEPOIS de 04 e 05. Cada célula bairro×DS×faixa×sexo×raça (saída do 04)
# é repartida entre as idades da faixa na proporção da tabela DS×sexo×idade
# (saída do 05). Arredondamento controlado com DUAS margens:
#   - soma das idades           = célula da base principal (bairro, raça, faixa)
#   - soma dos bairros e raças  = tabela DS × sexo × idade
# Saída: só linhas com FREQ > 0 (≈3,1 milhões em 2000–2026). Excede o limite
# do Excel; use CSV no TabNet / BI.
# =====================================================================
rm(list = ls())
raiz <- getwd()
ult <- function(p) sort(list.files(file.path(raiz, "resultados"), pattern = p, full.names = TRUE), decreasing = TRUE)[1]
pb <- read.csv(ult("^populacao_salvador_bairro_ds_\\d{4}_\\d{4}\\.csv$"))
pi <- read.csv(ult("^populacao_salvador_ds_sexo_idade_\\d{4}_\\d{4}\\.csv$"))

pb <- pb[order(pb$ANO, pb$DS, pb$SEXO, pb$FXET, pb$COD_BAIRRO, pb$RACA), ]
pi <- pi[order(pi$ANO, pi$DS, pi$SEXO, pi$FXET, pi$IDADE), ]
kb <- split(seq_len(nrow(pb)), list(pb$ANO, pb$DS, pb$SEXO, pb$FXET), drop = TRUE)
ki <- split(seq_len(nrow(pi)), list(pi$ANO, pi$DS, pi$SEXO, pi$FXET), drop = TRUE)

saida <- vector("list", length(kb)); z <- 0
for (g in names(kb)) {
  ib <- kb[[g]]; ia <- ki[[g]]
  B <- pb$FREQ[ib]; A <- pi$FREQ[ia]; n <- length(B); m <- length(A)
  stopifnot(sum(A) == sum(B))
  if (m == 1) {
    X <- matrix(B, n, 1)
  } else {
    X <- if (sum(A) > 0) outer(B, A / sum(A)) else matrix(0, n, m)
    Xi <- floor(X); r <- B - rowSums(Xi); cc <- A - colSums(Xi)
    if (sum(r) > 0) {
      fr <- as.vector(t(X - Xi))                         # ordem linha a linha (igual ao Python)
      ordem <- order(-fr, seq_along(fr))
      for (k in ordem) {
        i <- (k - 1) %/% m + 1; j <- (k - 1) %% m + 1
        if (r[i] > 0 && cc[j] > 0) { Xi[i, j] <- Xi[i, j] + 1; r[i] <- r[i] - 1; cc[j] <- cc[j] - 1 }
      }
      for (i in which(r > 0)) for (j in which(cc > 0)) {    # garantia (raramente usado)
        d <- min(r[i], cc[j]); Xi[i, j] <- Xi[i, j] + d; r[i] <- r[i] - d; cc[j] <- cc[j] - d
      }
    }
    X <- Xi
  }
  z <- z + 1
  saida[[z]] <- data.frame(ANO = pb$ANO[ib][1], DS = pb$DS[ib][1],
                           COD_BAIRRO = rep(pb$COD_BAIRRO[ib], each = m),
                           IDADE = rep(pi$IDADE[ia], times = n), FXET = pb$FXET[ib][1],
                           SEXO = pb$SEXO[ib][1], RACA = rep(pb$RACA[ib], each = m),
                           FREQ = as.integer(as.vector(t(X))))
}
res <- do.call(rbind, saida)
stopifnot(all(res$FREQ >= 0))
res <- res[res$FREQ > 0, ]
arq <- file.path(raiz, "resultados", sprintf("populacao_salvador_bairro_ds_idade_raca_%d_%d.csv", min(res$ANO), max(res$ANO)))
write.csv(res, arq, row.names = FALSE, fileEncoding = "UTF-8")
cat("Arquivo gerado:", arq, " | linhas:", nrow(res), "\n")
