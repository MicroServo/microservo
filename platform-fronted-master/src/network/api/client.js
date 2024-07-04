import request from '@/utils/request'

// 用户名登录
export function loginByUsername(data) {
  return request({
    url: '/loginByUsername',
    method: 'post',
    data
  })
}

// 邮箱登录
export function loginByEmail(data) {
  return request({
    url: '/loginByEmail',
    method: 'post',
    data
  })
}
// 注册
export function register(data) {
  return request({
    url: '/register',
    method: 'post',
    data
  })
}

// 发送验证码
export function sendEmail(data) {
  return request({
    url: '/sendEmail',
    method: 'post',
    data
  })
}

// 找回密码
export function retrieve(data) {
  return request({
    url: '/retrieve',
    method: 'post',
    data
  })
}
