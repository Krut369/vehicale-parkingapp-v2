<!-- src/components/SummaryChart.vue -->
<template>
  <div class="mt-5">
    <h4 class="mb-3">Parking Lot Spot Status Summary</h4>
    <canvas id="lot-summary"></canvas>
  </div>
</template>

<script>
import { onMounted } from 'vue'
import { Chart, BarElement, BarController, CategoryScale, LinearScale, Title, Tooltip, Legend } from 'chart.js'
import api from '../api/api'

Chart.register(BarController, BarElement, CategoryScale, LinearScale, Title, Tooltip, Legend)

export default {
  setup() {
    onMounted(async () => {
      const res = await api.get('/api/admin/spot-status')
      const data = res.data

      const labels = data.map(d => d.lot_name)
      const available = data.map(d => d.available)
      const occupied = data.map(d => d.occupied)

      const ctx = document.getElementById('lot-summary').getContext('2d')
      new Chart(ctx, {
        type: 'bar',
        data: {
          labels,
          datasets: [
            {
              label: 'Available',
              data: available,
              backgroundColor: 'rgba(40, 167, 69, 0.7)' // green
            },
            {
              label: 'Occupied',
              data: occupied,
              backgroundColor: 'rgba(220, 53, 69, 0.7)' // red
            }
          ]
        },
        options: {
          responsive: true,
          plugins: {
            legend: { position: 'top' },
            title: { display: true, text: 'Available vs Occupied Spots by Lot' }
          }
        }
      })
    })
  }
}
</script>
