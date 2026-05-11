# Dashboard Power BI - COMEX Stat 2025

Especificação técnica e guia de desenvolvimento do dashboard no Power BI Desktop para análise das exportações brasileiras.

---

## Visão Geral

O dashboard será composto por **5 páginas analíticas** interconectadas, respondendo às 35 perguntas de negócio documentadas em `Perguntas-de-Negocio.md`.

---

## Estrutura do Dashboard

### Página 1: Visão Geral (Executive Summary)

**Objetivo:** Apresentar os principais indicadores e métricas de alto nível.

**KPIs (Cards):**
- 💰 Valor Total FOB Exportado (2025)
- ⚖️ Peso Total Exportado (KG)
- 📊 Quantidade Total de Transações
- 🏆 Top Produto Exportado (nome + valor)
- 🌍 Top País Destinatário (nome + valor)
- 📈 Crescimento YoY (%)

**Gráficos:**
1. **Evolução Mensal** - Gráfico de linha (VL_FOB por mês)
2. **Top 5 Produtos** - Gráfico de barras horizontais
3. **Top 5 Países** - Gráfico de barras horizontais
4. **Distribuição por Região** - Mapa do Brasil (VL_FOB por estado)

**Filtros:**
- Ano (slider)
- Mês (dropdown)

---

### Página 2: Análise Temporal

**Objetivo:** Responder às perguntas sobre evolução temporal das exportações.

**KPIs:**
- Valor FOB no Mês Atual
- Crescimento vs Mês Anterior
- Média Mensal FOB
- Trimestre com Maior Valor

**Gráficos:**
1. **Tendência Anual** - Gráfico de área (VL_FOB acumulado)
2. **Comparativo Mensal** - Gráfico de colunas (ano atual vs anterior)
3. **Sazonalidade** - Gráfico de linha com média móvel (12 meses)
4. **Distribuição Trimestral** - Gráfico de barras empilhadas

**Filtros:**
- Período (date range)
- Ano (botões)
- Comparar com ano anterior (toggle)

---

### Página 3: Produtos (NCM)

**Objetivo:** Análise detalhada dos produtos mais comercializados.

**KPIs:**
- Total de Produtos Distintos (NCM)
- Ticket Médio por Produto
- Produto com Maior Crescimento
- Categoria Mais Exportada

**Gráficos:**
1. **Top 10 Produtos** - Gráfico de barras horizontais com drill-down
2. **Participação por Categoria** - Gráfico de doughnut
3. **Correlação Peso x Valor** - Scatter plot (KG vs VL_FOB)
4. **Preço Unitário Médio** - Ranking (VL_FOB / KG_LIQUIDO)
5. **Evolução por Categoria** - Gráfico de linha múltipla

**Filtros:**
- Categoria de Produto (dropdown)
- NCM específico (search)
- Período (slider)

**Segmentações:**
- Por categoria (botões slicer)

---

### Página 4: Destinos Geográficos

**Objetivo:** Análise de países e blocos econômicos.

**KPIs:**
- Total de Países Destinatários
- País com Maior Crescimento
- Bloco Econômico Líder
- Exportações para a China (específico)

**Gráficos:**
1. **Mapa Mundial** - Mapa coroplético (VL_FOB por país)
2. **Top 10 Países** - Gráfico de barras com bandeiras
3. **Distribuição por Bloco** - Gráfico de pizza ou sunburst
4. **Evolução por Continente** - Gráfico de linha múltipla
5. **Matriz Estado x País** - Heatmap (VL_FOB cruzado)

**Filtros:**
- Continente (dropdown)
- Bloco Econômico (dropdown)
- País específico (search)

**Drill-down:**
- Continente → País → Detalhes

---

### Página 5: Balança Comercial

**Objetivo:** Comparar exportações vs importações (se dados de importação disponíveis).

**KPIs:**
- Saldo da Balança Comercial
- Exportações Totais
- Importações Totais
- Relação Exportação/Importação (%)

**Gráficos:**
1. **Exportações vs Importações** - Gráfico de colunas lado a lado
2. **Saldo Mensal** - Gráfico de colunas com linha de saldo
3. **Superávit/Déficit por Produto** - Gráfico de barras divergentes
4. **Saldo por País** - Gráfico de barras horizontais (positivo/negativo)
5. **Evolução Acumulada** - Gráfico de área com linha de tendência

