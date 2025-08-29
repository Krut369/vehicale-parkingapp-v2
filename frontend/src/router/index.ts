// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'

import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import AdminDashboard from '../views/AdminDashboard.vue'
import AdminReservations from '../views/AdminReservations.vue'
import AdminOverview from '../views/AdminOverview.vue'
import UserDashboard from '../views/UserDashboard.vue'
import BookingView from '../views/BookingView.vue'
import HistoryView from '../views/HistoryView.vue'
import ExportCSV from '../views/ExportCSV.vue'
import ManageLots from '../views/ManageLots.vue'
import ViewUsers from '../views/ViewUsers.vue'
import NotFound from '../views/NotFound.vue'

const routes = [
  { path: '/', component: LoginView },
  { path: '/register', component: RegisterView },
  { path: '/admin', component: AdminDashboard, meta: { requiresAuth: true, role: 'admin' } },
  { path: '/admin/lots', component: ManageLots, meta: { requiresAuth: true, role: 'admin' } },
  { path: '/admin/users', component: ViewUsers, meta: { requiresAuth: true, role: 'admin' } },
  { path: '/admin/reservations', component: AdminReservations, meta: { requiresAuth: true, role: 'admin' } },
  { path: '/admin/overview', component: AdminOverview, meta: { requiresAuth: true, role: 'admin' } },
  { path: '/user', component: UserDashboard, meta: { requiresAuth: true, role: 'user' } },
  { path: '/user/book', component: BookingView, meta: { requiresAuth: true, role: 'user' } },
  { path: '/user/history', component: HistoryView, meta: { requiresAuth: true, role: 'user' } },
  { path: '/user/export', component: ExportCSV, meta: { requiresAuth: true, role: 'user' } },
  { path: '/:pathMatch(.*)*', name: 'NotFound', component: NotFound }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const role = localStorage.getItem('role')
  const isAuthenticated = !!role

  if (to.meta.requiresAuth && !isAuthenticated) {
    return next('/')
  }

  if (to.meta.role && role !== to.meta.role) {
    return next('/')
  }

  next()
})

export default router
