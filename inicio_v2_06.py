from pathlib import Path

import pandas as pd

from proceso_v2_06 import (
    cargar_archivos_csv,
    diagnosticar_estructuras_archivos
)

from exportacion.excel import (
    crear_libro_informe,
    construir_resumen as construir_resumen_excel,
    construir_calidad,
    construir_calidad_faltantes,
    construir_calidad_duplicados,
    construir_calidad_espacios,
    construir_calidad_consistencia,
    construir_correcciones,
    construir_pendientes,
    construir_datos_limpios,
    guardar_libro_informe,
    ajustar_ancho_columnas,
    formatear_resumen,
    formatear_calidad,
    formatear_correcciones,
    formatear_pendientes,
    formatear_datos_limpios
)

from exportacion.informe import construir_informe
from exportacion.informe import exportar_informe_txt

from exportacion.datos import exportar_datos_csv


from analisis.calidad import procesar_calidad

from presentacion.consola import (
    mostrar_compatibilidad_tipos,
    mostrar_decision,
    mostrar_validacion_registros,
    mostrar_diagnostico_estructural,
    mostrar_estructura_objetivo,
    mostrar_resumen_proceso,
    mostrar_consolidacion_bloqueada
)

from validacion.consolidacion import (
    validar_cantidad_registros,
    validar_procedencia
)

from reglas.estructura import (
    determinar_estado_consolidacion,
    analizar_condiciones_tipos,
    clasificar_compatibilidad_tipos_varios,
    determinar_estado_final,
)

from limpieza.estructura import (
    agregar_columnas_faltantes,
    alinear_columnas
)

from validacion.estructura import (
    validar_estructura
)

from validacion.archivo import (
    validar_archivo_exportado
)

from detectores.conflictos_tipos import (
    construir_diagnostico_conflictos_numericos
)

from modelo.resultados_v2 import (
    crear_resultado_proceso,
    construir_datos_finales,
    construir_resumen
)

# ----------------------------------------------------------
# Configuración
# ----------------------------------------------------------

CARPETA_ENTRADA = Path("pruebas_v2_06")


# ----------------------------------------------------------
# Localizar archivos CSV
# ----------------------------------------------------------


archivos_csv = [
    Path("pruebas_v2_06/archivo_X.csv"),
    Path("pruebas_v2_06/archivo_W.csv")
]

# ----------------------------------------------------------
# Cargar archivos y detectar encabezados duplicados
# ----------------------------------------------------------

resultado_carga = cargar_archivos_csv(
    archivos_csv
)

duplicados_por_archivo = resultado_carga[
    "duplicados_por_archivo"
]

datos_archivos = resultado_carga[
    "datos_archivos"
]

nombres_archivos = resultado_carga[
    "nombres_archivos"
]

print()
print("DIAGNÓSTICO DE ENCABEZADOS DUPLICADOS:")

if duplicados_por_archivo:
    for nombre, duplicados in duplicados_por_archivo.items():
        print(f"Archivo: {nombre}")
        print(f"Columnas duplicadas: {duplicados}")
else:
    print("No se detectaron encabezados duplicados.")

# print()
# ----------------------------------------------------------
# Diagnóstico de estructura común
# ----------------------------------------------------------

# ----------------------------------------------------------
# Diagnóstico estructural y construcción de estructura objetivo
# ----------------------------------------------------------

resultado_estructural = diagnosticar_estructuras_archivos(
    datos_archivos,
    nombres_archivos
)

diagnostico_estructural = resultado_estructural[
    "diagnostico_estructural"
]

columnas_comunes = diagnostico_estructural[
    "columnas_comunes"
]

mostrar_diagnostico_estructural(
    diagnostico_estructural
)

estructura_objetivo = resultado_estructural[
    "estructura_objetivo"
]

mostrar_estructura_objetivo(
    estructura_objetivo
)

# ----------------------------------------------------------
# Homogeneizar estructuras
# ----------------------------------------------------------

datos_homogeneizados = []

validaciones_estructura = {}

