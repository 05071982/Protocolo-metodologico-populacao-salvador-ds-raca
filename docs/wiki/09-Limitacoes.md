# 9. Limitações

1. **Limites dos DS mudaram.** A tabela SESAB de 2010 usa a divisão de DS da época, e 2022 usa o shapefile de 2023. Subúrbio Ferroviário, São Caetano/Valéria e Itapagipe seguem outra divisão administrativa. Parte da variação 2010→2022 desses DS é mudança de limite, não de população.
2. **Setores inteiros num só DS.** Cada setor vai inteiro para o DS de maior área. Só 60 dos 4.542 setores têm menos de 90% da área no DS escolhido.
3. **Raça em 2010.** A distribuição de raça **por DS** vem de um banco com 78% de cobertura; o método assume que os setores perdidos têm a mesma composição racial do seu DS. O total municipal por sexo × idade × raça é o universo do IBGE (SIDRA 3175).
4. **Abertura de faixas.** O método das coortes não considera a mortalidade diferente entre as duas metades da faixa. O erro é pequeno e maior em 60–69 anos.
5. **2000–2009.** Desde a v4, 2000 fecha com o Censo 2000 (sexo × idade, raça e totais por DS) e 2001–2009 são interpolados entre 2000 e 2010. A distribuição **interna** de 2000 (DS × idade × raça e bairros) continua sendo a de 2010, ajustada às margens de 2000, porque não há setores de 2000 no projeto. A raça de 2000 vem da amostra do censo, e 0,7% sem declaração foi redistribuído. A categoria amarela de 2010 (1,4%, contra 0,3% em 2000 e 0,15% em 2022) é sabidamente atípica; leia sua tendência com cautela.
6. **2023 em diante.** A tendência 2010–2022 é prolongada; a migração intramunicipal recente não entra.
7. **Bairros fora de 2022.** Cada bairro segue a dinâmica do seu DS (a estrutura relativa de 2022 fica constante dentro do DS), porque não há base de 2010 confiável por bairro. Os totais de bairro em 2022 diferem do IBGE em no máximo ±20 pessoas por causa do arredondamento.
8. **Células pequenas.** Indígena e amarela por bairro e faixa etária são estimativas de modelo, não contagens. Evite calcular taxas com denominadores menores que cerca de 100 pessoas; prefira agregar faixas ou anos.
9. **Totais TCU com quebras.** Os totais mudam de método entre períodos (projeções de 2000, de 2010 e, depois de 2022, com correção de cobertura). Os saltos em 2007, 2010, 2022 e 2023 são artefatos. Para análise de tendência use `FREQ_CENSO`.
10. **Aquarius.** O bairro foi delimitado pela área dos setores. O setor `292740805060272` (35% da área no Aquarius) ficou na Pituba.
11. **SESAB e MS/DATASUS fora dos censos.** Nos anos censitários a base é igual à SESAB. Nos demais, a estrutura etária difere (até 10% de dissimilaridade em 2019), porque a SESAB repete a estrutura do censo anterior, e os totais diferem em 2007 e 2023. As diferenças estão publicadas em `resultados/reconciliacao_sesab_2000_2025.csv` ([página 13](13-Dialogo-entre-bases)).
12. **Idade simples por DS.** 2010 é observada; em 2000 e 2022 as idades de 20 anos ou mais vêm de Sprague (0–19 fecham com os censos).

## Próximos aprimoramentos

- Incorporar indicadores administrativos de dinâmica intramunicipal: nascidos vivos (SINASC) por bairro, óbitos (SIM), cadastros da Atenção Primária, ligações de água e energia. Isso permitiria um modelo de **razão-correlação** (Swanson & Tayman, 2012) para corrigir a tendência depois de 2022.
- Substituir 2010 pelo Censo 2030 quando sair, mantendo 2022 como âncora.
- Estimar intervalos de incerteza por bairro (*bootstrap* sobre setores).
