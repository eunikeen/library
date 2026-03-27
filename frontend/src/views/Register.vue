<template>
  <div class="register-container">
    <div class="register-box">

      <h2>Create Account</h2>
      <p class="subtitle">Daftar untuk mulai menggunakan</p>

      <input v-model="form.username" placeholder="Username" />
      <input v-model="form.password" type="password" placeholder="Password" />

      <button @click="submit">Register</button>

      <p class="switch">
        Sudah punya akun?
        <router-link to="/login">Login</router-link>
      </p>

    </div>
  </div>
</template>

<script>
import { register } from "../services/api";

export default {
  data() {
    return {
      form: {
        username: "",
        password: ""
      }
    };
  },
  methods: {
    async submit() {
      try {
        await register(this.form);
        alert("Berhasil register!");
        this.$router.push("/login");
      } catch (err) {
        alert("Register gagal!");
      }
    }
  }
};
</script>

<style>
.register-container {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #f3f4f6, #e5e7eb);
}

.register-box {
  width: 340px;
  background: white;
  padding: 30px;
  border-radius: 16px;
  box-shadow: 0 15px 40px rgba(0,0,0,0.1);
  text-align: center;
}

.register-box h2 {
  margin-bottom: 5px;
}

.subtitle {
  font-size: 14px;
  color: #6b7280;
  margin-bottom: 20px;
}

.register-box input {
  width: 100%;
  padding: 12px;
  margin-bottom: 12px;
  border-radius: 10px;
  border: 1px solid #e5e7eb;
  outline: none;
}

.register-box input:focus {
  border-color: #7f1d1d;
}

.register-box button {
  width: 100%;
  padding: 12px;
  background: #7f1d1d;
  color: white;
  border: none;
  border-radius: 10px;
  cursor: pointer;
}

.auth-box button:hover {
  background: #5f0f0f;
}

.switch {
  margin-top: 15px;
  font-size: 13px;
}

.switch a {
  color: #7f1d1d;
  font-weight: bold;
  text-decoration: none;
}
</style>