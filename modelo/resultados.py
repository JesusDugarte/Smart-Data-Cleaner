def crear_resultado(
    cantidad_hallazgos,
    unidad_hallazgo,
    cantidad_afectados,
    unidad_afectada,
    detalle
):
    resultado = construir_resultado_consolidacion(
        total_archivos=3,
        registros_esperados=9,
        registros_obtenidos=9,
        integridad_valores=True,
        procedencia_registros={
            "archivo_A.csv": 3,
            "archivo_B.csv": 3,
            "archivo_F.csv": 3
        },
        conflictos_tipos={},
        estado_consolidacion="LISTO"
    )

    return resultado

def adaptar_faltantes(resultado_detector):
    detalle, total = resultado_detector

    resultado = crear_resultado(
        total,
        "celda",
        total,
        "celda",
        detalle
    )

    return resultado

def adaptar_espacios_externos(resultado_detector):
    total = sum(
        detalle["cantidad"]
        for detalle in resultado_detector.values()
    )

    resultado = crear_resultado(
        total,
        "celda",
        total,
        "celda",
        resultado_detector
    )

    return resultado

def normalizar_resultado(codigo, resultado_detector):

    if codigo == "V1-01":
        return adaptar_faltantes(resultado_detector)

    if codigo == "V1-02":
        return adaptar_espacios_externos(resultado_detector)

    if codigo == "V1-03":
        return adaptar_case_inconsistente(resultado_detector)

    if codigo == "V1-04":
        return adaptar_acentos_inconsistentes(resultado_detector)

    if codigo == "V1-05":
        return adaptar_representaciones_equivalentes(resultado_detector)

    if codigo == "V1-06":
        return adaptar_representacion_dominante(resultado_detector)

    if codigo == "V1-07":
        return adaptar_resultado_por_columna(resultado_detector)

    if codigo == "V1-08":
        return adaptar_resultado_vacio(
            "celda",
            "celda"
    )

    if codigo == "V1-09":
        return adaptar_telefonos_repetidos(
            resultado_detector
        )

    if codigo == "V1-10":
       return adaptar_registros_duplicados(
           resultado_detector
        )   

    if codigo == "V1-11":
        return adaptar_resultado_por_columna(resultado_detector)

    if codigo == "V1-12":
        return adaptar_multiples_formatos_fecha(
            resultado_detector
        )

    if codigo == "V1-13":
        return adaptar_resultado_vacio(
            "fila",
            "fila"
        )

    if codigo == "V1-14":
        return adaptar_resultado_vacio(
            "valor",
            "registro"
        )

    if codigo == "V1-15":
        return adaptar_resultado_vacio(
            "valor",
            "registro"
        )

    return resultado_detector

def adaptar_case_inconsistente(resultado_detector):
    cantidad_hallazgos = len(
        resultado_detector.get("Ciudad", {})
    )

    cantidad_afectados = sum(
        detalle["cantidad_afectados"]
        for detalle in resultado_detector.get("Ciudad", {}).values()
    )

    return crear_resultado(
        cantidad_hallazgos,
        "grupo",
        cantidad_afectados,
        "celda",
        resultado_detector
    )


def adaptar_acentos_inconsistentes(resultado_detector):
    cantidad_hallazgos = len(
        resultado_detector.get("Ciudad", {})
    )

    cantidad_afectados = sum(
        detalle["cantidad_afectados"]
        for detalle in resultado_detector.get("Ciudad", {}).values()
    )

    return crear_resultado(
        cantidad_hallazgos,
        "grupo",
        cantidad_afectados,
        "celda",
        resultado_detector
    )


def adaptar_representaciones_equivalentes(resultado_detector):
    cantidad_hallazgos = len(
        resultado_detector.get("Ciudad", {})
    )

    cantidad_afectados = sum(
        detalle["cantidad_afectados"]
        for detalle in resultado_detector.get("Ciudad", {}).values()
    )

    return crear_resultado(
        cantidad_hallazgos,
        "grupo",
        cantidad_afectados,
        "celda",
        resultado_detector
    )


def adaptar_representacion_dominante(resultado_detector):
    cantidad_hallazgos = len(
        resultado_detector.get("Ciudad", {})
    )

    return crear_resultado(
        cantidad_hallazgos,
        "grupo",
        0,
        "no_aplica",
        resultado_detector
    )

def adaptar_resultado_por_columna(
    resultado_detector,
    unidad_hallazgo="celda",
    unidad_afectada="celda"
):
    cantidad_hallazgos = sum(
        detalle["cantidad"]
        for detalle in resultado_detector.values()
    )

    return crear_resultado(
        cantidad_hallazgos,
        unidad_hallazgo,
        cantidad_hallazgos,
        unidad_afectada,
        resultado_detector
    )


def adaptar_resultado_vacio(
    unidad_hallazgo,
    unidad_afectada
):
    return crear_resultado(
        0,
        unidad_hallazgo,
        0,
        unidad_afectada,
        {}
    )


def adaptar_multiples_formatos_fecha(resultado_detector):
    detalle = resultado_detector.get(
        "Fecha_Registro",
        {}
    )

    cantidad_hallazgos = detalle.get(
        "cantidad_formatos",
        0
    )

    cantidad_afectados = sum(
        detalle.get("formatos", {}).values()
    )

    return crear_resultado(
        cantidad_hallazgos,
        "formato",
        cantidad_afectados,
        "fecha",
        resultado_detector
    )

def adaptar_telefonos_repetidos(resultado_detector):
    detalle = resultado_detector.get(
        "Telefono",
        {}
    )

    return crear_resultado(
        detalle.get("cantidad_hallazgos", 0),
        detalle.get("unidad_hallazgo", "valor"),
        detalle.get("cantidad_afectados", 0),
        detalle.get("unidad_afectada", "registro"),
        detalle.get("valores", {})
    )


def adaptar_registros_duplicados(resultado_detector):
    detalle = resultado_detector.get(
        "registros",
        {}
    )

    return crear_resultado(
        detalle.get("cantidad_hallazgos", 0),
        detalle.get("unidad_hallazgo", "grupo"),
        detalle.get("cantidad_afectados", 0),
        detalle.get("unidad_afectada", "fila"),
        {
            "filas": detalle.get("filas", [])
        }
    )

def construir_resultado_consolidacion(
    total_archivos,
    registros_esperados,
    registros_obtenidos,
    estructura_objetivo,
    integridad_valores,
    procedencia_registros,
    conflictos_tipos,
    compatibilidad_tipos,
    validaciones,
    estado_consolidacion
):
    return {
        "total_archivos": total_archivos,
        "registros_esperados": registros_esperados,
        "registros_obtenidos": registros_obtenidos,
        "estructura_objetivo": estructura_objetivo,
        "integridad_valores": integridad_valores,
        "procedencia": procedencia_registros,
        "conflictos_tipos": conflictos_tipos,
        "compatibilidad_tipos": compatibilidad_tipos,
        "validaciones": validaciones,
        "estado_consolidacion": estado_consolidacion
    }