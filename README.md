# Projeto ETL - Análise de Dados de Exportação COMEX Stat 2025

Projeto de Extração, Transformação e Carga (ETL) de dados de exportação brasileira do COMEX Stat 2025, com análise preditiva via regressão linear e geração de modelo dimensional para banco de dados.

## Sinta-se a vontade para acessar a wiki do projeto

https://github.com/Lupahlinda/Projeto-ETL-COMEXStat-2025/wiki


##  Funcionalidades

- **Extração**: Leitura de dados CSV locais de exportações 2025
- **Transformação**: Expansão de dados via dicionários (países, estados, URFs, produtos NCM)
- **Análise Preditiva**: Regressão linear para previsão de valores FOB de exportação
- **Visualização**: Gráficos comparativos (previsões vs reais, resíduos, distribuição)
- **Modelagem**: Geração de modelo conceitual HTML e script SQL MySQL (Star Schema)

##  Estrutura de Pastas

```
Projeto-ETL-COMEXStat-2025/
├── dicionarios/          # Dicionários de dados para enriquecimento
│   ├── dict_bloco.csv       # Blocos econômicos
│   ├── dict_country.csv     # Países
│   ├── dict_municipio.csv   # Municípios brasileiros
│   ├── dict_ncm_product.csv # Produtos NCM
│   ├── dict_sg_uf.csv       # Estados brasileiros
│   ├── dict_urf.csv         # Unidades de Despacho
│   └── dict_via.csv         # Vias de transporte
├── input/                # Arquivos CSV de entrada (dados fixos)
│   ├── Exportacoes_reduzidos.csv
│   ├── Importacoes_reduzidos.csv
│   ├── NCM.csv
│   ├── NCM_UNIDADE.csv
│   ├── PAIS.csv
│   ├── PAIS_BLOCO.csv
│   ├── UF.csv
│   ├── UF_MUN.csv
│   ├── URF.csv
│   └── VIA.csv
├── output/               # Arquivos gerados
│   ├── dados_finais.csv        # Dataset processado
│   ├── modelo_conceitual.html  # Diagrama ER interativo
│   ├── comexstat_mysql_schema.sql # Script SQL MySQL
│   └── grafico_previsao_completo.png # Visualização da regressão
├── src/                  # Código fonte
│   ├── extract.py        # Leitura de dados CSV
│   ├── map.py            # Transformação e enriquecimento
│   ├── regressao.py      # Análise preditiva
│   ├── load.py           # Geração de modelo e SQL
│   └── validate.py       # Validações
├── main.py              # Script principal
├── reset_project.py     # Script de limpeza/reset
└── requirements.txt     # Dependências Python
```

##  Como Executar

### Pré-requisitos
- Python 3.8+
- pip

### Instalação

```bash
# Clone o repositório
git clone https://github.com/Lupahlinda/Projeto-ETL-COMEXStat-2025.git
cd Projeto-ETL-COMEXStat-2025

# Instale as dependências
pip install -r requirements.txt
```

### Execução

```bash
# Executar pipeline ETL completo
python main.py

# Limpar projeto (remover outputs gerados)
python reset_project.py
```

##  Pipeline ETL

### 1. Extração (`extract.py`)
- Lê `input/Exportacoes_reduzidos.csv` com dados de exportação 2025
- Colunas: CO_ANO, CO_MES, CO_NCM, CO_UNID, CO_PAIS, SG_UF_NCM, CO_VIA, CO_URF, QT_ESTAT, KG_LIQUIDO, VL_FOB, flag

### 2. Transformação (`map.py`)
- **Detectar valores vazios**: Preenche com zeros
- **Expandir estados**: Merge com dicionário de UF
- **Expandir países**: Merge com dicionário de países
- **Expandir URFs**: Merge com dicionário de unidades de despacho
- **Expandir produtos NCM**: Merge com dicionário de produtos
- **Filtrar dados**: Remove registros com flag=0 (inválidos)

### 3. Análise Preditiva (`regressao.py`)
- **Modelo**: Regressão Linear com One-Hot Encoding para variáveis categóricas
- **Features**: CO_ANO, CO_MES, CO_NCM, CO_UNID, CO_PAIS, SG_UF_NCM, CO_VIA, CO_URF, QT_ESTAT, KG_LIQUIDO
- **Target**: VL_FOB (valor FOB da exportação)
- **Métricas**: MSE, MAE, RMSE, R² Score
- **Saída**: Gráfico 2x2 com previsões vs reais, resíduos, histograma e painel de métricas

### 4. Carga/Modelagem (`load.py`)
- Gera modelo conceitual HTML com diagrama ER (Mermaid.js)
- Gera script SQL MySQL com Star Schema:
  - Dimensões: tempo, produto, país, estado, via, URF
  - Fato: tabela de exportações
- Gera arquivo CSV final processado

##  Arquivos Gerados

| Arquivo | Descrição |
|---------|-----------|
| `output/dados_finais.csv` | Dataset completo enriquecido |
| `output/modelo_conceitual.html` | Diagrama ER interativo (abra no navegador) |
| `output/comexstat_mysql_schema.sql` | Script SQL para criar banco MySQL |
| `output/grafico_previsao_completo.png` | Visualização da análise de regressão |

##  Modelo de Dados

O projeto implementa modelo dimensional **Star Schema** com 9 tabelas obrigatórias:

### Tabelas de Dimensão
- **dim_tempo**: Ano, mês, trimestre, semestre
- **dim_produto**: Código NCM, descrição do produto
- **dim_pais**: Código e nome do país
- **dim_estado**: Sigla e nome do estado
- **dim_via**: Código e descrição da via de transporte
- **dim_urf**: Código e nome da unidade de despacho

### Tabelas de Fato
- **fato_exportacao**: Métricas de exportação (VL_FOB, KG_LIQUIDO, QT_ESTAT)

### Tabelas Auxiliares
- **dim_bloco**: Blocos econômicos
- **dim_municipio**: Municípios brasileiros

##  Tecnologias

- **pandas**: Manipulação de dados
- **scikit-learn**: Machine learning (regressão linear, métricas)
- **matplotlib**: Visualização de dados
- **numpy**: Operações numéricas

##  Scripts Disponíveis

| Script | Função |
|--------|--------|
| `main.py` | Executa pipeline ETL completo |
| `reset_project.py` | Limpa outputs e cache, preserva dados de input |

##  Estrutura do Código

```
src/
├── extract.py      # ler_dados_csv(), baixar_csv()
├── map.py          # detectar_valores_vazios(), expandir_dados(), agro_filtering()
├── regressao.py    # aplicar_regressao_completa() - modelo ML
├── load.py         # carregar_dados_banco(), gerar_sql_mysql_star_schema(), 
│                   # gerar_html_modelo_conceitual(), executar_load_completo()
└── validate.py     # Funções de validação de dados
```

##  Desenvolvido para
Análise de comércio exterior brasileiro - Dados COMEX Stat 2025
