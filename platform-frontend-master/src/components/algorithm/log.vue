<template>
  <div>
    <div class="log-box">
      <p class="title">
        {{ $t('algo.log') }}
        <el-form
          class="flex-box"
          label-position="left"
          label-width="auto">
          <el-form-item :label="$t('algo.lineCounts')">
            <el-input-number
              v-model="line_num"
              :min="1"
              size="small"/>
          </el-form-item>
          <WhiteButton @click.native="getContainerLog">{{ $t('button.obtain') }}</WhiteButton>
        </el-form>
      </p>
      <div class="log-content">
        {{ containerLog }}
      </div>
    </div>
  </div>
</template>

<script>
import WhiteButton from '@/components/button/whiteButton.vue'
export default {
  name: 'Log',
  components: {
    WhiteButton
  },
  props:{
    containerLog:{
      type: String,
      default: ''
    },
    id: {
      type: Number,
      default: null
    }
  },
  data() {
    return {
      line_num: 20
    }
  },
  methods: {
    getContainerLog() {
      const url =  `/api/container/getContainerLog?line_num=${this.line_num}&id=${this.id}`
      this.$http({
        method: 'get',
        url: url
      }).then((res) => {
        const resData = res.data
        if (resData.code === 0) {
          this.containerLog = resData.data
          this.$message.success(resData.message)
        } else {
          this.$message.error(resData.message)
        }
      })
    }
  }
}
</script>

<style scoped>
.log-box{
  border: 1px solid #DCDEE6;
  height: calc(100vh - 300px);
  border-radius: 3px;
}
.title{
  background-color: #F5F7F9;
  margin: 0;
  font-size: 15px;
  font-weight: bold;
  color: #333333;
  padding: 10px 0 10px 10px;
  border-radius: 3px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.log-content{
  padding: 10px;
  color: #374E5C;
  font-size: 14px;
  margin: 0;
  height: calc(100vh - 378px);
  overflow-y: auto;
}
.flex-box{
  display: flex;
  align-items: center;
}
.flex-box /deep/ .el-form-item{
  margin-bottom: 0;
}
</style>
