<template>
  <h3 class="fw-semibold mb-3">My summary</h3>

  <p v-if="bySubject.length === 0" class="text-muted">Attempt a quiz to see your summary.</p>

  <div v-else class="row g-4">
    <div class="col-lg-6">
      <div class="card border-0 shadow-sm">
        <div class="card-body">
          <h6>Average score per subject (%)</h6>
          <BarChart :labels="subjectNames" :values="averages" :max="100" />
        </div>
      </div>
    </div>
    <div class="col-lg-6">
      <div class="card border-0 shadow-sm">
        <div class="card-body">
          <h6>Quizzes attempted per subject</h6>
          <BarChart :labels="subjectNames" :values="attempts" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../../api'
import BarChart from '../../components/BarChart.vue'

export default {
  name: 'UserSummary',
  components: { BarChart },
  data() {
    return {
      bySubject: [], // [{ subject: 'Python', attempts: 2, average: 75, best: 100 }, ...]
    }
  },
  computed: {
    subjectNames() {
      return this.bySubject.map((row) => row.subject)
    },
    averages() {
      return this.bySubject.map((row) => row.average)
    },
    attempts() {
      return this.bySubject.map((row) => row.attempts)
    },
  },
  async mounted() {
    const response = await api.get('/summary')
    this.bySubject = response.data.by_subject
  },
}
</script>
