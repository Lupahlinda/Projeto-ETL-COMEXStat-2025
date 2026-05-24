#!/bin/bash
# Script para facilitar a execução do projeto ETL COMEXStat

echo "=== ETL COMEXStat - Script de Execução ==="
echo ""

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
python main.py

echo ""
echo "=== Execução concluída ==="
echo "Arquivos gerados:"
echo "  - output/dados_finais.csv"
echo "  - output/modelo_conceitual.html"
echo "  - output/comexstat_mysql_schema.sql"
echo "  - output/grafico_previsao_completo.png"
