import unittest
from io import StringIO
from contextlib import redirect_stdout

from presentacion.consola import mostrar_resumen_proceso


def construir_resultado_prueba(estado_csv="VALIDADO"):
    return {
        "diagnostico": {
            "archivos_analizados": 2
        },
        "decision": {
            "estado_consolidacion": "LISTO",
            "calidad": {
                "hallazgos": [],
                "recomendaciones": []
            }
        },
        "ejecucion": {
            "consolidacion_realizada": True
        },
        "validacion": {
            "registros": {
                "realizada": True,
                "esperados": 6,
                "obtenidos": 6,
                "valida": True
            },
            "procedencia": {
                "realizada": True,
                "resultados": {}
            },
            "archivo_exportado": {
                "realizada": True,
                "archivo": "datos_limpios.csv",
                "filas": 6,
                "columnas": 4,
                "filas_correctas": True,
                "columnas_correctas": True,
                "estado": estado_csv
            }
        },
        "resultado": {
            "estado_final": "LISTO",
            "correcciones": {},
            "pendientes": []
        }
    }


class PruebaPresentacionExportacion(unittest.TestCase):

    def obtener_salida(self, resultado):
        salida = StringIO()

        with redirect_stdout(salida):
            mostrar_resumen_proceso(resultado)

        return salida.getvalue()

    def test_muestra_estado_csv_validado(self):
        resultado = construir_resultado_prueba("VALIDADO")
        salida = self.obtener_salida(resultado)

        self.assertIn("datos_limpios.csv", salida)
        self.assertIn("VALIDADO", salida)


if __name__ == "__main__":
    unittest.main(verbosity=2)
