<template>
  <div id="setting">
    Setting Page
  </div>
</template>

<script>
export default {
  mounted () {
    this.$store.commit('setTitle', '설정')
    this.$store.commit('setActivate', this.$route.name)
  }
}
</script>
