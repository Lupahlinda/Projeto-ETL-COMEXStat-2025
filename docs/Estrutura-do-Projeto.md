# Estrutura do Projeto

Documento detalhado da estrutura de diretórios e arquivos do Projeto ETL - COMEX Stat 2025.

---

## Visão Geral

O projeto segue uma estrutura organizada e modular, separando dados, código, documentação e scripts em diretórios dedicados para facilitar manutenção e escalabilidade.

---

## Estrutura Completa

```
Projeto-ETL-COMEXStat-2025/
├── data/                                    # DADOS DO PROJETO
│   ├── input/                             # Arquivos CSV de entrada (dados fixos)
│   │   ├── Exportacoes_reduzidos.csv     # Dados de exportações 2025
│   │   ├── Importacoes_reduzidos.csv     # Dados de importações 2025
│   │   ├── NCM.csv                       # Tabela de códigos NCM
│   │   ├── NCM_UNIDADE.csv              # Unidades de medida NCM
│   │   ├── PAIS.csv                     # Tabela de países
│   │   ├── PAIS_BLOCO.csv               # Blocos econômicos por país
│   │   ├── UF.csv                       # Tabela de estados (UF)
│   │   ├── UF_MUN.csv                   # Municípios por UF
│   │   ├── URF.csv                      # Unidades de Despacho
│   │   └── VIA.csv                      # Vias de transporte
│   ├── output/                           # Arquivos gerados pelo pipeline
│   │   ├── dados_carregados.csv         # Dados brutos carregados
│   │   ├── dados_transformados.csv      # Dados após transformação
│   │   ├── dados_com_previsoes.csv      # Dados com previsões do modelo
│   │   ├── dados_finais.csv             # Dataset final processado
│   │   ├── modelo_conceitual.html       # Diagrama ER interativo
│   │   ├── comexstat_mysql_schema.sql   # Script SQL MySQL
│   │   └── grafico_previsao_completo.png # Visualização da regressão
│   └── dictionaries/                     # Dicionários de dados para enriquecimento
│       ├── dict_bloco.csv               # Blocos econômicos
│       ├── dict_country.csv             # Países com traduções
│       ├── dict_municipio.csv           # Municípios brasileiros
│       ├── dict_ncm_product.csv         # Produtos NCM com traduções
│       ├── dict_sg_uf.csv               # Estados brasileiros
│       ├── dict_urf.csv                 # Unidades de Despacho
│       └── dict_via.csv                 # Vias de transporte
│
├── notebooks/                             # JUPYTER NOTEBOOKS (Execução Interativa)
│   ├── 00_Introducao.ipynb             # Visão geral e configuração inicial
│   ├── 01_Extract.ipynb                # Extração de dados brutos
│   ├── 02_Transform.ipynb              # Transformação e enriquecimento
│   ├── 03_Regressao.ipynb              # Modelagem preditiva
│   └── 04_Load.ipynb                   # Geração de modelos de dados
│
├── scripts/                               # SCRIPTS PYTHON PRINCIPAIS
│   ├── main.py                          # Executa pipeline ETL completo
│   ├── reset_project.py                 # Limpa outputs e cache
│   └── executar.sh                      # Script shell para execução facilitada
│
├── src/                                   # CÓDIGO FONTE (Módulos Python)
│   ├── extract.py                       # Leitura de dados CSV
│   ├── map.py                           # Transformação e enriquecimento
│   ├── regressao.py                     # Análise preditiva
│   ├── load.py                          # Geração de modelo e SQL
│   ├── reducao.py                       # Redução de dataset
│   └── validate.py                      # Validações de dados
│
├── docs/                                  # DOCUMENTAÇÃO DETALHADA
│   ├── Estrutura-do-Projeto.md         # Este arquivo
│   ├── Home.md                          # Visão geral do projeto
│   ├── Arquitetura-ETL.md              # Pipeline detalhado
│   ├── Modelo-de-Dados.md              # Star Schema
│   ├── Guia-de-Uso.md                   # Como executar
│   └── API-e-Modulos.md                # Documentação técnica
│
├── .vscode/                               # CONFIGURAÇÕES VS CODE
│   └── settings.json                    # Configurações do editor
│
├── venv_linux/                            # AMBIENTE VIRTUAL PYTHON
│   ├── bin/                             # Executáveis Python
│   ├── lib/                             # Bibliotecas instaladas
│   └── ...                              # Outros arquivos do ambiente
│
├── .git/                                  # CONTROLE DE VERSÃO
│   └── ...                              # Arquivos do Git
│
├── requirements.txt                       # DEPENDÊNCIAS PYTHON
├── README.md                              # DOCUMENTAÇÃO PRINCIPAL
├── .gitignore                             # ARQUIVOS IGNORADOS PELO GIT
└── Para-apresentacao.drawio.xml          # DIAGRAMA DRAWIO (Modelo de dados)
```

