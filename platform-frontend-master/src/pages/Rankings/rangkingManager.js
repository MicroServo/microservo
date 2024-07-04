import EventManager from '../../utils/event'
import LRUCache from '../../utils/lru'

import {
  getEvaluationMetrics,
  getAlgorithmType,
  getAlgorithms,
  getAllMedals,
  getAllRecords,
  createRecord,
  addNewAlgorithm,
  queryRecordDetailData,
  reEvaluation
} from '../../network/api/ranking'

/**
 * ## 核心方法使用
 *
 * 1. render 渲染页面
 * 2. setAlgorithmType 改变算法类型
 * 3. setEvaluationMetric 改变评估指标
 *
 * ## event类型
 * - error
 *    - 回调传参
 *    ```json
 *    {
 *      "name": "createRecord",
 *      "msg": "some meaagse",
 *      "data": {}
 *    }
 *    ```
 *    - createRecord
 *    - addNewAlgorithm
 *    - reEvaluation
 * - success
 *    - 回调传参
 *    ```json
 *    {
 *      "name": "createRecord",
 *      "msg": "some meaagse",
 *      "data": {}
 *    }
 *    ```
 *    - createRecord
 *    - addNewAlgorithm
 *    - reEvaluation
 * - update
 *    - 回调传参
 *    ```json
 *    {
 *      "name": "medal",
 *      "data": [] // or {}
 *    }
 *    ```
 *    - medal []
 *    - record []
 *    - algorithmTypeList {value: String || Number, data: []}
 *    - evaluationMetricList {value: String || Number, data: []}
 *    - algorithmList []
 *    - recordDetail {data: [], evaluationMetricList: []}
 */
class RankingManager extends EventManager {
  constructor() {
    super()

    /**
     * 当前选择的故障类型
     */
    this.algorithmType = -1

    /**
     * 当前选择的评估指标
     */
    this.evaluationMetric = -1

    /**
     * 评估指标列表 服务器获取
     */
    this.evaluationMetricList = []

    /**
     * 故障类型列表 服务器获取
     */
    this.algorithmTypeList = []

    /**
     * 算法列表 服务器获取
     */
    this.algorithmList = []

    /**
     * 数据图 减少查询次数 key = algorithmType | value = list
     */
    this.medalsMap = new LRUCache()

    /**
     * 数据集细则表数据图 减少查询次数 key = algorithmType | value = list
     */
    this.recordsMap = new LRUCache()

    /**
     * 数据集细则表详细数据图 减少查询次数 key = recordId | value = list
     */
    this.recordsDetailMap = new LRUCache()

    /**
     * medal 获取函数 async
     */
    this.queryMedalData = this.getData(getAllMedals, this.medalsMap)

    /**
     * record 获取函数 async
     */
    this.queryRecordData = this.getData(getAllRecords, this.recordsMap, null, (item, params) => {
      item.recordId = item.record_id
      item.algorithmList = item.algorithm_list
      item.algorithmType = params.algorithm_type
      item.algorithmTypeName = this.getAlgorithmTypeName(params.algorithm_type)
      return item
    })

    /**
     * recordDetail 获取函数 async
     */
    this.queryRecordDetailData = this.getData(queryRecordDetailData, this.recordsDetailMap)
  }

  /**
   * 外部需要渲染数据
   *
   * ***外部* 调用此函数时应该确保所有的事件均绑定完毕**
   */
  async render() {
    await this.getAllBaseData()
    await this.queryAlgorithmListData()
    console.log('data update')
    this.dataUpdate()
  }

  /**
   * 设置算法类型
   * @param {Number} algorithmType 算法类型
   * @returns none
   */
  setAlgorithmType(algorithmType) {
    console.log(algorithmType)
    this.algorithmType = algorithmType
    // 数据更新
    this.dataUpdate()
  }

  /**
   * 设置评估指标
   * @param {Number} evaluationMetric 设置评估指标
   * @returns none
   */
  setEvaluationMetric(evaluationMetric) {
    if (evaluationMetric === this.evaluationMetric) return
    this.evaluationMetric = evaluationMetric
    // 数据更新
    this.dataUpdate()
  }

