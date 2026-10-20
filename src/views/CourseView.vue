<script setup>
    import { RouterLink } from "vue-router";
    import store from "@/store"
</script>
<template>
    <main class="page" v-if="courses">
        <header class="page-header">
            <span class="eyebrow">{{ term }} {{ year }}</span>
            <h1>{{ courses["name"] }}</h1>
            <p>{{ courses["sessions"].length }} sessions · videos, notes and source code</p>
        </header>

        <div class="accordion sessions" id="accordionCourse">
            <div class="accordion-item session" v-for="each, index in courses['sessions']">
                <h2 class="accordion-header">
                    <button :class="['accordion-button', (index) ? 'collapsed' : '']" type="button" data-bs-toggle="collapse"
                        :data-bs-target="'#collapse'+index" :aria-expanded="!index" :aria-controls="'collapse'+index">
                        <span class="day-num">{{ String(index).padStart(2, '0') }}</span>
                        <span class="session-name">{{ each["name"] }}</span>
                    </button>
                </h2>
                <div :id="'collapse'+index" :class="['accordion-collapse', 'collapse', (!index) ? 'show' : '']"
                    data-bs-parent="#accordionCourse">
                    <div class="accordion-body">
                        <div class="actions">
                            <RouterLink v-if="each['youtube-video-id']" class="action action-primary"
                                :to="{name: 'course-video', params:{video: each['youtube-video-id']}}">
                                ▶ Watch video
                            </RouterLink>
                            <span v-else class="action disabled">▶ Video coming soon</span>

                            <a v-if="each['slides']" class="action" :href="each['slides']" target="_blank">Slides</a>
                            <span v-else class="action disabled">Slides</span>

                            <a v-if="each['notes']" class="action" :href="each['notes']" target="_blank">Notes</a>
                            <span v-else class="action disabled">Notes</span>

                            <a v-if="each['source-code']" class="action" :href="courses['base-url']+each['source-code']">
                                ⬇ Source code
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </main>
</template>
<script>
    export default{
        props: ["year", "term", "name"],
        computed:{
            courses(){
                var items = store.getters.filterCourses(this.year, this.term);

                items = items.filter(each => each["name"] == this.name);
                return items[0];
            }
        }
    }
</script>
<style scoped>
    .sessions {
        display: flex;
        flex-direction: column;
        gap: 12px;
        --bs-accordion-border-width: 0;
        --bs-accordion-btn-focus-box-shadow: 0 0 0 3px rgba(66, 184, 131, .25);
        --bs-accordion-active-bg: #fff;
        --bs-accordion-active-color: var(--ink);
    }

    .session {
        border: 1px solid var(--line) !important;
        border-radius: var(--radius) !important;
        overflow: hidden;
        box-shadow: var(--shadow-sm);
        transition: box-shadow .15s, border-color .15s;
    }

    .session:hover {
        border-color: #cbd5e1 !important;
        box-shadow: var(--shadow-md);
    }

    .accordion-button {
        gap: 16px;
        padding: 18px 20px;
        font-weight: 600;
        color: var(--ink);
        border-radius: 0 !important;
    }

    .accordion-button:not(.collapsed) {
        box-shadow: inset 0 -1px 0 var(--line);
    }

    .day-num {
        flex-shrink: 0;
        display: inline-grid;
        place-items: center;
        width: 40px;
        height: 40px;
        border-radius: 10px;
        font-size: .85rem;
        font-weight: 700;
        color: var(--vue-dark);
        background: var(--accent-soft);
        font-family: 'JetBrains Mono', monospace;
    }

    .accordion-button:not(.collapsed) .day-num {
        color: #fff;
        background: var(--vue);
    }

    .session-name {
        line-height: 1.35;
    }

    .accordion-body {
        padding: 18px 20px 20px 76px;
    }

    .actions {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
    }

    .action {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 8px 16px;
        font-size: .9rem;
        font-weight: 500;
        border-radius: 999px;
        border: 1px solid var(--line);
        color: var(--ink-soft);
        background: #fff;
        text-decoration: none;
        transition: background .15s, border-color .15s, color .15s;
    }

    a.action:hover {
        border-color: var(--vue);
        color: var(--vue-dark);
        background: var(--accent-soft);
    }

    .action-primary {
        background: var(--vue);
        border-color: var(--vue);
        color: #fff;
    }

    a.action-primary:hover {
        background: var(--vue-dark);
        border-color: var(--vue-dark);
        color: #fff;
    }

    .action.disabled {
        color: #94a3b8;
        background: #f8fafc;
        border-style: dashed;
        cursor: not-allowed;
    }

    @media (max-width: 600px) {
        .accordion-body {
            padding-left: 20px;
        }
    }
</style>
