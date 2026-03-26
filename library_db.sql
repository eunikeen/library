CREATE DATABASE library_db;
USE library_db;

CREATE TABLE IF NOT EXISTS users (
    id INT(11) AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(200) NOT NULL,
    role ENUM('admin', 'user') DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  
);
INSERT INTO users (username, password, role) VALUES
('admin', 'admin', 'admin'),
('user', 'user', 'user');

CREATE TABLE IF NOT EXISTS books (
    id INT(11) AUTO_INCREMENT PRIMARY KEY,
    judul VARCHAR(200) NOT NULL,
    penulis VARCHAR(200) DEFAULT NULL,
    penerbit VARCHAR(200) DEFAULT NULL,
    tahun_terbit INT(10) DEFAULT NULL,
    deskripsi TEXT DEFAULT NULL,
    stok INT(11) DEFAULT 5,
    kategori_id ENUM('teknologi', 'sains', 'novel', 'kesehatan', 'ekonomi') NOT NULL,
    cover_url VARCHAR(500) NOT NULL
);
INSERT INTO books (judul, penulis, penerbit, tahun_terbit, deskripsi, stok, kategori_id, cover_url) VALUES

-- ================== TEKNOLOGI ==================
('Clean Code', 'Robert C. Martin', 'Prentice Hall', 2008, 'Panduan menulis kode yang bersih dan mudah dipahami.', 8, 1, 'https://covers.openlibrary.org/b/isbn/9780132350884-L.jpg'),

('The Pragmatic Programmer', 'Andrew Hunt, David Thomas', 'Addison-Wesley', 1999, 'Panduan praktis menjadi programmer profesional.', 7, 1, 'https://covers.openlibrary.org/b/isbn/9780201616224-L.jpg'),

('Introduction to Algorithms', 'Thomas H. Cormen', 'MIT Press', 2009, 'Buku utama untuk algoritma dan struktur data.', 6, 1, 'https://covers.openlibrary.org/b/isbn/9780262033848-L.jpg'),

-- ================== SAINS ==================
('A Brief History of Time', 'Stephen Hawking', 'Bantam Books', 1988, 'Penjelasan tentang alam semesta dan konsep waktu.', 9, 2, 'https://covers.openlibrary.org/b/isbn/9780553380163-L.jpg'),

('Cosmos', 'Carl Sagan', 'Random House', 1980, 'Eksplorasi ilmu pengetahuan dan alam semesta.', 7, 2, 'https://covers.openlibrary.org/b/isbn/9780345539434-L.jpg'),

('The Selfish Gene', 'Richard Dawkins', 'Oxford University Press', 1976, 'Teori evolusi melalui perspektif gen.', 5, 2, 'https://covers.openlibrary.org/b/isbn/9780192860927-L.jpg'),

-- ================== NOVEL ==================
('Laskar Pelangi', 'Andrea Hirata', 'Bentang Pustaka', 2005, 'Kisah inspiratif anak-anak Belitung.', 10, 3, 'https://covers.openlibrary.org/b/isbn/9789793062791-L.jpg'),

('Bumi Manusia', 'Pramoedya Ananta Toer', 'Hasta Mitra', 1980, 'Novel sejarah tentang perjuangan di masa kolonial.', 8, 3, 'https://covers.openlibrary.org/b/isbn/9789799731233-L.jpg'),

('Harry Potter and the Sorcerer\'s Stone', 'J.K. Rowling', 'Bloomsbury', 1997, 'Petualangan Harry Potter di dunia sihir.', 12, 3, 'https://covers.openlibrary.org/b/isbn/9780439708180-L.jpg'),

-- ================== KESEHATAN ==================
('Gray\'s Anatomy for Students', 'Richard Drake', 'Elsevier', 2014, 'Buku anatomi manusia untuk mahasiswa kedokteran.', 6, 4, 'https://covers.openlibrary.org/b/isbn/9780702051319-L.jpg'),

('Robbins Basic Pathology', 'Vinay Kumar', 'Elsevier', 2017, 'Dasar patologi untuk mahasiswa medis.', 5, 4, 'https://covers.openlibrary.org/b/isbn/9780323353175-L.jpg'),

('Guyton and Hall Textbook of Medical Physiology', 'John E. Hall', 'Elsevier', 2016, 'Dasar fisiologi manusia.', 4, 4, 'https://covers.openlibrary.org/b/isbn/9781455770052-L.jpg'),

-- ================== EKONOMI ==================
('Principles of Economics', 'N. Gregory Mankiw', 'Cengage Learning', 2017, 'Dasar teori ekonomi mikro dan makro.', 9, 5, 'https://covers.openlibrary.org/b/isbn/9781305585126-L.jpg'),

('Rich Dad Poor Dad', 'Robert T. Kiyosaki', 'Warner Books', 1997, 'Pelajaran keuangan pribadi.', 11, 5, 'https://covers.openlibrary.org/b/isbn/9781612680194-L.jpg'),

('Freakonomics', 'Steven D. Levitt', 'William Morrow', 2005, 'Pendekatan ekonomi dalam kehidupan sehari-hari.', 7, 5, 'https://covers.openlibrary.org/b/isbn/9780060731335-L.jpg');

CREATE TABLE IF NOT EXISTS borrowings (
    id INT(11) AUTO_INCREMENT PRIMARY KEY,
    user_id INT(11) DEFAULT NULL,
    book_id INT(11) DEFAULT NULL,
    tanggal_pinjam DATE DEFAULT NULL,
    tanggal_kembali DATE DEFAULT NULL,
    status ENUM('dipinjam', 'kembali') DEFAULT 'dipinjam',
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (book_id) REFERENCES books(id)
);
