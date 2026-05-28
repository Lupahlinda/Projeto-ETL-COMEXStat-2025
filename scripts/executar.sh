#!/bin/bash
# Script para facilitar a execução do projeto ETL COMEXStat

echo "=== ETL COMEXStat - Script de Execução ==="
echo ""

# Voltar ao diretório raiz do projeto
cd "$(dirname "$0")/.."

# Ativar o ambiente virtual
if [ -d "venv_linux" ]; then
    echo "Ativando ambiente virtual venv_linux..."
    source venv_linux/bin/activate
elif [ -d "venv" ]; then
    echo "Ativando ambiente virtual venv..."
    source venv/bin/activate
else
    echo "Erro: Nenhum ambiente virtual encontrado."
    echo "Crie um ambiente virtual com: python3 -m venv venv_linux"
    echo "Depois instale as dependências: pip install -r requirements.txt"
    exit 1
fi

# Executar o script principal
echo ""
echo "Executando o script principal..."
python scripts/main.py

echo ""
echo "=== Execução concluída ==="
echo "Arquivos gerados:"
echo "  - data/output/dados_finais.csv"
echo "  - data/output/modelo_conceitual.html"
echo "  - data/output/comexstat_mysql_schema.sql"
echo "  - data/output/grafico_previsao_completo.png"