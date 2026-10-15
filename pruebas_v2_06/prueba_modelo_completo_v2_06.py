from modelo.resultados_v2 import crear_resultado_proceso

import unittest
import pandas as pd


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
# CONSTRUIR Y PROBAR EL RESULTADO COMPLETO
# ----------------------------------------------------------

def construir_resultado_prueba():

    estado_final = "REVISAR"

    datos_finales = pd.DataFrame({
        "ID": [1, 2, 3, 4, 5, 6],
        "Nombre": [
            "Ana", "Carlos", "Luisa",
            "Pedro", "Marta", "Luis"
        ],
        "Precio": [100, 200, 150, 250, 300, 400],
        "Archivo_Origen": [
            "archivo_X.csv",
            "archivo_X.csv",
            "archivo_X.csv",
            "archivo_S.csv",
            "archivo_S.csv",
            "archivo_S.csv"
        ]
    })

    resumen = {
        "archivos_analizados": 2,
        "registros_procesados": 6,
        "categorias_con_hallazgos": [],
        "correcciones_realizadas": {},
        "pendientes": ["Precio"]
    }

    correcciones = {}
    pendientes = ["Precio"]

    return crear_resultado_proceso(
        diagnostico=diagnostico,
        decision=decision,
        ejecucion=ejecucion,
        validacion=validacion,
        estado_final=estado_final,
        datos_finales=datos_finales,
        resumen=resumen,
        correcciones=correcciones,
        pendientes=pendientes
    )


class PruebaModeloCompleto(unittest.TestCase):

    def setUp(self):
        self.resultado = construir_resultado_prueba()

    def test_contiene_las_cinco_secciones(self):
        self.assertEqual(
            set(self.resultado.keys()),
            {
                "diagnostico",
                "decision",
                "ejecucion",
                "validacion",
                "resultado"
            }
        )

    def test_conserva_estado_final(self):
        self.assertEqual(
            self.resultado["resultado"]["estado_final"],
            "REVISAR"
        )

    def test_conserva_seis_registros(self):
        datos = self.resultado["resultado"]["datos"]

        self.assertEqual(len(datos), 6)
        self.assertEqual(
            self.resultado["resultado"]["resumen"][
                "registros_procesados"
            ],
            6
        )

    def test_conserva_procedencia(self):
        datos = self.resultado["resultado"]["datos"]

        self.assertEqual(
            datos["Archivo_Origen"].value_counts().to_dict(),
            {
                "archivo_X.csv": 3,
                "archivo_S.csv": 3
            }
        )

    def test_conserva_decision_y_validacion(self):
        self.assertEqual(
            self.resultado["decision"]["estado_consolidacion"],
            "REVISAR"
        )

        self.assertEqual(
            self.resultado["validacion"]["registros"]["esperados"],
            6
        )

        self.assertEqual(
            self.resultado["validacion"]["registros"]["obtenidos"],
            6
        )

    def test_conserva_resultado_bloqueado_sin_datos(self):
        resultado = crear_resultado_proceso(
            diagnostico={},
            decision={
                "estado_consolidacion": "BLOQUEADO"
            },
            ejecucion={
                "consolidacion_realizada": False
            },
            validacion={},
            estado_final="BLOQUEADO",
            datos_finales=pd.DataFrame(),
            resumen={
                "archivos_analizados": 2,
                "registros_procesados": 0,
                "categorias_con_hallazgos": [],
                "correcciones_realizadas": {},
                "pendientes": []
            },
            correcciones={},
            pendientes=[]
        )

        self.assertEqual(
            resultado["resultado"]["estado_final"],
            "BLOQUEADO"
        )

        self.assertEqual(
            resultado["decision"]["estado_consolidacion"],
            "BLOQUEADO"
        )

        self.assertFalse(
            resultado["ejecucion"]["consolidacion_realizada"]
        )

        self.assertTrue(
            resultado["resultado"]["datos"].empty
        )

        self.assertEqual(
            resultado["resultado"]["resumen"]["registros_procesados"],
            0
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)