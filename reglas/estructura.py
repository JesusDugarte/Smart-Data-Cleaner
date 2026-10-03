

from detectores.estructura import (
    detectar_columnas_comunes_varios,
    detectar_frecuencia_columnas,
    detectar_archivos_por_columna,
    detectar_tipos_por_columna,
    detectar_diferencias_tipos_varios
)

def analizar_compatibilidad_estructural_varios(estructura_global):
    total_archivos = estructura_global["total_archivos"]
    columnas_comunes = estructura_global["columnas_comunes"]
    columnas_por_archivo = estructura_global["columnas_por_archivo"]
    diferencias_tipos = estructura_global["diferencias_tipos"]

    if total_archivos == 0:
        return "SIN_BASE_COMUN"

    if len(columnas_comunes) == 0:
        return "SIN_BASE_COMUN"

    conjuntos_columnas = [
        set(columnas)
        for columnas in columnas_por_archivo.values()
    ]

    estructura_equivalente = all(
        columnas == conjuntos_columnas[0]
        for columnas in conjuntos_columnas
    )

    if estructura_equivalente:
        if diferencias_tipos:
            return "ESTRUCTURA_COMUN_TIPOS_DIFERENTES"

        return "ESTRUCTURA_EQUIVALENTE"

    return "ESTRUCTURA_PARCIAL"

def construir_estructura_global(archivos, nombres_archivos):
    cantidad_archivos = len(archivos)

    columnas_comunes = detectar_columnas_comunes_varios(archivos)

    frecuencia_columnas = detectar_frecuencia_columnas(archivos)

    tipos_por_columna = detectar_tipos_por_columna(
        archivos,
        nombres_archivos
    )

    diferencias_tipos = detectar_diferencias_tipos_varios(
        tipos_por_columna
    )

    archivos_por_columna = detectar_archivos_por_columna(
        archivos,
        nombres_archivos
    )

    clasificacion = clasificar_frecuencia_columnas(
        frecuencia_columnas,
        cantidad_archivos
    )

    columnas_por_archivo = {}

    for datos, nombre in zip(archivos, nombres_archivos):
        columnas_por_archivo[nombre] = datos.columns.tolist()

    return {
        "total_archivos": cantidad_archivos,
        "columnas_comunes": sorted(columnas_comunes),
        "frecuencia_columnas": frecuencia_columnas,
        "clasificacion_columnas": clasificacion,
        "archivos_por_columna": archivos_por_columna,
        "tipos_por_columna": tipos_por_columna,
        "diferencias_tipos": diferencias_tipos,
        "columnas_por_archivo": columnas_por_archivo
    }

def crear_diagnostico_estructural(estructura_global):
    clasificacion = estructura_global["clasificacion_columnas"]

    columnas_comunes = []
    columnas_parciales = {}
    columnas_exclusivas = {}

    for columna, informacion in clasificacion.items():
        categoria = informacion["categoria"]

        if categoria == "COMUN":
            columnas_comunes.append(columna)

        elif categoria == "PARCIAL":
            columnas_parciales[columna] = informacion

        elif categoria == "EXCLUSIVA":
            columnas_exclusivas[columna] = informacion

    columnas_por_archivo = estructura_global["columnas_por_archivo"]

    nombres_archivos = list(columnas_por_archivo.keys())

    diferencias_orden = {}

    if nombres_archivos:
        archivo_base = nombres_archivos[0]
        orden_base = columnas_por_archivo[archivo_base]

        for nombre in nombres_archivos[1:]:
            orden_actual = columnas_por_archivo[nombre]

            if set(orden_actual) == set(orden_base):
                if orden_actual != orden_base:
                    diferencias_orden[nombre] = {
                        "orden": orden_actual,
                        "orden_base": orden_base,
                        "archivo_base": archivo_base
                    }

    compatibilidad = analizar_compatibilidad_estructural_varios(
        estructura_global
    )

    return {
        "total_archivos": estructura_global["total_archivos"],
        "columnas_comunes": sorted(columnas_comunes),
        "columnas_parciales": columnas_parciales,
        "columnas_exclusivas": columnas_exclusivas,
        "diferencias_tipos": estructura_global["diferencias_tipos"],
        "diferencias_orden": diferencias_orden,
        "compatibilidad": compatibilidad,
        "columnas_por_archivo": columnas_por_archivo
    }

