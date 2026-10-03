def mostrar_resumen(resumen):
    print("SMART DATA CLEANER — V1")
    print()

    print("RESUMEN")
    print("Estado del proceso: COMPLETADO")
    print(
        "Se procesaron",
        resumen["archivo"]["filas"],
        "registros."
    )
    print(
        "Se detectaron",
        resumen["diagnostico"]["tipos_problemas"],
        "tipos de problemas."
    )
    print(
        "Se realizaron",
        resumen["limpieza"]["transformaciones_totales"],
        "transformaciones."
    )
    print()

    print("ARCHIVO")
    print("Archivo:", resumen["archivo"]["nombre"])
    print("Filas:", resumen["archivo"]["filas"])
    print("Columnas:", resumen["archivo"]["columnas"])
    print()
    print("ESTRUCTURA")
    print(
        "Estado:",
        resumen["estructura"]["estado"]
    )
    print(
        "Columnas:",
        resumen["estructura"]["columnas"]
    )
    print(
        "Faltantes:",
        resumen["estructura"]["faltantes"]
    )
    print(
        "Adicionales:",
        resumen["estructura"]["adicionales"]
    )
    print(
        "Duplicadas:",
        resumen["estructura"]["duplicadas"]
    )
    print(
        "Colisiones:",
        resumen["estructura"]["colisiones"]
    )
    print(
        "Variantes:",
        resumen["estructura"]["variantes"]
    )
    print(
        "Equivalencias:",
        resumen["estructura"]["equivalencias"]
    )
    print()
    print("DIAGNÓSTICO")
    print(
    "Reglas evaluadas:",
    resumen["diagnostico"]["reglas_evaluadas"]
    )
    print(
    "Tipos de problemas detectados:",
    resumen["diagnostico"]["tipos_problemas"]
    )

    print("Reglas del catálogo por acción:")
    for accion, cantidad in resumen["diagnostico"]["conteo_acciones"].items():
        print(" ", accion + ":", cantidad)

    print("Hallazgos por acción:")
    for accion, cantidad in resumen["diagnostico"]["hallazgos_por_accion"].items():
        print(" ", accion + ":", cantidad)

        print()
    print("DIAGNÓSTICO NUMÉRICO")

    diagnostico_numerico_v2_03 = resumen["diagnostico"]["numerico_v2_03"]

    print(
        "Columnas analizadas:",
        diagnostico_numerico_v2_03["columnas_analizadas"]
    )

    print(
        "Columnas protegidas:",
        diagnostico_numerico_v2_03["protegidas"]
    )

    print(
        "Columnas ignoradas:",
        diagnostico_numerico_v2_03["ignoradas"]
    )

    print(
        "Columnas para convertir:",
        diagnostico_numerico_v2_03["convertir"]
    )

    print(
        "Columnas para revisar:",
        diagnostico_numerico_v2_03["revisar"]
    )

    print()

    print("LIMPIEZA")
    print(
        "Celdas limpiadas:",
        resumen["limpieza"]["celdas_limpiadas"]
    )
    print(
        "Celdas convertidas:",
        resumen["limpieza"]["celdas_convertidas"]
    )
    print(
        "Transformaciones totales:",
        resumen["limpieza"]["transformaciones_totales"]
    )

    print("Cambios por columna:")

    for columna, cambios in resumen["limpieza"]["cambios_por_columna"].items():

        print(" ", columna)

        print(
            "    Limpieza:",
            cambios["LIMPIEZA"]
        )

        print(
            "    Conversión:",
            cambios["CONVERSION"]
        )

        print(
            "    Total:",
            cambios["TOTAL"]
        )

    print()

    print("VALIDACIÓN")
    print(
        "Reglas de limpieza validadas:",
        resumen["validacion"]["reglas_limpieza_validadas"]
    )
    print(
        "Reglas con pendientes:",
        resumen["validacion"]["reglas_con_pendientes"]
    )

    print()

    print("RESULTADO")
    print(
        "Archivo generado:",
        resumen["exportacion"]["archivo"]
    )
    print(
        "Estado:",
        resumen["exportacion"]["estado"]
    )        

