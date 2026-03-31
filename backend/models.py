from db import get_db
import bcrypt

#BOOK
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
        """INSERT INTO books 
        (judul, pengarang, penerbit, tahun_terbit, deskripsi, stok, kategori_id, cover_url) 
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",
        (
            data["judul"],
            data["pengarang"],
            data["penerbit"],
            data["tahun_terbit"],
            data["deskripsi"],
            data.get("stok", 5),
            data.get("kategori_id"),
            data.get("cover_url")
        )
    )

    conn.commit()
    conn.close()


def update_book(book_id, data):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE books 
        SET judul=%s, pengarang=%s, penerbit=%s, tahun_terbit=%s, deskripsi=%s, stok=%s, kategori_id=%s, cover_url=%s
        WHERE id=%s
    """, (
        data["judul"],
        data["pengarang"],
        data["penerbit"],
        data["tahun_terbit"],
        data["deskripsi"],
        data.get("stok", 5),
        data.get("kategori_id"),
        data.get("cover_url"),
        book_id
    ))

    conn.commit()
    conn.close()


def delete_book(book_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE id=%s", (book_id,))
    conn.commit()
    conn.close()


#USER
def create_user(data):
    conn = get_db()
    cursor = conn.cursor()

    import bcrypt
    hashed = bcrypt.hashpw(data["password"].encode(), bcrypt.gensalt())

    cursor.execute(
        "INSERT INTO users (username, password, role) VALUES (%s,%s,%s)",
        (data["username"], hashed, data.get("role", "user"))
    )

    conn.commit()
    conn.close()
def get_user_borrowings(user_id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            b.id,
            b.book_id,
            u.username,
            bk.judul,
            bk.cover_url,
            b.tanggal_pinjam,
            b.status
        FROM borrowings b
        JOIN users u ON b.user_id = u.id
        JOIN books bk ON b.book_id = bk.id
        WHERE b.user_id = %s
    """, (user_id,))

    data = cursor.fetchall()
    conn.close()
    return data

def get_user_by_username(username):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    user = cursor.fetchone()

    conn.close()
    return user

#BORROWING
def borrow_book(user_id, book_id):
    conn = get_db()
    cursor = conn.cursor()

    # cek stok
    cursor.execute("SELECT stok FROM books WHERE id=%s", (book_id,))
    book = cursor.fetchone()

    if not book or book[0] <= 0:
        conn.close()
        return False

    # insert transaksi
    cursor.execute("""
        INSERT INTO borrowings (user_id, book_id, tanggal_pinjam, status)
        VALUES (%s, %s, CURDATE(), 'dipinjam')
    """, (user_id, book_id))

    # kurangi stok
    cursor.execute(
        "UPDATE books SET stok = stok - 1 WHERE id=%s",
        (book_id,)
    )

    conn.commit()
    conn.close()
    return True


def return_book(user_id, book_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id FROM borrowings
        WHERE user_id=%s AND book_id=%s AND status='dipinjam'
        LIMIT 1
    """, (user_id, book_id))

    data = cursor.fetchone()

    if not data:
        conn.close()
        return False

    borrow_id = data[0]

    cursor.execute("""
        UPDATE borrowings
        SET status='kembali', tanggal_kembali=CURDATE()
        WHERE id=%s
    """, (borrow_id,))

    cursor.execute("UPDATE books SET stok = stok + 1 WHERE id=%s", (book_id,))

    conn.commit()
    conn.close()

    return True


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