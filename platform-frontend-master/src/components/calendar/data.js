/**
 * @FileDescription
 * 日历数据管理器
 * @Author
 * Wen Long
 * @Date
 * 2024/3/30
 * @LastEditors
 * Wen Long
 * @LastEditTime
 * 2024/4/2
 */

/**
 * 随机测试数据生成器生成器
 * @returns 随机测试数据生成器
 */
import { getGroundTruth } from '@/network/api/fault-list.js'
import { getFutureFault } from '../../network/api/fault'
function createRandomData() {
  const dataMap = new Map()
  const DAY = 1000 * 60 * 60 * 24
  const ERROR_MIN_AMOUNT = 5
  const ERROR_MAX_AMOUNT = 10
  const WAITING_MIN = 1
  const WAITING_MAX = 100
  const DURATION_MAX = 60 * 120 // s
  const DURATION_MIN = 60 * 10 // s
  const ERROR = ['cpu', 'pod-failure', 'network-delay', 'memory', 'loss', 'abort', 'delay']
  /**
   * 随机测试数据生成器
   */
  return function(begin, end) {
    const waiting = parseInt(Math.random() * (WAITING_MAX - WAITING_MIN) + WAITING_MIN)
    const date = new Date(begin)
    const y = date.getFullYear()
    const m = date.getMonth() + 1
    const d = date.getDate()
    const key = y.toString() + '-' + m.toString() + '-' + d.toString()
    console.log(y, m, d)
    console.log(y, m, d, Math.floor(begin / 1000), Math.floor(end / 1000))
    if (dataMap.get(key) !== undefined) {
      return new Promise((resolve, reject) => {
        setTimeout(() => {
          resolve(dataMap.get(key))
        }, waiting)
      })
    } else {
      const errorAmount = parseInt(Math.random() * (ERROR_MAX_AMOUNT - ERROR_MIN_AMOUNT) + ERROR_MIN_AMOUNT)
      const errorList = []
      for (let i = 0; i < errorAmount; i++) {
        const timestamp = begin + parseInt(Math.random() * (DAY - 0) + 0)
        const duration = parseInt(Math.random() * (DURATION_MAX - DURATION_MIN) + DURATION_MIN)
        errorList.push({
          timestamp: timestamp,
          service: 'cartservice',
          cmdb_id: 'cartservice-5cdcc9d789-7vvkh',
          failure_type: ERROR[parseInt(Math.random() * (ERROR.length - 1))],
          duration: duration
        })
      }
      dataMap.set(key, errorList)
    }
  }
}

class CalendarDataManager {
  constructor() {
    /**
     * 随机数据生成器
     */
    this.testDataCreater = createRandomData()

    /**
     * 一天的毫秒数
     */
    this.DAY = 1000 * 60 * 60 * 24

    /**
     * 一周的毫秒数
     */
    this.WEEK = this.DAY * 7

    /**
     * 临时变量
     */
    let temp = null

    /**
     * 类型
     * - week 按周
     * - day 按天
     *
     * 返回的数据会不同
     */
    this.type = 'week'

    /**
     * 数据图
     *
     * 获得过的数据不会重新访问服务器
     */
    this.dataMap = new Map()

    /**
     * 选中的日期的当天的开始时间戳
     * 取消选中之后改成null
     * 在day模式下 这个就是当天的开始时间戳
     * week模式下可以不进行选中
     *
     * week切换到day时
     * - 此值不设定，则day是当天
     * - 设定则为设定那天
     *
     * day切换到week时
     * - 会切换到对应那天的那周
     */
    this.selectedDate = null

    temp = new Date()
    temp.setHours(0, 0, 0, 0)

    /**
     * 本日开始的时间戳
     */
    this.TODAY_BEGIN = temp.getTime()

    temp = new Date()
    temp.setDate(new Date().getDate() - new Date().getDay())
    temp.setHours(0, 0, 0, 0)

    /**
     * 本周开始的时间戳
     * - 星期天返回的是0
     * - 一周从星期天开始计算
     */
    this.WEEK_BEGIN = temp.getTime()

    /**
     * ### 显示的日期起始时间戳
     */
    this.SHOW_BEGIN = this.WEEK_BEGIN

    // console.log(new Date(), new Date(this.TODAY_BEGIN), new Date(this.WEEK_BEGIN), new Date(this.SHOW_BEGIN), this.SHOW_BEGIN)
    /**
     * 随机字符串生成器
     * - 保证绝对不重复
     * - 用于card渲染的key
     */
    this.generateRandomString = this.generateRandomStringBase()
  }

