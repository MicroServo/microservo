<template>
  <div class="box">
    <el-dialog
      :append-to-body="appendToBody"
      :visible.sync="dialogVisible_"
      width="30%"
      @close="handleClose">
      <span slot="title">{{ title }}</span>
      <div class="content">
        <slot name="content"/>
      </div>
      <div class="info">
        <slot name="info"/>
      </div>
      <div>
        <slot name="center"/>
      </div>
      <div class="footer">
        <slot name="footer" />
      </div>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'Dialog',
  props:{
    title:{
      type: String,
      default: ''
    },
    dialogVisible:{
      type: Boolean,
      default: false
    },
    appendToBody: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {

    }
  },
  // 计算属性
  computed: {
    dialogVisible_: {
      get() {
        return this.dialogVisible
      },
      // 值一改变就会调用set【可以用set方法去改变父组件的值】
      set(v) {
        //   console.log(v, 'v')
        //   this.$emit('changeDrawer', v)
      }
    }
  },

  methods:{
    // 子组件向父组件传方法，传布尔值；请求父组件关闭抽屉
    handleClose() {
      this.$emit('changeDialog', false)
    }
  }
}
</script>

<style scoped>
.box /deep/ .el-dialog{
  border-radius: 12px;
}
.box /deep/ .el-dialog__header{
  text-align: left;
  font-weight: bold;
  padding: 15px;
}
.box /deep/ .el-dialog__body{
  padding: 10px;
  text-align: left;
}
.content{
  float: left;
}
.info{
  float: left;
  padding: 10px;
}
.footer{
  clear: both;
  display: flex;
  align-items: center;
  justify-content: flex-end;
}
</style>