def traducir_compatibilidad(codigo):
    traducciones = {
        "ESTRUCTURA_EQUIVALENTE": "Estructuras equivalentes",
        "ESTRUCTURA_PARCIAL": "Estructura parcialmente compatible",
        "SIN_BASE_COMUN": "No se encontró una base estructural común",
        "ESTRUCTURA_COMUN_TIPOS_DIFERENTES": (
            "Estructura común con diferencias de tipos"
        )
    }

    return traducciones.get(codigo, codigo)

def mostrar_diagnostico_estructural(diagnostico):
    print()
    print("DIAGNÓSTICO ESTRUCTURAL")
    print("-----------------------")

    print("Archivos analizados:", diagnostico["total_archivos"])

    print()
    print("COLUMNAS COMUNES")

    if diagnostico["columnas_comunes"]:
        for columna in diagnostico["columnas_comunes"]:
            print("  •", columna)
    else:
        print("  Ninguna")

    print()
    print("COLUMNAS PARCIALES")

    if diagnostico["columnas_parciales"]:
        for columna, informacion in diagnostico["columnas_parciales"].items():
            print(
                "  •",
                columna,
                "→ presente en",
                informacion["frecuencia"],
                "de",
                informacion["total_archivos"],
                "archivo(s)"
            )
    else:
        print("  Ninguna")

    print()
    print("COLUMNAS EXCLUSIVAS")

    if diagnostico["columnas_exclusivas"]:
        for columna, informacion in diagnostico["columnas_exclusivas"].items():
            print(
                "  •",
                columna,
                "→ presente en",
                informacion["frecuencia"],
                "archivo(s)"
            )
    else:
        print("  Ninguna")

    print()
    print("DIFERENCIAS DE TIPOS")

    if diagnostico["diferencias_tipos"]:
        for columna, informacion in diagnostico["diferencias_tipos"].items():
            print(
                "  •",
                columna,
                "→",
                informacion
            )
    else:
        print("  Ninguna")

    print()
    print("DIFERENCIAS DE ORDEN")

    if diagnostico["diferencias_orden"]:
        for archivo, informacion in diagnostico["diferencias_orden"].items():
            print("  •", archivo)
    else:
        print("  Ninguna")

    print()
    print("COMPATIBILIDAD")
    print(
        " ",
        traducir_compatibilidad(diagnostico["compatibilidad"])
    )

def mostrar_compatibilidad_tipos(
    diagnostico_conflictos_tipos,
    clasificaciones_tipos
):
    print()
    print("COMPATIBILIDAD DE TIPOS")

    if not clasificaciones_tipos:
        print("No se detectaron diferencias de tipos.")
        return

    for columna, clasificaciones in clasificaciones_tipos.items():
        print(f"Columna: {columna}")

        diagnostico_columna = diagnostico_conflictos_tipos[columna]
        analisis_por_archivo = (
            diagnostico_columna["analisis_por_archivo"]
        )

        for archivo, clasificacion in clasificaciones.items():
            print(
                f"  {archivo} → {clasificacion}"
            )

            resultado = analisis_por_archivo[archivo]

            if resultado["valores_no_convertibles"] > 0:
                print(
                    "                 "
                    "Valores no convertibles:",
                    resultado["valores_no_convertibles"]
                )

def mostrar_decision(estado_consolidacion, motivos):
    print()
    print("DECISIÓN")
    print(
        "Estado de consolidación:",
        estado_consolidacion
    )

    if motivos["hay_incompatibilidades"]:
        print(
            "Motivo: Se detectaron "
            "incompatibilidades de tipos."
        )
    elif motivos["hay_datos_insuficientes"]:
        print(
            "Motivo: Hay datos insuficientes "
            "para analizar completamente los tipos."
        )
    elif motivos["hay_conflictos"]:
        print(
            "Motivo: Se detectaron diferencias "
            "de tipos compatibles potencialmente."
        )

