# API e Módulos

## Estrutura de Módulos

```
src/
├── extract.py      # Extração de dados
├── map.py          # Transformação e enriquecimento
├── regressao.py    # Análise preditiva
├── load.py         # Carga e modelagem
└── validate.py     # Validações
```

---

## extract.py

Módulo de extração de dados de arquivos CSV.

### ler_dados_csv(file_path, delimiter=";")

Lê um arquivo CSV e retorna um DataFrame pandas.

**Parâmetros:**
| Parâmetro | Tipo | Padrão | Descrição |
|-----------|------|--------|-----------|
| file_path | str | - | Caminho do arquivo CSV |
| delimiter | str | ";" | Separador de campos |

**Retorno:** DataFrame pandas

**Exemplo:**
```python
from src.extract import ler_dados_csv

df = ler_dados_csv("data/data/input/Exportacoes_reduzidos.csv", delimiter=";")
print(f"Carregados {len(df)} registros")
```

### ler_csv_para_validacao(file_path, delimiter=";")

Lê CSV para validação de dados.

**Parâmetros:** Iguais a `ler_dados_csv`

**Retorno:** DataFrame pandas

### baixar_csv(url, filename)

Verifica e retorna dados locais de exportações.

**Nota:** O projeto usa exclusivamente dados locais do arquivo data/input/Exportacoes_reduzidos.csv.

---

## map.py

Módulo de transformação e enriquecimento de dados.

### detectar_valores_vazios(df: pd.DataFrame) -> pd.DataFrame

Detecta e preenche valores vazios (NaN) com zeros.

**Parâmetros:**
| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| df | pd.DataFrame | DataFrame de entrada |

**Retorno:** DataFrame com valores vazios preenchidos

**Exemplo:**
```python
from src.map import detectar_valores_vazios

df_limpo = detectar_valores_vazios(df)
```

### expandir_estados(df, sg_uf_dict_path)

Expande dados com informações de estados brasileiros.

**Parâmetros:**
| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| df | pd.DataFrame | DataFrame de entrada |
| sg_uf_dict_path | str | Caminho para dict_sg_uf.csv |

**Retorno:** DataFrame enriquecido com colunas de estado

### expandir_paises(df, dict_country_path)

Expande dados com informações de países.

**Parâmetros:**
| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| df | pd.DataFrame | DataFrame de entrada |
| dict_country_path | str | Caminho para dict_country.csv |

**Retorno:** DataFrame enriquecido com colunas de país

### expandir_ncm(df, dict_ncm_path)

Expande dados com informações de produtos NCM.

**Parâmetros:**
| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| df | pd.DataFrame | DataFrame de entrada |
| dict_ncm_path | str | Caminho para dict_ncm_product.csv |

**Retorno:** DataFrame enriquecido com colunas de produto

### expandir_urf(df, dict_urf_path)

Expande dados com informações de URFs (Unidades da Receita Federal).

**Parâmetros:**
| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| df | pd.DataFrame | DataFrame de entrada |
| dict_urf_path | str | Caminho para dict_urf.csv |

**Retorno:** DataFrame enriquecido com colunas de URF

### agro_filtering(df) -> pd.DataFrame

Filtra dados removendo registros inválidos (flag=0).

**Parâmetros:**
| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| df | pd.DataFrame | DataFrame de entrada |

**Retorno:** DataFrame filtrado

### expandir_dados(df) -> pd.DataFrame

Executa todas as expansões em sequência.

**Fluxo interno:**
1. expandir_estados
2. expandir_paises
3. expandir_urf
4. expandir_ncm
5. agro_filtering

**Exemplo:**
```python
from src.map import expandir_dados

df_enriquecido = expandir_dados(df)
```

---

## regressao.py

Módulo de análise preditiva usando regressão linear.

### aplicar_regressao_completa(df, produto=None)

Aplica modelo de regressão linear completo.

**Parâmetros:**
| Parâmetro | Tipo | Padrão | Descrição |
|-----------|------|--------|-----------|
| df | pd.DataFrame | - | Dataset com dados de exportação |
| produto | str | None | Produto específico ou None para todos |

**Retorno:** dict com métricas do modelo

```python
{
    'produto': str,
    'mse': float,
    'mae': float,
    'registros_analisados': int,
    'total_registros': int
}
```

**Features utilizadas:**
- CO_ANO, CO_MES
- CO_NCM, CO_UNID
- CO_PAIS, SG_UF_NCM
- CO_VIA, CO_URF
- QT_ESTAT, KG_LIQUIDO

