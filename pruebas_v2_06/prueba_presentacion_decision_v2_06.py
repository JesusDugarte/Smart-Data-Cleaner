from presentacion.consola import mostrar_decision


print("=== PRUEBA 1 ===")

mostrar_decision(
    "LISTO",
    {
        "hay_incompatibilidades": False,
        "hay_conflictos": False,
        "hay_datos_insuficientes": False
    }
)


print()
print("=== PRUEBA 2 ===")

mostrar_decision(
    "REVISAR",
    {
        "hay_incompatibilidades": False,
        "hay_conflictos": True,
        "hay_datos_insuficientes": False
    }
)


print()
print("=== PRUEBA 3 ===")

mostrar_decision(
    "REVISAR",
    {
        "hay_incompatibilidades": False,
        "hay_conflictos": False,
        "hay_datos_insuficientes": True
    }
)


print()
print("=== PRUEBA 4 ===")

mostrar_decision(
    "BLOQUEADO",
    {
        "hay_incompatibilidades": True,
        "hay_conflictos": False,
        "hay_datos_insuficientes": False
    }
)