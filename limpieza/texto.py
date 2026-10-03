def limpiar_espacios_externos(datos):
    datos_limpios = datos.copy()

    for columna in datos_limpios.columns:
        if datos_limpios[columna].dtype == "object":
            datos_limpios[columna] = datos_limpios[columna].str.strip()

    return datos_limpios

def limpiar_email(datos):
    datos_limpios = datos.copy()

    datos_limpios["Email"] = datos_limpios["Email"].str.lower()

    return datos_limpios