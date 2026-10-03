import pandas as pd

def detectar_registros_duplicados(datos):
    resultados = {}

    columnas_comparacion = [
        "Nombre",
        "Email",
        "Telefono",
        "Ciudad",
        "Fecha_Registro"
    ]

    columnas_disponibles = [
        columna
        for columna in columnas_comparacion
        if columna in datos.columns
    ]

    if not columnas_disponibles:
        return resultados

    duplicados = datos.duplicated(
        subset=columnas_disponibles,
        keep=False
    )

    filas_duplicadas = datos.index[duplicados].tolist()

    if filas_duplicadas:
        grupos_duplicados = datos[
            duplicados
        ].groupby(
            columnas_disponibles,
            dropna=False
        ).groups

        resultados["registros"] = {
            "cantidad_hallazgos": len(grupos_duplicados),
            "unidad_hallazgo": "grupo",
            "cantidad_afectados": len(filas_duplicadas),
            "unidad_afectada": "fila",
            "filas": filas_duplicadas
        }

    return resultados



def detectar_ids_duplicados(datos):
    resultados = {}

    if "ID" not in datos.columns:
        return resultados

    ids = datos["ID"].dropna()

    conteo = ids.value_counts()
    duplicados = conteo[conteo > 1]

    if not duplicados.empty:
        resultados["ID"] = {
            "cantidad_hallazgos": int(len(duplicados)),
            "unidad_hallazgo": "valor",
            "cantidad_afectados": int(duplicados.sum()),
            "unidad_afectada": "registro",
            "valores": duplicados.to_dict()
        }

    return resultados

def detectar_tipos_incompatibles(datos):
    resultados = {}

    if "ID" in datos.columns:
        ids_invalidos = (
            datos["ID"].notna()
            & ~datos["ID"].apply(
                lambda valor: isinstance(valor, int)
            )
        )

        filas = datos.index[ids_invalidos].tolist()

        if filas:
            resultados["ID"] = {
                "cantidad_hallazgos": len(filas),
                "unidad_hallazgo": "valor",
                "cantidad_afectados": len(filas),
                "unidad_afectada": "registro",
                "filas": filas
            }

    if "Fecha_Registro" in datos.columns:
        fechas = datos["Fecha_Registro"].dropna()

        fechas_invalidas = fechas.apply(
            lambda valor: pd.isna(
                pd.to_datetime(valor, errors="coerce")
            )
        )

        filas = fechas.index[fechas_invalidas].tolist()

        if filas:
            resultados["Fecha_Registro"] = {
                "cantidad_hallazgos": len(filas),
                "unidad_hallazgo": "valor",
                "cantidad_afectados": len(filas),
                "unidad_afectada": "registro",
                "filas": filas
            }

    return resultados


