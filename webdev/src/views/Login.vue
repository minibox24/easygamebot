<template>
  <div class="login">
    <span class="title mb-3">비밀번호를 입력해주세요.</span>
    <b-form-input
      class="pw" type="password"
      v-model="password" placeholder="비밀번호"
    />
  </div>
</template>

<script>
export default {
  mounted () {
    this.$store.commit('setTitle', '로그인')
    this.$router.push(this.$route.params.path ?? '/')
  },
  data () {
    return {
      password: localStorage.getItem('password')
    }
  },
  watch: {
    password (pw) {
      localStorage.setItem('password', pw)
      if (pw === '1234') {
        this.$router.push(this.$route.params.path ?? '/')
      }
    }
  }
}
</script>

<style scoped>
.login {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  flex-direction: column;
}

.title {
  font-weight: 900;
  font-size: 2.5rem;
}

.pw {
  width: 50%;
}
</style>
