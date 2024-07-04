import router from '@/router'
import axios from 'axios'

export const userStore = {
  roles: [],
  permissions: []
}

export const UserUtils = {

  checkLogin() {
    return localStorage.getItem('user') != null && localStorage.getItem('token') != null
  },

  resetUserStore() {
    userStore.roles = []
    userStore.permissions = []
    localStorage.removeItem('user')
    localStorage.removeItem('token')
  },

  logout() {
    return new Promise((resolve, reject) => {
      axios.post('display/user/logout').then(response => {
        UserUtils.resetUserStore()
        const path = router.app.$route.path
        if (path === '/' || path === '/home') {
          location.reload()
        } else {
          router.push({ path: '/home' })
        }
        resolve(response)
      }).catch(error => {
        reject(error)
      })
    })
  }
}

export const hasPermission = (permissions) => {
  if (Array.isArray(permissions)) {
    return permissions.some(permission => userStore.permissions.includes(permission))
  } else {
    return userStore.permissions.includes(permissions)
  }
}