def clasificar_frecuencia_columnas(frecuencia_columnas, cantidad_archivos):
    clasificacion = {}

    for columna, frecuencia in frecuencia_columnas.items():

        if frecuencia == cantidad_archivos:
            categoria = "COMUN"

        elif frecuencia == 1:
            categoria = "EXCLUSIVA"

        else:
            categoria = "PARCIAL"

        clasificacion[columna] = {
            "frecuencia": frecuencia,
            "total_archivos": cantidad_archivos,
            "categoria": categoria
        }

    return clasificacion

def analizar_estructuras_archivos(archivos, nombres_archivos):
    estructura_global = construir_estructura_global(
        archivos,
        nombres_archivos
    )

    diagnostico = crear_diagnostico_estructural(
        estructura_global
    )

    return diagnostico

def construir_estructura_objetivo(archivos):
    estructura_objetivo = []

    for datos in archivos:
        for columna in datos.columns:
            if columna not in estructura_objetivo:
                estructura_objetivo.append(columna)

    return estructura_objetivo

def clasificar_compatibilidad_tipos(resultado):
    if resultado["valores_analizados"] == 0:
        return "SIN_DATOS"

    if resultado["valores_no_convertibles"] == 0:
        return "COMPATIBLE_POTENCIAL"

    return "INCOMPATIBLE"

def clasificar_compatibilidad_tipos_varios(
    diagnostico_conflictos_tipos
):

    clasificaciones_tipos = {}

    for columna, diagnostico in (
        diagnostico_conflictos_tipos.items()
    ):

        clasificaciones_tipos[columna] = {}

        for archivo, resultado in (
            diagnostico["analisis_por_archivo"].items()
        ):

            clasificacion = (
                clasificar_compatibilidad_tipos(
                    resultado
                )
            )

            clasificaciones_tipos[columna][archivo] = (
                clasificacion
            )

    return clasificaciones_tipos

def analizar_condiciones_tipos(clasificaciones_tipos):

    hay_incompatibilidades = False
    hay_conflictos = False
    hay_datos_insuficientes = False

    for columna, clasificaciones in clasificaciones_tipos.items():

        for archivo, clasificacion in clasificaciones.items():

            if clasificacion == "INCOMPATIBLE":
                hay_incompatibilidades = True

            if clasificacion == "SIN_DATOS":
                hay_datos_insuficientes = True

        if all(
            clasificacion == "COMPATIBLE_POTENCIAL"
            for clasificacion in clasificaciones.values()
        ):
            hay_conflictos = True

    return {
        "hay_incompatibilidades": hay_incompatibilidades,
        "hay_conflictos": hay_conflictos,
        "hay_datos_insuficientes": hay_datos_insuficientes
    }

def determinar_estado_consolidacion(
    compatibilidad_estructural,
    hay_conflictos,
    hay_incompatibilidades,
    hay_datos_insuficientes
):
    if hay_incompatibilidades:
        return "BLOQUEADO"

    if compatibilidad_estructural == "SIN_BASE_COMUN":
        return "BLOQUEADO"

    if hay_conflictos or hay_datos_insuficientes:
        return "REVISAR"

    return "LISTO"

def determinar_estado_final(
    estado_consolidacion,
    validacion_registros_realizada,
    validacion_registros_correcta,
    validacion_procedencia_realizada,
    validacion_procedencia_correcta
):
    if estado_consolidacion == "BLOQUEADO":
        return "BLOQUEADO"

    if estado_consolidacion == "REVISAR":
        return "REVISAR"

    if not validacion_registros_realizada:
        return "REVISAR"

    if not validacion_procedencia_realizada:
        return "REVISAR"

    if not validacion_registros_correcta:
        return "REVISAR"

    if not validacion_procedencia_correcta:
        return "REVISAR"

    return "LISTO"