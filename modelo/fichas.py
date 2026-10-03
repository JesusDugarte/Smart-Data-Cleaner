def crear_ficha(
    codigo,
    nombre,
    severidad,
    accion,
    cantidad_hallazgos,
    unidad_hallazgo,
    cantidad_afectados,
    unidad_afectada,
    detalle
):
    ficha = {
        "codigo": codigo,
        "nombre": nombre,
        "severidad": severidad,
        "accion": accion,
        "cantidad_hallazgos": cantidad_hallazgos,
        "unidad_hallazgo": unidad_hallazgo,
        "cantidad_afectados": cantidad_afectados,
        "unidad_afectada": unidad_afectada,
        "detalle": detalle
    }

    return ficha

def crear_ficha_archivo(nombre_archivo, formato, estructura):

    return {
        "archivo": nombre_archivo,
        "formato": formato,
        "estructura": estructura
    }

def crear_grupo_estructural(archivos, columnas_comunes):

    return {
        "archivos": archivos,
        "columnas_comunes": columnas_comunes,
        "observaciones": []
    }