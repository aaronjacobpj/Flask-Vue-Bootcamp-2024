<template>
    <main class="page video-page">
        <button class="back" type="button" @click="$router.back()">← Back to sessions</button>
        <div class="player">
            <div class="ratio ratio-16x9">
                <iframe :src="'https://www.youtube.com/embed/'+video+'?rel=0'" title="YouTube video" allowfullscreen></iframe>
            </div>
        </div>
    </main>
</template>
<script>
    export default{
        props: ["video"]
    }
</script>
<style scoped>
    .video-page {
        max-width: 1100px;
    }

    .back {
        border: 0;
        background: none;
        padding: 6px 0;
        margin-bottom: 16px;
        font-weight: 500;
        color: var(--muted);
        transition: color .15s;
    }

    .back:hover {
        color: var(--vue-dark);
    }

    .player {
        border-radius: var(--radius);
        overflow: hidden;
        background: #000;
        box-shadow: var(--shadow-md);
    }
</style>
