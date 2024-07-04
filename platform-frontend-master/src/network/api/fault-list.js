import request from '@/utils/request'

export function getGroundTruth(params) {
  return request({
    url: '/chaosmesh/get',
    method: 'get',
    params
  })
}
// 导出
export function groundtruthextract(params) {
  return request({
    url: '/chaosmesh/groundtruthextract',
    method: 'get',
    responseType:'blob',
    params
  })
}
