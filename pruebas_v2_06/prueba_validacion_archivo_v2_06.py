
import unittest
import tempfile
from pathlib import Path

import pandas as pd

from validacion.archivo import validar_archivo_exportado


class PruebaValidacionArchivo(unittest.TestCase):

    def test_csv_correcto_debe_quedar_validado(self):
        datos_esperados = pd.DataFrame({
            "ID": [1, 2, 3],
            "Nombre": ["Ana", "Luis", "Marta"]
        })

        with tempfile.TemporaryDirectory() as carpeta:
            archivo = Path(carpeta) / "datos_limpios.csv"

            datos_esperados.to_csv(
                archivo,
                index=False
            )

            resultado = validar_archivo_exportado(
                archivo,
                datos_esperados.columns.tolist(),
                len(datos_esperados)
            )

        self.assertEqual(
            resultado["estado"],
            "VALIDADO"
        )

        self.assertEqual(
            resultado["filas"],
            3
        )

        self.assertEqual(
            resultado["columnas"],
            2
        )

        self.assertTrue(
            resultado["filas_correctas"]
        )

        self.assertTrue(
            resultado["columnas_correctas"]
        )

    def test_cantidad_incorrecta_de_filas_debe_revisar(self):
        datos_esperados = pd.DataFrame({
            "ID": [1, 2, 3],
            "Nombre": ["Ana", "Luis", "Marta"]
        })

        datos_exportados = pd.DataFrame({
            "ID": [1, 2],
            "Nombre": ["Ana", "Luis"]
        })

        with tempfile.TemporaryDirectory() as carpeta:
            archivo = Path(carpeta) / "datos_limpios.csv"

            datos_exportados.to_csv(
                archivo,
                index=False
            )

            resultado = validar_archivo_exportado(
                archivo,
                datos_esperados.columns.tolist(),
                len(datos_esperados)
            )

        self.assertEqual(
            resultado["estado"],
            "REVISAR"
        )

        self.assertEqual(
            resultado["filas"],
            2
        )

        self.assertFalse(
            resultado["filas_correctas"]
        )

        self.assertTrue(
            resultado["columnas_correctas"]
        )

    def test_columnas_incorrectas_deben_revisarse(self):
        datos_esperados = pd.DataFrame({
            "ID": [1, 2, 3],
            "Nombre": ["Ana", "Luis", "Marta"]
        })

        datos_exportados = pd.DataFrame({
            "Nombre": ["Ana", "Luis", "Marta"],
            "ID": [1, 2, 3]
        })

        with tempfile.TemporaryDirectory() as carpeta:
            archivo = Path(carpeta) / "datos_limpios.csv"

            datos_exportados.to_csv(
                archivo,
                index=False
            )

            resultado = validar_archivo_exportado(
                archivo,
                datos_esperados.columns.tolist(),
                len(datos_esperados)
            )

        self.assertEqual(
            resultado["estado"],
            "REVISAR"
        )

        self.assertTrue(
            resultado["filas_correctas"]
        )

        self.assertFalse(
            resultado["columnas_correctas"]
        )

    def test_formato_no_soportado_debe_revisarse(self):
        archivo = Path("datos_limpios.txt")

        resultado = validar_archivo_exportado(
            archivo,
            ["ID", "Nombre"],
            3
        )

        self.assertEqual(
            resultado["estado"],
            "REVISAR"
        )

        self.assertEqual(
            resultado["motivo"],
            "Formato de archivo no soportado"
        )

    def test_archivo_inexistente_debe_devolver_error_controlado(self):
        with tempfile.TemporaryDirectory() as carpeta:
            archivo = Path(carpeta) / "inexistente.csv"

            resultado = validar_archivo_exportado(
                archivo,
                ["ID", "Nombre"],
                3
            )

        self.assertEqual(
            resultado["estado"],
            "ERROR"
        )

        self.assertEqual(
            resultado["motivo"],
            "ARCHIVO_NO_ENCONTRADO"
        )

    def test_csv_vacio_debe_devolver_error_controlado(self):
        with tempfile.TemporaryDirectory() as carpeta:
            archivo = Path(carpeta) / "vacio.csv"
            archivo.write_text("", encoding="utf-8")

            resultado = validar_archivo_exportado(
                archivo,
                ["ID", "Nombre"],
                0
            )

        self.assertEqual(
            resultado["estado"],
            "ERROR"
        )

        self.assertEqual(
            resultado["motivo"],
            "ARCHIVO_NO_LEIBLE"
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
