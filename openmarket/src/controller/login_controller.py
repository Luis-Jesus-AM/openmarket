from model.usuario_model import obtener_usuario_por_correo

def validar_login(correo, password):
    if correo == "" or password == "":
        return "campos_vacios"

    usuario = obtener_usuario_por_correo(correo)

    if not usuario:
        return "no_existe"

    if usuario["contraseña"] != password:
        return "password_incorrecto"


    return {
        "id": usuario["id_usuario"],
        "nombre": usuario["nombre"], 
        "correo": usuario["correo"]
    }