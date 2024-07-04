<template>
  <div class="box">
    <div class="top">
      <span class="text1">
        {{ $t('container.train') }}
      </span>
      <span class="text2">
        <slot />
      </span>
    </div>
    <div class="bottom">
      <p>
        {{ $t('container.train_time') }}：
        <span class="text3">{{ time }}</span>
      </p>
      <p>
        {{ $t('container.train_situation') }}：
        <span class="text3">{{ situation }}</span>
      </p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DCard1',
  props:{
    time:{
      type: String,
      default: ''
    },
    situation:{
      type: String,
      default: ''
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
  margin-right: 10px;
}
.bottom{
  margin-top: 30px;
}
.bottom{
  color: #748C9A;
  font-size: 13px;
  font-family: OPPOSans R,微软雅黑;
}
.bottom p{
  margin: 5px 0;
}
.text3{
  color: #374E5C;
}
</style>