**Filtros:**
- Tipo (Exportação/Importação/Balança)
- Período (date range)
- Produto específico

**Alertas Visuais:**
- Cor verde para superávit
- Cor vermelha para déficit

---

## Design e Layout

### Paleta de Cores

```
Cores Principais:
- Primária: #1f4e79 (Azul corporativo)
- Secundária: #2e75b6 (Azul claro)
- Destaque: #c55a11 (Laranja)
- Sucesso: #70ad47 (Verde)
- Alerta: #c00000 (Vermelho)
- Neutro: #7f7f7f (Cinza)

Cores de Fundo:
- Fundo: #ffffff (Branco)
- Cards: #f2f2f2 (Cinza claro)
- Bordas: #d9d9d9 (Cinza médio)
```

### Tipografia

- **Títulos:** Segoe UI Bold, 14-16pt
- **KPIs:** Segoe UI Bold, 24-32pt
- **Labels:** Segoe UI Regular, 10-12pt
- **Valores:** Segoe UI Semibold, 12-14pt

### Layout

- **Tamanho:** 16:9 (1920x1080)
- **Margens:** 20px em todos os lados
- **Espaçamento entre visuais:** 10px
- **Cabeçalho:** 60px de altura com título e filtros globais

---

## Fonte de Dados

### Conexão

**Tipo:** MySQL Database (ou arquivo CSV se não houver banco)

**Configuração:**
```
Servidor: [localhost ou IP do servidor MySQL]
Banco de dados: comexstat_dw
Autenticação: Windows ou SQL Server
```

### Tabelas/Views Utilizadas

1. **v_exportacoes_consolidadas** - View principal com todos os joins
2. **dim_tempo** - Para filtros de data
3. **dim_produto** - Para filtros de produto
4. **dim_pais** - Para filtros de país
5. **dim_estado** - Para filtros de estado
6. **fato_exportacao** - Para métricas detalhadas

### Relacionamentos no Power BI

```
fato_exportacao (1) -- (N) dim_tempo
fato_exportacao (1) -- (N) dim_produto
fato_exportacao (1) -- (N) dim_pais
fato_exportacao (1) -- (N) dim_estado
fato_exportacao (1) -- (N) dim_via
fato_exportacao (1) -- (N) dim_urf
```

---

## Medidas DAX (Exemplos)

### Métricas Básicas

```dax
// Valor Total FOB
Valor Total FOB = SUM(fato_exportacao[VL_FOB])

// Peso Total
Peso Total KG = SUM(fato_exportacao[KG_LIQUIDO])

// Quantidade de Transações
Total Transações = COUNTROWS(fato_exportacao)

// Ticket Médio
Ticket Médio = DIVIDE([Valor Total FOB], [Total Transações], 0)
```

### Métricas de Crescimento

```dax
// Valor FOB Ano Anterior
Valor FOB AA = CALCULATE(
    [Valor Total FOB],
    SAMEPERIODLASTYEAR(dim_tempo[Data])
)

// Crescimento YoY
Crescimento YoY = 
    VAR FOB_Atual = [Valor Total FOB]
    VAR FOB_Anterior = [Valor FOB AA]
    RETURN
        DIVIDE(FOB_Atual - FOB_Anterior, FOB_Anterior, 0)
```

### Ranking e TOP N

```dax
// Top Produto
Top Produto = 
    TOPN(1, 
        VALUES(dim_produto[id_product]), 
        [Valor Total FOB], 
        DESC
    )

// Ranking de Países
Ranking Países = 
    RANKX(
        ALL(dim_pais[id_country]),
        [Valor Total FOB],
        ,DESC
    )
```

---

## Interatividade

### Filtros Cruzados

- Selecionar um país no mapa atualiza todos os gráficos
- Clicar em um produto filtra as análises temporais
- Selecionar estado atualiza análise de URFs

### Tooltips Personalizados

Criar páginas de tooltip com:
- Detalhes do produto/país selecionado
- Comparativo com período anterior
- Tendência dos últimos 12 meses

### Navegação

Adicionar botões de navegação:
- "Próxima Página" / "Página Anterior"
- "Voltar ao Início" (Visão Geral)
- Ícones intuitivos para cada página

