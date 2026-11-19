# =====================================================================
# Funções auxiliares — Protocolo de estimativa populacional de Salvador
# =====================================================================

# ---------------------------------------------------------------------
# Arredondamento controlado pelo maior resto (Hamilton)
# x     : vetor numérico (valores fracionários >= 0)
# total : inteiro que a soma do resultado deve atingir
# Desempate: menor índice primeiro (ordem estável), igual à implementação
# de referência em Python (numpy argsort kind = "stable").
# ---------------------------------------------------------------------
arred_maior_resto <- function(x, total) {
  fl  <- floor(x)
  rem <- as.integer(round(total - sum(fl)))
  if (rem > 0) {
    ordem <- order(-(x - fl), seq_along(x))   # estável
    idx <- ordem[seq_len(rem)]
    fl[idx] <- fl[idx] + 1
  }
  as.integer(fl)
}

# ---------------------------------------------------------------------
# Ajuste proporcional iterativo (IPF / raking — Deming & Stephan, 1940)
# para matriz 2D com margens de linha e coluna.
# ---------------------------------------------------------------------
ipf_2d <- function(semente, margem_linha, margem_coluna, iter = 300) {
  X <- semente
  for (i in seq_len(iter)) {
    rs <- rowSums(X); X <- X * ifelse(rs > 0, margem_linha / rs, 0)
    cs <- colSums(X); X <- sweep(X, 2, ifelse(cs > 0, margem_coluna / cs, 0), `*`)
  }
  X
}

# ---------------------------------------------------------------------
# Composição no ano t pela Razão Censitária com razões variáveis (v4)
#   2000 a 2009 : s(t) ∝ s2000^(1-w) * s2010^w ,  w = (t - 2000)/10   (interpolação entre censos)
#   2010 em diante: s(t) ∝ s2010^(1-w) * s2022^w ,  w = (t - 2010)/12  (w > 1 após 2022 = extrapolação)
# s00, s10, s22 : vetores de participação (mesma ordem de células)
# ---------------------------------------------------------------------
composicao_ano <- function(s00, s10, s22, ano) {
  if (ano < 2010) {
    w <- (ano - 2000) / 10
    s <- exp((1 - w) * log(s00) + w * log(s10))
  } else {
    w <- (ano - 2010) / 12
    s <- exp((1 - w) * log(s10) + w * log(s22))
  }
  s / sum(s)
}