  /**
   * 恢复默认值
   */
  restore() {
    this.type = 'week'
    this.selectedDate = null
    this.SHOW_BEGIN = this.WEEK_BEGIN
  }

  /**
   * 强制刷新数据
   * @returns 数据
   */
  refresh() {
    this.dataMap.clear()
  }

  /**
   * 获取当前类型
   * - week
   * - day
   * @returns type
   */
  getType() {
    return this.type
  }

  /**
   * 设置当前类型
   * - week
   * - day
   * @param {String} type 类型
   */
  setType(type) {
    if (type === 'week' && this.type !== 'week') {
      // 转为week
      this.type = type
      /**
       * 此时SHOW_BEGIN是day显示的那天
       * 将显示那周
       * SHOW_BEGIN = SHOW_BEGIN那天对应的那周的开始时间戳
       */
      this.SHOW_BEGIN = this.timestampGetWeekBegin(this.SHOW_BEGIN)
    } else if (type === 'day' && this.type !== 'day') {
      // 转为day
      this.type = type
      /**
       * 如果选中了某一天，那么就显示那一天
       * 没选中则显示本日
       */
      this.SHOW_BEGIN = this.selectedDate ? this.selectedDate : this.TODAY_BEGIN
    }
  }

  /**
   * 获取选中的日期开始时间戳
   * @returns selectedDate
   */
  getSelectedDate() {
    return this.selectedDate
  }

  /**
   * 设置选中的日期
   * - 取消选中传入null
   * @param {Number} selectedDate 选中的日期
   */
  setSelectedDate(selectedDate) {
    this.selectedDate = typeof selectedDate === 'number' ? selectedDate : null
  }

  /**
   * ### 获取数据
   *
   * 可能需要访问服务器
   * 所以是异步
   *
   * - 查过去数据接口为 查询故障
   * - 查未来数据接口为 查询待注入故障
   *
   * @param {Boolean} past 是否查询过去数据
   * @param {Boolean} future 是否查询未来数据
   * @returns data
   */
  async getDataSync(past = true, future = false) {
    // 先检索第一天的前一天的数据
    await this.queryDataByDayRange(this.SHOW_BEGIN - this.DAY, this.SHOW_BEGIN, past, future)
    if (this.type === 'day') return await this.queryDataByDayRange(this.SHOW_BEGIN, this.SHOW_BEGIN + this.DAY, past, future)
    else if (this.type === 'week') return await this.queryDataByDayRange(this.SHOW_BEGIN, this.SHOW_BEGIN + this.WEEK, past, future)
  }

  /**
   * 返回日历需要的日期
   * @returns 日历需要的日期
   */
  getCalendarShowDate() {
    let begin = this.SHOW_BEGIN
    let end = 0
    if (this.type === 'day') {
      end = begin + this.DAY
    } else if (this.type === 'week') {
      end = begin + this.WEEK
    }
    const res = []
    while (begin < end) {
      const date = new Date(begin)
      const y = date.getFullYear() < 10 ? '0' + date.getFullYear().toString() : date.getFullYear().toString()
      const M = date.getMonth() + 1 < 10 ? '0' + (date.getMonth() + 1).toString() : (date.getMonth() + 1).toString()
      const d = date.getDate() < 10 ? '0' + date.getDate().toString() : date.getDate().toString()
      const D = date.getDay()
      begin += this.DAY
      res.push({
        y: y,
        M: M,
        d: d,
        D: D
      })
    }
    return res
  }

