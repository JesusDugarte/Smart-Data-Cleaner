import unittest
import tempfile
from pathlib import Path

from exportacion.informe import (
    construir_informe,
    exportar_informe_txt
)


def crear_informe_prueba(estado_final="COMPLETADO"):
    return construir_informe(
        resumen={
            "archivos_analizados": 2,
            "registros_procesados": 3
        },
        diagnostico_calidad={
            "faltantes": {
                "Nombre": {
                    "total": 3,
                    "presentes": 3,
                    "faltantes": 0,
                    "porcentaje_faltante": 0.0
                }
            },
            "duplicados": {
                "total": 3,
                "filas_duplicadas": 0,
                "filas_unicas": 3,
                "porcentaje_duplicados": 0.0
            },
            "espacios": {
                "Nombre": {
                    "total": 3,
                    "valores_con_espacios": 0,
                    "espacios_iniciales": 0,
                    "espacios_finales": 0,
                    "espacios_internos": 0
                }
            },
            "consistencia_texto": {
                "Nombre": {
                    "total": 3,
                    "valores_unicos": 3,
                    "variaciones_capitalizacion": 0,
                    "detalle_variaciones": {},
                    "frecuencias_variaciones": {}
                }
            }
        },
        decision_calidad={
            "hallazgos": []
        },
        correcciones={},
        pendientes=[],
        estado_final=estado_final,
        validacion={
            "calidad": {
                "calidad": []
            },
            "registros": {
                "esperados": 3,
                "obtenidos": 3,
                "valida": True
            },
            "procedencia": {
                "resultados": {}
            },
            "archivo_exportado": {
                "archivo": "datos_limpios.csv",
                "realizada": True,
                "filas": 3,
                "columnas": 2,
                "filas_correctas": True,
                "columnas_correctas": True,
                "estado": "VALIDADO"
            }
        },
        diagnostico_estructural={},
        decision_estructural={
            "motivos": {
                "hay_incompatibilidades": False,
                "hay_encabezados_duplicados": False
            }
        }
    )


class PruebaConstruirInforme(unittest.TestCase):

    def test_debe_conservar_los_datos_recibidos(self):
        resumen = {
            "archivos_analizados": 2,
            "registros_procesados": 10
        }

        diagnostico_calidad = {"faltantes": {}}
        decision_calidad = {"hallazgos": []}
        correcciones = {}
        pendientes = []
        estado_final = "COMPLETADO"
        validacion = {}
        diagnostico_estructural = {}
        decision_estructural = {}

        informe = construir_informe(
            resumen,
            diagnostico_calidad,
            decision_calidad,
            correcciones,
            pendientes,
            estado_final,
            validacion,
            diagnostico_estructural,
            decision_estructural
        )

        self.assertEqual(informe["resumen"], resumen)
        self.assertEqual(informe["diagnostico"], diagnostico_calidad)
        self.assertEqual(informe["decision"], decision_calidad)
        self.assertEqual(informe["correcciones"], correcciones)
        self.assertEqual(informe["pendientes"], pendientes)
        self.assertEqual(informe["estado_final"], estado_final)
        self.assertEqual(informe["validacion"], validacion)
        self.assertEqual(
            informe["diagnostico_estructural"],
            diagnostico_estructural
        )
        self.assertEqual(
            informe["decision_estructural"],
            decision_estructural
        )
        self.assertEqual(informe["duplicados_por_archivo"], {})


