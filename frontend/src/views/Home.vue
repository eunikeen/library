<template>
  <div>
    <h2>Recommended</h2>

    <div class="grid">
      <BookCard
        v-for="b in books"
        :key="b.id"
        :book="b"
        @borrow="pinjam"
      />
    </div>
  </div>
</template>

<script>
import { getBooks, borrowBook } from "../services/api";
import BookCard from "../components/BookCard.vue";

export default {
  components: { BookCard },
  data() {
    return { books: [] };
  },
  methods: {
    async load() {
      const res = await getBooks();
      this.books = res.data;
    },
    async pinjam(id) {
      await borrowBook(id);
      alert("Dipinjam!");
      this.load();
    }
  },
  mounted() {
    this.load();
  }
};
</script>