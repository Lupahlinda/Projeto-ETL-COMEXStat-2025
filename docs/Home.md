# Projeto ETL COMEX Stat 2025 - Wiki

Bem-vindo à documentação do projeto ETL para análise de dados de exportação brasileira!

## Visão Geral

Este projeto implementa um pipeline completo de **Extração, Transformação e Carga (ETL)** de dados do [COMEX Stat](http://www.mdic.gov.br/balanca/bd/comexstat-bd), o sistema oficial de estatísticas de comércio exterior do Brasil.

O projeto foi desenvolvido como trabalho acadêmico da disciplina de Business Intelligence e Data Warehouse, aplicando conceitos modernos de engenharia de dados e machine learning.

## Funcionalidades Principais

- **Extração**: Leitura de dados CSV de exportações 2025
- **Transformação**: Enriquecimento via dicionários (países, estados, produtos NCM)
- **Análise Preditiva**: Regressão linear para previsão de valores FOB
- **Modelagem**: Geração de modelo dimensional Star Schema para banco de dados MySQL
- **Execução Interativa**: Suporte completo via Jupyter Notebooks

## Métodos de Execução

O projeto oferece duas formas de execução:

### 🎓 Via Jupyter Notebooks (Recomendado)
Execução interativa ideal para análise exploratória e debugging:
- Notebooks organizados por etapa do pipeline
- Visualização integrada de resultados
- Execução célula por célula
- Ideal para aprendizado e experimentação

### ⚙️ Via Scripts Python
Execução automatizada para produção:
- Scripts principais no diretório `scripts/`
- Execução completa em um único comando
- Ideal para automação e integração contínua

## Navegação Rápida

| Página | Descrição |
|--------|-----------|
| [Estrutura do Projeto](Estrutura-do-Projeto) | Estrutura completa de diretórios e arquivos |
| [Arquitetura ETL](Arquitetura-ETL) | Fluxo completo do pipeline ETL |
| [Modelo de Dados](Modelo-de-Dados) | Star Schema e diagrama ER |
| [Guia de Uso](Guia-de-Uso) | Como executar o projeto |
| [API e Módulos](API-e-Modulos) | Documentação dos módulos Python |

## Tecnologias

- **Python 3.8+**
- **pandas** - Manipulação de dados
- **scikit-learn** - Machine learning (regressão linear)
- **matplotlib** - Visualização de dados
- **Jupyter Notebook** - Ambiente de desenvolvimento interativo
- **MySQL** - Banco de dados relacional (modelo dimensional)

## Estrutura do Projeto

O projeto segue uma estrutura organizada e modular:

```
Projeto-ETL-COMEXStat-2025/
├── data/              # Dados do projeto
│   ├── input/        # Arquivos de entrada
│   ├── output/       # Arquivos gerados
│   └── dictionaries/ # Dicionários de dados
├── notebooks/        # Jupyter Notebooks
├── scripts/          # Scripts Python principais
├── src/              # Código fonte (módulos)
└── docs/             # Documentação detalhada
```

Para a estrutura completa, consulte o documento [Estrutura do Projeto](Estrutura-do-Projeto).

## Destaques da Versão Atual

### ✨ Novidades (2026)
- **Jupyter Notebooks**: 5 notebooks interativos para execução passo a passo
- **Estrutura Reorganizada**: Diretórios organizados por função
- **Documentação Expandida**: Nova seção de estrutura do projeto
- **Execução Flexível**: Suporte tanto a notebooks quanto scripts

### 🎯 Características Principais
- Pipeline ETL completo e funcional
- Modelo de machine learning integrado
- Documentação abrangente
- Código modular e reutilizável
- Suporte a múltiplas formas de execução

## Repositório

🔗 [github.com/Lupahlinda/Projeto-ETL-COMEXStat-2025](https://github.com/Lupahlinda/Projeto-ETL-COMEXStat-2025)

---

## Créditos

Este projeto foi desenvolvido com base no trabalho de **[Pedro Tuto](https://github.com/Pedro-Tuto)** - [ETL-Comexstat-export-2024](https://github.com/Pedro-Tuto/ETL-Comexstat-export-2024).

A estrutura inicial e conceitos de ETL foram inspirados nesse repositório base, posteriormente adaptado e expandido para dados de 2025, com adição de notebooks Jupyter e reorganização completa da estrutura.

---

## Informações Acadêmicas

- **Disciplina:** Business Intelligence e Data Warehouse
- **Professor:** Rodrigo Gonçalves Pinto
- **Instituição:** IESB - Instituto de Educação Superior de Brasília (Campus Ceilândia - DF)
- **Aluno:** Luis Henrique Costa (RA: 24114290041)
- **Curso:** ADS - Análise e Desenvolvimento de Sistemas

---

## Começando Rápido

### Instalação
```bash
# Clone o repositório
git clone https://github.com/Lupahlinda/Projeto-ETL-COMEXStat-2025.git
cd Projeto-ETL-COMEXStat-2025

# Instale as dependências
pip install -r requirements.txt
```

### Execução via Jupyter (Recomendado)
```bash
# Instale o Jupyter
pip install jupyter notebook

# Inicie os notebooks
jupyter notebook notebooks/

# Execute em ordem:
# 00_Introducao.ipynb → 01_Extract.ipynb → 02_Transform.ipynb → 
# 03_Regressao.ipynb → 04_Load.ipynb
```

### Execução via Scripts
```bash
# Linux
bash scripts/executar.sh

# Windows/macOS
python scripts/main.py
```

Para instruções detalhadas, consulte o [Guia de Uso](Guia-de-Uso).

---

*Documentação atualizada em 2026*