class PruebaExportarInformeTxt(unittest.TestCase):

    def test_debe_generar_txt_con_secciones_principales(self):
        informe = crear_informe_prueba()

        with tempfile.TemporaryDirectory() as carpeta:
            archivo = Path(carpeta) / "informe_prueba.txt"

            exportar_informe_txt(informe, archivo)

            self.assertTrue(archivo.exists())

            contenido = archivo.read_text(encoding="utf-8")

        self.assertIn("SMART DATA CLEANER", contenido)
        self.assertIn("INFORME DEL PROCESO", contenido)
        self.assertIn("RESUMEN", contenido)
        self.assertIn("FALTANTES", contenido)
        self.assertIn("DUPLICADOS", contenido)
        self.assertIn("ESPACIOS", contenido)
        self.assertIn("CONSISTENCIA DE TEXTO", contenido)
        self.assertIn("CORRECCIONES REALIZADAS", contenido)
        self.assertIn("PENDIENTES", contenido)
        self.assertIn("VALIDACIÓN", contenido)
        self.assertIn("ARCHIVO EXPORTADO", contenido)
        self.assertIn("VALIDACIÓN DE CORRECCIONES", contenido)
        self.assertIn("RESULTADO FINAL", contenido)
        self.assertIn("Estado: COMPLETADO", contenido)
        self.assertIn("Estado: VALIDADO", contenido)

    def test_bloqueo_por_encabezados_duplicados_debe_explicarse(self):
        informe = crear_informe_prueba(estado_final="BLOQUEADO")
        informe["decision_estructural"]["motivos"][
            "hay_encabezados_duplicados"
        ] = True
        informe["duplicados_por_archivo"] = {
            "clientes.csv": ["Nombre"]
        }
        informe["validacion"]["archivo_exportado"] = {
            "archivo": "datos_limpios.csv",
            "realizada": False,
            "filas": None,
            "columnas": None,
            "filas_correctas": False,
            "columnas_correctas": False,
            "estado": "NO_REALIZADA",
            "motivo": "El proceso quedó bloqueado."
        }

        with tempfile.TemporaryDirectory() as carpeta:
            archivo = Path(carpeta) / "informe_bloqueado.txt"
            exportar_informe_txt(informe, archivo)
            contenido = archivo.read_text(encoding="utf-8")

        self.assertIn("MOTIVO DEL BLOQUEO", contenido)
        self.assertIn("Se detectaron encabezados duplicados.", contenido)
        self.assertIn("Archivo afectado: clientes.csv", contenido)
        self.assertIn("Columnas duplicadas: ['Nombre']", contenido)
        self.assertIn("ETAPAS NO EJECUTADAS", contenido)
        self.assertIn("Consolidación: No realizada.", contenido)
        self.assertIn("Estado: NO_REALIZADA", contenido)
        self.assertIn("El proceso quedó bloqueado.", contenido)

    def test_bloqueo_por_incompatibilidad_de_tipos_debe_detallarse(self):
        informe = crear_informe_prueba(estado_final="BLOQUEADO")
        informe["decision_estructural"]["motivos"][
            "hay_incompatibilidades"
        ] = True
        informe["diagnostico_estructural"] = {
            "compatibilidad_tipos": {
                "diagnostico": {
                    "Precio": {
                        "analisis_por_archivo": {
                            "archivo_A.csv": {
                                "valores_analizados": 3,
                                "valores_convertibles": 2,
                                "valores_no_convertibles": 1
                            }
                        }
                    }
                }
            }
        }
        informe["validacion"]["archivo_exportado"] = {
            "archivo": "datos_limpios.csv",
            "realizada": False,
            "filas": None,
            "columnas": None,
            "filas_correctas": False,
            "columnas_correctas": False,
            "estado": "NO_REALIZADA",
            "motivo": "El proceso quedó bloqueado."
        }

        with tempfile.TemporaryDirectory() as carpeta:
            archivo = Path(carpeta) / "informe_incompatible.txt"
            exportar_informe_txt(informe, archivo)
            contenido = archivo.read_text(encoding="utf-8")

        self.assertIn("MOTIVO DEL BLOQUEO", contenido)
        self.assertIn("Se detectaron incompatibilidades de tipos.", contenido)
        self.assertIn("Columna: Precio", contenido)
        self.assertIn("archivo_A.csv", contenido)
        self.assertIn("Valores analizados: 3", contenido)
        self.assertIn("Valores convertibles: 2", contenido)
        self.assertIn("Valores no convertibles: 1", contenido)
        self.assertIn("ETAPAS NO EJECUTADAS", contenido)
        self.assertIn("Estado: NO_REALIZADA", contenido)

    def test_debe_informar_ambos_motivos_de_bloqueo(self):
        informe = crear_informe_prueba(estado_final="BLOQUEADO")

        informe["decision_estructural"]["motivos"][
            "hay_incompatibilidades"
        ] = True
        informe["decision_estructural"]["motivos"][
            "hay_encabezados_duplicados"
        ] = True

        informe["diagnostico_estructural"] = {
            "compatibilidad_tipos": {
                "diagnostico": {
                    "Precio": {
                        "analisis_por_archivo": {
                            "archivo_A.csv": {
                                "valores_analizados": 3,
                                "valores_convertibles": 2,
                                "valores_no_convertibles": 1
                            }
                        }
                    }
                }
            }
        }

        informe["duplicados_por_archivo"] = {
            "archivo_B.csv": ["Nombre"]
        }

        with tempfile.TemporaryDirectory() as carpeta:
            archivo = Path(carpeta) / "informe_doble_bloqueo.txt"
            exportar_informe_txt(informe, archivo)
            contenido = archivo.read_text(encoding="utf-8")

        self.assertIn("Se detectaron incompatibilidades de tipos.", contenido)
        self.assertIn("Se detectaron encabezados duplicados.", contenido)
        self.assertIn("Archivo afectado: archivo_B.csv", contenido)


if __name__ == "__main__":
    unittest.main(verbosity=2)
