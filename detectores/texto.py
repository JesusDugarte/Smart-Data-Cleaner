from reglas.texto import quitar_acentos, normalizar_texto

def detectar_espacios_externos(datos, columnas_originales):
    resultados = {}

    for columna in columnas_originales:
        if datos[columna].dtype == "object":
            tiene_espacios = (
                datos[columna].notna()
                & (datos[columna].str.strip() != datos[columna])
            )

            filas_afectadas = datos.index[tiene_espacios].tolist()

            if tiene_espacios.any():
                resultados[columna] = {
                    "cantidad": int(tiene_espacios.sum()),
                    "filas": filas_afectadas
                }

    return resultados

def detectar_case_inconsistente(datos, columnas_originales):
    resultados = {}

    for columna in columnas_originales:
        if datos[columna].dtype == "object":
            valores = datos[columna].dropna()
            grupos = {}

            for valor in valores:
                clave = valor.lower()

                if clave not in grupos:
                    grupos[clave] = []

                grupos[clave].append(valor)

            variantes = {}

            for clave, valores_originales in grupos.items():
                if len(set(valores_originales)) > 1:
                    cantidad_afectados = len(valores_originales)

                    variantes[clave] = {
                        "variantes": sorted(set(valores_originales)),
                        "cantidad_afectados": cantidad_afectados
                    }

            if variantes:
                resultados[columna] = variantes

    return resultados

def detectar_acentos_inconsistentes(datos, columnas_originales):
    resultados = {}

    for columna in columnas_originales:
        if datos[columna].dtype == "object":
            valores = datos[columna].dropna()
            grupos = {}

            for valor in valores:
                clave = quitar_acentos(valor)

                if clave not in grupos:
                    grupos[clave] = []

                grupos[clave].append(valor)

            variantes = {}

            for clave, valores_originales in grupos.items():
                if len(set(valores_originales)) > 1:
                    cantidad_afectados = len(valores_originales)

                    variantes[clave] = {
                        "variantes": sorted(set(valores_originales)),
                        "cantidad_afectados": cantidad_afectados
                    }

            if variantes:
                resultados[columna] = variantes

    return resultados

def detectar_representaciones_equivalentes(datos, columnas_originales):
    resultados = {}

    for columna in columnas_originales:
        if datos[columna].dtype == "object":
            valores = datos[columna].dropna()
            grupos = {}

            for valor in valores:
                clave = normalizar_texto(valor)

                if clave not in grupos:
                    grupos[clave] = []

                grupos[clave].append(valor)

            equivalentes = {}

            for clave, valores_originales in grupos.items():
                if len(set(valores_originales)) > 1:
                    cantidad_afectados = len(valores_originales)

                    equivalentes[clave] = {
                        "variantes": sorted(set(valores_originales)),
                        "cantidad_afectados": cantidad_afectados
                    }

            if equivalentes:
                resultados[columna] = equivalentes

    return resultados

def detectar_representacion_dominante(datos, columnas_originales):
    resultados = {}

    for columna in columnas_originales:
        if datos[columna].dtype == "object":

            valores = datos[columna].dropna()

            grupos = {}

            for valor in valores:
                clave = normalizar_texto(valor)

                if clave not in grupos:
                    grupos[clave] = {}

                if valor not in grupos[clave]:
                    grupos[clave][valor] = 0

                grupos[clave][valor] += 1

            dominantes = {}

            for clave, variantes in grupos.items():

                if len(variantes) > 1:
                    representacion_dominante = max(
                        variantes,
                        key=variantes.get
                    )

                    dominantes[clave] = {
                        "representacion": representacion_dominante,
                        "frecuencia": variantes[representacion_dominante],
                        "variantes": variantes
                    }

            if dominantes:
                resultados[columna] = dominantes

    return resultados

def detectar_email_incompleto(datos):
    resultados = {}

    if "Email" not in datos.columns:
        return resultados

    emails = datos["Email"].dropna()

    es_incompleto = (
        emails.str.contains("@", regex=False)
        & emails.str.endswith("@")
    )

    filas_afectadas = emails.index[es_incompleto].tolist()

    if filas_afectadas:
        resultados["Email"] = {
            "cantidad": len(filas_afectadas),
            "filas": filas_afectadas
        }

    return resultados