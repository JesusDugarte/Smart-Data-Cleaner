def interpretar_calidad(diagnostico):

    hallazgos = []
    recomendaciones = []

    faltantes = diagnostico["faltantes"]

    for columna, resultado in faltantes.items():

        if resultado["faltantes"] > 0:

            clasificacion = clasificar_faltantes(
                resultado
            )

            hallazgo = {
                "categoria": "faltantes",
                "columna": columna,
                "problema": clasificacion,
                "detalle": {
                    "cantidad": resultado["faltantes"],
                    "porcentaje": resultado["porcentaje_faltante"]
                }
            }

            hallazgos.append(hallazgo)

    duplicados = diagnostico["duplicados"]

    if duplicados["filas_duplicadas"] > 0:

        hallazgo = {
            "categoria": "duplicados",
            "columna": None,
            "problema": "filas_duplicadas",
            "detalle": {
                "cantidad": duplicados["filas_duplicadas"],
                "porcentaje": duplicados["porcentaje_duplicados"]
            }
        }

        hallazgos.append(hallazgo)

        recomendacion = {
            "categoria": "duplicados",
            "columna": None,
            "accion": "revisar_filas_duplicadas"
        }

        recomendaciones.append(recomendacion)

    espacios = diagnostico["espacios"]

    for columna, resultado in espacios.items():

        if resultado["valores_con_espacios"] > 0:

            hallazgo = {
                "categoria": "espacios",
                "columna": columna,
                "problema": "valores_con_espacios",
                "detalle": {
                    "cantidad": resultado["valores_con_espacios"],
                    "iniciales": resultado["espacios_iniciales"],
                    "finales": resultado["espacios_finales"],
                    "internos": resultado["espacios_internos"]
                }
            }

            hallazgos.append(hallazgo)

            recomendacion = {
                "categoria": "espacios",
                "columna": columna,
                "accion": "normalizar_espacios"
            }

            recomendaciones.append(recomendacion)

    consistencia_texto = diagnostico["consistencia_texto"]

    for columna, resultado in consistencia_texto.items():

        if resultado["variaciones_capitalizacion"] > 0:

            decisiones_capitalizacion = (
                determinar_correcciones_capitalizacion(
                    resultado["frecuencias_variaciones"]
                )
            )

            hallazgo = {
                "categoria": "consistencia_texto",
                "columna": columna,
                "problema": "variaciones_capitalizacion",
                "detalle": {
                    "cantidad": resultado[
                        "variaciones_capitalizacion"
                    ],
                    "variaciones": resultado[
                        "detalle_variaciones"
                    ],
                    "decisiones": decisiones_capitalizacion
                }
            }

            hallazgos.append(hallazgo)

            for clave, decision in (
                decisiones_capitalizacion.items()
            ):

                if decision["corregible"]:

                    recomendacion = {
                        "categoria": "consistencia_texto",
                        "columna": columna,
                        "accion": "normalizar_capitalizacion",
                        "grupo": clave,
                        "forma_dominante": (
                            decision["forma_dominante"]
                        )
                    }

                    recomendaciones.append(
                        recomendacion
                    )

    hay_hallazgos = len(hallazgos) > 0

    return {
        "hay_hallazgos": hay_hallazgos,
        "hallazgos": hallazgos,
        "recomendaciones": recomendaciones
    }

def determinar_correcciones_capitalizacion(
    frecuencias_variaciones
):
    resultado = {}

    for clave, variantes in frecuencias_variaciones.items():

        total = sum(variantes.values())

        frecuencia_dominante = max(
            variantes.values()
        )

        variantes_dominantes = [
            variante
            for variante, frecuencia in variantes.items()
            if frecuencia == frecuencia_dominante
        ]

        if len(variantes_dominantes) == 1:
            variante_dominante = variantes_dominantes[0]
        else:
            variante_dominante = None

        porcentaje_dominante = (
            frecuencia_dominante / total
        ) * 100

        corregible = (
            variante_dominante is not None
            and porcentaje_dominante > 50
        )

        resultado[clave] = {
            "forma_dominante": variante_dominante,
            "frecuencia_dominante": frecuencia_dominante,
            "total": total,
            "porcentaje": porcentaje_dominante,
            "corregible": corregible
        }

    return resultado

def clasificar_faltantes(resultado):
    porcentaje_faltante = resultado["porcentaje_faltante"]

    if porcentaje_faltante == 0:
        return "SIN_FALTANTES"

    if porcentaje_faltante < 50:
        return "FALTANTES_PARCIALES"

    if porcentaje_faltante < 100:
        return "FALTANTES_SIGNIFICATIVOS"

    return "SIN_DATOS"