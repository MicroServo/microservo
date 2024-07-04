import request from '@/utils/request'

export function getEvaluationMetrics() {
  return request({
    url: '/indicators/fetch',
    method: 'get'
  })
}

export function getAlgorithmType() {
  return request({
    url: '/algorithm/fetchalgorithmtype',
    method: 'get'
  })
}

export function getAlgorithms(params) {
  return request({
    url: '/leaderboard/getalgorithms',
    method: 'get',
    params
  })
}

export function getAllMedals(params) {
  return request({
    url: '/leaderboard/getallmedals',
    method: 'get',
    params
  })
}

export function getAllRecords(params) {
  return request({
    url: '/leaderboard/getallrecords',
    method: 'get',
    params
  })
}

export function createRecord(params) {
  return request({
    url: '/leaderboard/createrecord',
    method: 'get',
    params
  })
}

export function addNewAlgorithm(params) {
  return request({
    url: '/leaderboard/addnewalgorithm',
    method: 'get',
    params
  })
}

export function queryRecordDetailData(params) {
  return request({
    url: '/leaderboard/queryrecorddata',
    method: 'get',
    params
  })
}

export function reEvaluation(params) {
  return request({
    url: '/leaderboard/reevaluation',
    method: 'get',
    params
  })
}
