from database.database import db

def obtener_corte():
    query = """
    SELECT 
        v.id_venta,
        SUM(d.cantidad * d.precio_unitario) AS total,
        v.fecha_venta
    FROM ventas v
    INNER JOIN detalle_ventas d ON v.id_venta = d.id_venta
    GROUP BY v.id_venta
    ORDER BY v.fecha_venta DESC
    """
    return db.query(query)


def obtener_corte_hoy():
    query = """
    SELECT 
        v.id_venta,
        SUM(d.cantidad * d.precio_unitario) AS total,
        v.fecha_venta
    FROM ventas v
    INNER JOIN detalle_ventas d ON v.id_venta = d.id_venta
    WHERE DATE(v.fecha_venta) = CURDATE()
    GROUP BY v.id_venta
    ORDER BY v.fecha_venta DESC
    """
    return db.query(query)

def obtener_actividad_reciente():
    query = """
    SELECT
        v.id_venta,
        SUM(d.cantidad * d.precio_unitario) AS total,
        v.fecha_venta
    FROM ventas v
    INNER JOIN detalle_ventas d
        ON v.id_venta = d.id_venta
    WHERE v.fecha_venta >= NOW() - INTERVAL 1 DAY
    GROUP BY v.id_venta
    ORDER BY v.fecha_venta DESC
    """
    return db.query(query)

def total_corte_hoy():
    query = """
    SELECT 
        COALESCE(SUM(d.cantidad * d.precio_unitario), 0) AS total_dia
    FROM ventas v
    INNER JOIN detalle_ventas d ON v.id_venta = d.id_venta
    WHERE DATE(v.fecha_venta) = CURDATE()
    """
    resultado = db.query_one(query)

    return resultado["total_dia"] if resultado else 0 

def obtener_corte_filtrado(tipo_filtro, numero_periodo):
    query = """
    SELECT 
        v.id_venta,
        SUM(d.cantidad * d.precio_unitario) AS total,
        v.fecha_venta
    FROM ventas v
    INNER JOIN detalle_ventas d ON v.id_venta = d.id_venta
    """

    if tipo_filtro == "semana":
        query += " WHERE WEEK(v.fecha_venta, 1) = %s AND YEAR(v.fecha_venta) = YEAR(CURDATE())"
    elif tipo_filtro == "mes":
        query += " WHERE MONTH(v.fecha_venta) = %s AND YEAR(v.fecha_venta) = YEAR(CURDATE())"
        
    query += """
    GROUP BY v.id_venta
    ORDER BY v.fecha_venta DESC
    """
    return db.query(query, (numero_periodo,))