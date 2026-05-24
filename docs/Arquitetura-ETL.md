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

## Fase 1: EXTRAÇÃO (`extract.py`)

### Fonte de Dados

O pipeline ETL usa **exclusivamente dados locais**:

- Usa arquivos CSV pré-existentes na pasta `input/`
- Arquivo principal: `input/Exportacoes_reduzidos.csv`
- Vantagens: Mais rápido, sem dependência de internet, dados fixos
- Uso: Desenvolvimento, testes e produção

### Como Executar

No Linux, use o script shell que ativa automaticamente o ambiente virtual:

```bash
bash executar.sh
```

Em outros sistemas operacionais:

```bash
python main.py
```

### Entradas
- `input/Exportacoes_reduzidos.csv` - Dados de exportação 2025 (local)
- Dicionários em `dicionarios/` para enriquecimento

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

---

## Fase 2: TRANSFORMAÇÃO (`map.py`)

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
    └──► agro_filtering() ─────────────► Remove flag=0 (inválidos)
```

### Dicionários Utilizados

| Dicionário | Coluna de Join | Descrição |
|------------|----------------|-----------|
| dict_sg_uf.csv | SG_UF_NCM | Estados brasileiros |
| dict_country.csv | CO_PAIS | Países de destino |
| dict_urf.csv | CO_URF | Unidades da Receita Federal |
| dict_ncm_product.csv | CO_NCM | Produtos NCM |
| dict_via.csv | CO_VIA | Vias de transporte |
| dict_bloco.csv | CO_BLOCO | Blocos econômicos |
| dict_municipio.csv | CO_MUNICIPIO | Municípios |

---

## Fase 3: ANÁLISE PREDITIVA (`regressao.py`)

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
1. **Previsões vs Valores Reais** - Scatter plot com linha ideal
2. **Análise de Resíduos** - Resíduos vs valores previstos
3. **Distribuição dos Resíduos** - Histograma
4. **Painel de Métricas** - Estatísticas do modelo

---

## Fase 4: CARGA (`load.py`)

### Saídas Geradas

| Arquivo | Formato | Conteúdo |
|---------|---------|----------|
| dados_finais.csv | CSV | Dataset completo processado |
| modelo_conceitual.html | HTML | Diagrama ER interativo (Mermaid.js) |
| comexstat_mysql_schema.sql | SQL | Script para criar banco MySQL |
| grafico_previsao_completo.png | PNG | Visualização da regressão |

### Modelo Dimensional (Star Schema)

**Tabelas de Dimensão**:
- dim_tempo (ano, mês, trimestre)
- dim_produto (NCM, descrição)
- dim_pais (código, nome)
- dim_estado (UF, nome)
- dim_via (código, descrição)
- dim_urf (código, nome)

**Tabela Fato**:
- fato_exportacao (métricas de exportação)

---

## Fluxo Completo

```python
# main.py
from src.extract import ler_dados_csv
from src.map import detectar_valores_vazios, expandir_dados
from src.regressao import aplicar_regressao_completa
from src.load import executar_load_completo

# 1. Extrair
df = ler_dados_csv(r"input\Exportacoes_reduzidos.csv")

# 2. Transformar
df = detectar_valores_vazios(df)
df = expandir_dados(df)

# 3. Analisar
resultado = aplicar_regressao_completa(df)

# 4. Carregar
executar_load_completo(df, r"output\dados_finais.csv")
```

---

## Próximos Passos Sugeridos

- [ ] Implementar carga real em banco MySQL/PostgreSQL
- [ ] Adicionar logging estruturado
- [ ] Criar testes unitários
- [ ] Implementar validação de esquema