for datos, archivo in zip(
    datos_archivos,
    archivos_csv
):

    datos_limpios = agregar_columnas_faltantes(
        datos,
        estructura_objetivo
    )

    datos_limpios = alinear_columnas(
        datos_limpios,
        estructura_objetivo
    )

    # Validar ANTES de agregar metadatos técnicos

    resultado_estructura = validar_estructura(
        datos_limpios,
        estructura_objetivo
    )

    validaciones_estructura[archivo.name] = resultado_estructura

#    print()
#    print(
#        "Validación estructural:",
#        archivo.name,
#        resultado_estructura
#    )

    # Agregar procedencia después de validar estructura

    datos_limpios["Archivo_Origen"] = (
        archivo.name
    )

    datos_homogeneizados.append(
        datos_limpios
    )


# ----------------------------------------------------------
# Diagnóstico de diferencias de tipos
# ----------------------------------------------------------
diferencias_tipos = diagnostico_estructural[
    "diferencias_tipos"
]

# ----------------------------------------------------------
# Diagnóstico de compatibilidad de tipos
# ----------------------------------------------------------

diagnostico_conflictos_tipos = (
    construir_diagnostico_conflictos_numericos(
        datos_archivos,
        nombres_archivos,
        diferencias_tipos
    )
)

# ----------------------------------------------------------
# Clasificación de compatibilidad
# ----------------------------------------------------------
clasificaciones_tipos = (
    clasificar_compatibilidad_tipos_varios(
        diagnostico_conflictos_tipos
    )
)

mostrar_compatibilidad_tipos(
    diagnostico_conflictos_tipos,
    clasificaciones_tipos
)

# ----------------------------------------------------------
# Analizar condiciones globales de tipos
# ----------------------------------------------------------

condiciones_tipos = analizar_condiciones_tipos(
    clasificaciones_tipos
)

hay_incompatibilidades = condiciones_tipos["hay_incompatibilidades"]
hay_conflictos = condiciones_tipos["hay_conflictos"]
hay_datos_insuficientes = condiciones_tipos["hay_datos_insuficientes"]

estado_consolidacion = determinar_estado_consolidacion(
    compatibilidad_estructural=diagnostico_estructural[
        "compatibilidad"
    ],
    hay_conflictos=hay_conflictos,
    hay_incompatibilidades=hay_incompatibilidades,
    hay_datos_insuficientes=hay_datos_insuficientes
)

if duplicados_por_archivo:
    estado_consolidacion = "BLOQUEADO"

# ----------------------------------------------------------
# Consolidar archivos
# ----------------------------------------------------------

diagnostico = {
    "archivos_analizados": len(archivos_csv),
    "estructura": {
        "columnas_comunes": columnas_comunes,
        "columnas_parciales": diagnostico_estructural["columnas_parciales"],
        "columnas_exclusivas": diagnostico_estructural["columnas_exclusivas"],
        "diferencias_orden": diagnostico_estructural["diferencias_orden"],
        "compatibilidad": diagnostico_estructural["compatibilidad"],
        "columnas_por_archivo": diagnostico_estructural["columnas_por_archivo"]
    },
    "estructura_objetivo": estructura_objetivo,
    "diferencias_tipos": diferencias_tipos,
    "compatibilidad_tipos": {
        "diagnostico": diagnostico_conflictos_tipos,
        "clasificacion": clasificaciones_tipos
    },
}

decision = {
    "estado_consolidacion": estado_consolidacion,
    "compatibilidad_estructural":
        diagnostico_estructural["compatibilidad"],
    "motivos": {
        "hay_incompatibilidades": hay_incompatibilidades,
        "hay_conflictos": hay_conflictos,
        "hay_datos_insuficientes": hay_datos_insuficientes,
        "hay_diferencias_estructurales":
            diagnostico_estructural["compatibilidad"] == "ESTRUCTURA_PARCIAL",
        "hay_encabezados_duplicados": bool(duplicados_por_archivo)
    }
}

mostrar_decision(
    estado_consolidacion,
    decision["motivos"]
)

consolidacion_realizada = (
    estado_consolidacion != "BLOQUEADO"
)

procedencia = {}

for datos, nombre in zip(
    datos_archivos,
    nombres_archivos
):
    procedencia[nombre] = {
        "registros_aportados": len(datos)
    }

ejecucion = {
    "consolidacion_realizada": consolidacion_realizada,
    "procedencia": procedencia
}

