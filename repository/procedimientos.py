def ejecutar_sp(cursor, nombre, parametros=()):
    marcadores = ", ".join(["%s"] * len(parametros))

    # nombre proviene de constantes del código, nunca de la petición.
    cursor.execute(
        f"CALL {nombre}({marcadores})",
        parametros
    )

    filas = []

    # Consumir todos los resultados antes de reutilizar el cursor.
    while True:
        if cursor.with_rows:
            filas.extend(cursor.fetchall())

        if not cursor.nextset():
            break

    return filas