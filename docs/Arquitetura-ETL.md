# Arquitetura do Pipeline ETL

## Visão Geral

O pipeline ETL processa dados de exportação brasileira em 4 fases principais:

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   EXTRACT   │ -> │  TRANSFORM  │ -> │  REGRESSÃO  │ -> │    LOAD     │
│             │    │             │    │             │    │             │
│ CSV Local   │    │ Enriquecer  │    │ Prever      │    │ Modelo +    │
│ Dicionários │    │ Filtrar     │    │ VL_FOB      │    │ SQL + CSV   │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

---

## Métodos de Execução

O pipeline pode ser executado de duas formas:

### 🎓 Via Jupyter Notebooks (Recomendado)
- Notebooks interativos em `notebooks/`
- Execução célula por célula
- Visualização integrada de resultados
- Ideal para análise exploratória

### ⚙️ Via Scripts Python
- Scripts automatizados em `scripts/`
- Execução completa em um comando
- Ideal para produção e automação

---

## Fase 1: EXTRAÇÃO

### Implementação
- **Módulo Python**: `src/extract.py`
- **Notebook**: `notebooks/01_Extract.ipynb`
- **Script**: `scripts/main.py` (etapa 1)

### Fonte de Dados

O pipeline ETL usa **exclusivamente dados locais**:

- Usa arquivos CSV pré-existentes na pasta `data/input/`
- Arquivo principal: `data/input/Exportacoes_reduzidos.csv`
- Vantagens: Mais rápido, sem dependência de internet, dados fixos
- Uso: Desenvolvimento, testes e produção

### Como Executar

**Via Jupyter Notebook:**
```bash
jupyter notebook notebooks/
# Execute: 01_Extract.ipynb
```

**Via Script:**
```bash
# Linux
bash scripts/executar.sh

# Windows/macOS
python scripts/main.py
```

### Entradas
- `data/input/Exportacoes_reduzidos.csv` - Dados de exportação 2025 (local)
- Dicionários em `data/dictionaries/` para enriquecimento

### Colunas do CSV
| Coluna | Descrição |
|--------|-----------|
| CO_ANO | Ano |
| CO_MES | Mês |
| CO_NCM | Código NCM do produto |
| CO_UNID | Código da unidade |
| CO_PAIS | Código do país de destino |
| SG_UF_NCM | Sigla do estado |
| CO_VIA | Código da via de transporte |
| CO_URF | Código da URF |
| QT_ESTAT | Quantidade estatística |
| KG_LIQUIDO | Peso líquido (kg) |
| VL_FOB | Valor FOB |
| flag | Flag de validação |

### Funções Principais
```python
ler_dados_csv(file_path, delimiter=";")                    # Lê CSV
baixar_csv(url, filename)                                 # Usa dados locais
baixar_totais_validacao(url, filename)                    # Validação local
```

### Saídas
- `data/output/dados_carregados.csv` - Dados brutos carregados

---

## Fase 2: TRANSFORMAÇÃO

### Implementação
- **Módulo Python**: `src/map.py`
- **Notebook**: `notebooks/02_Transform.ipynb`
- **Script**: `scripts/main.py` (etapa 2)

### Fluxo de Transformação

```
Dados Brutos
    │
    ├──► detectar_valores_vazios() ──► Preenche NaN com 0
    │
    ├──► expandir_estados() ─────────► Merge com dict_sg_uf.csv
    │
    ├──► expandir_paises() ──────────► Merge com dict_country.csv
    │
    ├──► expandir_urf() ─────────────► Merge com dict_urf.csv
    │
    ├──► expandir_ncm() ─────────────► Merge com dict_ncm_product.csv
    │
    └──► Remove flag se existir ──────► Limpeza final
```

### Dicionários Utilizados

| Dicionário | Localização | Coluna de Join | Descrição |
|------------|-------------|----------------|-----------|
| dict_sg_uf.csv | data/dictionaries/ | SG_UF_NCM | Estados brasileiros |
| dict_country.csv | data/dictionaries/ | CO_PAIS | Países de destino |
| dict_urf.csv | data/dictionaries/ | CO_URF | Unidades da Receita Federal |
| dict_ncm_product.csv | data/dictionaries/ | CO_NCM | Produtos NCM |
| dict_via.csv | data/dictionaries/ | CO_VIA | Vias de transporte |
| dict_bloco.csv | data/dictionaries/ | CO_BLOCO | Blocos econômicos |
| dict_municipio.csv | data/dictionaries/ | CO_MUNICIPIO | Municípios |

### Funções Principais
```python
detectar_valores_vazios(df)           # Detecta e trata valores nulos
expandir_dados(df)                   # Expande com todos os dicionários
expandir_estados(df, dict_path)      # Enriquece com dados de estados
expandir_paises(df, dict_path)       # Enriquece com dados de países
expandir_ncm(df, dict_path)          # Enriquece com dados de produtos
expandir_urf(df, dict_path)          # Enriquece com dados de URFs
```

### Saídas
- `data/output/dados_transformados.csv` - Dados após transformação

---

## Fase 3: ANÁLISE PREDITIVA

### Implementação
- **Módulo Python**: `src/regressao.py`
- **Notebook**: `notebooks/03_Regressao.ipynb`
- **Script**: `scripts/main.py` (etapa 3)

### Modelo de Regressão Linear

**Objetivo**: Prever o valor FOB das exportações

**Features (X)**:
- CO_ANO, CO_MES
- CO_NCM, CO_UNID
- CO_PAIS, SG_UF_NCM
- CO_VIA, CO_URF
- QT_ESTAT, KG_LIQUIDO

