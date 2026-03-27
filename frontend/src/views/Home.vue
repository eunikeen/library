<template>
  <div class="container">

    <!-- HEADER -->
    <div class="header">
      <h2 class="logo">Perpustakaan</h2>

      <input v-model="search" placeholder="Cari buku..." />

      <div class="actions">
        <button @click="$router.push('/login')">Login</button>
        <button @click="$router.push('/register')">Register</button>
        <button class="admin" @click="goAdmin">Admin</button>
      </div>
    </div>

    <div class="hero">
      <h3>Temukan Buku Yang Anda Cari</h3>
    </div>

    <!-- CATEGORY -->
    <div class="categories">
      <span 
        :class="{ active: activeCategory === null }"
        @click="activeCategory = null"
      >
        All
      </span>

      <span 
        v-for="c in categories"
        :key="c"
        :class="{ active: activeCategory === c }"
        @click="activeCategory = c"
      >
        {{ c }}
      </span>
    </div>

    <!-- BOOK GRID -->
    <div class="grid">
      <div 
        v-for="b in filteredBooks"
        :key="b.id"
        class="card"
        @click="selected = b"
      >
        <img :src="b.cover_url" />
        <h4>{{ b.judul }}</h4>
        <p>{{ b.penulis }}</p>
      </div>
    </div>

    <!-- DETAIL MODAL -->
<div v-if="selected" class="modal">
  <div class="modal-box">

    <!-- IMAGE -->
    <div class="left">
      <img :src="selected.cover_url" />
    </div>

    <!-- INFO -->
    <div class="right">
      <h2>{{ selected.judul }}</h2>

      <p class="author">
        {{ selected.penulis }} ({{ selected.tahun_terbit }})
      </p>

      <p class="desc">
        {{ selected.deskripsi }}
      </p>

      <div class="meta">
        <span>📚 Stok: {{ selected.stok }}</span>
        <span>🏷️ {{ selected.kategori_id }}</span>
      </div>

      <!-- BUTTON -->
      <div class="actions">
        <button class="btn primary" @click="borrow(selected.id)">
          Pinjam
        </button>

        <button class="btn secondary" @click="selected = null">
          Tutup
        </button>
      </div>
    </div>

  </div>
</div>

  </div>
</template>

<script>
import { getBooks, borrowBook } from "../services/api";
import BookCard from "../components/BookCard.vue";
export default {
  components: { BookCard },
  data() {
    return {
      books: [],
      selected: null,
      search: "",
      activeCategory: null,
      categories: ["Teknologi", "Sains", "Novel", "Kesehatan", "Ekonomi"]
    };
  },

  computed: {
    filteredBooks() {
      return this.books.filter(b => {
        return (
          (!this.activeCategory || b.kategori_id === this.activeCategory) &&
          b.judul.toLowerCase().includes(this.search.toLowerCase())
        );
      });
    }
  },

  methods: {
    async load() {
      const res = await getBooks();
      this.books = res.data;
    },

    async borrow(id) {
      const token = localStorage.getItem("token");

      if (!token) {
        alert("Login dulu!");
        this.$router.push("/login");
        return;
      }

      await borrowBook(id);
      alert("Berhasil pinjam");
    },

    goAdmin() {
      const role = localStorage.getItem("role");

      if (role !== "admin") {
        alert("Harus login admin!");
        this.$router.push("/login");
        return;
      }

      this.$router.push("/admin");
    }
  },

  mounted() {
    this.load();
  }
};
</script>

<style>
.container {
  width: 100%;
  max-width: none;
  padding: 20px;
  background: #ffffff;
}

/* HEADER */
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 20px;
  font-weight:bold;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  margin-left: 20px;
  margin-right: 20px;
  color: #690303;
}

.header input {
  margin-left: 20px;

  width: 700px;
  padding: 10px;
  border-radius: 10px;
  border: none;
  background: #f6f6f6;
}

.header .actions button {
  font-size: 15px;
  font-weight:500;
  background: #690303;
  color: white;
  padding: 6px 14px;
  border-radius: 20px;
  margin-right: 10px;
  cursor: pointer;
}

.hero {
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 16px;
  font-weight:bold;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  color: #690303;
  padding-top: 5px;
}

/* CATEGORY */
.categories {
  margin: 3px 0;
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-bottom: 20px;
}

.categories span {
  margin-right: 2px;
  padding: 6px 15px;
  background: #690303;
  color: white;
  border-radius: 10px;
  cursor: pointer;
}

/* GRID */
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(230px, 1fr));
  gap: 25px;
  padding: 40px;
}

/* MODAL */
.modal {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.7);

  display: flex;
  justify-content: center;
  align-items: center;

  backdrop-filter: blur(4px); 
}

/* BOX */
.modal-box {
  display: flex;
  gap: 30px;
  background: #690303;
  padding: 25px;
  border-radius: 16px;

  width: 700px;
  max-width: 90%;

  box-shadow: 0 20px 40px rgba(0,0,0,0.2);
}

/* LEFT */
.left img {
  width: 200px;
  height: 300px;
  object-fit: cover;
  border-radius: 12px;
}

/* RIGHT */
.right {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 1px;
}

.right h2 {
  font-size: 30px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  font-weight: 800;
  color: #ffffff;
  margin-bottom: 1px;
}

.author {
  font-size: 20px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  font-weight: 600;
  color: #ffffff;
  margin-bottom: 10px;
}

.desc {
  font-size: 15px;
  font-weight: 450;
  margin-top: 5px;
  color: #ffffff;
  line-height: 1.5;
}

/* META */
.meta {
  display: flex;
  gap: 15px;
  font-size: 12px;
  margin-top: 30px;
  color: #ffffff;
}

/* BUTTONS */
.actions {
  display: flex;
  gap: 10px;
  margin-top: 15px;
}

.btn {
  padding: 8px 14px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  font-size: 13px;
}

/* PRIMARY */
.btn.primary {
  background: #ffffff;
  color: #690303;
}

.btn.primary:hover {
  background: #690303;
  color: #ffffff; 
}

/* SECONDARY */
.btn.secondary {
  background: #ffffff;
  color: #690303;
}

.btn.secondary:hover {
  background: #690303;
  color: #ffffff;
}
</style>