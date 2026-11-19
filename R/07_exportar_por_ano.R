# =====================================================================
# 07_exportar_por_ano.R — um CSV por ano (idade detalhada) + dicionário, num único zip
# Rode DEPOIS de 06_bairro_idade_raca.R.
# Por quê: com a idade detalhada a série passa de 1.048.576 linhas (limite do Excel);
# cada ano tem ~115 mil linhas e abre no Excel.
# Saída: resultados/populacao_bairro_idade_raca_por_ano.zip com
#   pop_bairro_idade_raca_AAAA.csv (ANO;DS;NOME_DS;COD_BAIRRO;NOME_BAIRRO;IDADE;FXET;SEXO;RACA;FREQ)
#   dicionario_bairros.csv, dicionario_ds.csv, dicionario_fxet.csv, dicionario_sexo.csv, dicionario_raca.csv
#   (e DICIONARIO.xlsx, se o pacote openxlsx estiver instalado)
# Bairros sem população residente (ex.: 2 – Aeroporto) entram com 1 linha por ano e FREQ = 0.
# =====================================================================
rm(list = ls())
raiz <- getwd()
ult <- function(p) sort(list.files(file.path(raiz, "resultados"), pattern = p, full.names = TRUE), decreasing = TRUE)[1]
res <- read.csv(ult("^populacao_salvador_bairro_ds_idade_raca_\\d{4}_\\d{4}\\.csv$"))
dd  <- function(a) read.csv(file.path(raiz, "dados/dicionarios", a), check.names = FALSE)
bai <- dd("bairros.csv"); dsn <- dd("ds.csv"); fx <- dd("fxet.csv"); sx <- dd("sexo.csv"); rc <- dd("raca.csv")
stopifnot(nrow(bai) == 171, setequal(bai$COD_BAIRRO, 1:171))

sem <- bai[!bai$COD_BAIRRO %in% res$COD_BAIRRO, ]
if (nrow(sem) > 0) {
  z <- expand.grid(ANO = sort(unique(res$ANO)), k = seq_len(nrow(sem)))
  z <- data.frame(ANO = z$ANO, DS = sem$DS_PRINCIPAL[z$k], COD_BAIRRO = sem$COD_BAIRRO[z$k],
                  IDADE = 0L, FXET = 1L, SEXO = 1L, RACA = 1L, FREQ = 0L)
  res <- rbind(res[, names(z)], z)
}
res$NOME_DS <- dsn$NOME_DS[match(res$DS, dsn$DS)]
res$NOME_BAIRRO <- bai$BAIRRO[match(res$COD_BAIRRO, bai$COD_BAIRRO)]
stopifnot(!anyNA(res$NOME_DS), !anyNA(res$NOME_BAIRRO))
cols <- c("ANO", "DS", "NOME_DS", "COD_BAIRRO", "NOME_BAIRRO", "IDADE", "FXET", "SEXO", "RACA", "FREQ")

tmp <- file.path(tempdir(), "pop_por_ano"); unlink(tmp, recursive = TRUE); dir.create(tmp)
totais <- read.csv(file.path(raiz, "dados/entrada/totais_municipais.csv"))
for (a in sort(unique(res$ANO))) {
  d <- res[res$ANO == a, cols]
  d <- d[order(d$DS, d$COD_BAIRRO, d$IDADE, d$SEXO, d$RACA), ]
  stopifnot(sum(d$FREQ) == round(totais$TOTAL[totais$ANO == a]), setequal(d$COD_BAIRRO, 1:171))
  write.table(d, file.path(tmp, sprintf("pop_bairro_idade_raca_%d.csv", a)), sep = ";",
              row.names = FALSE, quote = FALSE, fileEncoding = "UTF-8")
}
write.table(bai, file.path(tmp, "dicionario_bairros.csv"), sep = ";", row.names = FALSE, fileEncoding = "UTF-8", na = "")
for (nm in c("ds", "fxet", "sexo", "raca"))
  write.table(dd(paste0(nm, ".csv")), file.path(tmp, paste0("dicionario_", nm, ".csv")), sep = ";", row.names = FALSE, quote = FALSE, fileEncoding = "UTF-8")
if (requireNamespace("openxlsx", quietly = TRUE)) {
  idade <- data.frame(IDADE = 0:100, FXET = c(1, rep(2, 4), 3 + (5:79 - 5) %/% 5, rep(18, 21)))
  openxlsx::write.xlsx(list(BAIRRO = bai, DS = dsn, FXET = fx, IDADE = idade, SEXO = sx, RACA = rc),
                       file.path(tmp, "DICIONARIO.xlsx"))
}
arq <- file.path(raiz, "resultados", "populacao_bairro_idade_raca_por_ano.zip")
unlink(arq)
if (requireNamespace("zip", quietly = TRUE)) {
  zip::zipr(arq, list.files(tmp, full.names = TRUE))
} else {
  old <- setwd(tmp); utils::zip(arq, list.files(tmp)); setwd(old)   # no Windows requer Rtools; prefira install.packages("zip")
}
cat("Arquivo gerado:", arq, "\n")
