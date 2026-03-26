from db import get_db
import bcrypt

# ========================
# BOOK
# ========================
def get_all_books():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM books")
    data = cursor.fetchall()
    conn.close()
    return data


def add_book(data):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO books (judul, penulis, penerbit, tahun_terbit, deskripsi, stok, kategori_id, cover_url) VALUES (%s,%s,%s,%s,%s,%s)",
        (data["judul"], data["penulis"], data["penerbit"], data["tahun_terbit"], data["deskripsi"], data.get("stok", 5), data("kategori_id"), data.get("cover_url"))
    )
    conn.commit()
    conn.close()


def update_book(book_id, data):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE books 
        SET judul=%s, penulis=%s, penerbit=%s, tahun_terbit=%s, deskripsi=%s, stok=%s, kategori_id=%s, cover_url=%s
        WHERE id=%s
    """, (data["judul"], data["penulis"], data["penerbit"], data["tahun_terbit"], data["deskripsi"], data.get("stok", 5), data("kategori_id"), data.get("cover_url"), book_id))
    conn.commit()
    conn.close()


def delete_book(book_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE id=%s", (book_id,))
    conn.commit()
    conn.close()


# ========================
# USER
# ========================
def create_user(data):
    conn = get_db()
    cursor = conn.cursor()

    hashed = bcrypt.hashpw(data["password"].encode(), bcrypt.gensalt())

    cursor.execute(
        "INSERT INTO users (username, password, role) VALUES (%s,%s,%s)",
        (data["username"], hashed, data.get("role", "user"))
    )

    conn.commit()
    conn.close()


def get_user_by_username(username):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    user = cursor.fetchone()

    conn.close()
    return user


# ========================
# BORROWING
# ========================
def borrow_book(user_id, book_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT stok FROM books WHERE id=%s", (book_id,))
    book = cursor.fetchone()

    if not book or book[0] <= 0:
        conn.close()
        return False

    cursor.execute("""
        INSERT INTO borrowings (user_id, book_id, tanggal_pinjam, status)
        VALUES (%s, %s, CURDATE(), 'dipinjam')
    """, (user_id, book_id))

    cursor.execute("UPDATE books SET stok = stok - 1 WHERE id=%s", (book_id,))

    conn.commit()
    conn.close()
    return True


def return_book(borrow_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT book_id FROM borrowings WHERE id=%s", (borrow_id,))
    data = cursor.fetchone()
    book_id = data[0]

    cursor.execute("""
        UPDATE borrowings 
        SET status='kembali', tanggal_kembali=CURDATE()
        WHERE id=%s
    """, (borrow_id,))

    cursor.execute("UPDATE books SET stok = stok + 1 WHERE id=%s", (book_id,))

    conn.commit()
    conn.close()


def get_borrowings():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT b.id, u.username, bk.judul, b.tanggal_pinjam, b.status
        FROM borrowings b
        JOIN users u ON b.user_id = u.id
        JOIN books bk ON b.book_id = bk.id
    """)

    data = cursor.fetchall()
    conn.close()
    return data