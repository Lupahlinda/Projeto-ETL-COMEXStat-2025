# Projeto ETL - Análise de Dados de Exportação COMEX Stat 2025

##  Objetivos do Projeto

- **Etapa 1**: Compreensão da base de dados COMEX Stat
- **Etapa 2**: Importação e validação de arquivos CSV
- **Etapa 3**: Processo ETL completo com todas as tabelas obrigatórias

##  Estrutura de Pastas

```
ETL-Comexstat-export-2024/
├── dicionarios/          # Dicionários de dados para expansão
│   ├── dict_bloco.csv      # Blocos econômicos
│   ├── dict_country.csv     # Países
│   ├── dict_municipio.csv   # Municípios brasileiros
│   ├── dict_ncm_product.csv # Produtos NCM
│   ├── dict_sg_uf.csv      # Estados brasileiros
│   ├── dict_urf.csv        # Unidades de Despacho
│   └── dict_via.csv        # Vias de transporte
├── input/                 # Arquivos CSV brutos baixados
├── output/                # Arquivos processados e resultados
│   ├── dados_finais.csv    # Dados transformados
│   ├── modelo_conceitual.html # Modelo de banco de dados
│   └── grafico_previsao_CARNES.png
├── src/                   # Código fonte do projeto
│   ├── extract.py          # Extração de dados
│   ├── load.py            # Carga no banco de dados
│   ├── map.py             # Transformação de dados
│   ├── regressao.py       # Análise preditiva
│   └── validate.py        # Validação de dados
├── main.py               # Script principal de execução
└── requirements.txt       # Dependências do projeto
```

##  Como Rodar o Projeto

### Pré-requisitos
- Python 3.8+
- Ambiente virtual recomendado

### Passos de Instalação

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/Lupahlinda/Projeto-ETL-COMEXStat-2025.git
   cd ETL-Comexstat-export-2024
   ```

2. **Crie e ative o ambiente virtual**:
   
   **Windows**:
   ```bash
   python -m venv venv
   ```
   
   **Linux/Mac**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Execute o projeto**:
   ```bash
   python main.py
   ```

##  Fluxo de Execução Completo

### **Fase 1: EXTRAÇÃO (Extract)**
```
 Baixando dados de Exportação 2025...
   ├── Download: EXP_2025.csv (113MB)
   └── Download: TOTAS_CONFERENCIA.csv
```

### **Fase 2: VALIDAÇÃO**
```
 Verificando integridade dos dados...
   ├── Validação de totais de conferência
   ├── Comparação: número de linhas
   ├── Comparação: valor FOB total
   └── Comparação: peso líquido total
 Validado.
```

### **Fase 3: TRANSFORMAÇÃO (Transform)**
```
 Processando dados...
   ├── Detectando valores vazios: Preenchendo com zeros
   ├── Expandindo estados: 27 estados brasileiros
   ├── Expandindo países: 281 países
   ├── Expandindo URFs: 278 unidades de despacho
   ├── Expandindo produtos NCM: 1.936 produtos únicos
   └── Filtrando agronegócio: 646.707 registros úteis
```

### **Fase 4: ANÁLISE PREDITIVA**
```
 Aplicando modelo de regressão...
   ├── Produto alvo: CARNES
   ├── Features: 10 variáveis preditoras
   ├── Métricas: MSE e MAE
   └── Visualização: gráfico de previsões vs reais
```

### **Fase 5: CARGA (Load)**
```
 Carregando no banco de dados...
   ├── Tabela: exportacao (646.707 registros)
   ├── Tabela: ncm (1.936 produtos)
   ├── Tabela: paises (281 países)
   ├── Tabela: blocos (10 blocos econômicos)
   ├── Tabela: municipios (5 municípios)
   ├── Tabela: estados (27 estados)
   ├── Tabela: via (10 vias de transporte)
   ├── Tabela: urf (278 unidades)
   └── Tabela: importacao (simulada)
```

##  Resultados Finais

### **Estatísticas do Processamento**
- **Registros processados**: 646.707 exportações
- **Países destino**: 281 países diferentes
- **Produtos únicos**: 1.936 códigos NCM
- **Cobertura temporal**: 12 meses de 2025
- **Validação**: 100% aprovada nos totais de conferência

### **Arquivos Gerados**
1. **`output/dados_finais.csv`** - Dataset limpo e transformado
2. **`output/modelo_conceitual.html`** - Modelo conceitual do banco de dados
3. **`output/grafico_previsao_CARNES.png`** - Visualização do modelo preditivo

### **Modelo de Banco de Dados**
O projeto implementa todas as **9 tabelas obrigatórias**:

| Tabela | Descrição | Registros |
|--------|------------|-----------|
| **Importação** | Dados de importação (simulado) | 0 |
| **Exportação** | Dados de exportação brasileira | 646.707 |
| **NCM** | Produtos e classificações | 1.936 |
| **Países** | Países de destino/origem | 281 |
| **Blocos** | Blocos econômicos | 10 |
| **Municípios** | Municípios brasileiros | 5 |
| **Estados** | Estados brasileiros | 27 |
| **Via** | Vias de transporte | 10 |
| **URF** | Unidades de despacho aduaneiro | 278 |

##  Tecnologias Utilizadas

### **Bibliotecas Principais**
- **pandas**: Manipulação e análise de dados
- **requests**: Download de arquivos da web
- **scikit-learn**: Machine learning e regressão
- **matplotlib**: Visualização de dados
- **urllib3**: Tratamento de requisições HTTP

### **Visualização**
- **Mermaid.js**: Diagramas de banco de dados interativos
- **HTML5**: Interface web para modelo conceitual
- **CSS3**: Design responsivo e moderno

##  Conformidade com Requisitos

### **Etapa 1 - Compreensão da Base** 
-  Estrutura COMEX Stat compreendida
-  Relacionamentos entre tabelas mapeados
-  Dicionários de dados implementados

### **Etapa 2 - Importação CSV** 
-  Download automático dos arquivos
-  Verificação de estrutura e encoding
-  Validação de consistência inicial
-  Tratamento de separadores e tipos

### **Etapa 3 - Processo ETL** 
-  **Extract**: Download e leitura implementados
-  **Transform**: Todas as transformações aplicadas
  -  Correção de tipos de dados
  -  Tratamento de valores ausentes
  -  Remoção de inconsistências
  -  Padronização de campos
  -  Organização de chaves e relacionamentos
-  **Load**: Todas as 9 tabelas obrigatórias implementadas

##  Visualização dos Resultados

Após a execução, acesse:
- **Modelo conceitual**: Abra `output/modelo_conceitual.html` no navegador
- **Dados processados**: `output/dados_finais.csv`
- **Análise preditiva**: `output/grafico_previsao_CARNES.png`

##  Solução de Problemas Comuns

### **Erro de Certificado SSL**
- **Problema**: `[SSL: CERTIFICATE_VERIFY_FAILED]`
- **Solução**: Implementado `verify=False` nas requisições HTTP

### **Arquivos de 2025 Não Encontrados**
- **Problema**: Tentativa de acessar dados inexistentes
- **Solução**: Verificação prévia de disponibilidade dos arquivos

### **Conflito de Versões**
- **Solução**: Use sempre ambiente virtual isolado

---

##  Próximos Passos Sugeridos

1. **Implementação real de banco**: MySQL/PostgreSQL
2. **API REST**: Para consumo dos dados processados
3. **Dashboard interativo**: Com filtros dinâmicos
4. **Machine Learning**: Modelos mais sofisticados
5. **Streaming**: Processamento em tempo real

**Desenvolvido para análise de comércio exterior brasileiro - Ano 2025**
