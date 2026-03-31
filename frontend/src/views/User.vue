<template>
  <div class="user-container">

    <!-- HEADER -->
    <div class="header">
      <h2>Buku Saya</h2>
      <button class="logout" @click="logout">Logout</button>
    </div>

    <!-- LOADING -->
    <p v-if="loading">Loading...</p>

    <!-- EMPTY -->
    <p v-if="!loading && borrowings.length === 0">
      Tidak ada buku yang dipinjam
    </p>

    <!-- LIST -->
    <div class="grid">
      <div v-for="b in borrowings" :key="b.id" class="card">

        <h3>{{ b.judul }}</h3>

        <p 
          :class="b.status === 'dipinjam' ? 'status red' : 'status green'"
        >
          Status: {{ b.status }}
        </p>

        <!-- BUTTON RETURN -->
        <button 
          v-if="b.status === 'dipinjam'"
          class="btn"
          @click="kembali(b.book_id)"
        >
          Kembalikan
        </button>

      </div>
    </div>

  </div>
</template>

<script>
import { getMyBorrowings, returnBook } from "../services/api"

export default {
  data() {
    return {
      borrowings: [],
      loading: false
    }
  },

  methods: {
    async load() {
      try {
        this.loading = true

        const res = await getMyBorrowings()
        console.log("BORROWINGS:", res.data)

        this.borrowings = res.data
      } catch (err) {
        console.error(err)
        alert("Gagal ambil data")
      } finally {
        this.loading = false
      }
    },

    async kembali(bookId) {
      try {
        console.log("RETURN BOOK ID:", bookId)

        await returnBook(bookId)

        alert("Berhasil dikembalikan")

        this.load()
      } catch (err) {
        console.error(err)
        alert("Gagal mengembalikan")
      }
    },

    logout() {
      localStorage.removeItem("token")
      localStorage.removeItem("role")
      this.$router.push("/login")
    }
  },

  mounted() {
    const token = localStorage.getItem("token")

    if (!token) {
      alert("Harus login dulu!")
      this.$router.push("/login")
      return
    }

    this.load()
  }
}
</script>

<style>
.user-container {
  padding: 20px;
  background: #f8fafc;
  min-height: 100vh;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.logout {
  background: #690303;
  color: white;
  border: none;
  padding: 8px 14px;
  border-radius: 8px;
  cursor: pointer;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 20px;
}

.card {
  background: white;
  padding: 15px;
  border-radius: 12px;
  border: 1px solid #eee;
  box-shadow: 0 5px 10px rgba(0,0,0,0.05);
}

.card h3 {
  margin-bottom: 10px;
}

.status {
  margin-bottom: 10px;
  font-weight: bold;
}

.red {
  color: #690303;
}

.green {
  color: #10b981;
}

.btn {
  background: #690303;
  color: white;
  border: none;
  padding: 8px 12px;
  border-radius: 6px;
  cursor: pointer;
}

.btn:hover {
  background: #690303;
}
</style>