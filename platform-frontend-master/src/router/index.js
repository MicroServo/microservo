import Vue from 'vue'
import Router from 'vue-router'
import home from '@/pages/home.vue'
import UserManagement from '@/pages/UserManagement'
import userManage from '@/pages/UserManagement/components/userManage'
import roleManage from '@/pages/UserManagement/components/roleManage'
import AlgorithmManagement from '@/pages/AlgorithmManagement'
import AlgorithmTemplate from '@/pages/AlgorithmTemplate'
import DataMonitorError from '@/pages/DataMonitorError'
import DataMonitorTopology from '@/pages/DataMonitorTopology'
import EvaluateData from '@/pages/EvaluateData'
import EvaluateDataDetail from '@/pages/EvaluateData/EvaluateDataDetail'
import Rankings from '@/pages/Rankings'
import FaultInjection from '@/pages/FaultInjection'
import UserCenter from '@/pages/UserCenter'
import Login from '@/pages/Client/Login'
import Reg from '@/pages/Client/Reg'
import PwdReset from '@/pages/Client/PwdReset'
import fault from '@/pages/DataMonitorError/components/fault.vue'
import log from '@/pages/DataMonitorError/components/log.vue'
import metric from '@/pages/DataMonitorError/components/metric.vue'
import trace from '@/pages/DataMonitorError/components/trace.vue'
Vue.use(Router)

/**
 * breadcrumb设置为null或者不设置都不会显示
 * 当面包屑长度大于0时，前面会自动添加主页
 * breadcrumb设置你希望本页面显示的面包屑
 * breadcrumb会遍历你的父路由
 */
export default new Router({
  routes: [
    {
      path: '/',
      name: 'home',
      redirect: '/home',
      meta: {
        breadcrumb: null
      }
    },
    {
      name: 'home',
      path: '/home',
      component: home,
      meta: {
        breadcrumb: '主页',
        en: 'Homepage'
      }
    },
    {
      name: 'UserManagement',
      path: '/userManagement',
      redirect: '/userManagement/user',
      component: UserManagement,
      meta: {
        breadcrumb: '用户管理',
        en: 'User management'
      },
      children: [
        {
          path: 'user',
          name: 'user',
          component: userManage,
          meta: {
            breadcrumb: '用户列表',
            en: 'User list',
            DMETLName: 'user'
          }
        },
        {
          path: 'role',
          name: 'role',
          component: roleManage,
          meta: {
            breadcrumb: '角色列表',
            en: 'Role management',
            DMETLName: 'role'
          }
        }
      ]
    },
    {
      name: 'FaultInjection',
      path: '/faultInjection',
      component: FaultInjection,
      meta: {
        breadcrumb: '故障注入',
        en: 'FaultInjection'
      }
    },
    {
      name: 'AlgorithmManagement',
      path: '/algorithmManagement',
      component: AlgorithmManagement,
      meta: {
        breadcrumb: '算法管理',
        en: 'AlgorithmMarket'
      }
    },
    {
      name: 'AlgorithmTemplate',
      path: '/algorithmTemplate',
      component: AlgorithmTemplate,
      meta: {
        breadcrumb: '算法配置',
        en: 'Configuration'
      }
    },
    {
      name: 'DataMonitorTopology',
      path: '/dataMonitor/topology',
      component: DataMonitorTopology,
      meta: {
        breadcrumb: '拓扑',
        en: 'Topology',
        DMETLName: 'topology'
      }
    },
    {
      name: 'DataMonitorError',
      path: '/dataMonitor/error',
      redirect: '/dataMonitor/error/fault',
      component: DataMonitorError,
      meta: {
        breadcrumb: '故障数据',
        en: 'DataDisplay'
      },
      children: [
        {
          path: 'fault',
          name: 'fault',
          component: fault,
          meta: {
            breadcrumb: '故障',
            en: 'Fault',
            DMEName: 'fault',
            DMETLName: 'error'
          }
        },
        {
          path: 'log',
          name: 'log',
          component: log,
          meta: {
            breadcrumb: '日志',
            en: 'Log',
            DMEName: 'log',
            DMETLName: 'error'
          }
        },
        {
          path: 'metric',
          name: 'metric',
          component: metric,
          meta: {
            breadcrumb: '指标',
            en: 'Metric',
            DMEName: 'metric',
            DMETLName: 'error'
          }
        },
        {
          path: 'trace',
          name: 'trace',
          component: trace,
          meta: {
            breadcrumb: '调用链',
            en: 'Trace',
            DMEName: 'trace',
            DMETLName: 'error'
          }
        }
      ]
    },
    {
      name: 'DataMonitor',
      path: '/dataMonitor',
      redirect: '/dataMonitor/error/fault',
      meta: {
        breadcrumb: null
      }
    },
    {
      name: 'EvaluateData',
      path: '/evaluateData',
      component: EvaluateData,
      meta: {
        breadcrumb: '算法评估',
        en: 'Evaluation'
      },
      children:[
        {
          path: 'evaluateDataDetail',
          name: 'EvaluateDataDetail',
          component: EvaluateDataDetail,
          meta: {
            breadcrumb: '数据详情',
            en: 'Data details'
          }
        }
      ]
    },
    {
      name: 'Rankings',
      path: '/rankings',
      component: Rankings,
      meta: {
        breadcrumb: '排行榜',
        en: 'Leaderboard'
      }
    },
    {
      name: 'UserCenter',
      path: '/userCenter',
      component: UserCenter,
      meta: {
        breadcrumb: '用户中心',
        en: 'User Center'
      }
    },
    {
      name: 'Reg',
      path: '/reg',
      component: Reg,
      meta: {
        noHeader: true
      }
    },
    {
      name: 'Login',
      path: '/login',
      component: Login,
      meta: {
        noHeader: true
      }
    },
    {
      name: 'PwdReset',
      path: '/pwdReset',
      component: PwdReset,
      meta: {
        noHeader: true
      }
    }
  ]
})
