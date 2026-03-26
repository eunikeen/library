<template>
  <div class="container">
    <div class="sidebar">
      <h2>⚙️ Admin Panel</h2>

      <ul>
        <li @click="$router.push('/')">🏠 Home</li>
        <li @click="$router.push('/admin')">📚 Kelola Buku</li>
        <li @click="logout">🚪 Logout</li>
      </ul>
    </div>

    <div class="content">
      <router-view />
    </div>
  </div>
</template>

<script>
export default {
  methods: {
    logout() {
      localStorage.clear();
      this.$router.push("/login");
    }
  }
};
</script>

<style>
.container {
  display: flex;
}

.sidebar {
  width: 220px;
  height: 100vh;
  background: #f4f6f9;
  padding: 20px;
}

.content {
  flex: 1;
  padding: 20px;
}
</style>