import pandas as pd


def detectar_valores_numericos(datos, columna):
    valores = datos[columna].dropna()

    if len(valores) == 0:
        return {
            "columna": columna,
            "valores_analizados": 0,
            "valores_convertibles": 0,
            "valores_no_convertibles": 0,
            "porcentaje_convertible": 0
        }

    convertidos = pd.to_numeric(
        valores,
        errors="coerce"
    )

    valores_convertibles = convertidos.notna().sum()
    valores_no_convertibles = convertidos.isna().sum()

    porcentaje_convertible = (
        valores_convertibles / len(valores)
    ) * 100

    return {
        "columna": columna,
        "valores_analizados": len(valores),
        "valores_convertibles": valores_convertibles,
        "valores_no_convertibles": valores_no_convertibles,
        "porcentaje_convertible": porcentaje_convertible
    }
def detectar_ceros_iniciales(datos, columna):
    valores = datos[columna].dropna()

    valores_con_ceros = []

    for valor in valores:
        valor = str(valor)

        if (
            valor.isdigit()
            and len(valor) > 1
            and valor.startswith("0")
        ):
            valores_con_ceros.append(valor)

    return {
        "columna": columna,
        "valores_analizados": len(valores),
        "valores_con_ceros_iniciales": len(valores_con_ceros),
        "ejemplos": valores_con_ceros[:5]
    }
def detectar_separadores_numericos(datos, columna):
    valores = datos[columna].dropna()

    valores_con_separador = []

    for valor in valores:
        valor = str(valor)

        if "." in valor:
            partes = valor.split(".")

            if len(partes) == 2:
                parte_derecha = partes[1]

                if len(parte_derecha) == 3 and parte_derecha.isdigit():
                    valores_con_separador.append(valor)

    return {
        "columna": columna,
        "valores_analizados": len(valores),
        "valores_con_separador": len(valores_con_separador),
        "ejemplos": valores_con_separador[:5]
    }
def detectar_patron_numerico(valor):

    valor = str(valor)

    if valor.isdigit():
        return "ENTERO"

    if "." in valor and "," in valor:

        partes_punto = valor.split(".")

        if len(partes_punto) >= 2:

            parte_decimal = partes_punto[-1]
            parte_entera = ".".join(
                partes_punto[:-1]
            )

            if (
                parte_decimal.isdigit()
                and len(parte_decimal) >= 1
            ):

                grupos_punto = parte_entera.split(".")

                if len(grupos_punto) == 1:

                    grupos_miles = parte_entera.split(",")

                    if (
                        len(grupos_miles) >= 2
                        and grupos_miles[0].isdigit()
                        and all(
                            grupo.isdigit()
                            and len(grupo) == 3
                            for grupo in grupos_miles[1:]
                        )
                    ):
                        return "MILES_COMA_DECIMAL_PUNTO"

        partes_coma = valor.split(",")

        if len(partes_coma) >= 2:

            parte_decimal = partes_coma[-1]
            parte_entera = ",".join(
                partes_coma[:-1]
            )

            if (
                parte_decimal.isdigit()
                and len(parte_decimal) >= 1
            ):

                grupos_coma = parte_entera.split(",")

                if len(grupos_coma) == 1:

                    grupos_miles = parte_entera.split(".")

                    if (
                        len(grupos_miles) >= 2
                        and grupos_miles[0].isdigit()
                        and all(
                            grupo.isdigit()
                            and len(grupo) == 3
                            for grupo in grupos_miles[1:]
                        )
                    ):
                        return "MILES_PUNTO_DECIMAL_COMA"

    if "." in valor:

        partes = valor.split(".")

        if len(partes) == 2:

            parte_entera = partes[0]
            parte_decimal = partes[1]

            if (
                parte_entera.isdigit()
                and parte_decimal.isdigit()
            ):

                if len(parte_decimal) == 3:
                    return "AMBIGUO"

                return "DECIMAL_PUNTO"

    if "," in valor:

        partes = valor.split(",")

        if len(partes) == 2:

            parte_entera = partes[0]
            parte_decimal = partes[1]

            if (
                parte_entera.isdigit()
                and parte_decimal.isdigit()
                and len(parte_decimal) == 3
            ):
                return "MILES_COMA"

    return "OTRO"
def detectar_patrones_columna(datos, columna):

    valores = datos[columna].dropna()

    patrones = {}

    for valor in valores:

        patron = detectar_patron_numerico(valor)

        if patron not in patrones:
            patrones[patron] = 0

        patrones[patron] += 1

    return {
        "columna": columna,
        "valores_analizados": len(valores),
        "patrones": patrones
    }
def decidir_conversion_numerica(patrones):

    patrones_permitidos = {
        "ENTERO",
        "DECIMAL_PUNTO"
    }

    patrones_encontrados = set(patrones.keys())

    if patrones_encontrados.issubset(patrones_permitidos):
        return "CONVERTIR"

    return "REVISAR"
from reglas.columnas import es_columna_protegida


def decidir_columna_numerica(datos, columna):

    resultado = detectar_valores_numericos(
        datos,
        columna
    )

    protegida = es_columna_protegida(columna)

    if protegida:
        decision = "PROTEGER"

    elif resultado["porcentaje_convertible"] == 100:
        decision = "EVALUAR"

    else:
        decision = "REVISAR"

    return {
        "columna": columna,
        "porcentaje_convertible": resultado["porcentaje_convertible"],
        "protegida": protegida,
        "decision": decision
    }
def analizar_columna_numerica(datos, columna):

    resultado_convertibilidad = detectar_valores_numericos(
        datos,
        columna
    )

    protegida = es_columna_protegida(columna)

    resultado_patrones = detectar_patrones_columna(
        datos,
        columna
    )

    if protegida:
        decision = "PROTEGER"

    elif resultado_convertibilidad["porcentaje_convertible"] < 100:
        decision = "REVISAR"

    else:
        decision = decidir_conversion_numerica(
            resultado_patrones["patrones"]
        )

    return {
        "columna": columna,
        "valores_analizados": resultado_convertibilidad[
            "valores_analizados"
        ],
        "valores_convertibles": resultado_convertibilidad[
            "valores_convertibles"
        ],
        "valores_no_convertibles": resultado_convertibilidad[
            "valores_no_convertibles"
        ],
        "porcentaje_convertible": resultado_convertibilidad[
            "porcentaje_convertible"
        ],
        "protegida": protegida,
        "patrones": resultado_patrones["patrones"],
        "decision": decision
    }
def analizar_datos_numericos(datos):

    resultados = []

    for columna in datos.columns:

        resultado = analizar_columna_numerica(
            datos,
            columna
        )

        if (
            resultado["valores_analizados"] > 0
            and resultado["porcentaje_convertible"] == 0
            and not resultado["protegida"]
        ):
            resultado["decision"] = "IGNORAR"

        resultados.append(resultado)

    return resultados