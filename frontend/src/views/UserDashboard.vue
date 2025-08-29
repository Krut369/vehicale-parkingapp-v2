<template>
  <div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2 class="mb-0">User Dashboard</h2>
      <div class="d-flex gap-2">
        <button @click="loadData" class="btn btn-outline-primary">
          <i class="fas fa-sync-alt"></i> Refresh
        </button>
         </div>
    </div>

    <!-- Available Parking Lots -->
    <div class="row">
      <div class="col-12">
        <div class="d-flex justify-content-between align-items-center mb-4">
          <h3 class="mb-0">Available Parking Lots</h3>
          <span class="badge bg-primary fs-6">{{ lots.length }} lots available</span>
        </div>
        
        <div v-if="loading" class="text-center py-5">
          <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
          <p class="mt-3 text-muted">Loading available parking lots...</p>
        </div>
        
        <div v-else-if="lots.length === 0" class="alert alert-info">
          <i class="fas fa-info-circle me-2"></i>
          No parking lots available at the moment. Please check back later.
        </div>
        
        <div v-else class="row">
          <div v-for="lot in lots" :key="lot.id" class="col-md-6 col-lg-4 mb-4">
            <div class="card h-100 border-0 shadow-sm hover-shadow">
              <div class="card-body">
                <div class="d-flex justify-content-between align-items-start mb-3">
                  <h5 class="card-title mb-0">{{ lot.name }}</h5>
                  <span class="badge bg-success">{{ lot.available_spots }} spots</span>
                </div>
                <p class="card-text text-muted mb-3">
                  <i class="fas fa-map-marker-alt me-2"></i>
                  {{ lot.address }}
                </p>
                <div class="d-flex justify-content-between align-items-center mb-3">
                  <span class="text-primary fw-bold">₹{{ lot.price_per_hour }}/hour</span>
                  <small class="text-muted">Available spots: {{ lot.available_spots }}</small>
                </div>
                <button 
                  @click="bookSpot(lot.id)" 
                  class="btn btn-primary w-100"
                  :disabled="booking"
                >
                  <i class="fas fa-parking me-2"></i>
                  {{ booking ? 'Booking...' : 'Book Spot' }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../api/api'

export default {
  name: 'UserDashboard',
  data() {
    return { 
      lots: [],
      loading: false,
      booking: false
    }
  },
  async mounted() {
    await this.loadData()
  },
  methods: {
    async loadData() {
      this.loading = true
      try {
        // Load available lots
        const lotsRes = await api.get('/api/user/available-lots')
        this.lots = lotsRes.data
      } catch (error) {
        console.error('Error loading data:', error)
      } finally {
        this.loading = false
      }
    },
    async bookSpot(lot_id) {
      this.booking = true
      const user_id = localStorage.getItem('user_id')
      try {
        await api.post('/api/user/book', { lot_id, user_id })
        this.showSuccess('Spot booked successfully!')
        await this.loadData()
      } catch (err) {
        this.showError('Booking failed: No spots available or error occurred.')
      } finally {
        this.booking = false
      }
    },
    logout() {
      localStorage.clear()
      this.$router.push('/')
    },
    showSuccess(message) {
      alert(message)
    },
    showError(message) {
      alert('Error: ' + message)
    }
  }
}
</script>

<style scoped>
.hover-shadow:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.15) !important;
  transition: all 0.3s ease;
}

.card {
  transition: all 0.3s ease;
}

.btn {
  transition: all 0.2s ease;
}

.btn:hover {
  transform: translateY(-1px);
}

.badge {
  font-size: 0.8rem;
}
</style>