  /**
   * 数据更新 认为基础数据都获取完毕
   *
   * **数据更新是异步函数，但是由于是通过事件更新数据，所以是同步函数**
   *
   * @param {Boolean} queryMedals 是否强制检索Medals 默认false
   * @param {Boolean} queryRecords 是否强制检索Records 默认false
   */
  dataUpdate(queryMedals = false, queryRecords = false) {
    // evaluationMetric update
    this.getEvaluationMetricList(null, true)
    // medal update
    // this.updateAllMedals(queryMedals)
    // record update
    this.updateAllRecords(queryRecords)
  }

  /**
   * 细则表新建记录
   * @param {Number} algorithmType 算法类型
   * @param {String} dataSet 数据集名字 starttime_endtime
   * @param {Array} algorithmList 算法id列表
   * @param {Array} evaluationMetricList 评估指标列表
   */
  createRecord(algorithmType, dataSet, algorithmList) {
    createRecord({
      algorithm_type: algorithmType,
      dataset: dataSet,
      algorithm_list: algorithmList
    }).then((res) => {
      this.trigger('success', {
        name: 'createRecord',
        msg: '',
        data: res
      })
    }).catch((err) => {
      this.trigger('error', {
        name: 'createRecord',
        msg: '',
        data: err
      })
    })
  }

  /**
   * 往记录内部增加算法
   * @param {Number} recordId 记录id
   * @param {Array} algorithmList 算法id列表
   */
  addNewAlgorithm(recordId, algorithmList) {
    addNewAlgorithm({
      record_id: recordId,
      algorithm_list: algorithmList
    }).then((res) => {
      this.trigger('success', {
        name: 'addNewAlgorithm',
        msg: '',
        data: {
          res: res,
          recordId: recordId
        }
      })
    }).catch((err) => {
      this.trigger('error', {
        name: 'addNewAlgorithm',
        msg: '',
        data: {
          err: err,
          recordId: recordId
        }
      })
    })
  }

  reEvaluation(recordId, algorithm) {
    reEvaluation({
      record_id: recordId,
      algorithm: algorithm
    }).then((res) => {
      this.trigger('success', {
        name: 'reEvaluation',
        msg: '',
        data: res
      })
    }).catch((err) => {
      this.trigger('error', {
        name: 'reEvaluation',
        msg: '',
        data: err
      })
    })
  }

  /**
   * 根据record id清空对应数据（为了刷新数据）
   * @param {Number} recordId record id
   * @returns 清空情况
   */
  clearRecordDetailById(recordId) {
    return this.recordsDetailMap.delete(recordId)
  }

  /**
   * 获取评估指标列表
   * @param {String} algorithmTypeName 算法类型 默认null 代表采用类当前算法类型（**不是算法类型id**）（理论上类的算法类型应该与组件统一）
   * @param {Boolean} event 是否发送事件 默认false
   * @returns value:evaluationMetric, data: evaluationMetricList
   */
  getEvaluationMetricList(algorithmTypeName = null, event = false) {
    algorithmTypeName = algorithmTypeName || this.algorithmTypeList.find((item) => item.id === this.algorithmType).algorithmTypeName
    const evaluationMetric = this.evaluationMetric
    const res = this.evaluationMetricList.filter((item) => item.algorithmType === algorithmTypeName)
    if (res.find((item) => item.id === evaluationMetric) === undefined) this.evaluationMetric = res.length > 0 ? res[0].id : -1
    if (event) {
      this.trigger('update', {
        name: 'evaluationMetricList',
        data: {
          value: this.evaluationMetric,
          data: res
        }
      })
    }
    return {
      value: this.evaluationMetric,
      data: res
    }
  }

