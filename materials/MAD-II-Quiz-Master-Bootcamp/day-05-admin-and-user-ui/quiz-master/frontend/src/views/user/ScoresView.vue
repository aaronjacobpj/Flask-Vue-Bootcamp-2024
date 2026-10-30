<template>
  <h3 class="fw-semibold mb-3">My scores</h3>

  <div class="card border-0 shadow-sm table-responsive">
    <table class="table mb-0">
      <thead class="table-light">
        <tr><th>Quiz</th><th>Subject</th><th>Attempted</th><th>Score</th><th>%</th></tr>
      </thead>
      <tbody>
        <tr v-for="score in scores" :key="score.id">
          <td>{{ score.quiz_title }}</td>
          <td>{{ score.subject_name }}</td>
          <td>{{ score.attempted_at.replace('T', ' ') }}</td>
          <td>{{ score.total_scored }} / {{ score.total_questions }}</td>
          <td>
            <span class="badge" :class="score.percentage >= 50 ? 'bg-success' : 'bg-warning text-dark'">{{ score.percentage }}%</span>
          </td>
        </tr>
        <tr v-if="scores.length === 0"><td colspan="5" class="text-muted">You have not attempted any quiz yet.</td></tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import api from '../../api'

export default {
  name: 'ScoresView',
  data() {
    return { scores: [] }
  },
  async mounted() {
    const response = await api.get('/scores')
    this.scores = response.data
  },
}
</script>
