# Projeto ETL - Análise de Dados de Exportação COMEX Stat 2025

Projeto de Extração, Transformação e Carga (ETL) de dados de exportação brasileira do COMEX Stat 2025, com análise preditiva via regressão linear e geração de modelo dimensional para banco de dados.

---

##  Agradecimentos e Créditos

Este projeto foi desenvolvido com base no trabalho de **[Pedro Tuto](https://github.com/Pedro-Tuto)** - [ETL-Comexstat-export-2024](https://github.com/Pedro-Tuto/ETL-Comexstat-export-2024).

A estrutura inicial e conceitos de ETL foram inspirados nesse repositório base, posteriormente adaptado e expandido para dados de 2025.

---

##  Informações Acadêmicas

| | |
|:---|:---|
| **Disciplina** | Business Intelligence e Data Warehouse |
| **Professor** | Rodrigo Gonçalves Pinto |
| **Instituição** | IESB - Instituto de Educação Superior de Brasília |
| **Campus** | Ceilândia - DF |
| **Aluno** | Luis Henrique Costa |
| **RA** | 24114290041 |
| **Curso** | ADS - Análise e Desenvolvimento de Sistemas |

---

##  Sumário

- [Funcionalidades](#-funcionalidades)
- [Como Executar](#-como-executar)
- [Pipeline ETL](#-pipeline-etl)
- [Arquivos Gerados](#-arquivos-gerados)
- [Modelo de Dados](#-modelo-de-dados)
- [Tecnologias](#-tecnologias)
- [Estrutura do Código](#-estrutura-do-código)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Documentação](#-documentação)
- [Repositório Base](#-agradecimentos-e-créditos)
- [Informações Acadêmicas](#-informações-acadêmicas)

---

##  Funcionalidades

- **Extração**: Leitura de dados CSV locais de exportações 2025
- **Transformação**: Expansão de dados via dicionários (países, estados, URFs, produtos NCM)
- **Análise Preditiva**: Regressão linear para previsão de valores FOB de exportação
- **Visualização**: Gráficos comparativos (previsões vs reais, resíduos, distribuição)
- **Modelagem**: Geração de modelo conceitual HTML e script SQL MySQL (Star Schema)

##  Como Executar

### Pré-requisitos
- Python 3.8+
- pip
- (Linux) bash
- (Opcional) Jupyter Notebook/Lab para execução interativa

### Instalação

```bash
# Clone o repositório
git clone https://github.com/Lupahlinda/Projeto-ETL-COMEXStat-2025.git
cd Projeto-ETL-COMEXStat-2025

# Instale as dependências
pip install -r requirements.txt

# Se desejar usar Jupyter Notebook (opcional)
pip install jupyter notebook
# ou
pip install jupyterlab
```

### Execução

#### Execução via Jupyter Notebooks (Recomendado)

Para uma experiência interativa e melhor visualização dos resultados, recomendamos executar o projeto via Jupyter Notebooks.

**Iniciar o Jupyter:**
```bash
# Iniciar Jupyter Notebook
jupyter notebook notebooks/

# Ou JupyterLab (interface mais moderna)
jupyter lab notebooks/
```

**Sequência de Execução:**
Execute os notebooks em ordem sequencial:

1. **`00_Introducao.ipynb`** - Visão geral e configuração inicial
2. **`01_Extract.ipynb`** - Extração de dados
3. **`02_Transform.ipynb`** - Transformação e enriquecimento
4. **`03_Regressao.ipynb`** - Modelagem preditiva
5. **`04_Load.ipynb`** - Geração de modelos de dados

#### Execução via Scripts Python

##### Linux (Recomendado)
```bash
# Executar pipeline ETL completo usando o script shell
bash scripts/executar.sh

# Limpar projeto (remover outputs gerados)
python scripts/reset_project.py
```

##### Windows / macOS / Outros
```bash
# Executar pipeline ETL completo
python scripts/main.py

# Limpar projeto (remover outputs gerados)
python scripts/reset_project.py
```

##  Pipeline ETL

### 1. Extração (`src/extract.py` / `notebooks/01_Extract.ipynb`)
- Lê `data/input/Exportacoes_reduzidos.csv` com dados de exportação 2025
- Colunas: CO_ANO, CO_MES, CO_NCM, CO_UNID, CO_PAIS, SG_UF_NCM, CO_VIA, CO_URF, QT_ESTAT, KG_LIQUIDO, VL_FOB, flag

### 2. Transformação (`src/map.py` / `notebooks/02_Transform.ipynb`)
- **Detectar valores vazios**: Preenche com zeros
- **Expandir estados**: Merge com dicionário de UF
- **Expandir países**: Merge com dicionário de países
- **Expandir URFs**: Merge com dicionário de unidades de despacho
- **Expandir produtos NCM**: Merge com dicionário de produtos
- **Filtrar dados**: Remove registros com flag=0 (inválidos)

### 3. Análise Preditiva (`src/regressao.py` / `notebooks/03_Regressao.ipynb`)
- **Modelo**: Regressão Linear com One-Hot Encoding para variáveis categóricas
- **Features**: CO_ANO, CO_MES, CO_NCM, CO_UNID, CO_PAIS, SG_UF_NCM, CO_VIA, CO_URF, QT_ESTAT, KG_LIQUIDO
- **Target**: VL_FOB (valor FOB da exportação)
- **Métricas**: MSE, MAE, RMSE, R² Score
- **Saída**: Gráfico 2x2 com previsões vs reais, resíduos, histograma e painel de métricas

### 4. Carga/Modelagem (`src/load.py` / `notebooks/04_Load.ipynb`)
- Gera modelo conceitual HTML com diagrama ER (Mermaid.js)
- Gera script SQL MySQL com Star Schema:
  - Dimensões: tempo, produto, país, estado, via, URF
  - Fato: tabela de exportações
- Gera arquivo CSV final processado

##  Arquivos Gerados

| Arquivo | Descrição |
|---------|-----------|
| `data/output/dados_finais.csv` | Dataset completo enriquecido |
| `data/output/modelo_conceitual.html` | Diagrama ER interativo (abra no navegador) |
| `data/output/comexstat_mysql_schema.sql` | Script SQL para criar banco MySQL |
| `data/output/grafico_previsao_completo.png` | Visualização da análise de regressão |

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
- **jupyter**: Ambiente de desenvolvimento interativo

##  Estrutura do Código

### Módulos Python (`src/`)
- **extract.py**: `ler_dados_csv()`, `baixar_csv()`
- **map.py**: `detectar_valores_vazios()`, `expandir_dados()`
- **regressao.py**: `aplicar_regressao_completa()` - modelo ML
- **load.py**: `carregar_dados_banco()`, `gerar_sql_mysql_star_schema()`, `gerar_html_modelo_conceitual()`, `executar_load_completo()`
- **validate.py**: Funções de validação de dados

### Scripts Principais (`scripts/`)
- **main.py**: Executa pipeline ETL completo
- **reset_project.py**: Limpa outputs e cache
- **executar.sh**: Script shell para execução facilitada

### Jupyter Notebooks (`notebooks/`)
- **00_Introducao.ipynb**: Visão geral e configuração
- **01_Extract.ipynb**: Extração de dados
- **02_Transform.ipynb**: Transformação e enriquecimento
- **03_Regressao.ipynb**: Modelagem preditiva
- **04_Load.ipynb**: Geração de modelos de dados

##  Estrutura do Projeto

Para uma visualização detalhada da estrutura de diretórios e arquivos do projeto, consulte o documento de estrutura completa em [`docs/Estrutura-do-Projeto.md`](./docs/Estrutura-do-Projeto.md).

**Resumo dos principais diretórios:**
- `data/`: Dados do projeto (input, output, dicionários)
- `notebooks/`: Jupyter Notebooks para execução interativa
- `scripts/`: Scripts Python principais
- `src/`: Código fonte (módulos Python)
- `docs/`: Documentação detalhada do projeto

##  Documentação

📚 A documentação completa está disponível na pasta [`docs/`](./docs/):

- **[Home](./docs/Home.md)** - Visão geral do projeto
- **[Estrutura do Projeto](./docs/Estrutura-do-Projeto.md)** - Estrutura completa de diretórios e arquivos
- **[Arquitetura ETL](./docs/Arquitetura-ETL.md)** - Pipeline detalhado
- **[Modelo de Dados](./docs/Modelo-de-Dados.md)** - Star Schema
- **[Guia de Uso](./docs/Guia-de-Uso.md)** - Como executar
- **[API e Módulos](./docs/API-e-Modulos.md)** - Documentação técnica

---

##  Repositório Base

Este projeto foi desenvolvido com base no trabalho de **[Pedro Tuto](https://github.com/Pedro-Tuto)** - [ETL-Comexstat-export-2024](https://github.com/Pedro-Tuto/ETL-Comexstat-export-2024).

---

##  Informações Acadêmicas

| | |
|:---|:---|
| **Disciplina** | Business Intelligence e Data Warehouse |
| **Professor** | Rodrigo Gonçalves Pinto |
| **Instituição** | IESB - Instituto de Educação Superior de Brasília |
| **Campus** | Ceilândia - DF |
| **Aluno** | Luis Henrique Costa |
| **RA** | 24114290041 |
| **Curso** | ADS - Análise e Desenvolvimento de Sistemas |

---

**Desenvolvido para:** Análise de comércio exterior brasileiro - Dados COMEX Stat 2025