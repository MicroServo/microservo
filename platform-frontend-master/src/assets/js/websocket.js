import { downloadLog, deleteLog } from '@/network/api/log'
import { downloadTrace, deleteTrace } from '@/network/api/trace'
import { downloadMetric, deleteMetric } from '@/network/api/metric'
import { saveAs } from 'file-saver'

const createDownloadWebsocket = (name, url, downloadApi, deleteApi) => {
  return function(data, readyToDownload, errorFunc, waitingFunc) {
    const wb = new WebSocket(process.env.VUE_APP_BASE_WEBSOCKET_URL + url)
    let id = -1
    let success = false
    wb.onopen = () => {
      wb.send(JSON.stringify(data))
    }
    wb.onmessage = (res) => {
      console.log('websocket', res)
      const msg = JSON.parse(res.data)
      switch (msg.type) {
        case 'process':
          onwaiting(msg)
          break
        case 'error':
          onerror({ error: msg.msg })
          break
        case 'download':
          ondownload(msg)
          break
      }
    }
    wb.onclose = () => {
      if (!success) {
        onerror({ error: '连接关闭' })
      }
      console.log(name + '连接关闭')
    }
    const download = () => {
      downloadApi({
        id: id
      }).then(response => {
        saveAs(new Blob([response]), name + 'data.zip')
        deleteApi({ id: id }).then(() => {
          success = true
          wb.close()
        })
      })
        .catch(error => {
          console.error('下载失败:', error)
          wb.close()
        })
    }
    const ondownload = (downloadMsg) => {
      if (readyToDownload !== null && readyToDownload !== undefined) {
        id = downloadMsg.id
        readyToDownload()
      } else {
        onerror({ error: '未提供下载函数' })
        wb.close()
      }
    }
    const onwaiting = (waitingMsg) => {
      if (waitingFunc !== null && waitingFunc !== undefined) waitingFunc(waitingMsg)
    }
    const onerror = (errorMsg) => {
      wb.close()
      if (errorFunc !== null && errorFunc !== undefined) errorFunc(errorMsg)
    }
    return download
  }
}

const getLogDownloadFunction = createDownloadWebsocket('log', 'logexport/', downloadLog, deleteLog)
const getTraceDownloadFunction = createDownloadWebsocket('trace', 'traceexport/', downloadTrace, deleteTrace)
const getMetricDownloadFunction = createDownloadWebsocket('metric', 'metricexport/', downloadMetric, deleteMetric)

export default {
  getLogDownloadFunction,
  getTraceDownloadFunction,
  getMetricDownloadFunction
}
