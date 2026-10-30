<template>
  <h3 class="fw-semibold mb-3">Search results for “{{ $route.query.q }}”</h3>

  <div class="row g-4">
    <div class="col-md-4">
      <div class="card border-0 shadow-sm">
        <div class="card-header bg-white fw-semibold">Users ({{ users.length }})</div>
        <ul class="list-group list-group-flush">
          <li v-for="user in users" :key="user.id" class="list-group-item">
            {{ user.full_name }} <div class="small text-muted">{{ user.email }}</div>
          </li>
        </ul>
      </div>
    </div>
    <div class="col-md-4">
      <div class="card border-0 shadow-sm">
        <div class="card-header bg-white fw-semibold">Subjects ({{ subjects.length }})</div>
        <ul class="list-group list-group-flush">
          <li v-for="subject in subjects" :key="subject.id" class="list-group-item">
            <router-link to="/admin">{{ subject.name }}</router-link>
            <div class="small text-muted">{{ subject.chapter_count }} chapters</div>
          </li>
        </ul>
      </div>
    </div>
    <div class="col-md-4">
      <div class="card border-0 shadow-sm">
        <div class="card-header bg-white fw-semibold">Quizzes ({{ quizzes.length }})</div>
        <ul class="list-group list-group-flush">
          <li v-for="quiz in quizzes" :key="quiz.id" class="list-group-item">
            <router-link :to="'/admin/quizzes/' + quiz.id">{{ quiz.title }}</router-link>
            <div class="small text-muted">{{ quiz.subject_name }} › {{ quiz.chapter_name }}</div>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../../api'

export default {
  name: 'SearchView',
  data() {
    return { users: [], subjects: [], quizzes: [] }
  },
  mounted() {
    this.search()
  },
  watch: {
    // searching again from the navbar only changes ?q= in the URL, so run the search again
    '$route.query.q'() {
      this.search()
    },
  },
  methods: {
    async search() {
      const response = await api.get('/admin/search', { params: { q: this.$route.query.q } })
      this.users = response.data.users
      this.subjects = response.data.subjects
      this.quizzes = response.data.quizzes
    },
  },
}
</script>
