<template>
  <div class="input-box">
    <span>{{ name }}</span>
    <b-form-input v-if="type === 'int'" type="number" @input="update" class="input" v-model="value"/>
    <b-form-input
      v-else-if="type === 'password'" class="input input-passwd"
      :type="showpw ? 'text' : 'password'" @input="update" v-model="value"
    />
    <b-form-tags
      v-else-if="type === 'stocks'" @input="update" v-model="value" :limit="10"
      limitTagsText="주식 종목은 최대 10개입니다" duplicateTagText="중복되는 이름입니다"
      placeholder="" class="input input-stocks" tag-variant="light" add-button-variant="light" remove-on-delete
    />
    <b-form-checkbox
      v-else-if="type === 'bool'"
      @input="update"
      :value="true"
      :unchecked-value="false"
    >
      멘션
    </b-form-checkbox>
    <div v-else-if="type === 'work_money'" class="work-money-box">
      <b-form-input class="input" type="number" ref="wm1" @input="update" v-model="value.split('-').map(Number)[0]"/>
      <span>-</span>
      <b-form-input class="input" type="number" ref="wm2" @input="update" v-model="value.split('-').map(Number)[1]"/>
    </div>
    <b-form-input v-else @input="update" class="input" v-model="value"/>
  </div>
</template>

<script>
export default {
  name: 'Input',
  props: ['value', 'name', 'type', 'showpw'],
  methods: {
    update (value) {
      if (this.type === 'work_money') {
        this.$emit('input', `${this.$refs.wm1.$el.value}-${this.$refs.wm2.$el.value}`)
        return
      }
      this.$emit('input', value)
    }
  }
}
</script>

<style>
.input-stocks input { color: white!important }
.input-stocks .text-muted { color: orange!important }
</style>

<style scoped>
.input-box {
  margin: 2rem 1rem;
}

.input {
  border-color: gray;
  background: gray;
  color: white;
  max-width: 18.5rem;
  margin-top: .5rem;
}

.work-money-box {
  display: flex;
  align-items: baseline;
}

.work-money-box > input {
  max-width: 8.5rem;
}

.work-money-box > span {
  margin: .6rem;
}
</style>
