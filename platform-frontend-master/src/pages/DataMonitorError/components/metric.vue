<template>
  <div class="DME-metric">
    <div class="DME-metric__left">
      <header>
        <div class="DME-metric-l__header-select">
          <span>PodName:</span>
          <el-select
            v-model="selectedPodname"
            placeholder="Select"
            style="width: 200px"
            size="mini"
          >
            <el-option
              v-for="(item, i) in podnameOptions"
              :key="i"
              :label="item"
              :value="item"
            />
          </el-select>
        </div>
        <div>
          <el-button
            size="mini"
            icon="el-icon-download"
            @click="metricDataExport"
          >
            <span O-R>{{ $t('button.download') }}</span>
          </el-button>
        </div>
      </header>
      <CardTitle style="margin: 0;">
        {{ $t('dataMonitor.podList') }}
      </CardTitle>
      <main>
        <el-checkbox
          v-model="checkAll"
          :indeterminate="isIndeterminate"
          @change="handleCheckAllChange"
        >
          {{ $t('button.all') }}
        </el-checkbox>
        <el-checkbox-group
          v-model="selectedNames"
          class="DME-metric__checkbox-group"
          @change="handleCheckedNameChange"
        >
          <el-checkbox
            v-for="name in metricsNames"
            :key="name"
            :label="name"
            :value="name"
          >
            {{ name }}
          </el-checkbox>
        </el-checkbox-group>
      </main>
    </div>
    <div class="DME-metric__right">
      <div>
        <MetricCard
          v-for="(card, i) in metricChartsShow"
          ref="metricCard"
          :key="i"
          :name="card.name"
          :pod="selectedPodname"
          :style="{ '--name': card.name }"
          class="DME-metric-chart"
          @syncTime="syncTime"
          @hideCard="hideCard"
        />
      </div>
    </div>
    <el-dialog
      :append-to-body="true"
      :visible.sync="dialogVisible"
      :title="$t('button.download')">
      <el-form inline>
        <el-form-item>
          <el-date-picker
            v-model="downloadDuration"
            :picker-options="pickerOptions"
            :start-placeholder="$t('placeholder.startTime')"
            :end-placeholder="$t('placeholder.endTime')"
            type="datetimerange"
            range-separator="-"/>
        </el-form-item>
        <el-form-item :label="$t('dataMonitor.step')">
          <el-select
            v-model="downloadStep">
            <el-option
              v-for="item in downloadStepOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"/>
          </el-select>
        </el-form-item>

      </el-form>

      <span
        slot="footer"
        class="dialog-footer">
        <el-button @click="dialogVisible = false">{{ $t('button.cancel') }}</el-button>
        <el-button
          type="primary"
          @click="metricDataExportConfirm">{{ $t('button.download') }}</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import CardTitle from '@/components/CardTitle'
