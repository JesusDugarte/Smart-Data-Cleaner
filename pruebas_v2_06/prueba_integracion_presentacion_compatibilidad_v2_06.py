
import unittest
from io import StringIO
from contextlib import redirect_stdout

import pandas as pd

from detectores.estructura import (
    detectar_tipos_por_columna,
    detectar_diferencias_tipos_varios,
)
from detectores.conflictos_tipos import (
    construir_diagnostico_conflictos_numericos,
)
from reglas.estructura import (
    clasificar_compatibilidad_tipos_varios,
)
from presentacion.consola import (
    mostrar_compatibilidad_tipos,
)


class PruebaIntegracionPresentacionCompatibilidad(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # 1. Cargar los archivos de prueba.
        archivo_X = pd.read_csv(
            "pruebas_v2_06/archivo_X.csv"
        )
        archivo_Z = pd.read_csv(
            "pruebas_v2_06/archivo_Z.csv"
        )

        datos_archivos = [archivo_X, archivo_Z]
        nombres_archivos = [
            "archivo_X.csv",
            "archivo_Z.csv",
        ]

        # 2. Detectar los tipos de datos.
        tipos_por_columna = detectar_tipos_por_columna(
            datos_archivos,
            nombres_archivos,
        )

        # 3. Detectar diferencias entre los tipos.
        diferencias_tipos = detectar_diferencias_tipos_varios(
            tipos_por_columna
        )

        # 4. Analizar los conflictos de tipos.
        cls.diagnostico_conflictos_tipos = (
            construir_diagnostico_conflictos_numericos(
                datos_archivos,
                nombres_archivos,
                diferencias_tipos,
            )
        )

        # 5. Clasificar la compatibilidad.
        cls.clasificaciones_tipos = (
            clasificar_compatibilidad_tipos_varios(
                cls.diagnostico_conflictos_tipos
            )
        )

        # 6. Capturar la presentación en consola.
        salida = StringIO()

        with redirect_stdout(salida):
            mostrar_compatibilidad_tipos(
                cls.diagnostico_conflictos_tipos,
                cls.clasificaciones_tipos,
            )

        cls.salida_consola = salida.getvalue()

    def test_identifica_la_columna_precio(self):
        self.assertIn(
            "Precio",
            self.diagnostico_conflictos_tipos,
        )

    def test_clasifica_correctamente_archivo_X(self):
        self.assertEqual(
            self.clasificaciones_tipos["Precio"]["archivo_X.csv"],
            "COMPATIBLE_POTENCIAL",
        )

    def test_clasifica_correctamente_archivo_Z(self):
        self.assertEqual(
            self.clasificaciones_tipos["Precio"]["archivo_Z.csv"],
            "INCOMPATIBLE",
        )

    def test_detecta_un_valor_no_convertible_en_Z(self):
        resultado = (
            self.diagnostico_conflictos_tipos
            ["Precio"]
            ["analisis_por_archivo"]
            ["archivo_Z.csv"]
        )

        self.assertEqual(
            resultado["valores_no_convertibles"],
            1,
        )

    def test_presenta_las_clasificaciones_y_el_conflicto(self):
        self.assertIn("COMPATIBILIDAD DE TIPOS", self.salida_consola)
        self.assertIn("COMPATIBLE_POTENCIAL", self.salida_consola)
        self.assertIn("INCOMPATIBLE", self.salida_consola)
        self.assertIn(
            "Valores no convertibles: 1",
            self.salida_consola,
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
