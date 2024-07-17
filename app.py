# from flask import Flask, request, jsonify
# from flask_sqlalchemy import SQLAlchemy

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
# db = SQLAlchemy(app)



# # Product Model
# class Product(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     price = db.Column(db.Float, nullable=False)
#     quantity = db.Column(db.Integer, nullable=False)



# # Routes for Products
# # @app.route("/products", methods=["GET"])
# # def get_products():
# #     products = Product.query.all()
# #     if products:
# #         return jsonify([{
# #             "id": product.id,
# #             "name": product.name,
# #             "price": product.price,
# #             "quantity": product.quantity
# #         } for product in products])
# #     else:
# #         return jsonify({"message": "Product not found"})


# @app.route("/products", methods=["GET"])
# def get_products():
#     try:
#         products = Product.query.all()
#         if not product:
#             return jsonify({"error": "Product not found"})

#         products_list = []
#         for product in products:
#             products_list.append({
#                 "id": product.id,
#                 "name": product.name,
#                 "price": product.price,
#                 "quantity": product.quantity
#             })

#         return jsonify(products_list)

#     except Exception as e:
#         return jsonify({"error": str(e)})

#     finally:
#         db.session.close()



# # SHow product by id
# # @app.route("/showProduct/<int:id>", methods=["GET"])
# # def get_product_by_id(id):
# #     product = Product.query.get(id)
# #     if product:
# #         return jsonify({
# #             "id": product.id,
# #             "name": product.name,
# #             "price": product.price,
# #             "quantity": product.quantity
# #         })
# #     else:
# #         return jsonify({"message": "Product not found"})



# @app.route("/products/<int:id>", methods=["GET"])
# def get_product_by_id(id):
#     try:
#         product = Product.query.get(id)
#         if not product:
#             return jsonify({"error": "Product not found"})
        
#         product_data = {
#             "id": product.id,
#             "name": product.name,
#             "price": product.price,
#             "quantity": product.quantity
#         }
#         return jsonify(product_data)

#     except Exception as e:
#         return jsonify({"error": str(e)})
    
#     finally:
#         db.session.close()



# @app.route("/products", methods=["POST"])
# def create_product():
#     try:
#         data = request.json
#         # Check if any required field is missing
#         if not name and not price and not quantity:
#             return jsonify({"error": "Missing required fields"})

#         # Assign default values if fields are not provided
#         name = data.get('name')
#         price = data.get('price')
#         quantity = data.get('quantity')

#         default_price = 0.0
#         default_quantity = 0

#         if not price:
#             price = default_price
#         if not quantity:
#             quantity = default_quantity

#         # Check if a product with the same name, price, and quantity exists
#         existing_product = Product.query.filter_by(name=name, price=price, quantity=quantity).first()
#         if existing_product:
#             return jsonify({"error": "Product already exists with the same name, price, and quantity."})

#         # If no existing product found, create a new one
#         new_product = Product(name=name, price=price, quantity=quantity)
#         db.session.add(new_product)
#         db.session.commit()

#         return jsonify({"message": "Product added successfully."})

#     except Exception as e:
#         db.session.rollback()
#         return jsonify({"error": str(e)})

#     finally:
#         db.session.close()



# @app.route("/products/<int:id>", methods=["PUT"])
# def update_product(id):
#     try:
#         product = Product.query.get(id)
#         if not product:
#             return jsonify({"error": "Product not found"})
        
#         data = request.json
#         if not data:
#             return jsonify({"error": "No data provided for update"})

#         if 'name' in data:
#             product.name = data['name']
#         if 'price' in data:
#             product.price = data['price']
#         if 'quantity' in data:
#             product.quantity = data['quantity']

#         db.session.commit()
#         return jsonify({"message": "Product updated successfully"})

#     except Exception as e:
#         db.session.rollback()
#         return jsonify({"error": str(e)}), 500

#     finally:
#         db.session.close()


