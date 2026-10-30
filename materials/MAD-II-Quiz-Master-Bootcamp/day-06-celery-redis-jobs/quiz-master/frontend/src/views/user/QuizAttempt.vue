<template>
  <!-- After submitting: show the result -->
  <div v-if="result" class="card border-0 shadow-sm col-12 col-md-6 col-lg-4 mx-auto mt-5 text-center">
    <div class="card-body p-4">
      <h4>Quiz submitted</h4>
      <p class="display-6 my-3">{{ result.total_scored }} / {{ result.total_questions }}</p>
      <p class="text-muted">{{ result.percentage }}%</p>
      <router-link to="/scores" class="btn btn-primary me-2">My scores</router-link>
      <router-link to="/dashboard" class="btn btn-outline-secondary">Back to quizzes</router-link>
    </div>
  </div>

  <!-- Before submitting: show the questions -->
  <div v-else>
    <div class="d-flex justify-content-between align-items-center mb-3">
      <div>
        <h3 class="fw-semibold mb-0">{{ quiz.title }}</h3>
        <small class="text-muted">{{ quiz.subject_name }} › {{ quiz.chapter_name }}</small>
      </div>
      <span class="badge fs-6" :class="secondsLeft < 60 ? 'bg-danger' : 'bg-dark'">⏱ {{ timeLeft }}</span>
    </div>

    <form @submit.prevent="submit">
      <div v-for="(question, index) in questions" :key="question.id" class="card border-0 shadow-sm mb-3">
        <div class="card-body">
          <p class="fw-semibold">Q{{ index + 1 }}. {{ question.statement }}</p>
          <template v-for="(option, i) in question.options" :key="i">
            <div v-if="option" class="form-check">
              <!-- answers[question.id] = 1, 2, 3 or 4 -->
              <label class="form-check-label">
                <input v-model="answers[question.id]" class="form-check-input" type="radio" :value="i + 1" />
                {{ option }}
              </label>
            </div>
          </template>
        </div>
      </div>
      {{ answers }}
      <!-- Object.keys(answers).length = how many questions have an answer -->
      <button class="btn btn-success">Submit ({{ Object.keys(answers).length }}/{{ questions.length }} answered)</button>
    </form>
  </div>
</template>

<script>
import api, { errorText } from '../../api'

export default {
  name: 'QuizAttempt',
  data() {
    return {
      quizId: this.$route.params.id, // from the URL /quiz/:id
      quiz: {},
      questions: [], // questions WITHOUT the correct answers
      answers: {}, // { questionId: chosen option number }
      secondsLeft: 0,
      result: null, // filled after submitting
    }
  },
  computed: {
    // 125 seconds -> "2:05"
    timeLeft() {
      const minutes = Math.floor(this.secondsLeft / 60)
      const seconds = this.secondsLeft % 60
      return minutes + ':' + String(seconds).padStart(2, '0')
    },
  },
  async mounted() {
    try {
      const response = await api.get('/quizzes/' + this.quizId + '/attempt')
      this.quiz = response.data.quiz
      this.questions = response.data.questions
      this.secondsLeft = this.quiz.time_duration * 60
      this.startTimer()
    } catch (error) {
      this.$store.dispatch('showMessage', { type: 'danger', text: errorText(error) })
      this.$router.push('/dashboard')
    }
  },
  unmounted() {
    clearInterval(this.timer) // stop the timer when leaving the page
  },
  methods: {
    startTimer() {
      // runs every 1000 ms (1 second)
      this.timer = setInterval(() => {
        this.secondsLeft = this.secondsLeft - 1
        if (this.secondsLeft === 0) this.submit() // time is up -> submit automatically
      }, 1000)
    },
    async submit() {
      clearInterval(this.timer)
      try {
        const response = await api.post('/quizzes/' + this.quizId + '/submit', { answers: this.answers })
        this.result = response.data // { total_scored, total_questions, percentage }
      } catch (error) {
        this.$store.dispatch('showMessage', { type: 'danger', text: errorText(error) })
      }
    },
  },
}
</script>
