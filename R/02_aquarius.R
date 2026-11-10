# =====================================================================
# 02_aquarius.R — Bairro 171 (Aquarius, Lei Municipal 9.778/2024)
# Identifica os setores censitários 2022 rotulados "Pituba" pelo IBGE
# que estão dentro do polígono oficial do Aquarius.
# Regra adotada: setor com > 50% da área no Aquarius => bairro 171.
# Resultado (nov/2026): 7 setores; o setor 292740805060272 (35%) ficou na Pituba.
# =====================================================================
rm(list = ls())

pkgs <- c("sf", "dplyr")
novos <- pkgs[!pkgs %in% rownames(installed.packages())]
if (length(novos) > 0) install.packages(novos)
library(sf); library(dplyr)

pasta <- "C:/Users/SEU_USUARIO/Documents/pop_ds"   # <-- ajuste

setores <- st_read(file.path(pasta, "BA_setores_CD2022.shp"), quiet = TRUE) |>
  filter(CD_MUN == "2927408", NM_BAIRRO == "Pituba") |>
  st_transform(31984) |> st_make_valid()

aq <- st_read(file.path(pasta, "delimitacao_de_bairros_oficial.shp"), quiet = TRUE) |>
  filter(NOME_BAIRR == "Aquarius") |>
  st_transform(31984) |> st_make_valid()

setores$area <- as.numeric(st_area(setores))
ov <- st_intersection(setores[, c("CD_SETOR", "area")], aq) |>
  mutate(a = as.numeric(st_area(geometry))) |> st_drop_geometry()

setores$prop_aq <- 0
setores$prop_aq[match(ov$CD_SETOR, setores$CD_SETOR)] <- pmin(ov$a / ov$area, 1)

write.csv(st_drop_geometry(setores)[, c("CD_SETOR", "prop_aq")],
          file.path(pasta, "setores_pituba_aquarius.csv"), row.names = FALSE)

print(table(cut(setores$prop_aq, c(-0.01, 0.1, 0.5, 0.9, 1))))
print(setores$CD_SETOR[setores$prop_aq > 0.5])
