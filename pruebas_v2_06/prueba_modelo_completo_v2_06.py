from modelo.resultados_v2 import crear_resultado_proceso


# ----------------------------------------------------------
# DIAGNÓSTICO
# ----------------------------------------------------------

diagnostico = {
    "archivos_analizados": 2,

    "estructura": {
        "columnas_comunes": [
            "ID",
            "Nombre",
            "Precio"
        ],
        "columnas_parciales": {},
        "columnas_exclusivas": {},
        "diferencias_orden": {},
        "compatibilidad": "ESTRUCTURA_EQUIVALENTE",
        "columnas_por_archivo": {
            "archivo_X.csv": [
                "ID",
                "Nombre",
                "Precio"
            ],
            "archivo_S.csv": [
                "ID",
                "Nombre",
                "Precio"
            ]
        }
    },

    "estructura_objetivo": [
        "ID",
        "Nombre",
        "Precio"
    ],

    "diferencias_tipos": {
        "Precio": {
            "tipos": [
                "int64",
                "float64"
            ],
            "cantidad_tipos": 2
        }
    },

    "compatibilidad_tipos": {
        "diagnostico": {},
        "clasificacion": {
            "Precio": {
                "archivo_X.csv": "COMPATIBLE_POTENCIAL",
                "archivo_S.csv": "SIN_DATOS"
            }
        }
    }
}


# ----------------------------------------------------------
# DECISIÓN
# ----------------------------------------------------------

decision = {
    "estado_consolidacion": "REVISAR",

    "motivos": {
        "hay_incompatibilidades": False,
        "hay_conflictos": False,
        "hay_datos_insuficientes": True
    }
}


# ----------------------------------------------------------
# EJECUCIÓN
# ----------------------------------------------------------

ejecucion = {
    "consolidacion_realizada": True,

    "procedencia": {
        "archivo_X.csv": {
            "registros_aportados": 3
        },
        "archivo_S.csv": {
            "registros_aportados": 3
        }
    }
}


# ----------------------------------------------------------
# VALIDACIÓN
# ----------------------------------------------------------

validacion = {
    "estructura": {
        "archivo_X.csv": {
            "realizada": True,
            "valida": True,
            "columnas_faltantes": [],
            "columnas_adicionales": [],
            "orden_correcto": True
        },
        "archivo_S.csv": {
            "realizada": True,
            "valida": True,
            "columnas_faltantes": [],
            "columnas_adicionales": [],
            "orden_correcto": True
        }
    },

    "registros": {
        "realizada": True,
        "esperados": 6,
        "obtenidos": 6,
        "valida": True
    }
}


# ----------------------------------------------------------
# RESULTADO
# ----------------------------------------------------------

resultado = {
    "estado_final": "REVISAR"
}


# ----------------------------------------------------------
# CONSTRUIR RESULTADO COMPLETO
# ----------------------------------------------------------

resultado_proceso = crear_resultado_proceso(
    diagnostico=diagnostico,
    decision=decision,
    ejecucion=ejecucion,
    validacion=validacion,
    resultado=resultado
)


# ----------------------------------------------------------
# MOSTRAR RESULTADO
# ----------------------------------------------------------

print()
print("RESULTADO PROCESO V2-06:")
print(resultado_proceso)