import MetricCard from '@/components/MetricCard'
import { metricPodnameOptions, metricMetricsNames, metricMetricCharts } from '@/utils/staticData'
import { downloadMetric, getPodList, getMetricName } from '@/network/api/metric'
import { saveAs } from 'file-saver'
import { message } from '@/utils/utils'
export default {
  components: {
    CardTitle,
    MetricCard
  },
  data() {
    return {
      checkAll: false,
      isIndeterminate: true,
      podnameOptions: [],
      selectedPodname: 'checkoutservice',
      metricsNames: [],
      selectedNames: [
        'container_cpu_cfs_periods_total',
        'container_cpu_cfs_throttled_seconds_total',
        'container_cpu_load_average_10s',
        'container_cpu_system_seconds_total',
        'container_threads'
      ],
      metricCharts: [],
      metricChartsShow: [],
      dialogVisible: false,
      downloadDuration: null,
      downloadStep: 1,
      downloadStepOptions: [
        {
          value: 1,
          label: '1'
        },
        {
          value: 15,
          label: '15'
        },
        {
          value: 30,
          label: '30'
        },
        {
          value: 60,
          label: '60'
        }
      ],
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
  mounted() {
    const p1 = new Promise((resolve, reject) => {
      getPodList().then((res) => {
        this.podnameOptions = Array.from(new Set(res))
        this.selectedPodname = this.podnameOptions[0] || ''
        console.log('p1 resolve')
        resolve()
      })
    })
    const p2 = new Promise((resolve, reject) => {
      getMetricName().then((res) => {
        this.metricsNames = Array.from(new Set(res))
        this.metricCharts = this.metricsNames.map((item) => {
          return {
            name: item,
            subtext: ''
          }
        })
        console.log('p2 resolve')
        resolve()
      })
    })
    Promise.all([p1, p2]).then(() => {
      this.showCharts()
    })
  },
  methods: {
    handleCheckAllChange(val) {
      this.selectedNames = val ? this.metricsNames : []
      this.isIndeterminate = false
      this.showCharts()
    },
    handleCheckedNameChange(value) {
      const checkedCount = value.length
      this.checkAll = checkedCount === this.metricsNames.length
      this.isIndeterminate = checkedCount > 0 && checkedCount < this.metricsNames.length
      this.showCharts()
    },
    showCharts() {
      const pushCharts = () => {
        this.selectedNames.forEach((select) => {
          if (this.metricChartsShow.find(item => item.name === select) === undefined && this.metricCharts.find(item => item.name === select) !== undefined) {
            this.metricChartsShow.push(this.metricCharts.find(item => item.name === select))
          }
        }) // 加入
        this.metricChartsShow = this.metricChartsShow.filter((item) => this.selectedNames.indexOf(item.name) !== -1)
        // console.log(this.metricChartsShow)
        // this.updateData()
        // 删除
      }
      pushCharts()
      // 目前页面结构使用视图变换会出现渲染顺序不正确
      // 视图变换强制在最顶层
      // if (document.startViewTransition) { // 如果支持就视图变换
      //   document.startViewTransition(() => { // 开始视图变换
      //     pushCharts()
      //   })
      // } else { // 不支持就执行原来的逻辑
      //   pushCharts()
      // }
    },
    metricDataExport() {
      this.dialogVisible = true
    },
    metricDataExportConfirm() {
      const duration = this.downloadDuration
      if (!duration) {
        message('请填写完整信息')
        return
      }
      this.dialogVisible = false
      const startTime = Math.floor(duration[0] / 1000)
      const endTime = Math.floor(duration[1] / 1000)
      message('已开始查询，请等待下载', 'success')
      downloadMetric({
        start_time: startTime,
        end_time: endTime,
        step: this.downloadStep
      }).then((res) => {
        saveAs(new Blob([res]), 'data.zip')
      })
    },
    syncTime(time) {
      const metricCards = this.$refs.metricCard
      for (const metricCard of metricCards) {
        metricCard.receiveTime(time)
      }
    },
    hideCard(name) {
      this.selectedNames = this.selectedNames.filter((item) => item !== name)
      this.showCharts()
    }
  }
}
</script>

<style>
.DME-metric {
  position: relative;
  text-align: left !important;
  display: flex;
  height: 100%;
}
.DME-metric__left {
  position: relative;
  box-sizing: border-box;
  width: 400px;
  border-right: 1px solid #E9EBF2;
}
.DME-metric__right {
  position: relative;
  width: calc(100% - 400px);
}
.DME-metric__left > header {
  display: flex;
  box-sizing: border-box;
  height: 45px;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #E9EBF2;
}
.DME-metric__left > header > div {
  height: auto;
  display: flex;
  align-items: center;
  padding: 0px 5px;
}
.DME-metric-l__header-select > span {
  font-size: 12px;
  line-height: 20px;
  margin-right: 5px;
}
.DME-metric__left > main {
  height: calc(100% - 45px - 24px);
  overflow: auto;
}
.DME-metric__checkbox-group {
  display: flex;
  flex-direction: column;
}
.DME-metric__checkbox-group label {
  max-width: 100%;
  overflow: hidden;
  margin-right: 5px;
  border-radius: 4px;
}
.DME-metric__checkbox-group > .is-checked {
  background-color: #E5F5FF;
}
.DME-metric__checkbox-group label:hover {
  overflow: auto;
}
.DME-metric__right {
  height: 100%;
  overflow: auto;
}
.DME-metric__right > div {
  display: flex;
  text-align: center;
  flex-wrap: wrap;
  justify-content: center;
}
.DME-metric-chart {
  view-transition-name: var(--name);
  display: block;
}
</style>
