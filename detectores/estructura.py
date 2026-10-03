def detectar_columnas(datos):
    return datos.columns.tolist()

def detectar_cantidad_columnas(datos):
    return len(datos.columns)

def detectar_tipos_datos(datos):
    return datos.dtypes.to_dict()

def detectar_mismo_orden(datos_a, datos_b):
    return datos_a.columns.tolist() == datos_b.columns.tolist()

def detectar_columnas_comunes(datos_a, datos_b):
    columnas_a = set(datos_a.columns)
    columnas_b = set(datos_b.columns)

    return columnas_a & columnas_b

def detectar_columnas_exclusivas(datos_a, datos_b):
    columnas_a = set(datos_a.columns)
    columnas_b = set(datos_b.columns)

    return {
        "solo_a": columnas_a - columnas_b,
        "solo_b": columnas_b - columnas_a
    }

def detectar_diferencias_tipo(datos_a, datos_b):

    columnas_comunes = (
        set(datos_a.columns)
        & set(datos_b.columns)
    )

    diferencias = {}

    for columna in columnas_comunes:

        tipo_a = datos_a[columna].dtype
        tipo_b = datos_b[columna].dtype

        if tipo_a != tipo_b:

            diferencias[columna] = {
                "tipo_a": str(tipo_a),
                "tipo_b": str(tipo_b)
            }

    return diferencias

def detectar_diferencia_cantidad_columnas(datos_a, datos_b):

    cantidad_a = detectar_cantidad_columnas(datos_a)
    cantidad_b = detectar_cantidad_columnas(datos_b)

    return {
        "cantidad_a": cantidad_a,
        "cantidad_b": cantidad_b,
        "diferente": cantidad_a != cantidad_b
    }

def detectar_orden_columnas(datos):
    return {
        columna: posicion
        for posicion, columna in enumerate(datos.columns, start=1)
    }

def detectar_cantidad_registros(datos):
    return len(datos)

def analizar_estructura_archivo(datos):

    return {
        "cantidad_registros": detectar_cantidad_registros(datos),
        "cantidad_columnas": detectar_cantidad_columnas(datos),
        "columnas": detectar_columnas(datos),
        "tipos": detectar_tipos_datos(datos),
        "orden": detectar_orden_columnas(datos)
    }

def comparar_estructuras(datos_a, datos_b):

    return {
        "cantidad_columnas": detectar_diferencia_cantidad_columnas(
            datos_a,
            datos_b
        ),

        "columnas_comunes": detectar_columnas_comunes(
            datos_a,
            datos_b
        ),

        "columnas_exclusivas": detectar_columnas_exclusivas(
            datos_a,
            datos_b
        ),

        "mismo_orden": detectar_mismo_orden(
            datos_a,
            datos_b
        ),

        "diferencias_tipo": detectar_diferencias_tipo(
            datos_a,
            datos_b
        )
    }

def detectar_columnas_comunes_varios(archivos):

    if not archivos:
        return set()

    columnas_comunes = set(archivos[0].columns)

    for archivo in archivos[1:]:
        columnas_comunes = columnas_comunes.intersection(
            set(archivo.columns)
        )

    return columnas_comunes

def detectar_frecuencia_columnas(archivos):
    frecuencia = {}

    for datos in archivos:
        for columna in datos.columns:
            if columna not in frecuencia:
                frecuencia[columna] = 0

            frecuencia[columna] += 1

    return frecuencia

def detectar_archivos_por_columna(archivos, nombres_archivos):
    archivos_por_columna = {}

    for datos, nombre in zip(archivos, nombres_archivos):
        for columna in datos.columns:
            if columna not in archivos_por_columna:
                archivos_por_columna[columna] = []

            archivos_por_columna[columna].append(nombre)

    return archivos_por_columna

def detectar_tipos_por_columna(archivos, nombres_archivos):
    tipos_por_columna = {}

    for datos, nombre in zip(archivos, nombres_archivos):
        for columna in datos.columns:
            if columna not in tipos_por_columna:
                tipos_por_columna[columna] = {}

            tipo = str(datos[columna].dtype)

            if tipo not in tipos_por_columna[columna]:
                tipos_por_columna[columna][tipo] = []

            tipos_por_columna[columna][tipo].append(nombre)

    return tipos_por_columna

def detectar_diferencias_tipos_varios(tipos_por_columna):
    diferencias = {}

    for columna, tipos in tipos_por_columna.items():
        if len(tipos) > 1:
            diferencias[columna] = {
                "tipos": list(tipos.keys()),
                "cantidad_tipos": len(tipos),
                "archivos_por_tipo": tipos
            }

    return diferencias

def detectar_diferencias_orden_varios(archivos, nombres_archivos):
    if not archivos:
        return {}

    orden_base = archivos[0].columns.tolist()
    diferencias = {}

    for datos, nombre in zip(archivos, nombres_archivos):
        orden_actual = datos.columns.tolist()

        if orden_actual != orden_base:
            diferencias[nombre] = {
                "orden": orden_actual,
                "orden_base": orden_base
            }

    return diferencias