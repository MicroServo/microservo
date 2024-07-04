<template>
  <div class="week-picker">
    <img
      src="../../assets/images/主页/编组 8.png"
      draggable="false"
      @click="lastWeek"
    >
    <el-date-picker
      v-model="weekMonday"
      :clearable="false"
      type="week"
      format="yyyy - WW"
      placeholder="选择周"
      size="mini"
      @change="setWeek"
    />
    <img
      src="../../assets/images/主页/编组 8备份.png"
      draggable="false"
      @click="nextWeek"
    >
  </div>
</template>

<script>
export default {
  data() {
    return {
      timer: null,
      weekMonday: new Date().setDate(new Date().getDate() - new Date().getDay() + 1)
    }
  },
  methods: {
    lastWeek() {
      if (this.timer) clearTimeout(this.timer)
      this.timer = setTimeout(() => {
        this.weekMonday -= 1000 * 60 * 60 * 24 * 7
        this.$emit('lastWeek')
      }, 300)
    },
    nextWeek() {
      if (this.timer) clearTimeout(this.timer)
      this.timer = setTimeout(() => {
        this.weekMonday += 1000 * 60 * 60 * 24 * 7
        this.$emit('nextWeek')
      }, 300)
    },
    setWeek() {
      this.weekMonday = new Date(this.weekMonday).getTime()
      this.$emit('setWeek', this.weekMonday)
    },
    initWeek(weekMonday) {
      this.weekMonday = weekMonday
      this.$emit('setWeek', this.weekMonday)
    },
    getTime() {
      return [this.weekMonday - 1000 * 60 * 60 * 24 * 1, this.weekMonday + 1000 * 60 * 60 * 24 * 6]
    }
  }
}
</script>

<style scoped>
.week-picker {
  display: flex;
  text-align: center;
  margin: 5px;
  /* width: 261px;
height: 40px; */
background: #F5F7F9;
border-radius: 12px;

}

.week-picker >>> .el-input__inner{
    background-color:#F5F7F9 ;
    border:0;
    width:180px
}
.week-picker >>> .el-date-editor.el-input{
    width:180px
}
.week-picker > img {
  cursor: pointer;
  user-select: none;
  width: 28px;
  height: 28px;
}
</style>
