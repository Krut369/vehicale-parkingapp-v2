<template>
  <div class="container mt-4">
    <h2 class="mb-4">Admin Dashboard</h2>
    
    <!-- Navigation Cards -->
    <div class="row">
      <div class="col-md-3 mb-3">
        <router-link to="/admin/lots" class="btn btn-primary w-100 h-100 d-flex flex-column justify-content-center align-items-center" style="min-height: 120px;">
          <i class="fas fa-parking mb-2" style="font-size: 2rem;"></i>
          <span>Manage Parking Lots</span>
        </router-link>
      </div>
      <div class="col-md-3 mb-3">
        <router-link to="/admin/users" class="btn btn-secondary w-100 h-100 d-flex flex-column justify-content-center align-items-center" style="min-height: 120px;">
          <i class="fas fa-users mb-2" style="font-size: 2rem;"></i>
          <span>View Registered Users</span>
        </router-link>
      </div>
      <div class="col-md-3 mb-3">
        <router-link to="/admin/reservations" class="btn btn-info w-100 h-100 d-flex flex-column justify-content-center align-items-center" style="min-height: 120px;">
          <i class="fas fa-car mb-2" style="font-size: 2rem;"></i>
          <span>Reserved Parking Slots</span>
        </router-link>
      </div>
      <div class="col-md-3 mb-3">
        <router-link to="/admin/overview" class="btn btn-success w-100 h-100 d-flex flex-column justify-content-center align-items-center" style="min-height: 120px;">
          <i class="fas fa-chart-bar mb-2" style="font-size: 2rem;"></i>
          <span>Overview & Analytics</span>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AdminDashboard'
}
</script>

<style scoped>
.btn {
  transition: all 0.3s ease;
  text-decoration: none;
}

.btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}
</style>
