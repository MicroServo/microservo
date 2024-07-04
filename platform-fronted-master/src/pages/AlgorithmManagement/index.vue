<template>
  <structure3>
    <template #card-r-1>
      <el-row>
        <el-col
          :span="15"
          class="left-box">
          <!-- 三个按钮 -->
          <div class="top-button">
            <div class="card-title">
              <span>{{ $t('algoTemplate.algo') }}</span>
            </div>
            <div>
              <el-form
                :inline="true"
                size="small">
                <el-form-item>
                  <el-select
                    v-model="algorithm_type"
                    :placeholder="$t('placeholder.algoType')"
                    class="inputWidth2"
                    clearable
                    @change="changeAlgorithmType">
                    <el-option
                      v-for="item in typeList"
                      :key="item.id"
                      :label="item.algorithm_type_name"
                      :value="item.id"/>
                  </el-select>
                </el-form-item>
                <el-button
                  type="info"
                  @click="downloadAlgorithm">{{ $t('button.sample') }}</el-button>
                <el-button
                  type="info"
                  @click="exportDialog=true">
                  <i class="el-icon-download"/>
                  {{ $t('button.fileExport') }}
                </el-button>
                <BlueButton
                  :size="'inline'"
                  @click.native="importDialog=true">
                  <i class="el-icon-upload2"/>
                  {{ $t('button.import') }}
                </BlueButton>
              </el-form>
            </div>
          </div>
          <!-- 算法列表 -->
          <span
            v-for="(item,index) in algorithmList"
            :key="index"
            :value="index">
            <Card
              :name="item.algorithm_name"
              :storage="item.mem_limit"
              :cpu="item.cpu_count"
              :status="item.container_created"
              @openDeleteAlgorithm="deleteAlgorithmVisble=true,deleteAlgorithmName=item.algorithm_name"
              @openAlgorithmDetail="handleAlgorithmDetail(item)" />
          </span>
        </el-col>
        <!-- 评估指标列表 -->
        <el-col
          :span="9"
          class="right-box">
          <div class="card-title">
            <span>{{ $t('algoTemplate.rightTitle') }}</span>
          </div>
          <el-table
            :data="tableData"
            fit>
            <el-table-column
              :label="$t('table.indicatorName')"
              prop="indicator_name"/>
            <el-table-column
              :label="$t('table.operate')"
              prop="name"
              width="100">
              <template slot-scope="{row}">
                <el-button
                  type="text"
                  @click="handleIndicatorDetail(row)">{{ $t('table.detail') }}</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-col>
      </el-row>
      <!-- 算法详情drawer -->
      <Drawer
        :drawer="drawer"
        :title="$t('algo.detail')"
        @changeDrawer="changeDrawer">
        <DCard1
          :algorithm-detail="algorithmDetail"
        >
          <span v-if="algorithmDetail.container_created">
            <img
              :title="$t('button.restart')"
              src="../../assets/images/算法管理/算法详情/restart.png"
              @click="restartContainerVisble=true">
            <img
              :title="$t('button.delete')"
              src="../../assets/images/算法管理/算法详情/delete@2x.png"
              @click="deleteContainerVisble=true">
          </span>
          <img
            v-else
            :title="$t('button.start')"
            src="../../assets/images/算法管理/算法详情/create.png"
            @click="createVisible = true">
        </DCard1>
        <DCard2
          v-if="algorithmDetail.is_split">
          <img
            src="../../assets/images/算法管理/算法详情/cloud-sync@2x(1).png"
            @click="trainVisible=true;trainType=1">
          <img
            src="../../assets/images/算法管理/算法详情/delete@2x(1).png"
            @click="trainVisible=true;trainType=0">
        </DCard2>
        <Log
          :container-log="containerLog"
          :id="algorithmDetail.id"/>
      </Drawer>
      <!-- 评估指标详情drawer -->
      <Drawer
        :drawer="detailDrawer"
        :title="$t('table.detail')"
        @changeDrawer="changeDrawer"
      >
        <json-viewer
          :value="indicatorDetail"
          :expand-depth="5"
        />
      </Drawer>
      <!-- 配置文件导出dialog -->
      <Dialog
        :dialogVisible="exportDialog"
        :title="$t('button.fileExport')"
        @changeDialog="changeDialog">
        <template slot="content">
          <el-form
            :model="exportForm"
            label-position="left"
            label-width="auto">
            <el-form-item
              :label="$t('algo.splitornot')"
              prop="is_split">
              <el-radio
                v-model="exportForm.is_split"
                label="0">{{ $t('button.no') }}</el-radio>
              <el-radio
                v-model="exportForm.is_split"
                label="1">{{ $t('button.yes') }}</el-radio>
            </el-form-item>
          </el-form>
        </template>
        <template slot="footer">
          <WhiteButton
            @click.native="changeDialog(false)">{{ $t('button.cancel') }}</WhiteButton>
          <BlueButton
            @click.native="exportAlgorithm">{{ $t('button.confirm') }}</BlueButton>
        </template>
      </Dialog>
      <!-- 算法导入dialog -->
      <Dialog
        :dialogVisible="importDialog"
        :title="$t('button.import')"
        @changeDialog="changeDialog">
        <template slot="content">
          <el-form
            ref="importForm"
            :model="importForm"
            :rules="importRules"
            label-position="left"
            label-width="auto">
            <el-form-item
              :label="$t('algo.name')"
              prop="algorithm_name">
              <el-input
                v-model="importForm.algorithm_name"
                :placeholder="$t('placeholder.alogoName')"
                class="inputWidth2"/>
            </el-form-item>
            <el-form-item
              :label="$t('algo.type')"
              prop="algorithm_type">
              <el-select
                v-model="importForm.algorithm_type"
                :placeholder="$t('placeholder.algoType')"
                class="inputWidth2">
                <el-option
                  v-for="item in typeList"
                  :key="item.id"
                  :label="item.algorithm_type_name"
                  :value="item.id"/>
              </el-select>
            </el-form-item>
            <el-form-item
              :label="$t('algo.dataType')"
              prop="dataset_type">
              <el-select
                v-model="importForm.dataset_type"
                :placeholder="$t('placeholder.dataType')"
                multiple
                class="inputWidth2">
                <el-option
                  v-for="item in dataTypeList"
                  :key="item.id"
                  :label="item.name"
                  :value="item.id"/>
              </el-select>
            </el-form-item>
            <!-- <el-form-item
              :label="$t('algoTemplate.indicator')"
              prop="indicator_name">
              <el-select
                v-model="importForm.indicator_name"
                :placeholder="$t('placeholder.indicator')"
                class="inputWidth2">
                <el-option
                  v-for="item in tableData"
                  :key="item.indicator_name"
                  :label="item.indicator_name"
                  :value="item.indicator_name"/>
              </el-select>
            </el-form-item> -->
            <el-form-item
              :label="$t('algo.splitornot')"
              prop="is_split"
              label-width="auto">
              <el-radio
                v-model="importForm.is_split"
                label="0">{{ $t('button.no') }}</el-radio>
              <el-radio
                v-model="importForm.is_split"
                label="1">{{ $t('button.yes') }}</el-radio>
            </el-form-item>
            <el-form-item
              :label="$t('algo.upload')"
              prop="uploaded_file">
              <el-upload
                :limit="1"
                :file-list="importForm.uploaded_file"
                :before-upload="beforeUpload"
                :auto-upload="false"
                :on-change="changeFile"
                accept=".zip"
                action="">
                <el-button
                  size="small"
                  type="primary">{{ $t('button.upload') }}</el-button>
                <span>{{ $t('placeholder.fileType') }}</span>
              </el-upload>
            </el-form-item>
          </el-form>
        </template>
        <template slot="footer">
          <WhiteButton
            @click.native="changeDialog(false)">{{ $t('button.cancel') }}</WhiteButton>
          <BlueButton
            :loading="importLoading"
            @click.native="handleImport">{{ $t('button.confirm') }}</BlueButton>
        </template>
      </Dialog>
      <!-- 创建容器dialog -->
      <Dialog
        :dialogVisible="createVisible"
        :title="$t('container.create')"
        @changeDialog="changeDialog">
        <template slot="content">
          <el-form
            :model="createForm"
            label-position="left"
            label-width="auto">
            <el-form-item
              label="cpu"
              prop="cpu_count">
              <el-input-number
                v-model="createForm.cpu_count"
                :min="1"
                :max="32"
                :label="$t('container.cpu')" />
            </el-form-item>
            <el-form-item
              :label="$t('container.mem')"
              prop="mem_limit">
              <el-input-number
                v-model="createForm.mem_limit"
                :min="1"
                :max="64"
                :label="$t('container.mem')" />
            </el-form-item>
          </el-form>
        </template>
        <template slot="footer">
          <WhiteButton
            @click.native="changeDialog(false)">{{ $t('button.cancel') }}</WhiteButton>
          <BlueButton
            @click.native="handleCreateContainer">{{ $t('button.confirm') }}</BlueButton>
        </template>
      </Dialog>
      <!-- 删除容器dialog -->
      <Dialog
        :dialogVisible="deleteContainerVisble"
        @changeDialog="changeDialog">
        <template slot="info">
          <div class="dialogFir">
            <img
              class="imgDia"
              src="@/assets/images/评估数据/warning.png">{{ $t('container.delete1') }}
          </div>
          <div class="dialogSed">{{ $t('container.delete2') }}</div>
        </template>
        <template slot="footer">
          <WhiteButton
            @click.native="changeDialog(false)">{{ $t('button.cancel') }}</WhiteButton>
          <RedButton
            @click.native="handleDeleteContainer()">{{ $t('button.delete') }}</RedButton>
        </template>
      </Dialog>
      <!-- 删除算法dialog -->
      <Dialog
        :dialogVisible="deleteAlgorithmVisble"
        @changeDialog="changeDialog">
        <template slot="info">
          <div class="dialogFir">
            <img
              class="imgDia"
              src="@/assets/images/评估数据/warning.png">{{ $t('container.delete1') }}
          </div>
          <div class="dialogSed">{{ $t('algo.delete') }}</div>
        </template>
        <template slot="footer">
          <WhiteButton
            @click.native="changeDialog(false)">{{ $t('button.cancel') }}</WhiteButton>
          <RedButton
            @click.native="handleDeleteAlgorithm()">{{ $t('button.delete') }}</RedButton>
        </template>
      </Dialog>
      <!-- 启动容器dialog -->
      <Dialog
        :dialogVisible="startContainerVisble"
        @changeDialog="changeDialog">
        <template slot="info">
          <div class="dialogFir">
            <img
              class="imgDia"
              src="@/assets/images/info.png">{{ $t('container.start1') }}
          </div>
          <div class="dialogSed">{{ $t('container.start2') }}</div>
        </template>
        <template slot="footer">
          <WhiteButton
            @click.native="changeDialog(false)">{{ $t('button.cancel') }}</WhiteButton>
          <BlueButton
            @click.native="handleStartContainer()">{{ $t('button.confirm') }}</BlueButton>
        </template>
      </Dialog>
      <!-- 重启容器dialog -->
      <Dialog
        :dialogVisible="restartContainerVisble"
        @changeDialog="changeDialog">
        <template slot="info">
          <div class="dialogFir">
            <img
              class="imgDia"
              src="@/assets/images/info.png">{{ $t('container.restart1') }}
          </div>
          <div class="dialogSed">{{ $t('container.restart2') }}</div>
        </template>
        <template slot="footer">
          <WhiteButton
            @click.native="changeDialog(false)">{{ $t('button.cancel') }}</WhiteButton>
          <BlueButton
            @click.native="handleRestartContainer()">{{ $t('button.confirm') }}</BlueButton>
        </template>
      </Dialog>
      <!-- 训练算法dialog -->
      <Dialog
        :dialogVisible="trainVisible"
        :title="trainTitle"
        @changeDialog="changeDialog">
        <template slot="content">
          <el-form
            ref="trainForm"
            :model="trainForm"
            :rules="trainRules"
            label-position="left"
            label-width="auto">
            <el-form-item
              :label="$t('table.taskName')"
              prop="task_name">
              <el-input
                v-model="trainForm.task_name"
                :placeholder="$t('placeholder.taskName')"
                class="inputWidth2"/>
            </el-form-item>
            <el-form-item
              :label="$t('algoTemplate.dataset')"
              prop="dataset_range">
              <el-date-picker
                v-model="trainForm.dataset_range"
                :picker-options="value1Option"
                :start-placeholder="$t('placeholder.startTime')"
                :end-placeholder="$t('placeholder.endTime')"
                class="inputWidth2"
                type="datetimerange"
                value-format="timestamp"
                range-separator="-"/>
            </el-form-item>
            <el-form-item
              v-if="trainType===1"
              :label="$t('algoTemplate.time')"
              prop="start_time">
              <el-date-picker
                :picker-options="value2Option"
                v-model="trainForm.start_time"
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
            @click.native="handleTrain">{{ $t('button.confirm') }}</BlueButton>
        </template>
      </Dialog>
    </template>
  </structure3>
