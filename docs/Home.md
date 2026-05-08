# Projeto ETL COMEX Stat 2025 - Wiki

Bem-vindo à documentação do projeto ETL para análise de dados de exportação brasileira!

## Visão Geral

Este projeto implementa um pipeline completo de **Extração, Transformação e Carga (ETL)** de dados do [COMEX Stat](http://www.mdic.gov.br/balanca/bd/comexstat-bd), o sistema oficial de estatísticas de comércio exterior do Brasil.

## Funcionalidades Principais

- **Extração**: Leitura de dados CSV de exportações 2025
- **Transformação**: Enriquecimento via dicionários (países, estados, produtos NCM)
- **Análise Preditiva**: Regressão linear para previsão de valores FOB
- **Modelagem**: Geração de modelo dimensional Star Schema para banco de dados MySQL

## Navegação Rápida

| Página | Descrição |
|--------|-----------|
| [Arquitetura ETL](Arquitetura-ETL) | Fluxo completo do pipeline ETL |
| [Modelo de Dados](Modelo-de-Dados) | Star Schema e diagrama ER |
| [Guia de Uso](Guia-de-Uso) | Como executar o projeto |
| [API e Módulos](API-e-Modulos) | Documentação dos módulos Python |

## Tecnologias

- **Python 3.8+**
- **pandas** - Manipulação de dados
- **scikit-learn** - Machine learning (regressão)
- **matplotlib** - Visualização

## Repositório

🔗 [github.com/Lupahlinda/Projeto-ETL-COMEXStat-2025](https://github.com/Lupahlinda/Projeto-ETL-COMEXStat-2025)

---

## Créditos

Este projeto foi desenvolvido com base no trabalho de **[Pedro Tuto](https://github.com/Pedro-Tuto)** - [ETL-Comexstat-export-2024](https://github.com/Pedro-Tuto/ETL-Comexstat-export-2024).

A estrutura inicial e conceitos de ETL foram inspirados nesse repositório base, posteriormente adaptado e expandido para dados de 2025.

---

*Documentação atualizada em 2025*
