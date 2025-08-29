<template>
  <div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2 class="mb-0">Your Reservation History</h2>
      <div class="d-flex gap-2">
        <button @click="loadHistory" class="btn btn-outline-primary">
          <i class="fas fa-sync-alt"></i> Refresh
        </button>
        <router-link to="/user" class="btn btn-outline-secondary">
          <i class="fas fa-arrow-left"></i> Back to Dashboard
        </router-link>
      </div>
    </div>

    <!-- Summary Cards -->
    <div class="row mb-4">
      <div class="col-md-4">
        <div class="card bg-primary text-white">
          <div class="card-body text-center">
            <h5 class="card-title">Active Reservations</h5>
            <h3>{{ activeReservations.length }}</h3>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card bg-success text-white">
          <div class="card-body text-center">
            <h5 class="card-title">Completed Reservations</h5>
            <h3>{{ completedReservations.length }}</h3>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card bg-info text-white">
          <div class="card-body text-center">
            <h5 class="card-title">Total Spent</h5>
            <h3>₹{{ totalSpent }}</h3>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="mt-3 text-muted">Loading your reservation history...</p>
    </div>

    <!-- Content when data is loaded -->
    <div v-else>
      <!-- No Reservations -->
      <div v-if="history.length === 0" class="alert alert-info">
        <i class="fas fa-info-circle me-2"></i>
        No reservations yet. Start by booking your first parking spot!
      </div>

      <!-- Reservations Table -->
      <div v-else class="table-responsive">
        <table class="table table-hover">
          <thead class="table-light">
            <tr>
              <th>Lot</th>
              <th>Spot ID</th>
              <th>Start Time</th>
              <th>End Time</th>
              <th>Duration</th>
              <th>Cost (₹)</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="res in history" :key="res.spot_id + res.start_time">
              <td>
                <strong>{{ res.lot_name }}</strong>
              </td>
              <td>
                <span class="badge bg-secondary">{{ res.spot_id }}</span>
              </td>
              <td>{{ formatDate(res.start_time) }}</td>
              <td>{{ res.end_time ? formatDate(res.end_time) : 'Ongoing' }}</td>
              <td>
                <span v-if="res.duration_hours" class="text-muted">
                  {{ res.duration_hours }}h
                </span>
                <span v-else class="text-muted">-</span>
              </td>
              <td>
                <span class="fw-bold text-success">{{ res.cost || '-' }}</span>
              </td>
              <td>
                <span 
                  :class="res.end_time ? 'badge bg-success' : 'badge bg-warning'"
                >
                  <i :class="res.end_time ? 'fas fa-check' : 'fas fa-clock'" class="me-1"></i>
                  {{ res.end_time ? 'Completed' : 'Active' }}
                </span>
              </td>
              <td>
                <button 
                  v-if="!res.end_time" 
                  @click="releaseSpot(res)"
                  class="btn btn-danger btn-sm"
                  :disabled="releasing"
                >
                  <i class="fas fa-stop me-1"></i>
                  {{ releasing ? 'Releasing...' : 'Release' }}
                </button>
                <span v-else class="text-muted">
                  <i class="fas fa-check-circle text-success"></i>
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Success/Error Messages -->
    <div v-if="message" class="alert mt-3" :class="messageType">
      <i :class="messageIcon" class="me-2"></i>
      {{ message }}
    </div>
  </div>
</template>

<script>
import api from '../api/api'

export default {
  name: 'HistoryView',
  data() {
    return {
      history: [],
      loading: false,
      releasing: false,
      message: '',
      messageType: 'alert-info',
      messageIcon: 'fas fa-info-circle'
    }
  },
  computed: {
    activeReservations() {
      return this.history.filter(r => !r.end_time)
    },
    completedReservations() {
      return this.history.filter(r => r.end_time)
    },
    totalSpent() {
      const total = this.history
        .filter(r => r.cost && r.cost > 0)
        .reduce((sum, r) => sum + (r.cost || 0), 0)
      return total.toFixed(2)
    }
  },
  async mounted() {
    await this.loadHistory()
  },
  methods: {
    async loadHistory() {
      this.loading = true
      this.clearMessage()
      
      try {
        const user_id = localStorage.getItem('user_id')
        const response = await api.get(`/api/user/history/${user_id}`)
        this.history = response.data
        
        // Add duration calculation for each reservation
        this.history.forEach(res => {
          if (res.end_time) {
            const start = new Date(res.start_time)
            const end = new Date(res.end_time)
            const durationMs = end - start
            res.duration_hours = (durationMs / (1000 * 60 * 60)).toFixed(1)
          }
        })
        
        console.log('History loaded:', this.history.length, 'reservations')
      } catch (error) {
        console.error('Error loading history:', error)
        this.showMessage('Failed to load reservation history', 'alert-danger', 'fas fa-exclamation-triangle')
      } finally {
        this.loading = false
      }
    },
    
    async releaseSpot(reservation) {
      this.releasing = true
      this.clearMessage()
      
      try {
        const user_id = localStorage.getItem('user_id')
        const response = await api.post('/api/user/release', { user_id })
        
        const cost = response.data.cost
        this.showMessage(
          `Spot released successfully! Cost: ₹${cost}`, 
          'alert-success', 
          'fas fa-check-circle'
        )
        
        // Reload history to show updated data
        await this.loadHistory()
        
      } catch (error) {
        console.error('Error releasing spot:', error)
        this.showMessage(
          'Failed to release spot. Please try again.', 
          'alert-danger', 
          'fas fa-exclamation-triangle'
        )
      } finally {
        this.releasing = false
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
    },
    
    showMessage(text, type = 'alert-info', icon = 'fas fa-info-circle') {
      this.message = text
      this.messageType = type
      this.messageIcon = icon
      
      // Auto-hide success messages after 5 seconds
      if (type === 'alert-success') {
        setTimeout(() => {
          this.clearMessage()
        }, 5000)
      }
    },
    
    clearMessage() {
      this.message = ''
    }
  }
}
</script>

<style scoped>
.table-responsive {
  max-height: 600px;
  overflow-y: auto;
}

.badge {
  font-size: 0.8rem;
}

.btn {
  transition: all 0.2s ease;
}

.btn:hover {
  transform: translateY(-1px);
}

.card {
  transition: all 0.3s ease;
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.alert {
  animation: fadeIn 0.3s ease-in;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
