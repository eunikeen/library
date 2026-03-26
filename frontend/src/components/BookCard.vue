<template>
  <div class="card">
    <h4>{{ book.judul }}</h4>
    <p>{{ book.penulis }}</p>
    <p>{{ book.penerbit }}</p>
    <p>{{ book.tahun_terbit }}</p>
    <p>{{ book.deskripsi }}</p>
    <p>Stok: {{ book.stok }}</p>
    <p>Kategori ID: {{ book.kategori_id }}</p>
    <p>Cover URL: {{ book.cover_url }}</p>

    <button @click="$emit('borrow', book.id)">Pinjam</button>
  </div>
</template>

<script>
export default {
  props: ["book"]
};
</script>

<style>
.card {
  width: 150px;
  padding: 10px;
  border-radius: 10px;
  background: white;
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
}
</style>