validacion = {
    "estructura": {
        "resultados_por_archivo": validaciones_estructura
    }
}

validacion_registros_realizada = False
registros_esperados = None
registros_obtenidos = None
registros_validos = None

validacion_procedencia_realizada = False
resultado_procedencia = None


resultado_archivo_exportado = {
    "realizada": False,
    "archivo": "datos_limpios.csv",
    "filas": None,
    "columnas": None,
    "filas_correctas": False,
    "columnas_correctas": False,
    "estado": "NO_REALIZADA",
    "motivo": (
        "La exportación no se realizó "
        "porque el proceso quedó BLOQUEADO. "
        "Si el archivo existe, puede pertenecer "
        "a una ejecución anterior."
    )
}


if estado_consolidacion == "BLOQUEADO":

    mostrar_consolidacion_bloqueada(
        compatibilidad_estructural=diagnostico_estructural[
            "compatibilidad"
        ],
        hay_incompatibilidades=hay_incompatibilidades,
        duplicados_por_archivo=duplicados_por_archivo
    )

    estado_final = determinar_estado_final(
        estado_consolidacion=estado_consolidacion,
        validacion_registros_realizada=False,
        validacion_registros_correcta=None,
        validacion_procedencia_realizada=False,
        validacion_procedencia_correcta=None
    )

    datos_finales = pd.DataFrame()

    resultado_calidad = {
        "datos": pd.DataFrame(),

        "diagnostico": {
            "faltantes": {},
            "duplicados": {
                "total": 0,
                "filas_duplicadas": 0,
                "filas_unicas": 0,
                "porcentaje_duplicados": 0.0
            },
            "espacios": {},
            "consistencia_texto": {}
        },

        "decision": {
            "calidad": {
                "hallazgos": [],
                "recomendaciones": [],
                "estado": "REVISAR"
            }
        },

        "ejecucion": {
            "calidad": {
                "realizada": False
            },
            "correcciones": {}
        },

        "validacion": {
            "calidad": []
        },

        "resultado": {
            "correcciones": {},
            "pendientes": [
                {
                    "categoria": "consolidacion",
                    "columna": None,
                    "accion": "resolver_incompatibilidades"
                }
            ]
        }
    }
    resumen = {
        "archivos_analizados": len(archivos_csv),
        "registros_procesados": 0,
        "categorias_con_hallazgos": [],
        "correcciones_realizadas": {},
        "pendientes": resultado_calidad["resultado"]["pendientes"]
    }

else:

    datos_consolidados = pd.concat(
        datos_homogeneizados,
        ignore_index=True
    )

    datos_para_calidad = datos_consolidados.drop(
    columns=["Archivo_Origen"]
    )


    resultado_calidad = procesar_calidad(
        datos_para_calidad
    )

    datos_corregidos = resultado_calidad["datos"]

    datos_finales = construir_datos_finales(
        datos_corregidos,
        datos_consolidados
    )

    resumen = construir_resumen(
        diagnostico,
        resultado_calidad["diagnostico"],
        resultado_calidad["decision"]["calidad"],
        datos_finales,
        resultado_calidad["ejecucion"]["correcciones"],
        resultado_calidad["resultado"]["pendientes"]
    )

    diagnostico["calidad"] = resultado_calidad["diagnostico"]

    # ------------------------------------------------------
    # Validar cantidad de registros
    # ------------------------------------------------------

    resultado_validacion = validar_cantidad_registros(
        datos_archivos,
        datos_consolidados
    )

    registros_esperados = resultado_validacion[
        "registros_esperados"
    ]

    registros_obtenidos = resultado_validacion[
        "registros_obtenidos"
    ]

    registros_validos = resultado_validacion[
        "valida"
    ]

    validacion_registros_realizada = True

    resultado_procedencia = validar_procedencia(
        datos_archivos,
        nombres_archivos,
        datos_consolidados
    )
    
    validacion_procedencia_realizada = True

    validacion_procedencia_correcta = all(
        resultado["valida"]
        for resultado in resultado_procedencia.values()
    )

    estado_final = determinar_estado_final(
        estado_consolidacion=estado_consolidacion,
        estado_calidad=resultado_calidad["decision"]["calidad"]["estado"],
        validacion_registros_realizada=validacion_registros_realizada,
        validacion_registros_correcta=registros_validos,
        validacion_procedencia_realizada=validacion_procedencia_realizada,
        validacion_procedencia_correcta=validacion_procedencia_correcta
    )


    if estado_final != "BLOQUEADO":
        exportar_datos_csv(
            datos_finales,
            "salida/datos_limpios.csv"
        )

        resultado_archivo_exportado = validar_archivo_exportado(
            Path("salida/datos_limpios.csv"),
            datos_finales.columns.tolist(),
            len(datos_finales)
        )

        resultado_archivo_exportado["realizada"] = True


        if resultado_archivo_exportado["estado"] in {
            "REVISAR",
            "ERROR"
        }:
            estado_final = "REVISAR"


    mostrar_validacion_registros(
        registros_esperados,
        registros_obtenidos,
        registros_validos
    )
