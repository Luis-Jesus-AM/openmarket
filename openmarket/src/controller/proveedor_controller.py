# Importamos las funciones del modelo (asumiendo que tu archivo de modelo se llama proveedor_model)
from model.proveedor_model import obtener_proveedores, agregar_proveedor

def listar_proveedores():
    """
    Intermedia entre la vista y el modelo para obtener la lista de proveedores.
    """
    # Llama al método del modelo y le regresa los datos limpios a la vista de Flet
    return obtener_proveedores()


def registrar_proveedor(nombre, correo, telefono, producto_que_vende, direccion):
    """
    Intermedia entre la vista y el modelo para registrar un nuevo proveedor.
    Valida campos obligatorios antes de golpear la base de datos.
    """
    # Validación previa en el controlador por seguridad (por ejemplo, el nombre es obligatorio)
    if not nombre or not nombre.strip():
        return False
        
    # Pasa exactamente los 5 parámetros recolectados de la View hacia el Model
    resultado = agregar_proveedor(
        nombre=nombre,
        correo=correo,
        telefono=telefono,
        producto_que_vende=producto_que_vende,
        direccion=direccion
    )
    
    return resultado