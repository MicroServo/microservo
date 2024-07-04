<template>
  <div>
    <div class="card-title">{{ $t('table.task') }}：{{ info.task_name }}</div>
    <el-descriptions
      :column="3"
      :label-style="drawerLabel"
      :content-style="drawerContent"
      style="margin-bottom: 16px"
      border>
      <el-descriptions-item :label="$t('table.dataType')">
        <template v-if="info.dataset_type">
          <el-tag
            v-for="item in info.dataset_type"
            :key="item"
            class="my-tag">
            {{ item }}
          </el-tag>
        </template>
        <template v-else>
          -
        </template>
      </el-descriptions-item>
      <el-descriptions-item :label="$t('table.executor')">{{ info.execute_person }}</el-descriptions-item>
      <el-descriptions-item :label="$t('table.timePeriod')">{{ info.dataset_range }}</el-descriptions-item>
      <el-descriptions-item :label="$t('placeholder.startTime')">{{ info.start_time }}</el-descriptions-item>
      <el-descriptions-item :label="$t('table.cost')">
        <span v-if="info.cost==='-'">-</span>
        <span v-else>{{ info.cost }}s</span>
      </el-descriptions-item>
    </el-descriptions>
    <el-empty
      v-if="info.res==='无结果'"
      :description="$t('table.noData')" />
    <div v-else>
      <!-- prf -->
      <div v-if="f1List.length>0">
        <div class="title">
          <div class="card-title">
            <span>{{ info.indicator.indicator_name }}</span>
          </div>
          <el-radio-group
            v-model="radio2"
            size="small">
            <el-radio-button label="table"/>
            <el-radio-button label="graph"/>
          </el-radio-group>
        </div>
        <el-table
          v-if="radio2==='table'"
          ref="f1List"
          :data="f1List"
          fit
          stripe
          highlight-current-row
          style="margin-bottom: 16px;width: 100%"
        >
          <!-- <el-table-column
            prop="epoch"
            label="epoch"
          /> -->
          <el-table-column
            prop="precision"
            show-overflow-tooltip
            label="precision"
          />
          <el-table-column
            prop="recall"
            show-overflow-tooltip
            label="recall"
          />
          <el-table-column
            prop="f1_score"
            show-overflow-tooltip
            label="f1-score"
          />
        </el-table>
        <div
          v-else
          id="barChart2"
          class="barChart"/>
      </div>
      <!-- accuracyk -->
      <div v-if="accuracykList.length>0">
        <div class="title">
          <div class="card-title">
            <span>accuracy@k</span>
          </div>
          <el-radio-group
            v-model="radio3"
            size="small">
            <el-radio-button label="table"/>
            <el-radio-button label="graph"/>
          </el-radio-group>
        </div>
        <el-table
          v-if="radio3==='table'"
          ref="accuracykList"
          :data="accuracykList"
          fit
          stripe
          highlight-current-row
          style="margin-bottom: 16px;width: 100%"
        >
          <!-- <el-table-column
            prop="epoch"
            label="epoch"
          /> -->
          <el-table-column
            prop="accuracy@1"
            show-overflow-tooltip
            label="accuracy@1"
          />
          <el-table-column
            prop="accuracy@2"
            show-overflow-tooltip
            label="accuracy@2"
          />
          <el-table-column
            prop="accuracy@3"
            show-overflow-tooltip
            label="accuracy@3"
          />
          <el-table-column
            prop="accuracy@4"
            show-overflow-tooltip
            label="accuracy@4"
          />
          <el-table-column
            prop="accuracy@5"
            show-overflow-tooltip
            label="accuracy@5"
          />
        </el-table>
        <div
          v-else
          id="barChart3"
          class="barChart"/>
      </div>
    </div>
  </div>
</template>

<script>
import structure3 from '@/components/structure/structure3.vue'
import * as echarts from 'echarts'
import resize from '@/components/echart/resize.js'

