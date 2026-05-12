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

def baixar_csv(url, filename, usar_dados_locais=True):
    """
    Baixa dados do COMEX Stat ou usa dados locais.
    
    Args:
        url: URL do arquivo para download (se usar_dados_locais=False)
        filename: Nome do arquivo para salvar
        usar_dados_locais: Se True, usa dados locais em input/. Se False, baixa da URL.
    
    Returns:
        str: Caminho do arquivo utilizado
    """
    if usar_dados_locais:
        print("Usando dados locais (input/Exportacoes_reduzidos.csv)")
        arquivo_local = "input/Exportacoes_reduzidos.csv"
        if not os.path.exists(arquivo_local):
            raise FileNotFoundError(f"Arquivo não encontrado: {arquivo_local}")
        print(f"   Arquivo encontrado: {os.path.getsize(arquivo_local)/(1024*1024):.2f} MB")
        return arquivo_local
    else:
        print(f"Baixando dados de {url}...")
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"   Download concluído: {filename}")
            print(f"   Tamanho: {os.path.getsize(filename)/(1024*1024):.2f} MB")
            return filename
        except Exception as e:
            print(f"   Erro ao baixar: {e}")
            raise

def baixar_totais_validacao(url, filename, usar_dados_locais=True):
    """
    Baixa totais de validação ou usa dados locais.
    
    Args:
        url: URL do arquivo para download (se usar_dados_locais=False)
        filename: Nome do arquivo para salvar
        usar_dados_locais: Se True, usa dados locais. Se False, baixa da URL.
    """
    if usar_dados_locais:
        print("Usando dados de validação locais.")
    else:
        print(f"Baixando totais de validação de {url}...")
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"   Download concluído: {filename}")
        except Exception as e:
            print(f"   Erro ao baixar: {e}")
            raise
