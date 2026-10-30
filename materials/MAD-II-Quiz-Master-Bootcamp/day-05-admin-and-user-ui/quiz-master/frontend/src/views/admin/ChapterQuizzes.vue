<template>
  <nav>
    <ol class="breadcrumb small mb-2">
      <li class="breadcrumb-item"><router-link to="/admin">Subjects</router-link></li>
      <li class="breadcrumb-item active">{{ chapter.subject_name }}</li>
    </ol>
  </nav>
  <div class="d-flex justify-content-between align-items-center mb-3">
    <h3 class="fw-semibold mb-0">{{ chapter.name }} · Quizzes</h3>
    <button class="btn btn-primary" @click="newQuiz">+ New quiz</button>
  </div>

  <!-- add / edit form -->
  <div v-if="form" class="card shadow-sm mb-4 border-primary">
    <div class="card-body">
      {{ form }}
      <h6 class="mb-3">{{ form.id ? 'Edit quiz' : 'New quiz' }}</h6>
      <form class="row g-2" @submit.prevent="save">
        <div class="col-md-4"><input v-model="form.title" class="form-control" placeholder="Title" required /></div>
        <div class="col-md-2"><input v-model="form.date_of_quiz" type="date" class="form-control" /></div>
        <div class="col-md-2">
          <div class="input-group">
            <input v-model.number="form.time_duration" type="number" min="1" class="form-control" required />
            <span class="input-group-text">min</span>
          </div>
        </div>
        <div class="col-md-2"><input v-model="form.remarks" class="form-control" placeholder="Remarks" /></div>
        <div class="col-md-2 d-flex gap-2">
          <button class="btn btn-success flex-fill">Save</button>
          <button type="button" class="btn btn-outline-secondary" @click="form = null">✕</button>
        </div>
      </form>
    </div>
  </div>

  <div class="card border-0 shadow-sm table-responsive">
    <table class="table mb-0">
      <thead class="table-light">
        <tr><th>Title</th><th>Date</th><th>Duration</th><th>Questions</th><th class="text-end">Actions</th></tr>
      </thead>
      <tbody>
        <tr v-for="quiz in quizzes" :key="quiz.id">
          <td>{{ quiz.title }} <div class="small text-muted">{{ quiz.remarks }}</div></td>
          <td>{{ quiz.date_of_quiz }}</td>
          <td>{{ quiz.time_duration }} min</td>
          <td><span class="badge" :class="quiz.question_count ? 'bg-success' : 'bg-secondary'">{{ quiz.question_count }}</span></td>
          <td class="text-end">
            <router-link :to="'/admin/quizzes/' + quiz.id" class="btn btn-sm btn-link text-decoration-none">Questions</router-link>
            <button class="btn btn-sm btn-link text-decoration-none" @click="editQuiz(quiz)">Edit</button>
            <button class="btn btn-sm btn-link text-decoration-none text-danger" @click="deleteQuiz(quiz)">Delete</button>
          </td>
        </tr>
        <tr v-if="quizzes.length === 0"><td colspan="5" class="text-muted">No quizzes in this chapter yet.</td></tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import api, { errorText } from '../../api'

export default {
  name: 'ChapterQuizzes',
  data() {
    return {
      chapterId: this.$route.params.id, // from the URL /admin/chapters/:id
      chapter: {},
      quizzes: [],
      form: null, // the quiz being added or edited (null = form hidden)
    }
  },
  mounted() {
    this.loadQuizzes()
  },
  methods: {
    async loadQuizzes() {
      const response = await api.get('/chapters/' + this.chapterId + '/quizzes')
      this.chapter = response.data.chapter
      this.quizzes = response.data.quizzes
    },
    newQuiz() {
      const today = new Date().toISOString().slice(0, 10) // "2026-10-25"
      this.form = { title: '', date_of_quiz: today, time_duration: 10, remarks: '' }
    },
    editQuiz(quiz) {
      this.form = { ...quiz } // a copy, so the table does not change while typing

    },
    async save() {
      try {
        if (this.form.id) {
          await api.put('/quizzes/' + this.form.id, this.form)
        } else {
          await api.post('/chapters/' + this.chapterId + '/quizzes', this.form)
        }
        this.form = null
        this.$store.dispatch('showMessage', { type: 'success', text: 'Quiz saved' })
        this.loadQuizzes()
      } catch (error) {
        this.$store.dispatch('showMessage', { type: 'danger', text: errorText(error) })
      }
    },
    async deleteQuiz(quiz) {
      if (!confirm('Delete quiz "' + quiz.title + '"? All scores for it will be removed.')) return
      await api.delete('/quizzes/' + quiz.id)
      this.loadQuizzes()
    },
  },
}
</script>
