<template>
  <div class="AF__diff-setting">
    <header>
      <span O-B>http-delay</span>
    </header>
    <main>
      <div>
        <span O-B>delay</span>
        <el-input
          v-model="delay"
          size="mini"/>
        <span O-R>{{ $t('fault.example') }}:2000ms</span>
      </div>
    </main>
  </div>
</template>

<script>
export default {
  data() {
    return {
      delay: ''
    }
  },
  methods: {
    getData() {
      return {
        delay: this.delay
      }
    }
  }
}
</script>

<style>

</style>
