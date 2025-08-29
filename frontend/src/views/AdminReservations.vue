<template>
  <div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2>Reserved Parking Slots</h2>
      <div>
        <button @click="loadReservations" class="btn btn-primary me-2">
          <i class="fas fa-sync-alt"></i> Refresh
        </button>
        <router-link to="/admin" class="btn btn-secondary">
          <i class="fas fa-arrow-left"></i> Back to Dashboard
        </router-link>
      </div>
    </div>
    
    <!-- Summary Cards -->
    <div class="row mb-4">
      <div class="col-md-4">
        <div class="card bg-primary text-white">
          <div class="card-body">
            <h5 class="card-title">Active Reservations</h5>
            <h3>{{ activeReservations.length }}</h3>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card bg-success text-white">
          <div class="card-body">
            <h5 class="card-title">Completed Today</h5>
            <h3>{{ completedReservations.length }}</h3>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card bg-info text-white">
          <div class="card-body">
            <h5 class="card-title">Total Revenue</h5>
            <h3>₹{{ totalRevenue }}</h3>
          </div>
        </div>
      </div>
    </div>

    <!-- Reservations Table -->
    <div v-if="loading" class="text-center">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
    
    <div v-else-if="reservations.length === 0" class="alert alert-info">
      No reservations found.
    </div>
    
    <div v-else class="table-responsive">
      <table class="table table-bordered table-hover">
        <thead class="table-light">
          <tr>
            <th>Reservation ID</th>
            <th>Lot</th>
            <th>Spot ID</th>
            <th>User</th>
            <th>Start Time</th>
            <th>End Time</th>
            <th>Duration</th>
            <th>Cost (₹)</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="res in reservations" :key="res.reservation_id">
            <td>{{ res.reservation_id }}</td>
            <td>{{ res.lot_name }}</td>
            <td>{{ res.spot_id }}</td>
            <td>
              <div>{{ res.user_username }}</div>
              <small class="text-muted">{{ res.user_email }}</small>
            </td>
            <td>{{ formatDate(res.start_time) }}</td>
            <td>{{ res.end_time ? formatDate(res.end_time) : 'Ongoing' }}</td>
            <td>{{ res.duration_hours ? res.duration_hours + 'h' : '-' }}</td>
            <td>{{ res.cost || '-' }}</td>
            <td>
              <span 
                :class="res.status === 'Active' ? 'badge bg-warning' : 'badge bg-success'"
              >
                {{ res.status }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import api from '../api/api'

export default {
  name: 'AdminReservations',
  data() {
    return {
      reservations: [],
      loading: false
    }
  },
  computed: {
    activeReservations() {
      return this.reservations.filter(r => r.status === 'Active')
    },
    completedReservations() {
      return this.reservations.filter(r => r.status === 'Completed')
    },
    totalRevenue() {
      const revenue = this.reservations
        .filter(r => r.cost && r.cost > 0)
        .reduce((sum, r) => sum + (r.cost || 0), 0)
      return revenue.toFixed(2)
    }
  },
  async mounted() {
    await this.loadReservations()
  },
  beforeRouteEnter(to, from, next) {
    // Ensure fresh data when entering the route
    next(vm => {
      vm.loadReservations()
    })
  },
  beforeRouteUpdate(to, from, next) {
    // Refresh data when the route updates
    this.loadReservations()
    next()
  },
  methods: {
    async loadReservations() {
      this.loading = true
      try {
        console.log('Loading admin reservations...')
        const response = await api.get('/api/admin/reservations')
        console.log('Reservations response:', response.data)
        this.reservations = response.data
        console.log('Reservations loaded:', this.reservations.length)
      } catch (error) {
        console.error('Error loading reservations:', error)
        console.error('Error details:', error.response?.data || error.message)
      } finally {
        this.loading = false
      }
    },
    formatDate(dateStr) {
      try {
        if (!dateStr) return '-'
        return new Date(dateStr).toLocaleString()
      } catch (error) {
        console.error('Error formatting date:', dateStr, error)
        return dateStr || '-'
      }
    }
  }
}
</script>

<style scoped>
.table-responsive {
  max-height: 600px;
  overflow-y: auto;
}
</style> 