from limpieza.calidad import (
    corregir_espacios,
    corregir_capitalizacion
)

def ejecutar_correcciones(datos, recomendaciones):
    datos_corregidos = datos.copy()

    correcciones = {}
    pendientes = []

    for recomendacion in recomendaciones:
        accion = recomendacion["accion"]

        if accion == "normalizar_espacios":
            resultado_espacios = corregir_espacios(
                datos_corregidos
            )

            datos_corregidos = resultado_espacios["datos"]

            correcciones["espacios"] = (
                resultado_espacios["correcciones"]["espacios"]
            )

        elif accion == "normalizar_capitalizacion":
            decisiones_capitalizacion = {
                recomendacion["grupo"]: {
                    "forma_dominante": recomendacion[
                        "forma_dominante"
                    ],
                    "corregible": True
                }
            }

            resultado_capitalizacion = (
                corregir_capitalizacion(
                    datos_corregidos,
                    decisiones_capitalizacion
                )
            )

            datos_corregidos = (
                resultado_capitalizacion["datos"]
            )

            correcciones_capitalizacion = (
                resultado_capitalizacion[
                    "correcciones"
                ]["capitalizacion"]
            )

            for columna, detalle in (
                correcciones_capitalizacion.items()
            ):

                if "capitalizacion" not in correcciones:
                    correcciones["capitalizacion"] = {}

                if columna not in correcciones["capitalizacion"]:
                    correcciones["capitalizacion"][
                        columna
                    ] = {
                        "valores_corregidos": 0
                    }

                correcciones["capitalizacion"][
                    columna
                ]["valores_corregidos"] += (
                    detalle["valores_corregidos"]
                )

        else:
            pendientes.append(recomendacion)

    return {
        "datos": datos_corregidos,
        "correcciones": correcciones,
        "pendientes": pendientes
    }