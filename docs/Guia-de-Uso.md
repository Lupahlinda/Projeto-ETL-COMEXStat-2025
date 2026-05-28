# Guia de Uso

Este guia fornece instruções passo a passo para executar o pipeline ETL, configurar o banco de dados MySQL e conectar ao Power BI Desktop.

---

## Pré-requisitos

### Software Necessário
- **Python 3.8+** - Para executar o pipeline ETL
- **MySQL Server** - Banco de dados relacional (opcional)
- **MySQL Workbench** - Interface gráfica para gerenciar o MySQL (opcional)
- **Power BI Desktop** - Ferramenta de BI para visualização de dados (opcional)
- **Jupyter Notebook** - Para execução interativa (recomendado)

### Bibliotecas Python
```bash
pip install -r requirements.txt
```

Para execução via Jupyter Notebooks:
```bash
pip install jupyter notebook
# ou
pip install jupyterlab
```

Dependências principais:
- pandas
- requests
- scikit-learn
- matplotlib
- numpy

---

## Execução do Pipeline ETL

O projeto oferece **duas formas** de execução:

### 🎓 Via Jupyter Notebooks (Recomendado)

Ideal para análise exploratória, debugging e aprendizado.

#### Instalação do Jupyter
```bash
pip install jupyter notebook
```

#### Iniciar os Notebooks
```bash
# Navegar para o diretório raiz do projeto
cd Projeto-ETL-COMEXStat-2025

# Iniciar Jupyter Notebook na pasta notebooks/
jupyter notebook notebooks/

# Ou JupyterLab (interface mais moderna)
jupyter lab notebooks/
```

#### Sequência de Execução
Execute os notebooks **em ordem sequencial**:

1. **`00_Introducao.ipynb`** 
   - Configuração inicial do ambiente
   - Verificação da estrutura do projeto
   - Importação de bibliotecas

2. **`01_Extract.ipynb`**
   - Carregamento de dados brutos
   - Análise exploratória inicial
   - Salvamento para próxima etapa

3. **`02_Transform.ipynb`**
   - Detecção de valores vazios
   - Expansão com dicionários
   - Enriquecimento dos dados

4. **`03_Regressao.ipynb`**
   - Aplicação de modelo de regressão
   - Avaliação de métricas
   - Geração de visualizações

5. **`04_Load.ipynb`**
   - Geração de script SQL
   - Criação de documentação HTML
   - Finalização do pipeline

### ⚙️ Via Scripts Python

Ideal para automação e execução em produção.

#### Linux
```bash
# Executar pipeline completo
bash scripts/executar.sh

# Limpar projeto
python scripts/reset_project.py
```

#### Windows / macOS / Outros
```bash
# Executar pipeline completo
python scripts/main.py

# Limpar projeto
python scripts/reset_project.py
```

---

## Arquivos Gerados

Após a execução do pipeline, os seguintes arquivos serão criados na pasta `data/output/`:

| Arquivo | Descrição |
|---------|-----------|
| `dados_carregados.csv` | Dados brutos após extração |
| `dados_transformados.csv` | Dados após transformação |
| `dados_com_previsoes.csv` | Dados com previsões do modelo |
| `dados_finais.csv` | Dataset completo processado |
| `modelo_conceitual.html` | Diagrama ER interativo (Mermaid.js) |
| `comexstat_mysql_schema.sql` | Script SQL para criar banco MySQL |
| `grafico_previsao_completo.png` | Visualização da análise de regressão |

---

## Configuração do Banco de Dados MySQL (Opcional)

### Passo 1: Iniciar o MySQL Server

1. Abra o **MySQL Workbench**
2. Conecte-se ao seu servidor MySQL local ou remoto
3. Certifique-se de que o servidor está rodando

### Passo 2: Executar o Script SQL

1. No MySQL Workbench, clique em **File** → **Run SQL Script...**
2. Navegue até a pasta `data/output/` do projeto
3. Selecione o arquivo `comexstat_mysql_schema.sql`
4. Clique em **Run** para executar o script

O script irá:
- Criar o banco de dados `comexstat_db`
- Criar as tabelas de dimensão (dim_tempo, dim_ncm, dim_pais, etc.)
- Criar a tabela fato (fato_exportacao)
- Inserir os dados processados
- Criar índices para performance

### Passo 3: Verificar a Criação

Após a execução, verifique se as tabelas foram criadas:

```sql
USE comexstat_db;
SHOW TABLES;
```

Você deve ver as seguintes tabelas:
- dim_tempo
- dim_ncm
- dim_pais
- dim_estado
- dim_via
- dim_urf
- dim_unidade
- dim_bloco
- dim_municipio
- fato_exportacao

