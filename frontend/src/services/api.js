import axios from "axios"

const API = axios.create({
  baseURL: "http://localhost:5000"
})

API.interceptors.request.use(config => {
  const token = localStorage.getItem("token")

  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }

  return config
})

export const login = data => API.post("/login", data)
export const register = data => API.post("/register", data)

export const getBooks = () => API.get("/books")

export const borrowBook = id => API.post(`/borrow/${id}`)
export const returnBook = id => API.post(`/return/${id}`)

export const addBook = data => API.post("/books", data)
export const updateBook = (id, data) => API.put(`/books/${id}`, data)
export const deleteBook = id => API.delete(`/books/${id}`)
export const getMyBorrowings = () => API.get("/my-borrowings")