</template>

<script>
import {
  downloadAlgorithm,
  exportAlgorithm,
  fetchAlgorithmType
} from '../../network/api/algorithm'
import { saveAs } from 'file-saver'
import RedButton from '@/components/button/redButton.vue'
import structure3 from '@/components/structure/structure3.vue'
import BlueButton from '@/components/button/blueButton.vue'
import WhiteButton from '@/components/button/whiteButton.vue'
import Dialog from '@/components/dialog/index.vue'
import Drawer from '@/components/drawer/index.vue'
import Card from '@/components/algorithm/card.vue'
import DCard1 from '@/components/algorithm/dCard1.vue'
import DCard2 from '@/components/algorithm/dCard2.vue'
import Log from '@/components/algorithm/log.vue'
export default {
  name: 'AlgorithmManagement',
  components: {
    structure3,
    BlueButton,
    WhiteButton,
    Card,
    Drawer,
    DCard1,
    DCard2,
    Log,
    Dialog,
    RedButton
  },
  data() {
    const validateFile = (rule, value, callback) => {
      if (this.importForm.uploaded_file.length === 0) {
        callback(new Error())
      } else {
        callback()
      }
    }
    return {
      drawer: false,
      detailDrawer: false,
      indicatorDetail: '',
      algorithmDetail: '',
      tableData: [],
      algorithmList:[],
      dialogVisible: false,
      importDialog: false,
      exportDialog: false,
      deleteContainerVisble: false,
      restartContainerVisble: false,
      startContainerVisble: false,
      deleteAlgorithmVisble: false,
      importLoading:false,
      deleteAlgorithmName: '',
      formLabelAlign: '',
      file1: [],
      file2: [],
      typeList: [],
      dataTypeList: [{
        id: 'metric',
        name: '指标'
      }, {
        id: 'log',
        name: '日志'
      }, {
        id: 'trace',
        name: '调用链'
      }
      ],
      importForm: { // 算法上传表单
        algorithm_name: '',
        algorithm_type: '',
        dataset_type: '',
        indicator_name: '',
        is_split: '0',
        uploaded_file: []
      },
      exportForm: {
        is_split: '0'
      },
      importRules: {
        algorithm_name: [{ required: true, trigger: 'blur' }],
        algorithm_type: [{ required: true, trigger: 'blur' }],
        dataset_type: [{ required: true, trigger: 'blur' }],
        indicator_name: [{ required: true, trigger: 'blur' }],
        uploaded_file: [{ required: true, validator: validateFile, trigger: 'blur' }]
      },
      trainForm:{
        task_name: '',
        dataset_range: '',
        start_time: ''
      },
      trainRule0: {
        task_name: [{ required: true, trigger: 'blur' }],
        dataset_range: [{ required: true, trigger: 'blur' }]
      },
      trainRule1: {
        task_name: [{ required: true, trigger: 'blur' }],
        dataset_range: [{ required: true, trigger: 'blur' }],
        start_time: [{ required: true, trigger: 'blur' }]
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
      },
      createVisible: false,
      createForm: {
        cpu_count: 1,
        mem_limit: 1
      },
      line_num: 20,
      containerLog: '',
      trainVisible: false,
      trainType: 0,
      algorithm_type: '',
      originList: [] // 原始算法列表
    }
  },
  computed: {
    trainTitle() {
      return this.trainType === 0 ? this.$t('container.instant_train') : this.$t('container.timed_train')
    },
    trainRules() {
      return this.trainType === 0 ? this.trainRule0 : this.trainRule1
    }
  },
  mounted() {
    this.algorithmFetch()
    this.indicatorsFetch()
    this.getAlgorithmType()
  },
  methods: {
    changeAlgorithmType() {
      this.algorithmList = []
      this.originList.forEach(item => {
        if (item.algorithm_type === this.algorithm_type || this.algorithm_type === '') {
          this.algorithmList.push(item) // 将符合条件的元素添加到新列表中
        }
      })
    },
    getAlgorithmType() {
      fetchAlgorithmType().then((res) => {
        this.typeList = res
      })
    },
    changeFile(file, fileList) {
      this.importForm.uploaded_file = file
    },
    // 更新算法详情
    updateAlgorithm() {
      if (this.algorithmDetail) {
        const algorithmList = this.algorithmList
        for (let i = 0; i < algorithmList.length; i++) {
          if (algorithmList[i].id === this.algorithmDetail.id) {
            this.algorithmDetail = algorithmList[i]
            this.getContainerLog()
          }
        }
      }
    },
    // http-创建容器
    handleCreateContainer() {
      const mem_limit = this.createForm.mem_limit + 'g'
      const url = '/api/container/start'
      this.$http({
        method: 'post',
        url: url,
        data:JSON.stringify({
          'algorithm_name': this.algorithmDetail.algorithm_name,
          'cpu_count': this.createForm.cpu_count,
          'mem_limit': mem_limit
        })
      }).then((res) => {
        const resData = res.data
        if (resData.code === 0) {
          this.$message.success(resData.message)
        } else {
          this.$message.error(resData.message)
        }
      }).catch((res) => {
        this.$message.error('容器创建失败')
      })
      this.changeDialog(false)
      this.algorithmFetch()
    },
    // 打开抽屉
    changeDrawer(v) {
      this.drawer = v
      this.detailDrawer = v
    },
    resetImportForm() {
      for (const key in this.importForm) {
        if (key === 'is_split') {
          this.importForm[key] = '0'
        } else if (key === 'uploaded_file') {
          this.importForm[key] = []
        } else {
          this.importForm[key] = ''
        }
      }
    },
    resetExportForm() {
      this.exportForm.is_split = 0
    },
    resetTrainForm() {
      for (const key in this.trainForm) {
        this.trainForm[key] = ''
      }
    },
    changeDialog(v) {
      this.exportDialog = v
      this.importDialog = v
      this.createVisible = v
      this.deleteContainerVisble = v
      this.restartContainerVisble = v
      this.startContainerVisble = v
      this.deleteAlgorithmVisble = v
      this.trainVisible = v
      this.resetImportForm()
      this.resetExportForm()
      this.resetTrainForm()
    },
    // 上传文件之前
    beforeUpload(file) {
      const fileSuffix = file.name.substring(file.name.lastIndexOf('.') + 1)
      if (fileSuffix !== 'zip') {
        this.$message.error('您需要上传zip格式的文件')
        return false
      }
    },
    handleTrain() {
      this.$refs.trainForm.validate(valid => {
        if (valid) {
          let url = ''
          const range = this.trainForm.dataset_range.map(num => Math.ceil(num / 1000))
          const dataset_range = range.join(',')
          const start_time =  Math.ceil(this.trainForm.start_time / 1000)
          if (this.trainType === 0) {
            url =  `/api/algorithm/trainalgorithm?algorithm_id=${this.algorithmDetail.id}&task_name=${this.trainForm.task_name}&dataset_range=${dataset_range}&execute_type=0`
          } else {
            // 定时
            url =  `/api/algorithm/trainalgorithm?algorithm_id=${this.algorithmDetail.id}&task_name=${this.trainForm.task_name}&dataset_range=${dataset_range}&execute_type=1&start_time=${start_time}`
          }
          this.trainAlgotihtm(url)
        }
      })
    },
    // 训练算法
    trainAlgotihtm(url) {
      this.$http({
        method: 'get',
        url: url
      }).then((res) => {
        const resData = res.data
        if (resData.code === 0) {
          this.$message.success(resData.message)
        } else {
          this.$message.error(resData.message)
        }
      })
      this.trainVisible = false
    },
    // 获取算法
    algorithmFetch() {
      const url = '/api/algorithm/fetch'
      this.$http({
        method: 'get',
        url: url
      }).then((res) => {
        const resData = res.data
        if (resData.code === 0) {
          const list = resData.data
          for (let i = 0; i < list.length; i++) {
            if (list[i].mem_limit) {
              list[i].mem_limit = list[i].mem_limit.replace('g', '')
            }
          }
          this.originList = resData.data
          this.algorithmList = resData.data
          this.updateAlgorithm()
        }
      })
    },
    // 获取评估指标列表
    indicatorsFetch() {
      const url = '/api/indicators/fetch'
      this.$http({
        method: 'get',
        url: url
      }).then((res) => {
        const resData = res.data
        if (resData.code === 0) {
          this.tableData = resData.data
        }
      })
    },
    // 查看评估指标详情
    handleIndicatorDetail(row) {
      this.detailDrawer = true
      const str = row.format_json.replaceAll('\'', '\"')
      this.indicatorDetail = JSON.parse(str)
    },
    // 查看算法详情
    handleAlgorithmDetail(row) {
      this.algorithmDetail = row
      this.containerLog = ''
      this.getContainerLog()
      this.drawer = true
    },
    // 配置文件导出
    exportAlgorithm() {
      exportAlgorithm({
        is_split: this.exportForm.is_split
      }).then((res) => {
        let name = 'algorithmTemplate_issplit.zip'
        if (this.exportForm.is_split === 0) {
          name = 'algorithmTemplate_nosplit.zip'
        }
        saveAs(new Blob([res]), name)
        this.changeDialog(false)
      })
    },
    // 样例数据集下载
    downloadAlgorithm() {
      downloadAlgorithm().then((res) => {
        console.log(res)
        saveAs(new Blob([res]), 'dataset.zip')
        this.changeDialog(false)
      })
    },
    // 删除容器
    handleDeleteContainer() {
      this.changeDialog(false)
      const url = '/api/container/delete'
      this.$http({
        method: 'post',
        url: url,
        data:JSON.stringify({
          'algorithm_name': this.algorithmDetail.algorithm_name
        })
      }).then((res) => {
        const resData = res.data
        if (resData.code === 0) {
          this.$message.success(resData.message)
        } else {
          this.$message.error(resData.message)
        }
        this.algorithmFetch()
      })
    },
    // http-删除算法
    handleDeleteAlgorithm() {
      const url = '/api/algorithm/delete'
      this.$http({
        method: 'post',
        url: url,
        data:JSON.stringify({
          'algorithm_name': this.deleteAlgorithmName
        })
      }).then((res) => {
        const resData = res.data
        if (resData.code === 0) {
          this.$message.success(resData.message)
        } else {
          this.$message.error(resData.message)
        }
        this.changeDialog(false)
        this.algorithmFetch()
      })
    },
    handleStartContainer() {
      const url = '/api/container/start'
      this.$http({
        method: 'post',
        url: url,
        data:JSON.stringify({
          'algorithm_name': this.algorithmDetail.algorithm_name
        })
      }).then((res) => {
        const resData = res.data
        if (resData.code === 0) {
          this.$message.success(resData.message)
        } else {
          this.$message.error(resData.message)
        }
        this.changeDialog(false)
        this.algorithmFetch()
      })
    },
    // http-重启容器
    handleRestartContainer() {
      const url = '/api/container/restart'
      this.$http({
        method: 'post',
        url: url,
        data:JSON.stringify({
          'algorithm_name': this.algorithmDetail.algorithm_name
        })
      }).then((res) => {
        const resData = res.data
        if (resData.code === 0) {
          this.$message.success(resData.message)
        } else {
          this.$message.error(resData.message)
        }
        this.changeDialog(false)
        this.algorithmFetch()
      })
    },
    // 导入算法
    handleImport() {
      this.$refs.importForm.validate(valid => {
        if (valid) {
          this.importLoading = true
          const param = new FormData()
          param.append('algorithm_name', this.importForm.algorithm_name)
          param.append('algorithm_type', this.importForm.algorithm_type)
          // param.append('indicator_name', this.importForm.indicator_name)
          param.append('dataset_type', this.importForm.dataset_type.join(','))
          param.append('is_split', this.importForm.is_split)
          param.append('uploaded_file', this.importForm.uploaded_file.raw)
          const url = '/api/algorithm/import'
          this.$http({
            method: 'post',
            url: url,
            headers:{
              'Content-Type':'multipart/form-data'
            },
            data:param
          }).then((res) => {
            const resData = res.data
            if (resData.code === 0) {
              this.$message.success(resData.message)
            } else {
              this.$message.error(resData.message)
            }
            this.changeDialog(false)
            this.algorithmFetch()
            this.importLoading = false
          })
        }
      })
    },
    // 获取容器日志
    getContainerLog() {
      const url =  `/api/container/getContainerLog?line_num=${this.line_num}&id=${this.algorithmDetail.id}`
      this.$http({
        method: 'get',
        url: url
      }).then((res) => {
        const resData = res.data
        if (resData.code === 0) {
          this.containerLog = resData.data
        } else {
          this.$message.error(resData.message)
        }
      }).catch((res) => {
        this.$message.error('获取日志失败')
      })
    }
  }

}
</script>

<style scoped>
.left-box{
  /* border-right: 1px #E9EBF2 solid; */
  padding-right: 15px;
  text-align: left;
}
.right-box{
  margin-top: 10px;
}
.top-button{
  margin-top: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.top-button /deep/ .el-button{
  border:none;
  border-radius: 12px;
  padding: 11px 12px;
  /* background: #EDF0F2; */
}
.top-button /deep/ .el-button--info{
  background-color: #EDF0F2;
  color: #374E5C;
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
