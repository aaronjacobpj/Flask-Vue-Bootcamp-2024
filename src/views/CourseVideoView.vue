<template>
    <main style="width: 100%; display: flex; justify-content: center;">
        <div style="width: 80%; display: flex; justify-content: center;">
            <div class="ratio ratio-16x9">
                <iframe :src="'https://www.youtube.com/embed/'+video+'?rel=0'" title="YouTube video" allowfullscreen></iframe>
            </div>
        </div>
    </main> 
</template>
<script>
    export default{
        props: ["video"],
        data()
        {

        },
        computed:{
        }
    }
</script>