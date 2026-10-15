import unittest
import pandas as pd

from reglas.calidad import determinar_estado_calidad
from validacion.calidad import validar_espacios, validar_capitalizacion

class PruebaEstadoCalidad(unittest.TestCase):

    def test_sin_pendientes_y_validaciones_satisfactorias(self):
        resultados = [
            {"estado": "CORREGIDO"},
            {"estado": "SIN_ACCION"},
        ]

        estado = determinar_estado_calidad([], resultados)

        self.assertEqual(estado, "LISTO")

    def test_con_pendientes_debe_revisar(self):
        pendientes = [
            {"accion": "revisar_faltantes"}
        ]

        estado = determinar_estado_calidad(pendientes, [])

        self.assertEqual(estado, "REVISAR")

    def test_correccion_incompleta_debe_revisar(self):
        resultados = [
            {"estado": "CORREGIDO_CON_PENDIENTES"}
        ]

        estado = determinar_estado_calidad([], resultados)

        self.assertEqual(estado, "REVISAR")

    def test_error_de_validacion_debe_bloquear(self):
        resultados = [
            {"estado": "ERROR"}
        ]

        estado = determinar_estado_calidad([], resultados)

        self.assertEqual(estado, "BLOQUEADO")

    def test_estado_desconocido_debe_bloquear(self):
        resultados = [
            {"estado": "ESTADO_DESCONOCIDO"}
        ]

        estado = determinar_estado_calidad([], resultados)

        self.assertEqual(estado, "BLOQUEADO")


    def test_espacios_corregidos_completamente(self):
        antes = pd.DataFrame({
            "Ciudad": [" Bogotá ", "Medellín  ", "Cali  Norte"]
        })
        despues = pd.DataFrame({
            "Ciudad": ["Bogotá", "Medellín", "Cali Norte"]
        })

        resultado = validar_espacios(antes, despues, "Ciudad")

        self.assertEqual(resultado["antes"], 3)
        self.assertEqual(resultado["despues"], 0)
        self.assertEqual(resultado["corregidos"], 3)
        self.assertEqual(resultado["pendientes"], 0)
        self.assertEqual(resultado["estado"], "CORREGIDO")

    def test_espacios_corregidos_parcialmente(self):
        antes = pd.DataFrame({
            "Ciudad": [" Bogotá ", "Medellín  ", "Cali  Norte"]
        })
        despues = pd.DataFrame({
            "Ciudad": ["Bogotá", "Medellín  ", "Cali Norte"]
        })

        resultado = validar_espacios(antes, despues, "Ciudad")

        self.assertEqual(resultado["antes"], 3)
        self.assertEqual(resultado["despues"], 1)
        self.assertEqual(resultado["corregidos"], 2)
        self.assertEqual(resultado["pendientes"], 1)
        self.assertEqual(
            resultado["estado"],
            "CORREGIDO_CON_PENDIENTES"
        )

    def test_espacios_sin_correccion(self):
        antes = pd.DataFrame({
            "Ciudad": [" Bogotá ", "Medellín  "]
        })
        despues = pd.DataFrame({
            "Ciudad": [" Bogotá ", "Medellín  "]
        })

        resultado = validar_espacios(antes, despues, "Ciudad")

        self.assertEqual(resultado["antes"], 2)
        self.assertEqual(resultado["despues"], 2)
        self.assertEqual(resultado["corregidos"], 0)
        self.assertEqual(resultado["pendientes"], 2)
        self.assertEqual(resultado["estado"], "NO_CORREGIDO")

    def test_espacios_sin_accion_necesaria(self):
        datos = pd.DataFrame({
            "Ciudad": ["Bogotá", "Medellín", "Cali"]
        })

        resultado = validar_espacios(datos, datos.copy(), "Ciudad")

        self.assertEqual(resultado["antes"], 0)
        self.assertEqual(resultado["despues"], 0)
        self.assertEqual(resultado["corregidos"], 0)
        self.assertEqual(resultado["pendientes"], 0)
        self.assertEqual(resultado["estado"], "SIN_ACCION")

    def test_capitalizacion_corregida_completamente(self):
        antes = pd.DataFrame({
            "Ciudad": [
                "Bogota",
                "Bogota",
                "Bogota",
                "bogota",
                "BOGOTA"
            ]
        })

        despues = pd.DataFrame({
            "Ciudad": [
                "Bogota",
                "Bogota",
                "Bogota",
                "Bogota",
                "Bogota"
            ]
        })

        resultado = validar_capitalizacion(
            antes,
            despues,
            "Ciudad",
            "bogota",
            "Bogota"
        )

        self.assertEqual(resultado["antes"], 2)
        self.assertEqual(resultado["despues"], 0)
        self.assertEqual(resultado["corregidos"], 2)
        self.assertEqual(resultado["pendientes"], 0)
        self.assertEqual(resultado["estado"], "CORREGIDO")

    def test_capitalizacion_corregida_parcialmente(self):
        antes = pd.DataFrame({
            "Ciudad": [
                "Bogota",
                "Bogota",
                "Bogota",
                "bogota",
                "BOGOTA"
            ]
        })

        despues = pd.DataFrame({
            "Ciudad": [
                "Bogota",
                "Bogota",
                "Bogota",
                "Bogota",
                "BOGOTA"
            ]
        })

        resultado = validar_capitalizacion(
            antes,
            despues,
            "Ciudad",
            "bogota",
            "Bogota"
        )

        self.assertEqual(resultado["antes"], 2)
        self.assertEqual(resultado["despues"], 1)
        self.assertEqual(resultado["corregidos"], 1)
        self.assertEqual(resultado["pendientes"], 1)
        self.assertEqual(
            resultado["estado"],
            "CORREGIDO_CON_PENDIENTES"
        )

    def test_capitalizacion_sin_correccion(self):
        antes = pd.DataFrame({
            "Ciudad": [
                "Bogota",
                "Bogota",
                "Bogota",
                "bogota",
                "BOGOTA"
            ]
        })

        despues = antes.copy()

        resultado = validar_capitalizacion(
            antes,
            despues,
            "Ciudad",
            "bogota",
            "Bogota"
        )

        self.assertEqual(resultado["antes"], 2)
        self.assertEqual(resultado["despues"], 2)
        self.assertEqual(resultado["corregidos"], 0)
        self.assertEqual(resultado["pendientes"], 2)
        self.assertEqual(resultado["estado"], "NO_CORREGIDO")

    def test_capitalizacion_sin_accion_necesaria(self):
        datos = pd.DataFrame({
            "Ciudad": [
                "Bogota",
                "Bogota",
                "Bogota"
            ]
        })

        resultado = validar_capitalizacion(
            datos,
            datos.copy(),
            "Ciudad",
            "bogota",
            "Bogota"
        )

        self.assertEqual(resultado["antes"], 0)
        self.assertEqual(resultado["despues"], 0)
        self.assertEqual(resultado["corregidos"], 0)
        self.assertEqual(resultado["pendientes"], 0)
        self.assertEqual(resultado["estado"], "SIN_ACCION")

    def test_capitalizacion_indices_incompatibles_debe_devolver_error(self):
        antes = pd.DataFrame({
            "Ciudad": ["BOGOTA", "bogota"]
        })

        despues = pd.DataFrame(
            {
                "Ciudad": ["Bogota", "Bogota"]
            },
            index=[10, 11]
        )

        resultado = validar_capitalizacion(
            antes,
            despues,
            "Ciudad",
            "bogota",
            "Bogota"
        )

        self.assertEqual(resultado["estado"], "ERROR")
        self.assertEqual(
            resultado["motivo"],
            "INDICES_INCOMPATIBLES"
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
