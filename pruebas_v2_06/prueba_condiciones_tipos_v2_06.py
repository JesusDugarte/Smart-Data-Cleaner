import unittest

from reglas.estructura import analizar_condiciones_tipos


class PruebaAnalizarCondicionesTipos(unittest.TestCase):

    def test_todos_los_archivos_compatibles(self):
        clasificaciones = {
            "Precio": {
                "archivo_X.csv": "COMPATIBLE_POTENCIAL",
                "archivo_Y.csv": "COMPATIBLE_POTENCIAL",
            }
        }

        resultado = analizar_condiciones_tipos(clasificaciones)

        self.assertFalse(resultado["hay_incompatibilidades"])
        self.assertTrue(resultado["hay_conflictos"])
        self.assertFalse(resultado["hay_datos_insuficientes"])

    def test_un_archivo_incompatible(self):
        clasificaciones = {
            "Precio": {
                "archivo_X.csv": "COMPATIBLE_POTENCIAL",
                "archivo_Z.csv": "INCOMPATIBLE",
            }
        }

        resultado = analizar_condiciones_tipos(clasificaciones)

        self.assertTrue(resultado["hay_incompatibilidades"])
        self.assertFalse(resultado["hay_conflictos"])
        self.assertFalse(resultado["hay_datos_insuficientes"])

    def test_un_archivo_sin_datos(self):
        clasificaciones = {
            "Precio": {
                "archivo_X.csv": "COMPATIBLE_POTENCIAL",
                "archivo_S.csv": "SIN_DATOS",
            }
        }

        resultado = analizar_condiciones_tipos(clasificaciones)

        self.assertFalse(resultado["hay_incompatibilidades"])
        self.assertFalse(resultado["hay_conflictos"])
        self.assertTrue(resultado["hay_datos_insuficientes"])

    def test_incompatibilidad_y_datos_insuficientes(self):
        clasificaciones = {
            "Precio": {
                "archivo_X.csv": "INCOMPATIBLE",
                "archivo_S.csv": "SIN_DATOS",
            }
        }

        resultado = analizar_condiciones_tipos(clasificaciones)

        self.assertTrue(resultado["hay_incompatibilidades"])
        self.assertFalse(resultado["hay_conflictos"])
        self.assertTrue(resultado["hay_datos_insuficientes"])


if __name__ == "__main__":
    unittest.main(verbosity=2)