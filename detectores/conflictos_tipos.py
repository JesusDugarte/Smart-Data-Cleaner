import pandas as pd


def analizar_compatibilidad_numerica(
    datos,
    columna
):
    valores_totales = len(datos[columna])
    valores_analizados = 0
    valores_faltantes = 0
    valores_convertibles = 0
    valores_no_convertibles = 0

    for valor in datos[columna]:

        if pd.isna(valor):
            valores_faltantes += 1
            continue

        valores_analizados += 1

        try:
            float(valor)
            valores_convertibles += 1

        except (ValueError, TypeError):
            valores_no_convertibles += 1

    return {
        "columna": columna,
        "valores_totales": valores_totales,
        "valores_analizados": valores_analizados,
        "valores_faltantes": valores_faltantes,
        "valores_convertibles": valores_convertibles,
        "valores_no_convertibles": valores_no_convertibles
    }

def construir_diagnostico_conflictos_numericos(
    datos_archivos,
    nombres_archivos,
    diferencias_tipos
):
    diagnosticos = {}

    for columna, informacion in diferencias_tipos.items():

        analisis_por_archivo = {}

        for datos, nombre in zip(
            datos_archivos,
            nombres_archivos
        ):
            resultado = analizar_compatibilidad_numerica(
                datos,
                columna
            )

            analisis_por_archivo[nombre] = resultado

        diagnosticos[columna] = {
            "columna": columna,
            "tipos": informacion["tipos"],
            "cantidad_tipos": informacion["cantidad_tipos"],
            "archivos_por_tipo": informacion[
                "archivos_por_tipo"
            ],
            "analisis_por_archivo": analisis_por_archivo
        }

    return diagnosticos