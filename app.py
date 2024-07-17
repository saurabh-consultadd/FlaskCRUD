from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
db = SQLAlchemy(app)


# Database Schema
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)


# Show all products
@app.route("/showProduct", methods=["GET"])
def get_products():
    products = Product.query.all()
    return jsonify([{
        "id": product.id,
        "name": product.name,
        "price": product.price,
        "quantity": product.quantity
    } for product in products])


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


# Add product
@app.route("/addProduct", methods=["POST"])
def create_product():
    data = request.json
    name = data.get("name")
    price = data.get("price")
    quantity = data.get("quantity")

    # Check if a product with the same name, price, and quantity exists
    existing_product = Product.query.filter_by(name=name, price=price, quantity=quantity).first()

    # Check if a product with the same name and price exists
    if not existing_product:
        existing_product = Product.query.filter_by(name=name, price=price).first()

    # Check if a product with the same name and quantity exists
    if not existing_product:
        existing_product = Product.query.filter_by(name=name, quantity=quantity).first()

    if existing_product:
        return jsonify({"error": "Product already exists."})


    new_product = Product(name=name, price=price, quantity=quantity)
    db.session.add(new_product)
    db.session.commit()

    return jsonify({"message": "Product added successfully."})



# Update Product
@app.route("/updateProduct/<int:id>", methods=["PUT"])
def update_product(id):
    product = Product.query.get(id)
    data = request.json
    product.name = data['name']
    product.price = data['price']
    product.quantity = data['quantity']
    db.session.commit()
    return jsonify({"message": "Product updated successfully."})


# Delete Product
@app.route("/deleteProduct/<int:id>", methods=["DELETE"])
def delete_product(id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted successfully."})



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
