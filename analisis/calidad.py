from detectores.calidad import (
    detectar_faltantes,
    detectar_duplicados,
    detectar_espacios,
    detectar_consistencia_texto
)

from analisis.correcciones import ejecutar_correcciones

from reglas.calidad import (
    interpretar_calidad,
    determinar_estado_calidad
)
from validacion.calidad import (
    validar_espacios,
    validar_capitalizacion
)

def analizar_calidad(datos):

    diagnostico = {
        "faltantes": detectar_faltantes(datos),
        "duplicados": detectar_duplicados(datos),
        "espacios": detectar_espacios(datos),
        "consistencia_texto": detectar_consistencia_texto(datos)
    }

    return diagnostico

def procesar_calidad(datos):

    datos_antes = datos

    resultado_calidad = analizar_calidad(datos_antes)

    interpretacion = interpretar_calidad(
        resultado_calidad
    )

    recomendaciones = interpretacion["recomendaciones"]

    resultado_correcciones = ejecutar_correcciones(
        datos_antes,
        recomendaciones
    )

    datos_despues = resultado_correcciones["datos"]

    resultados_validacion = []

    for recomendacion in recomendaciones:

        if recomendacion["accion"] == "normalizar_espacios":

            resultado_validacion = validar_espacios(
                datos_antes,
                datos_despues,
                recomendacion["columna"]
            )

            resultados_validacion.append(
                resultado_validacion
            )

        elif recomendacion["accion"] == "normalizar_capitalizacion":

            resultado_validacion = validar_capitalizacion(
                datos_antes,
                datos_despues,
                recomendacion["columna"],
                recomendacion["grupo"],
                recomendacion["forma_dominante"]
            )

            resultados_validacion.append(
                resultado_validacion
            )

    estado_calidad = determinar_estado_calidad(
        resultado_correcciones["pendientes"],
        resultados_validacion
    )

    decision = {
        "calidad": {
            "hallazgos": interpretacion["hallazgos"],
            "recomendaciones": recomendaciones,
            "estado": estado_calidad
        }
    }

    ejecucion = {
        "calidad": {
            "realizada": True
        },
        "correcciones": resultado_correcciones["correcciones"]
    }

    validacion = {
        "calidad": resultados_validacion
    }

    resultado = {
        "correcciones": resultado_correcciones["correcciones"],
        "pendientes": resultado_correcciones["pendientes"]
    }

    return {
        "datos": datos_despues,
        "diagnostico": resultado_calidad,
        "decision": decision,
        "ejecucion": ejecucion,
        "validacion": validacion,
        "resultado": resultado
    }