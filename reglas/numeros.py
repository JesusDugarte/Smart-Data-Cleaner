def decidir_conversion_formatos(patrones):

    patrones_encontrados = set(
        patrones.keys()
    )

    formatos_seguros = {
        "ENTERO",
        "DECIMAL_PUNTO",
        "MILES_COMA"
    }

    formatos_regionales = {
        "MILES_COMA_DECIMAL_PUNTO",
        "MILES_PUNTO_DECIMAL_COMA"
    }

    if not patrones_encontrados:
        return "IGNORAR"

    if patrones_encontrados.issubset(
        formatos_seguros
    ):
        return "CONVERTIR"

    regionales_encontrados = (
        patrones_encontrados.intersection(
            formatos_regionales
        )
    )

    if len(regionales_encontrados) == 1:
        return "CONVERTIR"

    if len(regionales_encontrados) > 1:
        return "REVISAR"

    return "REVISAR"

from detectores.numeros import (
    detectar_patrones_columna
)

from reglas.columnas import (
    es_columna_protegida
)

def analizar_columna_numerica_v2(datos, columna):

    if es_columna_protegida(columna):
        return {
            "columna": columna,
            "decision": "PROTEGER"
        }

    resultado = detectar_patrones_columna(
        datos,
        columna
    )

    patrones = resultado["patrones"]

    if patrones == {"OTRO": resultado["valores_analizados"]}:
        decision = "IGNORAR"

    else:
        decision = decidir_conversion_formatos(
            patrones
        )

    return {
        "columna": columna,
        "valores_analizados": resultado[
            "valores_analizados"
        ],
        "patrones": patrones,
        "decision": decision
    }