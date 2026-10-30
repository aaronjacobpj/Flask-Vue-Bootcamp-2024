<template>
  <div class="d-flex justify-content-between align-items-center mb-3">
    <h3 class="fw-semibold mb-0">Subjects</h3>
    <button class="btn btn-primary" @click="newSubject">+ New subject</button>
  </div>

  <!-- One small form, used to add or edit a subject or a chapter -->
  <div v-if="form" class="card shadow-sm mb-4 border-primary">
    <div class="card-body">
      <h6 class="mb-3">{{ form.id ? 'Edit' : 'New' }} {{ form.type }}</h6>
      <form class="row g-2" @submit.prevent="save">
        <div class="col-md-4"><input v-model="form.name" class="form-control" placeholder="Name" required /></div>
        <div class="col-md-6"><input v-model="form.description" class="form-control" placeholder="Description" /></div>
        <div class="col-md-2 d-flex gap-2">
          <button class="btn btn-success flex-fill">Save</button>
          <button type="button" class="btn btn-outline-secondary" @click="form = null">✕</button>
        </div>
      </form>
    </div>
  </div>

  <p v-if="subjects.length === 0" class="text-muted">No subjects yet. Create the first one.</p>

  <div class="row g-4">
    <div v-for="subject in subjects" :key="subject.id" class="col-lg-6">
      <div class="card border-0 shadow-sm h-100">
        <div class="card-header bg-white d-flex justify-content-between align-items-start">
          <div>
            <h5 class="mb-0">{{ subject.name }}</h5>
            <small class="text-muted">{{ subject.description }}</small>
          </div>
          <div class="btn-group btn-group-sm">
            <button class="btn btn-outline-primary" @click="editSubject(subject)">Edit</button>
            <button class="btn btn-outline-danger" @click="deleteSubject(subject)">Delete</button>
          </div>
        </div>

        <div class="card-body p-0">
          <table class="table table-sm mb-0">
            <thead class="table-light">
              <tr><th class="ps-3">Chapter</th><th>Quizzes</th><th class="text-end pe-3">Actions</th></tr>
            </thead>
            <tbody>
              <tr v-for="chapter in subject.chapters" :key="chapter.id">
                <td class="ps-3">{{ chapter.name }}</td>
                <td>{{ chapter.quiz_count }}</td>
                <td class="text-end pe-3">
                  <router-link :to="'/admin/chapters/' + chapter.id" class="btn btn-sm btn-link text-decoration-none">Quizzes</router-link>
                  <button class="btn btn-sm btn-link text-decoration-none" @click="editChapter(chapter)">Edit</button>
                  <button class="btn btn-sm btn-link text-decoration-none text-danger" @click="deleteChapter(chapter)">Delete</button>
                </td>
              </tr>
              <tr v-if="subject.chapters.length === 0"><td colspan="3" class="ps-3 text-muted small">No chapters</td></tr>
            </tbody>
          </table>
        </div>

        <div class="card-footer bg-white">
          <button class="btn btn-sm btn-outline-primary" @click="newChapter(subject)">+ Chapter</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api, { errorText } from '../../api'

export default {
  name: 'AdminDashboard',
  data() {
    return {
      subjects: [], // each subject comes with its list of chapters
      form: null, // the subject/chapter being added or edited (null = form hidden)
    }
  },
  mounted() {
    this.loadSubjects()
  },
  methods: {
    async loadSubjects() {
      const response = await api.get('/subjects')
      this.subjects = response.data
    },

    // ---- open the form ----
    newSubject() {
      this.form = { type: 'subject', name: '', description: '' }
    },
    editSubject(subject) {
      this.form = { type: 'subject', id: subject.id, name: subject.name, description: subject.description }
    },
    newChapter(subject) {
      this.form = { type: 'chapter', subject_id: subject.id, name: '', description: '' }
    },
    editChapter(chapter) {
      this.form = { type: 'chapter', id: chapter.id, name: chapter.name, description: chapter.description }
    },

    // ---- save: POST to create, PUT to update ----
    async save() {
      try {
        if (this.form.type === 'subject' && this.form.id) {
          await api.put('/subjects/' + this.form.id, this.form)
        } else if (this.form.type === 'subject') {
          await api.post('/subjects', this.form)
        } else if (this.form.id) {
          await api.put('/chapters/' + this.form.id, this.form)
        } else {
          await api.post('/subjects/' + this.form.subject_id + '/chapters', this.form)
        }
        this.form = null
        this.$store.dispatch('showMessage', { type: 'success', text: 'Saved' })
        this.loadSubjects()
      } catch (error) {
        this.$store.dispatch('showMessage', { type: 'danger', text: errorText(error) })
      }
    },

    // ---- delete ----
    async deleteSubject(subject) {
      if (!confirm('Delete "' + subject.name + '" with all its chapters and quizzes?')) return
      await api.delete('/subjects/' + subject.id)
      this.loadSubjects()
    },
    async deleteChapter(chapter) {
      if (!confirm('Delete chapter "' + chapter.name + '"?')) return
      await api.delete('/chapters/' + chapter.id)
      this.loadSubjects()
    },
  },
}
</script>
