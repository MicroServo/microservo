<template>
  <div class="box">
    <div class="top">
      <span class="text1">
        <div v-if="algorithmDetail.container_created" class="dotClass greenDot" />
        <div v-else class="dotClass redDot"/>
        {{ $t('algo.container') }}
      </span>
      <span class="text2">
        <slot/>
      </span>
    </div>
    <div class="bottom">
      <div class="mode">
        <img
          src="../../assets/images/算法管理/编组@2x.png"
          class="modeImg">
        <div class="disposition">
          <span v-if="algorithmDetail.mem_limit">
            <span class="number">{{ algorithmDetail.mem_limit }}</span>
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
          <span v-if="algorithmDetail.cpu_count">
            <span class="number">{{ algorithmDetail.cpu_count }}</span>
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
  name: 'DCard1',
  props:{
    algorithmDetail:{
      type: Object,
      default: null
    }
  },
  data() {
    return {
    }
  },
  methods: {
  }
}
</script>

<style scoped>
.box{
  display: inline-block;
  margin: 5px;
  width: calc((100% - 65px)/2);
  height: 150px;
  background-color: rgb(245, 247, 249);
  border-radius: 12px;
  padding: 10px;
  transition: all 0.3s linear 0s;
  color: rgba(55, 78, 92, 1);
  overflow: auto;
}
.top{
  display: flex;
  justify-content: space-between;
  border-bottom: 1px rgba(220, 222, 230, 1) solid;
  padding: 10px 0;
}
.text1{
  line-height: 25px;
  font-weight:bold;
  display: flex;
  align-items: center;
}
.text2{
  display: flex;
  align-items: center;
}
.text2 img{
  width: 20px;
  height: 20px;
}
.text2 img:hover{
  filter: invert(49%) sepia(55%) saturate(4197%) hue-rotate(179deg) brightness(103%) contrast(103%);
}
.text2 img:first-child{
  /* margin-right: 10px; */
}
.false{
  color:#F05D63;
  transition: all 0.3s linear 0s;
}
.modeImg{
  transition: all 0.3s linear 0s;
}
.bottom{
  display: flex;
  justify-content: space-around;
  margin-top: 30px;
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
  font-size: 13px;
  font-weight: bold;
}
.text4{
  color: rgba(116, 140, 154, 1);
  font-size: 13px;
  transition: all 0.3s linear 0s;
  display: block;
}
.greenDot{
  background-color: #57CF95;
  width:10px;
  height:10px;
  border-radius: 50%;
  margin-right: 5px;
}
.redDot{
  background-color: #F05D63;
  width:10px;
  height:10px;
  border-radius: 50%;
  margin-right: 5px;
}
.dotClass {
  width:10px;
  height:10px;
  border-radius: 50%;
  margin-left: 10px;
}
</style>
