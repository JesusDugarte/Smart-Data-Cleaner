import unittest
import pandas as pd

from validacion.consolidacion import validar_procedencia
class PruebaValidacionProcedencia(unittest.TestCase):

    def test_procedencia_correcta(self):
        datos_archivo_a = pd.DataFrame({
            "ID": [1, 2]
        })

        datos_archivo_b = pd.DataFrame({
            "ID": [3, 4]
        })

        datos_consolidados = pd.DataFrame({
            "ID": [1, 2, 3, 4],
            "Archivo_Origen": [
                "archivo_A.csv",
                "archivo_A.csv",
                "archivo_B.csv",
                "archivo_B.csv"
            ]
        })

        resultado = validar_procedencia(
            datos_archivos=[
                datos_archivo_a,
                datos_archivo_b
            ],
            nombres_archivos=[
                "archivo_A.csv",
                "archivo_B.csv"
            ],
            datos_consolidados=datos_consolidados
        )

        self.assertTrue(
            resultado["archivo_A.csv"]["valida"]
        )

        self.assertTrue(
            resultado["archivo_B.csv"]["valida"]
        )
    def test_procedencia_incorrecta(self):
        datos_archivo_a = pd.DataFrame({
            "ID": [1, 2]
        })

        datos_archivo_b = pd.DataFrame({
            "ID": [3, 4]
        })

        datos_consolidados = pd.DataFrame({
            "ID": [1, 2, 3, 4],
            "Archivo_Origen": [
                "archivo_A.csv",
                "archivo_A.csv",
                "archivo_A.csv",
                "archivo_B.csv"
            ]
        })

        resultado = validar_procedencia(
            datos_archivos=[
                datos_archivo_a,
                datos_archivo_b
            ],
            nombres_archivos=[
                "archivo_A.csv",
                "archivo_B.csv"
            ],
            datos_consolidados=datos_consolidados
        )

        self.assertFalse(
            resultado["archivo_A.csv"]["valida"]
        )

        self.assertFalse(
            resultado["archivo_B.csv"]["valida"]
        )
    def test_procedencia_vacia_no_debe_considerarse_correcta(self):
        resultado = validar_procedencia(
            datos_archivos=[],
            nombres_archivos=[],
            datos_consolidados=pd.DataFrame({
                "ID": [],
                "Archivo_Origen": []
            })
        )

        validacion_correcta = (
            bool(resultado)
            and all(
                detalle["valida"]
                for detalle in resultado.values()
            )
        )

        self.assertEqual(resultado, {})
        self.assertFalse(validacion_correcta)
if __name__ == "__main__":
    unittest.main(verbosity=2)