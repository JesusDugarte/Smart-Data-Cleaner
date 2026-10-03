from reglas.telefonos import normalizar_telefono

def limpiar_telefonos(datos):
    datos_limpios = datos.copy()

    datos_limpios["Telefono"] = datos_limpios["Telefono"].apply(
        normalizar_telefono
    )

    return datos_limpios