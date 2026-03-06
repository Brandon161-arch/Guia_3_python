import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)


productos = []


class Producto:

    def __init__(self, id: int, nombre: str, precio: float):
        self.id = id
        self.nombre = nombre
        self.precio = precio

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "precio": self.precio
        }



@app.route('/api/productos', methods=['GET'])
def obtener_productos():

    lista = [p.to_dict() for p in productos]

    return jsonify({
        "total": len(lista),
        "productos": lista
    }), 200



@app.route('/api/productos', methods=['POST'])
def crear_producto():

    data = request.get_json()

    if not data or "nombre" not in data or "precio" not in data:
        return jsonify({"error": "Datos incompletos"}), 400

    nuevo = Producto(
        id=len(productos) + 1,
        nombre=data["nombre"],
        precio=data["precio"]
    )

    productos.append(nuevo)

    return jsonify({
        "mensaje": "Producto creado",
        "data": nuevo.to_dict()
    }), 201


if __name__ == '__main__':
    app.run(
        port=int(os.getenv("PORT", 5000)),
        debug=os.getenv("FLASK_DEBUG", "True") == "True"
    )