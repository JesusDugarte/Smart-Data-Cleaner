
import unittest
from pathlib import Path

from proceso_v2_06 import cargar_archivos_csv


class PruebaCargaArchivos(unittest.TestCase):

    def test_carga_dos_archivos_correctamente(self):
        archivos = [
            Path("pruebas_v2_06/archivo_integracion_L.csv"),
            Path("pruebas_v2_06/archivo_integracion_L2.csv")
        ]

        resultado = cargar_archivos_csv(archivos)

        self.assertEqual(
            len(resultado["datos_archivos"]),
            2
        )
        self.assertEqual(
            resultado["nombres_archivos"],
            [
                "archivo_integracion_L.csv",
                "archivo_integracion_L2.csv"
            ]
        )
        self.assertEqual(
            [len(df) for df in resultado["datos_archivos"]],
            [3, 3]
        )
        self.assertEqual(
            resultado["duplicados_por_archivo"],
            {}
        )

    def test_detecta_encabezados_duplicados(self):
        archivos = [
            Path("pruebas_v2_06/prueba_encabezados_duplicados.csv"),
            Path("pruebas_v2_06/archivo_integracion_L.csv")
        ]

        resultado = cargar_archivos_csv(archivos)

        self.assertEqual(
            resultado["duplicados_por_archivo"],
            {
                "prueba_encabezados_duplicados.csv": {
                    "ID": 2
                }
            }
        )

    def test_rechaza_menos_de_dos_archivos(self):
        with self.assertRaises(ValueError):
            cargar_archivos_csv([
                Path("pruebas_v2_06/archivo_integracion_L.csv")
            ])


if __name__ == "__main__":
    unittest.main(verbosity=2)
