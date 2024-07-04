<!--公有header组件-->
<template>
  <div class="headerBox">
    <div class="header">
      <div class="leftBox">
        <img
          v-if="lang==='zh'"
          src="../../assets/images/logo/logo-zh.png"
          class="logo">
        <img
          v-if="lang==='en'"
          src="../../assets/images/logo/logo-en-new.png"
          class="logo">
      </div>
      <nav class="nav">
        <ul>
          <li :class="{'on':currentRoute === '/home'||currentRoute === '/'} ">
            <router-link to="/home">{{ $t("menu.home") }}</router-link>
          </li>
          <li :class="{'on':currentRoute ==='/faultInjection'} ">
            <router-link to="/faultInjection">{{ $t("menu.faultInjection") }}</router-link>
          </li>
          <li :class="{'on':currentRoute ==='/dataMonitor'} ">
            <router-link to="/dataMonitor">{{ $t("menu.dataMonitor") }}</router-link>
          </li>
          <li :class="{'on':currentRoute ==='/rankings'} ">
            <router-link to="/rankings">{{ $t("menu.rankingList") }}</router-link>
          </li>
          <li :class="{'on':currentRoute ==='/algorithmManagement'} ">
            <router-link to="/algorithmManagement">{{ $t("menu.algorithmManagement") }}</router-link>
          </li>
          <li :class="{'on':currentRoute ==='/algorithmTemplate'} ">
            <router-link to="/algorithmTemplate">{{ $t("menu.algorithmTemplate") }}</router-link>
          </li>
          <li :class="{'on':currentRoute ==='/evaluateData'} ">
            <router-link to="/evaluateData">{{ $t("menu.evaluateData") }}</router-link>
          </li>
          <!-- <li :class="{'on':currentRoute ==='/userManagement'} ">
            <router-link to="/userManagement">{{ $t("menu.userManagement") }}</router-link>
          </li> -->
        </ul>
      </nav>
      <div class="btnW">
        <div class="rightBox">
          <!-- 语言切换 -->
          <div
            class="languageChoose"
            @click="changeLanguage">
            <img src="../../assets/images/主页/编组@2x(21).png">
            <span v-if="lang==='en'">中文</span>
            <span v-if="lang==='zh'">ENGLISH</span>
          </div>
          <!-- 消息提示 -->
          <!-- <div class="languageChoose">
            <img src="../../assets/images/主页/编组@2x.png">
          </div> -->
          <span class="line">|</span>
          <div class="my-dropdown">
            <el-dropdown @command="handleCommand">
              <div class="flex-box">
                <el-avatar
                  :size="30"
                  :src="circleUrl"
                  @click="goRouter('/userCenter')"/>
                <div class="nameBox">
                  <span
                    class="userName"
                    @click="goRouter('/userCenter')">{{ userName }}</span>
                  <span class="userRole">{{ userRole }}</span>
                </div>
                <img
                  src="../../assets/images/主页/编组33@2x.png"
                  class="dropDown">
              </div>

              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item command="user">{{ $t("menu.userCenter") }}</el-dropdown-item>
                <el-dropdown-item
                  command="logout"
                  style="background-color: white;">{{ $t("menu.logout") }}</el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>
          </div>

        </div>
      </div>
    </div>
    <div
      class="position">
      <breadcrumb :lang="lang"/>
    </div>

  </div>
</template>

<script>
import breadcrumb from '@/components/breadcrumb'
export default {
  name: 'Header',
  components: {
    breadcrumb
  },
  data() {
    return {
      circleUrl: 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png',
      currentRoute: '',

      userName: localStorage.getItem('username'),
      userRole: 'User',
      userObject: null,
      localPath: '',
      lang: 'en'
    }
  },
  watch: {
    $route(to, from) {
      this.loadChange()
    }
  },
  created() {
  },
  // 页面挂载之后,解析路由，给出面包屑，路由里面一定要含有breadCom组件的path
  mounted: function() {
    this.loadChange()
  },
  methods: {
    handleUpdate() {
      this.$emit('updataPage', false)
    },
    handleCommand(command) {
      switch (command) {
        case 'user':
          this.goRouter('/userCenter')
          break
        case 'logout':
          this.signout()
          break
      }
    },
    // 切换语言
    changeLanguage() {
      if (this.lang === 'en') {
        this.lang = 'zh'
      } else {
        this.lang = 'en'
      }
      localStorage.setItem('lang', this.lang)
      this.$i18n.locale = this.lang
      this.handleUpdate()
    },
    goRouter(value) {
      if (value === '#') {
        return
      }
      this.$router.push(value)
    },
    loadChange() {
      const routeObj = this.$router.currentRoute
      if (routeObj.hasOwnProperty('redirectedFrom')) {
        this.currentRoute = routeObj.redirectedFrom
      } else {
        this.currentRoute = routeObj.fullPath
      }
      if (this.currentRoute.indexOf('dataMonitor') !== -1) {
        this.currentRoute = '/dataMonitor'
      }
      if (this.currentRoute.indexOf('userManagement') !== -1) {
        this.currentRoute = '/userManagement'
      }
      if (this.currentRoute.indexOf('evaluateData') !== -1) {
        this.currentRoute = '/evaluateData'
      }
    },
    // 登出，清除localstorage
    signout() {
      localStorage.clear()
      this.$router.push('/login')
      location.reload()
    }
  }
}
</script>

