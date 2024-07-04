<template>
  <div class="box" @click="handleAlgorithmDetail">
    <div class="top">
      <span class="text1">{{ name }}</span>
      <span class="flex-box">
        <span v-if="status===true" class="text2">{{ $t('algo.deployed') }}</span>
        <span v-else class="text2 false">{{ $t('algo.undeployed') }}</span>
        <i
          title="删除"
          class="el-icon-delete"
          @click.stop="deleteAlgorithm"
        />
      </span>
    </div>
    <div class="bottom">
      <div class="mode">
        <img src="../../assets/images/算法管理/编组@2x.png" class="modeImg">
        <div class="disposition">
          <span v-if="storage">
            <span class="number">{{ storage }}</span>
            <span class="text3">G</span><br>
          </span>
          <span v-else>
            -
          </span>
          <span class="text4">
            {{ $t('algo.mem') }}
          </span>
        </div>
      </div>
      <div class="mode">
        <img src="../../assets/images/算法管理/编组@2x(1).png" class="modeImg">
        <div class="disposition">
          <span v-if="cpu">
            <span class="number">{{ cpu }}</span>
          </span>
          <span v-else>
            -
          </span>
          <span class="text4">
            CPU
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Card',
  props:{
    name: {
      type: String,
      default: '算法'
    },
    storage:{
      type: String,
      default: null
    },
    cpu:{
      type: String,
      default: null
    },
    status:{
      type: Boolean,
      default: true
    }
  },
  data() {
    return {

    }
  },
  methods: {
    deleteAlgorithm() {
      this.$emit('openDeleteAlgorithm')
    },
    handleAlgorithmDetail() {
      this.$emit('openAlgorithmDetail')
    }
  }
}
</script>

<style scoped>
.box{
  display: inline-block;
  margin: 5px;
  width: calc((100% - 100px)/3);
  height: 200px;
  background-color: rgb(245, 247, 249);
  border-radius: 12px;
  padding: 10px;
  transition: all 0.3s linear 0s;
  color: rgba(55, 78, 92, 1);
}
.top{
  display: flex;
  justify-content: space-between;
  border-bottom: 1px rgba(220, 222, 230, 1) solid;
  padding: 10px 0;
}
.text1{
  font-weight:bold;
}
.text2{
  display: flex;
  align-items: center;
  margin-right: 10px;
}
.false{
  color:#F05D63;
  transition: all 0.3s linear 0s;
}
.box:hover .false{
  color: white;
}
.modeImg{
  transition: all 0.3s linear 0s;
}
.box:hover .modeImg{
  filter: invert(100%) sepia(99%) saturate(0%) hue-rotate(23deg) brightness(113%) contrast(101%);
}
.box:hover{
  background-color: #00A0FF;
  box-shadow: 0px 2px 8px 0px rgba(0,160,255,0.5);
  color: white;
}
.bottom{
  display: flex;
  justify-content: space-around;
  margin-top: 60px;
  align-items: center;
}
.number{
  font-size: 25px;
  font-weight: bold;
}
.disposition{
  display: inline;
  margin-left: 10px;
}
.mode{
  display: flex;
  align-items: center;
}
.text3{
  font-size: 14px;
  font-weight: bold;
}
.text4{
  color: rgba(116, 140, 154, 1);
  font-size: 14px;
  transition: all 0.3s linear 0s;
  display: block;
}
.box:hover .text4{
  color: white;
}
.greenDot{
  background-color: #57CF95;
  width:10px;
  height:10px;
  border-radius: 50%;
}
.redDot{
  background-color: #F05D63;
  width:10px;
  height:10px;
  border-radius: 50%;
}
.dotClass {
  width:10px;
  height:10px;
  border-radius: 50%;
  margin-left: 10px;
}
.flex-box{
  display: flex;
  align-items: center;
}
</style>
