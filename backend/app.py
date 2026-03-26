from flask import Flask, request, jsonify
from flask_cors import CORS
import bcrypt

from models import get_categories, add_category
from models import *
from auth import *

app = Flask(__name__)
CORS(app)

# ========================
# AUTH
# ========================
@app.route("/register", methods=["POST"])
def register():
    create_user(request.json)
    return jsonify({"message": "Registered"})


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    user = get_user_by_username(data["username"])

    if not user:
        return jsonify({"message": "User not found"}), 404

    if not bcrypt.checkpw(data["password"].encode(), user["password"].encode()):
        return jsonify({"message": "Wrong password"}), 401

    token = generate_token(user)

    return jsonify({
        "token": token,
        "role": user["role"]
    })


# ========================
# BOOK (USER)
# ========================
@app.route("/books", methods=["GET"])
@token_required
def books():
    return jsonify(get_all_books())


# ========================
# BOOK (ADMIN)
# ========================
@app.route("/books", methods=["POST"])
@token_required
@admin_only
def add():
    add_book(request.json)
    return jsonify({"message": "Added"})


@app.route("/books/<int:id>", methods=["PUT"])
@token_required
@admin_only
def update(id):
    update_book(id, request.json)
    return jsonify({"message": "Updated"})


@app.route("/books/<int:id>", methods=["DELETE"])
@token_required
@admin_only
def delete(id):
    delete_book(id)
    return jsonify({"message": "Deleted"})


# ========================
# BORROW
# ========================
@app.route("/borrow/<int:book_id>", methods=["POST"])
@token_required
def borrow(book_id):
    user_id = request.user["id"]

    if not borrow_book(user_id, book_id):
        return jsonify({"message": "Stok habis"}), 400

    return jsonify({"message": "Berhasil pinjam"})


@app.route("/return/<int:id>", methods=["POST"])
@token_required
def return_b(id):
    return_book(id)
    return jsonify({"message": "Dikembalikan"})


@app.route("/borrowings", methods=["GET"])
@token_required
@admin_only
def all_borrow():
    return jsonify(get_borrowings())


if __name__ == "__main__":
    app.run(debug=True)

