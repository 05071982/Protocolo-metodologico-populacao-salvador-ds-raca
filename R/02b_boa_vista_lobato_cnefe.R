# =====================================================================
# 02b_boa_vista_lobato_cnefe.R — Bairro 172 (Boa Vista do Lobato,
# Lei Municipal 9.919/2025, de 18/12/2025)
#
# A lei define o bairro por uma lista de logradouros e ainda não há
# polígono oficial. Este script usa o CNEFE 2022 do IBGE (endereços
# com setor censitário e coordenadas) para listar os endereços do
# Lobato e de seu entorno, por logradouro, com o setor 2022, o setor
# 2010 (pelas coordenadas) e o DS.
#
# Entrada: CSV do CNEFE 2022 de Salvador (IBGE, Arquivos_CNEFE,
# município 2927408), malha 2010 e polígonos oficiais em C:/setor.
# Saída:   C:/setor/cnefe_lobato_logradouros.csv (pequeno; colocar no
#          Drive). A seleção dos logradouros da lei é feita depois.
# =====================================================================
rm(list = ls())

pkgs <- c("sf", "dplyr", "data.table")
novos <- pkgs[!pkgs %in% rownames(installed.packages())]
if (length(novos) > 0) install.packages(novos)
library(sf); library(dplyr); library(data.table)

pasta  <- "C:/setor"
pasta2 <- "C:/setor/Novo"
arq_cnefe <- "C:/setor/2927408_SALVADOR.csv"            # CNEFE 2022 (225 MB)

# ---- 1. CNEFE 2022 ---------------------------------------------------
cn <- fread(arq_cnefe, sep = ";", encoding = "UTF-8", colClasses = "character")
if (!any(grepl("SEGLOGR", names(cn)))) stop("Colunas do CNEFE não reconhecidas: ", paste(names(cn), collapse = ", "))
if (any(grepl("\u00c3", head(cn[[grep("^NOM_SEGLOGR", names(cn))[1]]], 5000))))   # acentos quebrados
  cn <- fread(arq_cnefe, sep = ";", encoding = "Latin-1", colClasses = "character")
nm <- names(cn)
col <- function(p) nm[grepl(p, nm, ignore.case = TRUE)][1]
cn <- data.table(
  CD_SETOR_2022 = substr(cn[[col("^COD_SETOR")]], 1, 15),
  TIPO    = cn[[col("TIPO_SEGLOGR")]],
  TITULO  = cn[[col("TITULO_SEGLOGR")]],
  NOME    = cn[[col("^NOM_SEGLOGR")]],
  LOCALID = cn[[col("LOCALIDADE")]],
  ESPECIE = cn[[col("^COD_ESPECIE")]],
  LAT = as.numeric(gsub(",", ".", cn[[col("^LATITUDE")]])),
  LON = as.numeric(gsub(",", ".", cn[[col("^LONGITUDE")]]))
)
cn <- cn[!is.na(LAT) & !is.na(LON)]
pts <- st_as_sf(cn, coords = c("LON", "LAT"), crs = 4674, remove = FALSE) |>
  st_transform(31984)

# ---- 2. Recorte: Lobato oficial + 300 m (pega ruas de divisa) --------
bai <- st_read(file.path(pasta2, "delimitacao_de_bairros_oficial.shp"), quiet = TRUE) |>
  st_transform(31984) |> st_make_valid()
campo_nome <- names(bai)[grepl("NOME", names(bai), ignore.case = TRUE)][1]
lob <- bai[bai[[campo_nome]] == "Lobato", ]
pts <- pts[st_intersects(pts, st_buffer(st_union(lob), 300), sparse = FALSE)[, 1], ]

# bairro oficial atual de cada endereço
pts$BAIRRO_OFICIAL <- bai[[campo_nome]][st_nearest_feature(pts, bai)]
pts$BAIRRO_OFICIAL[!st_intersects(pts, st_union(bai), sparse = FALSE)[, 1]] <- NA

# ---- 3. Setor 2010 e DS pelas coordenadas ----------------------------
set10 <- st_read(file.path(pasta, "setores2010_salvador.shp"), quiet = TRUE) |>
  st_transform(31984) |> st_make_valid()
campo10 <- names(set10)[grepl("^CD_GEOCOD|^CD_SETOR", names(set10))][1]
i10 <- st_intersects(pts, set10)
pts$CD_SETOR_2010 <- vapply(i10, function(i) if (length(i)) set10[[campo10]][i[1]] else NA_character_, "")

ds <- st_read(file.path(pasta2, "DISTRITO_SANITARIO.shp"), quiet = TRUE) |>
  st_transform(31984) |> st_make_valid()
campo_ds <- names(ds)[grepl("NOME|DS|DIST", names(ds), ignore.case = TRUE)][1]
ids <- st_intersects(pts, ds)
pts$DS <- vapply(ids, function(i) if (length(i)) as.character(ds[[campo_ds]][i[1]]) else NA_character_, "")

# ---- 4. Agrega por setor × logradouro --------------------------------
out <- st_drop_geometry(pts) |>
  group_by(CD_SETOR_2022, CD_SETOR_2010, DS, BAIRRO_OFICIAL, TIPO, TITULO, NOME, LOCALID) |>
  summarise(N_END = n(),
            N_DOM = sum(ESPECIE == "1"),          # domicílio particular
            LAT = round(mean(LAT), 6), LON = round(mean(LON), 6),
            .groups = "drop") |>
  arrange(NOME, CD_SETOR_2022)

write.csv(out, file.path(pasta, "cnefe_lobato_logradouros.csv"),
          row.names = FALSE, fileEncoding = "UTF-8")
cat("Linhas:", nrow(out), " Endereços:", sum(out$N_END), " Domicílios:", sum(out$N_DOM), "\n")
print(table(out$BAIRRO_OFICIAL, useNA = "ifany"))