  /**
   * 跳转回今天
   */
  toToday() {
    if (this.type === 'day') this.SHOW_BEGIN = this.TODAY_BEGIN
    else if (this.type === 'week') this.SHOW_BEGIN = this.WEEK_BEGIN
  }

  /**
   * 跳转到明天
   */
  nextDay() {
    this.SHOW_BEGIN += this.DAY
  }

  /**
   * 跳转到昨天
   */
  lastDay() {
    this.SHOW_BEGIN -= this.DAY
  }

  /**
   * 跳转到下一周
   */
  nextWeek() {
    this.SHOW_BEGIN += this.WEEK
  }

  /**
   * 跳转到上一周
   */
  lastWeek() {
    this.SHOW_BEGIN -= this.WEEK
  }

  /**
   * 跳转到指定日期
   * @param {*} day 日期
   */
  setDay(day) {
    this.SHOW_BEGIN = new Date(day).setHours(0, 0, 0, 0)
  }

  /**
   * 跳转到指定周
   * @param {*} week 周
   */
  setWeek(week) {
    this.SHOW_BEGIN = new Date(week).setHours(0, 0, 0, 0)
  }

  /**
   * async
   *
   * 根据时间段获取数据
   * - 如果数据map中没存，则发请求检索
   * - 存储则直接调用
   *
   * ### 注意
   * 1. 查询1月1日的数据会处理1月1日开始持续到1月2日结束的数据
   * 2. 查询1月1日的数据，不会获得12月31日开始持续到1月1日结束的数据
   *
   * 所以查询1月1日数据之前需要先查询完12月31日数据
   * @param {Number} begin 起始时间戳 建议是某天的起始
   * @param {Number} end 结束时间戳 建议是某天的结束
   * @returns 这段时间内的数据
   */
  async queryDataByDayRange(begin = null, end = null, past = true, future = false) {
    // console.log(past, future)
    if (!begin || !end) return []
    const res = []
    while (begin < end) {
      const today = new Date(begin)
      const tomorrow = new Date(begin + this.DAY)
      // console.log(today, tomorrow, new Date(this.SHOW_BEGIN), this.SHOW_BEGIN)
      const y = today.getFullYear()
      const m = today.getMonth() + 1 // month从0开始
      const d = today.getDate()
      const dataMap = this.dataMap
      const key = y.toString() + '-' + m.toString() + '-' + d.toString()
      if (dataMap.get(key) === undefined || !dataMap.get(key).query) {
        const startTime = begin
        const endTime = begin + this.DAY
        const now = Date.now()
        /* <----------------- 测试 -----------------> */
        // const getData = await this.testDataCreater(begin, begin + this.DAY)

        const getPastData = startTime <= now ? await getGroundTruth({
          start_time: Math.floor(startTime / 1000),
          end_time: Math.floor(endTime / 1000)
        }).then((res) => {
          res.ground_truth.forEach((item) => {
            item.timestamp *= 1000
          })
          return res.ground_truth
        }) : []
        const getFutureData = endTime >= now ? await getFutureFault({
          start_time: Math.max(Math.floor(startTime / 1000), Math.floor(now / 1000)),
          end_time: Math.floor(endTime / 1000)
        }).then((res) => {
          res.ground_truth.forEach((item) => {
            item.timestamp *= 1000
          })
          return res.ground_truth
        }) : []
        const getDateAfter = []
        getPastData.forEach((data, i) => {
          getDateAfter.push({
            data: this.deepClone(data)
          })
        })
        getFutureData.forEach((data, i) => {
          getDateAfter.push({
            data: this.deepClone(data)
          })
        })
        /* <----------------- 测试 -----------------> */
        const todayData = dataMap.get(key) === undefined ? getDateAfter : getDateAfter.concat(dataMap.get(key).data)
        const tempRes = this.afterProcessing(begin, todayData)
        if (tempRes.tomorrow.length !== 0) {
          // 处理隔天
          const ty = tomorrow.getFullYear()
          const tm = tomorrow.getMonth() + 1 // month从0开始
          const td = tomorrow.getDate()
          const tkey = ty.toString() + '-' + tm.toString() + '-' + td.toString()
          if (dataMap.get(tkey) === undefined) {
            dataMap.set(tkey, {
              data: this.deepClone(tempRes.tomorrow),
              query: false
            })
          } else {
            dataMap.get(tkey).data = this.deepClone(tempRes.tomorrow)
            dataMap.get(tkey).query = false
          }
        }
        dataMap.set(key, {
          data: this.deepClone(tempRes.today),
          query: true
        })
      }
      const data = dataMap.get(key).data
      const now = Date.now()
      const temp = []
      data.forEach((d) => {
        // 检查时间
        if (now < d.data.timestamp) {
          if (future) {
            temp.push(d)
          }
        } else {
          if (past) {
            temp.push(d)
          }
        }
      })
      res.push(temp)
      begin += this.DAY
    }
    return res
  }

