import pandas as pd

def detectar_formato_fecha(fecha):
    if pd.isna(fecha):
        return "FALTANTE"

    if "-" in fecha:
        return "YYYY-MM-DD"

    partes = fecha.split("/")

    if len(partes[0]) == 4:
        return "YYYY/MM/DD"
    else:
        return "DD/MM/YYYY"

def convertir_fecha(fecha):
    if pd.isna(fecha):
        return fecha

    if "-" in fecha:
        return pd.to_datetime(fecha, format="%Y-%m-%d")

    if "/" in fecha:
        partes = fecha.split("/")

        if len(partes[0]) == 4:
            return pd.to_datetime(fecha, format="%Y/%m/%d")
        else:
            return pd.to_datetime(fecha, format="%d/%m/%Y")