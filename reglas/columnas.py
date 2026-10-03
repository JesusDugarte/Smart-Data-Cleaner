import unicodedata
import pandas as pd

def normalizar_nombre_columna(nombre_columna):
    nombre_columna = nombre_columna.strip().lower()
    nombre_columna = unicodedata.normalize("NFD", nombre_columna)
    nombre_columna = nombre_columna.encode("ascii", "ignore").decode("utf-8")
    return nombre_columna

COLUMNAS_ESTANDAR = [
    "ID",
    "Nombre",
    "Email",
    "Telefono",
    "Ciudad",
    "Fecha_Registro"
]

COLUMNAS_ESTANDAR_NORMALIZADAS = {
    normalizar_nombre_columna(columna): columna
    for columna in COLUMNAS_ESTANDAR
}

EQUIVALENCIAS_COLUMNAS = {
    "telefono": "Telefono",
    "fecha registro": "Fecha_Registro",
}
COLUMNAS_PROTEGIDAS = {
    "ID",
    "Telefono",
    "Codigo",
    "Documento",
    "SKU",
    "Codigo_Postal"
}
def es_columna_protegida(nombre_columna):
    return nombre_columna in COLUMNAS_PROTEGIDAS

def buscar_equivalencia_columna(nombre_columna):
    return EQUIVALENCIAS_COLUMNAS.get(nombre_columna)

def resolver_nombre_columna(nombre_columna):
    nombre_normalizado = normalizar_nombre_columna(nombre_columna)

    if nombre_normalizado in COLUMNAS_ESTANDAR_NORMALIZADAS:
        return COLUMNAS_ESTANDAR_NORMALIZADAS[nombre_normalizado]

    return buscar_equivalencia_columna(nombre_normalizado)

def detectar_columnas_duplicadas(columnas_originales):
    serie = pd.Series(columnas_originales)

    return serie[
        serie.duplicated(keep=False)
    ].unique().tolist()

def detectar_colisiones_columnas(resultados):
    colisiones = []

    for i, resultado in enumerate(resultados):
        if resultado["resuelta"] is None:
            continue

        for otro in resultados[i + 1:]:
            if otro["resuelta"] is None:
                continue

            if resultado["resuelta"] == otro["resuelta"]:
                if resultado["original"] != otro["original"]:
                    colisiones.append(resultado["resuelta"])

    return list(set(colisiones))

def detectar_columnas_faltantes(columnas_resueltas):
    return [
        columna
        for columna in COLUMNAS_ESTANDAR
        if columna not in columnas_resueltas
    ]

def detectar_columnas_adicionales(columnas_originales, columnas_resueltas):
    return [
        original
        for original, resuelta in zip(
            columnas_originales,
            columnas_resueltas
        )
        if resuelta is None
    ]

def analizar_columna(nombre_columna):
    nombre_normalizado = normalizar_nombre_columna(nombre_columna)

    if nombre_columna in COLUMNAS_ESTANDAR:
        return {
            "original": nombre_columna,
            "normalizada": nombre_normalizado,
            "resuelta": nombre_columna,
            "tipo": "ESTANDAR"
        }

    if nombre_normalizado in COLUMNAS_ESTANDAR_NORMALIZADAS:
        return {
            "original": nombre_columna,
            "normalizada": nombre_normalizado,
            "resuelta": COLUMNAS_ESTANDAR_NORMALIZADAS[nombre_normalizado],
            "tipo": "VARIANTE"
        }

    if nombre_normalizado in EQUIVALENCIAS_COLUMNAS:
        return {
            "original": nombre_columna,
            "normalizada": nombre_normalizado,
            "resuelta": EQUIVALENCIAS_COLUMNAS[nombre_normalizado],
            "tipo": "EQUIVALENCIA"
        }

    return {
        "original": nombre_columna,
        "normalizada": nombre_normalizado,
        "resuelta": None,
        "tipo": "ADICIONAL"
    }

def construir_mapeo_columnas(resultados):
    mapeo = {}

    for resultado in resultados:
        if resultado["resuelta"] is not None:
            mapeo[resultado["original"]] = resultado["resuelta"]

    return mapeo

def aplicar_mapeo_columnas(datos, mapeo, colisiones=None):
    if colisiones:
        raise ValueError(
            "No se puede aplicar el mapeo: existen colisiones de columnas."
        )

    return datos.rename(columns=mapeo)

def analizar_columnas(columnas):
    resultados = []

    for columna in columnas:
        resultado = analizar_columna(columna)
        resultados.append(resultado)

    columnas_resueltas = [
        resultado["resuelta"]
        for resultado in resultados
        if resultado["resuelta"] is not None
    ]

    faltantes = detectar_columnas_faltantes(columnas_resueltas)

    duplicadas = detectar_columnas_duplicadas(columnas)
    colisiones = detectar_colisiones_columnas(resultados)

    adicionales = detectar_columnas_adicionales(
        columnas,
        [resultado["resuelta"] for resultado in resultados]
    )

    if faltantes or duplicadas or colisiones:
        estado = "ERROR"
    elif adicionales:
        estado = "REVISAR"
    else:
        estado = "OK"
    return {
        "colisiones": colisiones,
        "detalle": resultados,
        "faltantes": faltantes,
        "adicionales": adicionales,
        "duplicadas": duplicadas,
        "estado": estado
        
    }