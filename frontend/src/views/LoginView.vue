<template>
  <div class="container mt-5">
    <h2 class="mb-3">Login</h2>
    <form @submit.prevent="login">
      <input v-model="username" placeholder="Username" class="form-control mb-2" required>
      <input v-model="password" type="password" placeholder="Password" class="form-control mb-3" required>
      <button class="btn btn-primary w-100">Login</button>
    </form>
    <p class="mt-3">
      Don't have an account?
      <router-link to="/register">Register</router-link>
    </p>
  </div>
</template>

<script>
import api from '../api/api'

export default {
  data() {
    return {
      username: '',
      password: ''
    }
  },
  methods: {
    async login() {
      try {
        const res = await api.post('/api/auth/login', {
          username: this.username,
          password: this.password
        })
        localStorage.setItem('user_id', res.data.user_id)
        localStorage.setItem('role', res.data.role)
        this.$router.push(res.data.role === 'admin' ? '/admin' : '/user')
      } catch (err) {
        alert('Invalid username or password')
      }
    }
  }
}
</script>