**Target:** VL_FOB

**Métricas calculadas:**
- MAE (Mean Absolute Error)
- MSE (Mean Squared Error)
- RMSE (Root Mean Squared Error)
- R² Score

**Exemplo:**
```python
from src.regressao import aplicar_regressao_completa

# Analisar todos os produtos
resultado = aplicar_regressao_completa(df)
print(f"R²: {resultado['r2']:.4f}")

# Analisar produto específico
resultado = aplicar_regressao_completa(df, produto="CARNES")
```

### aplicar_regressao(df, produto)

Função legada. Alias para `aplicar_regressao_completa`.

---

## load.py

Módulo de carga e geração de modelos de dados.

### executar_load_completo(df, output_file)

Executa a fase completa de load.

**Parâmetros:**
| Parâmetro | Tipo | Padrão | Descrição |
|-----------|------|--------|-----------|
| df | pd.DataFrame | - | Dataset processado |
| output_file | str | "data/output/dados_finais.csv" | Caminho de saída |

**Ações realizadas:**
1. Verifica se dados já existem
2. Carrega no banco (simulação)
3. Gera HTML do modelo conceitual
4. Gera script SQL MySQL

**Exemplo:**
```python
from src.load import executar_load_completo

executar_load_completo(df, "data/output/dados_finais.csv")
```

### gerar_html_modelo_conceitual(df, output_path)

Gera arquivo HTML com diagrama ER interativo.

**Parâmetros:**
| Parâmetro | Tipo | Padrão | Descrição |
|-----------|------|--------|-----------|
| df | pd.DataFrame | - | Dataset para estatísticas |
| output_path | str | "data/output/modelo_conceitual.html" | Caminho de saída |

**Retorno:** bool (sucesso/falha)

### gerar_sql_mysql_star_schema(df)

Gera script SQL completo para MySQL com Star Schema.

**Parâmetros:**
| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| df | pd.DataFrame | Dataset para gerar INSERTs |

**Retorno:** bool (sucesso/falha)

**Arquivo gerado:** `data/output/comexstat_mysql_schema.sql`

**Conteúdo do SQL:**
- DROP/CREATE DATABASE
- CREATE TABLE para 6 dimensões + 1 fato
- INSERTs com dados únicos
- Views para Power BI
- Índices otimizados
- Instruções de integração

### verificar_dados_existentes(file_path)

Verifica se os dados já foram processados.

**Parâmetros:**
| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| file_path | str | Caminho do arquivo CSV |

**Retorno:** bool

### carregar_dados_banco(df, db_name)

Simula carregamento no banco de dados.

**Parâmetros:**
| Parâmetro | Tipo | Padrão | Descrição |
|-----------|------|--------|-----------|
| df | pd.DataFrame | - | Dataset a carregar |
| db_name | str | "comexstat_db" | Nome do banco |

**Retorno:** bool (sucesso/falha)

**Nota:** Esta é uma simulação. A implementação real requer conector MySQL/PostgreSQL.

---

## validate.py

Módulo de validação de dados.

**Funções:**
- Validação de estrutura CSV
- Verificação de tipos de dados
- Validação de consistência

---

## Exemplo de Uso Completo

```python
from src.extract import ler_dados_csv
from src.map import detectar_valores_vazios, expandir_dados
from src.regressao import aplicar_regressao_completa
from src.load import executar_load_completo

# 1. Extrair dados
df = ler_dados_csv("data/input/Exportacoes_reduzidos.csv")

# 2. Transformar dados
df = detectar_valores_vazios(df)
df = expandir_dados(df)

# 3. Aplicar regressão
metricas = aplicar_regressao_completa(df)
print(f"Modelo R²: {metricas['r2']:.4f}")

# 4. Carregar e gerar outputs
executar_load_completo(df, "data/output/dados_finais.csv")
```

---

## Constantes e Configurações

### Caminhos de Arquivos (extract.py)

```python
data/input/Exportacoes_reduzidos.csv  # Dados de exportação locais
```

### Caminhos de Dicionários (map.py)

```python
dicionarios/dict_sg_uf.csv
dicionarios/dict_country.csv
dicionarios/dict_urf.csv
dicionarios/dict_ncm_product.csv
```

### Configurações de Modelo (regressao.py)

```python
test_size = 0.2      # 20% para teste
random_state = 42    # Seed para reprodutibilidade
```
