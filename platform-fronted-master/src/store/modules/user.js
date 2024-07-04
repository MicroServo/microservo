import { login, logout, getInfo } from '@/assets/js/user'
import { updateUser } from '@/assets/js/manage'
import { getToken, setToken, removeToken } from '@/utils/auth'

const getDefaultState = () => {
  return {
    token: getToken(),
    name: '',
    avatar: 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
    ownRoles: []
  }
}

const state = getDefaultState()

const mutations = {
  RESET_STATE: (state) => {
    Object.assign(state, getDefaultState())
  },
  SET_TOKEN: (state, token) => {
    state.token = token
  },
  SET_NAME: (state, name) => {
    state.name = name
  },
  SET_AVATAR: (state, avatar) => {
    state.avatar = avatar
  },
  SET_OWN_ROLES: (state, ownRoles) => {
    state.ownRoles = ownRoles
  }
}

const actions = {
  // user login
  login({ commit }, userInfo) {
    const { username, password } = userInfo
    removeToken() // must remove  token  first
    // 请求
    return new Promise((resolve, reject) => {
      login({ username: username.trim(), password: password })
        .then((data) => {
          const { token } = data

          commit('SET_TOKEN', token)
          setToken(token)
          resolve()
        })
        .catch((error) => {
          reject(error)
        })
    })
  },

  // get user info
  getInfo({ commit, state }) {
    return new Promise((resolve, reject) => {
      setToken(getToken())
      getInfo()
        .then((data) => {
          if (!data) {
            return reject('Verification failed, please Login again.')
          }
          const { name, ownRoles } = data
          commit('SET_NAME', name)
          commit('SET_OWN_ROLES', ownRoles)
          resolve(data)
        })
        .catch((error) => {
          reject(error)
        })
    })
  },

  // update user info
  updateInfo({ state }, params) {
    return new Promise((resolve, reject) => {
      updateUser(params)
        .then((data) => {
          resolve(data)
        })
        .catch(() => {
          reject()
        })
    })
  },

  // user logout
  logout({ commit, state }) {
    return new Promise((resolve, reject) => {
      logout(state.token)
        .then(() => {
          removeToken() // must remove  token  first
          commit('RESET_STATE')
          resolve()
        })
        .catch((error) => {
          reject(error)
        })
    })
  },

  // remove token
  resetToken({ commit }) {
    return new Promise((resolve) => {
      removeToken() // must remove  token  first
      commit('RESET_STATE')
      resolve()
    })
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}
