<template>
  <div class="container mt-4">
    <h3 class="mb-3">Registered Users</h3>

    <!-- Add User Form -->
    <div class="mb-4">
      <h5>Add New User</h5>
      <form @submit.prevent="addUser">
        <div class="row mb-2">
          <div class="col">
            <input v-model="newUser.username" class="form-control" placeholder="Username" required />
          </div>
          <div class="col">
            <input v-model="newUser.email" class="form-control" placeholder="Email" required />
          </div>
          <div class="col">
            <input v-model="newUser.password" class="form-control" type="password" placeholder="Password" required />
          </div>
          <div class="col">
            <button class="btn btn-primary" type="submit">Add User</button>
          </div>
        </div>
      </form>
    </div>

    <!-- Users Table -->
    <table class="table table-striped">
      <thead class="table-light">
        <tr>
          <th>ID</th>
          <th>Username</th>
          <th>Email</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in users" :key="user.id">
          <td>{{ user.id }}</td>
          <td v-if="editUserId !== user.id">{{ user.username }}</td>
          <td v-else>
            <input v-model="editUser.username" class="form-control" />
          </td>

          <td v-if="editUserId !== user.id">{{ user.email }}</td>
          <td v-else>
            <input v-model="editUser.email" class="form-control" />
          </td>

          <td>
            <button v-if="editUserId !== user.id" class="btn btn-sm btn-warning me-2" @click="startEdit(user)">
              Edit
            </button>
            <button v-if="editUserId === user.id" class="btn btn-sm btn-success me-2" @click="saveEdit(user.id)">
              Save
            </button>
            <button v-if="editUserId === user.id" class="btn btn-sm btn-secondary me-2" @click="cancelEdit">
              Cancel
            </button>
            <button class="btn btn-sm btn-danger" @click="deleteUser(user.id)">
              Delete
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import api from '../api/api'

export default {
  data() {
    return {
      users: [],
      editUserId: null,
      editUser: { username: '', email: '' },
      newUser: { username: '', email: '', password: '' },
    }
  },
  async mounted() {
    this.fetchUsers()
  },
  methods: {
    async fetchUsers() {
      const res = await api.get('/api/admin/users')
      this.users = res.data
    },
    startEdit(user) {
      this.editUserId = user.id
      this.editUser = { username: user.username, email: user.email }
    },
    cancelEdit() {
      this.editUserId = null
      this.editUser = { username: '', email: '' }
    },
    async saveEdit(userId) {
      await api.put(`/api/admin/users/${userId}`, this.editUser)
      this.fetchUsers()
      this.cancelEdit()
    },
    async deleteUser(userId) {
      if (confirm('Are you sure you want to delete this user?')) {
        await api.delete(`/api/admin/users/${userId}`)
        this.fetchUsers()
      }
    },
    async addUser() {
      await api.post('/api/admin/users', this.newUser)
      this.newUser = { username: '', email: '', password: '' }
      this.fetchUsers()
    }
  }
}
</script>
