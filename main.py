from src.extract import baixar_csv, baixar_totais_validacao, ler_dados_csv
from src.map import detectar_valores_vazios, expandir_dados
from src.regressao import aplicar_regressao_completa
from src.load import executar_load_completo

URL_BASE = "https://balanca.economia.gov.br/balanca/bd/comexstat-bd/ncm/EXP_2025.csv"
URL_VALIDACAO = "https://balanca.economia.gov.br/balanca/bd/comexstat-bd/ncm/EXP_TOTAIS_CONFERENCIA.csv"

# Configuração: True = dados locais (padrão), False = baixar do COMEX Stat
USAR_DADOS_LOCAIS = True

baixar_csv(URL_BASE, "EXP_2025.csv", usar_dados_locais=USAR_DADOS_LOCAIS)
baixar_totais_validacao(URL_VALIDACAO, "2025_validation.csv", usar_dados_locais=USAR_DADOS_LOCAIS)

df = ler_dados_csv(r"input\Exportacoes_reduzidos.csv")
print(f"Dados carregados: {len(df)} registros")

df = detectar_valores_vazios(df)
df = expandir_dados(df)

resultado = aplicar_regressao_completa(df)

print("Consolidando arquivo final.")
df.to_csv(r"output\dados_finais.csv", index=False)

print("\n=== FASE LOAD ===")
executar_load_completo(df, r"output\dados_finais.csv")
