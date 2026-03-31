<template>
  <div class="admin-container">

    <div class="admin-header">
      <h2>Admin Panel</h2>
      <button @click="$router.push('/')">← Kembali</button>
      <button @click="logout">Logout</button>
    </div>

    <div class="admin-content">

      <div class="form-box">
        <h3>{{ editId ? "Edit Buku" : "Tambah Buku" }}</h3>

        <input v-model="form.judul" placeholder="Judul" />
        <input v-model="form.pengarang" placeholder="Pengarang" />
        <input v-model="form.penerbit" placeholder="Penerbit" />
        <input v-model="form.tahun_terbit" placeholder="Tahun Terbit" />
        <input v-model="form.deskripsi" placeholder="Deskripsi" />
        <input v-model="form.stok" placeholder="Stok" />

        <select v-model="form.kategori_id">
          <option disabled value="">Pilih Kategori</option>
          <option>teknologi</option>
          <option>sains</option>
          <option>hukum</option>
          <option>kesehatan</option>
          <option>ekonomi</option>
        </select>

        <input v-model="form.cover_url" placeholder="Cover URL" />

        <button @click="save">
          {{ editId ? "Update" : "Tambah" }}
        </button>
      </div>

      <div class="table-box">
        <h3>Daftar Buku</h3>

        <table>
          <thead>
            <tr>
              <th>Cover</th>
              <th>Judul</th>
              <th>Pengarang</th>
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
              <td>{{ b.pengarang }}</td>
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

    logout() {
      localStorage.removeItem("token")
      localStorage.removeItem("role")
      this.userRole = null
      this.$router.push("/login")
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
    const role = localStorage.getItem("role");

    if (role !== "admin") {
      alert("Akses hanya untuk admin!");
      this.$router.push("/");
      return;
    }

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

.admin-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
  margin-left: 20px;
  margin-right: 20px;
}

.admin-header h2 {
  color: #690303;
}

.admin-header button {
  background: #690303;
  color: white;
  height: 40px;
  margin-top: 15px;
  padding: 8px 12px;
  border-radius: 8px;
  border: 1px solid #690303;
}

.admin-content {
  display: flex;
  gap: 20px;
}

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

.edit {
  background: #690303;
  color: white;
  margin-right: 5px;
}

.delete {
  background: #690303;
  color: white;
}

button {
  border: none;
  padding: 6px 10px;
  border-radius: 6px;
  cursor: pointer;
}
</style>