<template>
  <nav>
    <ol class="breadcrumb small mb-2">
      <li class="breadcrumb-item"><router-link to="/admin">Subjects</router-link></li>
      <li class="breadcrumb-item">
        <router-link :to="'/admin/chapters/' + quiz.chapter_id">{{ quiz.chapter_name }}</router-link>
      </li>
    </ol>
  </nav>
  <div class="d-flex justify-content-between align-items-center mb-3">
    <h3 class="fw-semibold mb-0">{{ quiz.title }} · Questions</h3>
    <button class="btn btn-primary" @click="newQuestion">+ New question</button>
  </div>

  <!-- add / edit form -->
  <div v-if="form" class="card shadow-sm mb-4 border-primary">
    <div class="card-body">
      <form @submit.prevent="save">
        <div class="mb-3">
          <label class="form-label">Question</label>
          <textarea v-model="form.statement" class="form-control" rows="2" required></textarea>
        </div>
        <label class="form-label">Options <span class="text-muted small">(select the correct one)</span></label>
        <!-- i = 1, 2, 3, 4 -->
        <div v-for="i in 4" :key="i" class="input-group mb-2">
          <div class="input-group-text">
            <input v-model="form.correct_option" class="form-check-input mt-0" type="radio" :value="i" />
          </div>
          <input v-model="form.options[i - 1]" class="form-control" :placeholder="'Option ' + i" :required="i <= 2" />
        </div>
        <div class="d-flex gap-2 mt-3">
          <button class="btn btn-success">Save question</button>
          <button type="button" class="btn btn-outline-secondary" @click="form = null">Cancel</button>
        </div>
      </form>
    </div>
  </div>

  <div v-for="(question, index) in questions" :key="question.id" class="card border-0 shadow-sm mb-3">
    <div class="card-body">
      <div class="d-flex justify-content-between">
        <p class="fw-semibold mb-2">Q{{ index + 1 }}. {{ question.statement }}</p>
        <div class="text-nowrap">
          <button class="btn btn-sm btn-link text-decoration-none" @click="editQuestion(question)">Edit</button>
          <button class="btn btn-sm btn-link text-decoration-none text-danger" @click="deleteQuestion(question)">Delete</button>
        </div>
      </div>
      <ol class="mb-0 small">
        <template v-for="(option, i) in question.options" :key="i">
          <li v-if="option" :class="{ 'text-success fw-semibold': i + 1 === question.correct_option }">
            {{ option }} <span v-if="i + 1 === question.correct_option">✓</span>
          </li>
        </template>
      </ol>
    </div>
  </div>
  <p v-if="questions.length === 0" class="text-muted">No questions yet.</p>
</template>

<script>
import api, { errorText } from '../../api'

export default {
  name: 'QuizQuestions',
  data() {
    return {
      quizId: this.$route.params.id, // from the URL /admin/quizzes/:id
      quiz: {},
      questions: [],
      form: null, // the question being added or edited (null = form hidden)
    }
  },
  mounted() {
    this.loadQuestions()
  },
  methods: {
    async loadQuestions() {
      const response = await api.get('/quizzes/' + this.quizId + '/questions')
      this.quiz = response.data.quiz
      this.questions = response.data.questions
    },
    newQuestion() {
      this.form = { statement: '', options: ['', '', '', ''], correct_option: 1 }
    },
    editQuestion(question) {
      this.form = {
        id: question.id,
        statement: question.statement,
        options: question.options.map((option) => option || ''), // null -> ''
        correct_option: question.correct_option,
      }
    },
    async save() {
      try {
        if (this.form.id) {
          await api.put('/questions/' + this.form.id, this.form)
        } else {
          await api.post('/quizzes/' + this.quizId + '/questions', this.form)
        }
        this.form = null
        this.$store.dispatch('showMessage', { type: 'success', text: 'Question saved' })
        this.loadQuestions()
      } catch (error) {
        this.$store.dispatch('showMessage', { type: 'danger', text: errorText(error) })
      }
    },
    async deleteQuestion(question) {
      if (!confirm('Delete this question?')) return
      await api.delete('/questions/' + question.id)
      this.loadQuestions()
    },
  },
}
</script>
