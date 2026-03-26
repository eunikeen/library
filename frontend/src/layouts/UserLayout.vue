<template>
  <div class="container">
    <Sidebar />
    <div class="content">
      <router-view />
    </div>
  </div>
</template>

<script>
import Sidebar from "../components/Sidebar.vue";
export default { components: { Sidebar } };
</script>

<style>
.container {
  display: flex;
}
.content {
  flex: 1;
  padding: 20px;
}
</style>