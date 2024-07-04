
import router from './router'
import axios from 'axios'
import { UserUtils } from './store/user'
import ElementUI from 'element-ui'
import { Message } from 'element-ui'

// axios拦截器, 默认增加请求头token
axios.interceptors.request.use(
  config => {
    if (localStorage.getItem('token')) {
      config.headers.Authorization = 'token ' + localStorage.getItem('token')
    }
    return config
  },
  err => {
    return Promise.reject(err)
  }
)

// 防止同时弹出多个错误提示
let hasErrorMessage = false
const showErrorMessage = (response) => {
  console.log(response)
  if (!hasErrorMessage && response.data.message && response.status !== 401) {
    // ElementUI.Message.error(response.data.message)
    hasErrorMessage = true
    setTimeout(() => {
      hasErrorMessage = false
    }, 1000)
  }
}
// 更新token
const updateToken = (response) => {
  const oldToken = localStorage.getItem('token')
  const newToken = response.headers.authorization
  if (newToken && oldToken !== newToken) {
    localStorage.setItem('token', newToken)
  }
  // 检查是否需要移除token
  if (response.headers['remove-token']) {
    localStorage.removeItem('token')
  }
}
// axios 接口错误拦截
axios.interceptors.response.use(
  function(res) {
    updateToken(res)
    if (res.data && res.data.status && res.data.status !== 200) {
      showErrorMessage(res)
      return Promise.reject(res)
    } else if (res.data.message === 'Token expired') {
      Message.error(res.data.message)
      router.push({ path: '/login' })
      return Promise.reject(res)
    } else {
      return res
    }
  },
  function(error) {
    const err = error.response.data
    if (err.message === 'Token expired') {
      router.push({ path: '/login' })
    } else if (![500, 400, 404].includes(error.response.status)) {
      updateToken(error.response)
      showErrorMessage(error.response)
      // 401 Unauthorized
      if (error.response.status === 401) {
        UserUtils.resetUserStore()
        setTimeout(() => {
          const path = router.app.$route.path
          if (path === '/' || path === '/home') {
            location.reload()
          } else {
            router.push({ path: '/home' })
          }
        })
      }
    }
    return Promise.reject(error)
  }
)