---

## Descrição Detalhada dos Diretórios

### 📂 `data/` - Dados do Projeto

Contém todos os arquivos de dados utilizados e gerados pelo pipeline ETL.

#### `data/input/` - Dados de Entrada
Arquivos CSV fixos fornecidos como entrada para o pipeline:
- **Exportacoes_reduzidos.csv**: Dados principais de exportação
- **Importacoes_reduzidos.csv**: Dados de importação (futuro uso)
- **NCM.csv**: Tabela de códigos NCM (Nomenclatura Comum do Mercosul)
- **PAIS.csv**: Tabela de países
- **UF.csv**: Tabela de unidades federativas (estados)
- **URF.csv**: Tabela de Unidades de Despacho
- **VIA.csv**: Tabela de vias de transporte

#### `data/output/` - Dados Gerados
Arquivos CSV e outros formatos gerados durante a execução do pipeline:
- **dados_carregados.csv**: Dados brutos após extração
- **dados_transformados.csv**: Dados após transformação
- **dados_com_previsoes.csv**: Dados com previsões do modelo ML
- **dados_finais.csv**: Dataset final completo
- **modelo_conceitual.html**: Diagrama ER interativo
- **comexstat_mysql_schema.sql**: Script SQL para banco de dados
- **grafico_previsao_completo.png**: Visualização da análise de regressão

#### `data/dictionaries/` - Dicionários de Dados
Arquivos CSV utilizados para enriquecimento e normalização dos dados:
- **dict_bloco.csv**: Blocos econômicos (Mercosul, UE, etc.)
- **dict_country.csv**: Países com nomes em português, inglês e espanhol
- **dict_municipio.csv**: Municípios brasileiros
- **dict_ncm_product.csv**: Produtos NCM com descrições multilíngue
- **dict_sg_uf.csv**: Estados brasileiros com regiões
- **dict_urf.csv**: Unidades de Despacho (alfândegas)
- **dict_via.csv**: Vias de transporte (marítima, aérea, etc.)

---

### 📓 `notebooks/` - Jupyter Notebooks

Contém notebooks Jupyter para execução interativa do pipeline ETL, ideal para análise exploratória e debugging.

#### Notebooks Disponíveis

1. **00_Introducao.ipynb**
   - Configuração inicial do ambiente
   - Verificação da estrutura do projeto
   - Importação de bibliotecas principais
   - Configuração de caminhos e diretórios

2. **01_Extract.ipynb**
   - Carregamento de dados brutos
   - Análise exploratória inicial
   - Verificação de integridade dos dados
   - Salvamento de dados para próxima etapa

3. **02_Transform.ipynb**
   - Detecção e tratamento de valores vazios
   - Expansão de dados com dicionários
   - Enriquecimento com informações geográficas
   - Limpeza e normalização

4. **03_Regressao.ipynb**
   - Aplicação de modelo de regressão linear
   - Avaliação de métricas (MSE, MAE, R², RMSE)
   - Geração de visualizações
   - Análise de resíduos

5. **04_Load.ipynb**
   - Geração de script SQL MySQL
   - Criação de documentação HTML
   - Geração de modelos dimensionais
   - Finalização do pipeline

---

### 🔧 `scripts/` - Scripts Python Principais

Scripts executáveis que automatizam a execução do pipeline ETL.

#### Scripts Disponíveis

1. **main.py**
   - Script principal que executa o pipeline completo
   - Orquestra as etapas de Extract, Transform, Regressão e Load
   - Inclui confirmações interativas do usuário
   - Gerencia dependências entre etapas

2. **reset_project.py**
   - Script de limpeza do projeto
   - Remove arquivos gerados durante execução
   - Limpa cache do Python
   - Recria estrutura de diretórios necessária

3. **executar.sh**
   - Script shell para execução facilitada (Linux)
   - Ativa automaticamente o ambiente virtual
   - Executa o pipeline completo
   - Fornece feedback visual do progresso

---

### 🐍 `src/` - Código Fonte

Contém os módulos Python que implementam a lógica do pipeline ETL.

#### Módulos Disponíveis

1. **extract.py**
   - `ler_dados_csv()`: Lê arquivos CSV
   - `baixar_csv()`: Gerencia dados locais
   - `ler_csv_para_validacao()`: Lê dados para validação

