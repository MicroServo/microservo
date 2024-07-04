<template>
  <div class="ranking-detail">
    <header>
      <el-button @click="datasetVisible = true">
        {{ $t('rankings.addDataset') }}
      </el-button>
      <el-button @click="createRecord">
        {{ $t('rankings.addEvaluation') }}
      </el-button>
    </header>
    <main>
      <rankingDetailTable
        v-show="tableShow"
        @showDetail="showDetail"/>
      <rankingDetailDetail
        v-show="!tableShow"
        @showTable="showTable"/>
    </main>
    <!-- 新增评测dialog -->
    <el-dialog
      :visible.sync="dialogVisible"
      :title="$t('rankings.addEvaluation')"
      width="500px">
      <div class="ranking-detail__dialog">
        <div class="form-item">
          <span>{{ $t('rankings.recordName') }}*</span>
          <el-input
            v-model="recordName"
            :placeholder="$t('placeholder.recordName')" />
        </div>
        <div class="form-item">
          <span>{{ $t('rankings.choose.type') }}*</span>
          <el-radio-group
            v-model="algorithmType"
            @input="algorithmTypeChange">
            <el-radio
              v-for="a in algorithmTypeList"
              :key="a.id"
              :label="a.id">{{
              a.algorithmTypeName }}</el-radio>
          </el-radio-group>
        </div>
        <div
          class="form-item">
          <span v-if="algorithmList.length!==0">{{ $t('rankings.choose.algo') }}</span>
          <el-checkbox-group v-model="algorithmListSelected">
            <el-checkbox
              v-for="a in algorithmList"
              :key="a.id"
              :label="a.id">
              {{ a.algorithmName }}
            </el-checkbox>
          </el-checkbox-group>
        </div>
        <div class="form-item">
          <span>{{ $t('rankings.choose.dataset') }}*</span>
          <el-select
            v-model="dataset"
            :placeholder="$t('placeholder.choose')"
            @change="selectChange">
            <el-option
              v-for="item in datasetList"
              :key="item.id"
              :label="item.dataset_name"
              :value="item.id"/>
          </el-select>
        </div>
      </div>
      <span
        slot="footer"
        class="dialog-footer">
        <el-button
          size="mini"
          @click="dialogVisible = false">{{ $t('button.cancel') }}</el-button>
        <el-button
          size="mini"
          type="primary"
          @click="createRecordConfirm">{{ $t('button.confirm') }}</el-button>
      </span>
    </el-dialog>
    <!-- 新增数据集dialog -->
    <Dialog
      :dialogVisible="datasetVisible"
      :title="$t('rankings.addDataset')"
      @changeDialog="changeDialog">
      <template slot="content">
        <el-form
          ref="datasetForm"
          :model="datasetForm"
          :rules="datasetRules"
          label-position="left"
          label-width="auto">
          <el-form-item
            :label="$t('rankings.datasetName')"
            prop="dataset_name">
            <el-input
              v-model="datasetForm.dataset_name"
              :placeholder="$t('placeholder.datasetName')"
              class="inputWidth2"/>
          </el-form-item>
          <el-form-item
            :label="$t('algoTemplate.dataset')"
            prop="dataset_range">
            <el-date-picker
              v-model="datasetForm.dataset_range"
              :picker-options="value1Option"
              :start-placeholder="$t('placeholder.startTime')"
              :end-placeholder="$t('placeholder.endTime')"
              class="inputWidth2"
              type="datetimerange"
              value-format="timestamp"
              range-separator="-"/>
          </el-form-item>
        </el-form>
      </template>
      <template slot="footer">
        <WhiteButton
          @click.native="changeDialog(false)">{{ $t('button.cancel') }}</WhiteButton>
        <BlueButton
          @click.native="createDataset">{{ $t('button.confirm') }}</BlueButton>
      </template>
    </Dialog>
  </div>
</template>

