const getters = {
  sidebar: (state) => state.app.sidebar,
  device: (state) => state.app.device,
  token: (state) => state.user.token,
  avatar: (state) => state.user.avatar,
  ownRoles: state => state.user.ownRoles,
  name: (state) => state.user.name,
  asyncRoutes: (state) => state.routes.asyncRoutes,
  hasLoadRoute: (state) => state.routes.hasLoadRoute
}
export default getters