**Target (y)**: VL_FOB

**Pré-processamento**:
```python
ColumnTransformer([
    ('cat', OneHotEncoder(handle_unknown='ignore'), 
     ['CO_PAIS', 'SG_UF_NCM'])
], remainder='passthrough')
```

### Métricas Calculadas

| Métrica | Descrição |
|---------|-----------|
| MAE | Mean Absolute Error |
| MSE | Mean Squared Error |
| RMSE | Root Mean Squared Error |
| R² | Coefficient of Determination |

### Visualizações Geradas

O modelo gera um gráfico 2x2 com:
1. **Estatísticas do Dataset** - Informações gerais dos dados
2. **Top 10 Produtos** - Gráfico de barras por valor FOB
3. **Top 10 Países** - Gráfico de barras por valor FOB
4. **Estatísticas do Modelo** - Métricas e performance

### Funções Principais
```python
aplicar_regressao_completa(df, produto=None)  # Aplica modelo completo
```

### Saídas
- `data/output/dados_com_previsoes.csv` - Dados com previsões
- `data/output/grafico_previsao_completo.png` - Visualização da análise

---

## Fase 4: CARGA

### Implementação
- **Módulo Python**: `src/load.py`
- **Notebook**: `notebooks/04_Load.ipynb`
- **Script**: `scripts/main.py` (etapa 4)

### Saídas Geradas

| Arquivo | Formato | Localização | Conteúdo |
|---------|---------|-------------|----------|
| dados_finais.csv | CSV | data/output/ | Dataset completo processado |
| modelo_conceitual.html | HTML | data/output/ | Diagrama ER interativo (Mermaid.js) |
| comexstat_mysql_schema.sql | SQL | data/output/ | Script para criar banco MySQL |
| grafico_previsao_completo.png | PNG | data/output/ | Visualização da regressão |

### Modelo Dimensional (Star Schema)

**Tabelas de Dimensão**:
- dim_tempo (ano, mês, trimestre)
- dim_ncm (código NCM, descrições)
- dim_pais (código, nome)
- dim_estado (UF, nome, região)
- dim_via (código, descrição)
- dim_urf (código, nome)
- dim_unidade (código, descrição)
- dim_bloco (código, nome)
- dim_municipio (código, nome)

**Tabela Fato**:
- fato_exportacao (métricas de exportação)

### Funções Principais
```python
executar_load_completo(df, output_csv_path)  # Gera todos os outputs
gerar_sql_mysql_star_schema(df)              # Gera script SQL
gerar_html_modelo_conceitual(df)              # Gera documentação HTML
carregar_dados_banco(df, db_name)            # Simula carregamento em banco
```

---

## Fluxo Completo

### Via Scripts Python
```python
# scripts/main.py
from src.extract import ler_dados_csv
from src.map import detectar_valores_vazios, expandir_dados
from src.regressao import aplicar_regressao_completa
from src.load import executar_load_completo

# 1. Extrair
df = ler_dados_csv("data/input/Exportacoes_reduzidos.csv")

# 2. Transformar
df = detectar_valores_vazios(df)
df = expandir_dados(df)

# 3. Analisar
resultado = aplicar_regressao_completa(df)

# 4. Carregar
executar_load_completo(df, None)
```

### Via Jupyter Notebooks
```python
# notebooks/01_Extract.ipynb
df = ler_dados_csv("data/input/Exportacoes_reduzidos.csv")
df.to_csv("data/output/dados_carregados.csv", index=False)

# notebooks/02_Transform.ipynb
df = pd.read_csv("data/output/dados_carregados.csv")
df = detectar_valores_vazios(df)
df = expandir_dados(df)
df.to_csv("data/output/dados_transformados.csv", index=False)

# notebooks/03_Regressao.ipynb
df = pd.read_csv("data/output/dados_transformados.csv")
resultado = aplicar_regressao_completa(df)
# Dados com previsões salvos automaticamente

# notebooks/04_Load.ipynb
df = pd.read_csv("data/output/dados_com_previsoes.csv")
executar_load_completo(df, None)
```

---

## Diagrama de Fluxo de Dados

```
data/input/Exportacoes_reduzidos.csv
         ↓
    [EXTRACT]
         ↓
data/output/dados_carregados.csv
         ↓
    [TRANSFORM]
         ↓
data/output/dados_transformados.csv
         ↓
    [REGRESSÃO]
         ↓
data/output/dados_com_previsoes.csv
         ↓
    [LOAD]
         ↓
├─► data/output/dados_finais.csv
├─► data/output/modelo_conceitual.html
├─► data/output/comexstat_mysql_schema.sql
└─► data/output/grafico_previsao_completo.png
```

---

## Dependências entre Etapas

Cada etapa depende da saída da etapa anterior:

1. **Extract** → Gera `dados_carregados.csv`
2. **Transform** → Usa `dados_carregados.csv`, gera `dados_transformados.csv`
3. **Regressão** → Usa `dados_transformados.csv`, gera `dados_com_previsoes.csv`
4. **Load** → Usa `dados_com_previsoes.csv`, gera outputs finais

**Importante:** Execute as etapas em ordem sequencial!

---

## Próximos Passos Sugeridos

- [ ] Implementar carga real em banco MySQL/PostgreSQL
- [ ] Adicionar logging estruturado
- [ ] Criar testes unitários para cada módulo
- [ ] Implementar validação de esquema automática
- [ ] Adicionar suporte a processamento paralelo
- [ ] Implementar cache inteligente para dicionários
- [ ] Criar dashboard automático no Power BI