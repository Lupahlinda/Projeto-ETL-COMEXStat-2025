# Perguntas de Negócio - COMEX Stat 2025

Documento com 35 perguntas analíticas formuladas para orientar a construção do modelo dimensional e dos dashboards no Power BI.

---

## 1. Evolução Temporal das Exportações (5 perguntas)

1. **Qual o valor total FOB das exportações brasileiras em 2025, mês a mês?**
   - *Métrica:* Soma de VL_FOB por CO_MES
   - *Visualização:* Gráfico de linha com tendência mensal

2. **Como foi o crescimento percentual das exportações comparado ao mesmo período do ano anterior?**
   - *Métrica:* Variação percentual YoY (Year over Year)
   - *Visualização:* Gráfico de colunas com linha de variação

3. **Qual o trimestre com maior volume de exportações em 2025?**
   - *Métrica:* Soma de VL_FOB agrupado por trimestre
   - *Visualização:* Gráfico de barras por trimestre

4. **Existe sazonalidade nas exportações? Quais meses apresentam picos e vales?**
   - *Métrica:* Média de VL_FOB por mês (considerando histórico)
   - *Visualização:* Gráfico de área com média móvel

5. **Qual a evolução do peso líquido (KG) exportado ao longo do ano?**
   - *Métrica:* Soma de KG_LIQUIDO por mês
   - *Visualização:* Gráfico de linha dual (valor e peso)

---

## 2. Produtos Mais Comercializados por NCM (6 perguntas)

6. **Quais são os 10 produtos (NCM) com maior valor FOB exportado em 2025?**
   - *Métrica:* TOP 10 soma de VL_FOB por CO_NCM
   - *Visualização:* Gráfico de barras horizontais

7. **Qual a participação percentual de cada categoria de produto nas exportações totais?**
   - *Métrica:* Percentual de VL_FOB por categoria
   - *Visualização:* Gráfico de pizza ou doughnut

8. **Quais produtos apresentaram maior crescimento em valor exportado comparado ao ano anterior?**
   - *Métrica:* Variação percentual por CO_NCM
   - *Visualização:* Tabela com indicadores de tendência

9. **Qual o peso médio por produto exportado? Existe correlação entre peso e valor?**
   - *Métrica:* Média de KG_LIQUIDO e VL_FOB por NCM
   - *Visualização:* Scatter plot (correlação peso x valor)

10. **Quais produtos têm o maior valor FOB por quilo (preço unitário médio)?**
    - *Métrica:* VL_FOB / KG_LIQUIDO por CO_NCM
    - *Visualização:* Ranking com formatação condicional

11. **Como está distribuída a quantidade estatística (QT_ESTAT) por categoria de produto?**
    - *Métrica:* Soma de QT_ESTAT por categoria
    - *Visualização:* Gráfico de árvore (treemap)

---

## 3. Principais Países Parceiros do Brasil (5 perguntas)

12. **Quais são os 10 principais países de destino das exportações brasileiras?**
    - *Métrica:* TOP 10 soma de VL_FOB por CO_PAIS
    - *Visualização:* Gráfico de barras horizontais ou mapa

13. **Qual o valor médio FOB por país e como varia ao longo do ano?**
    - *Métrica:* Média de VL_FOB por país por mês
    - *Visualização:* Gráfico de linhas múltiplas

14. **Quais países apresentaram maior crescimento nas importações do Brasil em 2025?**
    - *Métrica:* Variação percentual por CO_PAIS
    - *Visualização:* Tabela com setas de tendência

15. **Existe correlação entre a distância geográfica e o valor das exportações?**
    - *Métrica:* VL_FOB por país com classificação por continente
    - *Visualização:* Mapa coroplético com filtros por continente

16. **Qual a distribuição percentual das exportações por continente?**
    - *Métrica:* Percentual de VL_FOB por região geográfica
    - *Visualização:* Gráfico de pizza ou sunburst

---

## 4. Blocos Econômicos com Maior Participação (4 perguntas)

17. **Qual o valor total exportado para cada bloco econômico (UE, Mercosul, ASEAN, etc.)?**
    - *Métrica:* Soma de VL_FOB por CO_BLOCO
    - *Visualização:* Gráfico de barras empilhadas

18. **Qual a participação percentual de cada bloco econômico nas exportações totais?**
    - *Métrica:* Percentual de VL_FOB por bloco
    - *Visualização:* Gráfico de pizza ou gauge

19. **Quais blocos econômicos apresentaram maior crescimento nas exportações brasileiras?**
    - *Métrica:* Variação percentual por bloco
    - *Visualização:* Gráfico de colunas com variação

20. **Qual a evolução mensal das exportações para o Mercosul versus outros blocos?**
    - *Métrica:* VL_FOB por mês filtrado por bloco
    - *Visualização:* Gráfico de linha comparativo

---

## 5. Estados e Municípios com Maior Movimentação (5 perguntas)

