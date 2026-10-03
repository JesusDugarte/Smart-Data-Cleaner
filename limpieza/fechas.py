from reglas.fechas import convertir_fecha

def limpiar_fechas(datos):
    datos_limpios = datos.copy()

    datos_limpios["Fecha_Registro"] = (
        datos_limpios["Fecha_Registro"].apply(convertir_fecha)
    )

    return datos_limpios