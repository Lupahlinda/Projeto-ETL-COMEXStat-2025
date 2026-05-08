# Guia de Uso

## Instalação

### Requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes)
- Git

### Passo 1: Clonar o Repositório

```bash
git clone https://github.com/Lupahlinda/Projeto-ETL-COMEXStat-2025.git
cd Projeto-ETL-COMEXStat-2025
```

### Passo 2: Instalar Dependências

```bash
pip install -r requirements.txt
```

**Dependências instaladas:**
- pandas
- scikit-learn
- matplotlib
- numpy

---

## Execução

### Executar Pipeline Completo

```bash
python main.py
```

Este comando executa todo o fluxo ETL:
1. Extração dos dados CSV
2. Transformação e enriquecimento
3. Análise preditiva
4. Geração dos arquivos de saída

### Limpar Projeto

```bash
python reset_project.py
```

Remove todos os arquivos gerados em `output/`, mantendo os dados de entrada em `input/`.

---

## Estrutura de Diretórios

Após a execução, a estrutura será:

```
Projeto-ETL-COMEXStat-2025/
├── input/              # Dados de entrada (não alterar)
│   └── Exportacoes_reduzidos.csv
├── output/             # Arquivos gerados
│   ├── dados_finais.csv
│   ├── modelo_conceitual.html
│   ├── comexstat_mysql_schema.sql
│   └── grafico_previsao_completo.png
└── src/                # Código fonte
```

---

## Arquivos de Saída

### dados_finais.csv

Dataset completo processado, pronto para análise ou importação em banco de dados.

**Colunas principais:**
- Identificadores: CO_ANO, CO_MES, CO_NCM, CO_PAIS, etc.
- Métricas: QT_ESTAT, KG_LIQUIDO, VL_FOB
- Enriquecidas: nm_estado, id_country, id_product, etc.

### modelo_conceitual.html

Visualização interativa do modelo de dados.

**Como visualizar:**
1. Abra o arquivo em qualquer navegador
2. O diagrama ER será renderizado automaticamente
3. Mostra todas as 9 tabelas obrigatórias e seus relacionamentos

### comexstat_mysql_schema.sql

Script SQL completo para criar o banco de dados MySQL.

**Uso:**
```bash
mysql -u root -p < output/comexstat_mysql_schema.sql
```

**Inclui:**
- Criação das 6 tabelas de dimensão
- Criação da tabela fato
- Índices otimizados
- Views para Power BI
- Instruções de integração

### grafico_previsao_completo.png

Visualização dos resultados da regressão linear.

**Contém 4 subplots:**
1. Previsões vs Valores Reais
2. Análise de Resíduos
3. Distribuição dos Resíduos
4. Painel de Métricas (MAE, RMSE, R²)

---

## Configurações Avançadas

### Alterar Produto para Análise

Por padrão, a regressão analisa **todos os produtos**. Para analisar um produto específico, edite `main.py`:

```python
# Antes
resultado = aplicar_regressao_completa(df)

# Depois - exemplo para produto específico
resultado = aplicar_regressao_completa(df, produto="CARNES")
```

### Ajustar Percentual de Treino/Teste

Em `src/regressao.py`, altere o parâmetro `test_size`:

```python
X_train, X_test, y_train, y_test = train_test_split(
    X, y, 
    test_size=0.2,  # 20% para teste, altere aqui
    random_state=42
)
```

### Modificar Features do Modelo

Adicione ou remova features na lista em `regressao.py`:

```python
X = df_analise[[
    'CO_ANO', 'CO_MES', 'CO_NCM', 'CO_UNID',
    'CO_PAIS', 'SG_UF_NCM', 'CO_VIA', 'CO_URF',
    'QT_ESTAT', 'KG_LIQUIDO'
    # Adicione novas colunas aqui
]]
```

---

## Troubleshooting

### Erro: Arquivo não encontrado

**Problema:** `FileNotFoundError: input/Exportacoes_reduzidos.csv`

**Solução:** Verifique se o arquivo existe na pasta `input/`. Os dados de entrada são obrigatórios.

### Erro: Memory Error

**Problema:** Memória insuficiente para processar grandes datasets

**Solução:**
- Feche outros aplicativos
- Processo em chunks (requer modificação no código)
- Aumente a memória disponível

### Gráficos não aparecem

**Problema:** `matplotlib` não está instalado corretamente

**Solução:**
```bash
pip install --upgrade matplotlib
```

### Permissão negada ao criar arquivos

**Problema:** Erro ao salvar em `output/`

**Solução:**
```bash
# Windows - execute como Administrador
# Linux/Mac
chmod +w output/
```

---

## Fluxo de Trabalho Recomendado

1. **Primeira execução:**
   ```bash
   pip install -r requirements.txt
   python main.py
   ```

2. **Verificar resultados:**
   - Abra `output/modelo_conceitual.html` no navegador
   - Verifique `output/dados_finais.csv`

3. **Limpar e reexecutar:**
   ```bash
   python reset_project.py
   python main.py
   ```

4. **Importar no Power BI:**
   - Use o arquivo `output/comexstat_mysql_schema.sql`
   - Siga as instruções no próprio script SQL
