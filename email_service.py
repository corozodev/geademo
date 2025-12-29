def generate_email(correo, codigo):
    return f"""
    Para: {correo}
    Asunto: Beneficio especial 🎬

    Hola,

    Tu código de entrada al cine es: {codigo}

    ¡Disfrútalo!
    """
