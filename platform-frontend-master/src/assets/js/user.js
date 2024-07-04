import request from '@/utils/request'

export function login(data) {
  return request({
    url: '/login',
    method: 'post',
    data
  })
}

export function getInfo() {
  return request({
    url: '/info',
    method: 'get'
  })
}

export function logout() {
  return request({
    url: '/logout',
    method: 'get'
  })
}

export function getAuthorityDict() {
  return new Promise((resolve, reject) => {
    request({
      url: '/user/queryauthority',
      method: 'get'
    }).then((data) => {
      resolve(data)
    }).catch(() => {
      reject()
    })
  })
}
