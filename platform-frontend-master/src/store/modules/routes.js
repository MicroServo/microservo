import { getAuthorityDict } from '@/assets/js/user'

const state = {
  hasLoadRoute: false,
  asyncRoutes: []
}

const actions = {
  /**
   * @description
   * return dynamic routes
   * @returns {[{routes}]} dynamic routes
   */
  async createRoutes() {
    // getAuthorityDict
    await getAuthorityDict()
      .then((data) => {
        // return
        const authorityDict = data
        const routes = asyncRoutes.filter((item) => !item.name || authorityDict[item.name])
        state.asyncRoutes = routes
        state.hasLoadRoute = true
      })
      .catch(() => {
        console.log('net error')
      })
  }
}

export default {
  namespaced: true,
  state,
  actions
}
