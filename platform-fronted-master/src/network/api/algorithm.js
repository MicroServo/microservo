import request from '@/utils/request'

export function downloadAlgorithm(params) {
  return request({
    url: '/algorithm/download',
    method: 'get',
    responseType: 'blob',
    params
  })
}

export function exportAlgorithm(params) {
  return request({
    url: '/algorithm/export',
    method: 'get',
    responseType: 'blob',
    params
  })
}

export function importAlgorithm(params) {
  return request({
    url: '/algorithm/import',
    method: 'post',
    headers:{
      'Content-Type':'multipart/form-data'
    },
    data:params
  })
}

export function fetchAlgorithmType(params) {
  return request({
    url: '/algorithm/fetchalgorithmtype',
    method: 'get',
    params
  })
}
