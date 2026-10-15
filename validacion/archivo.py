import pandas as pd

from pandas.errors import EmptyDataError

def validar_archivo_exportado(
    archivo,
    columnas_esperadas,
    filas_esperadas
):
    if archivo.suffix.lower() not in {".csv", ".xlsx"}:
        return {
            "archivo": archivo.name,
            "estado": "REVISAR",
            "motivo": "Formato de archivo no soportado"
        }

    if not archivo.exists():
        return {
            "archivo": archivo.name,
            "estado": "ERROR",
            "motivo": "ARCHIVO_NO_ENCONTRADO"
        }

    try:
        if archivo.suffix.lower() == ".csv":
            datos_exportados = pd.read_csv(archivo)
        else:
            datos_exportados = pd.read_excel(archivo)

    except EmptyDataError:
        return {
            "archivo": archivo.name,
            "estado": "ERROR",
            "motivo": "ARCHIVO_NO_LEIBLE"
        }

    except (OSError, ValueError, ImportError) as error:
        return {
            "archivo": archivo.name,
            "estado": "ERROR",
            "motivo": "ARCHIVO_NO_LEIBLE"
        }


    filas_obtenidas = len(datos_exportados)
    columnas_obtenidas = len(datos_exportados.columns)

    filas_correctas = (
        filas_obtenidas == filas_esperadas
    )

    columnas_correctas = (
        datos_exportados.columns.tolist()
        == columnas_esperadas
    )

    if filas_correctas and columnas_correctas:
        estado = "VALIDADO"
    else:
        estado = "REVISAR"

    return {
        "archivo": archivo.name,
        "filas": filas_obtenidas,
        "columnas": columnas_obtenidas,
        "filas_correctas": filas_correctas,
        "columnas_correctas": columnas_correctas,
        "estado": estado
    }
