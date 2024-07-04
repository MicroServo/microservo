<template>
  <structure1 ref="structure">
    <template #card-l-1>
      <div class="card-title">
        <span>{{ $t("header.rightName1") }}</span>
      </div>
      <littleCalendar/>
    </template>
    <template #card-l-2>
      <div class="card-title">
        <span>{{ $t("fault.addFault") }}</span>
      </div>
      <faultTable
        :fault-list="faultList"
        @addFault="addFault"/>
    </template>
    <template #card-r-1>
      <faultList
        v-if="show === 'table'"
        :fault-list="faultList"
        @changeDataShower="changeDataShower"/>
      <calendar
        v-if="show === 'list'"
        page="faultInjection"
        @changeDataShower="changeDataShower"/>
    </template>
    <template #shadow>
      <addFault
        ref="addFault"
        :type="type"
        @finish="finish"/>
    </template>
  </structure1>
</template>

<script>
import structure1 from '@/components/structure/structure1.vue'
import littleCalendar from '@/components/littleCalendar/index.vue'
import faultTable from '@/components/faultTable/index.vue'
import addFault from '@/components/addFault/index.vue'
import faultList from '@/components/faultList/index.vue'
import calendar from '@/components/calendar/index.vue'
export default {
  name: 'FaultInjection',
  components: {
    structure1,
    littleCalendar,
    faultTable,
    addFault,
    faultList,
    calendar
  },
  data() {
    return {
      faultList: [{
        type: 'http',
        faultType: 'http',
        name: 'http',
        contain: ['http-delay', 'http-abort']
      },
      {
        type: 'net',
        faultType: 'network',
        name: 'network',
        contain: ['network-loss', 'network-delay']
      },
      {
        type: 'stress',
        faultType: 'stress',
        name: 'stress',
        contain: ['cpu', 'memory']
      },
      {
        type: 'pod',
        faultType: 'pod',
        name: 'pod',
        contain: ['pod']
      }],
      show: 'list',
      type: ''
    }
  },
  mounted() {
    //
  },
  methods: {
    addFault(data) {
      this.type = data.type.faultType
      this.$refs.structure.shadowEnter()
      // this.$refs.addFault.setData(data)
    },
    finish() {
      this.$refs.structure.shadowLeave()
    },
    changeDataShower(type) {
      this.show = type
    }
  }

}
</script>

<style scoped>

</style>
