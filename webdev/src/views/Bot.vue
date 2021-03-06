<template>
  <div id="bot">
    Bot Page
  </div>
</template>

<script>
export default {
  mounted () {
    this.$store.commit('setTitle', '봇')
    this.$store.commit('setActivate', this.$route.name)
  }
}
</script>
