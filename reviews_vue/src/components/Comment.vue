<template>
        <article class="media">
            <figure class="media-left">
                <p class="image is-64x64">
                <img src="http://localhost:8000/media/placeholder.jpg" />
                </p>
            </figure>
            <div class="media-content">
                <div class="content">
                <p>
                    <strong>{{ author }}</strong> <small>{{ created_at }}</small>
                    <br />
                    {{ text }}
                    <br />
                </p>
                </div>
            </div>
        </article>

</template>

<script>
export default {
  props: ['author', 'text', 'created_at'],
}
</script>