import { Message } from 'element-ui'

export const deepClone = (obj, cache = []) => {
  // 如果为普通数据类型，则直接返回，完成拷贝
  if (obj === null || typeof obj !== 'object') {
    return obj
  }
  // cache用来储存原始值和对应拷贝数据，在递归调用deepCopy函数时，如果本次拷贝的原始值在之前已经拷贝了，则直接返回储存中的copy值，这样的话就不用再循环复制本次原始值里面的每一项了。
  // 还有一个更为重要的作用，假如原始值里面嵌套两个引用地址相同的对象，使用cache可以保证拷贝出来的copy值里面两个对象的引用地址也相同。
  // 如果find查找的是一个空数组，则不会执行
  const hit = find(cache, (c) => c.original === obj)
  if (hit) {
    return hit.copy
  }
  // 定义拷贝的数据类型
  const copy = Array.isArray(obj) ? [] : {}
  // 用来记录拷贝的原始值和copy值
  cache.push[
    {
      original: obj,
      copy
    }
  ]
  // 递归调用深拷贝函数，拷贝对象中的每一个值
  Object.keys(obj).forEach((key) => {
    copy[key] = deepClone(obj[key], cache)
  })
  return copy
}

/**
 * 检测区间超时情况
 * @param {Number} s 起始时间戳
 * @param {Number} e 结束时间戳
 * @param {Number} duration 时长（min）
 * @param {Boolean} msg 是否有超时提示（默认true）
 * @returns Boolean 是否超时
 */
export function judgeDuration(s, e, duration, msg = true) {
  const res = (e - s) / 1000 / 60 <= duration
  if (!res) message('时间请限制在' + duration.toString() + '分钟内')
  return res
}

/**
 * 显示提示框
 * @param {String} msg 提示信息
 * @param {String} type 提示类型（默认error）
 * @param {Number} duration 提示时长（默认3000(ms)）
 */
export function message(msg, type, duration) {
  Message({
    message: msg,
    type: type || 'error',
    duration: duration || 3 * 1000
  })
}

/**
 * 防抖函数
 * @param {Function} func 待执行的函数
 * @param {Number} delay 防抖时间
 * @returns Function
 */
export function debounce(func, delay = 200) {
  let timerId
  return function(...args) {
    clearTimeout(timerId)
    timerId = setTimeout(() => {
      func.apply(this, args)
    }, delay)
  }
}

/**
 * 节流函数
 * @param {Function} func 待执行的函数
 * @param {Number} delay 防抖时间
 * @returns Function
 */
export function throttle(func, delay) {
  let timerId
  let lastExecutedTime = 0
  return function(...args) {
    const currentTime = Date.now()
    const timeSinceLastExecution = currentTime - lastExecutedTime
    if (timeSinceLastExecution >= delay) {
      func.apply(this, args)
      lastExecutedTime = currentTime
    } else {
      clearTimeout(timerId)
      timerId = setTimeout(() => {
        func.apply(this, args)
        lastExecutedTime = Date.now()
      }, delay - timeSinceLastExecution)
    }
  }
}

// 时间格式化
export function formatDate(data) {
  const date = new Date(data)// 时间戳为10位需*1000，时间戳为13位的话不需乘1000
  const Y = date.getFullYear() + '-'
  const M = (date.getMonth() + 1 < 10 ? '0' + (date.getMonth() + 1) : date.getMonth() + 1) + '-'
  const D = (date.getDate() < 10 ? '0' + date.getDate() : date.getDate()) + ' '
  const h = (date.getHours() < 10 ? '0' + date.getHours() : date.getHours()) + ':'
  const m = (date.getMinutes() < 10 ? '0' + date.getMinutes() : date.getMinutes()) + ':'
  const s = date.getSeconds() < 10 ? '0' + date.getSeconds() : date.getSeconds()
  return Y + M + D + h + m + s
}
