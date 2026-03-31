from flask import Flask, request, jsonify
from flask_cors import CORS
import bcrypt

from models import *
from auth import *

app = Flask(__name__)
CORS(app)

#AUTH
@app.route("/register", methods=["POST"])
def register():
    try:
        print("REGISTER DATA:", request.json)

        create_user(request.json)

        return jsonify({"message": "Registered"})
    except Exception as e:
        print("ERROR REGISTER:", e)
        return jsonify({"message": "Register gagal", "error": str(e)}), 500


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    user = get_user_by_username(data["username"])

    if not user:
        return jsonify({"message": "User not found"}), 404

    stored_password = user["password"]
    if isinstance(stored_password, str):
        stored_password = stored_password.encode()

    print(bcrypt.hashpw("admin".encode(), bcrypt.gensalt()))

    if not bcrypt.checkpw(data["password"].encode(), stored_password):
        return jsonify({"message": "Wrong password"}), 401

    token = generate_token(user)

    return jsonify({
        "token": token,
        "role": user["role"]
    })


#BOOK (USER)
@app.route("/books", methods=["GET"])
def books():
    return jsonify(get_all_books())

@app.route("/my-borrowings", methods=["GET"])
@token_required
def my_borrowings():
    user_id = request.user["id"]
    return jsonify(get_user_borrowings(user_id))

#BOOK (ADMIN)
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


#BORROW
@app.route("/borrow/<int:book_id>", methods=["POST"])
@token_required
def borrow(book_id):
    user_id = request.user["id"]

    if not borrow_book(user_id, book_id):
        return jsonify({"message": "Stok habis"}), 400

    return jsonify({"message": "Berhasil pinjam"})


@app.route("/return/<int:book_id>", methods=["POST"])
@token_required
def return_b(book_id):
    user_id = request.user["id"]

    success = return_book(user_id, book_id)

    if not success:
        return jsonify({"message": "Tidak ada pinjaman"}), 400

    return jsonify({"message": "Berhasil dikembalikan"})


#ADMIN
@app.route("/borrowings", methods=["GET"])
@token_required
@admin_only
def all_borrow():
    return jsonify(get_borrowings())


if __name__ == "__main__":
    app.run(debug=True)