<style scoped>
/* 目前headerBox高度是80px 如果需要改 同时需要去修改page结构组件 */
span:hover {
  cursor: pointer;
}
.headerBox {
  background-color: white;
  height: 80px;
  font-size: 13px;
}
.header {
  background-color: #FFFFFF;
  height: 55px;
  box-shadow: 0px 0px 12px 0px rgba(165,183,193,0.3), inset 0px -1px 0px 0px #E9EBF2;
  background: url(../../assets/images/主页/header_bg.png) 0 center no-repeat;
  background-size: contain;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.leftBox {
  display: flex;
  align-items: center;
}
.logo{
  margin-left: 20px;
}
.nav {
  width: 57%;
  max-width: 780px;
}
.nav ul {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
ul,li {
	list-style: none;
	padding: 0;
	margin: 0;
  min-width: 85px;
  height: 40px;
}
a {
  text-decoration: none;
  color: #000;
}
.nav li.on a {
  background: #00A0FF;
  box-shadow: 0px 2px 8px 0px rgba(0,160,255,0.5);
  border-radius: 8px;
  color: #FFFFFF;
  padding: 0 5px;
}
.nav a {
  font-weight: normal;
  color: #374E5C;
  text-align: center;
  min-width: 85px;
  height: 40px;
  background-color: #F5F7F9;
  border-radius: 8px;
  vertical-align: middle;
  display: table-cell;
  line-height: 1.3;
}
.nav a:hover {
  color:#748C9A;
}
.position {
  line-height: 20px;
  text-align: left;
  padding: 5px 0 0 10px;
  background-color: #f5f8fa;
}
.position a {
  font-weight: normal;
  font-size: 14px;
  color: #748C9A;
  line-height: 18px;
  text-align: left;
}
.position span{
  font-weight: normal;
  font-size: 14px;
  color: #748C9A;
  line-height: 18px;
  text-align: left;
}
.position a:hover {
  color: #748C9A;
}
.position .line {
  margin: 0 2px;
  font-weight: normal;
  font-size: 14px;
  color: #748C9A;
  line-height: 18px;
  text-align: left;
}
.container {
  width: 100%;
  background-color: #F5F8FA;
}
.rightCheck {
  flex: 1;
  padding-top: 1.2%;
  padding-left: 2%;
}
.breadTitle {
  margin: auto;
  height: 45px;
  width: 70%;
}
.header .btnW .line { margin: 0 5px;}
.languageChoose{
  height: 38px;
  padding: 0 12px;
  background: #F0F5F8;
  border-radius: 19px;
  display: flex;
  align-items: center;
  justify-content: space-around;
  margin-left: 5px;
  font-size: 12px;
}
.languageChoose:hover{
  color: rgb(131, 131, 131);
  filter: invert(0%) sepia(0%) saturate(0%) hue-rotate(324deg) brightness(96%) contrast(104%);
}
.languageChoose span{
  font-weight: 400;
  color: #748C9A;
  line-height: 20px;
  text-align: left;
  font-style: normal;
  text-transform: uppercase;
  min-width: 30px;
}
.languageChoose img{
  width: 15px;
  height: 15px;
}
.rightBox{
  display: flex;
  align-items: center;
}
.userName{
  font-size: 13px;
  color: #374E5C;
  display: block;
}
.userRole{
  font-size: 11px;
  color: #748C9A;
  display: block;
}
.line{
  color: #B5BEC4;
  cursor: default;
}
.nameBox{
  margin-left: 10px;
  max-width: 130px;
  text-align: left;
  margin-right: 10px;
}
.dropDown{
  width: 13px;
  height: 13px;
  margin-right: 5px;
}
.flex-box{
  display: flex;
  align-items: center;
}
</style>
