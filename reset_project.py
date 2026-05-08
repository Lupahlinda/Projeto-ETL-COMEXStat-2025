#!/usr/bin/env python3
"""
Script de Limpeza e Reset do Projeto ETL COMEX Stat 2025
================================================================

Este script realiza a limpeza completa do projeto, removendo todos os dados
gerados e preparando o ambiente para uma execução do zero.

Uso: python reset_project.py
"""

import os
import shutil
import glob
from datetime import datetime

def limpar_diretorio(diretorio, preservar=None):
    """Remove todos os arquivos de um diretório, mantendo a estrutura.
    
    Args:
        diretorio: Caminho do diretório a limpar
        preservar: Lista de nomes de arquivos para preservar (não apagar)
    """
    if preservar is None:
        preservar = []
    
    if os.path.exists(diretorio):
        print(f" Limpando diretório: {diretorio}")
        for arquivo in glob.glob(os.path.join(diretorio, '*')):
            nome_arquivo = os.path.basename(arquivo)
            if nome_arquivo in preservar:
                print(f"    Preservado (fixo): {nome_arquivo}")
                continue
            if os.path.isfile(arquivo):
                os.remove(arquivo)
                print(f"    Removido: {nome_arquivo}")
            elif os.path.isdir(arquivo):
                shutil.rmtree(arquivo)
                print(f"    Removido diretório: {nome_arquivo}")
    else:
        print(f" Diretório não encontrado: {diretorio}")

def criar_diretorios_necessarios():
    """Cria os diretórios necessários se não existirem."""
    diretorios = [
        'input',
        'output',
        'dicionarios',
        'src'
    ]
    
    for diretorio in diretorios:
        if not os.path.exists(diretorio):
            os.makedirs(diretorio)
            print(f"    Criado diretório: {diretorio}")

def limpar_arquivos_especificos():
    """Remove arquivos específicos gerados durante a execução."""
    arquivos_para_remover = [
        'log.txt',
        'modelagem_academica.txt',
        'modelagem_academica.md',
        'modelo_conceitual.html',
        'dados_finais.csv',
        'grafico_previsao_CARNES.png',
        'EXP_2025.csv',
        '2025_validation.csv'
    ]
    
    print(" Removendo arquivos específicos:")
    for arquivo in arquivos_para_remover:
        if os.path.exists(arquivo):
            os.remove(arquivo)
            print(f"    Removido: {arquivo}")

def limpar_cache_python():
    """Remove cache do Python."""
    cache_dirs = [
        '__pycache__',
        'src/__pycache__'
    ]
    
    print(" Limpando cache do Python:")
    for cache_dir in cache_dirs:
        if os.path.exists(cache_dir):
            shutil.rmtree(cache_dir)
            print(f"    Removido: {cache_dir}")

def main():
    """Função principal de limpeza do projeto."""
    print("=" * 60)
    print(" INICIANDO LIMPEZA COMPLETA DO PROJETO")
    print("=" * 60)
    print(f" Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print()
    
    # Arquivos fixos a preservar na pasta input
    ARQUIVOS_FIXOS_INPUT = [
        'Exportacoes_reduzidos.csv',
        'Importacoes_reduzidos.csv',
        'NCM.csv',
        'NCM_UNIDADE.csv',
        'PAIS.csv',
        'PAIS_BLOCO.csv',
        'UF.csv',
        'UF_MUN.csv',
        'URF.csv',
        'VIA.csv'
    ]
    
    # 1. Limpar diretórios principais
    print(" ETAPA 1: LIMPANDO DIRETÓRIOS PRINCIPAIS")
    limpar_diretorio('input', preservar=ARQUIVOS_FIXOS_INPUT)
    limpar_diretorio('output')
    print()
    
    # 2. Remover arquivos específicos
    print(" ETAPA 2: REMOVENDO ARQUIVOS ESPECÍFICOS")
    limpar_arquivos_especificos()
    print()
    
    # 3. Limpar cache do Python
    print(" ETAPA 3: LIMPANDO CACHE DO PYTHON")
    limpar_cache_python()
    print()
    
    # 4. Recriar estrutura necessária
    print(" ETAPA 4: RECONSTRUINDO ESTRUTURA")
    criar_diretorios_necessarios()
    print()
    
    # 5. Verificar estado final
    print(" ETAPA 5: VERIFICAÇÃO FINAL")
    
    # Verificar estado dos diretórios
    diretorios_status = {}
    for diretorio in ['input', 'output', 'dicionarios', 'src']:
        if os.path.exists(diretorio):
            arquivos = [f for f in os.listdir(diretorio) if os.path.isfile(os.path.join(diretorio, f))]
            dirs = [d for d in os.listdir(diretorio) if os.path.isdir(os.path.join(diretorio, d))]
            diretorios_status[diretorio] = f"{len(arquivos)} arquivos, {len(dirs)} subdiretórios"
        else:
            diretorios_status[diretorio] = "Não existe"
    
    print(" STATUS FINAL DOS DIRETÓRIOS:")
    for diretorio, status in diretorios_status.items():
        print(f"    {diretorio}/: {status}")
    
    print()
    print("=" * 60)
    print(" LIMPEZA CONCLUÍDA COM SUCESSO!")
    print(" Projeto pronto para execução do zero!")
    print(" Execute: python main.py")
    print("=" * 60)

if __name__ == "__main__":
    main()
