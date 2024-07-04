<template>
  <el-card
    style="width: 480px; margin: 10px; height: auto"
    shadow="hover"
  >
    <template #header>
      <div class="MC__header">
        <h3 style="margin-block: 0em; text-align: left">{{ name }}</h3>
        <div>
          <el-button
            :title="$t('button.synchronization')"
            circle
            icon="el-icon-upload"
            size="mini"
            @click="syncTime"
          />
          <el-button
            :title="$t('button.delete')"
            type="danger"
            circle
            icon="el-icon-error"
            size="mini"
            @click="hideCard"
          />
        </div>
      </div>
    </template>
    <div class="MC__container">
      <div class="MC__controller">
        <el-button-group size="mini">
          <el-button
            :disabled="timeListIndex === 0"
            type="primary"
            icon="el-icon-minus"
            size="mini"
            @click="changeTLI(-1)"
          />
          <el-button
            disabled
            style="width: 40px;padding-left: 0px;padding-right: 0px;"
            size="mini"
          >
            {{ timeList[timeListIndex][0] }}
          </el-button>
          <el-button
            :disabled="timeListIndex === timeList.length - 1"
            type="primary"
            icon="el-icon-plus"
            size="mini"
            @click="changeTLI(1)"
          />
        </el-button-group>
        <el-date-picker
          v-model="datetime"
          :picker-options="pickerOptions"
          :disabled-date="judge"
          size="mini"
          type="datetime"
          placeholder="Select date and time"
        />
      </div>
      <main>
        <div
          ref="chart"
          class="line-chart"
        />
      </main>
    </div>
  </el-card>
</template>

<script>// UploadFilled DeleteFilled
import * as echarts from 'echarts'
import { debounce, message } from '@/utils/utils'
import { getMetric } from '@/network/api/metric'
// import { metricChartData } from '@/utils/test'
export default {
  props: {
    name: {
      type: String,
      default: ''
    },
    pod: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      chart: null,
      datetime: new Date(),
      timeList: [
        ['1s', 1000 * 1],
        ['10s', 1000 * 10],
        ['1m', 1000 * 60],
        ['5m', 1000 * 60 * 5],
        ['15m', 1000 * 60 * 15],
        ['30m', 1000 * 60 * 30],
        ['1h', 1000 * 60 * 60],
        ['2h', 1000 * 60 * 60 * 2],
        ['6h', 1000 * 60 * 60 * 6],
        ['12h', 1000 * 60 * 60 * 12],
        ['1d', 1000 * 60 * 60 * 24],
        ['2d', 1000 * 60 * 60 * 24 * 2]
      ],
      timeListIndex: 4,
      debounceSearchData: null,
      chartData: [],
      pickerOptions: {
        disabledDate(time) {
          const curDate = (new Date()).getTime()
          const three = 14 * 24 * 3600 * 1000
          const threeMonths = curDate - three
          return time.getTime() > Date.now() || time.getTime() < threeMonths
        },
        shortcuts: [{
          text: this.$t('dataMonitor.oneMinute'),
          onClick(picker) {
            const end = new Date()
            const start = new Date()
            start.setTime(start.getTime() - 1000 * 60 * 1)
            picker.$emit('pick', [start, end])
          }
        }, {
          text: this.$t('dataMonitor.fiveMinute'),
          onClick(picker) {
            const end = new Date()
            const start = new Date()
            start.setTime(start.getTime() - 1000 * 60 * 5)
            picker.$emit('pick', [start, end])
          }
        }, {
          text: this.$t('dataMonitor.fifteenMinute'),
          onClick(picker) {
            const end = new Date()
            const start = new Date()
            start.setTime(start.getTime() - 1000 * 60 * 15)
            picker.$emit('pick', [start, end])
          }
        }]
      }
    }
  },
  watch: {
    pod() {
      this.searchData()
    }
  },
  mounted() {
    this.debounceSearchData = debounce(this.searchData, 200)
    this.searchData()
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
    judge(date) {
      return date.getTime() > Date.now()
    },
    changeTLI(step) {
      this.timeListIndex += step
      this.debounceSearchData()
    },
    syncTime() {
      // 同步时间
      this.$emit('syncTime', {
        timeListIndex: this.timeListIndex,
        datetime: this.datetime
      })
    },
    hideCard() {
      // 隐藏卡片
      this.$emit('hideCard', this.name)
    },
    receiveTime(time) {
      // 接收时间
      if (this.timeListIndex === time.timeListIndex && this.datetime === time.datetime) return
      this.timeListIndex = time.timeListIndex
      this.datetime = time.datetime
      this.searchData()
    },
    getDuration() {
      return [this.datetime.getTime() - this.timeList[this.timeListIndex][1], this.datetime.getTime()]
    },
    searchData() {
      const duration = this.timeList[this.timeListIndex][1]
      const startTime = this.datetime.getTime() - duration
      const endTime = this.datetime.getTime()
      getMetric({
        pod: this.pod,
        metric_name: this.name,
        start_time: parseInt(startTime / 1000),
        end_time: parseInt(endTime / 1000)
      }).then((res) => {
        if (Array.isArray(res)) {
          this.chartData = res
          this.draw()
        } else {
          throw new Error(res.error)
        }
      }).catch((err) => {
        this.chartData = []
        this.draw()
        message(err.message)
      })
    },
    draw() {
      if (!this.$refs.chart) return
      const chart = this.chart || echarts.init(this.$refs.chart)
      // const dataZoomStart = chart._model ? chart._model.option.dataZoom[0].start : 0
      // const dataZoomEnd = chart._model ? chart._model.option.dataZoom[0].end : 100
      const option = {
        title: {
          text: this.title,
          subtext: this.subtext,
          textStyle: {
            fontWeight: 'normal',
            fontSize: 20,
            color: '#90979c'
          },
          x: 'center'
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            lineStyle: {
              color: '#57617B'
            }
          }
        },
        grid: {
          left: '80px',
          right: '80px'
        },
        xAxis: {
          type: 'time',
          name: this.xName,
          boundaryGap: false,
          axisLine: {
            lineStyle: {
              color: '#57617B'
            }
          },
          splitLine: {
            show: false
          },
          axisLabel: {
            rotate: 40
          }
        },
        yAxis: {
          type: 'value',
          name: this.yName,
          axisTick: {
            show: false
          },
          axisLine: {
            lineStyle: {
              color: '#57617B'
            }
          },
          axisLabel: {
            margin: 10,
            textStyle: {
              fontSize: 14
            }
          },
          splitLine: {
            lineStyle: {
              type: 'dashed' // 设置为虚线
            }
          }
        },
        series: [
          {
            type: 'line',
            showSymbol: false,
            color: '#1890FF',
            lineStyle: {
              normal: {
                width: 1
              }
            },
            data: this.chartData.map((item) => ({
              name: item.time,
              value: [item.time, item.value]
            }))
          }
        ]
      }
      chart.setOption(option)
      this.chart = chart
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
.MC__header {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.MC__header > div {
  width: 100px;
  display: flex;
  justify-content: flex-end;
}
.MC__header > h3 {
  width: calc(100% - 100px);
  max-width: 100%;
  overflow: hidden;
}
.MC__header > h3:hover {
  overflow: auto;
}
.MC__header-close {
  cursor: pointer;
  position: absolute;
  font-size: 22px;
  top: -15px;
  right: -15px;
}
.MC__controller {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.line-chart {
  width: 100%;
  height: 400px;
}
</style>
