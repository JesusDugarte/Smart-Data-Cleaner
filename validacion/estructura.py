def validar_estructura(datos, estructura_objetivo):
    columnas_resultantes = datos.columns.tolist()

    columnas_faltantes = [
        columna
        for columna in estructura_objetivo
        if columna not in columnas_resultantes
    ]

    columnas_adicionales = [
        columna
        for columna in columnas_resultantes
        if columna not in estructura_objetivo
    ]

    orden_correcto = (
        columnas_resultantes == estructura_objetivo
    )

    estructura_valida = (
        not columnas_faltantes
        and not columnas_adicionales
        and orden_correcto
    )

    return {
        "valida": estructura_valida,
        "columnas_faltantes": columnas_faltantes,
        "columnas_adicionales": columnas_adicionales,
        "orden_correcto": orden_correcto
    }