def validar_correccion(antes, despues):
    resultado = {
        "antes": antes,
        "despues": despues,
        "corregidos": antes - despues,
        "pendientes": despues
    }

    if despues == 0:
        resultado["estado"] = "CORREGIDO"
    else:
        resultado["estado"] = "PENDIENTE"

    return resultado

def validar_fechas(
    faltantes_antes,
    faltantes_despues,
    tipo_dato,
    formatos_antes,
    fechas_presentes_antes
):
    resultado = {
        "formatos_antes": formatos_antes,
        "faltantes_antes": faltantes_antes,
        "faltantes_despues": faltantes_despues,
        "fechas_presentes_antes": fechas_presentes_antes,
        "tipo_dato": str(tipo_dato)
    }

    if str(tipo_dato) == "datetime64[ns]" and faltantes_despues == 0:
        resultado["estado"] = "CORREGIDO"
    elif str(tipo_dato) == "datetime64[ns]":
        resultado["estado"] = "CORREGIDO_CON_PENDIENTES"
    else:
        resultado["estado"] = "PENDIENTE"

    return resultado
