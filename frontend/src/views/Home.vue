<template>
  <div class="container">

    <div class="header">
      <h2 class="logo">Perpustakaan</h2>

      <input v-model="search" placeholder="Cari buku..." />

      <div class="actions">
        <button @click="$router.push('/login')">Login</button>
        <button @click="$router.push('/register')">Register</button>
        <button @click="goAdmin">Admin</button>

        <button v-if="userRole === 'user'" @click="$router.push('/user')">Buku Saya</button>
    </div>
    </div>

    <div class="hero">
      <h3>Temukan Buku Yang Anda Cari</h3>
    </div>

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

    <div class="grid">
      <BookCard
        v-for="b in filteredBooks"
        :key="b.id"
        :book="b"
        @borrow="borrow"
        @return="returnBook"
        @click.native="selected = b"
      />
    </div>

    <div v-if="selected" class="modal">
      <div class="modal-box">

        <div class="left">
          <img :src="selected.cover_url" />
    </div>

        <div class="right">
          <h2>{{ selected.judul }}</h2>

          <p class="author">
            {{ selected.pengarang }} ({{ selected.tahun_terbit }})
          </p>

          <p class="desc">
            {{ selected.deskripsi }}
      </p>

      <div class="meta">
        <span>📚 Stok: {{ selected.stok }}</span>
        <span>🏷️ {{ selected.kategori_id }}</span>
      </div>

      <div class="actions">
        <button class="btn primary" @click="borrow(selected.id)">
          Pinjam
        </button>

        <button 
          v-if="isUser" 
          class="btn primary" 
          @click="returnBook(selected.id)">
          Kembalikan
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
import { getBooks, borrowBook, returnBook as apiReturnBook } from "../services/api"
import BookCard from "../components/BookCard.vue";

export default {
    components: {
    BookCard
  },
  
  data() {
    return {
      books: [],
      selected: null,
      search: "",
      activeCategory: null,
      categories: ["Teknologi", "Sains", "Hukum", "Kesehatan", "Ekonomi"],

      userRole: null 
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
    },

    isLogin() {
      return !!localStorage.getItem("token");
    }
  },

  methods: {
    async load() {
      try {
        const res = await getBooks()
        console.log("DATA BUKU:", res.data)
        this.books = res.data
      } catch (err) {
        console.error(err)
      }
    },

    async borrow(id) {
      const token = localStorage.getItem("token");
      const role = localStorage.getItem("role");

      if (!token) {
        alert("Silakan login dulu!");
        this.$router.push("/login");
        return;
      }

      if (role === "admin") {
        alert("Admin tidak bisa meminjam!");
        return;
      }

      await borrowBook(id);
      alert("Berhasil pinjam");
      this.load();
    },

    async returnBook(id) {
      const token = localStorage.getItem("token")

      if (!token) {
        alert("Login dulu!")
        return
      }

      await apiReturnBook(id)
      alert("Berhasil kembali")
      this.load()
    },

    logout() {
      localStorage.removeItem("token")
      localStorage.removeItem("role")

      this.userRole = null
      this.$router.push("/login")
    },

    goAdmin() {
      const token = localStorage.getItem("token")
      const role = localStorage.getItem("role");

      if (!token) {
        alert("Login dulu!");
        this.$router.push("/login");
        return;
      }

      if (role !== "admin") {
        alert("Login sebagai admin dulu!");
        return;
      }

      this.$router.push("/admin");
    }
  },

  mounted() {
    this.userRole = localStorage.getItem("role")
    this.load();
  },

  watch: {
    $route() {
      this.userRole = localStorage.getItem("role")
    }
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

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(230px, 1fr));
  gap: 25px;
  padding: 40px;
}

.modal {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.7);

  display: flex;
  justify-content: center;
  align-items: center;

  backdrop-filter: blur(4px); 
}

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

.left img {
  width: 200px;
  height: 300px;
  object-fit: cover;
  border-radius: 12px;
}

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

.meta {
  display: flex;
  gap: 15px;
  font-size: 12px;
  margin-top: 30px;
  color: #ffffff;
}

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

.btn.primary {
  background: #ffffff;
  color: #690303;
}

.btn.primary:hover {
  background: #690303;
  color: #ffffff; 
}

.btn.secondary {
  background: #ffffff;
  color: #690303;
}

.btn.secondary:hover {
  background: #690303;
  color: #ffffff;
}
</style>