  /**
   * 查询记录(页面的查看详情) 通过事件回传记录数据
   * @param {Number} recordId record id
   * @param {String} algorithmTypeName 算法类型名称（record id对应的算法类型）
   * @param {Boolean} event 是否发送事件 默认true
   * @param {Boolean} query 是否强制查询 默认false
   * @returns data, evaluationMetricList, recordId
   */
  async getRecordDetailData(recordId, algorithmTypeName = null, event = true, query = false) {
    if (query || !this.recordsDetailMap.has(recordId)) {
      const data = await this.queryRecordDetailData({
        record_id: recordId
      }, recordId, query).then((res) => {
        return res
      }).catch((err) => {
        console.log(err)
        return null
      })
      console.log('getRecordDetailData', data)
      if (data) this.recordsDetailMap.set(recordId, data)
    }
    const data = this.recordsDetailMap.get(recordId)
    console.log('getRecordDetailData', data)
    if (Array.isArray(data)) {
      algorithmTypeName = algorithmTypeName || this.algorithmTypeList.find((item) => item.id === this.algorithmType).algorithmTypeName
      const evaluationMetricList = this.evaluationMetricList.filter((item) => item.algorithmType === algorithmTypeName)
      if (event) {
        this.trigger('update', {
          name: 'recordDetail',
          data: {
            data,
            evaluationMetricList,
            recordId,
            algorithmTypeName
          }
        })
      }
      return {
        data,
        evaluationMetricList,
        recordId,
        algorithmTypeName
      }
    }
    return {
      data: [],
      evaluationMetricList: [],
      recordId,
      algorithmTypeName
    }
  }

  /**
   * 获取algorithmTypeList
   * @returns algorithmTypeList
   */
  getAlgorithmTypeList() {
    return this.algorithmTypeList
  }

  /**
   * 根据算法id返回算法类型名字
   * @param {Number} algorithmType 算法id
   * @returns 算法类型名字
   */
  getAlgorithmTypeName(algorithmType = null) {
    const id = parseInt(algorithmType || this.algorithmType)
    return this.algorithmTypeList.find((item) => item.id === id).algorithmTypeName
  }

  /**
   * 根据算法id返回算法名字
   * @param {Number} algorithm 算法id
   * @returns 算法名字
   */
  getAlgorithmName(algorithm = null) {
    const id = parseInt(algorithm || -1)
    return this.algorithmList.find((item) => item.id === id).algorithmName
  }

  getAlgorithmList(algorithmTypeName = null) {
    algorithmTypeName = algorithmTypeName || this.algorithmTypeList.find((item) => item.id === this.algorithmType).algorithmTypeName
    return this.algorithmList.filter((item) => item.algorithmTypeName === algorithmTypeName)
  }

  /* <------------------------------- 上面是外部调用函数 -------------------------------> */

  /**
   * 1. 如果本地没有存储或者强制查询则向服务器查询算法类型
   * 2. 将查询的内容存储到数组中
   * 3. 通过信息传递给前端组件
   * @param {Boolean} event 是否发送事件 默认true
   * @param {Boolean} query 是否强制查询 默认false
   * @returns value: this.algorithmType, data: this.algorithmTypeList
   */
  async queryAlgorithmType(event = true, query = false) {
    if (query || this.algorithmTypeList.length === 0) {
      const list = await getAlgorithmType().then((res) => {
        res.forEach((item) => {
          item.algorithmTypeName = item.algorithm_type_name
        })
        return res
      }).catch((err) => {
        console.log(err)
        return []
      })
      this.algorithmTypeList = list
      if (this.algorithmTypeList.length > 0 && this.algorithmType === -1) {
        this.algorithmType = this.algorithmTypeList[0].id
      }
    }
    if (event) {
      this.trigger('update', {
        name: 'algorithmTypeList',
        data: {
          value: this.algorithmType,
          data: this.algorithmTypeList
        }
      })
    }
    return {
      value: this.algorithmType,
      data: this.algorithmTypeList
    }
  }

