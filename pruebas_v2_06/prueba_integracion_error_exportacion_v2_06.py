import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


RAIZ_PROYECTO = Path(__file__).resolve().parent.parent


class PruebaIntegracionErrorExportacion(unittest.TestCase):

    def test_error_en_validacion_exportada_cambia_estado_final(self):
        archivo_principal = RAIZ_PROYECTO / "inicio_v2_06.py"

        self.assertTrue(
            archivo_principal.is_file(),
            f"No existe el archivo requerido: {archivo_principal}"
        )

        with tempfile.TemporaryDirectory(
            prefix="prueba_error_exportacion_"
        ) as carpeta_temporal:

            carpeta = Path(carpeta_temporal)
            ruta_salida = carpeta.as_posix()

            contenido = archivo_principal.read_text(
                encoding="utf-8-sig"
            )

            # Redirigir todos los archivos generados a la carpeta temporal.
            contenido = contenido.replace(
                '"salida/datos_limpios.csv"',
                f'"{ruta_salida}/datos_limpios.csv"'
            )
            contenido = contenido.replace(
                'Path("salida/datos_limpios.csv")',
                f'Path("{ruta_salida}/datos_limpios.csv")'
            )
            contenido = contenido.replace(
                '"salida/informe_proceso.txt"',
                f'"{ruta_salida}/informe_proceso.txt"'
            )
            contenido = contenido.replace(
                '"salida/informe_proceso.xlsx"',
                f'"{ruta_salida}/informe_proceso.xlsx"'
            )

            # Sustituir la función importada por una función simulada.
            importacion_original = (
                "from validacion.archivo import (\n"
                "    validar_archivo_exportado\n"
                ")"
            )

            importacion_simulada = (
                "def validar_archivo_exportado("
                "archivo, columnas_esperadas, filas_esperadas):\n"
                "    return {\n"
                "        'archivo': archivo.name,\n"
                "        'filas': None,\n"
                "        'columnas': None,\n"
                "        'filas_correctas': False,\n"
                "        'columnas_correctas': False,\n"
                "        'estado': 'ERROR',\n"
                "        'motivo': 'ARCHIVO_NO_LEIBLE'\n"
                "    }"
            )

            self.assertIn(
                importacion_original,
                contenido,
                "No se encontró la importación esperada del validador."
            )

            contenido = contenido.replace(
                importacion_original,
                importacion_simulada,
                1
            )
            marcador_resultado = "libro = crear_libro_informe()"

            self.assertIn(
                marcador_resultado,
                contenido,
                "No se encontró el punto esperado para comprobar el resultado."
            )

            contenido = contenido.replace(
                marcador_resultado,
                'print("PRUEBA_ESTADO_INTERNO:", '
                'resultado_proceso["resultado"]["estado_final"])\n'
                'print("PRUEBA_MOTIVO_ERROR:", '
                'resultado_proceso["validacion"]["archivo_exportado"]["motivo"])\n'
                + marcador_resultado,
                1
            )

            script_temporal = carpeta / "inicio_prueba.py"
            script_temporal.write_text(
                contenido,
                encoding="utf-8"
            )

            ejecucion = subprocess.run(
                [sys.executable, str(script_temporal)],
                cwd=RAIZ_PROYECTO,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                env={
                    **os.environ,
                    "PYTHONPATH": (
                        str(RAIZ_PROYECTO)
                        + os.pathsep
                        + os.environ.get("PYTHONPATH", "")
                    ),
                    "PYTHONIOENCODING": "utf-8",
                },
            )

            salida_consola = (
                ejecucion.stdout + ejecucion.stderr
            )

            self.assertEqual(
                ejecucion.returncode,
                0,
                f"El programa terminó con error:\n{salida_consola}"
            )
            self.assertIn(
                "PRUEBA_ESTADO_INTERNO: REVISAR",
                salida_consola
            )
            self.assertIn(
                "PRUEBA_MOTIVO_ERROR: ARCHIVO_NO_LEIBLE",
                salida_consola
            )
            self.assertIn(
                "Estado final: REVISAR",
                salida_consola
            )

            archivo_csv = carpeta / "datos_limpios.csv"
            archivo_txt = carpeta / "informe_proceso.txt"
            archivo_excel = carpeta / "informe_proceso.xlsx"

            self.assertTrue(archivo_csv.is_file())
            self.assertTrue(archivo_txt.is_file())
            self.assertTrue(archivo_excel.is_file())
    def test_error_al_guardar_excel_no_impide_mostrar_resumen(self):
        archivo_principal = RAIZ_PROYECTO / "inicio_v2_06.py"

        with tempfile.TemporaryDirectory(
            prefix="prueba_error_excel_"
        ) as carpeta_temporal:

            carpeta = Path(carpeta_temporal)
            ruta_salida = carpeta.as_posix()

            contenido = archivo_principal.read_text(
                encoding="utf-8-sig"
            )

            contenido = contenido.replace(
                '"salida/datos_limpios.csv"',
                f'"{ruta_salida}/datos_limpios.csv"'
            )
            contenido = contenido.replace(
                'Path("salida/datos_limpios.csv")',
                f'Path("{ruta_salida}/datos_limpios.csv")'
            )
            contenido = contenido.replace(
                '"salida/informe_proceso.txt"',
                f'"{ruta_salida}/informe_proceso.txt"'
            )
            contenido = contenido.replace(
                '"salida/informe_proceso.xlsx"',
                f'"{ruta_salida}/informe_proceso.xlsx"'
            )

            marcador = "libro = crear_libro_informe()"

            self.assertIn(marcador, contenido)

            contenido = contenido.replace(
                marcador,
                'def guardar_libro_informe(libro, ruta_salida):\n'
                '    raise PermissionError("Acceso denegado de prueba")\n\n'
                + marcador,
                1
            )

            script_temporal = carpeta / "inicio_prueba.py"
            script_temporal.write_text(
                contenido,
                encoding="utf-8"
            )

            ejecucion = subprocess.run(
                [sys.executable, str(script_temporal)],
                cwd=RAIZ_PROYECTO,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                env={
                    **os.environ,
                    "PYTHONPATH": (
                        str(RAIZ_PROYECTO)
                        + os.pathsep
                        + os.environ.get("PYTHONPATH", "")
                    ),
                    "PYTHONIOENCODING": "utf-8",
                },
            )

            salida_consola = (
                ejecucion.stdout + ejecucion.stderr
            )

            self.assertEqual(
                ejecucion.returncode,
                0,
                f"El programa terminó con error:\n{salida_consola}"
            )
            self.assertIn(
                "ERROR: No se pudo guardar el informe Excel.",
                salida_consola
            )
            self.assertIn(
                "Detalle: Acceso denegado de prueba",
                salida_consola
            )
            self.assertIn(
                "RESUMEN",
                salida_consola
            )
            self.assertIn(
                "Estado final: LISTO",
                salida_consola
            )

if __name__ == "__main__":
    unittest.main()