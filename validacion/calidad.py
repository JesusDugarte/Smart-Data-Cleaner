import pandas as pd

from detectores.calidad import (
    detectar_espacios,
    detectar_consistencia_texto
)


def validar_espacios(
    datos_antes,
    datos_despues,
    columna
):

    diagnostico_antes = detectar_espacios(
        datos_antes
    )

    diagnostico_despues = detectar_espacios(
        datos_despues
    )

    resultado_antes = diagnostico_antes[columna]

    resultado_despues = diagnostico_despues[columna]

    antes = resultado_antes["valores_con_espacios"]

    despues = resultado_despues["valores_con_espacios"]

    corregidos = antes - despues

    pendientes = despues

    if antes == 0:

        estado = "SIN_ACCION"

    elif despues == 0:

        estado = "CORREGIDO"

    elif despues < antes:

        estado = "CORREGIDO_CON_PENDIENTES"

    elif despues == antes:

        estado = "NO_CORREGIDO"

    else:

        estado = "ERROR"

    return {
        "categoria": "espacios",
        "accion": "normalizar_espacios",
        "columna": columna,
        "antes": antes,
        "despues": despues,
        "corregidos": corregidos,
        "pendientes": pendientes,
        "estado": estado
    }

def validar_capitalizacion(
    datos_antes,
    datos_despues,
    columna,
    grupo,
    forma_dominante
):

    if not datos_antes.index.equals(datos_despues.index):
        return {
            "categoria": "consistencia_texto",
            "accion": "normalizar_capitalizacion",
            "columna": columna,
            "grupo": grupo,
            "forma_dominante": forma_dominante,
            "antes": None,
            "despues": None,
            "corregidos": 0,
            "pendientes": None,
            "estado": "ERROR",
            "motivo": "INDICES_INCOMPATIBLES"
        }

    diagnostico_antes = detectar_consistencia_texto(
        datos_antes
    )

    diagnostico_despues = detectar_consistencia_texto(
        datos_despues
    )

    resultado_antes = diagnostico_antes[columna]

    resultado_despues = diagnostico_despues[columna]

    variaciones_antes = resultado_antes[
        "detalle_variaciones"
    ].get(grupo, {})

    variaciones_despues = resultado_despues[
        "detalle_variaciones"
    ].get(grupo, {})

    antes = 0
    despues = 0
    corregidos = 0

    serie_antes = datos_antes[columna]
    serie_despues = datos_despues[columna]

    for indice, valor_antes in serie_antes.items():

        if pd.isna(valor_antes):
            continue

        if not isinstance(valor_antes, str):
            continue

        if valor_antes.lower() != grupo:
            continue

        if valor_antes == forma_dominante:
            continue

        antes += 1

        valor_despues = serie_despues.loc[indice]

        if (
            isinstance(valor_despues, str)
            and valor_despues == forma_dominante
        ):
            corregidos += 1
        else:
            despues += 1

    pendientes = despues
    if antes == 0:

        estado = "SIN_ACCION"

    elif despues == 0:

        estado = "CORREGIDO"

    elif despues < antes:

        estado = "CORREGIDO_CON_PENDIENTES"

    elif despues == antes:

        estado = "NO_CORREGIDO"

    else:

        estado = "ERROR"

    return {
        "categoria": "consistencia_texto",
        "accion": "normalizar_capitalizacion",
        "columna": columna,
        "grupo": grupo,
        "forma_dominante": forma_dominante,
        "antes": antes,
        "despues": despues,
        "corregidos": corregidos,
        "pendientes": pendientes,
        "estado": estado
    }
