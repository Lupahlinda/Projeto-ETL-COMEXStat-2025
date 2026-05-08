import pandas as pd
import os

def ler_dados_csv(file_path, delimiter=";"):
    """Lê arquivo CSV e retorna DataFrame."""
    df = pd.read_csv(file_path, sep=delimiter)
    return df

def ler_csv_para_validacao(file_path, delimiter=";"):
    """Lê arquivo CSV para validação."""
    df = pd.read_csv(file_path, sep=delimiter)
    return df

def baixar_csv(url, filename):
    """
    Usa arquivo local fixo em vez de baixar.
    Os dados fixos estão em input/Exportacoes_reduzidos.csv
    """
    print("Usando dados de Exportacao locais (Exportacoes_reduzidos.csv).")
    # Verifica se arquivo existe
    arquivo_local = "input/Exportacoes_reduzidos.csv"
    if not os.path.exists(arquivo_local):
        raise FileNotFoundError(f"Arquivo nao encontrado: {arquivo_local}")
    print(f"   Arquivo encontrado: {os.path.getsize(arquivo_local)/(1024*1024):.2f} MB")

def baixar_totais_validacao(url, filename):
    """
    Usa arquivo local fixo em vez de baixar.
    """
    print("Usando dados de validacao locais.")
    # Nao precisa baixar, usa os dados fixos disponiveis
