import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

from dotenv import load_dotenv 

#Cargar las variables de entorno
load_dotenv()

#crear instancia
app =  Flask(__name__)

# Configuración de la base de datos PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
#app.config['SQLALCHEMY_DATABASE_URI'] = "URL EXTERNA RENDER"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ============================
# MODELO PRODUCTOS
# ============================

class Producto(db.Model):
    __tablename__ = 'productos'
    
    codigo_barras = db.Column(db.String, primary_key=True)
    nombre = db.Column(db.String)
    precio_c = db.Column(db.Numeric(10,2))
    precio_v = db.Column(db.Numeric(10,2))
    descripcion = db.Column(db.String)

# ============================
# GET TODOS LOS PRODUCTOS
# ============================

@app.route('/productos', methods=['GET'])
def get_productos():
    productos = Producto.query.all()
    
    lista_productos = []
    
    for producto in productos:
        lista_productos.append({
            'codigo_barras': producto.codigo_barras,
            'nombre': producto.nombre,
            'precio_c': float(producto.precio_c) if producto.precio_c else 0,
            'precio_v': float(producto.precio_v) if producto.precio_v else 0,
            'descripcion': producto.descripcion
        })
        
    return jsonify(lista_productos)

# ============================
# GET PRODUCTO POR CODIGO
# ============================

@app.route('/productos/<codigo_barras>', methods=['GET'])
def get_producto(codigo_barras):
    producto = Producto.query.get(codigo_barras)
    
    if producto is None:
        return jsonify({'msg': 'Producto no encontrado'})
    
    return jsonify({
        'codigo_barras': producto.codigo_barras,
        'nombre': producto.nombre,
        'precio_c': float(producto.precio_c),
        'precio_v': float(producto.precio_v),
        'descripcion': producto.descripcion
    })

# ============================
# INSERTAR PRODUCTO
# ============================

@app.route('/productos', methods=['POST'])
def insert_producto():
    data = request.get_json()
    
    nuevo_producto = Producto(
        codigo_barras = data['codigo_barras'],
        nombre = data['nombre'],
        precio_c = data['precio_c'],
        precio_v = data['precio_v'],
        descripcion = data['descripcion']
    )
    
    db.session.add(nuevo_producto)
    db.session.commit()
    
    return jsonify({'msg': 'Producto agregado correctamente'})


# ============================
# ACTUALIZAR PRODUCTO
# ============================

@app.route('/productos/<codigo_barras>', methods=['PUT'])
def update_producto(codigo_barras):
    producto = Producto.query.get(codigo_barras)
    
    if producto is None:
        return jsonify({'msg': 'Producto no encontrado'})
    
    data = request.get_json()
    
    if "nombre" in data:
        producto.nombre = data['nombre']
        
    if "precio_c" in data:
        producto.precio_c = data['precio_c']
        
    if "precio_v" in data:
        producto.precio_v = data['precio_v']
        
    if "descripcion" in data:
        producto.descripcion = data['descripcion']
        
    db.session.commit()
    
    return jsonify({'msg': 'Producto actualizado correctamente'})




if __name__ == '__main__':
    app.run(debug=True) 