import unittest

import pandas as pd

from limpieza.calidad import (
    corregir_espacios,
    corregir_capitalizacion,
)

from analisis.correcciones import ejecutar_correcciones


class PruebaCorreccionesCalidad(unittest.TestCase):

    def test_corrige_espacios_y_registra_cambios(self):
        datos = pd.DataFrame({
            "Nombre": [
                " Ana ",
                "María  José",
                "Luis"
            ]
        })

        resultado = corregir_espacios(datos)

        self.assertEqual(
            resultado["datos"]["Nombre"].tolist(),
            ["Ana", "María José", "Luis"]
        )
        self.assertEqual(
            resultado["correcciones"]["espacios"]["Nombre"][
                "valores_corregidos"
            ],
            2
        )
        self.assertEqual(
            datos["Nombre"].tolist(),
            [" Ana ", "María  José", "Luis"]
        )

    def test_ignora_faltantes_al_corregir_espacios(self):
        datos = pd.DataFrame({
            "Nombre": [" Ana ", None, "   "]
        })

        resultado = corregir_espacios(datos)

        self.assertEqual(
            resultado["datos"]["Nombre"].tolist()[0],
            "Ana"
        )
        self.assertTrue(
            pd.isna(resultado["datos"]["Nombre"].iloc[1])
        )
        self.assertEqual(
            resultado["datos"]["Nombre"].iloc[2],
            ""
        )
        self.assertEqual(
            resultado["correcciones"]["espacios"]["Nombre"][
                "valores_corregidos"
            ],
            2
        )

    def test_corrige_capitalizacion_y_registra_cambios(self):
        datos = pd.DataFrame({
            "Ciudad": ["Bogota", "bogota", "BOGOTA"]
        })

        decisiones = {
            "bogota": {
                "forma_dominante": "Bogota",
                "corregible": True
            }
        }

        resultado = corregir_capitalizacion(
            datos,
            decisiones
        )

        self.assertEqual(
            resultado["datos"]["Ciudad"].tolist(),
            ["Bogota", "Bogota", "Bogota"]
        )
        self.assertEqual(
            resultado["correcciones"]["capitalizacion"]["Ciudad"][
                "valores_corregidos"
            ],
            2
        )
        self.assertEqual(
            datos["Ciudad"].tolist(),
            ["Bogota", "bogota", "BOGOTA"]
        )

    def test_no_corrige_capitalizacion_si_no_es_corregible(self):
        datos = pd.DataFrame({
            "Ciudad": ["Bogota", "bogota"]
        })

        decisiones = {
            "bogota": {
                "forma_dominante": "Bogota",
                "corregible": False
            }
        }

        resultado = corregir_capitalizacion(
            datos,
            decisiones
        )

        self.assertEqual(
            resultado["datos"]["Ciudad"].tolist(),
            ["Bogota", "bogota"]
        )
        self.assertEqual(
            resultado["correcciones"]["capitalizacion"],
            {}
        )

    def test_ejecutar_correcciones_conserva_acciones_pendientes(self):
        datos = pd.DataFrame({
            "Nombre": [" Ana "]
        })

        recomendaciones = [
            {
                "accion": "accion_no_implementada",
                "columna": "Nombre"
            }
        ]

        resultado = ejecutar_correcciones(
            datos,
            recomendaciones
        )

        self.assertEqual(
            resultado["datos"]["Nombre"].tolist(),
            [" Ana "]
        )
        self.assertEqual(
            resultado["correcciones"],
            {}
        )
        self.assertEqual(
            resultado["pendientes"],
            recomendaciones
        )


    def test_ejecutar_correcciones_sin_recomendaciones(self):
        datos = pd.DataFrame({
            "Nombre": [" Ana ", "Luis"]
        })

        datos_originales = datos.copy(deep=True)

        resultado = ejecutar_correcciones(datos, [])

        self.assertEqual(
            resultado["datos"]["Nombre"].tolist(),
            [" Ana ", "Luis"]
        )
        self.assertEqual(resultado["correcciones"], {})
        self.assertEqual(resultado["pendientes"], [])

        pd.testing.assert_frame_equal(
            datos,
            datos_originales
        )


    def test_acumula_varias_recomendaciones_capitalizacion(self):
        datos = pd.DataFrame({
            "Ciudad": [
                "Bogota", "bogota", "BOGOTA",
                "Medellin", "medellin", "MEDELLIN"
            ]
        })

        datos_originales = datos.copy(deep=True)

        recomendaciones = [
            {
                "accion": "normalizar_capitalizacion",
                "columna": "Ciudad",
                "grupo": "bogota",
                "forma_dominante": "Bogota"
            },
            {
                "accion": "normalizar_capitalizacion",
                "columna": "Ciudad",
                "grupo": "medellin",
                "forma_dominante": "Medellin"
            }        ]

        resultado = ejecutar_correcciones(
            datos,
            recomendaciones
        )

        self.assertEqual(
            resultado["datos"]["Ciudad"].tolist(),
            [
                "Bogota", "Bogota", "Bogota",
                "Medellin", "Medellin", "Medellin"
            ]
        )

        self.assertEqual(
            resultado["correcciones"]["capitalizacion"]["Ciudad"][
                "valores_corregidos"
            ],
            4
        )

        self.assertEqual(resultado["pendientes"], [])

        pd.testing.assert_frame_equal(
            datos,
            datos_originales
        )

    def test_combina_espacios_y_capitalizacion(self):
        datos = pd.DataFrame({
            "Ciudad": [
                " Bogota ", "bogota", "BOGOTA",
                " Medellin ", "medellin", "MEDELLIN"
            ]
        })

        datos_originales = datos.copy(deep=True)

        recomendaciones = [
            {
                "accion": "normalizar_espacios"
            },
            {
                "accion": "normalizar_capitalizacion",
                "columna": "Ciudad",
                "grupo": "bogota",
                "forma_dominante": "Bogota"
            },
            {
                "accion": "normalizar_capitalizacion",
                "columna": "Ciudad",
                "grupo": "medellin",
                "forma_dominante": "Medellin"
            }        ]

        resultado = ejecutar_correcciones(
            datos,
            recomendaciones
        )

        self.assertEqual(
            resultado["datos"]["Ciudad"].tolist(),
            [
                "Bogota", "Bogota", "Bogota",
                "Medellin", "Medellin", "Medellin"
            ]
        )

        self.assertEqual(
            resultado["correcciones"]["espacios"]["Ciudad"][
                "valores_corregidos"
            ],
            2
        )

        self.assertEqual(
            resultado["correcciones"]["capitalizacion"]["Ciudad"][
                "valores_corregidos"
            ],
            4
        )

        self.assertEqual(resultado["pendientes"], [])

        pd.testing.assert_frame_equal(
            datos,
            datos_originales
        )

    def test_capitalizacion_respeta_columna_recomendada(self):
        datos = pd.DataFrame({
            "Ciudad": ["Bogota", "bogota"],
            "Observacion": ["bogota", "BOGOTA"]
        })

        recomendaciones = [
            {
                "accion": "normalizar_capitalizacion",
                "columna": "Ciudad",
                "grupo": "bogota",
                "forma_dominante": "Bogota"
            }
        ]

        resultado = ejecutar_correcciones(
            datos,
            recomendaciones
        )

        self.assertEqual(
            resultado["datos"]["Ciudad"].tolist(),
            ["Bogota", "Bogota"]
        )

        self.assertEqual(
            resultado["datos"]["Observacion"].tolist(),
            ["bogota", "BOGOTA"]
        )

        self.assertEqual(
            resultado["correcciones"]["capitalizacion"]["Ciudad"][
                "valores_corregidos"
            ],
            1
        )

if __name__ == "__main__":
    unittest.main(verbosity=2)
