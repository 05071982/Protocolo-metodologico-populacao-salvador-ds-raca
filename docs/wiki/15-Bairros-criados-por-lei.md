# 15. Bairros criados por lei depois do Censo 2022

Salvador tinha 170 bairros na delimitação usada pelo IBGE no Censo 2022. Duas leis municipais criaram bairros depois disso:

| Código | Bairro | Lei | Desmembrado de | DS | Pop. 2010 (área atual) | Pop. 2022 |
|---|---|---|---|---|---|---|
| 171 | Aquarius | 9.778/2024 (DOM 26/01/2024) | Pituba (130) | 6 – Barra/Rio Vermelho | 3.248 | 4.839 |
| 172 | Boa Vista do Lobato | 9.919/2025 (18/12/2025) | Lobato (96), Alto do Cabrito (5), Boa Vista de São Caetano (20) | 11 – Subúrbio Ferroviário | 6.747 | 6.219 |

## 15.1 Decisão: bairros transversais aos anos

Os bairros novos aparecem **em toda a série (2000–2026), nos limites atuais**, e não só a partir do ano da lei. O valor de 2010 é a população que morava, em 2010, na área que hoje forma o bairro.

Motivos:

- **Coerência.** Os DS também estão nos limites atuais em toda a série.
- **Indicadores.** SIM, SINASC e SINAN são geocodificados pelo bairro atual. Se o denominador mudasse de limite no ano da lei, as taxas teriam uma quebra artificial nesse ano.
- **Reagregação.** As colunas `LEI_CRIACAO` e `BAIRRO_ORIGEM` do dicionário (`dados/dicionarios/bairros.csv`) permitem somar os bairros novos de volta aos bairros de origem. Assim a base fica comparável com os 170 bairros do IBGE 2022.

## 15.2 Aquarius (polígono oficial)

A Prefeitura publicou o polígono. Os setores da Pituba com mais de 50% da área dentro do polígono formam o bairro: 7 setores (`R/02_aquarius.R`).

## 15.3 Boa Vista do Lobato (lista de logradouros)

A Lei 9.919/2025 define o perímetro por **34 logradouros** e não traz mapa. O polígono oficial ainda não foi publicado, então o bairro foi delimitado assim:

1. **Endereços.** O CNEFE 2022 do IBGE traz cada endereço com logradouro, setor censitário de 2022 e coordenadas. `R/02b_boa_vista_lobato_cnefe.R` extrai os endereços do Lobato e de 300 m ao redor (34.495 endereços).
2. **Correspondência dos nomes.** Cada logradouro da lei foi ligado ao nome registrado no CNEFE, com cuidado para "1ª Travessa", abreviações e acentos.
   - 33 dos 34 foram encontrados.
   - A Rua Aristóteles Boaventura não consta do CNEFE com esse nome.
   - A "Travessa Oswaldo Martins de Castro" aparece no CNEFE como Rua.
   - A "1ª" e a "2ª Travessa Itaquaraci" aparecem juntas, como Travessa Itaquaraci.
3. **Recorte espacial.** Algumas ruas têm o mesmo nome em outros pontos da cidade ou atravessam vários bairros, como a Av. Afrânio Peixoto (Suburbana) e a Rua São Luís. Delas, só entraram os endereços a menos de 500 m do núcleo formado pelas ruas exclusivas da lei. A Av. Pedro Veríssimo tem 1 endereço, a 1,1 km, e ficou de fora.
4. **Fração por setor.** Para cada setor, a fração é o número de domicílios nos logradouros da lei dividido pelo total de domicílios do setor no CNEFE. Cada setor contribui para o bairro 172 com essa fração da sua população, por sexo e idade. Isso vale para os setores de 2022 e para os de 2010; os de 2010 foram localizados pelas coordenadas dos mesmos endereços.
5. **Calibração.** O DS 11 e o município não mudam nos anos de censo. Em 2022, a soma dos bairros de origem com a parte transferida reproduz exatamente o IBGE.

Resultado: **2.888 domicílios, todos no DS 11.** As frações por setor estão em `dados/entrada/boa_vista_lobato_fracao_setores.csv` e na aba BOA_VISTA_LOBATO da planilha.

| Bairro de origem | IBGE 2022 | Transferido para 172 | Base v5.1 2022 |
|---|---|---|---|
| Lobato (96) | 25.946 | 5.519 | 20.427 |
| Alto do Cabrito (5) | 15.654 | 501 | 15.153 |
| Boa Vista de São Caetano (20) | 13.496 | 199 | 13.297 |
| **Boa Vista do Lobato (172)** | — | — | **6.219** |

**Por que a regra proporcional, e não "setor inteiro se mais de 50%":** a regra do Aquarius daria 7.366 pessoas em 2022, contra 6.219 da proporcional. A diferença vem de setores no limiar: um setor com 50,8% dos domicílios nas ruas da lei entraria inteiro, e um com 49% ficaria todo de fora. A regra proporcional evita esse salto.

**Por que entram partes do Alto do Cabrito e da Boa Vista de São Caetano:** algumas ruas da lei, como a Ana Piedade e a Ramalho Santos, estão hoje no polígono desses bairros. A lei é a norma mais recente e define o bairro pelas ruas, então essas partes foram incluídas.

**Perfil (2022):** 93,2% negra (39,4% preta), 14,3% com 60 anos ou mais e 17,9% com menos de 15 anos.

**Revisão prevista:** quando a Prefeitura publicar o polígono oficial, refazer com `02_aquarius.R`, trocando o polígono, e conferir com esta delimitação.

## 15.4 Efeito sobre o restante da base

- **Anos de censo (2000, 2010 e 2022) e 2023–2026:** os DS e os demais bairros ficam idênticos à v5.
- **Anos entre censos (2001–2009 e 2011–2021):** a série é interpolada no nível da unidade bairro × DS. Ao acrescentar uma unidade, a normalização e o arredondamento mudam levemente as outras: até 3 pessoas por célula e até 56 pessoas por DS e ano (0,02%).

## 15.5 Próximos bairros

- **Lei com polígono:** usar `02_aquarius.R`.
- **Lei com lista de logradouros:** usar `02b_boa_vista_lobato_cnefe.R` com a lista da nova lei e o mesmo procedimento desta página.

Nos dois casos, o código seguinte vai para o dicionário e a série é regerada com `04` a `07`.
