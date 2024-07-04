<template>
  <div class="AF__diff-setting">
    <header>
      <span O-B>stress-cpu</span>
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
        <span O-B>load</span>
        <el-input-number
          v-model="load"
          :min="1"
          size="mini"/>
      </div>
    </main>
  </div>
</template>

<script>
export default {
  data() {
    return {
      workers: 1,
      load: 1
    }
  },
  methods: {
    getData() {
      return {
        workers: this.workers,
        load: this.load
      }
    }
  }
}
</script>

<style>

</style>
