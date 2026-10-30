<template>
  <h3 class="fw-semibold mb-3">Users</h3>

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
import api from '../../api'

export default {
  name: 'UsersView',
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
  },
}
</script>
