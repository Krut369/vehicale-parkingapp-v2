<!-- src/components/LotCard.vue -->
<template>
  <div class="card mb-3">
    <div class="card-body">
      <h5 class="card-title">{{ lot.name }}</h5>
      <p class="card-text">{{ lot.address }} ({{ lot.pin_code }})</p>
      <p class="card-text">₹{{ lot.price_per_hour }}/hr</p>
      <p class="card-text"><strong>Available Spots:</strong> {{ lot.available_spots }}</p>
      <button @click="$emit('book', lot.id)" class="btn btn-success">Book</button>
    </div>
  </div>
</template>

<script>
export default {
  props: ['lot']
}
</script>
