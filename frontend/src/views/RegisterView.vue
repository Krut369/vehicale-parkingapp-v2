<template>
  <div class="container mt-5">
    <h2 class="mb-3">Register</h2>
    <form @submit.prevent="register">
      <input v-model="username" placeholder="Username" class="form-control mb-2" required>
      <input v-model="email" placeholder="Email" class="form-control mb-2" required>
      <input v-model="phone_number" placeholder="Phone Number" class="form-control mb-2" required>
      <input v-model="password" type="password" placeholder="Password" class="form-control mb-3" required>
      <button class="btn btn-success w-100">Register</button>
    </form>
    <p class="mt-3">
      Already registered?
      <router-link to="/">Login</router-link>
    </p>
  </div>
</template>

<script>
import api from '../api/api'

export default {
  data() {
    return {
      username: '',
      email: '',
      phone_number: '',
      password: ''
    }
  },
  methods: {
    async register() {
      try {
        await api.post('/api/auth/register', {
          username: this.username,
          email: this.email,
          phone_number: this.phone_number,
          password: this.password
        })
        alert('Registered successfully! Please log in.')
        this.$router.push('/')
      } catch (err) {
        alert('Registration failed: Username or Email might already exist.')
      }
    }
  }
}
</script>
