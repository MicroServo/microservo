<template>
  <div class="download-progress-container">
    <el-progress
      :text-inside="true"
      :stroke-width="20"
      :percentage="percentage"
      :status="status"
      class="download-progress"/>
    <span class="download-progress-step">{{ msg }}</span>
  </div>
</template>

<script>
export default {
  data() {
    return {
      msg: '',
      percentage: 0,
      status: ''
    }
  },
  methods: {
    setPMS(p, m, s) {
      this.msg = m
      this.percentage = p
      this.status = s
    },
    setPercentage(percentage) {
      this.percentage = percentage
    },
    setMsg(msg) {
      this.msg = msg
    },
    setStatus(status) {
      this.status = status
    },
    resetting() {
      this.msg = ''
      this.percentage = 0
      this.status = ''
    }
  }
}
</script>

<style scoped>
.download-progress-container {
  display: inline-block;
  margin: 2px;
}
.download-progress {
  width: 150px;
}
.download-progress-step {
  display: inline-block;
  width: 100%;
  text-align: center;
  font-size: 12px;
}
</style>
