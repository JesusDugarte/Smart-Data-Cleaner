import unittest
from io import StringIO
from contextlib import redirect_stdout

from presentacion.consola import mostrar_compatibilidad_tipos


class PruebaPresentacionCompatibilidad(unittest.TestCase):

    def obtener_salida(
        self,
        diagnostico_conflictos_tipos,
        clasificaciones_tipos
    ):
        salida = StringIO()

        with redirect_stdout(salida):
            mostrar_compatibilidad_tipos(
                diagnostico_conflictos_tipos,
                clasificaciones_tipos
            )

        return salida.getvalue()

    def test_mostrar_clasificaciones_de_tipos(self):
        diagnostico = {
            "Precio": {
                "analisis_por_archivo": {
                    "archivo_X.csv": {
                        "valores_no_convertibles": 0
                    },
                    "archivo_S.csv": {
                        "valores_no_convertibles": 2
                    }
                }
            }
        }

        clasificaciones = {
            "Precio": {
                "archivo_X.csv": "COMPATIBLE_POTENCIAL",
                "archivo_S.csv": "SIN_DATOS"
            }
        }

        salida = self.obtener_salida(
            diagnostico,
            clasificaciones
        )

        self.assertIn("COMPATIBILIDAD DE TIPOS", salida)
        self.assertIn("Columna: Precio", salida)
        self.assertIn("archivo_X.csv", salida)
        self.assertIn("COMPATIBLE_POTENCIAL", salida)
        self.assertIn("archivo_S.csv", salida)
        self.assertIn("SIN_DATOS", salida)
        self.assertIn("Valores no convertibles:", salida)
        self.assertIn("2", salida)

    def test_sin_diferencias_de_tipos(self):
        salida = self.obtener_salida({}, {})

        self.assertIn("COMPATIBILIDAD DE TIPOS", salida)
        self.assertIn(
            "No se detectaron diferencias de tipos.",
            salida
        )


    def test_sin_datos_no_muestra_valores_no_convertibles(self):
        diagnostico = {
            "Precio": {
                "analisis_por_archivo": {
                    "archivo_X.csv": {
                        "valores_no_convertibles": 0
                    },
                    "archivo_S.csv": {
                        "valores_no_convertibles": 0
                    }
                }
            }
        }

        clasificaciones = {
            "Precio": {
                "archivo_X.csv": "COMPATIBLE_POTENCIAL",
                "archivo_S.csv": "SIN_DATOS"
            }
        }

        salida = self.obtener_salida(
            diagnostico,
            clasificaciones
        )

        self.assertIn("SIN_DATOS", salida)
        self.assertIn("COMPATIBLE_POTENCIAL", salida)
        self.assertNotIn("Valores no convertibles:", salida)


if __name__ == "__main__":
    unittest.main(verbosity=2)