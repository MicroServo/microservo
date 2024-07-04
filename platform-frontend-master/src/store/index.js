// store文件夹下所有状态的统一出口

import Vue from 'vue'
import Vuex from 'vuex'
import getters from './getters'
import app from './modules/app'
import settings from './modules/settings'
import user from './modules/user'
import routes from './modules/routes'

Vue.use(Vuex)

const state = {
  userInfo: {},
  // randomUrl: '',
  userObject: localStorage['userObject'],
  ruleForm: {
    name: '',
    courseId: '',
    detail: '',
    announcement: '',
    cover: '',
    category: [],
    tag: [],
    menu: []
  },
  productImgs: [],
  menu: []
}

const store = new Vuex.Store({
  modules: {
    app,
    settings,
    user,
    routes
  },
  getters,
  state: {
    promptDuration: 5000
  }
})

export default new Vuex.Store({
  state,
  store
})
