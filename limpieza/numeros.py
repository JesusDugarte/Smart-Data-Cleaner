import pandas as pd
from detectores.numeros import detectar_patron_numerico

def convertir_columna_numerica(datos, columna):

    datos_limpios = datos.copy()

    datos_limpios[columna] = pd.to_numeric(
        datos_limpios[columna],
        errors="coerce"
    )

    return datos_limpios

def convertir_columnas_numericas(datos, columnas):

    datos_limpios = datos.copy()

    for columna in columnas:

        datos_limpios = convertir_columna_numerica(
            datos_limpios,
            columna
        )

    return datos_limpios

def convertir_numero(valor, patron):

    if patron == "ENTERO":
        return int(valor)

    if patron == "DECIMAL_PUNTO":
        return float(valor)

    if patron == "MILES_COMA":
        valor = valor.replace(",", "")
        return int(valor)

    if patron == "MILES_COMA_DECIMAL_PUNTO":
        valor = valor.replace(",", "")
        return float(valor)

    if patron == "MILES_PUNTO_DECIMAL_COMA":
        valor = valor.replace(".", "")
        valor = valor.replace(",", ".")
        return float(valor)

    return None

def convertir_columna_numerica_v2(datos, columna):

    datos_limpios = datos.copy()

    valores_convertidos = []

    for valor in datos_limpios[columna]:

        if pd.isna(valor):
            valores_convertidos.append(valor)
            continue

        patron = detectar_patron_numerico(valor)

        convertido = convertir_numero(
            valor,
            patron
        )

        if convertido is None:
            valores_convertidos.append(valor)
        else:
            valores_convertidos.append(convertido)

    datos_limpios[columna] = valores_convertidos

    return datos_limpios