# ----------------------------------------------------------
# Mostrar estado final
# ----------------------------------------------------------

validacion["registros"] = {
    "realizada": validacion_registros_realizada,
    "esperados": registros_esperados,
    "obtenidos": registros_obtenidos,
    "valida": registros_validos
}

validacion["procedencia"] = {
    "realizada": validacion_procedencia_realizada,
    "resultados": resultado_procedencia
}

validacion["calidad"] = (
    resultado_calidad["validacion"]
)

validacion["archivo_exportado"] = (
    resultado_archivo_exportado
)

informe = construir_informe(
    resumen=resumen,
    diagnostico_calidad=resultado_calidad["diagnostico"],
    decision_calidad=resultado_calidad["decision"]["calidad"],
    correcciones=resultado_calidad["ejecucion"]["correcciones"],
    pendientes=resultado_calidad["resultado"]["pendientes"],
    estado_final=estado_final,
    validacion=validacion,
    diagnostico_estructural=diagnostico,
    decision_estructural=decision,
    duplicados_por_archivo=duplicados_por_archivo
)


exportar_informe_txt(
            informe,
            "salida/informe_proceso.txt"
        )

decision["calidad"] = resultado_calidad["decision"]["calidad"]

resultado_proceso = crear_resultado_proceso(
    diagnostico,
    decision,
    ejecucion,
    validacion,
    estado_final,
    datos_finales,
    resumen,
    resultado_calidad["ejecucion"]["correcciones"],
    resultado_calidad["resultado"]["pendientes"]
)

#print()
#print("AUDITORÍA RESULTADO_PROCESO")
#print("Diagnóstico:", resultado_proceso["diagnostico"].keys())
#print("Decisión:", resultado_proceso["decision"].keys())
#print("Ejecución:", resultado_proceso["ejecucion"].keys())
#print("Validación:", resultado_proceso["validacion"].keys())
#print("Resultado:", resultado_proceso["resultado"].keys())
#print("Estado final:", resultado_proceso["resultado"]["estado_final"])

libro = crear_libro_informe()

construir_resumen_excel(
    libro["Resumen"],
    resultado_proceso
)

formatear_resumen(
    libro["Resumen"]
)

construir_calidad(
    libro["Calidad"],
    resultado_calidad
)

formatear_calidad(
    libro["Calidad"]
)

construir_correcciones(
    libro["Correcciones"],
    resultado_proceso
)

formatear_correcciones(
    libro["Correcciones"]
)

construir_pendientes(
    libro["Pendientes"],
    resultado_proceso
)

formatear_pendientes(
    libro["Pendientes"]
)

construir_datos_limpios(
    libro["Datos_Limpios"],
    resultado_proceso
)

formatear_datos_limpios(
    libro["Datos_Limpios"]
)

for hoja in libro.worksheets:

    ajustar_ancho_columnas(hoja)

try:
    guardar_libro_informe(
        libro,
        "salida/informe_proceso.xlsx"
    )

    print()
    print("Informe Excel guardado correctamente.")

except OSError as error:
    print()
    print("ERROR: No se pudo guardar el informe Excel.")
    print(f"Detalle: {error}")

mostrar_resumen_proceso(
    resultado_proceso
)

#print()
#print("RESULTADO PROCESO V2-06:")
#print(resultado_proceso)

#print()
#print("ESTADO FINAL:", estado_final)
