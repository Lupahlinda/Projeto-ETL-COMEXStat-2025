import sys
import os

# Adicionar diretório raiz ao path para importar módulos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.extract import baixar_csv, baixar_totais_validacao, ler_dados_csv
from src.map import detectar_valores_vazios, expandir_dados
from src.regressao import aplicar_regressao_completa
from src.load import executar_load_completo

def solicitar_confirmacao(explicacao):
    """Solicita confirmação do usuário antes de prosseguir."""
    print("\n" + "="*60)
    print(explicacao)
    print("="*60)
    resposta = input("Deseja prosseguir? (s/n): ").lower().strip()
    return resposta == 's' or resposta == 'sim'

print("="*60)
print("PIPELINE ETL - COMEX Stat 2025")
print("="*60)
print("\nEste pipeline irá processar dados de exportação brasileira")
print("e gerar modelos de dados, o modelo em SQL para banco de dados.")
print("e o modelo em HTML para visualização (opcional).")
print("\nEtapas do processo:")
print("1. Carregamento de dados locais")
print("2. Mapeamento e expansão de dados")
print("3. Aplicação de regressão linear")
print("4. Geração de modelos de dados (SQL e HTML)")

# Etapa 1: Carregamento de dados locais
if solicitar_confirmacao("\nETAPA 1: CARREGAMENTO DE DADOS LOCAIS\n\nEsta etapa irá carregar os dados de exportações do arquivo local.\nOs dados contêm informações sobre exportações brasileiras por NCM, país, estado, etc."):
    baixar_csv(None, None)
    baixar_totais_validacao(None, None)
else:
    print("Processo cancelado pelo usuário.")
    exit()

# Etapa 2: Carregamento e processamento inicial
if solicitar_confirmacao("\nETAPA 2: CARREGAMENTO E PROCESSAMENTO INICIAL\n\nEsta etapa irá carregar o arquivo CSV de exportações, detectar valores vazios e expandir os dados para formato normalizado."):
    df = ler_dados_csv("data/input/Exportacoes_reduzidos.csv")
    print(f"\nDados carregados: {len(df)} registros")
    
    df = detectar_valores_vazios(df)
    df = expandir_dados(df)
    print(f"\nDados processados: {len(df)} registros")
else:
    print("Processo cancelado pelo usuário.")
    exit()

# Etapa 3: Regressão linear
if solicitar_confirmacao("\nETAPA 3: MODELAGEM PREDITIVA (REGRESSÃO LINEAR)\n\nEsta etapa irá aplicar um modelo de regressão linear para prever valores de exportação.\nSerá gerado um gráfico com as previsões vs valores reais."):
    resultado = aplicar_regressao_completa(df)
    print(f"\nModelo de regressão aplicado com sucesso.")
else:
    print("Processo cancelado pelo usuário.")
    exit()

# Etapa 4: Geração de modelos de dados
if solicitar_confirmacao("\nETAPA 4: GERAÇÃO DE MODELOS DE DADOS\n\nEsta etapa irá gerar:\n- Script SQL com modelo dimensional (Star Schema)\n- HTML com diagramas do modelo lógico e dimensional\n\nAmbos os modelos seguirão fielmente a estrutura definida no WIP.drawio.xml."):
    print("\n=== FASE LOAD ===")
    executar_load_completo(df, None)  # None para não criar dados_finais.csv
else:
    print("Processo cancelado pelo usuário.")
    exit()

print("\n" + "="*60)
print("PROCESSO CONCLUÍDO COM SUCESSO!")
print("="*60)
print("\nArquivos gerados:")
print("  - data/output/modelo_conceitual.html (Modelos Lógico e Dimensional)")
print("  - data/output/comexstat_mysql_schema.sql (Script SQL)")
print("  - data/output/grafico_previsao_completo.png (Gráfico de Regressão)")