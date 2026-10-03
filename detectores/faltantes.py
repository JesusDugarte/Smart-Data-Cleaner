def detectar_faltantes(datos):
    faltantes = datos.isna().sum()
    faltantes = faltantes[faltantes > 0]
    detalle = {}
    for columna, cantidad in faltantes.items():
        detalle[columna] = {"cantidad": int(cantidad)}
    total_faltantes = int(faltantes.sum())
    return detalle, total_faltantes

def detectar_filas_vacias(datos):
    filas_vacias = datos.isna().all(axis=1)

    filas_afectadas = datos.index[filas_vacias].tolist()

    if filas_afectadas:
        return {
            "filas": {
                "cantidad": len(filas_afectadas),
                "filas": filas_afectadas
            }
        }

    return {}
