<template>
  <structure5>
    <!-- 这里使用了router-link实现页面的跳转 ， 并且为了样式修改使用了没有触发事件的el-button -->
    <template #card-l-1>
      <div class="DMT-card-l-1">
        <router-link
          v-for="(route, i) in leftRouteList"
          :key="i"
          :class="{'DMT-card-l-1__link--selected': $route.meta.DMETLName === route.routeName}"
          :to="route.path"
          class="link DMT-card-l-1__link"
          o-r
        >
          {{ route.name }}
        </router-link>
      </div>
    </template>
    <template #card-r-1>
      <router-view/>
    </template>
  </structure5>
</template>

<script>
import structure5 from '@/components/structure/structure5.vue'
export default {
  name: 'UserManagement',
  components: {
    structure5
  },
  data() {
    return {
      path: 'user',
      leftRouteList: [
        {
          name: '用户管理',
          path: '/userManagement/user',
          routeName: 'user'
        },
        {
          name: '角色管理',
          path: '/userManagement/role',
          routeName: 'role'
        }
      ]
    }
  },
  mounted() {

  },
  methods: {
    goRouter(value) {
      this.path = value
      const path = '/userManagement/' + value
      this.$router.push(path)
    }
  }

}
</script>

<style scoped>
.DMT-card-l-1__link {
  position: relative;
  text-align: left;
  display: block;
  color: #374E5C;
  padding: 2px 5px;
  font-size: 14px;
  transition: .3s;
  z-index: 1;
}
.DMT-card-l-1__link::after {
  position: absolute;
  left: 0;
  top: 0;
  transform: translateX(-5px);
  width: calc(100% + 5px * 2);
  height: 100%;
  content: ' ';
  background: #e5f5ff00;
  z-index: -1;
  transition: .3s;
}
.DMT-card-l-1__link:hover,
.DMT-card-l-1__link--selected {
  transition: .3s;
  color: #00A0FF;
}
.DMT-card-l-1__link:hover::after,
.DMT-card-l-1__link--selected::after {
  transition: .3s;
  background: #E5F5FF;
}
.DMT-card-r-1 {
  width: 100%;
  height: 100%;
}
.DMT-card-r-1  > header{
  height: 30px;
  display: flex;
  align-items: center;
}
.DMT-card-r-1  > main {
  height: calc(100% - 30px);
}
</style>
