import pandas as pd
import os
import requests

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
    Usa dados locais de exportações.
    
    Args:
        filename: Nome do arquivo (mantido para compatibilidade, não usado)
    
    Returns:
        str: Caminho do arquivo local utilizado
    """
    print("Usando dados locais (input/Exportacoes_reduzidos.csv)")
    arquivo_local = "input/Exportacoes_reduzidos.csv"
    if not os.path.exists(arquivo_local):
        raise FileNotFoundError(f"Arquivo não encontrado: {arquivo_local}")
    print(f"   Arquivo encontrado: {os.path.getsize(arquivo_local)/(1024*1024):.2f} MB")
    return arquivo_local

def baixar_totais_validacao(url, filename):
    """
    Usa dados de validação locais.
    
    Args:
        url: URL do arquivo (mantido para compatibilidade, não usado)
        filename: Nome do arquivo (mantido para compatibilidade, não usado)
    """
    print("Usando dados de validação locais.")
