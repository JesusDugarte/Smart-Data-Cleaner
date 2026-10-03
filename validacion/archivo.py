import pandas as pd

def validar_archivo_exportado(
    archivo,
    columnas_esperadas,
    filas_esperadas
):
    if archivo.suffix.lower() == ".csv":
        datos_exportados = pd.read_csv(
            archivo,
            dtype={"Telefono": "string"}
        )
    elif archivo.suffix.lower() == ".xlsx":
        datos_exportados = pd.read_excel(
            archivo,
            dtype={"Telefono": "string"}
        )

    resultado = {
        "archivo": archivo.name,
        "filas": len(datos_exportados),
        "columnas": len(datos_exportados.columns),
        "columnas_correctas": (
            datos_exportados.columns.tolist()
            == columnas_esperadas
        ),
        "telefono_valido": False,
        "fechas_validas": False,
        "estado": "REVISAR"
    }

    # Validar teléfono
    if "Telefono" in datos_exportados.columns:
        telefonos = datos_exportados["Telefono"].dropna()

        telefonos_validos = (
            telefonos.str.len().eq(10)
            & telefonos.str.isdigit()
        )

        resultado["telefono_valido"] = telefonos_validos.all()

    # Validar fechas
    if "Fecha_Registro" in datos_exportados.columns:
        fechas = datos_exportados["Fecha_Registro"]

        fechas_convertidas = pd.to_datetime(
            fechas,
            errors="coerce"
        )

        fechas_validas = (
            fechas.isna()
            | fechas_convertidas.notna()
        )

        resultado["fechas_validas"] = fechas_validas.all()

    # Validación general
    if (
        resultado["filas"] == filas_esperadas
        and resultado["columnas"] == len(columnas_esperadas)
        and resultado["columnas_correctas"]
        and resultado["telefono_valido"]
        and resultado["fechas_validas"]
    ):
        resultado["estado"] = "VALIDADO"

    return resultado
