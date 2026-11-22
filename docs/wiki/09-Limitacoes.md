# 9. Limitações

1. **Limites.** Desde a v5, 2010 e 2022 estão nos limites atuais de bairro e DS. A tabela SESAB de 2010, nos limites da época, difere da base em até 0,8% por DS; quem comparar com números antigos do TabNet verá essa diferença.
2. **Setores inteiros numa só unidade.** Cada setor vai inteiro para uma unidade bairro × DS. Em 2022, 60 dos 4.542 setores têm menos de 90% da área no DS escolhido. Em 2010, a escolha usa o código da chave 2022 (2.874 setores) ou a maior área (669); setores divididos entre bairros geram imprecisão em bairros pequenos, como Centro Administrativo da Bahia (1.828 em 2010; 173 em 2022) e Mares.
3. **Raça em 2010.** Vem do universo, setor a setor (Pessoa03 e Pessoa05). Dentro dos grupos 60–69 e 70 ou mais, a raça de cada faixa quinquenal segue a do grupo no setor, ajustada ao universo municipal por sexo, idade e raça. Bairros de 2022 seguem a codificação de bairros do IBGE; em 2010, 96% da população cai no mesmo bairro pelo código e pelo polígono oficial.
4. **Abertura de faixas.** O método das coortes não considera a mortalidade diferente entre as duas metades da faixa. O erro é pequeno e maior em 60–69 anos.
5. **2000–2009.** Desde a v4, 2000 fecha com o Censo 2000 (sexo × idade, raça e totais por DS) e 2001–2009 são interpolados entre 2000 e 2010. A distribuição **interna** de 2000 (bairro × idade × raça) é a de 2010, ajustada às margens de 2000, porque não há setores de 2000 no projeto. A raça de 2000 vem da amostra do censo, e 0,7% sem declaração foi redistribuído. A categoria amarela de 2010 (1,4%, contra 0,3% em 2000 e 0,15% em 2022) é sabidamente atípica; leia sua tendência com cautela.
6. **2023 em diante.** A tendência 2010–2022 é prolongada no nível do DS, e os bairros mantêm a proporção de 2022 dentro do DS; a migração intramunicipal recente não entra.
7. **Bairros entre os censos.** Desde a v5, cada bairro tem estrutura observada em 2010 e 2022 e segue a própria trajetória. Bairros de expansão recente (Jardim das Margaridas, Patamares, Areia Branca) cresceram mais de 200% entre 2010 e 2022; após 2022 esse crescimento não é extrapolado. Em 2010 os bairros somam exatamente os setores, e em 2022 batem com o IBGE.
8. **Células pequenas.** Indígena e amarela por bairro e faixa etária são estimativas de modelo, não contagens. Evite calcular taxas com denominadores menores que cerca de 100 pessoas; prefira agregar faixas ou anos.
9. **Totais TCU com quebras.** Os totais mudam de método entre períodos (projeções de 2000, de 2010 e, depois de 2022, com correção de cobertura). Os saltos em 2007, 2010, 2022 e 2023 são artefatos. Para análise de tendência use `FREQ_CENSO`.
10. **Aquarius.** O bairro foi delimitado pela área dos setores. O setor `292740805060272` (35% da área no Aquarius) ficou na Pituba.
11. **SESAB e MS/DATASUS fora dos censos.** Nos anos censitários a base é igual à SESAB. Nos demais, a estrutura etária difere (até 10% de dissimilaridade em 2019), porque a SESAB repete a estrutura do censo anterior, e os totais diferem em 2007 e 2023. As diferenças estão publicadas em `resultados/reconciliacao_sesab_2000_2025.csv` ([página 13](13-Dialogo-entre-bases)).
12. **Idade simples por DS.** 2010 é observada nos setores (Pessoa11 e Pessoa12); em 2000 e 2022 as idades de 20 anos ou mais vêm de Sprague (0–19 fecham com os censos).

## Próximos aprimoramentos

- Incorporar indicadores administrativos de dinâmica intramunicipal: nascidos vivos (SINASC) por bairro, óbitos (SIM), cadastros da Atenção Primária, ligações de água e energia. Isso permitiria um modelo de **razão-correlação** (Swanson & Tayman, 2012) para corrigir a tendência depois de 2022.
- Substituir 2010 pelo Censo 2030 quando sair, mantendo 2022 como âncora.
- Estimar intervalos de incerteza por bairro (*bootstrap* sobre setores).
