import pandas as pd

def detectar_valores_vazios(df: pd.DataFrame) -> pd.DataFrame:
    if df.isna().any().any():
        print("Detectados valores vazios, preenchendo com zeros.")
        df = df.fillna(0)
        return df
    else:
        print("Nenhum valor vazio encontrado.")
        return df
    

def expandir_estados(df: pd.DataFrame, sg_uf_dict_path: str) -> pd.DataFrame:
    print("Expandindo estados.")
    sg_uf_dict = pd.read_csv(sg_uf_dict_path, sep=";")
    df_merged = pd.merge(df, sg_uf_dict, on="SG_UF_NCM", how="left")
    return df_merged


def expandir_paises(df: pd.DataFrame, dict_country_path: str) -> pd.DataFrame:
    print("Expandido países.")
    dict_country = pd.read_csv(dict_country_path, sep=";")
    df_merged = pd.merge(df, dict_country, on="CO_PAIS", how="left")
    return df_merged


def expandir_ncm(df: pd.DataFrame, dict_ncm_path: str) -> pd.DataFrame:
    print("Expandindo produtos NCM.")
    dict_ncm = pd.read_csv(dict_ncm_path, sep=";")
    dict_ncm['CO_NCM'] = pd.to_numeric(dict_ncm['CO_NCM'], errors='coerce')
    dict_ncm = dict_ncm.dropna(subset=['CO_NCM'])
    df_merged = pd.merge(df, dict_ncm, on="CO_NCM", how="left")
    return df_merged


def expandir_urf(df: pd.DataFrame, dict_urf_path: str) -> pd.DataFrame:
    print("Expandido URFs.")
    dict_urf = pd.read_csv(dict_urf_path, sep=";")
    df_merged = pd.merge(df, dict_urf, on="CO_URF", how="left")
    return df_merged

def expandir_dados(df: pd.DataFrame) -> pd.DataFrame:
    df = expandir_estados(df, r"dicionarios/dict_sg_uf.csv")
    df = expandir_paises(df, r"dicionarios/dict_country.csv")
    df = expandir_urf(df, r"dicionarios/dict_urf.csv")
    df = expandir_ncm(df, r"dicionarios/dict_ncm_product.csv")
    # Remove a coluna flag se existir, sem filtrar registros
    if "flag" in df.columns:
        df = df.drop(columns=["flag"])
    print(f"Dados processados: {len(df)} registros")
    return df



