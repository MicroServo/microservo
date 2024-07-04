<template>
  <el-card
    ref="chartCard"
    class="chart-card"
    shadow="hover">
    <div class="card_header">
      <h3
        class="card_header_text"
        style="margin-block-start: 0em;">{{ name }}</h3>
      <el-button
        class="card_header_button_2"
        title="删除"
        icon="el-icon-delete"
        size="small"
        circle
        @click="hide"/>
      <el-button
        class="card_header_button_1"
        icon="el-icon-refresh"
        circle
        size="small"
        title="同步"
        @click="copyTime"/>

    </div>
    <div class="chart-control">
      <el-button-group class="chart-control__btn-group">
        <el-button
          :disabled="timeListIndex === 0"
          class="chart-mini-button_1"
          size="small"
          icon="el-icon-minus"
          @click="timeListIndex--"/>
        <el-button
          class="chart-mini-button"
          size="small"
          type="text"
          disabled
          style="width: 4em;">{{ timeList[timeListIndex][0] }}</el-button>
        <el-button
          :disabled="timeListIndex === timeList.length - 1"

          class="chart-mini-button_2"
          size="small"
          icon="el-icon-plus"
          @click="timeListIndex++"/>
      </el-button-group>
      <el-date-picker
        v-model="datetime"
        :picker-options="picherOptions"
        prefix-icon=""
        class="chart-date-picker"
        title="结束时间"
        type="datetime"
        size="small"
        placeholder="选择日期时间"
        @change="draw"/>
    </div>
    <div
      ref="chart"
      class="line-chart" />
    <div
      v-if="false"
      class="moving-helper"/>
  </el-card>
</template>

<script>
import { getMetric } from '@/network/api/metric'
import * as echarts from 'echarts'

