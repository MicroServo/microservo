import request from '@/utils/request'

// 获取log num数据
export function getLogNum(params) {
  return request({
    url: '/lognum',
    method: 'get',
    params
  })
}

// log数据导出
export function downloadLog(params) {
  return request({
    url: '/logextract',
    method: 'get',
    responseType: 'blob',
    params
  })
}

// log数据删除
export function deleteLog(params) {
  return request({
    url: '/logzipdelete',
    method: 'delete',
    params
  })
}

// 获取log数据
export function getLog(params) {
  return request({
    url: '/log',
    method: 'get',
    params
  })
}
