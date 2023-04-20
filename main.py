import mysql.connector
from flask import Flask, request, jsonify
from flask import render_template, url_for, redirect

appInventario = Flask(__name__)

config = {
    "host":"localhost",
    "user": "adminVentas",
    "password": "Admin12345.",
    "database": "tiendaDeportiva",
    "raise_on_warnings": True
}

# Ruta index para ver datos de la base de datos (GET)
@appInventario.route('/inventarioproductos', methods=['GET'])
def index():
    if request.method == "GET":
        conexion = mysql.connector.connect(**config)
        miCursor = conexion.cursor()
        query = "SELECT * FROM inventarioProductos"
        miCursor.execute(query)
        response = miCursor.fetchall()
        miCursor.close()
        conexion.close()
    return render_template("index.html", results=response)
    

# Ruta para insertar datos en la base de datos (POST)
@appInventario.route('/inventarioproductos', methods=['POST'])
def insertar_producto():
    if request.method == 'POST':
        codigo = request.form['codigo']
        precio = request.form['precio']
        disponible = 1 if request.form.get('disponible') else 0

        conexion = mysql.connector.connect(**config)
        miCursor = conexion.cursor()
        query ="INSERT INTO inventarioProductos (codigo, precio, disponible) VALUES (%s, %s, %s)"
        val = (codigo, precio, disponible)
        miCursor.execute(query, val)
        conexion.commit()
        miCursor.close()
        conexion.close()
        return redirect('/inventarioproductos')
    return render_template('crear-producto.html')


# Ruta para editar productos (PUT)
@appInventario.route('/inventarioproductos/<string:id>', methods=['POST'])
def editar_producto(id):
    codigo = request.form['codigo']
    precio = request.form['precio']
    disponible = 1 if request.form.get('disponible') else 0
    conexion = mysql.connector.connect(**config)
    miCursor = conexion.cursor()
    query = 'UPDATE inventarioProductos SET codigo = %s, precio = %s, disponible = %s WHERE idProducto = %s'
    val = (codigo, precio, disponible, id)
    miCursor.execute(query, val)
    conexion.commit()
    miCursor.close()
    conexion.close()
    return redirect('/inventarioproductos')


@appInventario.route('/guardar-edicion/<string:id>', methods=['GET'])
def guardar_edicion(id):
    if request.method=="GET":
        conexion = mysql.connector.connect(**config)
        miCursor = conexion.cursor()
        query ="select * from inventarioProductos where idProducto=%s"
        val = (id,)
        miCursor.execute(query, val)
        response = miCursor.fetchone()
        conexion.commit()
        miCursor.close()
        conexion.close()
        return render_template('editar-producto.html', results=response)
    render_template('crear-producto.html')


    

# Ruta para eliminar productos (DELETE)
@appInventario.route('/eliminarproducto/<string:id>', methods=['POST'])
def eliminar_producto(id):
    conexion = mysql.connector.connect(**config)
    miCursor = conexion.cursor()
    query ="delete from inventarioProductos where idProducto=%s"
    val = (id,)
    miCursor.execute(query, val)
    response = miCursor.rowcount
    conexion.commit()
    miCursor.close()
    conexion.close()
    return redirect('/inventarioproductos')

if __name__ == "__main__":
    appInventario.run(debug=True)
