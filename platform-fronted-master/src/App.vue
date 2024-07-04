<template>
  <div id="app">
    <Header
      v-if="!$route.meta.noHeader"
      @updataPage="updataPage"/>
    <div class="page">
      <router-view v-if="isRouterAlive" />
    </div>
  </div>
</template>

<script>
import Header from '@/components/header'
export default {
  name: 'App',
  components: {
    Header
  },
  data() {
    return {
      isRouterAlive:true
    }
  },
  methods: {
    updataPage(v) {
      this.isRouterAlive = false
      this.$nextTick(function() {
        this.isRouterAlive = true
      })
    }
  }
}
</script>

<style>
html {
	height: auto;
	padding: 0;
	margin: 0;
	font-size: 16px;
	font-family: OPPOSans-M,"Microsoft Yahei","pingfang","Adobe Heiti Std","Arial","sans-serif";
	color: #000;
	line-height: 150%;
	text-align: center;
	-webkit-tap-highlight-color:rgba(0,0,0,0);
  background-color: #F5F8FA;
}
body{
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  padding: 0;
  margin: 0;
  margin-left: auto;
  margin-right: auto;
}
#app {
  width: 100%;
  height: 100%;
}
/* 隐藏expand的展开箭头 */
.el-table__expand-icon {
    visibility: hidden;
}
.el-popover{
  max-height: 30%;
  overflow: auto;
}
/* 页面通用类 */
.page {
  position: relative;
  height: calc(100% - 80px);
}
/* 全局滚动条样式 */
::-webkit-scrollbar {
  width: 8px;
	height: 8px;
  visibility: hidden !important;
}
::-webkit-scrollbar-track {
  background-color: rgba(0, 0, 0, 0.1) !important;
	border-radius: 4px;
}
::-webkit-scrollbar-thumb {
	border-radius: 4px;
	background-color: rgba(0, 0, 0, 0.15) !important;
}
/* 卡片标题 */
.card-title {
  position: relative;
  text-align: left;
  font-weight: bold;
  margin-bottom: 5px;
}
.card-title::before {
  display: inline-block;
  content: ' ';
  width: 2px;
  height: 16px;
  border-left: 2px solid #00A0FF;
  position: absolute;
  left: 0;
  top: -50%;
  transform: translateX(-5px) translateY(100%);
}
.card-title > span {
  margin-left: 5px;
}
</style>