def mostrar_consolidacion_bloqueada(
    compatibilidad_estructural,
    hay_incompatibilidades
):

    print()

    print("CONSOLIDACIÓN BLOQUEADA.")

    if compatibilidad_estructural == "SIN_BASE_COMUN":

        print(
            "No existe una base estructural común "
            "entre los archivos."
        )

    elif hay_incompatibilidades:

        print(
            "No se generará una consolidación "
            "debido a incompatibilidades de tipos."
        )

    else:

        print(
            "No se generará una consolidación "
            "debido a condiciones incompatibles."
        )

def mostrar_validacion_registros(
    registros_esperados,
    registros_obtenidos,
    registros_validos
):
    print()
    print("VALIDACIÓN DE REGISTROS:")

    print(
        "Esperados:",
        registros_esperados
    )

    print(
        "Obtenidos:",
        registros_obtenidos
    )

    print(
        "Válida:",
        registros_validos
    )

def mostrar_diagnostico_estructural(
    diagnostico_estructural
):
    print()
    print("DIAGNÓSTICO ESTRUCTURAL")
    print()

    print(
        "Archivos analizados:",
        diagnostico_estructural["total_archivos"]
    )

    print()
    print("Columnas comunes:")

    for columna in diagnostico_estructural["columnas_comunes"]:
        print(" ", columna)

    columnas_parciales = (
        diagnostico_estructural["columnas_parciales"]
    )

    if columnas_parciales:
        print()
        print("Columnas parciales:")

        for columna, informacion in columnas_parciales.items():
            print(
                " ",
                columna,
                "→ presente en",
                informacion["frecuencia"],
                "de",
                informacion["total_archivos"],
                "archivos"
            )

    columnas_exclusivas = (
        diagnostico_estructural["columnas_exclusivas"]
    )

    if columnas_exclusivas:
        print()
        print("Columnas exclusivas:")

        for columna, informacion in columnas_exclusivas.items():
            print(
                " ",
                columna,
                "→ presente en",
                informacion["frecuencia"],
                "de",
                informacion["total_archivos"],
                "archivos"
            )

    diferencias_orden = (
        diagnostico_estructural["diferencias_orden"]
    )

    if diferencias_orden:
        print()
        print("Diferencias de orden:")

        for archivo, informacion in diferencias_orden.items():
            print(
                " ",
                archivo
            )

    print()
    print(
        "Compatibilidad estructural:",
        diagnostico_estructural["compatibilidad"]
    )

def mostrar_estructura_objetivo(
    estructura_objetivo
):
    print()
    print("ESTRUCTURA OBJETIVO:")
    print(estructura_objetivo)