<script>
import rankingDetailTable from './table.vue'
import rankingDetailDetail from './detail.vue'
import rankingManager from '../../pages/Rankings/rangkingManager'
import BlueButton from '@/components/button/blueButton.vue'
import WhiteButton from '@/components/button/whiteButton.vue'
import Dialog from '@/components/dialog/index.vue'
import { message } from '../../utils/utils'
export default {
  components: {
    rankingDetailTable,
    rankingDetailDetail,
    BlueButton,
    WhiteButton,
    Dialog
  },
  props: {
    tableShow: {
      type: Boolean,
      default: true
    }
  },
  data() {
    return {
      // tableShow: true,
      dialogVisible: false,
      duration: null,
      algorithmType: -1,
      algorithmListSelected: [],
      evaluationMetricsSelected: [],
      algorithmTypeList: [],
      algorithmList: [],
      evaluationMetrics: [],
      datasetList: [],
      dataset: '',
      recordName: '',
      value1Option: {
        disabledDate(date) {
          return date.getTime() > Date.now() || date.getTime() < Date.now() - 1000 * 3600 * 24 * 14
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
      },
      datasetVisible: false,
      datasetForm:{
        dataset_range: '',
        dataset_name: ''
      },
      datasetRules: {
        dataset_name: [{ required: true, trigger: 'blur' }],
        dataset_range: [{ required: true, trigger: 'blur' }]
      }
    }
  },
  beforeMount() {
    rankingManager.addEventListener('update', this.rankingManagerUpdate.bind(this))
    rankingManager.addEventListener('error', this.rankingManagerError.bind(this))
    rankingManager.addEventListener('success', this.rankingManagerSuccess.bind(this))
  },
  beforeDestroy() {
    rankingManager.removeEventListener('update', this.rankingManagerUpdate.bind(this))
    rankingManager.removeEventListener('error', this.rankingManagerError.bind(this))
    rankingManager.removeEventListener('success', this.rankingManagerSuccess.bind(this))
  },
  methods: {
    changeDialog(v) {
      this.datasetVisible = v
      this.resetDatasetForm()
    },
    resetDatasetForm() {
      for (const key in this.datasetForm) {
        this.datasetForm[key]  = ''
      }
    },
    rankingManagerUpdate(event) {
      switch (event.name) {
        default:
          break
      }
    },
    rankingManagerError(event) {
      switch (event.name) {
        case 'createRecord':
          message('新增评测失败')
          console.log(event.data)
          break
        default:
          break
      }
    },
    rankingManagerSuccess(event) {
      switch (event.name) {
        case 'createRecord':
          message('新增评测成功', 'success')
          this.dialogVisible = false
          rankingManager.dataUpdate(false, true)
          break
        default:
          break
      }
    },
    selectChange() {
      rankingManager.setAlgorithmType(this.selectEM)
    },
    createRecord() {
      this.dialogVisible = true
      this.queryDataset()
      this.duration = null
      this.dataset = ''
      this.algorithmType = -1
      this.algorithmListSelected = []
      this.evaluationMetricsSelected = []

      this.algorithmTypeList = rankingManager.getAlgorithmTypeList()
      console.log('algorithmTypeList', this.algorithmTypeList)
    },
    // 新增数据集
    createDataset() {
      this.$refs.datasetForm.validate(valid => {
        if (valid) {
          const url = '/api/leaderboard/createdataset'
          this.$http({
            method: 'get',
            url: url,
            params: {
              dataset_name: this.datasetForm.dataset_name,
              start_time: Math.ceil(this.datasetForm.dataset_range[0] / 1000),
              end_time: Math.ceil(this.datasetForm.dataset_range[1] / 1000)
            }
          }).then((res) => {
            const resData = res.data
            if (resData.code === 0) {
              message('新增数据集成功', 'success')
            } else {
              message('新增数据集失败')
            }
          })
          this.datasetVisible = false
        }
      })
    },
    queryDataset() {
      const url = '/api/leaderboard/querydataset'
      this.$http({
        method: 'get',
        url: url
      }).then((res) => {
        const resData = res.data
        if (resData.code === 0) {
          this.datasetList = resData.data
        }
      })
    },
    algorithmTypeChange() {
      this.evaluationMetricsSelected = []
      this.algorithmListSelected = []
      this.algorithmList = rankingManager.getAlgorithmList(this.algorithmTypeList.find((item) => item.id === this.algorithmType).algorithmTypeName)
      this.evaluationMetrics = rankingManager.getEvaluationMetricList(this.algorithmTypeList.find((item) => item.id === this.algorithmType).algorithmTypeName).data
    },
    createRecordConfirm() {
      if (this.dataset && this.algorithmType && this.recordName) {
        // rankingManager.createRecord(this.algorithmType, this.dataset, this.algorithmListSelected.join(','))
        const url = '/api/leaderboard/createrecord'
        this.$http({
          method: 'get',
          url: url,
          params: {
            algorithm_type: this.algorithmType,
            dataset: this.dataset,
            algorithm_list: this.algorithmListSelected.join(','),
            record_name: this.recordName
          }
        }).then((res) => {
          const resData = res.data
          if (resData.code === 0) {
            message(this.$t('rankings.success2'), 'success')
          } else {
            message(this.$t('rankings.fail2'))
          }
        })
        this.dialogVisible = false
        rankingManager.dataUpdate(false, true)
      } else {
        message(this.$t('rankings.required'))
      }
    },
    showDetail() {
      this.tableShow = false
    },
    showTable() {
      this.tableShow = true
    }
  }
}
</script>

<style>
.ranking-detail {
  text-align: left;
}
.ranking-detail > header {
  margin-bottom: 10px;
}
.ranking-detail__dialog {
  display: flex;
  flex-direction: column;
}
.form-item{
  margin: 10px 0;
}
.inputWidth2{
  width: 250px;
  display: flex;
}
.ranking-detail /deep/ .el-color-picker__icon, .el-input, .el-textarea{
  width: 250px;
}
.el-date-editor--datetimerange.el-input__inner{
  width: 250px;
}
</style>
