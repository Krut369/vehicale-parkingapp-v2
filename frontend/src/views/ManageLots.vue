<template>
  <div class="container mt-4">
    <h3 class="mb-4">Manage Parking Lots</h3>

    <form @submit.prevent="createLot" class="row g-3 mb-5">
      <div class="col-md-6">
        <input v-model="lot.name" placeholder="Lot Name" class="form-control" required />
      </div>
      <div class="col-md-6">
        <input v-model="lot.address" placeholder="Address" class="form-control" required />
      </div>
      <div class="col-md-4">
        <input v-model="lot.pin_code" placeholder="Pin Code" class="form-control" required />
      </div>
      <div class="col-md-4">
        <input v-model.number="lot.price_per_hour" type="number" min="1" class="form-control" placeholder="Price/hr" required />
      </div>
      <div class="col-md-4">
        <input v-model.number="lot.total_spots" type="number" min="1" class="form-control" placeholder="No. of Spots" required />
      </div>
      <div class="col-12">
        <button class="btn btn-success w-100">Create Parking Lot</button>
      </div>
    </form>

    <h4>Existing Lots</h4>
    <ul class="list-group">
      <li v-for="l in lots" :key="l.id" class="list-group-item d-flex justify-content-between align-items-center">
        <div>
          <strong>{{ l.name }}</strong> — ₹{{ l.price_per_hour }}/hr — Spots: {{ l.total_spots }}
        </div>
        <button class="btn btn-danger btn-sm" @click="deleteLot(l.id)">Delete</button>
      </li>
    </ul>
  </div>
</template>

<script>
import api from '../api/api'

export default {
  data() {
    return {
      lot: {
        name: '',
        address: '',
        pin_code: '',
        price_per_hour: 0,
        total_spots: 0
      },
      lots: []
    }
  },
  async mounted() {
    this.fetchLots()
  },
  methods: {
    async fetchLots() {
      const res = await api.get('/api/admin/lots')
      this.lots = res.data
    },
    async createLot() {
      await api.post('/api/admin/create-lot', this.lot)
      alert('Parking lot created')
      this.lot = { name: '', address: '', pin_code: '', price_per_hour: 0, total_spots: 0 }
      this.fetchLots()
    },
    async deleteLot(id) {
      try {
        await api.delete(`/api/admin/delete-lot/${id}`)
        this.fetchLots()
      } catch {
        alert('Cannot delete — some spots may be occupied.')
      }
    }
  }
}
</script>
