<template>
  <div class="d-flex justify-content-between align-items-center mb-3">
    <h3 class="fw-semibold mb-0">Available quizzes</h3>
    <select v-model="selectedSubject" class="form-select w-auto">
      <option value="">All subjects</option>
      <option v-for="name in subjectNames" :key="name" :value="name">{{ name }}</option>
    </select>
  </div>
  <div class="card border-0 shadow-sm table-responsive">
    <table class="table mb-0">
      <thead class="table-light">
        <tr><th>Quiz</th><th>Subject › Chapter</th><th>Date</th><th>Questions</th><th>Duration</th><th></th></tr>
      </thead>
      <tbody>
        <tr v-for="quiz in shownQuizzes" :key="quiz.id">
          <td class="fw-semibold">{{ quiz.title }}</td>
          <td>{{ quiz.subject_name }} › {{ quiz.chapter_name }}</td>
          <td>{{ quiz.date_of_quiz }}</td>
          <td>{{ quiz.question_count }}</td>
          <td>{{ quiz.time_duration }} min</td>
          <td class="text-end">
            <router-link :to="'/quiz/' + quiz.id" class="btn btn-sm btn-primary">Start</router-link>
          </td>
        </tr>
        <tr v-if="shownQuizzes.length === 0"><td colspan="6" class="text-muted">No quizzes available.</td></tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import api from '../../api'

export default {
  name: 'UserDashboard',
  data() {
    return {
      quizzes: [], // all quizzes from the API
      selectedSubject: '', // '' means all subjects
    }
  },
  computed: {
    // subject names for the dropdown, without repeats
    subjectNames() {
      const names = this.quizzes.map((quiz) => quiz.subject_name)
      return [...new Set(names)]
    },
    // the quizzes shown in the table (re-calculated when the dropdown changes)
    shownQuizzes() {
      if (this.selectedSubject === '') return this.quizzes
      return this.quizzes.filter((quiz) => quiz.subject_name === this.selectedSubject)
    },
  },
  async mounted() {
    const response = await api.get('/quizzes')
    this.quizzes = response.data
  },
}
</script>
