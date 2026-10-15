
import unittest

import pandas as pd
from openpyxl import Workbook

from exportacion.excel import construir_datos_limpios


class PruebaDatosLimpiosExcel(unittest.TestCase):

    def test_construye_hoja_con_valores_normales_y_ausentes(self):
        datos = pd.DataFrame({
            "ID": [101],
            "Nombre": ["Ana Rodríguez"],
            "Precio": [float("nan")]
        })

        resultado_proceso = {
            "resultado": {
                "datos": datos
            }
        }

        libro = Workbook()
        hoja = libro.active

        construir_datos_limpios(
            hoja,
            resultado_proceso
        )

        self.assertEqual(hoja["A1"].value, "DATOS LIMPIOS")

        self.assertEqual(hoja["A3"].value, "ID")
        self.assertEqual(hoja["B3"].value, "Nombre")
        self.assertEqual(hoja["C3"].value, "Precio")

        self.assertEqual(hoja["A4"].value, 101)
        self.assertEqual(hoja["B4"].value, "Ana Rodríguez")
        self.assertIsNone(hoja["C4"].value)

        libro.close()


if __name__ == "__main__":
    unittest.main(verbosity=2)