  /**
   * 传入时间戳获取那周开始的时间戳
   *
   * *周开始是星期天*
   * @param {Number} timestamp 时间戳
   * @returns 时间戳那天对应的那周的起始时间戳
   */
  timestampGetWeekBegin(timestamp) {
    const date = new Date(timestamp)
    date.setDate(date.getDate() - date.getDay())
    date.setHours(0, 0, 0, 0)
    console.log('timestampGetWeekBegin', date)
    return date.getTime()
  }

  /**
   * 此函数需要处理data
   * 将其转换成可以渲染的数据
   * 渲染的规则是希望
   * - 故障每行均分且占住区域最大
   * - 留白区域最少
   * ```js
   * data: {
   *  data: {
   *    timestamp: 1711434600, // 时间戳 ms
   *    service: 'cartservice',
   *    cmdb_id: 'cartservice-5cdcc9d789-7vvkh',
   *    failure_type: 'cpu',
   *    duration: 60, // 单位 s
   *  },
   *  // 新增内容
   *  s: xxxx, // 今日开始时间戳 ms
   *  f: xxxx, // 今日结束时间戳 ms
   *  index: 0, // 第index+1列
   *  ans: 1, // 此组有ans列
   *  width: 1, // 占用一个单元宽度
   *  drawId: xxxx, // 渲染用id
   *  draw: true, // 是否渲染 理论上返回的都是true 会进行过滤
   * }
   * ```
   * 优化处理数据
   * - 可能同时发生故障，此时需要处理
   * - 故障可能有隔天的，需要处理
   *
   * **只处理一天**
   *
   * @param {Array} data 数据
   * @returns 优化后的数据
   */
  afterProcessing(begin, data) {
    if (data.length === 0) {
      return {
        today: [],
        tomorrow: []
      }
    }
    const end = begin + this.DAY
    const res = []
    const nextDayData = []
    // 先处理隔天情况
    data.forEach((item) => {
      item.drawId = item.drawId ? item.drawId : this.generateRandomString()
      item.s = item.data.timestamp < begin ? 0 : item.data.timestamp - begin
      item.f = item.data.timestamp + item.data.duration * 1000 > end ? end - begin : item.data.timestamp + item.data.duration * 1000 - begin
      /* 设置最小高度 最小高度是40min对应的高度 */
      // item.f = item.f - item.s < 1000 * 60 * 40 ? item.s + 1000 * 60 * 40 : item.f // 设置最小高度
      /* 设置最小高度 最小高度是40min对应的高度 */
      item.index = 0
      item.ans = 1
      item.width = 1
      item.draw = true
      if (item.data.timestamp + item.data.duration * 1000 > end) nextDayData.push(item) // 隔天的
      res.push(this.deepClone(item))
    })
    res.sort((a, b) => a.s - b.s)
    // 计算
    const meetingList = [[[]]]
    let ans = 1
    meetingList[0][0].push(res[0])
    res.forEach((item, i) => {
      if (i === 0) return
      const lastMeetingGroup = meetingList[meetingList.length - 1]
      const l = lastMeetingGroup.length
      lastMeetingGroup.sort((a, b) => a[0].f - b[0].f) // 结束时间从早到晚
      let inside = false
      if (l > 0 && lastMeetingGroup[l - 1][0].f > item.s) inside = true // 最大结束时间大于当前开始时间 没有时间重叠
      if (inside) {
        let canInsert = true
        if (lastMeetingGroup[0][0].f > item.s) canInsert = false // 最小结束时间大于当前开始时间 无法直接插入 需要新增一列
        if (canInsert) {
          item.ans = ans
          item.index = lastMeetingGroup[0][0].index // 这两者是同一列的
          lastMeetingGroup[0].unshift(item) // 插入最先结束的组
        } else {
          item.index = ans // item是第ans + 1列 所以index是ans
          ans++
          lastMeetingGroup.forEach((g) => {
            g.forEach((m) => {
              m.ans = ans // 列数加一
            })
          })
          item.ans = ans
          lastMeetingGroup.push([item]) // 增加一个组
        }
      } else {
        if (l === 0) lastMeetingGroup[0].push(item)
        else {
          ans = 1
          const now = [[item]]
          meetingList.push(now)
        }
      }
    })
    // 处理宽度
    meetingList.forEach((g) => {
      g.sort((a, b) => a[0].index - b[0].index) // 按照列位置排序
      g.forEach((m, i) => {
      // 最后一列不需要检查
        m.forEach((ele, ii) => {
          if (!ele.draw) return
          // 左侧需要检查，左侧可能有空间
          const eleUndraw = this.deepClone(ele)
          eleUndraw.draw = false
          let wr = 1
          let checkM = g[i + wr]
          while (checkM !== undefined && checkM.find((item, i) => {
            // 先往右侧找 找到一个不满足的就退出
            if (item.s <= ele.s && item.f > ele.s) return true
            else if (item.f >= ele.f && item.s < ele.f) return true
            else if (item.s >= ele.s && item.f <= ele.f) return true
            else return false
          }) === undefined) {
            wr++
            checkM.push(eleUndraw)
            checkM = g[i + wr]
          }
          ele.width = wr
          if (i > 0) {
            let wl = 1
            checkM = g[i - wl]
            while (checkM.find((item, i) => {
              // 再往左侧找 找到一个不满足的就退出
              if (item.s <= ele.s && item.f > ele.s) return true
              else if (item.f >= ele.f && item.s < ele.f) return true
              else if (item.s >= ele.s && item.f <= ele.f) return true
              else return false
            }) === undefined) {
              wl++
              checkM.push(eleUndraw)
              if (i - wl < 0) break
              checkM = g[i - wl]
            }
            ele.index = ele.index + 1 - wl
            ele.width = ele.width - 1 + wl
            if (ele.index !== i) {
              // 如果改变了左侧index
              const insertM = g[ele.index]
              insertM.pop() // 弹出最后一个压入的 eleUndraw
              insertM.push(this.deepClone(ele))
              res.push(this.deepClone(ele))
              ele.draw = false
            }
          }
        })
      })
    })
    return {
      today: res.filter((item) => item.draw).sort((a, b) => a.s - b.s),
      tomorrow: nextDayData
    }
  }

  /**
 * 对象深拷贝
 * @param {Object} obj 对象
 * @param {Object} cache cache
 * @returns 深拷贝的新的对象
 */
  deepClone(obj, cache = []) {
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
      copy[key] = this.deepClone(obj[key], cache)
    })
    return copy
  }

  /**
   * 随机字符串生成函数生成器
   * - 闭包存储map
   * @returns 随机字符串生成函数
   */
  generateRandomStringBase() {
    const idMap = new Map()
    idMap.set('', true)
    return function() {
      let result = ''
      const length = 10
      const characters = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
      const charactersLength = characters.length

      while (idMap.get(result) === true) {
        for (let i = 0; i < length; i++) {
          result += characters.charAt(Math.floor(Math.random() * charactersLength))
        }
      }
      idMap.set(result, true)

      return result
    }
  }
}

export default CalendarDataManager
