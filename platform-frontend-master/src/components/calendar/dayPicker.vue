<template>
  <div class="week-picker">
    <img
      src="../../assets/images/主页/编组 8.png"
      draggable="false"
      @click="lastDay"
    >
    <el-date-picker
      v-model="chooseDay"
      :clearable="false"
      type="date"
      placeholder="选择日期"
      size="mini"
      @change="setDay"
    />
    <img
      src="../../assets/images/主页/编组 8备份.png"
      draggable="false"
      @click="nextDay"
    >
  </div>
</template>

<script>
export default {
  data() {
    return {
      timer: null,
      chooseDay: ''
    }
  },
  methods: {
    lastDay() {
      if (this.timer) clearTimeout(this.timer)
      this.timer = setTimeout(() => {
        this.chooseDay -= 1000 * 60 * 60 * 24
        this.$emit('lastDay')
      }, 300)
    },
    nextDay() {
      if (this.timer) clearTimeout(this.timer)
      this.timer = setTimeout(() => {
        this.chooseDay += 1000 * 60 * 60 * 24
        this.$emit('nextDay')
      }, 300)
    },
    setDay() {
      console.log('ss')
      this.chooseDay = new Date(this.chooseDay).getTime()
      console.log('this.chooseDay', this.chooseDay)
      this.$emit('setDay', this.chooseDay)
    }
  }
}
</script>

<style scoped>
.week-picker {
  display: flex;
  text-align: center;
  margin: 17px;
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
