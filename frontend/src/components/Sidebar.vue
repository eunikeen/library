<template>
  <div class="sidebar">
    <h2>📘 BookBase</h2>

    <ul>
      <li>🏠 Discover</li>
      <li>📂 Category</li>
      <li>📚 My Library</li>
      <li>⬇️ Download</li>
      <li>❤️ Favourite</li>

      <li v-if="role==='admin'" @click="$router.push('/admin')">
        ⚙️ Admin
      </li>

      <li @click="logout">🚪 Logout</li>
    </ul>
  </div>
</template>

<script>
export default {
  data() {
    return {
      role: localStorage.getItem("role")
    };
  },
  methods: {
    logout() {
      localStorage.clear();
      this.$router.push("/login");
    }
  }
};
</script>

<style>
.sidebar {
  width: 220px;
  height: 100vh;
  background: #f4f6f9;
  padding: 20px;
}
.sidebar ul {
  list-style: none;
  padding: 0;
}
.sidebar li {
  margin: 15px 0;
  cursor: pointer;
}
</style>