def mostrar_resumen_proceso(resultado_proceso):

    print()
    print("===================================")
    print("SMART DATA CLEANER — V2-06")
    print("===================================")

    diagnostico = resultado_proceso["diagnostico"]
    decision = resultado_proceso["decision"]
    ejecucion = resultado_proceso["ejecucion"]
    validacion = resultado_proceso["validacion"]

    print()
    print("RESUMEN")

    print(
        "Archivos analizados:",
        diagnostico["archivos_analizados"]
    )

    print()
    print("DECISIÓN")

    print(
        "Estado de consolidación:",
        decision["estado_consolidacion"]
    )

    print()
    print("EJECUCIÓN")

    print(
        "Consolidación realizada:",
        ejecucion["consolidacion_realizada"]
    )

    print()
    print("CALIDAD DE DATOS")

    if "calidad" in diagnostico:

        calidad_proceso = diagnostico["calidad"]
        calidad = calidad_proceso["diagnostico"]

        print()
        print("FALTANTES")

        for columna, resultado in calidad["faltantes"].items():

            print(
                columna + ":",
                resultado["faltantes"],
                "faltantes /",
                resultado["total"],
                "total ("
                + f"{resultado['porcentaje_faltante']:.2f}%"
                + ")"
            )

        print()
        print("DUPLICADOS")

        duplicados = calidad["duplicados"]

        print(
            "Filas totales:",
            duplicados["total"]
        )

        print(
            "Filas duplicadas:",
            duplicados["filas_duplicadas"]
        )

        print(
            "Filas únicas:",
            duplicados["filas_unicas"]
        )

        print(
            "Porcentaje duplicados:",
            f"{duplicados['porcentaje_duplicados']:.2f}%"
        )

        print()
        print("ESPACIOS")

        espacios = calidad["espacios"]

        for columna, resultado in espacios.items():

            print(
                columna + ":",
                resultado["valores_con_espacios"],
                "valores con espacios /",
                resultado["total"],
                "total"
            )

            print(
                "  Iniciales:",
                resultado["espacios_iniciales"]
            )

            print(
                "  Finales:",
                resultado["espacios_finales"]
            )

            print(
                "  Internos:",
                resultado["espacios_internos"]
            )

        print()
        print("CONSISTENCIA DE TEXTO")

        consistencia_texto = calidad["consistencia_texto"]

        for columna, resultado in consistencia_texto.items():

            print()
            print(columna + ":")

            print(
                "  Valores analizados:",
                resultado["total"]
            )

            print(
                "  Valores únicos:",
                resultado["valores_unicos"]
            )

            print(
                "  Variaciones de capitalización:",
                resultado["variaciones_capitalizacion"]
            )

            if resultado["detalle_variaciones"]:

                print()
                print("  Detalle de variaciones:")

                for clave, variantes in resultado[
                    "detalle_variaciones"
                ].items():

                    print("   ", clave + ":")

                    for variante in variantes:

                        print(
                            "      ",
                            variante
                        )

        print()
        print("HALLAZGOS DE CALIDAD")

        interpretacion = calidad["interpretacion"]

        for hallazgo in interpretacion["hallazgos"]:

            print()
            print("Categoría:", hallazgo["categoria"])
            print("Columna:", hallazgo["columna"])
            print("Problema:", hallazgo["problema"])
            print("Detalle:", hallazgo["detalle"])

        print()
        print("RECOMENDACIONES")

        acciones = {
            "revisar_valores_faltantes":
                "Revisar valores faltantes",

            "revisar_filas_duplicadas":
                "Revisar filas duplicadas",

            "normalizar_espacios":
                "Normalizar espacios",

            "normalizar_capitalizacion":
                "Normalizar capitalización"
        }

        for recomendacion in interpretacion["recomendaciones"]:

            columna = recomendacion["columna"]

            if columna is None:
                columna = "Filas"

            accion = recomendacion["accion"]

            accion_mostrada = acciones.get(
                accion,
                accion
            )

            print(
                f"- {columna} → {accion_mostrada}"
            )

        print()
        print("CORRECCIONES REALIZADAS")

        correcciones = calidad_proceso["correcciones"]

        if correcciones:

            for categoria, resultados in correcciones.items():

                for columna, detalle in resultados.items():

                    print(
                        f"- {columna} → "
                        f"{detalle['valores_corregidos']} "
                        "valores corregidos"
                    )

        else:

            print("Ninguna")

        print()
        print("PENDIENTES")

        pendientes = calidad_proceso["pendientes"]

        if pendientes:

            for pendiente in pendientes:

                columna = pendiente["columna"]

                if columna is None:
                    columna = "Filas"

                accion = pendiente["accion"]

                accion_mostrada = acciones.get(
                    accion,
                    accion
                )

                print(
                    f"- {columna} → {accion_mostrada}"
                )

        else:

            print("Ninguna")

    else:

        print(
            "Análisis de calidad no realizado."
        )

    print()
    print("VALIDACIÓN")

    registros = validacion["registros"]

    if registros["realizada"]:

        print(
            "Registros:",
            registros["esperados"],
            "esperados /",
            registros["obtenidos"],
            "obtenidos /",
            registros["valida"]
        )

    procedencia = validacion["procedencia"]

    if procedencia["realizada"]:

        for archivo, resultado in procedencia["resultados"].items():

            print(
                archivo + ":",
                resultado["registros_esperados"],
                "esperados /",
                resultado["registros_obtenidos"],
                "obtenidos /",
                resultado["valida"]
            )

    else:

        print(
            "Validación de consolidación no realizada."
        )

    print()
    print("RESULTADO")

    print(
        "Estado final:",
        resultado_proceso["resultado"]["estado_final"]
    )