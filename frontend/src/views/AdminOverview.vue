<template>
  <div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2>Overview & Analytics</h2>
      <router-link to="/admin" class="btn btn-secondary">
        <i class="fas fa-arrow-left"></i> Back to Dashboard
      </router-link>
    </div>
    
    <summary-chart />
  </div>
</template>

<script>
import SummaryChart from '../components/SummaryChart.vue'

export default {
  name: 'AdminOverview',
  components: { SummaryChart }
}
</script> 