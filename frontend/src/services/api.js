import axios from "axios";

const API = "http://localhost:5000";

const getHeaders = () => ({
  headers: {
    Authorization: localStorage.getItem("token")
  }
});

// AUTH
export const login = (data) => axios.post(`${API}/login`, data);
export const register = (data) => axios.post(`${API}/register`, data);

// BOOK
export const getBooks = () => axios.get(`${API}/books`, getHeaders());
export const addBook = (data) => axios.post(`${API}/books`, data, getHeaders());
export const updateBook = (id, data) => axios.put(`${API}/books/${id}`, data, getHeaders());
export const deleteBook = (id) => axios.delete(`${API}/books/${id}`, getHeaders());

// 🔥 BORROW (INI YANG KAMU KURANG)
export const borrowBook = (id) =>
  axios.post(`${API}/borrow/${id}`, {}, getHeaders());

export const returnBook = (id) =>
  axios.post(`${API}/return/${id}`, {}, getHeaders());

export const getBorrowings = () =>
  axios.get(`${API}/borrowings`, getHeaders());

