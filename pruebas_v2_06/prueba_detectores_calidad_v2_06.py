import unittest

import pandas as pd

from detectores.calidad import (
    detectar_faltantes,
    detectar_duplicados,
    detectar_espacios,
    detectar_consistencia_texto,
)


class PruebaDetectoresCalidad(unittest.TestCase):

    def test_detecta_faltantes_y_calcula_porcentaje(self):
        datos = pd.DataFrame({
            "Nombre": ["Ana", None, "", "   "]
        })

        resultado = detectar_faltantes(datos)

        self.assertEqual(resultado["Nombre"]["total"], 4)
        self.assertEqual(resultado["Nombre"]["presentes"], 1)
        self.assertEqual(resultado["Nombre"]["faltantes"], 3)
        self.assertAlmostEqual(
            resultado["Nombre"]["porcentaje_faltante"],
            75.0
        )

    def test_detecta_filas_duplicadas(self):
        datos = pd.DataFrame({
            "ID": [1, 1, 2],
            "Nombre": ["Ana", "Ana", "Luis"]
        })

        resultado = detectar_duplicados(datos)

        self.assertEqual(resultado["total"], 3)
        self.assertEqual(resultado["filas_duplicadas"], 1)
        self.assertEqual(resultado["filas_unicas"], 2)
        self.assertAlmostEqual(
            resultado["porcentaje_duplicados"],
            100 / 3
        )

    def test_detecta_tipos_de_espacios(self):
        datos = pd.DataFrame({
            "Nombre": [
                " Ana",
                "Luis ",
                "María  José",
                "Carlos"
            ]
        })

        resultado = detectar_espacios(datos)

        self.assertEqual(
            resultado["Nombre"]["valores_con_espacios"],
            3
        )
        self.assertEqual(
            resultado["Nombre"]["espacios_iniciales"],
            1
        )
        self.assertEqual(
            resultado["Nombre"]["espacios_finales"],
            1
        )
        self.assertEqual(
            resultado["Nombre"]["espacios_internos"],
            1
        )

    def test_detecta_variaciones_de_capitalizacion(self):
        datos = pd.DataFrame({
            "Ciudad": [
                "Bogota",
                "bogota",
                "BOGOTA",
                "Medellin"
            ]
        })

        resultado = detectar_consistencia_texto(datos)

        diagnostico = resultado["Ciudad"]

        self.assertEqual(
            diagnostico["variaciones_capitalizacion"],
            1
        )
        self.assertEqual(
            set(diagnostico["detalle_variaciones"]["bogota"]),
            {"Bogota", "bogota", "BOGOTA"}
        )
        self.assertEqual(
            sum(
                diagnostico["frecuencias_variaciones"]["bogota"].values()
            ),
            3
        )

    def test_detectores_responden_ante_dataframe_vacio(self):
        datos = pd.DataFrame(columns=["Nombre"])

        self.assertEqual(detectar_faltantes(datos), {})
        self.assertEqual(detectar_espacios(datos), {})
        self.assertEqual(detectar_consistencia_texto(datos), {})

        resultado_duplicados = detectar_duplicados(datos)

        self.assertEqual(resultado_duplicados["total"], 0)
        self.assertEqual(
            resultado_duplicados["filas_duplicadas"],
            0
        )
        self.assertEqual(
            resultado_duplicados["filas_unicas"],
            0
        )
        self.assertEqual(
            resultado_duplicados["porcentaje_duplicados"],
            0.0
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
