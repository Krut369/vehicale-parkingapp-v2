<template>
  <div class="container mt-5 text-center">
    <h2 class="text-success">✅ Spot Booked Successfully!</h2>
    <p class="lead mt-3">Your parking spot has been reserved.</p>
    <p>Check your <router-link to="/user/history">reservation history</router-link> for details.</p>
    <router-link to="/user" class="btn btn-primary mt-4">Back to Dashboard</router-link>
  </div>
</template>

<script>
export default {
  name: 'BookingView',
  mounted() {
    // Optional: Clear any temporary booking state here
  }
}
</script>
