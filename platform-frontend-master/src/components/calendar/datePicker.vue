<template>
  <div class="week-picker">
    <img
      src="../../assets/images/主页/编组 8.png"
      draggable="false"
      @click="lastDate"
    >
    <el-date-picker
      v-model="date"
      :clearable="false"
      type="date"
      placeholder="选择天"
      size="mini"
      @change="setDate"
    />
    <img
      src="../../assets/images/主页/编组 8备份.png"
      draggable="false"
      @click="nextDate"
    >
  </div>
</template>

<script>
export default {
  data() {
    return {
      timer: null,
      date: new Date().setHours(0, 0, 0, 0)
    }
  },
  methods: {
    lastDate() {
      if (this.timer) clearTimeout(this.timer)
      this.timer = setTimeout(() => {
        this.date -= 1000 * 60 * 60 * 24
        this.$emit('lastDate')
      }, 300)
    },
    nextDate() {
      if (this.timer) clearTimeout(this.timer)
      this.timer = setTimeout(() => {
        this.date += 1000 * 60 * 60 * 24
        this.$emit('nextDate')
      }, 300)
    },
    setDate() {
      this.date = new Date(this.date).getTime()
      this.$emit('setDate', this.date)
    },
    initDate(date) {
      this.date = date
      this.$emit('setDate', this.date)
    },
    getTime() {
      return [this.date, this.date + 1000 * 60 * 60 * 24]
    }
  }
}
</script>

<style scoped>
.week-picker {
  display: flex;
  text-align: center;
  margin: 5px;
}
.week-picker > img {
  cursor: pointer;
  user-select: none;
  width: 28px;
  height: 28px;
}
</style>
