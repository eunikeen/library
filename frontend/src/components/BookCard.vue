<template>
  <div class="card">
    <img :src="book.cover_url" />
    <h4>{{ book.judul }}</h4>
    <p>{{ book.pengarang }}</p>
  </div>
</template>

<script>
export default {
  props: ["book"]
};
</script>

<style>
.card {
  border-radius: 18px;
  overflow: hidden;
  transition: 0.3s;
  cursor: pointer;
  color: #690303;
  border: 1px solid #e2e8f0;
}

.card:hover {
  transform: translateY(-6px);
  box-shadow: 0 10px 20px rgba(0,0,0,0.08);
}

.card img {
  width: 100%;
  height: 300px;
  border-radius: 10px;
}

.card h4 {
  font-size: 15px;
  margin: 8px 0 4px;
}

.card p {
  font-size: 12px;
  color: #000000;
}
</style>