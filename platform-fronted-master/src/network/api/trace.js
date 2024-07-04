import request from '@/utils/request'

export function getTraceList(params) {
  return request({
    url: '/trace',
    method: 'get',
    params
  })
}

export function getTrace(params) {
  return request({
    url: '/traceid',
    method: 'get',
    params
  })
}

// 获取topology数据
export function getTopology(params) {
  return request({
    url: '/topology',
    method: 'get',
    params
  })
}

// trace数据导出
export function downloadTrace(params) {
  return request({
    url: '/traceextract',
    method: 'get',
    responseType: 'blob',
    params
  })
}

// trace数据删除
export function deleteTrace(params) {
  return request({
    url: '/tracezipdelete',
    method: 'delete',
    params
  })
}
