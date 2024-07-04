<template>
  <div class="AF__diff-setting">
    <header>
      <span O-B>stress-memory</span>
    </header>
    <main>
      <div>
        <span O-B>workers</span>
        <el-input-number
          v-model="workers"
          :min="1"
          size="mini"/>
      </div>
      <div>
        <span O-B>size</span>
        <el-input
          v-model="size"
          size="mini"/>
        <span O-R>{{ $t('fault.example') }}:100%</span>
      </div>
    </main>
  </div>
</template>

<script>
export default {
  data() {
    return {
      workers: 1,
      size: ''
    }
  },
  methods: {
    getData() {
      return {
        workers: this.workers,
        size: this.size
      }
    }
  }
}
</script>

<style>

</style>
