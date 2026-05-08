import pandas as pd


def test_validate_data(data: pd.DataFrame, validation_data: pd.DataFrame):

    print("Verificando integridade dos dados com os totais para validação.")

    year = 2025

    bulk_year_lines_total = data.query(f"CO_ANO == {year}").copy().shape[0]
    valid_year_lines_total = (validation_data.query(f"CO_ANO == {year}").copy()["NUMERO_LINHAS"].values[0])

    assert (bulk_year_lines_total == valid_year_lines_total), f"Inconsistência no ano {year} - Número de linhas não corresponde"

    bulk_year_vlfob_total = (data.query(f"CO_ANO == {year}").copy()["VL_FOB"].sum())
    valid_year_vlfob_total = (validation_data.query(f"CO_ANO == {year}").copy()["VL_FOB"].values[0])

    assert (bulk_year_vlfob_total == valid_year_vlfob_total), f"Inconsistência no ano {year} - Valor FOB não corresponde"

    bulk_year_kgliquido_total = (data.query(f"CO_ANO == {year}").copy()["KG_LIQUIDO"].sum())
    valid_year_kgliquido_total = (validation_data.query(f"CO_ANO == {year}").copy()["KG_LIQUIDO"].values[0])

    assert (bulk_year_kgliquido_total == valid_year_kgliquido_total), f"Inconsistência no ano {year} - Peso liquido não corresponde"

    print("Validado.")