export default {
  name: 'LineChart',
  props: {
    // data: {
    //   type: Array,
    //   // required: true,
    // },
    // xName: {
    //   type: String,
    //   default: '',
    // },
    // yName: {
    //   type: String,
    //   default: '',
    // },
    name: {
      type: String,
      default: ''
    },
    pod: {
      type: String,
      default: ''
    }
    // subtext: {
    //   type: String,
    //   default: '',
    // },
  },
  data() {
    return {
      chart: null,
      datetime: null,
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
      chartPod: this.pod,
      timer: null, // 节流计时器
      control: false,
      picherOptions: {
        disabledDate(date) {
          // disabledDate 文档上：设置禁用状态，参数为当前日期，要求返回 Boolean
          return (
            date.getTime() > Date.now()
          )
        }
      }
    }
  },
  watch: {
    timeListIndex(newValue, oldValue) {
      if (this.timer) clearTimeout(this.timer)
      this.timer = setTimeout(() => {
        if (this.control) this.control = false
        else this.draw()
      }, 200)
    }
  },
  mounted() {
    window.addEventListener('resize', this.resize)
    this.draw()
  },
  beforeDestroy() {
    if (this.chart) {
      this.chart.dispose()
      this.chart = null
    }
    window.removeEventListener('resize', this.resize)
  },
  methods: {
    controlTime(timeListIndex, datetime) {
      if (timeListIndex === this.timeListIndex && datetime === this.datetime) return
      if (timeListIndex !== this.timeListIndex) {
        this.timeListIndex = timeListIndex
        this.control = true
      }
      if (datetime !== this.datetime) this.datetime = datetime
      this.draw()
    },
    hide() {
      this.$emit('hideChart', this.name)
    },
    copyTime() {
      this.$emit('copyTime', this.timeListIndex, this.datetime)
    },
    setPort(pod) {
      this.chartPod = pod
      this.draw()
    },
    searchChartData(start, end) {
      return new Promise((resolve, reject) => {
        getMetric({
          pod: this.chartPod,
          metric_name: this.name,
          start_time: parseInt(start / 1000),
          end_time: parseInt(end / 1000)
        }).then((res) => {
          resolve(res)
        })
      })
    },
    draw() {
      const start = (this.datetime === null ? new Date().getTime() : this.datetime) - this.timeList[this.timeListIndex][1]
      const end = this.datetime === null ? new Date().getTime() : this.datetime
      if (end > new Date().getTime()) {
        this.$message({
          type: 'warning',
          message: '请选择正确的结束时间',
          duration: this.$store.state.promptDuration
        })
        this.datetime = new Date().getTime()
        return
      }
      // if (this.chart) {
      //   this.chart.dispose()
      //   this.chart = null
      // }
      this.searchChartData(start, end).then((data) => {
        var dataZoomStart = 0
        var dataZoomEnd = 100
        const chart = this.chart || echarts.init(this.$refs.chart)
        if (chart._model !== undefined) {
          dataZoomStart = chart._model.option.dataZoom[0].start
          dataZoomEnd = chart._model.option.dataZoom[0].end
        }
        const option = {
          tooltip: {
            trigger: 'axis',
            axisPointer: {
              lineStyle: {
                color: '#57617B'
              }
            }
          },
          grid: {
            left: 56,
            right: 16,
            top:20
            // bottom: 20
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
          dataZoom: [
            {
              show: true,
              height: 25,
              xAxisIndex: [0],
              bottom: 10,
              start: dataZoomStart,
              end: dataZoomEnd,
              handleIcon:
                            'path://M306.1,413c0,2.2-1.8,4-4,4h-59.8c-2.2,0-4-1.8-4-4V200.8c0-2.2,1.8-4,4-4h59.8c2.2,0,4,1.8,4,4V413z',
              handleSize: '100%',
              textStyle: {
                color: '#57617B',
                fontSize: 8
              }
            },
            {
              type: 'inside',
              show: true,
              height: 15,
              start: 0,
              end: 100
            }
          ],
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
              data: data.map((item) => ({
                name: item.time,
                value: [item.time, item.value]
              }))
            }
          ]
        }
        chart.setOption(option)
        this.chart = chart
      })
    },
    resize() {
      if (this.chart) {
        this.chart.resize()
      }
    },
    initChart() {
      this.chart = echarts.init(this.$refs.chart)
      var dataZoomStart = 0
      var dataZoomEnd = 100
      if (this.chart._model !== undefined) {
        dataZoomStart = this.chart._model.option.dataZoom[0].start
        dataZoomEnd = this.chart._model.option.dataZoom[0].end
      }
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
          left: '100px',
          right: '100px'
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
        dataZoom: [
          {
            show: true,
            height: 25,
            xAxisIndex: [0],
            bottom: 0,
            start: dataZoomStart,
            end: dataZoomEnd,
            handleIcon:
                            'path://M306.1,413c0,2.2-1.8,4-4,4h-59.8c-2.2,0-4-1.8-4-4V200.8c0-2.2,1.8-4,4-4h59.8c2.2,0,4,1.8,4,4V413z',
            handleSize: '100%',
            textStyle: {
              color: '#57617B',
              fontSize: 8
            }
          },
          {
            type: 'inside',
            show: true,
            height: 15,
            start: 0,
            end: 100
          }
        ],
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

            data: this.data.map((item) => ({
              name: item.time,
              value: [item.time, item.value]
            }))
          }
        ]
      }

      this.chart.setOption(option)
      // 添加 resize 事件监听器以自适应窗口大小
      window.addEventListener('resize', () => {
        if (this.chart) {
          this.chart.resize()
        }
      })
    }
  }
}
</script>

<style scoped>
.chart-card >>> .el-card__body{
    padding: 16px;
}
.card_header{
    border-bottom: 1px solid #DCDEE6;
    height: 41px;
}
.card_header_text {
    float: left;
}

.card_header_button_1,
.card_header_button_2 {
    float: right;
    margin-right: 2px;
    /* width: 36px;
    height: 36px; */
    background-color: #aabbbb;
}

.card_header_button_1:hover {
    background: #409EFF !important;
    color: #fff;
}

.card_header_button_2:hover {
    background: #f73232 !important;
    color: #fff;
}

.chart-mini-button_1{
    background-color: #aabbbb;
    border-radius: 8px 0px 0px 8px;
}
.chart-mini-button_2 {
    background-color: #aabbbb;
    border-radius: 0px 8px 8px 0px;
}

.chart-mini-button_1:hover,
.chart-mini-button_2:hover{
    background-color: #409EFF;
    color: #fff;
}

.line-chart {
    display: absolute;
    width: 100%;
    height: 280px;
}

.chart-card {
    width: 46%;
    height: 399px;
    background: #F5F7F9;
    border-radius: 12px;
    border: 1px solid #E9EBF2;
}

.chart-control {
    margin-top: 16px;
    text-align: left;
    display: flex;
    justify-content: space-between;
}

.moving-helper {
    position: absolute;
    left: 0;
    top: 0;
    width: 2px;
    height: 100%;
    background-color: #409EFF;
}

.chart-mini-button {
    padding: 6px 0.5rem;
    background: #FFFFFF !important;
    color: #374E5C;
    font-size: 14px;
    line-height: 20px;
}
</style>
