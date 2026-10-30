<template>
  <button class="btn btn-outline-primary btn-sm" :disabled="busy" @click="exportCsv">
    {{ busy ? 'Preparing CSV…' : 'Export as CSV' }}
  </button>
</template>

<script>
// The CSV is made by a Celery job in the background:
//   1. start the job      2. ask "is it done?" every second      3. download the file
import api, { errorText } from '../api'

function wait(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms))
}

export default {
  name: 'ExportButton',
  data() {
    return { busy: false }
  },
  methods: {
    async exportCsv() {
      this.busy = true
      try {
        // 1. start the job
        const start = await api.post('/export')
        const taskId = start.data.task_id

        // 2. check every second (at most 30 times) until the job has finished
        let state = 'PENDING'
        for (let i = 0; i < 30; i++) {
          await wait(1000)
          const check = await api.get('/export/' + taskId)
          state = check.data.state
          if (state === 'SUCCESS' || state === 'FAILURE') break
        }
        if (state !== 'SUCCESS') throw new Error('Export failed. Is the Celery worker running?')

        // 3. download the file (through axios, so the token is sent)
        const file = await api.get('/export/' + taskId + '/file', { responseType: 'blob' })
        const link = document.createElement('a')
        link.href = URL.createObjectURL(file.data)
        link.download = 'quiz_master_export.csv'
        link.click()
        // Easier version but sacrifices security
        // open(import.meta.env.VITE_API_URL+'/export/' + taskId + '/file')

        this.$store.dispatch('showMessage', { type: 'success', text: 'Export ready - download started' })
      } catch (error) {
        this.$store.dispatch('showMessage', { type: 'danger', text: errorText(error) })
      }
      this.busy = false
    },
  },
}
</script>