# # @app.route("/products", methods=["POST"])
# # def create_product():
# #     data = request.json
# #     name = data.get('name')
# #     price = data.get('price')
# #     quantity = data.get('quantity')

# #     # Check if a product with the same name, price, and quantity exists
# #     existing_product = Product.query.filter_by(name=name, price=price, quantity=quantity).first()

# #     if existing_product:
# #         return jsonify({"error": "Product already exists with the same name, price, and quantity."})

# #     # If no existing product found, create a new one
# #     new_product = Product(name=name, price=price, quantity=quantity)
# #     db.session.add(new_product)
# #     db.session.commit()



# # @app.route("/products/<int:id>", methods=["PUT"])
# # def update_product(id):
# #     product = Product.query.get(id)
# #     if not product:
# #         return jsonify({"error": "Product not found"})

# #     data = request.json
# #     product.name = data.get('name', product.name)
# #     product.price = data.get('price', product.price)
# #     product.quantity = data.get('quantity', product.quantity)
# #     db.session.commit()
# #     return jsonify({"message": "Product updated successfully."})


# @app.route("/products/<int:id>", methods=["DELETE"])
# def delete_product(id):
#     try:
#         product = Product.query.get(id)
#         if not product:
#             return jsonify({"error": "Product not found"}), 404

#         db.session.delete(product)
#         db.session.commit()
#         return jsonify({"message": "Product deleted successfully."})

#     except Exception as e:
#         db.session.rollback()
#         return jsonify({"error": str(e)}), 500

#     finally:
#         db.session.close()


# # @app.route("/products/<int:id>", methods=["DELETE"])
# # def delete_product(id):
# #     product = Product.query.get(id)
# #     if not product:
# #         return jsonify({"error": "Product not found"})

# #     db.session.delete(product)
# #     db.session.commit()
# #     return jsonify({"message": "Product deleted successfully."})


# if __name__ == "__main__":
#     with app.app_context():
#         db.create_all()
#     app.run(debug=True)






# from flask import Flask, request, jsonify
# from flask_sqlalchemy import SQLAlchemy

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# db = SQLAlchemy(app)

# # Product Model
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     price = db.Column(db.Float, nullable=False)
#     quantity = db.Column(db.Integer, nullable=False)


# # Get all Products
# @app.route("/products", methods=["GET"])
# def get_products():
#     try:
#         products = Product.query.all()

#         products_list = []
#         for product in products:
#             products_list.append({
#                 "id": product.id,
#                 "name": product.name,
#                 "price": product.price,
#                 "quantity": product.quantity
#             })

#         return jsonify(products_list)

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


# # Get Product by ID
# @app.route("/products/<int:id>", methods=["GET"])
# def get_product_by_id(id):
#     try:
#         product = Product.query.get(id)

#         if not product:
#             return jsonify({"error": "Product not found"}), 404

#         product_data = {
#             "id": product.id,
#             "name": product.name,
#             "price": product.price,
#             "quantity": product.quantity
#         }

#         return jsonify(product_data)

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


# # Create Product
# @app.route("/products", methods=["POST"])
# def create_product():
#     try:
#         data = request.json

#         if not all(key in data for key in ['name', 'price', 'quantity']):
#             return jsonify({"error": "Missing required fields"}), 400

#         name = data['name']
#         price = data['price']
#         quantity = data['quantity']

#         # Check if a product with the same name, price, and quantity exists
#         existing_product = Product.query.filter_by(name=name, price=price, quantity=quantity).first()
#         if existing_product:
#             return jsonify({"error": "Product already exists with the same name, price, and quantity."}), 400

#         new_product = Product(name=name, price=price, quantity=quantity)
#         db.session.add(new_product)
#         db.session.commit()
#         return jsonify({"message": "Product added successfully."}), 201

#     except Exception as e:
#         db.session.rollback()
#         return jsonify({"error": str(e)}), 500

#     finally:
#         db.session.close()