21. **Quais são os 5 estados brasileiros com maior valor FOB exportado?**
    - *Métrica:* TOP 5 soma de VL_FOB por SG_UF_NCM
    - *Visualização:* Mapa do Brasil coroplético + ranking

22. **Qual a participação percentual de cada região (Norte, Nordeste, Sul, etc.) nas exportações?**
    - *Métrica:* Percentual de VL_FOB por região
    - *Visualização:* Gráfico de pizza ou mapa com regiões

23. **Quais URFs (Unidades de Receita Federal) processaram maior volume de exportações?**
    - *Métrica:* Soma de VL_FOB por CO_URF
    - *Visualização:* Tabela com drill-down por estado

24. **Qual a relação entre o estado de origem e os principais países de destino?**
    - *Métrica:* Matriz de VL_FOB cruzando estado x país
    - *Visualização:* Matriz de calor (heatmap)

25. **Como está distribuído o peso exportado por estado brasileiro?**
    - *Métrica:* Soma de KG_LIQUIDO por SG_UF_NCM
    - *Visualização:* Mapa de bolhas ou gráfico de barras

---

## 6. Vias de Transporte Mais Utilizadas (4 perguntas)

26. **Quais são as vias de transporte mais utilizadas nas exportações?**
    - *Métrica:* Contagem e valor FOB por CO_VIA
    - *Visualização:* Gráfico de barras com valor e quantidade

27. **Qual o valor médio FOB por via de transporte (marítima, aérea, terrestre)?**
    - *Métrica:* Média de VL_FOB por CO_VIA
    - *Visualização:* Gráfico de caixa (box plot)

28. **Existe correlação entre o tipo de produto e a via de transporte utilizada?**
    - *Métrica:* Cruzamento de categoria de produto x via
    - *Visualização:* Gráfico de barras empilhadas

29. **Qual a evolução do uso de diferentes vias de transporte ao longo do ano?**
    - *Métrica:* VL_FOB por CO_VIA por mês
    - *Visualização:* Gráfico de linha múltipla

---

## 7. Comportamento da Balança Comercial (6 perguntas)

30. **Qual o valor total FOB exportado versus importado em 2025?**
    - *Métrica:* Comparação VL_FOB exportação vs importação
    - *Visualização:* Gráfico de colunas lado a lado com indicador de saldo

31. **Qual o saldo da balança comercial (exportações - importações) mês a mês?**
    - *Métrica:* Diferença entre exportações e importações
    - *Visualização:* Gráfico de colunas com linha de saldo

32. **Quais produtos (NCM) apresentam superávit na balança comercial?**
    - *Métrica:* Diferença VL_FOB (exportação - importação) por produto
    - *Visualização:* Gráfico de barras horizontais com cores (positivo/negativo)

33. **Quais países apresentam os maiores déficits e superávits comerciais com o Brasil?**
    - *Métrica:* Saldo comercial por CO_PAIS
    - *Visualização:* Ranking com formatação condicional

34. **Como está a relação entre peso exportado e importado por produto?**
    - *Métrica:* Comparação de KG_LIQUIDO exportação vs importação
    - *Visualização:* Gráfico de dispersão ou bolhas

35. **Qual a tendência da balança comercial ao longo de 2025? Está melhorando ou piorando?**
    - *Métrica:* Saldo mensal acumulado
    - *Visualização:* Gráfico de área com linha de tendência

---

## Resumo por Categoria

| Categoria | Quantidade | Status |
|-----------|------------|--------|
| Evolução Temporal | 5 | ✅ Completo |
| Produtos (NCM) | 6 | ✅ Completo |
| Países Parceiros | 5 | ✅ Completo |
| Blocos Econômicos | 4 | ✅ Completo |
| Estados e Municípios | 5 | ✅ Completo |
| Vias de Transporte | 4 | ✅ Completo |
| Balança Comercial | 6 | ✅ Completo |
| **TOTAL** | **35 perguntas** | ✅ **Dentro do intervalo 20-70** |

---

## Observações para Implementação no Power BI

### Filtros e Segmentações Recomendados:
- Período (ano, mês, trimestre)
- Produto (NCM, categoria)
- País de destino (individual ou bloco)
- Estado brasileiro (UF)
- Via de transporte

### Indicadores-Chave (KPIs):
1. **Valor Total FOB Exportado**
2. **Peso Total Exportado (KG)**
3. **Quantidade de Transações**
4. **Ticket Médio por Exportação**
5. **Saldo da Balança Comercial**
6. **Top País Destinatário**
7. **Top Produto Exportado**
8. **Crescimento Percentual (YoY)**

### Relacionamentos no Modelo:
As perguntas acima podem ser respondidas utilizando o Star Schema implementado, com joins entre:
- `fato_exportacao` → todas as dimensões
- `dim_pais` → `dim_bloco` (para análise por bloco econômico)
- `dim_urf` → `dim_municipio` (para análise municipal)

---

*Documento criado para orientar o desenvolvimento do dashboard no Power BI Desktop*
