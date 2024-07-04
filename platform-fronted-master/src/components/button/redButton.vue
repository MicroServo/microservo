<template>
  <span
    :class="{inline:size==='inline'}"
    class="box"
  >
    <el-button
      :class="{wide:size==='wide'}"
      type="danger">
      <slot/>
    </el-button>
  </span>
</template>

<script>
export default {
  name: 'RedButton',
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
.box /deep/ .el-button--danger{
  background-color: #F05D63;
  box-shadow: 0px 2px 8px 0px rgba(240, 93, 99, 0.50);
}
.wide{
  width: 70px;
}
</style>