# # Update Product by ID
# @app.route("/products/<int:id>", methods=["PUT"])
# def update_product(id):
#     try:
#         product = Product.query.get(id)
#         if not product:
#             return jsonify({"error": "Product not found"}), 404

#         data = request.json
#         product.name = data.get('name', product.name)
#         product.price = data.get('price', product.price)
#         product.quantity = data.get('quantity', product.quantity)
#         db.session.commit()
#         return jsonify({"message": "Product updated successfully."})

#     except Exception as e:
#         db.session.rollback()
#         return jsonify({"error": str(e)}), 500

#     finally:
#         db.session.close()


# # Delete Product by ID
# @app.route("/products/<int:id>", methods=["DELETE"])
# def delete_product(id):
#     try:
#         product = Product.query.get(id)
#         if not product:
#             return jsonify({"error": "Product not found"}), 404

#         db.session.delete(product)
#         db.session.commit()
#         return jsonify({"message": "Product deleted successfully."})

#     except Exception as e:
#         db.session.rollback()
#         return jsonify({"error": str(e)}), 500

#     finally:
#         db.session.close()

# if __name__ == "__main__":
#     with app.app_context():
#         db.create_all()
#     app.run(debug=True)




from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from email_validator import validate_email, EmailNotValidError


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)


# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False, default="123")
    role = db.Column(db.String(50), nullable=False, default="user")


# GET All User
@app.route("/users", methods=["GET"])
def get_users():
    try:
        users = User.query.all()
        users_list = []

        for user in users:
            users_list.append({
                "id": user.id,
                "email": user.email,
                "role": user.role
            })

        if users_list.count() == 0:
            return jsonify({"No users found"})
        return jsonify(users_list)

    except Exception as e:
        return jsonify({"error": str(e)})
    

# GET User by ID
@app.route("/users/<int:id>", methods=["GET"])
def get_user_by_id(id):
    try:
        user = User.query.get(id)
        if not user:
            return jsonify({"error": "User not found"})

        user_data = {
            "id": user.id,
            "email": user.email,
            "role": user.role
        }

        return jsonify(user_data)

    except Exception as e:
        return jsonify({"error": str(e)})
    

# POST Create User
@app.route("/users", methods=["POST"])
def create_user():
    try:
        data = request.json
        if 'email' not in data:
            return jsonify({"error": "Email is required"}), 400

        email = data['email']
        password = data.get('password', '123')
        role = data.get('role', 'user')

        try:
            validate_email(email)
        except EmailNotValidError:
            return jsonify({"error": "Invalid email format. Must be a valid email address."}), 400

        # Check if a user with the same email exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({"error": "Email already exists"})

        new_user = User(email=email, password=password, role=role)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User added successfully."})

    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Email must be unique"})

    except EmailNotValidError:
        db.session.rollback()
        return jsonify({"error": "Invalid email format."})

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        db.session.close()


# PUT Update User by ID
@app.route("/users/<int:id>", methods=["PUT"])
def update_user(id):
    try:
        user = User.query.get(id)
        if not user:
            return jsonify({"error": "User not found"})

        data = request.json
        if 'password' in data:
            user.password = data['password'] if data['password'] else user.password

        if 'role' in data:
            user.role = data['role'] if data['role'] else user.role

        db.session.commit()
        return jsonify({"message": "User updated successfully."})

    except EmailNotValidError:
        db.session.rollback()
        return jsonify({"error": "Invalid email format."})

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)})

    finally:
        db.session.close()


# DELETE User by ID (Accessible to Admin Only)
@app.route("/users/<int:id>", methods=["DELETE"])
def delete_user(id):
    try:
        if not is_admin(request):
            return jsonify({"error": "Unauthorized access."})

        user = User.query.get(id)
        if not user:
            return jsonify({"error": "User not found"})

        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully."})

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)})

    finally:
        db.session.close()

# Function to check if the request is from an admin
def is_admin(request):
    return True 

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
