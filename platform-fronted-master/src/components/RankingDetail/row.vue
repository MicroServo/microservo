<template>
  <div class="RD-table-row">
    <div>
      <div class="evaluation-name">
        <span>{{ $t('rankings.recordName') }}：</span>
        <span>{{ data.record_name }}</span>
      </div>

      <span>{{ $t('rankings.datasetName') }}：</span>
      <span>{{ data.dataset }}</span>
    </div>
    <div>
      <el-button @click="addNewAlgorithm">
        {{ $t('rankings.addAlgorithm') }}
      </el-button>
      <el-button @click="showDetail">
        {{ $t('table.detail') }}
      </el-button>
    </div>
    <el-dialog
      :visible.sync="dialogVisible"
      :title="$t('rankings.addAlgorithm')"
      width="500px">
      <div class="RD-table-row__dialog">
        <div>
          <el-checkbox-group v-model="algorithmListSelected">
            <el-checkbox
              v-for="a in algorithmList"
              :key="a.id"
              :label="a.id">
              {{ a.algorithmName }}
            </el-checkbox>
          </el-checkbox-group>
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
          @click="addNewAlgorithmConfirm">{{ $t('button.confirm') }}</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import rankingManager from '../../pages/Rankings/rangkingManager'
import { message } from '../../utils/utils'

export default {
  props: {
    data: {
      default: () => {},
      type: Object
    }
  },
  data() {
    return {
      dialogVisible: false,
      algorithmListSelected: [],
      algorithmList: [],
      nowAlgorithmTypeList: [] // only id
    }
  },
  beforeMount() {
    rankingManager.addEventListener('error', this.addNewAlgorithmError.bind(this))
    rankingManager.addEventListener('success', this.addNewAlgorithmSuccess.bind(this))
  },
  mounted() {
    this.init()
  },
  beforeDestroy() {
    rankingManager.removeEventListener('error', this.addNewAlgorithmError.bind(this))
    rankingManager.removeEventListener('success', this.addNewAlgorithmSuccess.bind(this))
  },
  methods: {
    init() {
      this.nowAlgorithmTypeList = this.data.algorithmList.split(',').map((i) => parseInt(i))
      this.algorithmList = rankingManager.getAlgorithmList(this.data.algorithmTypeName).filter((i) => !this.nowAlgorithmTypeList.find((item) => item === i.id))
    },
    addNewAlgorithm() {
      if (this.algorithmList.length === 0) {
        message(this.$t('rankings.no'), 'warning')
        return
      }
      this.dialogVisible = true
    },
    addNewAlgorithmConfirm() {
      const algorithmListStr = this.algorithmListSelected.join(',')
      if (!algorithmListStr) return
      rankingManager.addNewAlgorithm(this.data.recordId, algorithmListStr)
    },
    showDetail() {
      console.log(this.data)
      rankingManager.getRecordDetailData(this.data.recordId, this.data.algorithmTypeName)
      this.$emit('showDetail')
    },
    addNewAlgorithmError(event) {
      switch (event.name) {
        case 'addNewAlgorithm':
          if (event.data.recordId !== this.data.recordId) break
          message(this.$t('rankings.fail1'))
          console.log(event.data)
          break
        default:
          break
      }
    },
    addNewAlgorithmSuccess(event) {
      switch (event.name) {
        case 'addNewAlgorithm':
          if (event.data.recordId !== this.data.recordId) break
          message(this.$t('rankings.success1'), 'success')
          this.dialogVisible = false
          rankingManager.clearRecordDetailById(this.data.recordId)
          rankingManager.dataUpdate(false, true)
          break
        default:
          break
      }
    }
  }
}
</script>

<style >
.RD-table-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border: 1px solid rgba(0, 0, 0, 0.4);
  border-radius: 5px;
  padding: 10px;
  margin: 5px 0px;
  background-color: rgb(245, 245, 245);
}
.evaluation-name{
  display: inline-block;
  width: 270px;
}
</style>
