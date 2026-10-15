
import unittest
from unittest.mock import Mock, patch

from exportacion.excel import guardar_libro_informe


class PruebaExportacionExcel(unittest.TestCase):

    def test_error_de_permisos_se_propaga(self):
        libro = Mock()

        with patch.object(
            libro,
            "save",
            side_effect=PermissionError("Acceso denegado")
        ):
            with self.assertRaisesRegex(
                PermissionError,
                "Acceso denegado"
            ):
                guardar_libro_informe(
                    libro,
                    "informe_prueba.xlsx"
                )

            libro.save.assert_called_once_with(
                "informe_prueba.xlsx"
            )

if __name__ == "__main__":
    unittest.main(verbosity=2)
