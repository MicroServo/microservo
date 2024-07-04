// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import axios from 'axios'
import './assets/iconfont/iconfont.js'
import '@/assets/css/color.css'
import '@/assets/font/font.css'
import 'normalize.css/normalize.css'
import store from './store/index'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import Viewer from 'v-viewer'
import 'viewerjs/dist/viewer.css'
import './axios-config'
import './permission'

import lang from 'element-ui/lib/locale/lang/en'
import locale from 'element-ui/lib/locale'

// 设置语言
locale.use(lang)

import JsonViewer from 'vue-json-viewer'
Vue.use(JsonViewer)

Vue.config.productionTip = false

Vue.prototype.$http = axios
Vue.prototype.$axios = axios

Vue.use(Viewer)

Vue.use(ElementUI)

// start-翻译配置
import VueI18n from 'vue-i18n'
// 从语言包文件中导入语言包对象
import zh from '@/assets/lang/zh'
import en from '@/assets/lang/en'

Vue.use(VueI18n)

const messages = {
  zh,
  en
}
const i18n = new VueI18n({
  messages,
  locale: 'en'
})
// end-翻译配置

new Vue({
  el: '#app',
  router,
  store,
  i18n,
  components: { App },
  template: '<App/>'
})

