
import unittest
from pathlib import Path


DIRECTORIO_PRUEBAS = Path(__file__).parent / "pruebas_v2_06"



def construir_suite_pruebas():
    """Descubre automáticamente los módulos de prueba."""

    cargador = unittest.TestLoader()

    suite = unittest.TestSuite()

    for archivo in sorted(DIRECTORIO_PRUEBAS.glob("prueba_*.py")):
        nombre_modulo = archivo.stem

        especificacion = __import__(
            "importlib.util",
            fromlist=["spec_from_file_location"]
        )

        spec = especificacion.spec_from_file_location(
            nombre_modulo,
            archivo
        )

        modulo = especificacion.module_from_spec(spec)
        spec.loader.exec_module(modulo)

        suite.addTests(cargador.loadTestsFromModule(modulo))

    return suite



def ejecutar_pruebas():
    """Ejecuta la suite y comunica si hubo fallos."""

    suite = construir_suite_pruebas()

    ejecutor = unittest.TextTestRunner(
        verbosity=2
    )

    resultado = ejecutor.run(suite)

    return resultado.wasSuccessful()


if __name__ == "__main__":
    pruebas_correctas = ejecutar_pruebas()

    if not pruebas_correctas:
        raise SystemExit(1)
