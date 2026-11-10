# =====================================================================
# Chave setor censitário 2022 -> bairro -> Distrito Sanitário (Salvador)
# Gera dados/entrada/chave_setor_bairro_ds_2022.csv (4.542 setores).
# Regra: cada setor recebe o DS de MAIOR área de interseção.
# Rodar na máquina onde estão os shapefiles (pasta "Pop DS - Censo 2022").
# =====================================================================
rm(list = ls())
pkgs <- c("sf", "dplyr")
novos <- pkgs[!pkgs %in% rownames(installed.packages())]
if (length(novos) > 0) install.packages(novos)
library(sf)
library(dplyr)

pasta <- "C:/Users/SEU_USUARIO/Desktop/Pop_DS"   # <-- ajuste o caminho

setores <- st_read(file.path(pasta, "BA_setores_CD2022.shp"), quiet = TRUE) |>
  filter(CD_MUN == "2927408") |>                  # Salvador
  st_transform(31984)                             # SIRGAS 2000 / UTM 24S

ds <- st_read(file.path(pasta, "DISTRITO_SANITARIO.shp"), quiet = TRUE) |>
  st_transform(31984) |>
  group_by(NOME_DIST) |> summarise(.groups = "drop")   # une as partes do Subúrbio

setores <- st_make_valid(setores); ds <- st_make_valid(ds)
setores$area_setor <- as.numeric(st_area(setores))

# Interseção e escolha do DS com MAIOR área de sobreposição (1 DS por setor)
inter <- st_intersection(setores[, c("CD_SETOR", "area_setor")], ds) |>
  mutate(area_int = as.numeric(st_area(geometry))) |>
  st_drop_geometry() |>
  group_by(CD_SETOR) |>
  mutate(prop_area = area_int / sum(area_int)) |>
  slice_max(area_int, n = 1, with_ties = FALSE) |>
  ungroup() |>
  select(CD_SETOR, NOME_DIST, prop_area)

# Setores que não tocam nenhum polígono de DS: DS mais próximo
sem_ds <- setdiff(setores$CD_SETOR, inter$CD_SETOR)
if (length(sem_ds) > 0) {
  s2 <- setores[setores$CD_SETOR %in% sem_ds, ]
  near <- st_nearest_feature(st_point_on_surface(s2), ds)
  inter <- bind_rows(inter, data.frame(CD_SETOR = s2$CD_SETOR,
                                       NOME_DIST = ds$NOME_DIST[near], prop_area = NA))
}

chave <- setores |>
  st_drop_geometry() |>
  select(CD_SETOR, CD_BAIRRO, NM_BAIRRO, AREA_KM2) |>
  left_join(inter, by = "CD_SETOR")

write.csv(chave, file.path(pasta, "chave_setor_bairro_DS_2022.csv"),
          row.names = FALSE, fileEncoding = "UTF-8")
cat("Setores:", nrow(chave), " | sem DS:", sum(is.na(chave$NOME_DIST)),
    " | setores com <90% da área no DS escolhido:", sum(chave$prop_area < 0.9, na.rm = TRUE), "\n")
# Suba o CSV gerado na pasta "População por DS" do Drive.
