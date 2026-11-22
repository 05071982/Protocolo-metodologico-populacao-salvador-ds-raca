# =====================================================================
# 01c_chave_bairro_prefeitura_bairro.R
# Verifica se cada bairro oficial cabe inteiro em uma Prefeitura-Bairro
# (PB) e gera a chave bairro -> PB.
# Entrada: C:/setor/Novo/delimitacao_de_bairros_oficial.shp
#          C:/setor/Novo/Pbairros/Prefeituras_Bairro.shp (10 PBs, 2018)
# Saída:   C:/setor/chave_bairro_prefeitura_bairro.csv (resultado em nov/2026: todo bairro tem
#          93% ou mais da área em uma única PB; nenhum tem mais de 3% em outra -> bairro inteiro na PB de maior área)
# =====================================================================
rm(list = ls())
library(sf); library(dplyr)

pasta2 <- "C:/setor/Novo"
arq_pb <- "C:/setor/Novo/Pbairros/Prefeituras_Bairro.shp"

bai <- st_read(file.path(pasta2, "delimitacao_de_bairros_oficial.shp"), quiet = TRUE) |>
  st_transform(31984) |> st_make_valid()
pb  <- st_read(arq_pb, quiet = TRUE) |> st_transform(31984) |> st_make_valid()
cat("Campos do shapefile de PB:", paste(names(pb), collapse = ", "), "\n")
print(st_drop_geometry(pb))   # confira se aparecem as 10 PBs

nome_b  <- names(bai)[grepl("NOME", names(bai), ignore.case = TRUE)][1]
# campo com o nome da PB: no shapefile da Prefeitura (2018) é "Subclasses"
# (20 polígonos; a PB II tem vários, pelas ilhas)
nome_pb <- if ("Subclasses" %in% names(pb)) "Subclasses" else
  names(pb)[sapply(st_drop_geometry(pb), function(v) is.character(v) && length(unique(v)) == 10)][1]
cat("Campo usado para a PB:", nome_pb, "\n")

bai$area_b <- as.numeric(st_area(bai))
x <- st_intersection(bai[, c(nome_b, "area_b")], pb[, nome_pb]) |>
  mutate(area = as.numeric(st_area(geometry))) |> st_drop_geometry()
names(x)[1:3] <- c("BAIRRO", "AREA_BAIRRO", "PREFEITURA_BAIRRO")

chave <- x |>
  group_by(BAIRRO, PREFEITURA_BAIRRO) |>
  summarise(PROP_AREA = sum(area) / first(AREA_BAIRRO), .groups = "drop") |>
  filter(PROP_AREA >= 0.001) |>
  arrange(BAIRRO, desc(PROP_AREA))

write.csv(chave, "C:/setor/chave_bairro_prefeitura_bairro.csv", row.names = FALSE, fileEncoding = "UTF-8")

# Bairros que não cabem inteiros em uma PB (menos de 99% da área na PB principal)
cruz <- chave |> group_by(BAIRRO) |> filter(max(PROP_AREA) < 0.99)
cat("Bairros:", n_distinct(chave$BAIRRO), " | PBs:", n_distinct(chave$PREFEITURA_BAIRRO),
    " | bairros divididos entre PBs:", n_distinct(cruz$BAIRRO), "\n")
print(as.data.frame(cruz))
