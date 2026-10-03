def detectar_cambios(antes, despues):
    cambios = []

    for columna in antes.columns:
        if columna not in despues.columns:
            continue

        diferentes = antes[columna].fillna("<VACIO>") != despues[columna].fillna("<VACIO>")

        filas = antes.index[diferentes].tolist()

        for fila in filas:
            cambios.append({
                "fila": fila,
                "columna": columna,
                "antes": antes.loc[fila, columna],
                "despues": despues.loc[fila, columna]
            })

    return cambios

CLASIFICACION_COLUMNAS = {
    "Nombre": "LIMPIEZA",
    "Email": "LIMPIEZA",
    "Telefono": "LIMPIEZA",
    "Ciudad": "LIMPIEZA",
    "Fecha_Registro": "CONVERSION"
}

def clasificar_cambios(cambios, columnas_convertir=None):

    if columnas_convertir is None:
        columnas_convertir = []

    resultados = []

    for cambio in cambios:

        columna = cambio["columna"]

        if columna in columnas_convertir:
            tipo = "CONVERSION"

        else:
            tipo = CLASIFICACION_COLUMNAS.get(
                columna,
                "NO_CLASIFICADO"
            )

        resultado = cambio.copy()
        resultado["tipo"] = tipo

        resultados.append(resultado)

    return resultados