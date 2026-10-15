import unittest
from io import StringIO
from contextlib import redirect_stdout

from presentacion.consola import mostrar_decision


class PruebaPresentacionDecision(unittest.TestCase):

    def obtener_salida(self, estado, motivos):
        salida = StringIO()

        with redirect_stdout(salida):
            mostrar_decision(estado, motivos)

        return salida.getvalue()

    def test_decision_listo_sin_motivo(self):
        salida = self.obtener_salida(
            "LISTO",
            {
                "hay_incompatibilidades": False,
                "hay_conflictos": False,
                "hay_datos_insuficientes": False,
                "hay_encabezados_duplicados": False,
                "hay_diferencias_estructurales": False,
            }
        )

        self.assertIn("Estado de consolidación: LISTO", salida)
        self.assertNotIn("Motivo:", salida)

    def test_revision_por_conflictos_de_tipos(self):
        salida = self.obtener_salida(
            "REVISAR",
            {
                "hay_incompatibilidades": False,
                "hay_conflictos": True,
                "hay_datos_insuficientes": False,
                "hay_encabezados_duplicados": False,
                "hay_diferencias_estructurales": False,
            }
        )

        self.assertIn("Estado de consolidación: REVISAR", salida)
        self.assertIn(
            "diferencias de tipos compatibles",
            salida
        )

    def test_revision_por_datos_insuficientes(self):
        salida = self.obtener_salida(
            "REVISAR",
            {
                "hay_incompatibilidades": False,
                "hay_conflictos": False,
                "hay_datos_insuficientes": True,
                "hay_encabezados_duplicados": False,
                "hay_diferencias_estructurales": False,
            }
        )

        self.assertIn("Estado de consolidación: REVISAR", salida)
        self.assertIn(
            "datos insuficientes",
            salida
        )

    def test_bloqueo_por_incompatibilidad_de_tipos(self):
        salida = self.obtener_salida(
            "BLOQUEADO",
            {
                "hay_incompatibilidades": True,
                "hay_conflictos": False,
                "hay_datos_insuficientes": False,
                "hay_encabezados_duplicados": False,
                "hay_diferencias_estructurales": False,
            }
        )

        self.assertIn("Estado de consolidación: BLOQUEADO", salida)
        self.assertIn(
            "incompatibilidades de tipos",
            salida
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)