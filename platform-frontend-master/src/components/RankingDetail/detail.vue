<template>
  <div class="RD-detail">
    <header class="header-box">
      <div>
        <el-button
          size="mini"
          @click="showTable">{{ $t('login.back') }}</el-button>
      </div>
      <div>
        <span>{{ $t('rankings.evaluationIndicators') }}</span>
        <el-checkbox-group
          v-model="evaluationMetricListSelected"
          class="inline-box">
          <el-checkbox
            v-for="e in evaluationMetricList"
            :key="e.id"
            :label="e.id">{{ e.indicatorName }}</el-checkbox>
        </el-checkbox-group>
      </div>
    </header>
    <main>
      <el-table
        :data="tableData"
        :header-cell-style="{'text-align':'center',color: '#1976d2',backgroundColor: '#c8dded',borderColor: '#0000001f'}"
        :cell-style="cellStyle"
        stripe
        style="width: 100%">
        <el-table-column
          :label="$t('algo.name')"
          fixed
          prop="algorithmName"
          width="300">
          <template slot-scope="scope">
            <div style="display: flex; justify-content: space-between;">
              <span>{{ scope.row.algorithmName }}</span>
              <el-button
                size="mini"
                @click="reEvaluation(scope.row.algorithm)">{{ $t('rankings.reEvaluation') }}</el-button>
            </div>
          </template>
        </el-table-column>
        <el-table-column
          :label="$t('rankings.situation')">
          <el-table-column
            v-for="em in evaluationMetricShowList"
            :key="em.id"
            :label="em.indicatorName">
            <el-table-column
              v-for="fj in Object.keys(em.formatJson)"
              :key="fj"
              :label="fj"
              :prop="em.indicatorName + '-' + fj"
              width="150"/>
          </el-table-column>
        </el-table-column>
      </el-table>
    </main>
  </div>
</template>

<script>
import rankingManager from '../../pages/Rankings/rangkingManager'
import { deepClone, message } from '../../utils/utils'
export default {
  data() {
    return {
      evaluationMetricListSelected: [],
      evaluationMetricList: [],
      tableData: [],
      recordId: null,
      algorithmTypeName: null
    }
  },
  computed: {
    evaluationMetricShowList() {
      return this.evaluationMetricList.filter((i) => this.evaluationMetricListSelected.find((item) => item === i.id))
    }
  },
  beforeMount() {
    rankingManager.addEventListener('update', this.rankingManagerUpdate.bind(this))
    rankingManager.addEventListener('error', this.reEvaluationError.bind(this))
    rankingManager.addEventListener('success', this.reEvaluationSuccess.bind(this))
  },
  beforeDestroy() {
    rankingManager.removeEventListener('update', this.rankingManagerUpdate.bind(this))
    rankingManager.removeEventListener('error', this.reEvaluationError.bind(this))
    rankingManager.removeEventListener('success', this.reEvaluationSuccess.bind(this))
  },
  mounted() {
  },
  methods: {
    cellStyle({ row, column, rowIndex, columnIndex }) {
      console.log(rowIndex)
      const style = { 'text-align':'center', borderColor: '#0000001f', backgroundColor: 'white', color: '#616161' }
      if (rowIndex % 2 === 0) {
        style.backgroundColor = 'rgb(237, 242, 246)'
      }
      return style
    },
    rankingManagerUpdate(event) {
      switch (event.name) {
        case 'recordDetail':
          console.log('recordDetail', event.data)
          this.evaluationMetricList = event.data.evaluationMetricList
          // 指标默认全选
          for (const item of this.evaluationMetricList) {
            console.log(item)
            this.evaluationMetricListSelected.push(item.id)
          }
          this.recordId = event.data.recordId
          this.algorithmTypeName = event.data.algorithmTypeName
          this.analyseTableData(deepClone(event.data.data))
          break
        default:
          break
      }
    },
    showTable() {
      this.evaluationMetricListSelected = []
      this.$emit('showTable')
    },
    analyseTableData(data) {
      const tableData = []
      data.forEach((item) => {
        item.algorithmName = rankingManager.getAlgorithmName(item.algorithm)
        this.evaluationMetricList.forEach((em) => {
          const itemEm = item[em.indicatorName] || {}
          console.log(itemEm)
          const keys = Object.keys(em.formatJson)
          console.log(keys)
          keys.forEach((key) => {
            console.log(itemEm[key])
            item[em.indicatorName + '-' + key] = itemEm[key]
          })
        })
        tableData.push(item)
      })
      this.tableData = tableData
      console.log(tableData)
    },
    reEvaluation(algorithm) {
      console.log('algorithm', algorithm)
      rankingManager.reEvaluation(this.recordId, algorithm)
    },
    reEvaluationError(event) {
      switch (event.name) {
        case 'reEvaluation':
          message(this.$t('rankings.fail'))
          console.log(event.data)
          break
        default:
          break
      }
    },
    reEvaluationSuccess(event) {
      switch (event.name) {
        case 'reEvaluation':
          message(this.$t('rankings.success'), 'success')
          rankingManager.getRecordDetailData(this.recordId, this.algorithmTypeName, true, true)
          break
        default:
          break
      }
    }
  }
}
</script>

<style scoped>
.RD-detail > header {
  display: flex;
  justify-content: flex-start;
  align-items: center;
}
.RD-detail > header > div:last-child {
  margin-left: 20px;
}
.header-box{
  margin: 20px 0;
}
.inline-box{
  display: inline-block;
}
</style>
