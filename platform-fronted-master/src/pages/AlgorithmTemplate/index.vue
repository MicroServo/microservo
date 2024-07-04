<template>
  <structure3>
    <template #card-r-1>
      <div class="topButton">
        <BlueButton
          @click.native="openAdd()">
          {{ $t("algoTemplate.newAlgoTemplate") }}
        </BlueButton>
        <RedButton
          v-if="selection.length>0"
          @click.native="handleDelete">
          {{ $t("button.deleteSelect") }}
        </RedButton>
      </div>
      <el-table
        ref="multipleTable"
        :data="AlgorithmList"
        fit
        stripe
        highlight-current-row
        @selection-change="val => selection = val"
      >
        <el-table-column
          type="selection"
          width="45" />
        <el-table-column
          :label="$t('table.templateName')"
          prop="template_name"
        />
        <el-table-column
          :label="$t('table.creater')"
          prop="create_person"
          show-overflow-tooltip
        />
        <el-table-column
          :label="$t('table.createDate')"
          prop="create_time"
          show-overflow-tooltip
        />
        <el-table-column
          :label="$t('table.operate')"
          fixed="right"
        > <template slot-scope="{row}">
          <el-button
            type="text"
            @click="handleUpdate(row)">
            {{ $t("table.detail") }}
          </el-button>
          <el-button
            v-if="row.status!='deleted'"
            type="text"
            @click="handleEdit(row)">
            {{ $t("table.execute") }}
          </el-button>
        </template>
        </el-table-column>
      </el-table>
      <!-- 分页器 -->
      <el-pagination
        :current-page="pageNum"
        :page-size="pageSize"
        :total="total"
        style="margin-top: 16px;"
        background
        align="right"
        layout="total, prev, pager, next, jumper"
        @current-change="handleCurrentChange" />
      <!-- 新建算法模板dialog -->
      <Dialog
        :dialogVisible="addVisible"
        :title="$t('algoTemplate.newAlgoTemplate')"
        @changeDialog="changeDialog">
        <template slot="content">
          <el-form
            ref="addForm"
            :rules="addRules"
            :model="addForm"
            label-width="auto"
            label-position="left"
            width="300px">
            <el-form-item
              :label="$t('algoTemplate.templateName')"
              prop="template_name">
              <el-input
                v-model="addForm.template_name"
                :placeholder="$t('placeholder.templateName')"
                class="inputWidth"/>
            </el-form-item>
            <el-form-item
              :label="$t('algoTemplate.algoType')"
              prop="type">
              <el-select
                v-model="addForm.type"
                :placeholder="$t('placeholder.algoType')"
                class="inputWidth">
                <el-option
                  v-for="item in typeList"
                  :key="item.id"
                  :label="item.algorithm_type_name"
                  :value="item.id"/>
              </el-select>
            </el-form-item>
            <el-form-item
              :label="$t('algoTemplate.algo')"
              prop="algorithm_id">
              <el-select
                v-model="addForm.algorithm_id"
                :placeholder="$t('placeholder.algo')"
                class="inputWidth">
                <el-option
                  v-for="item in algorithmList"
                  :key="item.id"
                  :label="item.algorithm_name"
                  :value="item.id"/>
              </el-select>
            </el-form-item>
            <el-form-item
              :label="$t('algoTemplate.indicator')"
              prop="indicator_id">
              <el-select
                v-model="addForm.indicator_id"
                :placeholder="$t('placeholder.indicator')"
                class="inputWidth">
                <el-option
                  v-for="item in indicatorList"
                  :key="item.id"
                  :label="item.name"
                  :value="item.id"/>
              </el-select>
            </el-form-item>
          </el-form>
        </template>
        <template slot="footer">
          <WhiteButton
            @click.native="changeDialog(false)">{{ $t('button.cancel') }}</WhiteButton>
          <BlueButton
            @click.native="taskTemplateCreate()">{{ $t('button.confirm') }}</BlueButton>
        </template>
      </Dialog>
      <!-- 执行dialog -->
      <Dialog
        :dialogVisible="editVisible"
        :title="$t('algoTemplate.execute')"
        @changeDialog="changeDialog">
        <template slot="content">
          <el-form
            ref="editForm"
            :model="editForm"
            :rules="editRules"
            label-width="auto"
            label-position="left"
            width="300px">
            <el-form-item
              :label="$t('table.taskName')"
              prop="name">
              <el-input
                v-model="editForm.name"
                :placeholder="$t('placeholder.taskName')"
                class="inputWidth2"/>
            </el-form-item>
            <!-- 精确到分 -->
            <el-form-item
              :label="$t('algoTemplate.dataset')"
              prop="value1">
              <el-date-picker
                v-model="editForm.value1"
                :picker-options="value1Option"
                :start-placeholder="$t('placeholder.startTime')"
                :end-placeholder="$t('placeholder.endTime')"
                class="inputWidth2"
                type="datetimerange"
                value-format="timestamp"
                range-separator="-"/>
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
            @click.native="handleExecute()">{{ $t('button.confirm') }}</BlueButton>
        </template>
      </Dialog>
      <!-- 模板详情drawer -->
      <Drawer
        :drawer="drawerOpen"
        :title="$t('algoTemplate.templateDetail')"
        @changeDrawer="changeDrawer">
        <el-descriptions
          :column="2"
          :label-style="drawerLabel"
          :content-style="drawerContent"
          class="desCss">
          <el-descriptions-item :label="$t('algoTemplate.name')">{{ algorithmDetail.template_name }}</el-descriptions-item>
          <el-descriptions-item :label="$t('algoTemplate.algoType')">{{ algorithmDetail.algorithm_type }}</el-descriptions-item>
          <el-descriptions-item :label="$t('algoTemplate.algo')">{{ algorithmDetail.algorithm_name }}</el-descriptions-item>
          <el-descriptions-item :label="$t('algoTemplate.indicator')">{{ algorithmDetail.indicator }}</el-descriptions-item>
          <el-descriptions-item :label="$t('table.creater')">{{ algorithmDetail.create_person }}</el-descriptions-item>
          <el-descriptions-item :label="$t('table.createDate')">{{ algorithmDetail.create_time }}</el-descriptions-item>
        </el-descriptions>
      </Drawer>
      <!-- 中断dialog -->
      <Dialog
        :dialogVisible="deleteVisible"
        @changeDialog="changeDialog">
        <template slot="info">
          <div class="dialogFir">
            <img
              class="imgDia"
              src="@/assets/images/评估数据/warning.png">{{ $t('algoTemplate.deleteTemplate') }}
          </div>
          <div class="dialogSed">{{ $t('placeholder.noRecover') }}</div>
        </template>
        <template slot="footer">
          <WhiteButton
            @click.native="changeDialog(false)">{{ $t('button.cancel') }}</WhiteButton>
          <RedButton
            @click.native="deleteTaskTemplate()">{{ $t('button.confirm') }}</RedButton>
        </template>
      </Dialog>
    </template>

  </structure3>
