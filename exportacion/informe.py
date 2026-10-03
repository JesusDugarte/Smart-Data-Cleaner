def construir_informe(
    resumen,
    diagnostico_calidad,
    correcciones,
    pendientes,
    estado_final,
    validacion
):
    return {
        "resumen": resumen,
        "hallazgos": diagnostico_calidad,
        "correcciones": correcciones,
        "pendientes": pendientes,
        "estado_final": estado_final,
        "validacion": validacion
    }

def exportar_informe_txt(informe, ruta_salida):
    with open(
        ruta_salida,
        "w",
        encoding="utf-8"
    ) as archivo:

        archivo.write(
            "SMART DATA CLEANER\n"
        )

        archivo.write(
            "INFORME DEL PROCESO\n"
        )

        archivo.write(
            "===================\n\n"
        )

        archivo.write(
            "RESUMEN\n"
        )

        archivo.write(
            "-------\n"
        )

        archivo.write(
            f"Archivos analizados: "
            f"{informe['resumen']['archivos_analizados']}\n"
        )

        archivo.write(
            f"Registros procesados: "
            f"{informe['resumen']['registros_procesados']}\n"
        )

        archivo.write(
            f"Estado final: "
            f"{informe['estado_final']}\n"
        )

        archivo.write("\n")

        archivo.write(
            "HALLAZGOS\n"
        )

        archivo.write(
            "---------\n"
        )

        archivo.write(
            "\nFALTANTES\n"
        )

        archivo.write(
            "---------\n"
        )

        faltantes = informe["hallazgos"]["faltantes"]
        hallazgos = informe["hallazgos"]["interpretacion"]["hallazgos"]

        for columna, resultado in faltantes.items():

            if resultado["faltantes"] == 0:
                continue

            archivo.write(
                f"{columna}:\n"
            )

            archivo.write(
                f"  Faltantes: "
                f"{resultado['faltantes']}\n"
            )

            archivo.write(
                f"  Total: "
                f"{resultado['total']}\n"
            )

            archivo.write(
                f"  Porcentaje: "
                f"{resultado['porcentaje_faltante']:.2f}%\n"
            )

            clasificacion = None

            for hallazgo in hallazgos:
                if (
                    hallazgo["categoria"] == "faltantes"
                    and hallazgo["columna"] == columna
                ):
                    clasificacion = hallazgo["problema"]
                    break

            if clasificacion is not None:
                archivo.write(
                    f"  Clasificación: "
                    f"{clasificacion}\n"
                )

            archivo.write("\n")

        archivo.write(
            "DUPLICADOS\n"
        )

        archivo.write(
            "----------\n"
        )

        duplicados = informe["hallazgos"]["duplicados"]

        archivo.write(
            f"Filas duplicadas: "
            f"{duplicados['filas_duplicadas']}\n"
        )

        archivo.write(
            f"Filas totales: "
            f"{duplicados['total']}\n"
        )

        archivo.write(
            f"Porcentaje: "
            f"{duplicados['porcentaje_duplicados']:.2f}%\n"
        )

        archivo.write("\n")

        archivo.write(
            "ESPACIOS\n"
        )

        archivo.write(
            "--------\n"
        )

        espacios = informe["hallazgos"]["espacios"]

        for columna, resultado in espacios.items():

            if resultado["valores_con_espacios"] == 0:
                continue

            archivo.write(
                f"{columna}:\n"
            )

            archivo.write(
                f"  Valores afectados: "
                f"{resultado['valores_con_espacios']}\n"
            )

            archivo.write(
                f"  Espacios iniciales: "
                f"{resultado['espacios_iniciales']}\n"
            )

            archivo.write(
                f"  Espacios finales: "
                f"{resultado['espacios_finales']}\n"
            )

            archivo.write(
                f"  Espacios internos: "
                f"{resultado['espacios_internos']}\n"
            )

            archivo.write("\n")

            archivo.write(
                "CONSISTENCIA DE TEXTO\n"
            )

            archivo.write(
                "---------------------\n"
            )

            consistencia_texto = (
                informe["hallazgos"]["consistencia_texto"]
            )

            for columna, resultado in (
                consistencia_texto.items()
            ):

                if resultado["variaciones_capitalizacion"] == 0:
                    continue

                archivo.write(
                    f"{columna}:\n"
                )

                archivo.write(
                    f"  Variaciones detectadas: "
                    f"{resultado['variaciones_capitalizacion']}\n"
                )

                frecuencias = (
                    resultado["frecuencias_variaciones"]
                )

                for grupo, variantes in frecuencias.items():

                    archivo.write(
                        f"\n  Grupo: {grupo}\n"
                    )

                    for variante, frecuencia in (
                        variantes.items()
                    ):

                        archivo.write(
                            f"    {variante}: "
                            f"{frecuencia}\n"
                        )

            decisiones = {}

            for hallazgo in hallazgos:
                if (
                    hallazgo["categoria"] == "consistencia_texto"
                    and hallazgo["columna"] == columna
                ):
                    decisiones = hallazgo["detalle"]["decisiones"]
                    break

            for grupo, decision in decisiones.items():

                archivo.write(
                    f"\n  Forma dominante: "
                    f"{decision['forma_dominante']}\n"
                )

                archivo.write(
                    f"  Porcentaje dominante: "
                    f"{decision['porcentaje']:.2f}%\n"
                )

                correccion = (
                    "Sí"
                    if decision["corregible"]
                    else "No"
                )

                archivo.write(
                    f"  Corrección posible: "
                    f"{correccion}\n"
                )

                archivo.write("\n")

        archivo.write(
            "CORRECCIONES REALIZADAS\n"
        )

        archivo.write(
            "-----------------------\n"
        )

        correcciones = informe["correcciones"]

        espacios = correcciones.get(
            "espacios",
            {}
        )

        if espacios:

            archivo.write("\n")

            archivo.write(
                "ESPACIOS\n"
            )

            archivo.write(
                "--------\n"
            )

            for columna, detalle in espacios.items():

                archivo.write(
                    f"{columna}:\n"
                )

                archivo.write(
                    f"  Valores corregidos: "
                    f"{detalle['valores_corregidos']}\n"
                )

        capitalizacion = correcciones.get(
            "capitalizacion",
            {}
        )

        if capitalizacion:

            archivo.write("\n")

            archivo.write(
                "CAPITALIZACIÓN\n"
            )

            archivo.write(
                "--------------\n"
            )

            for columna, detalle in capitalizacion.items():

                archivo.write(
                    f"{columna}:\n"
                )

                archivo.write(
                    f"  Valores corregidos: "
                    f"{detalle['valores_corregidos']}\n"
                )

                archivo.write("\n")
                archivo.write("PENDIENTES\n")
                archivo.write("----------\n")

                pendientes = informe["pendientes"]

                if pendientes:
                    for pendiente in pendientes:
                        categoria = pendiente["categoria"]
                        columna = pendiente["columna"]
                        accion = pendiente["accion"]

                        if columna is None:
                            archivo.write(
                                f"{categoria}:\n"
                            )
                        else:
                            archivo.write(
                                f"{categoria} - {columna}:\n"
                            )

                        archivo.write(
                            f"  Acción: {accion}\n"
                        )
                else:
                    archivo.write(
                        "No hay pendientes.\n"
                    )
                archivo.write("\n")
                archivo.write("VALIDACIÓN\n")
                archivo.write("----------\n")

                validacion = informe["validacion"]

                registros = validacion["registros"]

                archivo.write(
                    f"Registros: "
                    f"{registros['esperados']} esperados / "
                    f"{registros['obtenidos']} obtenidos / "
                    f"{registros['valida']}\n"
                )

                procedencia = validacion["procedencia"]

                for nombre, resultado in (
                    procedencia["resultados"].items()
                ):
                    archivo.write(
                        f"{nombre}: "
                        f"{resultado['registros_esperados']} esperados / "
                        f"{resultado['registros_obtenidos']} obtenidos / "
                        f"{resultado['valida']}\n"
                    )

                archivo.write("\n")
                archivo.write("RESULTADO FINAL\n")
                archivo.write("---------------\n")
                archivo.write(
                    f"Estado: {informe['estado_final']}\n"
                )