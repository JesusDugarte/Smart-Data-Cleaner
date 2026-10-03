CATALOGO_V1 = [
    {
        "codigo": "V1-01",
        "nombre": "Valores faltantes",
        "severidad": "MEDIA",
        "accion": "REPORTAR"
    },
    {
        "codigo": "V1-02",
        "nombre": "Espacios externos",
        "severidad": "BAJA",
        "accion": "LIMPIAR"
    },
    {
        "codigo": "V1-03",
        "nombre": "Inconsistencia de mayúsculas/minúsculas",
        "severidad": "BAJA",
        "accion": "REVISAR"
    },
        {
        "codigo": "V1-04",
        "nombre": "Inconsistencia de acentos",
        "severidad": "BAJA",
        "accion": "REVISAR"
    },
    {
        "codigo": "V1-05",
        "nombre": "Representaciones equivalentes",
        "severidad": "MEDIA",
        "accion": "REVISAR"
    },
    {
        "codigo": "V1-06",
        "nombre": "Representación dominante",
        "severidad": "BAJA",
        "accion": "PROPONER"
    },
    {
        "codigo": "V1-07",
        "nombre": "Formato de teléfono inconsistente",
        "severidad": "BAJA",
        "accion": "LIMPIAR"
    },
    {
        "codigo": "V1-08",
        "nombre": "Longitud de teléfono incorrecta",
        "severidad": "MEDIA",
        "accion": "REPORTAR"
    },
    {
        "codigo": "V1-09",
        "nombre": "Valor de teléfono repetido",
        "severidad": "MEDIA",
        "accion": "REPORTAR"
    },
    {
        "codigo": "V1-10",
        "nombre": "Registros potencialmente duplicados",
        "severidad": "MEDIA",
        "accion": "REVISAR"
    },
    {
        "codigo": "V1-11",
        "nombre": "Email incompleto",
        "severidad": "MEDIA",
        "accion": "REPORTAR"
    },
    {
        "codigo": "V1-12",
        "nombre": "Múltiples formatos de fecha",
        "severidad": "BAJA",
        "accion": "LIMPIAR"
    },
    {
        "codigo": "V1-13",
        "nombre": "Filas completamente vacías",
        "severidad": "BAJA",
        "accion": "LIMPIAR"
    },
    {
        "codigo": "V1-14",
        "nombre": "IDs duplicados",
        "severidad": "MEDIA",
        "accion": "REPORTAR"
    },
    {
        "codigo": "V1-15",
        "nombre": "Tipos de datos incompatibles",
        "severidad": "MEDIA",
        "accion": "REPORTAR"
    }
]

def obtener_regla(codigo):
    for regla in CATALOGO_V1:
        if regla["codigo"] == codigo:
            return regla

    return None