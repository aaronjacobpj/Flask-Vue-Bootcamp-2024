<script setup>
    import { RouterLink } from "vue-router";
    import store from "@/store";
</script>
<template>
    <nav class="navbar navbar-expand-lg navbar-dark app-nav sticky-top">
        <div class="container-fluid nav-inner">
            <a class="navbar-brand brand" href="/">
                <span class="brand-mark">
                    <span class="dot flask"></span><span class="dot vue"></span>
                </span>
                Flask &amp; Vue Bootcamp
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse justify-content-end" id="navbarNav">
                <span class="term-badge" v-if="year && term">{{ term }} {{ year }}</span>
                <ul class="navbar-nav">
                    <li class="nav-item" v-if="year && term" v-for="course in store.getters.filterCourses(year, term)">
                        <RouterLink class="nav-link" :to="{name: 'course' , params: {name: course['name'], term: term, year:year}}">
                            {{ course["name"] }}
                        </RouterLink>
                    </li>
                </ul>
            </div>
        </div>
    </nav>
</template>
<script>
    export default {
        computed: {
            term(){
                return this.$route.params.term;
            },
            year(){
                return this.$route.params.year;
            }
        }
    }
</script>
<style scoped>
    .app-nav {
        background: rgba(15, 23, 42, .92);
        backdrop-filter: saturate(180%) blur(12px);
        border-bottom: 1px solid rgba(255, 255, 255, .06);
        padding: 12px 0;
    }

    .nav-inner {
        max-width: 1200px;
        padding: 0 20px;
    }

    .brand {
        display: flex;
        align-items: center;
        gap: 10px;
        font-weight: 700;
        letter-spacing: -0.01em;
        color: #fff;
    }

    .brand-mark {
        display: inline-flex;
    }

    .dot {
        width: 14px;
        height: 14px;
        border-radius: 50%;
        display: inline-block;
    }

    .dot.flask {
        background: #94a3b8;
    }

    .dot.vue {
        background: var(--vue);
        margin-left: -5px;
        box-shadow: 0 0 0 2px rgba(15, 23, 42, .92);
    }

    .term-badge {
        color: #94a3b8;
        font-size: .8rem;
        font-weight: 500;
        margin-right: 12px;
        padding: 4px 10px;
        border: 1px solid rgba(148, 163, 184, .3);
        border-radius: 999px;
    }

    .nav-link {
        color: rgba(255, 255, 255, .72);
        font-weight: 500;
        border-radius: 8px;
        padding: 6px 14px !important;
        transition: background .15s, color .15s;
    }

    .nav-link:hover {
        color: #fff;
        background: rgba(255, 255, 255, .08);
    }

    .nav-link.router-link-active {
        color: #fff;
        background: rgba(66, 184, 131, .2);
    }

    @media (max-width: 991px) {
        .term-badge {
            display: inline-block;
            margin: 12px 0 6px;
        }
    }
</style>
