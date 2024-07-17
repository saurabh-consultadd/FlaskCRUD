from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
db = SQLAlchemy(app)


# Product Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)


# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=False)


# Routes for Products
@app.route("/products", methods=["GET"])
def get_products():
    products = Product.query.all()
    if products:
        return jsonify([{
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "quantity": product.quantity
        } for product in products])
    else:
        return jsonify({"message": "Product not found"})

# SHow product by id
@app.route("/showProduct/<int:id>", methods=["GET"])
def get_product_by_id(id):
    product = Product.query.get(id)
    if product:
        return jsonify({
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "quantity": product.quantity
        })
    else:
        return jsonify({"message": "Product not found"})

@app.route("/products", methods=["POST"])
def create_product():
    data = request.json
    name = data.get('name')
    price = data.get('price')
    quantity = data.get('quantity')

    # Check if a product with the same name, price, and quantity exists
    existing_product = Product.query.filter_by(name=name, price=price, quantity=quantity).first()

    if existing_product:
        return jsonify({"error": "Product already exists with the same name, price, and quantity."})

    # If no existing product found, create a new one
    new_product = Product(name=name, price=price, quantity=quantity)
    db.session.add(new_product)
    db.session.commit()
    return jsonify({"message": "Product added successfully."})


@app.route("/products/<int:id>", methods=["PUT"])
def update_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({"error": "Product not found"})

    data = request.json
    product.name = data.get('name', product.name)
    product.price = data.get('price', product.price)
    product.quantity = data.get('quantity', product.quantity)
    db.session.commit()
    return jsonify({"message": "Product updated successfully."})

@app.route("/products/<int:id>", methods=["DELETE"])
def delete_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({"error": "Product not found"})

    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted successfully."})



# Routes for Users
@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([{
        "id": user.id,
        "username": user.username,
        "role": user.role
    } for user in users])

@app.route("/users", methods=["POST"])
def create_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')

    # Check if username already exists
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"error": "Username already exists"})

    new_user = User(username=username, password=password, role=role)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User added successfully."})

@app.route("/users/<int:id>", methods=["PUT"])
def update_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"error": "User not found"})

    data = request.json
    user.username = data.get('username', user.username)
    user.password = data.get('password', user.password)
    user.role = data.get('role', user.role)
    db.session.commit()

    return jsonify({"message": "User updated successfully."})

@app.route("/users/<int:id>", methods=["DELETE"])
def delete_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"error": "User not found"})

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully."})

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
