# =====================================================================
# 01b_chave_setor2010.R — interseção dos setores censitários de 2010 com as
# unidades bairro × DS atuais (malha oficial de bairros + DS). Versão 5.
# Gera chave_setor2010_bairro_ds.csv com TODAS as interseções e a fração de área.
# A escolha final (python/v5_harmoniza_chave.py) usa a unidade da chave 2022 para
# setores com o mesmo código (se o polígono de 2010 tiver >= 25% da área nela) e,
# nos demais, a unidade de maior área. Resultado: dados/entrada/chave_setor_bairro_ds_2010.csv
# Entradas: malha de setores 2010 do IBGE recortada para Salvador (CD_GEOCODM 2927408),
#           DISTRITO_SANITARIO.shp e delimitacao_de_bairros_oficial.shp
# =====================================================================
rm(list = ls())
library(sf); library(dplyr)
sf_use_s2(FALSE)
pasta  <- "C:/setor"          # malha 2010 (setores2010_salvador.shp)
pasta2 <- "C:/setor/Novo"     # bairros e DS
set10 <- st_read(file.path(pasta, "setores2010_salvador.shp"), quiet = TRUE) |>
  st_transform(31984) |> st_make_valid() |> select(CD_SETOR = CD_GEOCODI)
ds <- st_read(file.path(pasta2, "DISTRITO_SANITARIO.shp"), quiet = TRUE) |>
  st_transform(31984) |> st_make_valid() |> group_by(NOME_DIST) |> summarise(.groups = "drop")
bai <- st_read(file.path(pasta2, "delimitacao_de_bairros_oficial.shp"), quiet = TRUE) |>
  st_transform(31984) |> st_make_valid()
uni <- st_intersection(bai, ds)
set10$area_setor <- as.numeric(st_area(set10))
inter <- st_intersection(set10, uni) |>
  mutate(area_int = as.numeric(st_area(geometry))) |>
  st_drop_geometry() |>
  group_by(CD_SETOR) |> mutate(prop_area = area_int / sum(area_int)) |> ungroup() |>
  filter(prop_area >= 0.001)
write.csv(inter, file.path(pasta, "chave_setor2010_bairro_ds.csv"), row.names = FALSE, fileEncoding = "UTF-8")
cat("Setores 2010 com chave:", n_distinct(inter$CD_SETOR), "de", nrow(set10), "\n")
