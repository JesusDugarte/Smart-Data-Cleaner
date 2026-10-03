from detectores.calidad import (
    detectar_faltantes,
    detectar_duplicados,
    detectar_espacios,
    detectar_consistencia_texto
)

from analisis.correcciones import ejecutar_correcciones

from reglas.calidad import interpretar_calidad


def analizar_calidad(datos):

    diagnostico = {
        "faltantes": detectar_faltantes(datos),
        "duplicados": detectar_duplicados(datos),
        "espacios": detectar_espacios(datos),
        "consistencia_texto": detectar_consistencia_texto(datos)
    }

    interpretacion = interpretar_calidad(diagnostico)

    diagnostico["interpretacion"] = interpretacion

    return diagnostico

def procesar_calidad(datos):

    resultado_calidad = analizar_calidad(datos)

    recomendaciones = (
        resultado_calidad["interpretacion"]["recomendaciones"]
    )

    resultado_correcciones = ejecutar_correcciones(
        datos,
        recomendaciones
    )

    return {
        "realizada": True,
        "datos": resultado_correcciones["datos"],
        "diagnostico": resultado_calidad,
        "correcciones": resultado_correcciones["correcciones"],
        "pendientes": resultado_correcciones["pendientes"]
    }