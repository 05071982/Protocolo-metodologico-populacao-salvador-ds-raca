# =====================================================================
# 05_idade_simples.R — População por DS × sexo × idade simples (0 a 100+)
# Rode DEPOIS de 04_atualizar_populacao.R. Os totais de cada faixa (FXET)
# batem exatamente com a base principal.
#
# Entradas:
#   resultados/populacao_salvador_ds_<ano_ini>_<ano_fim>.csv   (saída do 04)
#   dados/estrutura/proporcao_idade_simples_na_faixa.csv
#     P2010 = proporção observada da idade dentro da faixa (Censo 2010, DS × sexo)
#     P2022 = proporção estimada por Sprague a partir das faixas de 2022 (80+ = forma 2010)
# Método: p(idade | faixa, t) ∝ P2010^(1−w) · P2022^w,  w = (t − 2010)/12
#         FREQ = população da faixa × p, arredondada pelo maior resto dentro da faixa.
# =====================================================================
rm(list = ls())
raiz <- getwd()
source(file.path(raiz, "R", "funcoes.R"))

arq_ds <- list.files(file.path(raiz, "resultados"), pattern = "^populacao_salvador_ds_\\d{4}_\\d{4}\\.csv$", full.names = TRUE)
stopifnot(length(arq_ds) >= 1)
arq_ds <- sort(arq_ds, decreasing = TRUE)[1]          # o mais recente
pop_ds <- read.csv(arq_ds)
fx_tot <- aggregate(FREQ ~ ANO + DS + SEXO + FXET, pop_ds, sum)   # soma as raças

prop <- read.csv(file.path(raiz, "dados/estrutura/proporcao_idade_simples_na_faixa.csv"))
prop <- prop[order(prop$DS, prop$SEXO, prop$IDADE), ]
eps <- 1e-6

saida <- vector("list", nrow(fx_tot)); k <- 0
for (ano in sort(unique(fx_tot$ANO))) {
  w <- (ano - 2010) / 12
  for (ds in 1:12) for (sx in 1:2) {
    p <- prop[prop$DS == ds & prop$SEXO == sx, ]
    q <- exp((1 - w) * log(p$P2010 + eps) + w * log(p$P2022 + eps))
    tt <- fx_tot[fx_tot$ANO == ano & fx_tot$DS == ds & fx_tot$SEXO == sx, ]
    freq <- integer(nrow(p))
    for (f in 1:18) {
      m <- which(p$FXET == f)
      total_f <- tt$FREQ[tt$FXET == f]
      freq[m] <- arred_maior_resto(q[m] / sum(q[m]) * total_f, total_f)
    }
    k <- k + 1
    saida[[k]] <- data.frame(ANO = ano, DS = ds, SEXO = sx, IDADE = p$IDADE, FXET = p$FXET, FREQ = freq)
  }
}
pop_idade <- do.call(rbind, saida[seq_len(k)])

# Conferência: soma por faixa = base principal
chk <- merge(aggregate(FREQ ~ ANO + DS + SEXO + FXET, pop_idade, sum), fx_tot,
             by = c("ANO", "DS", "SEXO", "FXET"))
stopifnot(all(chk$FREQ.x == chk$FREQ.y), all(pop_idade$FREQ >= 0))

arq <- sub("populacao_salvador_ds_", "populacao_salvador_ds_sexo_idade_", arq_ds)
write.csv(pop_idade, arq, row.names = FALSE, fileEncoding = "UTF-8")
cat("Arquivo gerado:", arq, " | linhas:", nrow(pop_idade), "\n")
