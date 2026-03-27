<template>
  <div class="admin-container">

    <!-- HEADER -->
    <div class="admin-header">
      <h2>📚 Admin Panel</h2>
      <button @click="$router.push('/')">← Kembali</button>
    </div>

    <div class="admin-content">

      <!-- FORM -->
      <div class="form-box">
        <h3>{{ editId ? "Edit Buku" : "Tambah Buku" }}</h3>

        <input v-model="form.judul" placeholder="Judul" />
        <input v-model="form.penulis" placeholder="Penulis" />
        <input v-model="form.penerbit" placeholder="Penerbit" />
        <input v-model="form.tahun_terbit" placeholder="Tahun Terbit" />
        <input v-model="form.deskripsi" placeholder="Deskripsi" />
        <input v-model="form.stok" placeholder="Stok" />

        <select v-model="form.kategori_id">
          <option disabled value="">Pilih Kategori</option>
          <option>teknologi</option>
          <option>sains</option>
          <option>novel</option>
          <option>kesehatan</option>
          <option>ekonomi</option>
        </select>

        <input v-model="form.cover_url" placeholder="Cover URL" />

        <button @click="save">
          {{ editId ? "Update" : "Tambah" }}
        </button>
      </div>

      <!-- TABLE -->
      <div class="table-box">
        <h3>Daftar Buku</h3>

        <table>
          <thead>
            <tr>
              <th>Cover</th>
              <th>Judul</th>
              <th>Penulis</th>
              <th>Kategori</th>
              <th>Stok</th>
              <th>Aksi</th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="b in books" :key="b.id">
              <td>
                <img :src="b.cover_url" />
              </td>
              <td>{{ b.judul }}</td>
              <td>{{ b.penulis }}</td>
              <td>{{ b.kategori_id }}</td>
              <td>{{ b.stok }}</td>
              <td>
                <button class="edit" @click="edit(b)">Edit</button>
                <button class="delete" @click="hapus(b.id)">Hapus</button>
              </td>
            </tr>
          </tbody>
        </table>

      </div>

    </div>
  </div>
</template>

<script>
import { getBooks, addBook, updateBook, deleteBook } from "../services/api";

export default {
  data() {
    return {
      books: [],
      form: {},
      editId: null
    };
  },
  methods: {
    async load() {
      const res = await getBooks();
      this.books = res.data;
    },

    async save() {
      if (this.editId) {
        await updateBook(this.editId, this.form);
      } else {
        await addBook(this.form);
      }

      this.form = {};
      this.editId = null;
      this.load();
    },

    edit(b) {
      this.form = { ...b };
      this.editId = b.id;
    },

    async hapus(id) {
      if (!confirm("Yakin hapus?")) return;

      await deleteBook(id);
      this.load();
    }
  },

  mounted() {
    this.load();
  }
};
</script>

<style>
.admin-container {
  padding: 20px;
  background: #f8fafc;
  min-height: 100vh;
}

/* HEADER */
.admin-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.admin-header h2 {
  color: #7f1d1d;
}

.admin-header button {
  background: #1e293b;
  color: white;
  padding: 8px 12px;
  border-radius: 8px;
  border: none;
}

/* LAYOUT */
.admin-content {
  display: flex;
  gap: 20px;
}

/* FORM */
.form-box {
  width: 300px;
  background: white;
  padding: 20px;
  border-radius: 12px;
}

.form-box input,
.form-box select {
  width: 100%;
  padding: 8px;
  margin-bottom: 10px;
  border-radius: 8px;
  border: 1px solid #ddd;
}

.form-box button {
  width: 100%;
  padding: 10px;
  background: #7f1d1d;
  color: white;
  border: none;
  border-radius: 8px;
}

/* TABLE */
.table-box {
  flex: 1;
  background: white;
  padding: 20px;
  border-radius: 12px;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 10px;
  border-bottom: 1px solid #eee;
  text-align: left;
}

td img {
  width: 50px;
  height: 70px;
  object-fit: cover;
  border-radius: 6px;
}

/* BUTTON */
.edit {
  background: #f59e0b;
  color: white;
  margin-right: 5px;
}

.delete {
  background: #ef4444;
  color: white;
}

button {
  border: none;
  padding: 6px 10px;
  border-radius: 6px;
  cursor: pointer;
}
</style>