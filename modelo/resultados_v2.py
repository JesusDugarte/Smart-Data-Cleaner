def crear_resultado_proceso(
    diagnostico,
    decision,
    ejecucion,
    validacion,
    estado_final,
    datos_finales,
    resumen,
    correcciones,
    pendientes
):
    return {
        "diagnostico": diagnostico,
        "decision": decision,
        "ejecucion": ejecucion,
        "validacion": validacion,
        "resultado": {
            "estado_final": estado_final,
            "datos": datos_finales,
            "resumen": resumen,
            "correcciones": correcciones,
            "pendientes": pendientes
        }
    }

def construir_datos_finales(
    datos_corregidos,
    datos_consolidados
):
    if len(datos_corregidos) != len(datos_consolidados):
        raise ValueError(
            "Los datos corregidos y los datos consolidados "
            "no tienen la misma cantidad de registros."
        )

    datos_finales = datos_corregidos.copy()

    datos_finales["Archivo_Origen"] = (
        datos_consolidados["Archivo_Origen"].values
    )

    return datos_finales

def construir_resumen(
    diagnostico_v2_06,
    diagnostico_calidad,
    datos_finales,
    correcciones,
    pendientes
):
    categorias_con_hallazgos = []

    hallazgos = diagnostico_calidad[
        "interpretacion"
    ]["hallazgos"]

    for hallazgo in hallazgos:
        categoria = hallazgo["categoria"]

        if categoria not in categorias_con_hallazgos:
            categorias_con_hallazgos.append(categoria)

    correcciones_realizadas = {}

    for categoria, detalles in correcciones.items():
        total_corregidos = 0

        for columna, detalle in detalles.items():
            total_corregidos += detalle[
                "valores_corregidos"
            ]

        correcciones_realizadas[categoria] = (
            total_corregidos
        )

    return {
        "archivos_analizados": diagnostico_v2_06[
            "archivos_analizados"
        ],
        "registros_procesados": len(datos_finales),
        "categorias_con_hallazgos": (
            categorias_con_hallazgos
        ),
        "correcciones_realizadas": (
            correcciones_realizadas
        ),
        "pendientes": pendientes
    }