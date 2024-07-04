<template>
  <div class="DME-log">
    <header>
      <span
        v-for="(item, i) in list"
        :key="i"
        :class="{'DME-log__header-select--active': item.show}"
        O-B
        class="DME-log__header-select"
        @click="selectClick(i)"
      >
        <span>{{ $t(item.name ) }}</span>
      </span>
    </header>
    <main>
      <LogAmountShower v-show="list[0].show" />
      <LogQueryAndExport v-show="list[1].show" />
    </main>
  </div>
</template>

<script>
import LogAmountShower from '@/components/LogAmountShower'
import LogQueryAndExport from '@/components/LogQueryAndExport'
export default {
  components: {
    LogAmountShower,
    LogQueryAndExport
  },
  data() {
    return {
      list: [{
        name: this.$t('dataMonitor.numDisplay'),
        show: true
      },
      {
        name: this.$t('dataMonitor.qAndE'),
        show: false
      }]
    }
  },
  methods: {
    selectClick(index) {
      if (this.list[index].show) return
      this.list.forEach((item, i) => {
        item.show = false
        if (index === i) item.show = true
      })
    }
  }
}
</script>

<style>
.DME-log {
  height: 100%;
}
.DME-log > header {
  text-align: left;
  height: 34px;
}
.DME-log > header * {
  transition: .3s;
}
.DME-log > main {
  height: calc(100% - 34px);
}
.DME-log__header-select {
  position: relative;
  cursor: pointer;
  display: inline-block;
  padding: 0px 10px;
  color: #A5B7C1;
}
.DME-log__header-select > span {
  position: relative;
  display: inline-block;
  padding: 5px 0px;
}
.DME-log__header-select > span::after {
  content: ' ';
  width: 100%;
  height: 2px;
  position: absolute;
  left: 0;
  bottom: 0;
  transition: .3s;
}
.DME-log__header-select--active {
  color: #374E5C;
}
.DME-log__header-select--active > span::after {
  background-color: #00A0FF;
  transition: .3s;
}
.log-num{
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
