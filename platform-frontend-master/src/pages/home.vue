<!-- 主页-->
<template>
  <structure1>
    <template #card-l-1>
      <div class="card-title">
        <span>{{ $t("header.rightName1") }}</span>
      </div>
      <littleCalendar/>
    </template>
    <template #card-l-2>
      <div class="card-title">
        <span>{{ $t("header.rightName2") }}</span>
      </div>
      <dataShower/>
    </template>
    <template #card-r-1>
      <calendar/>
    </template>
  </structure1>
</template>

<script>
import structure1 from '@/components/structure/structure1.vue'
import calendar from '@/components/calendar/index.vue'
import littleCalendar from '@/components/littleCalendar/index.vue'
import dataShower from '@/components/dataShower/index.vue'
export default {
  name: 'HomePage',
  components: {
    structure1,
    calendar,
    littleCalendar,
    dataShower
  },
  data() {
    return {
      rightName1:'查看日期',
      rightName2:'最近历史记录'
    }
  },
  mounted() {

  },
  methods: {

  }

}
</script>

<style scoped>

</style>