export default {
  name:'EvaluateDataDetail',
  components: {
    structure3
  },
  mixins: [resize],
  data() {
    return {
      info: '',
      drawerLabel:{
        'width': '10%'
      },
      drawerContent:{
        'width':'23%'
      },
      accuracykList: [],
      radio3: 'table',
      topkList:[],
      radio1:'table',
      f1List:[],
      radio2:'table',
      chart1: null,
      chart2: null,
      chart3: null,
      autoResize:true,
      id: ''
    }
  },
  watch: {
    radio2(newVal) {
      if (newVal === 'graph') {
        this.$nextTick(() => {
          this.initChart2()
        })
      }
    },
    radio3(newVal) {
      if (newVal === 'graph') {
        this.$nextTick(() => {
          this.initChart3()
        })
      }
    }
  },
  mounted() {
    this.id = localStorage.getItem('taskId')
    this.getTaskExecuteInfo()
  },
  methods: {
    initChart3() {
      var chartDom = document.getElementById('barChart3')
      this.chart3 = echarts.init(chartDom)
      this.setOptions3()
    },
    setOptions3() {
      const xData = Object.keys(this.accuracykList[0])
      const yData = Object.values(this.accuracykList[0])
      this.chart3.setOption({
        xAxis: {
          type: 'category',
          data: xData,
          name: 'indicator'
        },
        yAxis: {
          type: 'value'
        },
        series: [{
          type: 'bar', // 可以是 'line', 'bar', 'scatter', 等等
          data: yData,
          itemStyle: {
            // 每个柱子颜色不同，可以使用渐变色或固定颜色数组
            color: function(params) {
              // params.dataIndex 为当前柱子的索引
              var colorList = ['#00a2fd', '#59cd96', '#f98c6e', '#7762e2', '#ce5787']
              return colorList[params.dataIndex]
            }
          }
        }]
      })
    },
    initChart2() {
      var chartDom = document.getElementById('barChart2')
      this.chart2 = echarts.init(chartDom)
      this.setOptions2()
    },
    setOptions2() {
      const xData = Object.keys(this.f1List[0])
      const yData = Object.values(this.f1List[0])
      this.chart2.setOption({
        tooltip: {  // 配置tooltip
          trigger: 'axis'  // 设置tooltip触发方式，这里设置为坐标轴触发
        },
        xAxis: {
          type: 'category',
          name: 'indicator',
          data: xData
        },
        yAxis: {
          name: 'value'
        },
        color:['#00A0FF', '#57CF95', '#F98B71'],
        legend: {
          right:'5px'
        },
        // dataset: {
        //   source: data
        // },
        series: [{ type: 'bar', data: yData }]
      })
    },
    getTaskExecuteInfo() {
      const url =  `/api/getTaskExecuteInfo?id=${this.id}`
      this.$http({
        method: 'get',
        url: url
      }).then((res) => {
        const resData = res.data
        if (resData.code === 0) {
          this.info = resData.data
          this.info.start_time = this.info.start_time.replace('年', '-').replace('月', '-').replace('日', '')
          this.info.dataset_type = this.info.dataset_type.split(',')
          this.handleRes(this.info)
        } else {
          this.$message.error(resData.message)
        }
      })
    },
    // souece 原字符串 start 要截取的位置 newStr 要插入的字符
    insertStr(source, start, newStr) {
      return source.slice(0, start) + newStr + source.slice(start)
    },
    handleRes(data) {
      const res = data.res
      const indicator = data.indicator.indicator_name
      if (indicator === 'accuracy_at_k') {
        this.accuracykList = [res]
      } else {
        this.f1List = [res]
      }
    }
  }
}
</script>

<style scoped>
.title{
  display: flex;
  justify-content:space-between;
  color: #222222;
  line-height: 25px;
  font-weight: bold;
  text-align: left;
  margin-bottom: 16px;
}
.barChart{
    height: 350px;
    width:100%
}
.my-tag{
  margin-right: 5px;
}
</style>
