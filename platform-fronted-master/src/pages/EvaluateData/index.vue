<template>
  <structure3>
    <template #card-r-1>
      <div v-if="$route.path=='/evaluateData'">
        <div class="topButton">
          <RedButton
            @click.native="deleteTask()">
            <i class="el-icon-delete"/>
            {{ $t("button.deleteSelect") }}
          </RedButton>
        </div>

        <el-table
          ref="multipleTable"
          :data="AlgorithmList"
          fit
          stripe
          highlight-current-row
          @selection-change="handleSelectionChange"
        >
          <el-table-column
            type="selection"
            width="45" />
          <el-table-column
            :label="$t('table.createDate')"
            prop="create_time"
          />
          <el-table-column
            :label="$t('table.taskName')"
            prop="name"
            show-overflow-tooltip
          />
          <el-table-column
            :label="$t('table.executor')"
            prop="create_person"
            show-overflow-tooltip
          />
          <el-table-column
            :label="$t('table.type')"
            show-overflow-tooltip
          >
            <template slot-scope="{row}">
              <i
                v-if="row.execute_status==='finished'"
                style="background-color: #57CF95;"
                class="dotCss"/>
              <i
                v-if="row.execute_status==='failed'"
                style="background-color: #FF8A65;"
                class="dotCss"/>
              <i
                v-if="row.execute_status==='running'"
                style="background-color: #FFF176;"
                class="dotCss"/>
              <i
                v-if="row.execute_status==='interrupted'"
                style="background-color: #FFC107;"
                class="dotCss"/>
              <i
                v-if="row.execute_status==='waiting'"
                style="background-color: #03A9F4;"
                class="dotCss"/>
              {{ row.execute_status }}
            </template>
          </el-table-column>
          <el-table-column
            :label="$t('table.operate')"
            fixed="right"
          > <template slot-scope="{row}">
            <el-button
              type="text"
              @click="openDetail(row)">
              {{ $t('table.detail') }}
            </el-button>
            <el-button
              v-if="row.execute_status==='running'||row.execute_status==='waiting'"
              type="text"
              @click="handleStop(row)">
              {{ $t('table.interrupt') }}
            </el-button>
            <el-button
              v-if="row.execute_status==='interrupted'||row.execute_status==='failed'||row.execute_status==='finish'"
              type="text"
              @click="handleExecuteAgain(row)">
              {{ $t('table.executeAgain') }}
            </el-button>
          </template>
          </el-table-column>
        </el-table>
        <!-- 分页器 -->
        <el-pagination
          :current-page="pageNum"
          :total="total"
          :page-size="pageSize"
          style="margin-top: 16px;"
          background
          align="right"
          layout="total, prev, pager, next, jumper"
          @current-change="handleCurrentChange" />
        <!-- 中断dialog -->
        <Dialog
          :dialogVisible="dialogVisible"
          @changeDialog="changeDialog">
          <template slot="info">
            <div class="dialogFir">
              <img
                class="imgDia"
                src="@/assets/images/评估数据/warning.png">{{ $t('evaluateData.interrupt1') }}
            </div>
            <div class="dialogSed">{{ $t('evaluateData.interrupt2') }}</div>
          </template>
          <template slot="footer">
            <WhiteButton
              @click.native="changeDialog(false)">{{ $t('button.cancel') }}</WhiteButton>
            <RedButton
              @click.native="stopExecuteTask()">{{ $t('table.interrupt') }}</RedButton>
          </template>
        </Dialog>
        <!-- 再次执行dialog -->
        <Dialog
          :dialogVisible="editVisible"
          :title="$t('table.executeAgain')"
          @changeDialog="changeDialog">
          <template slot="content">
            <el-form
              ref="editForm"
              :rules="editRules"
              :model="editForm"
              label-width="auto"
              label-position="left"
              width="300px">
              <el-form-item
                :label="$t('algoTemplate.dataset')"
                prop="datasetTime">
                <el-date-picker
                  :picker-options="datasetTimeOption"
                  v-model="editForm.datasetTime"
                  :start-placeholder="$t('placeholder.startTime')"
                  :end-placeholder="$t('placeholder.endTime')"
                  class="inputWidth2"
                  type="datetimerange"
                  range-separator="-"
                  value-format="timestamp"/>
              </el-form-item>
              <el-form-item
                :label="$t('algoTemplate.excuteMode')"
                prop="radio">
                <el-radio
                  v-model="editForm.radio"
                  label="0">{{ $t('algoTemplate.immediate') }}</el-radio>
                <el-radio
                  v-model="editForm.radio"
                  label="1">{{ $t('algoTemplate.timed') }}</el-radio>
              </el-form-item>
              <el-form-item
                v-if="editForm.radio==='1'"
                :label="$t('algoTemplate.time')"
                prop="value2">
                <el-date-picker
                  :picker-options="value2Option"
                  v-model="editForm.value2"
                  :placeholder="$t('placeholder.time')"
                  class="inputWidth2"
                  type="datetime"
                  value-format="timestamp"/>
              </el-form-item>
            </el-form>
          </template>
          <template slot="footer">
            <WhiteButton
              @click.native="changeDialog(false)">{{ $t('button.cancel') }}</WhiteButton>
            <BlueButton
              @click.native="executeTaskAgain()">{{ $t('button.confirm') }}</BlueButton>
          </template>
        </Dialog>
      </div>
      <router-view />
    </template>
  </structure3>
</template>