---

## Requisitos de Performance

### Otimizações

1. **Agregações:** Usar tabelas agregadas para visões de alto nível
2. **Filtros:** Aplicar filtros nas fontes quando possível
3. **Colunas Calculadas:** Evitar, preferir medidas
4. **Cardinalidade:** Reduzir cardinalidade de colunas de texto

### Limite de Dados

- Visualizações: Máximo 1000 pontos de dados visíveis
- Drill-down: Habilitar apenas quando necessário
- Mapas: Usar níveis de hierarquia para performance

---

## Publicação e Compartilhamento

### Configurações

- **Workspace:** Criar workspace dedicado no Power BI Service
- **Refresh:** Agendar refresh diário (se conectado a banco)
- **Permissões:** Configurar acesso para stakeholders

### Formatos de Exportação

#### Como Exportar no Power BI Desktop:

**1. Exportar para PDF:**
```
Arquivo → Exportar → Exportar para PDF
```
- Selecione as páginas desejadas (todas ou específicas)
- Escolha se inclui filtros aplicados
- Clique em "Exportar"
- O PDF mantém formatação, cores e layout

**2. Exportar para PowerPoint:**
```
Arquivo → Exportar → Exportar para PowerPoint
```
- Gera slides individuais para cada página do relatório
- Cada slide é uma imagem estática do dashboard
- Útil para apresentações acadêmicas/executivas
- Mantém qualidade visual mas sem interatividade

**3. Exportar Dados para Excel:**
```
Clique no visual → ... (reticências) → Exportar dados
```
- **Dados resumidos:** Exporta os dados agregados do visual
- **Dados subjacentes:** Exporta dados brutos da tabela fonte
- Formato .xlsx, pronto para análise adicional

**4. Publicar no Power BI Service (Nuvem):**
```
Home → Publicar → Selecionar workspace
```
- Requer conta Microsoft (gratuita ou corporativa)
- Permite compartilhar via link
- Atualizações automáticas com refresh agendado
- Acesso via navegador e aplicativo mobile

---

## Guia de Exportação Acadêmica

### Para Entrega na Faculdade (IESB)

**Formatos recomendados:**

1. **PDF (OBRIGATÓRIO)**
   - Nome do arquivo: `Dashboard_COMEX_2025_RA_24114290041.pdf`
   - Incluir todas as páginas
   - Verificar se todos os visuais estão legíveis

2. **PowerPoint (OPCIONAL - para apresentação)**
   - Nome: `Apresentacao_COMEX_2025_RA_24114290041.pptx`
   - Adicionar comentários explicativos nos slides

3. **Arquivo .pbix (FONTE)**
   - Nome: `Dashboard_COMEX_2025_RA_24114290041.pbix`
   - Compactar com os dados ou incluir instruções de conexão

**Checklist antes de exportar:**
- [ ] Filtros padrão aplicados (ano = 2025)
- [ ] Títulos e labels visíveis
- [ ] Paleta de cores consistente
- [ ] Sem dados sensíveis expostos
- [ ] Legenda dos gráficos legível

---

## Checklist de Validação

### Funcional

- [ ] Todos os KPIs calculam corretamente
- [ ] Filtros aplicam-se a todas as páginas
- [ ] Drill-down funciona em todos os visuais
- [ ] Tooltips aparecem corretamente
- [ ] Navegação entre páginas fluida

### Visual

- [ ] Paleta de cores consistente
- [ ] Fontes legíveis em todos os tamanhos
- [ ] Layout responsivo (ajuste de tela)
- [ ] Ícones intuitivos
- [ ] Títulos e labels claros

### Dados

- [ ] Valores correspondem às expectativas
- [ ] Formatação de moeda (R$) correta
- [ ] Datas formatadas corretamente
- [ ] Percentuais calculados corretamente
- [ ] Sem valores em branco inesperados

---

## Próximos Passos

1. **Conectar fonte de dados** (MySQL ou CSV)
2. **Criar modelo de dados** no Power BI
3. **Implementar medidas DAX**
4. **Construir visuais** página por página
5. **Aplicar design e formatação**
6. **Testar interatividade**
7. **Validar com stakeholders**
8. **Publicar e agendar refresh**

---

*Especificação técnica para desenvolvimento do dashboard no Power BI Desktop*
