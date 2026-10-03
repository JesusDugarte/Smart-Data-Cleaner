from detectores.faltantes import (
    detectar_faltantes,
    detectar_filas_vacias
)

from detectores.texto import (
    detectar_espacios_externos,
    detectar_case_inconsistente,
    detectar_acentos_inconsistentes,
    detectar_representaciones_equivalentes,
    detectar_representacion_dominante,
    detectar_email_incompleto
)

from detectores.telefonos import (
    detectar_formato_telefono,
    detectar_longitud_telefono,
    detectar_telefonos_repetidos
)

from detectores.integridad import (
    detectar_registros_duplicados,
    detectar_ids_duplicados,
    detectar_tipos_incompatibles
)

from detectores.fechas import detectar_multiples_formatos_fecha


MAPA_REGLAS = {
    "V1-01": detectar_faltantes,
    "V1-02": detectar_espacios_externos,
    "V1-03": detectar_case_inconsistente,
    "V1-04": detectar_acentos_inconsistentes,
    "V1-05": detectar_representaciones_equivalentes,
    "V1-06": detectar_representacion_dominante,
    "V1-07": detectar_formato_telefono,
    "V1-08": detectar_longitud_telefono,
    "V1-09": detectar_telefonos_repetidos,
    "V1-10": detectar_registros_duplicados,
    "V1-11": detectar_email_incompleto,
    "V1-12": detectar_multiples_formatos_fecha,
    "V1-13": detectar_filas_vacias,
    "V1-14": detectar_ids_duplicados,
    "V1-15": detectar_tipos_incompatibles
}