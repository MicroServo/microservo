<!--
 * @FileDescription
 * 根据路由动态面包屑
 * @Author
 * Wen Long
 * @Date
 * 2024/4/2
 * @LastEditors
 * Wen Long
 * @LastEditTime
 * 2024/4/2
 -->
<template>
  <div class="breadcrumb">
    <div
      v-for="(d, i) in data"
      :key="i">
      <router-link :to="d.path">{{ d.breadcrumb }}</router-link>
      <span v-if="i !== data.length - 1">></span>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    lang: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      data: []
    }
  },
  watch: {
    $route(to, from) {
      this.updateData()
    },
    lang(newVal, oldVal) {
      console.log(newVal)
      this.lang = newVal
      this.updateData()
    }
  },
  mounted() {
    this.updateData()
  },
  methods: {
    updateData() {
      const currentRoute = this.$route
      // 获取之前路由上设置的meta
      const matchedRoutes = currentRoute.matched
      console.log(matchedRoutes)
      const data = []
      matchedRoutes.forEach(route => {
        // 获取每一个路由记录的meta信息
        const meta = route.meta
        const lang = localStorage.getItem('lang')
        if (lang === 'zh') {
          data.push({
            breadcrumb: meta.breadcrumb === null || meta.breadcrumb === undefined ? null : meta.breadcrumb,
            path: route.path
          })
        } else {
          data.push({
            breadcrumb: meta.en === null || meta.en === undefined ? null : meta.en,
            path: route.path
          })
        }
      })
      this.data = data.filter((ele) => ele.breadcrumb !== null)
      if (this.data.length > 0) {
        this.data.unshift({
          breadcrumb:  this.$t('menu.name'),
          path: '/home'
        })
      }
    }
  }
}
</script>

<style scoped>
.breadcrumb {
  display: flex;
  justify-content: start;
  align-items: center;
}
.breadcrumb > div > span {
  padding: 0px 5px;
  color: #748C9A;
}
a {
  font-family: OPPOSans, OPPOSans;
  font-weight: normal;
  font-size: 14px;
  color: #748C9A;
  line-height: 18px;
  text-align: left;
  text-decoration: none;
}
a:hover {
  color: #748C9A;
  text-decoration: none;
}
</style>
