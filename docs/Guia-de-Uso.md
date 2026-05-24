# Guia de Uso

Este guia fornece instruções passo a passo para executar o pipeline ETL, configurar o banco de dados MySQL e conectar ao Power BI Desktop.

---

## Pré-requisitos

### Software Necessário
- **Python 3.8+** - Para executar o pipeline ETL
- **MySQL Server** - Banco de dados relacional
- **MySQL Workbench** - Interface gráfica para gerenciar o MySQL
- **Power BI Desktop** - Ferramenta de BI para visualização de dados

### Bibliotecas Python
```bash
pip install -r requirements.txt
```

Dependências:
- pandas
- requests
- scikit-learn
- matplotlib
- numpy

---

## Execução do Pipeline ETL

### Linux (Recomendado)

Execute o pipeline usando o script shell que ativa automaticamente o ambiente virtual:

```bash
bash executar.sh
```

### Windows / macOS / Outros

Execute o pipeline diretamente com Python:

```bash
python main.py
```

**Nota:** O pipeline usa exclusivamente dados locais do arquivo `input/Exportacoes_reduzidos.csv`. Não há opção de download automático.

---

## Arquivos Gerados

Após a execução do pipeline, os seguintes arquivos serão criados na pasta `output/`:

| Arquivo | Descrição |
|---------|-----------|
| `dados_finais.csv` | Dataset completo processado e enriquecido |
| `modelo_conceitual.html` | Diagrama ER interativo (Mermaid.js) |
| `comexstat_mysql_schema.sql` | Script SQL para criar banco MySQL |
| `grafico_previsao_completo.png` | Visualização da análise de regressão |

---

## Configuração do Banco de Dados MySQL

### Passo 1: Iniciar o MySQL Server

1. Abra o **MySQL Workbench**
2. Conecte-se ao seu servidor MySQL local ou remoto
3. Certifique-se de que o servidor está rodando

### Passo 2: Executar o Script SQL

1. No MySQL Workbench, clique em **File** → **Run SQL Script...**
2. Navegue até a pasta `output/` do projeto
3. Selecione o arquivo `comexstat_mysql_schema.sql`
4. Clique em **Run** para executar o script

O script irá:
- Criar o banco de dados `comexstat_db`
- Criar as tabelas de dimensão (dim_tempo, dim_produto, dim_pais, etc.)
- Criar a tabela fato (fato_exportacao)
- Inserir os dados processados
- Criar views otimizadas para Power BI

### Passo 3: Verificar a Criação

Após a execução, verifique se as tabelas foram criadas:

```sql
USE comexstat_db;
SHOW TABLES;
```

Você deve ver as seguintes tabelas:
- dim_tempo
- dim_produto
- dim_pais
- dim_localidade
- dim_via
- dim_unidade
- fato_exportacao
- v_exportacoes_consolidadas (view)
- v_analise_produto (view)
- v_analise_pais (view)

---

## Conexão com Power BI Desktop

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
3. Selecione as tabelas/views desejadas:
   - `v_exportacoes_consolidadas` (recomendada - view principal)
   - `v_analise_produto` (análise por produto)
   - `v_analise_pais` (análise por país)
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

**Problema:** `FileNotFoundError: Arquivo não encontrado: input/Exportacoes_reduzidos.csv`

**Solução:**
- Verifique se o arquivo existe na pasta `input/`
- O pipeline usa exclusivamente dados locais, certifique-se de que os arquivos de entrada estão presentes

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

## Estrutura de Diretórios

```
Projeto-ETL-COMEXStat-2025/
├── dicionarios/          # Dicionários de dados
├── input/                # Arquivos CSV de entrada
├── output/               # Arquivos gerados pelo ETL
├── src/                  # Código fonte Python
├── docs/                 # Documentação
├── main.py              # Script principal
└── requirements.txt     # Dependências Python
```
## Suporte

Para mais informações, consulte:
- [Documentação do Modelo de Dados](./Modelo-de-Dados.md)
- [Arquitetura do Pipeline ETL](./Arquitetura-ETL.md)
- [API e Módulos Python](./API-e-Modulos.md)
