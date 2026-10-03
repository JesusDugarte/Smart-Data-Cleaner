import pandas as pd


def corregir_espacios(datos):
    datos_corregidos = datos.copy()

    correcciones_espacios = {}

    for columna in datos_corregidos.columns:

        if datos_corregidos[columna].dtype != "object":
            continue

        for indice, valor in datos_corregidos[columna].items():

            if pd.isna(valor):
                continue

            if not isinstance(valor, str):
                continue

            valor_corregido = valor.strip()

            valor_corregido = " ".join(
                valor_corregido.split()
            )

            if valor_corregido != valor:

                datos_corregidos.at[
                    indice,
                    columna
                ] = valor_corregido

                if columna not in correcciones_espacios:
                    correcciones_espacios[columna] = {
                        "valores_corregidos": 0
                    }

                correcciones_espacios[columna][
                    "valores_corregidos"
                ] += 1

    return {
    "datos": datos_corregidos,
    "correcciones": {
        "espacios": correcciones_espacios
    }
}

def corregir_capitalizacion(
    datos,
    decisiones_capitalizacion
):
    datos_corregidos = datos.copy()

    correcciones_capitalizacion = {}

    for columna in datos_corregidos.columns:

        if datos_corregidos[columna].dtype != "object":
            continue

        for clave, decision in decisiones_capitalizacion.items():

            if not decision["corregible"]:
                continue

            forma_dominante = decision[
                "forma_dominante"
            ]

            valores_corregidos = 0

            for indice, valor in datos_corregidos[
                columna
            ].items():

                if pd.isna(valor):
                    continue

                if not isinstance(valor, str):
                    continue

                if valor.lower() != clave:
                    continue

                if valor == forma_dominante:
                    continue

                datos_corregidos.at[
                    indice,
                    columna
                ] = forma_dominante

                valores_corregidos += 1

            if valores_corregidos > 0:

                if columna not in correcciones_capitalizacion:
                    correcciones_capitalizacion[columna] = {
                        "valores_corregidos": 0
                    }

                correcciones_capitalizacion[
                    columna
                ]["valores_corregidos"] += valores_corregidos

    return {
        "datos": datos_corregidos,
        "correcciones": {
            "capitalizacion":
                correcciones_capitalizacion
        }
    }