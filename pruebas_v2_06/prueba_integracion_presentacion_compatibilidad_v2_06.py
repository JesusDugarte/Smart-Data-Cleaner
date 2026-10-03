import pandas as pd

from detectores.estructura import (
    detectar_tipos_por_columna,
    detectar_diferencias_tipos_varios
)

from detectores.conflictos_tipos import (
    construir_diagnostico_conflictos_numericos
)

from reglas.estructura import (
    clasificar_compatibilidad_tipos_varios
)

from presentacion.consola import (
    mostrar_compatibilidad_tipos
)

archivo_X = pd.read_csv(
    "pruebas_v2_06/archivo_X.csv"
)

archivo_Z = pd.read_csv(
    "pruebas_v2_06/archivo_Z.csv"
)

datos_archivos = [
    archivo_X,
    archivo_Z
]

nombres_archivos = [
    "archivo_X.csv",
    "archivo_Z.csv"
]

tipos_por_columna = detectar_tipos_por_columna(
    datos_archivos,
    nombres_archivos
)

diferencias_tipos = detectar_diferencias_tipos_varios(
    tipos_por_columna
)

diagnostico_conflictos_tipos = (
    construir_diagnostico_conflictos_numericos(
        datos_archivos,
        nombres_archivos,
        diferencias_tipos
    )
)

clasificaciones_tipos = (
    clasificar_compatibilidad_tipos_varios(
        diagnostico_conflictos_tipos
    )
)

mostrar_compatibilidad_tipos(
    clasificaciones_tipos
)