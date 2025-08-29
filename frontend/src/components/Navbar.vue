<!-- src/components/Navbar.vue -->
<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container-fluid">
      <a class="navbar-brand" href="#">Parking App</a>
      <div class="collapse navbar-collapse">
        <ul class="navbar-nav me-auto">
          <li v-if="role === 'admin'" class="nav-item">
            <router-link class="nav-link" to="/admin">Dashboard</router-link>
          </li>
          <li v-if="role === 'admin'" class="nav-item">
            <router-link class="nav-link" to="/admin/lots">Manage Lots</router-link>
          </li>
          <li v-if="role === 'admin'" class="nav-item">
            <router-link class="nav-link" to="/admin/users">Users</router-link>
          </li>
          <li v-if="role === 'user'" class="nav-item">
            <router-link class="nav-link" to="/user">Dashboard</router-link>
          </li>
          <li v-if="role === 'user'" class="nav-item">
            <router-link class="nav-link" to="/user/history">History</router-link>
          </li>
          <li v-if="role === 'user'" class="nav-item">
            <router-link class="nav-link" to="/user/export">Export CSV</router-link>
          </li>
        </ul>
        <button v-if="role" class="btn btn-outline-light" @click="logout">Logout</button>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  computed: {
    role() {
      return localStorage.getItem('role')
    }
  },
  methods: {
    logout() {
      localStorage.clear()
      this.$router.push('/')
    }
  }
}
</script>
