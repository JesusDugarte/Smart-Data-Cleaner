
import csv

import pandas as pd

from detectores.estructura import (
    detectar_columnas_duplicadas
)

from reglas.estructura import (
    analizar_estructuras_archivos,
    construir_estructura_objetivo
)


def cargar_archivos_csv(archivos_csv):
    """Detecta encabezados duplicados y carga los archivos CSV."""

    if len(archivos_csv) < 2:
        raise ValueError(
            "V2-06 requiere al menos 2 archivos CSV."
        )

    duplicados_por_archivo = {}

    for archivo in archivos_csv:

        with archivo.open(
            "r",
            encoding="utf-8-sig",
            newline=""
        ) as archivo_csv_abierto:

            encabezado = next(
                csv.reader(archivo_csv_abierto),
                []
            )

        duplicados = detectar_columnas_duplicadas(
            encabezado
        )

        if duplicados:
            duplicados_por_archivo[archivo.name] = duplicados

    datos_archivos = []

    for archivo in archivos_csv:

        datos = pd.read_csv(archivo)

        datos_archivos.append(datos)

    nombres_archivos = [
        archivo.name
        for archivo in archivos_csv
    ]

    return {
        "duplicados_por_archivo": duplicados_por_archivo,
        "datos_archivos": datos_archivos,
        "nombres_archivos": nombres_archivos
    }

def diagnosticar_estructuras_archivos(
    datos_archivos,
    nombres_archivos
):
    """Analiza la estructura de los archivos cargados."""

    diagnostico_estructural = analizar_estructuras_archivos(
        datos_archivos,
        nombres_archivos
    )

    estructura_objetivo = construir_estructura_objetivo(
        datos_archivos
    )

    return {
        "diagnostico_estructural": diagnostico_estructural,
        "estructura_objetivo": estructura_objetivo
    }