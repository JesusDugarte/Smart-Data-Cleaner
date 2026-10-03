import pandas as pd

def detectar_faltantes(datos):
    diagnostico = {}

    if datos.empty:
        return diagnostico

    for columna in datos.columns:
        total = len(datos)
        faltantes = 0

        for valor in datos[columna]:
            if pd.isna(valor):
                faltantes += 1
            elif isinstance(valor, str) and valor.strip() == "":
                faltantes += 1

        presentes = total - faltantes

        if total > 0:
            porcentaje_faltante = (
                faltantes / total
            ) * 100
        else:
            porcentaje_faltante = None

        diagnostico[columna] = {
            "total": total,
            "presentes": presentes,
            "faltantes": faltantes,
            "porcentaje_faltante": porcentaje_faltante
        }

    return diagnostico

def detectar_duplicados(datos):
    total = len(datos)

    if total == 0:
        return {
            "total": 0,
            "filas_duplicadas": 0,
            "filas_unicas": 0,
            "porcentaje_duplicados": 0.0
        }

    filas_duplicadas = datos.duplicated().sum()
    filas_unicas = total - filas_duplicadas
    porcentaje_duplicados = (
        filas_duplicadas / total
    ) * 100

    return {
        "total": total,
        "filas_duplicadas": int(filas_duplicadas),
        "filas_unicas": filas_unicas,
        "porcentaje_duplicados": porcentaje_duplicados
    }

def detectar_espacios(datos):
    diagnostico = {}

    if datos.empty:
        return diagnostico

    for columna in datos.columns:

        if not datos[columna].dtype == "object":
            continue

        total = len(datos)
        valores_con_espacios = 0
        espacios_iniciales = 0
        espacios_finales = 0
        espacios_internos = 0

        for valor in datos[columna]:

            if pd.isna(valor):
                continue

            if not isinstance(valor, str):
                continue

            if valor.strip() == "":
                continue

            tiene_inicial = valor != valor.lstrip()
            tiene_final = valor != valor.rstrip()
            tiene_interno = "  " in valor.strip()

            if tiene_inicial or tiene_final or tiene_interno:
                valores_con_espacios += 1

            if tiene_inicial:
                espacios_iniciales += 1

            if tiene_final:
                espacios_finales += 1

            if tiene_interno:
                espacios_internos += 1

        diagnostico[columna] = {
            "total": total,
            "valores_con_espacios": valores_con_espacios,
            "espacios_iniciales": espacios_iniciales,
            "espacios_finales": espacios_finales,
            "espacios_internos": espacios_internos
        }

    return diagnostico

def detectar_consistencia_texto(datos):
    diagnostico = {}

    if datos.empty:
        return diagnostico

    for columna in datos.columns:

        if datos[columna].dtype != "object":
            continue

        valores = []

        for valor in datos[columna]:

            if pd.isna(valor):
                continue

            if not isinstance(valor, str):
                continue

            if valor.strip() == "":
                continue

            valores.append(valor)

        grupos = {}

        for valor in valores:

            clave = valor.lower()

            if clave not in grupos:
                grupos[clave] = {}

            if valor not in grupos[clave]:
                grupos[clave][valor] = 0

            grupos[clave][valor] += 1

        variaciones = {}
        frecuencias_variaciones = {}

        for clave, variantes in grupos.items():

            if len(variantes) > 1:

                variaciones[clave] = list(
                    variantes.keys()
                )

                frecuencias_variaciones[clave] = variantes

        diagnostico[columna] = {
            "total": len(valores),
            "valores_unicos": len(set(valores)),
            "variaciones_capitalizacion": len(variaciones),
            "detalle_variaciones": variaciones,
            "frecuencias_variaciones": frecuencias_variaciones
        }

    return diagnostico