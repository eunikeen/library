import { createRouter, createWebHistory } from "vue-router";

import Home from "../views/Home.vue";
import Admin from "../views/Admin.vue";
import Login from "../views/Login.vue";

import UserLayout from "../layouts/UserLayout.vue";
import AdminLayout from "../layouts/AdminLayout.vue";

const routes = [
  {
    path: "/",
    component: UserLayout,
    children: [{ path: "", component: Home }]
  },
  {
    path: "/admin",
    component: AdminLayout,
    children: [{ path: "", component: Admin }]
  },
  {
    path: "/login",
    component: Login
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

// 🔐 GUARD
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("token");
  const role = localStorage.getItem("role");

  if (!token && to.path !== "/login") return next("/login");

  if (to.path.startsWith("/admin") && role !== "admin") {
    return next("/");
  }

  next();
});

export default router;