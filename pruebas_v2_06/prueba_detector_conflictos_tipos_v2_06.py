import unittest
import pandas as pd
from pathlib import Path

from detectores.conflictos_tipos import analizar_compatibilidad_numerica
from detectores.conflictos_tipos import construir_diagnostico_conflictos_numericos


class PruebaAnalizarCompatibilidadNumerica(unittest.TestCase):

    def test_todos_los_valores_son_convertibles(self):
        datos = pd.DataFrame({
            "Precio": [1000, 2500]
        })

        resultado = analizar_compatibilidad_numerica(
            datos,
            "Precio"
        )

        self.assertEqual(resultado["valores_totales"], 2)
        self.assertEqual(resultado["valores_analizados"], 2)
        self.assertEqual(resultado["valores_faltantes"], 0)
        self.assertEqual(resultado["valores_convertibles"], 2)
        self.assertEqual(resultado["valores_no_convertibles"], 0)

    def test_detecta_valores_no_convertibles(self):
        datos = pd.DataFrame({
            "Precio": [1000, "sin precio", 2500]
        })

        resultado = analizar_compatibilidad_numerica(
            datos,
            "Precio"
        )

        self.assertEqual(resultado["valores_totales"], 3)
        self.assertEqual(resultado["valores_analizados"], 3)
        self.assertEqual(resultado["valores_faltantes"], 0)
        self.assertEqual(resultado["valores_convertibles"], 2)
        self.assertEqual(resultado["valores_no_convertibles"], 1)

    def test_identifica_valores_faltantes(self):
        datos = pd.DataFrame({
            "Precio": [1000, None, 2500]
        })

        resultado = analizar_compatibilidad_numerica(
            datos,
            "Precio"
        )

        self.assertEqual(resultado["valores_totales"], 3)
        self.assertEqual(resultado["valores_analizados"], 2)
        self.assertEqual(resultado["valores_faltantes"], 1)
        self.assertEqual(resultado["valores_convertibles"], 2)
        self.assertEqual(resultado["valores_no_convertibles"], 0)

    def test_diagnostico_de_los_dos_csv_convertibles(self):
        raiz_proyecto = Path(__file__).resolve().parent.parent

        archivo_a = raiz_proyecto / "pruebas_v2_06" / "archivo_tipos_convertibles_A.csv"
        archivo_b = raiz_proyecto / "pruebas_v2_06" / "archivo_tipos_convertibles_B.csv"

        datos_a = pd.read_csv(archivo_a)
        datos_b = pd.read_csv(archivo_b)

        datos_archivos = [datos_a, datos_b]
        nombres_archivos = [
            archivo_a.name,
            archivo_b.name,
        ]

        diferencias_tipos = {
            "Precio": {
                "tipos": ["int64", "object"],
                "cantidad_tipos": 2,
                "archivos_por_tipo": {
                    "int64": [archivo_a.name],
                    "object": [archivo_b.name],
                },
            }
        }

        diagnostico = construir_diagnostico_conflictos_numericos(
            datos_archivos,
            nombres_archivos,
            diferencias_tipos,
        )

        self.assertIn("Precio", diagnostico)

        for nombre in nombres_archivos:
            resultado = diagnostico["Precio"]["analisis_por_archivo"][nombre]

            self.assertEqual(resultado["valores_totales"], 2)
            self.assertEqual(resultado["valores_analizados"], 2)
            self.assertEqual(resultado["valores_faltantes"], 0)
            self.assertEqual(resultado["valores_convertibles"], 2)
            self.assertEqual(resultado["valores_no_convertibles"], 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
