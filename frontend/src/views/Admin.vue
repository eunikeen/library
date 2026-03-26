<template>
  <div>
    <h3>Tambah Buku</h3>

    <input v-model="form.judul" placeholder="Judul" />
    <input v-model="form.penulis" placeholder="Penulis" />
    <input v-model="form.penerbit" placeholder="Penerbit" />
    <input v-model="form.tahun_terbit" placeholder="Tahun Terbit" />
    <input v-model="form.deskripsi" placeholder="Deskripsi" />
    <input v-model="form.stok" placeholder="Stok" />
    <input v-model="form.kategori_id" placeholder="Kategori ID" />
    <input v-model="form.cover_url" placeholder="Cover URL" />

    <button @click="save">Tambah</button>

    <h3>Daftar Buku</h3>

    <div v-for="b in books" :key="b.id">
      {{ b.judul }}

      <button @click="edit(b)">Edit</button>
      <button @click="hapus(b.id)">Hapus</button>
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
      await deleteBook(id);
      this.load();
    }
  },
  mounted() {
    this.load();
  }
};
</script>