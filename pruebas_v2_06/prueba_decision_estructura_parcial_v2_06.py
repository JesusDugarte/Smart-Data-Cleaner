import unittest

from reglas.estructura import determinar_estado_consolidacion


class PruebaDecisionEstructuraParcial(unittest.TestCase):

    def test_estructura_equivalente_debe_quedar_lista(self):
        estado = determinar_estado_consolidacion(
            compatibilidad_estructural="ESTRUCTURA_EQUIVALENTE",
            hay_conflictos=False,
            hay_incompatibilidades=False,
            hay_datos_insuficientes=False
        )

        self.assertEqual(estado, "LISTO")

    def test_estructura_parcial_debe_requerir_revision(self):
        estado = determinar_estado_consolidacion(
            compatibilidad_estructural="ESTRUCTURA_PARCIAL",
            hay_conflictos=False,
            hay_incompatibilidades=False,
            hay_datos_insuficientes=False
        )

        self.assertEqual(estado, "REVISAR")

    def test_incompatibilidad_de_tipos_debe_bloquear(self):
        estado = determinar_estado_consolidacion(
            compatibilidad_estructural=(
                "ESTRUCTURA_COMUN_TIPOS_DIFERENTES"
            ),
            hay_conflictos=False,
            hay_incompatibilidades=True,
            hay_datos_insuficientes=False
        )

        self.assertEqual(estado, "BLOQUEADO")

    def test_sin_base_comun_debe_bloquear(self):
        estado = determinar_estado_consolidacion(
            compatibilidad_estructural="SIN_BASE_COMUN",
            hay_conflictos=False,
            hay_incompatibilidades=False,
            hay_datos_insuficientes=False
        )

        self.assertEqual(estado, "BLOQUEADO")

    def test_conflictos_de_tipos_deben_requerir_revision(self):
        estado = determinar_estado_consolidacion(
            compatibilidad_estructural="ESTRUCTURA_EQUIVALENTE",
            hay_conflictos=True,
            hay_incompatibilidades=False,
            hay_datos_insuficientes=False
        )

        self.assertEqual(estado, "REVISAR")

    def test_datos_insuficientes_deben_requerir_revision(self):
        estado = determinar_estado_consolidacion(
            compatibilidad_estructural="ESTRUCTURA_EQUIVALENTE",
            hay_conflictos=False,
            hay_incompatibilidades=False,
            hay_datos_insuficientes=True
        )

        self.assertEqual(estado, "REVISAR")

    def test_incompatibilidad_prevalece_sobre_estructura_parcial(self):
        estado = determinar_estado_consolidacion(
            compatibilidad_estructural="ESTRUCTURA_PARCIAL",
            hay_conflictos=False,
            hay_incompatibilidades=True,
            hay_datos_insuficientes=False
        )

        self.assertEqual(estado, "BLOQUEADO")

if __name__ == "__main__":
    unittest.main(verbosity=2)
