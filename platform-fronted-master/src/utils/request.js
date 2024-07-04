import axios from 'axios'
import { Message } from 'element-ui'
import store from '@/store'
import { getToken } from '@/utils/auth'
import router from '../router'
// create an axios instance
const service = axios.create({
  baseURL: '/api/'// url = base url + request url
//   baseURL: process.env.VUE_APP_BASE_API// url = base url + request url
})

// request interceptor
service.interceptors.request.use(
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

// response interceptor
service.interceptors.response.use(
  /**
   * If you want to get http information such as headers or status
   * Please return  response => response
  */

  /**
   * Determine the request status by custom code
   * Here is just an example
   * You can also judge the status by HTTP Status Code
   */
  response => {
    if (response.data.message === 'Token expired') {
      Message.error(response.data.message)
      response.push({ path: '/login' })
      return Promise.reject(response)
    }
    if (response instanceof Blob) {
      return response
    } else {
      if (response.data instanceof Blob) {
        return response.data
      } else {
        return response.data.data
      }
    }
  },
  error => {
    const err = error.response.data
    if (err.message === 'Token expired') {
      router.push({ path: '/login' })
    }
    Message({
      message: error.message,
      type: 'error',
      duration: 5 * 1000
    })
    return Promise.reject(error)
  }
)

export default service
