import pandas as pd
def agregar_columnas_faltantes(datos, estructura_objetivo):
    datos_homogeneizados = datos.copy()

    for columna in estructura_objetivo:
        if columna not in datos_homogeneizados.columns:
            datos_homogeneizados[columna] = pd.NA

    return datos_homogeneizados

def alinear_columnas(datos, estructura_objetivo):
    datos_ordenados = datos[
        estructura_objetivo
    ].copy()

    return datos_ordenados