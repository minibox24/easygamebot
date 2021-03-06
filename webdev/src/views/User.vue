<template>
  <div id="user">
    User Page
  </div>
</template>

<script>
export default {
  mounted () {
    this.$store.commit('setTitle', '유저')
    this.$store.commit('setActivate', this.$route.name)
  }
}
</script>
