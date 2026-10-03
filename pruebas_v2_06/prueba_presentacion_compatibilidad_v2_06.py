def mostrar_compatibilidad(clasificaciones_tipos):
    print()
    print("COMPATIBILIDAD")

    if not clasificaciones_tipos:
        print("No se detectaron diferencias de tipos.")
        return

    for columna, clasificaciones in clasificaciones_tipos.items():
        print(f"Columna: {columna}")

        for archivo, clasificacion in clasificaciones.items():
            print(
                f"  {archivo} → {clasificacion}"
            )


clasificaciones_tipos = {
    "Precio": {
        "archivo_X.csv": "COMPATIBLE_POTENCIAL",
        "archivo_S.csv": "SIN_DATOS"
    }
}

mostrar_compatibilidad(clasificaciones_tipos)