</template>

<script>
import {
  formatDate
} from '@/utils/utils'
import {
  fetchAlgorithmType
} from '../../network/api/algorithm'
import WhiteButton from '@/components/button/whiteButton.vue'
import Dialog from '@/components/dialog/index.vue'
import BlueButton from '@/components/button/blueButton.vue'
import Drawer from '@/components/drawer/index.vue'
import structure3 from '@/components/structure/structure3.vue'
import RedButton from '@/components/button/redButton.vue'
export default {
  name: 'AlgorithmTemplate',
  components: {
    structure3,
    Drawer,
    BlueButton,
    Dialog,
    WhiteButton,
    RedButton
  },
  data() {
    // 定时时间验证
    var validateValue2 = (rule, value, callback) => {
      if (this.editForm.radio === '1') {
        if (this.editForm.value2 === '') {
          callback(new Error())
        } else {
          callback()
        }
      } else {
        callback()
      }
    }
    return {
      AlgorithmList:[],
      selection: [],
      addVisible:false,
      deleteVisible: false,
      pageNum: 1,
      pageSize: 10,
      total: 0,
      addForm: {
        template_name: '',
        type: '',
        algorithm_id:'',
        indicator_id:[]
      }, // 新增算法模板
      algorithmList:[], // 算法列表,
      indicatorList:[], // 评估列表,
      editVisible:false, // 执行明细
      editForm:{
        template_id: '',
        name: '',
        value1: [],
        radio: '0',
        value2: ''
      },
      typeList: [],
      drawerOpen:false, // 模板详情侧边栏
      algorithmDetail:{},
      drawerLabel:{
        'color': '#748C9A',
        'min-width': '70px'
      },
      drawerContent:{
        'color': '#374E5C',
        'min-width':'80px'
      },
      addRules: {
        template_name: [{ required: true, trigger: 'blur' }],
        type: [{ required: true, trigger: 'blur' }],
        algorithm_id: [{ required: true, trigger: 'blur' }],
        indicator_id: [{ required: true, trigger: 'blur' }]
      },
      editRules: {
        name: [{ required: true, trigger: 'blur' }],
        value1: [{ required: true, trigger: 'blur' }],
        value2: [{ validator: validateValue2, trigger: 'blur' }]
      },
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
      value2Option: {
        disabledDate(date) {
          return date.getTime() < Date.now()
        }
      }
    }
  },
  watch: {
    'addForm.type'(newVal, oldVal) {
      this.getAlgorithmByType()
      if (newVal !== '') {
        this.getIndicatorByAlgorithmType()
      }
    },
    'addForm.algorithm_id'(newVal, oldVal) {
      console.log(newVal)
    },
    'addForm.indicator_id'(newVal, oldVal) {
      console.log(newVal)
    }
  },
  mounted() {
    this.getTaskTemplateList()
    this.getAlgorithmType()
  },
  methods: {
    getAlgorithmType() {
      fetchAlgorithmType().then((res) => {
        this.typeList = res
      })
    },
    changeDialog(v) {
      this.addVisible = v
      this.editVisible = v
      this.deleteVisible = v
      this.resetAddForm()
      this.resetEditForm()
    },
    resetAddForm() {
      for (const key in this.addForm) {
        this.addForm[key] = ''
      }
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
    // open执行dialog
    handleEdit(row) {
      this.editForm.template_id = row.id
      this.editVisible = true
    },
    handleDelete() {
      this.deleteVisible = true
    },
    // 删除模板
    deleteTaskTemplate() {
      const url = '/api/deleteTaskTemplate'
      console.log(this.selection)
      const ids = this.selection.map((item) => item.id).join(',')
      this.$http({
        method: 'post',
        url: url,
        data:JSON.stringify({
          'ids': ids
        })
      }).then((res) => {
        const resData = res.data
        if (resData.code === 0) {
          this.$message.success(resData.message)
          this.getTaskTemplateList()
        } else {
          this.$message.error(resData.message)
        }
        this.deleteVisible = false
      })
    },
    changeDrawer(v) {
      this.drawerOpen = v
    },
    openAdd() {
      this.addVisible = true
      this.getAlgorithmByType()
    },
    addCancel() {
      this.addVisible = false
      this.resetAddForm()
    },
    handleCurrentChange(val) {
      this.pageNum = val
      console.log(val)
      this.getTaskTemplateList()
    },
    getAlgorithmByType() {
      const url = `/api/getAlgorithmByType?type=${this.addForm.type}`
      this.$http({
        method: 'get',
        url: url
      }).then((res) => {
        if (res.data.code === 0) {
          console.log(JSON.parse(res.data.data))
          this.algorithmList = JSON.parse(res.data.data)
        }
      })
    },
    // 根据算法id返回指标
    getIndicatorByAlgorithmType() {
      const url = `/api/getIndicatorByAlgorithmType?id=${this.addForm.type}`
      this.$http({
        method: 'get',
        url: url
      }).then((res) => {
        if (res.data.code === 0) {
          this.indicatorList = res.data.data
          console.log(this.indicatorList)
        }
      })
    },
    // 创建算法模版，算法和指标选择以后创建模版
    taskTemplateCreate() {
      this.$refs.addForm.validate(valid => {
        if (valid) {
          const url = '/api/taskTemplateCreate'
          this.$http({
            method: 'post',
            url: url,
            data:JSON.stringify({
              'template_name':this.addForm.template_name,
              'algorithm_id':this.addForm.algorithm_id,
              'indicator_id':this.addForm.indicator_id
            })
          }).then((res) => {
            const resData = res.data
            if (resData.code === 0) {
              this.$message.success(resData.message)
              this.resetAddForm()
              this.getTaskTemplateList()
            } else {
              this.$message.error(resData.message)
            }
            this.addVisible = false
          })
        }
      })
    },
    handleUpdate(row) {
      this.drawerOpen = true
      this.algorithmDetail = row
    },
    // 获取模板列表
    getTaskTemplateList() {
      const url = `/api/getTaskTemplateList?page=${this.pageNum}&page_size=${this.pageSize}`
      this.$http({
        method: 'get',
        url: url
      }).then((res) => {
        const resData = res.data
        if (resData.code === 0) {
          this.total = resData.data.total
          const list = resData.data.info
          for (let i = 0; i < list.length; i++) {
            list[i].create_time = formatDate(list[i].create_time)
          }
          this.AlgorithmList = list
        } else {
          this.$message.error(resData.message)
        }
      })
    },
    // 用户点击执行
    handleExecute() {
      this.$refs.editForm.validate(valid => {
        if (valid) {
          for (let i = 0; i < this.editForm.value1.length; i++) {
            const timestamp = this.editForm.value1[i]
            this.editForm.value1[i] = Math.floor(timestamp / 1000)
          }
          const dataset_range = this.editForm.value1.join(',')
          const url = '/api/executeTaskTemplate'
          this.$http({
            method: 'post',
            url: url,
            data:JSON.stringify({
              'template_id': this.editForm.template_id,
              'task_name': this.editForm.name,
              'dataset_range': dataset_range,
              'execute_type': this.editForm.radio,
              'start_time': Math.floor(this.editForm.value2 / 1000)
            })
          }).then((res) => {
            const resData = res.data
            if (resData.code === 0) {
              this.$message.success(resData.message)
              this.editVisible = false
              this.resetEditForm()
              this.getTaskTemplateList()
            } else {
              this.$message.error(resData.message)
            }
          })
        }
      })
    }
  }

}
</script>

<style scoped>
.topButton{
  display: block;
  width: auto;
  text-align: left;
  margin-bottom: 10px;
}
.inputWidth{
  width: 224px;
  display: flex;
}
.inputWidth2{
  width: 250px;
  display: flex;
}
.dialogCss{
  border-radius: 12px;
}
.dialogCss /deep/ .el-dialog__title{
  display: flex;
}
.my-label{
  color: #748C9A;
  width: 70px;
}
.my-content{
  color: #374E5C;
}
.desCss{
  margin-left: 16px;
  margin-right:16px
}
.drawerBut{
  position: absolute;
  bottom: 16px;
  right: 16px;
}
.desCss /deep/ .el-descriptions-item__container .el-descriptions-item__content, .el-descriptions-item__container .el-descriptions-item__label{
  display: block;
}
.my-class{
  margin-bottom: 5px;
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
</style>
