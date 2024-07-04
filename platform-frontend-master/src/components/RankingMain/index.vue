<template>
  <div class="ranking-main">
    <header>
      <span>
        请选择评估指标
      </span>
      <el-select
        v-model="selectEM"
        placeholder="请选择"
        @change="selectChange">
        <el-option
          v-for="item in selectEMOptions"
          :key="item.id"
          :label="item.indicatorName"
          :value="item.id"/>
      </el-select>
    </header>
    <main>
      <el-table
        :data="tableData"
        stripe
        border
        style="width: 100%">
        <el-table-column
          prop="algorithm"
          label="方法名"
          width="220"/>
        <el-table-column
          prop="gold"
          label="金牌"/>
        <el-table-column
          prop="silver"
          label="银牌"/>
        <el-table-column
          prop="copper"
          label="铜牌"/>
        <el-table-column
          prop="strawberry"
          label="酸草莓奖"/>
        <el-table-column
          prop="total"
          label="奖牌榜总榜"
          width="200"/>
      </el-table>
    </main>
  </div>
</template>

<script>
import rankingManager from '../../pages/Rankings/rangkingManager'
export default {
  data() {
    return {
      selectEMOptions: [],
      selectEM: -1,
      tableData: []
    }
  },
  beforeMount() {
    rankingManager.addEventListener('update', this.rankingManagerUpdate.bind(this))
  },
  beforeDestroy() {
    rankingManager.removeEventListener('update', this.rankingManagerUpdate.bind(this))
  },
  methods: {
    rankingManagerUpdate(event) {
      switch (event.name) {
        case 'evaluationMetricList':
          this.selectEM = event.data.value
          this.selectEMOptions = event.data.data
          break
        case 'medal':
          this.tableData = event.data
          break
        default:
          break
      }
    },
    selectChange() {
      rankingManager.setEvaluationMetric(this.selectEM)
    }
  }
}
</script>

<style>
.ranking-main {
  text-align: left;
}
.ranking-main > header {
  margin-bottom: 10px;
}
</style>
