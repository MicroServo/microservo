<template>
  <div class="box">
    <el-button :class="{wide:size==='wide'}">
      <slot/>
    </el-button>
  </div>

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
  display: inline;
  margin: 0 5px;
}
.box /deep/ .el-button{
  border:none;
  border-radius: 12px;
  padding: 10px 12px;
  color: #374E5C;
  border: 1px solid #A5B7C1;
  /* background: #EDF0F2; */
}
.wide{
  width: 70px;
}
</style>
