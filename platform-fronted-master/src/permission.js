import router, { asyncRoutes } from './router'
import { userStore, UserUtils } from './store/user'
import { Message } from 'element-ui'

function hasPermission(permissions, route) {
  if (route.permissions) {
    return permissions.some(permission => route.permissions.includes(permission))
  } else {
    return true
  }
}

function filterAsyncRoutes(routes, permissions) {
  const res = []

  routes.forEach(route => {
    const tmp = { ...route }
    if (hasPermission(permissions, tmp)) {
      if (tmp.children) {
        tmp.children = filterAsyncRoutes(tmp.children, permissions)
      }
      res.push(tmp)
    }
  })

  return res
}

const whiteList = ['/login', '/reg', '/pwdReset'] // no redirect whitelist

const getRedirectPath = (route) => {
  let str = route.path
  // 参数处理
  if (route.query) {
    const query = Object.keys(route.query).map(key => `${key}=${route.query[key]}`).join('&')
    if (query) {
      str += `?${query}`
    }
  }
  return str
}

router.beforeEach(async(to, from, next) => {
  const loginInfo = localStorage.getItem('token')
  if (loginInfo) {
    next()
  } else {
    /* not logged in */
    if (whiteList.indexOf(to.path) !== -1) {
      next()
    } else {
      // other pages that do not have permission to access are redirected to the login page.
      Message.error('请先登录')
      next(`/login?redirect=${getRedirectPath(to)}`)
    }
  }
})
