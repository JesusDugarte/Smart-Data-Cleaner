from reglas.fechas import detectar_formato_fecha

def detectar_multiples_formatos_fecha(datos):
    resultados = {}

    if "Fecha_Registro" not in datos.columns:
        return resultados

    fechas = datos["Fecha_Registro"].dropna()

    formatos = fechas.apply(detectar_formato_fecha)

    conteo_formatos = formatos.value_counts()

    if len(conteo_formatos) > 1:
        resultados["Fecha_Registro"] = {
            "cantidad_formatos": int(len(conteo_formatos)),
            "formatos": conteo_formatos.to_dict()
        }

    return resultados