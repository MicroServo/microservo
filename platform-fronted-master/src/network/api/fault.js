import request from '@/utils/request'

export function faultInjection(data) {
  return request({
    url: '/chaosmesh/inject',
    method: 'post',
    data
  })
}

export function getFutureFault(params) {
  return request({
    url: '/chaosmesh/getfuture',
    method: 'get',
    params
  })
}

export function faultDelete(data) {
  return request({
    url: '/chaosmesh/delete',
    method: 'post',
    data
  })
}

export function getFaultList() {
  return request({
    url: '/chaosmesh/fetch',
    method: 'get'
  })
}

export function faultExtract(params) {
  return request({
    url: '/chaosmesh/groundtruthextract',
    method: 'get',
    responseType: 'blob',
    params
  })
}

