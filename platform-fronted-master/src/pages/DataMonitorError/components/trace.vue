<template>
  <div class="DME-trace">
    <div class="DME-trace__left">
      <header O-R>
        <div>
          <el-date-picker
            v-model="datetime"
            :disabled-date="judge"
            :picker-options="pickerOptions"
            size="mini"
            type="datetimerange"
            start-placeholder="Start date"
            end-placeholder="End date"
            style="width: 200px; margin-right: 5px"
          />
          <el-button
            :disabled="!datetime"
            size="mini"
            icon="el-icon-search"
            @click="searchTraceList"
          >
            {{ $t('button.search') }}
          </el-button>
        </div>
        <div>
          <el-button
            :disabled="!datetime"
            size="mini"
            icon="el-icon-download"
            @click="traceDataExport">
            {{ $t('button.download') }}
          </el-button>
        </div>
      </header>
      <main class="left-box">
        <TraceCard
          v-for="(trace, i) in traceList.slice((currentPage - 1) * 10, currentPage * 10)"
          :key="i"
          :data="trace"
          :active="(currentPage - 1) * 10 + i === activeTraceCard"
          @click="clickTraceCard((currentPage - 1) * 10 + i)"
        />
        <el-empty v-if="traceList.length===0"/>
      </main>
      <footer>
        <el-pagination
          v-if="traceList.length!==0"
          :total="total"
          :page-size="10"
          :current-page.sync="currentPage"
          small
          layout="prev, pager, next"
        />
      </footer>
    </div>
    <div class="DME-trace__right">
      <header v-show="traceGraph.length > 0">
        <div class="DME-trace__detail">
          <div O-B>
            <span>{{ traceGraph[0] && traceGraph[0].operation_name }}</span>
          </div>
          <div O-R>
            <div class="DME-trace__detail__little">
              <span>{{ $t('trace.startingPoint') }}</span>
              <span>{{ traceGraph[0] && new Date(traceGraph[0].timestamp / 1000).toLocaleString() }}</span>
            </div>
            <div class="DME-trace__detail__little">
              <span>{{ $t('trace.duration') }}</span>
              <span>{{ traceGraph[0] && traceGraph[0].duration / 1000 }}ms</span>
            </div>
            <span class="DME-trace__detail-id">{{ traceGraph[0] && traceGraph[0].span_id }}</span>
          </div>
        </div>
        <div>
          <el-radio-group
            v-model="showType"
            size="mini">
            <el-radio-button
              :label="$t('button.chart')"
            />
            <el-radio-button
              :label="$t('button.table')"
            />
          </el-radio-group>
        </div>
      </header>
      <main>
        <TraceGraph
          v-if="showType === $t('button.chart')"
          :data="traceGraph"
        />
        <TraceTable
          v-else-if="showType === $t('button.table')"
          :data="traceGraph"
        />
      </main>
    </div>
  </div>
</template>

<script>
import TraceCard from '@/components/TraceCard'
import TraceGraph from '@/components/TraceGraph'
import TraceTable from '@/components/TraceTable'
import { getTraceList, getTrace, downloadTrace } from '@/network/api/trace'
import { judgeDuration, message, deepClone } from '@/utils/utils'
import { saveAs } from 'file-saver'
export default {
  name: 'Trace',
  components: {
    TraceCard,
    TraceGraph,
    TraceTable
  },
  data() {
    return {
      showGraph: true,
      datetime: null,
      traceGraph: [],
      traceList: [],
      currentPage: 1,
      showType: this.$t('button.chart'),
      activeTraceCard: -1,
      traceMap: new Map(), // 减少调用接口次数
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
  computed: {
    total() {
      return this.traceList.length
    }
  },
  methods: {
    judge(date) {
      console.log(date)
      return date.getTime() >= Date.now()
    },
    clickTraceCard(i) {
      console.log(i)
      this.activeTraceCard = i
      const searchId = this.traceList[i].trace_id
      if (this.traceMap.has(searchId)) {
        this.traceGraph = deepClone(this.traceMap.get(searchId))
      } else {
        this.traceGraph = []
        getTrace({
          trace_id: searchId
        }).then((res) => {
          const traceGraph = res
          this.traceMap.set(searchId, deepClone(traceGraph))
          this.traceGraph = traceGraph
        }).catch((err) => {
          message(err.message)
          this.traceGraph = []
        })
      }
    },
    searchTraceList() {
      if (!this.datetime) return
      const startTime = this.datetime[0].getTime()
      const endTime = this.datetime[1].getTime()
      if (judgeDuration(startTime, endTime, 15)) {
        const loading = this.$loading({
          lock: true, // lock的修改符--默认是false
          text: 'loading', // 显示在加载图标下方的加载文案
          spinner: 'el-icon-loading', // 自定义加载图标类名
          background: 'white', // 遮罩层颜色
          target: document.querySelector('.left-box') // loadin覆盖的dom元素节点
        })
        getTraceList({
          start_time: Math.floor(startTime / 1000),
          end_time: Math.floor(endTime / 1000)
        }).then((res) => {
          this.currentPage = 1
          this.activeTraceCard = -1
          this.traceList = res
          this.clickTraceCard(0)
          loading.close()
        }).catch((err) => {
          message(err.message)
          loading.close()
        })
      }
    },
    traceDataExport() {
      const startTime = Math.floor(this.datetime[0].getTime() / 1000)
      const endTime = Math.floor(this.datetime[1].getTime() / 1000)
      downloadTrace({
        start_time: startTime,
        end_time: endTime
      }).then((res) => {
        saveAs(new Blob([res]), 'data.zip')
      })
    }
  }
}
</script>

<style>
.DME-trace {
  position: relative;
  display: flex;
  height: 100%;
  text-align: left;
}
.DME-trace__left {
  position: relative;
  box-sizing: border-box;
  width: 450px;
  border-right: 1px solid #E9EBF2;
}
.DME-trace__right {
  position: relative;
  width: calc(100% - 450px);
}
.DME-trace__left > header {
  display: flex;
  box-sizing: border-box;
  height: 45px;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #E9EBF2;
}
.DME-trace__left > header > div {
  height: auto;
  display: flex;
  align-items: center;
  padding: 0px 5px;
}
.DME-trace__left > main {
  height: calc(100% - 45px * 2);
  padding: 0px 10px;
  overflow: auto;
}
.DME-trace__left > footer {
  display: flex;
  box-sizing: border-box;
  height: 45px;
  border-top: 1px solid #E9EBF2;
  justify-content: center;
  align-items: center;
}
.DME-trace__right > header {
  height: 60px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.DME-trace__right > main {
  height: calc(100% - 60px);
}
.DME-trace__detail > div:nth-child(1) {
  font-size: 18px;
}
.DME-trace__detail > div:nth-child(2) {
  display: flex;
  align-items: center;
  margin-top: 5px;
}
.DME-trace__detail__little {
  font-size: 12px;
  display: flex;
  align-items: center;
  margin: 0px 5px;
}
.DME-trace__detail__little > span:nth-child(1) {
  padding: 0px 6px;
  background-color: #748C9A;
  border-radius: 8px;
  color: white;
}
.DME-trace__detail__little > span:nth-child(2) {
  margin: 0px 5px;
  font-size: 13px;
}
.DME-trace__detail-id {
  color: #748C9A;
  font-size: 12px;
  margin-left: 5px;
}
</style>
