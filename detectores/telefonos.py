from reglas.telefonos import normalizar_telefono

def detectar_formato_telefono(datos):
    resultados = {}

    if "Telefono" not in datos.columns:
        return resultados

    telefonos = datos["Telefono"]

    tiene_formato_inconsistente = (
        telefonos.notna()
        & (telefonos != telefonos.apply(normalizar_telefono))
    )

    filas_afectadas = datos.index[tiene_formato_inconsistente].tolist()

    if filas_afectadas:
        resultados["Telefono"] = {
            "cantidad": len(filas_afectadas),
            "filas": filas_afectadas
        }

    return resultados

def detectar_longitud_telefono(datos):
    resultados = {}

    if "Telefono" not in datos.columns:
        return resultados

    telefonos = datos["Telefono"]

    telefonos_normalizados = telefonos.apply(normalizar_telefono)

    es_invalido = (
        telefonos_normalizados.notna()
        & (
            (telefonos_normalizados.str.len() != 10)
            | (~telefonos_normalizados.str.isdigit())
        )
    )

    filas_afectadas = datos.index[es_invalido].tolist()

    if filas_afectadas:
        resultados["Telefono"] = {
            "cantidad": len(filas_afectadas),
            "filas": filas_afectadas
        }

    return resultados

def detectar_telefonos_repetidos(datos):
    resultados = {}

    if "Telefono" not in datos.columns:
        return resultados

    telefonos = datos["Telefono"].dropna()
    conteo = telefonos.value_counts()
    repetidos = conteo[conteo > 1]

    if not repetidos.empty:
        resultados["Telefono"] = {
            "cantidad_hallazgos": int(len(repetidos)),
            "unidad_hallazgo": "valor",
            "cantidad_afectados": int(repetidos.sum()),
            "unidad_afectada": "registro",
            "valores": repetidos.to_dict()
        }

    return resultados