---

## Conexão com Power BI Desktop (Opcional)

### Passo 1: Criar Novo Relatório

1. Abra o **Power BI Desktop**
2. Clique em **Novo Relatório** em branco
3. A interface do Power BI será aberta

### Passo 2: Obter Dados do MySQL

1. Clique na guia **Página Inicial** → **Obter Dados**
2. Selecione **Banco de Dados** → **MySQL**
3. A janela de conexão MySQL será aberta

### Passo 3: Configurar a Conexão

Preencha os campos:

| Campo | Valor |
|-------|-------|
| **Servidor** | Nome do seu servidor MySQL (ex: `localhost` ou endereço IP) |
| **Banco de Dados** | `comexstat_db` |
| **Nome de Usuário** | Seu usuário MySQL (ex: `root`) |
| **Senha** | Sua senha MySQL |

### Passo 4: Selecionar os Dados

1. Clique em **Conectar**
2. O Power BI irá carregar as tabelas disponíveis
3. Selecione as tabelas desejadas:
   - `fato_exportacao` (tabela fato principal)
   - `dim_*` (tabelas de dimensão)
4. Clique em **Carregar**

### Passo 5: Criar Visualizações

Agora você pode criar dashboards usando os dados:

**KPIs Sugeridos:**
- Total de Exportações (VL_FOB)
- Peso Total (KG_LIQUIDO)
- Número de Transações
- Top 10 Países
- Top 10 Produtos

**Gráficos Sugeridos:**
- Gráfico de barras: Exportações por País
- Gráfico de linha: Evolução temporal das exportações
- Mapa: Distribuição geográfica das exportações
- Gráfico de pizza: Distribuição por categoria de produto

---

## Solução de Problemas

### Erro: Arquivo não encontrado

**Problema:** `FileNotFoundError: Arquivo não encontrado: data/input/Exportacoes_reduzidos.csv`

**Solução:**
- Verifique se o arquivo existe na pasta `data/input/`
- Certifique-se de que os arquivos de entrada estão presentes
- Execute o notebook `00_Introducao.ipynb` para verificar a estrutura

### Erro: Módulo não encontrado

**Problema:** `ModuleNotFoundError: No module named 'src'`

**Solução:**
- Execute os notebooks a partir do diretório `notebooks/`
- Ou execute o script usando `python scripts/main.py` do diretório raiz

### Erro: Conexão MySQL falhou

**Problema:** Não foi possível conectar ao servidor MySQL

**Solução:**
- Verifique se o MySQL Server está rodando
- Confirme as credenciais (usuário e senha)
- Teste a conexão no MySQL Workbench antes de usar no Power BI

### Erro: Power BI não conecta ao MySQL

**Problema:** O Power BI não consegue conectar ao MySQL

**Solução:**
- Instale o driver MySQL para Windows (MySQL Connector/ODBC)
- Verifique se o firewall não está bloqueando a conexão
- Use `localhost` ou o IP correto do servidor

---

## Estrutura de Diretórios (Resumida)

Para a estrutura completa, consulte [Estrutura do Projeto](Estrutura-do-Projeto.md).

```
Projeto-ETL-COMEXStat-2025/
├── data/                  # Dados do projeto
│   ├── input/           # Arquivos CSV de entrada
│   ├── output/          # Arquivos gerados pelo ETL
│   └── dictionaries/    # Dicionários de dados
├── notebooks/           # Jupyter Notebooks
├── scripts/             # Scripts Python principais
├── src/                 # Código fonte Python
├── docs/                # Documentação
└── requirements.txt     # Dependências Python
```

---

## Dicas de Uso

### Para Aprendizado
- Use os **Jupyter Notebooks** para entender cada etapa
- Execute célula por célula para ver os resultados intermediários
- Modifique parâmetros e observe os impactos

### Para Produção
- Use os **scripts Python** para execução automatizada
- Implemente agendamento (cron job, Windows Task Scheduler)
- Monitore logs e resultados

### Para Análise
- Abra `data/output/modelo_conceitual.html` no navegador
- Visualize o gráfico de regressão gerado
- Explore o dataset final em `data/output/dados_finais.csv`

---

## Suporte

Para mais informações, consulte:
- [Estrutura do Projeto](./Estrutura-do-Projeto.md) - Estrutura completa de diretórios
- [Modelo de Dados](./Modelo-de-Dados.md) - Star Schema detalhado
- [Arquitetura do Pipeline ETL](./Arquitetura-ETL.md) - Fluxo detalhado
- [API e Módulos Python](./API-e-Modulos.md) - Documentação técnica
- [Home](./Home.md) - Visão geral do projeto