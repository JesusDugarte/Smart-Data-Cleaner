import pandas as pd


def exportar_datos_csv(datos, ruta_salida):
    datos.to_csv(
        ruta_salida,
        index=False
    )