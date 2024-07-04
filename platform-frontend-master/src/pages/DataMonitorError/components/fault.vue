<template>
  <calendar page="dataMonitor"/>
</template>

<script>
import calendar from '@/components/calendar/index.vue'
export default {
  name: 'Fault',
  components: {
    calendar
  },
  props: ['time', 'activeName']
}
</script>

<style>

</style>
