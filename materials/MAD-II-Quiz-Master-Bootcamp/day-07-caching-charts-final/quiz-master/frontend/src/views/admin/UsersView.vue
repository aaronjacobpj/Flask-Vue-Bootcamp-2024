<template>
  <div class="d-flex flex-wrap gap-2 justify-content-between align-items-center mb-3">
    <h3 class="fw-semibold mb-0">Users</h3>
    <div class="d-flex flex-wrap gap-2">
      <button class="btn btn-sm btn-outline-secondary" @click="runJob('reminders')">Send reminders now</button>
      <button class="btn btn-sm btn-outline-secondary" @click="runJob('monthly-report')">Send monthly report now</button>
      <ExportButton />
    </div>
  </div>

  <div class="card border-0 shadow-sm table-responsive">
    <table class="table mb-0">
      <thead class="table-light">
        <tr><th>Name</th><th>Email</th><th>Qualification</th><th>Status</th><th class="text-end">Action</th></tr>
      </thead>
      <tbody>
        <tr v-for="user in users" :key="user.id">
          <td>{{ user.full_name }}</td>
          <td>{{ user.email }}</td>
          <td>{{ user.qualification || '—' }}</td>
          <td>
            <span v-if="user.active" class="badge bg-success">Active</span>
            <span v-else class="badge bg-danger">Blocked</span>
          </td>
          <td class="text-end">
            <button v-if="user.active" class="btn btn-sm btn-outline-danger" @click="toggle(user)">Block</button>
            <button v-else class="btn btn-sm btn-outline-success" @click="toggle(user)">Unblock</button>
          </td>
        </tr>
        <tr v-if="users.length === 0"><td colspan="5" class="text-muted">No users registered yet.</td></tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import api, { errorText } from '../../api'
import ExportButton from '../../components/ExportButton.vue'

export default {
  name: 'UsersView',
  components: { ExportButton },
  data() {
    return { users: [] }
  },
  mounted() {
    this.loadUsers()
  },
  methods: {
    async loadUsers() {
      const response = await api.get('/admin/users')
      this.users = response.data
    },
    async toggle(user) {
      await api.patch('/admin/users/' + user.id + '/toggle') // block <-> unblock
      this.loadUsers()
    },
    // Run a scheduled Celery job right now (useful for the demo)
    async runJob(name) {
      try {
        const response = await api.post('/admin/jobs/' + name)
        this.$store.dispatch('showMessage', { type: 'success', text: response.data.message })
      } catch (error) {
        this.$store.dispatch('showMessage', { type: 'danger', text: errorText(error) })
      }
    },
  },
}
</script>