  /**
   * 1. 如果本地没有存储或者强制查询则向服务器查询算法类型
   * 2. 将查询的内容存储到数组中
   * 3. 通过信息传递给前端组件
   * @param {Boolean} event 是否发送事件 默认true
   * @param {Boolean} query 是否强制查询 默认false
   * @returns evaluationMetricList
   */
  async queryEvaluationMetrics(event = true, query = false) {
    if (query || this.evaluationMetricList.length === 0) {
      const list = await getEvaluationMetrics().then((res) => {
        res.forEach((item) => {
          item.indicatorName = item.indicator_name
          item.algorithmType = item.algorithm_type
          item.formatJson = JSON.parse(item.format_json.replace(/'/g, '"'))
        })
        return res
      }).catch((err) => {
        console.log(err)
        return []
      })
      this.evaluationMetricList = list
      if (this.evaluationMetricList.length > 0 && this.evaluationMetric === -1) {
        this.evaluationMetric = this.evaluationMetricList[0].id
      }
    }
    if (event) {
      this.trigger('update', {
        name: 'evaluationMetricListFull',
        data: this.evaluationMetricList
      })
    }
    return this.evaluationMetricList
  }

  /**
   * 查询数据
   * @param {Function} api 接口函数
   * @param {Map} dataMap 数据图
   * @returns 查询函数
   */
  getData(api, dataMap, defaultData = [], func = null) {
    return async function(params, key, query = false) {
      if (!query && dataMap.has(key)) return dataMap.get(key)
      else {
        const data = await api(params).then((res) => func ? res.map((item) => func(item, params)) : res).catch((err) => {
          console.log(err)
          return null
        })
        if (data !== null) dataMap.set(key, data)
        return data || []
      }
    }
  }

  /**
   * 获取算法列表数据
   *
   * 此处会根据算法类型一次性获取全部算法（不理解为什么不把所有的算法一次性返回给我
   *
   *
   * **依赖于algorithmTypeList**
   */
  async queryAlgorithmListData(event = true, query = false) {
    if (this.algorithmTypeList.length === 0) return
    if (query || this.algorithmList.length === 0) {
      const algorithmTypeList = this.algorithmTypeList
      const list = algorithmTypeList.map((algorithmType) => {
        return getAlgorithms({
          algorithm_type: algorithmType.id
        }).then((res) => {
          res.forEach((item) => {
            item.algorithmName = item.algorithm_name
          })
          return res
        }).catch(err => {
          console.log(err)
          return []
        })
      })
      const algorithmList = await Promise.all(list)
      const res = []
      algorithmList.forEach((algorithms, i) => {
        algorithms.forEach((algorithm) => {
          algorithm.algorithmTypeId = algorithmTypeList[i].id
          algorithm.algorithmTypeName = algorithmTypeList[i].algorithmTypeName
          res.push(algorithm)
        })
      })
      this.algorithmList = res
    }
    if (event) {
      this.trigger('update', {
        name: 'algorithmList',
        data: this.algorithmList
      })
    }
    return this.algorithmList
  }

  /**
   * 获取全部的基础数据
   * - get_evaluation_metrics
   * - get_failure_type
   * - get_algorithms
   */
  getAllBaseData() {
    return Promise.all([
      this.queryEvaluationMetrics(),
      this.queryAlgorithmType()
    ])
  }

  /**
   * **依赖于algorithmTypeList**
   *
   * 更新medal数据到图中
   */
  async updateAllMedals(query = false) {
    if (this.algorithmTypeList.length === 0) return
    const algorithmType = this.algorithmType
    const data = await this.queryMedalData({
      algorithm_type: algorithmType
    }, algorithmType, query)
    const showData = this.filterDetailMedalsAndSort(data)
    // 触发更新事件
    this.trigger('update', {
      name: 'medal',
      data: showData
    })
  }

  /**
   * **依赖于evaluationMetricList**
   *
   * 筛选并且排序
   */
  filterDetailMedalsAndSort(data) {
    if (this.evaluationMetricList.length === 0) return []
    const evaluationMetric = this.evaluationMetricList.find((item) => item.id === this.evaluationMetric).indicatorName
    const showData = data.filter((item) => this.algorithmList.find((item_) => item_.algorithmName === item.algorithm).algorithmTypeId === this.algorithmType).map((item) => {
      return {
        algorithm: item.algorithm,
        gold: item[evaluationMetric].gold,
        silver: item[evaluationMetric].silver,
        copper: item[evaluationMetric].copper,
        strawberry: item[evaluationMetric].strawberry,
        total: item[evaluationMetric].total
      }
    })
    showData.sort((a, b) => b.total - a.total)
    return showData
  }

  /**
   * **依赖于algorithmTypeList**
   *
   * 更新record数据到图中
   */
  async updateAllRecords(query = false) {
    if (this.algorithmTypeList.length === 0) return
    const algorithmType = this.algorithmType
    const data = await this.queryRecordData({
      algorithm_type: algorithmType
    }, algorithmType, query)
    this.trigger('update', {
      name: 'record',
      data: data
    })
  }
}

/**
 * 单例
 */
const rankingManager = new RankingManager()

export default rankingManager
