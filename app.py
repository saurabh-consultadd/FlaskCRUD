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
        if 'email' in data:
            return jsonify({"error": "Email cannot be updated"})
        
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
def is_admin(request=True):
    return True 


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
    