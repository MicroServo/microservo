import Cookies from 'js-cookie'
import request from '@/utils/request'

const TokenKey = 'vue_admin_template_token'

export function getToken() {
  return Cookies.get(TokenKey)
}

export function setToken(token) {
  request.defaults.headers.Authorization = 'token ' + token
  return Cookies.set(TokenKey, token)
}

export function removeToken() {
  request.defaults.headers.Authorization = ''
  return Cookies.remove(TokenKey)
}
