<template>
  <div class="login-container">
    <div class="login-box">

      <h2>Welcome Back</h2>
      <p class="subtitle">Login untuk melanjutkan</p>

      <input v-model="form.username" placeholder="Username" />
      <input v-model="form.password" type="password" placeholder="Password" />

      <button @click="submit">Login</button>

      <p class="switch">
        Belum punya akun?
        <router-link to="/register">Register</router-link>
      </p>

    </div>
  </div>
</template>

<script>
import { login } from "../services/api";

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
        const res = await login(this.form);

        console.log("LOGIN RESPONSE:", res.data);

        localStorage.setItem("token", res.data.token);
        localStorage.setItem("role", res.data.role);

        console.log("ROLE SET:", localStorage.getItem("role"));

        if (res.data.role === "admin") {
          this.$router.push("/admin");
        } else {
          this.$router.push("/");
        }

      } catch {
        console.error(err)
        alert("Login gagal");
      }
    }
  }
};
</script>

<style>
.login-container {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #f3f4f6, #e5e7eb);
}

.login-box {
  width: 340px;
  background: white;
  padding: 30px;
  border-radius: 16px;
  box-shadow: 0 15px 40px rgba(0,0,0,0.1);
  text-align: center;
}

.login-box h2 {
  margin-bottom: 5px;
}

.subtitle {
  font-size: 14px;
  color: #6b7280;
  margin-bottom: 20px;
}

.login-box input {
  width: 100%;
  padding: 12px;
  margin-bottom: 12px;
  border-radius: 10px;
  border: 1px solid #e5e7eb;
  outline: none;
  transition: 0.2s;
}

.login-box input:focus {
  border-color: #7f1d1d;
}

.login-box button {
  width: 100%;
  padding: 12px;
  background: #7f1d1d;
  color: white;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: 0.2s;
}

.login-box button:hover {
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
