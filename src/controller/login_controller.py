from model.usuario_model import obtener_usuario_por_correo
def validar_login(correo, password):

    usuario = obtener_usuario_por_correo(correo)

    if not usuario:
        return False

    if usuario[3] != password:
        return False

    return True