<script>
import WhiteButton from '@/components/button/whiteButton.vue'
import Dialog from '@/components/dialog/index.vue'
import BlueButton from '@/components/button/blueButton.vue'
import RedButton from '@/components/button/redButton.vue'
import structure3 from '@/components/structure/structure3.vue'
export default {
  name: 'EvaluateData',
  components: {
    structure3,
    WhiteButton,
    Dialog,
    BlueButton,
    RedButton
  },
  data() {
    // 定时时间验证
    var validateValue2 = (rule, value, callback) => {
      if (this.editForm.radio === '1') {
        if (this.editForm.value2 === '') {
          callback(new Error(this.$t('placeholder.timeReqired')))
        } else {
          callback()
        }
      } else {
        callback()
      }
    }
    return {
      AlgorithmList:[],
      pageNum: 1,
      pageSize :10,
      total: 0,
      ifDelete: true,
      multipleSelection: '',
      stopTaskId: '', // 选择中断的任务id
      dialogVisible:false,
      editVisible:false,
      editForm:{
        task_id: '',
        datasetTime: [],
        radio: '0',
        value2: ''
      },
      editRules: {
        datasetTime: [{ required: true, trigger: 'blur' }],
        value2: [{ validator: validateValue2, trigger: 'blur' }]
      },
      datasetTimeOption: {
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
      value2Option: {
        disabledDate(date) {
          return date.getTime() < Date.now()
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
    this.getTaskExecuteList()
  },
  methods: {
    handleStop(row) {
      this.stopTaskId = row.id
      this.dialogVisible = true
    },
    // 删除
    deleteTask() {
      if (!this.ifDelete) {
        this.$message.error('您当前选中项中包含waiting和running状态的任务，请先中断')
      } else if (this.multipleSelection === '') {
        this.$message.error('当前页您未选择删除项')
      }  else {
        const url = '/api/deleteExecuteTask'
        this.$http({
          method: 'post',
          url: url,
          data:JSON.stringify({
            'ids': this.multipleSelection
          })
        }).then((res) => {
          const resData = res.data
          if (resData.code === 0) {
            this.$message.success(resData.message)
            this.getTaskExecuteList()
          } else {
            this.$message.error(resData.message)
          }
        })
      }
      this.ifDelete = true
    },
    changeDialog(v) {
      this.dialogVisible = v
      this.editVisible = v
      this.resetEditForm()
    },
    resetEditForm() {
      for (const key in this.editForm) {
        if (key === 'radio') {
          this.editForm[key] = '0'
        } else {
          this.editForm[key] = ''
        }
      }
    },
    // 分页获取评估数据
    getTaskExecuteList() {
      const url = `/api/getTaskExecuteList?page=${this.pageNum}&page_size=${this.pageSize}`
      this.$http({
        method: 'get',
        url: url
      }).then((res) => {
        const resData = res.data
        if (resData.code === 0) {
          const list = resData.data.info
          this.AlgorithmList = list
          this.total = resData.data.total
        } else {
          this.$message.error(resData.message)
        }
      })
    },
    handleCurrentChange(val) {
      this.pageNum = val
      this.getTaskExecuteList()
    },
    // 批量删除
    handleSelectionChange(val) {
      const tableList = []
      this.ifDelete = true
      val.forEach((item) => {
        if (item.execute_status !== 'running' && item.execute_status !== 'waiting') {
          tableList.push(item.id)
        } else {
          this.ifDelete = false
        }
      })
      this.multipleSelection = tableList.join(',')
    },
    // 打开详情页面
    openDetail(row) {
      localStorage.setItem('taskId', row.id)
      this.$router.push({
        path: '/evaluateData/evaluateDataDetail'
      })
    },
    // http-再次执行
    executeTaskAgain() {
      this.$refs.editForm.validate(valid => {
        if (valid) {
          for (let i = 0; i < this.editForm.datasetTime.length; i++) {
            const timestamp = this.editForm.datasetTime[i]
            this.editForm.datasetTime[i] = Math.floor(timestamp / 1000)
          }
          const dataset_range = this.editForm.datasetTime.join(',')
          const url = '/api/executeTaskAgain'
          this.$http({
            method: 'post',
            url: url,
            data:JSON.stringify({
              'task_id': this.editForm.task_id,
              'dataset_range': dataset_range,
              'execute_type': this.editForm.radio,
              'start_time': Math.floor(this.editForm.value2 / 1000)
            })
          }).then((res) => {
            const resData = res.data
            if (resData.code === 0) {
              this.$message.success(resData.message)
              this.getTaskExecuteList()
              this.changeDialog(false)
            } else {
              this.$message.error(resData.message)
            }
          })
        }
      })
    },
    handleExecuteAgain(row) {
      this.editForm.task_id = row.id
      this.editVisible = true
    },
    // http-中断
    stopExecuteTask() {
      const url = '/api/stopExecuteTask'
      const param = new FormData()
      param.append('id', this.stopTaskId)
      this.$http({
        method: 'post',
        url: url,
        data: JSON.stringify({
          'id': this.stopTaskId
        })
      }).then((res) => {
        const resData = res.data
        if (resData.code === 0) {
          this.$message.success(resData.message)
        } else {
          this.$message.error(resData.message)
        }
        this.changeDialog(false)
        this.getTaskExecuteList()
      })
    }
  }

}
</script>

<style scoped>
.topButton{
  display: block;
  text-align: left;
  margin-bottom: 10px;
}
.dotCss{
  width: 8px;
  height:8px;
  margin-right:5px;
  border-radius: 50%;
  display: inline-block;
}
.dialogBut{
  width: 76px;
  height: 36px;
}
.imgDia{
  width: 20px;
  height: 20px;
  margin-right: 8px;
}
.dialogFir{
  display: flex;
  align-items: center;
  color: #222222;
  font-size: 16px;
  line-height: 25px;
}
.dialogSed{
  display: flex;
  color: #767676;
  font-size: 14px;
  margin: 12px 0 0 28px;
}
.inputWidth2{
  width: 250px;
  display: flex;
}
</style>