2. **map.py**
   - `detectar_valores_vazios()`: Identifica e trata valores nulos
   - `expandir_dados()`: Expande dados com dicionários
   - `expandir_estados()`: Enriquece com dados de estados
   - `expandir_paises()`: Enriquece com dados de países
   - `expandir_ncm()`: Enriquece com dados de produtos
   - `expandir_urf()`: Enriquece com dados de URFs

3. **regressao.py**
   - `aplicar_regressao_completa()`: Aplica modelo de regressão
   - Gera visualizações e métricas
   - Implementa pipeline de machine learning

4. **load.py**
   - `executar_load_completo()`: Orquestra geração de modelos
   - `gerar_sql_mysql_star_schema()`: Gera script SQL
   - `gerar_html_modelo_conceitual()`: Gera documentação HTML
   - `carregar_dados_banco()`: Simula carregamento em banco

5. **validate.py**
   - `test_validate_data()`: Valida integridade dos dados
   - Compara totais com dados de validação
   - Verifica consistência de valores

6. **reducao.py**
   - Script de redução de dataset
   - Aplica amostragem aleatória
   - Mantém representatividade estatística

---

### 📚 `docs/` - Documentação

Contém documentação detalhada do projeto em formato Markdown.

#### Documentos Disponíveis

- **Estrutura-do-Projeto.md**: Este arquivo - estrutura completa
- **Home.md**: Visão geral do projeto
- **Arquitetura-ETL.md**: Detalhes do pipeline ETL
- **Modelo-de-Dados.md**: Especificação do Star Schema
- **Guia-de-Uso.md**: Instruções de execução
- **API-e-Modulos.md**: Documentação técnica das funções

---

### ⚙️ `scripts/` - Scripts de Automação

Scripts executáveis para automação de tarefas comuns.

- **main.py**: Script principal do pipeline
- **reset_project.py**: Limpeza de outputs
- **executar.sh**: Execução facilitada em Linux

---

## Fluxo de Dados na Estrutura

```
data/input/ 
    ↓ [extract.py / 01_Extract.ipynb]
data/output/dados_carregados.csv
    ↓ [map.py / 02_Transform.ipynb]
data/output/dados_transformados.csv
    ↓ [regressao.py / 03_Regressao.ipynb]
data/output/dados_com_previsoes.csv
    ↓ [load.py / 04_Load.ipynb]
data/output/dados_finais.csv
data/output/modelo_conceitual.html
data/output/comexstat_mysql_schema.sql
data/output/grafico_previsao_completo.png
```

---

## Boas Práticas de Organização

### 📁 Separar Dados de Código
- `data/`: Contém apenas arquivos de dados
- `src/`: Contém apenas código fonte
- Facilita backup e versionamento

### 📓 Modularização
- Cada módulo em `src/` tem responsabilidade única
- Notebooks separados por etapa do pipeline
- Scripts dedicados para tarefas específicas

### 📚 Documentação Integrada
- Documentação detalhada em `docs/`
- README.md como visão geral rápida
- Comentários no código para detalhes técnicos

### 🔄 Ambiente Virtual Isolado
- `venv_linux/`: Ambiente Python isolado
- Evita conflitos de dependências
- Facilita reprodução de ambiente

---

## Atualizações Recentes

### Reorganização (2026-05-27)
- ✅ Criado diretório `data/` unificado
- ✅ Movido `input/`, `output/`, `dicionarios/` para `data/`
- ✅ Renomeado `dicionarios/` para `dictionaries/`
- ✅ Criado diretório `notebooks/` para Jupyter Notebooks
- ✅ Criado diretório `scripts/` para scripts principais
- ✅ Removidos ambientes virtuais duplicados
- ✅ Atualizado `.gitignore` com nova estrutura
- ✅ Atualizados todos os caminhos nos arquivos

### Migração para Jupyter (2026-05-27)
- ✅ Criados 5 notebooks Jupyter interativos
- ✅ Mantida compatibilidade com scripts Python originais
- ✅ Documentação atualizada com novas opções de execução

---

## Próximas Melhorias Sugeridas

1. **Tests/**: Adicionar diretório para testes unitários
2. **config/**: Separar arquivos de configuração
3. **logs/**: Diretório dedicado para logs de execução
4. **temp/**: Diretório para arquivos temporários
5. **deployment/**: Scripts e configurações para deployment

---

**Última atualização:** 27 de maio de 2026  
**Versão da estrutura:** 2.0 (Reorganização completa)