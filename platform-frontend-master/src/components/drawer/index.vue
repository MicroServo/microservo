<template>
  <div class="drawer">
    <el-drawer
      :visible.sync="drawer_"
      size="30%"
      @close="handleClose">
      <template slot="title">
        <div class="card-title">
          <span>{{ title }}</span>
        </div>
      </template>
      <el-divider/>
      <div class="slot-box">
        <slot/>
      </div>
      <div class="button-box">
        <BlueButton
          @click.native="handleClose">{{ $t('button.confirm') }}</BlueButton>
      </div>
    </el-drawer>
  </div>
</template>

<script>
import BlueButton from '@/components/button/blueButton.vue'
export default {
  name: 'Drawer',
  components:{
    BlueButton
  },
  props: {
    title: {
      type: String,
      default: '标题'
    },
    drawer:{
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
    drawer_: {
      get() {
        return this.drawer
      },
      // 值一改变就会调用set【可以用set方法去改变父组件的值】
      set(v) {
        //   console.log(v, 'v')
        //   this.$emit('changeDrawer', v)
      }
    }
  },
  methods: {
    // 子组件向父组件传方法，传布尔值；请求父组件关闭抽屉
    handleClose() {
      this.$emit('changeDrawer', false)
    }
  }
}
</script>

<style scoped>
.drawer /deep/ .el-drawer__header{
  padding: 10px 0 0 5px;
  margin-bottom: 0;
  color: #222222;
}
.drawer /deep/ .el-divider--horizontal{
  margin: 5px 0;
}
.slot-box{
  height: calc(100% - 70px);
  padding: 5px;
  overflow-y: auto;
  max-height: 100%;
  text-align: left;
}
.button-box{
  position: fixed;
  right: 10px;
  background-color: white;
  margin: 10px 10px 10px 0;
}

</style>
