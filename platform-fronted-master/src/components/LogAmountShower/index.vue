<template>
  <div class="log-amount-shower">
    <header>
      <el-radio-group
        v-model="selectType"
        @input="drawChart">
        <el-radio :label="1">{{ $t('dataMonitor.oneDay') }}</el-radio>
        <el-radio :label="2">{{ $t('dataMonitor.oneWeek') }}</el-radio>
        <el-radio :label="3">{{ $t('dataMonitor.twoWeek') }}</el-radio>
      </el-radio-group>
    </header>
    <div
      ref="chart"
      class="chart"/>
  </div>
</template>

<script>
import { getLogNum } from '@/network/api/log'
import { message } from '@/utils/utils'
import * as echarts from 'echarts'
export default {
  data() {
    return {
      chart: null,
      selectType: 1,
      id: ''
    }
  },
  computed: {
    logNum() {
      const m30 = 1000 * 60 * 30
      if (Date.now() - this.logNumMap.get('begin') > m30) {
        this.logNumMap.clear()
        this.logNumMap.set('begin', Date.now())
      }
      const st = this.selectType
      if (this.logNumMap.has(st)) return new Promise((resolve) => { resolve([this.logNumMap.get(st), this.id]) })
      else {
        return new Promise((resolve) => {
          getLogNum({
            time_select: st
          }).then((res) => {
            this.logNumMap.set(st, res)
            this.logNumMap.set('begin', Date.now())
            resolve([res, this.id])
          })
        })
      }
    },
    logNumMap() {
      if (!window.logNumMap) {
        window.logNumMap = new Map()
        window.logNumMap.set('begin', Date.now())
      }
      return window.logNumMap
    }
  },
  mounted() {
    this.drawChart()
    window.addEventListener('resize', this.resize)
  },
  beforeUnmount() {
    if (this.chart) {
      this.chart.dispose()
      this.chart = null
    }
    window.removeEventListener('resize', this.resize)
  },
  methods: {
    async drawChart() {
      if (!this.$refs.chart) return
      const loading = this.$loading({
        lock: true, // lock的修改符--默认是false
        text: 'loading', // 显示在加载图标下方的加载文案
        spinner: 'el-icon-loading', // 自定义加载图标类名
        background: 'white', // 遮罩层颜色
        target: document.querySelector('.chart') // loadin覆盖的dom元素节点
      })
      const id = parseInt(Math.random() * 1000000)
      this.id = id
      const data_ = await this.logNum
      const data = data_[0]
      if (data_[1] !== id) return
      if (this.chart) this.chart.dispose()
      const chart = echarts.init(this.$refs.chart)

      const x_data = data.map((item) => item.date)
      const y_data = data.map((item) => item.log_count)

      const option = {
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        grid: {
          containLabel: true
        },

        xAxis: {
          type: 'category',
          data: x_data,
          axisTick: {
            alignWithLabel: true
          }
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            name: 'Count',
            data: y_data,
            type: 'bar',
            itemStyle: {
              color: '#1E90FF'
            }
          }
        ]
      }
      chart.setOption(option)
      this.chart = chart
      loading.close()
    },
    resize() {
      if (this.chart) {
        this.chart.resize()
      }
    }
  }
}
</script>

<style>
.log-amount-shower,
.log-amount-shower > div {
  position: relative;
  width: 100%;
  height: 100%;
}
.log-amount-shower > header {
  position: absolute;
  right: 20px;
  bottom: 20px;
  z-index: 999;
}
</style>
