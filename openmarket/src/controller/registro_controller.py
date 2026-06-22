from model.usuario_model import agregar_usuario, obtener_usuario_por_correo

def registrar_nuevo_usuario(nombre, correo, contraseña, confirmar_contraseña, telefono):
    
    if not nombre.strip() or not correo.strip() or not contraseña.strip():
        return {"exito": False, "mensaje": "Nombre, Correo y Contraseña son obligatorios."}

    if contraseña != confirmar_contraseña:
        return {"exito": False, "mensaje": "Las contraseñas no coinciden."}

    try:
        existe = obtener_usuario_por_correo(correo.strip())
        if existe:
            return {"exito": False, "mensaje": "Este correo ya está registrado con otra cuenta."}

        agregar_usuario(
            nombre=nombre.strip(),
            correo=correo.strip(),
            contraseña=contraseña, 
            telefono=telefono.strip() if telefono else None
        )
        return {"exito": True, "mensaje": "¡Usuario registrado con éxito!"}

    except Exception as e:
        return {"exito": False, "mensaje": f"Error en la base de datos: {str(e)}"}