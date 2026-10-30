<template>
  <h3 class="fw-semibold mb-3">Summary</h3>

  <!-- 4 number cards: users, subjects, quizzes, attempts -->
  <div class="row g-3 mb-4">
    <div v-for="name in ['users', 'subjects', 'quizzes', 'attempts']" :key="name" class="col-6 col-md-3">
      <div class="card border-0 shadow-sm text-center">
        <div class="card-body">
          <div class="fs-3 fw-semibold text-primary">{{ totals[name] }}</div>
          <div class="text-muted text-capitalize small">{{ name }}</div>
        </div>
      </div>
    </div>
  </div>

  <div class="row g-4">
    <div class="col-lg-6">
      <div class="card border-0 shadow-sm">
        <div class="card-body">
          <h6>Top score per subject (%)</h6>
          <BarChart :labels="subjectNames" :values="bestScores" :max="100" />
        </div>
      </div>
    </div>
    <div class="col-lg-6">
      <div class="card border-0 shadow-sm">
        <div class="card-body">
          <h6>Quiz attempts per subject</h6>
          <BarChart :labels="subjectNames" :values="attempts" />
        </div>
      </div>
    </div>
  </div>
  <p v-if="bySubject.length === 0" class="text-muted mt-3">No quiz attempts yet - charts will fill in once users take quizzes.</p>
</template>

<script>
import api from '../../api'
import BarChart from '../../components/BarChart.vue'

export default {
  name: 'AdminSummary',
  components: { BarChart },
  data() {
    return {
      totals: {}, // { users: 3, subjects: 2, quizzes: 4, attempts: 5 }
      bySubject: [], // [{ subject: 'Python', attempts: 3, best: 100, average: 80 }, ...]
    }
  },
  computed: {
    subjectNames() {
      return this.bySubject.map((row) => row.subject)
    },
    bestScores() {
      return this.bySubject.map((row) => row.best)
    },
    attempts() {
      return this.bySubject.map((row) => row.attempts)
    },
  },
  async mounted() {
    const response = await api.get('/admin/summary')
    this.totals = response.data.totals
    this.bySubject = response.data.by_subject
  },
}
</script>
