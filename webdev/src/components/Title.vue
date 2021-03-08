<script>
export default {
  name: 'Title'
}
</script>

<style scoped>
#title {
  display: flex;
  width: 100%;
  height: 3.5rem;
  background: #344A5F;
  color: white;
  align-items: center;
}

#title > span {
  padding-left: 1rem;
  font-size: 2rem;
  user-select: none;
}
</style>

<template>
  <div id="title">
    <span>{{ this.$store.state.title }}</span>
  </div>
</template>
