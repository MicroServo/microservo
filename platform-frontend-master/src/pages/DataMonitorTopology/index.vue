<template>
  <structure4>
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
      <div class="DMT-card-r-1">
        <header>
          <CardTitle>
            {{ $t('dataMonitor.diagram') }}
          </CardTitle>
        </header>
        <main>
          <TraceTopology />
        </main>
      </div>
    </template>
  </structure4>
</template>

<script>
import structure4 from '@/components/structure/structure4.vue'
import TraceTopology from '@/components/TraceTopology'
import CardTitle from '@/components/CardTitle'
export default {
  components: {
    structure4,
    TraceTopology,
    CardTitle
  },
  data() {
    return {
      leftRouteList: [
        {
          name: this.$t('dataMonitor.topology'),
          path: '/dataMonitor/topology',
          routeName: 'topology'
        },
        {
          name: this.$t('dataMonitor.faultData'),
          path: '/dataMonitor/error',
          routeName: 'error'
        }
      ]
    }
  }
}
</script>

<style>
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
.nav{
  color: #374E5C;
  text-decoration: none;
  margin: 0;
  text-align: left;
  padding: 10px;
  font-size: 14px;
  cursor: pointer;
}
.nav:hover{
  color: #00A0FF;
}
.navSelect{
  color: #00A0FF;
  background-color: #E5F5FF;
}
</style>
