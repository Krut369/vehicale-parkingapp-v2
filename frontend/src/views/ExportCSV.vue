<template>
  <div class="container mt-4">
    <!-- Header Section -->
    <div class="row mb-4">
      <div class="col-12">
        <div class="d-flex justify-content-between align-items-center">
          <div>
            <h2 class="mb-1">
              <i class="fas fa-chart-line me-2 text-primary"></i>
              Parking Analytics & Export
            </h2>
            <p class="text-muted mb-0">View your parking history and export data</p>
          </div>
          <div class="d-flex gap-2">
            <button @click="loadData" class="btn btn-outline-secondary" :disabled="loading">
              <i class="fas fa-sync-alt me-2"></i>
              {{ loading ? 'Loading...' : 'Refresh' }}
            </button>
            <button @click="exportCSV" class="btn btn-primary" :disabled="exporting || !hasData">
              <i class="fas fa-download me-2"></i>
              {{ exporting ? 'Exporting...' : 'Export CSV' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="mt-3 text-muted">Loading your parking data...</p>
    </div>

    <!-- Content when data is loaded -->
    <div v-else>
      <!-- Chart Section -->
      <div class="row mb-4" v-if="completedReservations.length > 0">
        <div class="col-12">
          <div class="card border-0 shadow-sm">
            <div class="card-header bg-white">
              <h5 class="mb-0">
                <i class="fas fa-chart-line me-2 text-success"></i>
                Completed Reservations Over Time
              </h5>
            </div>
            <div class="card-body">
              <canvas id="completedReservationsChart" width="400" height="200"></canvas>
            </div>
          </div>
        </div>
      </div>

      <!-- No Reservations -->
      <div v-if="!hasData" class="text-center py-4">
        <i class="fas fa-inbox text-muted" style="font-size: 3rem;"></i>
        <h5 class="text-muted mt-3">No Bookings Found</h5>
        <p class="text-muted">You haven't made any parking bookings yet.</p>
      </div>
    </div>

    <!-- Alert Messages -->
    <div v-if="exportMessage" class="mt-3">
      <div :class="exportMessageClass" role="alert">
        <i class="fas fa-info-circle me-2"></i>
        {{ exportMessage }}
      </div>
    </div>
  </div>
</template>

<script>
import api from '../api/api'
import { Chart, BarElement, BarController, CategoryScale, LinearScale, Title, Tooltip, Legend, LineElement, LineController, PointElement } from 'chart.js'

// Register Chart.js components
Chart.register(BarElement, BarController, CategoryScale, LinearScale, Title, Tooltip, Legend, LineElement, LineController, PointElement)

export default {
  name: 'ExportCSV',
  data() {
    return {
      loading: false,
      exporting: false,
      exportMessage: '',
      exportMessageClass: '',
      bookingData: [],
      chart: null
    }
  },
  computed: {
    hasData() {
      return this.bookingData.length > 0
    },
    completedReservations() {
      return this.bookingData.filter(booking => booking.status === 'Completed')
    }
  },
  async mounted() {
    await this.loadData()
  },
  methods: {
    async loadData() {
      const user_id = localStorage.getItem('user_id')
      if (!user_id) {
        this.showMessage('Please log in to view data.', 'alert-danger')
        return
      }

      this.loading = true
      this.clearMessage()

      try {
        const response = await api.post('/api/user/export-csv', { user_id })
        this.bookingData = response.data.data || []
        
        // Create chart after data is loaded and DOM is updated
        this.$nextTick(() => {
          this.createChart()
        })
      } catch (err) {
        console.error('Load error:', err)
        this.showMessage('Failed to load booking data.', 'alert-danger')
      } finally {
        this.loading = false
      }
    },

    createChart() {
      console.log('Creating chart...')
      console.log('Completed reservations count:', this.completedReservations.length)
      
      if (this.completedReservations.length === 0) {
        console.log('No completed reservations to chart')
        return
      }

      const ctx = document.getElementById('completedReservationsChart')
      if (!ctx) {
        console.error('Canvas element not found')
        return
      }

      // Destroy existing chart if it exists
      if (this.chart) {
        this.chart.destroy()
      }

      // Process data for chart
      const chartData = this.processChartData()
      console.log('Chart data:', chartData)

      // Only create chart if we have valid data
      if (!chartData || chartData.labels.length === 0 || chartData.values.length === 0) {
        console.log('No valid chart data, skipping chart creation')
        return
      }

      this.chart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: chartData.labels,
          datasets: [{
            label: 'Completed Reservations',
            data: chartData.values,
            borderColor: 'rgb(40, 167, 69)',
            backgroundColor: 'rgba(40, 167, 69, 0.2)',
            tension: 0.1,
            fill: true,
            pointBackgroundColor: 'rgb(40, 167, 69)',
            pointBorderColor: '#fff',
            pointBorderWidth: 2,
            pointRadius: 6
          }]
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              position: 'top',
            },
            title: {
              display: true,
              text: 'Completed Reservations Timeline'
            }
          },
          scales: {
            y: {
              beginAtZero: true,
              ticks: {
                stepSize: 1
              }
            }
          }
        }
      })
      
      console.log('Chart created successfully')
    },

    processChartData() {
      const monthlyData = {}
      
      console.log('Processing chart data for completed reservations:')
      this.completedReservations.forEach((reservation, index) => {
        console.log(`Reservation ${index + 1}:`, reservation)
        
        // Validate that end_time exists and is a valid date
        if (!reservation.end_time) {
          console.log(`Reservation ${index + 1} has no end_time, skipping`)
          return
        }
        
        try {
          const date = new Date(reservation.end_time)
          if (isNaN(date.getTime())) {
            console.log(`Reservation ${index + 1} has invalid end_time: ${reservation.end_time}`)
            return
          }
          
          const monthKey = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`
          monthlyData[monthKey] = (monthlyData[monthKey] || 0) + 1
          console.log(`Month key: ${monthKey}, count: ${monthlyData[monthKey]}`)
        } catch (error) {
          console.error(`Error processing reservation ${index + 1}:`, error)
        }
      })

      const sortedMonths = Object.keys(monthlyData).sort()
      console.log('Sorted months:', sortedMonths)
      
      if (sortedMonths.length === 0) {
        console.log('No valid data for chart')
        return {
          labels: [],
          values: []
        }
      }
      
      const result = {
        labels: sortedMonths.map(month => {
          const [year, monthNum] = month.split('-')
          const date = new Date(parseInt(year), parseInt(monthNum) - 1)
          return date.toLocaleDateString('en-US', { month: 'short', year: 'numeric' })
        }),
        values: sortedMonths.map(month => monthlyData[month])
      }
      
      console.log('Final chart data:', result)
      return result
    },

    async exportCSV() {
      if (!this.hasData) {
        this.showMessage('No data to export.', 'alert-info')
        return
      }

      this.exporting = true
      this.clearMessage()

      try {
        this.createAndDownloadCSV(this.bookingData)
        this.showMessage(`Successfully exported ${this.bookingData.length} bookings!`, 'alert-success')
      } catch (err) {
        console.error('Export error:', err)
        this.showMessage('Error exporting CSV data.', 'alert-danger')
      } finally {
        this.exporting = false
      }
    },

    createAndDownloadCSV(data) {
      // Create CSV content
      const headers = ['Reservation ID', 'Lot Name', 'Spot ID', 'Start Time', 'End Time', 'Cost', 'Status']
      const csvContent = [
        headers.join(','),
        ...data.map(row => [
          row.reservation_id,
          `"${row.lot_name}"`,
          row.spot_id,
          `"${row.start_time}"`,
          `"${row.end_time || ''}"`,
          row.cost || 0,
          row.status
        ].join(','))
      ].join('\n')

      // Create and download file
      const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
      const link = document.createElement('a')
      const url = URL.createObjectURL(blob)
      link.setAttribute('href', url)
      link.setAttribute('download', `parking_history_${new Date().toISOString().split('T')[0]}.csv`)
      link.style.visibility = 'hidden'
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
    },

    showMessage(message, className) {
      this.exportMessage = message
      this.exportMessageClass = `alert ${className}`
    },

    clearMessage() {
      this.exportMessage = ''
      this.exportMessageClass = ''
    }
  }
}
</script>

<style scoped>
.card {
  transition: all 0.3s ease;
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.15) !important;
}

.btn {
  transition: all 0.2s ease;
}

.btn:hover {
  transform: translateY(-1px);
}

.table {
  font-size: 0.9rem;
}

.badge {
  font-size: 0.8rem;
}

.spinner-border {
  width: 3rem;
  height: 3rem;
}
</style>
