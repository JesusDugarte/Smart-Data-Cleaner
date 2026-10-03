from presentacion.consola import mostrar_compatibilidad_tipos

diagnostico_conflictos_tipos = {
    "Precio": {
        "analisis_por_archivo": {
            "archivo_X.csv": {
                "valores_no_convertibles": 0
            },
            "archivo_S.csv": {
                "valores_no_convertibles": 0
            }
        }
    }
}

clasificaciones_tipos = {
    "Precio": {
        "archivo_X.csv": "COMPATIBLE_POTENCIAL",
        "archivo_S.csv": "SIN_DATOS"
    }
}
mostrar_compatibilidad_tipos(
    diagnostico_conflictos_tipos,
    clasificaciones_tipos
)