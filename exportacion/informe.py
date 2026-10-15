
def construir_informe(
    resumen,
    diagnostico_calidad,
    decision_calidad,
    correcciones,
    pendientes,
    estado_final,
    validacion,
    diagnostico_estructural,
    decision_estructural,
    duplicados_por_archivo=None
):
    return {
        "resumen": resumen,
        "diagnostico": diagnostico_calidad,
        "decision": decision_calidad,
        "correcciones": correcciones,
        "pendientes": pendientes,
        "estado_final": estado_final,
        "validacion": validacion,
        "diagnostico_estructural": diagnostico_estructural,
        "decision_estructural": decision_estructural,
        "duplicados_por_archivo": duplicados_por_archivo or {}
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

        if informe["estado_final"] == "BLOQUEADO":

            archivo.write("MOTIVO DEL BLOQUEO\n")
            archivo.write("------------------\n")

            decision_estructural = informe[
                "decision_estructural"
            ]

            diagnostico_estructural = informe[
                "diagnostico_estructural"
            ]

            if decision_estructural["motivos"][
                "hay_incompatibilidades"
            ]:

                archivo.write(
                    "Se detectaron incompatibilidades "
                    "de tipos.\n"
                )

                archivo.write("\n")

                diagnostico_tipos = (
                    diagnostico_estructural[
                        "compatibilidad_tipos"
                    ]["diagnostico"]
                )

                for columna, detalle_columna in (
                    diagnostico_tipos.items()
                ):

                    archivo.write(
                        f"Columna: {columna}\n"
                    )

                    analisis_por_archivo = (
                        detalle_columna[
                            "analisis_por_archivo"
                        ]
                    )

                    for nombre_archivo, detalle in (
                        analisis_por_archivo.items()
                    ):

                        archivo.write(
                            f"  {nombre_archivo}:\n"
                        )

                        archivo.write(
                            f"    Valores analizados: "
                            f"{detalle['valores_analizados']}\n"
                        )

                        archivo.write(
                            f"    Valores convertibles: "
                            f"{detalle['valores_convertibles']}\n"
                        )

                        archivo.write(
                            f"    Valores no convertibles: "
                            f"{detalle['valores_no_convertibles']}\n"
                        )

                        archivo.write("\n")

            if decision_estructural["motivos"][
                "hay_encabezados_duplicados"
            ]:

                archivo.write(
                    "Se detectaron encabezados duplicados.\n"
                )

                duplicados_por_archivo = informe.get(
                    "duplicados_por_archivo",
                    {}
                )

                for nombre_archivo, duplicados in (
                    duplicados_por_archivo.items()
                ):
                    archivo.write(
                        f"Archivo afectado: {nombre_archivo}\n"
                    )

                    archivo.write(
                        f"Columnas duplicadas: {duplicados}\n"
                    )

                archivo.write("\n")

            archivo.write("ETAPAS NO EJECUTADAS\n")
            archivo.write("--------------------\n")

            archivo.write(
                "Consolidación: No realizada.\n"
            )

            archivo.write(
                "Análisis de calidad: No realizado.\n"
            )

            archivo.write(
                "Validación de consolidación: "
                "No realizada.\n"
            )

            archivo.write("\n")

            archivo_exportado = informe["validacion"]["archivo_exportado"]

            archivo.write(
                "ARCHIVO EXPORTADO\n"
            )

            archivo.write(
                "-----------------\n"
            )

            archivo.write(
                f"Archivo: {archivo_exportado['archivo']}\n"
            )

            if archivo_exportado["realizada"]:
                archivo.write(
                    f"Filas: {archivo_exportado['filas']}\n"
                )
                archivo.write(
                    f"Columnas: {archivo_exportado['columnas']}\n"
                )
                archivo.write(
                    f"Filas correctas: "
                    f"{archivo_exportado['filas_correctas']}\n"
                )
                archivo.write(
                    f"Columnas correctas: "
                    f"{archivo_exportado['columnas_correctas']}\n"
                )
                archivo.write(
                    f"Estado: {archivo_exportado['estado']}\n"
                )
            else:
                archivo.write(
                    f"Estado: {archivo_exportado['estado']}\n"
                )
                archivo.write(
                    f"Motivo: {archivo_exportado['motivo']}\n"
                )
            return

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

        faltantes = informe["diagnostico"]["faltantes"]
        hallazgos = informe["decision"]["hallazgos"]

        hay_faltantes = False

        for columna, resultado in faltantes.items():
            if resultado["faltantes"] == 0:
                continue

            hay_faltantes = True

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

        if not faltantes:
            archivo.write(
                "No se pudo evaluar la presencia "
                "de valores faltantes.\n"
            )

        elif not hay_faltantes:
            archivo.write(
                "No se encontraron valores faltantes.\n"
            )

        archivo.write("\n")
        archivo.write(
            "DUPLICADOS\n"
        )

        archivo.write(
            "----------\n"
        )

        duplicados = informe["diagnostico"]["duplicados"]

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

        espacios = informe["diagnostico"]["espacios"]

        hay_espacios = False

        for columna, resultado in espacios.items():

            if resultado["valores_con_espacios"] == 0:
                continue

            hay_espacios = True

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

        if not espacios:
            archivo.write(
                "No se pudo evaluar la presencia "
                "de espacios problemáticos.\n"
            )

        elif not hay_espacios:
            archivo.write(
                "No se encontraron valores con "
                "espacios problemáticos.\n"
            )

        archivo.write("\n")

        archivo.write(
            "CONSISTENCIA DE TEXTO\n"
        )

        archivo.write(
            "---------------------\n"
        )

        consistencia_texto = (
            informe["diagnostico"]["consistencia_texto"]
        )

        hay_variaciones = False

        for columna, resultado in (
            consistencia_texto.items()
        ):

            if resultado["variaciones_capitalizacion"] == 0:
                continue

            hay_variaciones = True

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

                    decisiones = (
                        hallazgo["detalle"]["decisiones"]
                    )

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

        if not consistencia_texto:
            archivo.write(
                "No se pudo evaluar la consistencia "
                "del texto.\n"
            )

        elif not hay_variaciones:
            archivo.write(
                "No se encontraron variaciones "
                "de capitalización.\n"
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
        if not espacios and not capitalizacion:
            archivo.write(
                "No se realizaron correcciones.\n"
            )

        archivo.write(
            "PENDIENTES\n"
        )

        archivo.write(
            "----------\n"
        )

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

        archivo.write(
            "VALIDACIÓN\n"
        )

        archivo.write(
            "----------\n"
        )

        validacion = informe["validacion"]

        validacion_calidad = validacion["calidad"]["calidad"]

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

        archivo_exportado = validacion["archivo_exportado"]

        archivo.write(
            "ARCHIVO EXPORTADO\n"
        )

        archivo.write(
            "-----------------\n"
        )

        archivo.write(
            f"Archivo: {archivo_exportado['archivo']}\n"
        )

        if archivo_exportado["realizada"]:
            archivo.write(
                f"Filas: {archivo_exportado['filas']}\n"
            )

            archivo.write(
                f"Columnas: {archivo_exportado['columnas']}\n"
            )

            archivo.write(
                f"Filas correctas: "
                f"{archivo_exportado['filas_correctas']}\n"
            )

            archivo.write(
                f"Columnas correctas: "
                f"{archivo_exportado['columnas_correctas']}\n"
            )

            archivo.write(
                f"Estado: {archivo_exportado['estado']}\n"
            )

        else:
            archivo.write(
                f"Estado: {archivo_exportado['estado']}\n"
            )

            archivo.write(
                f"Motivo: {archivo_exportado['motivo']}\n"
            )

        archivo.write("\n")

        archivo.write(
            "VALIDACIÓN DE CORRECCIONES\n"
        )

        archivo.write(
            "--------------------------\n"
        )

        if not validacion_calidad:
            archivo.write(
                "No se requirió validar correcciones.\n"
            )

        else:
            for resultado in validacion_calidad:

                archivo.write("\n")

                if resultado["categoria"] == "consistencia_texto":
                    nombre_categoria = "CONSISTENCIA DE TEXTO"
                else:
                    nombre_categoria = resultado["categoria"].upper()

                archivo.write(
                    f"{nombre_categoria}\n"
                )

                archivo.write(
                    f"{'-' * len(nombre_categoria)}\n"
                )

                archivo.write(
                    f"{resultado['columna']}:\n"
                )

                if resultado["categoria"] == "consistencia_texto":
                    archivo.write(
                        f"  Grupo: {resultado['grupo']}\n"
                    )

                    archivo.write(
                        f"  Forma dominante: "
                        f"{resultado['forma_dominante']}\n"
                    )

                archivo.write(
                    f"  Antes: {resultado['antes']}\n"
                )

                archivo.write(
                    f"  Despues: {resultado['despues']}\n"
                )

                archivo.write(
                    f"  Corregidos: {resultado['corregidos']}\n"
                )

                archivo.write(
                    f"  Pendientes: {resultado['pendientes']}\n"
                )

                archivo.write(
                    f"  Estado: {resultado['estado']}\n"
                )


        archivo.write("\n")

        archivo.write(
            "RESULTADO FINAL\n"
        )

        archivo.write(
            "---------------\n"
        )

        archivo.write(
            f"Estado: {informe['estado_final']}\n"
        )
