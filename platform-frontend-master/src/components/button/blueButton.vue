<template>
  <span
    :class="{inline:size==='inline'}"
    class="box"
  >
    <el-button
      :class="{wide:size==='wide'}"
      type="primary">
      <slot/>
    </el-button>
  </span>
</template>

<script>
export default {
  name: 'BlueButton',
  props:{
    size: {
      type: String,
      default: 'normal'
    }
  },
  data() {
    return {

    }
  }
}
</script>

<style scoped>
.box{
  margin: 0 5px;
}
.inline{
  display: inline;
}
.box /deep/ .el-button{
  border:none;
  border-radius: 12px;
  padding: 11px 12px;
  /* background: #EDF0F2; */
}
.box /deep/ .el-button--primary{
  background-color: #00A0FF;
  box-shadow: 0px 2px 8px 0px rgba(0,160,255,0.5);
}
.wide{
  width: 70px;
}
</style>
