def validar_cantidad_registros(
    datos_archivos,
    datos_consolidados
):
    registros_esperados = sum(
        len(datos)
        for datos in datos_archivos
    )

    registros_obtenidos = len(
        datos_consolidados
    )

    registros_validos = (
        registros_esperados
        == registros_obtenidos
    )

    return {
        "registros_esperados": registros_esperados,
        "registros_obtenidos": registros_obtenidos,
        "valida": registros_validos
    }

def validar_procedencia(
    datos_archivos,
    nombres_archivos,
    datos_consolidados
):
    resultados = {}

    for datos, nombre in zip(
        datos_archivos,
        nombres_archivos
    ):
        registros_esperados = len(datos)

        registros_obtenidos = (
            datos_consolidados["Archivo_Origen"] == nombre
        ).sum()

        registros_validos = (
            registros_esperados == registros_obtenidos
        )

        resultados[nombre] = {
            "registros_esperados": registros_esperados,
            "registros_obtenidos": registros_obtenidos,
            "valida": registros_validos
        }

    return resultados