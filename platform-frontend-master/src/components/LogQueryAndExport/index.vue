<template>
  <div class="logQAE-container">
    <header>
      <el-date-picker
        v-model="duration"
        :disabled-date="judge"
        :picker-options="pickerOptions"
        type="datetimerange"
        start-placeholder="Start date"
        end-placeholder="End date"
        size="mini"
      />
      <el-button
        :disabled="!duration"
        size="mini"
        @click="logDataQuery"
      >
        <span O-R>{{ $t('button.search') }}</span>
        <template #icon>
          <Search />
        </template>
      </el-button>
      <el-input
        v-model="search"
        :placeholder="$t('dataMonitor.infoSearch')"
        :disabled="!duration"
        style="width: 140px"
        size="mini"
        @input="searchChange"
      />
      <el-select
        v-model="selectedPodName"
        :title="$t('dataMonitor.podnameClassify')"
        placeholder="Select"
        style="width: 140px"
        size="mini"
      >
        <el-option
          v-for="item in options"
          :key="item"
          :label="item"
          :value="item"
        />
      </el-select>
      <el-button
        :disabled="!duration"
        :title="$t('dataMonitor.logExport')"
        style="float: right; margin: 0;"
        size="mini"
        @click="logDataExport"
      >
        <span O-R>{{ $t('button.download') }}</span>
      </el-button>
    </header>
    <main class="table-box">
      <el-table
        :data="tableData"
        height="100%"
        style="width: 100%"
      >
        <el-table-column
          prop="id"
          label="ID"
          width="250"
        />
        <el-table-column
          prop="podName"
          label="PodName"
          width="250"
        />
        <el-table-column
          :label="$t('dataMonitor.time')"
          prop="time"
          width="180"
        />
        <el-table-column
          :label="$t('dataMonitor.info')">
          <template #default="scope">
            <article class="LQAE-article">
              <el-tooltip
                placement="top"
                effect="light"
              >
                <template #content>
                  <span
                    class="LogQAE__popper"
                    v-html="scope.row.showMessage"
                  />
                </template>
                <span
                  truncated
                >
                  <span v-html="scope.row.showMessage" />
                </span>
              </el-tooltip>
            </article>
          </template>
        </el-table-column>
        <el-table-column
          :label="$t('dataMonitor.operate')"
          width="120"
        >
          <template #default="scope">
            <el-button
              type="text"
              @click="showLogDetail(scope.row)"
            >{{ $t('table.detail') }}</el-button>
          </template>
        </el-table-column>
      </el-table>
    </main>
    <footer>
      <el-pagination
        :current-page.sync="currentPage"
        :page-size.sync="pageSize"
        :page-sizes="[5, 10, 15, 20]"
        :small="small"
        :disabled="disabled"
        :background="background"
        :total="total"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </footer>
    <Drawer
      :drawer="showDetail"
      :title="$t('table.detail')"
      @changeDrawer="(val) => {showDetail = val}"
    >
      <json-viewer
        :value="logData"
        :expand-depth="5"
      />
    </Drawer>
    <!-- <PlatformDrawer
      :visible="showDetail"
      :body="true"
      title="日志预览"
      size="700px"
      @changeVisible="(val) => {showDetail = val}"
    >
      <JsonViewer
        :value="logData"
        class="platform-json-viewer"
        theme="my-json-theme"
        copyable
        boxed
      />
    </PlatformDrawer> -->
  </div>
</template>

<script>
import { getPodList } from '@/network/api/metric'
import { saveAs } from 'file-saver'
import PlatformDrawer from '@/components/PlatformDrawer'
import JsonViewer from 'vue-json-viewer'
import { getLog, downloadLog } from '@/network/api/log'
import { judgeDuration, message } from '@/utils/utils'
import Drawer from '@/components/drawer/index.vue'
export default {
  components: {
    PlatformDrawer,
    JsonViewer,
    Drawer
  },
  data() {
    return {
      duration: null,
      search: '',
      currentPage: 1,
      pageSize: 10,
      small: false,
      background: false,
      disabled: false,
      showDetail: false,
      logData: {},
      logList: [],
      selectedPodName: 'all',
      options: ['all'],
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
    tableData() {
      let showData = []
      if (this.selectedPodName === 'all') showData =  this.logList
      else showData = this.logList.filter((item) => item.podName === this.selectedPodName)
      if (this.search !== '') showData = showData.filter((item) => item.message.toLowerCase().indexOf(this.search.toLowerCase()) !== -1)
      showData.forEach((data) => {
        data.showMessage = this.replace(data.message)
      })
      return showData.slice((this.currentPage - 1) * this.pageSize, this.currentPage * this.pageSize)
    },
    total() {
      const showData = this.logList.filter((item) => this.selectedPodName === 'all' ? true : item.podName === this.selectedPodName)
      if (this.search === '') return showData.length
      else return showData.filter((item) => item.message.toLowerCase().indexOf(this.search.toLowerCase()) !== -1).length
    }
  },
  mounted() {
    getPodList().then((res) => {
      this.options = this.options.concat(res)
    })
  },
  methods: {
    judge(date) {
      return date.getTime() >= Date.now()
    },
    handleSizeChange() {
      //
    },
    handleCurrentChange() {
      //
    },
    replace(str) {
      // 大小写不敏感匹配时，保留原有数据
      let lowerStr = str.toLowerCase()
      const lowerSearch = this.search.toLowerCase()
      if (!lowerSearch) return str
      const before = '<span search-results>'
      const after = '</span>'
      let startPos = 0
      while (startPos < lowerStr.length) {
        const index = lowerStr.indexOf(lowerSearch, startPos)
        if (index === -1) break
        const target = str.slice(index, index + lowerSearch.length)
        str = str.slice(0, index) + before + target + after + str.slice(index + lowerSearch.length)
        lowerStr = lowerStr.slice(0, index) + before + target + after + lowerStr.slice(index + lowerSearch.length)
        startPos = index + before.length + lowerSearch.length + after.length
      }
      return str
    },
    showLogDetail(row) {
      console.log(row)
      this.logData = row.detail
      this.showDetail = true
    },
    logDataExport() {
      // 日志数据导出
      const startTime = Math.floor(this.duration[0].getTime() / 1000)
      const endTime = Math.floor(this.duration[1].getTime() / 1000)
      downloadLog({
        start_time: startTime,
        end_time: endTime
      }).then((res) => {
        saveAs(new Blob([res]), 'data.zip')
      })
    },
    logDataQuery() {
      // 日志数据查询
      if (!this.duration) return
      const startTime = this.duration[0].getTime()
      const endTime = this.duration[1].getTime()
      if (judgeDuration(startTime, endTime, 15)) {
        this.search = ''
        this.selectedPodName = 'all'
        const loading = this.$loading({
          lock: true, // lock的修改符--默认是false
          text: 'loading', // 显示在加载图标下方的加载文案
          spinner: 'el-icon-loading', // 自定义加载图标类名
          background: 'white', // 遮罩层颜色
          target: document.querySelector('.table-box') // loadin覆盖的dom元素节点
        })
        getLog({
          node: 'minikube',
          start_time: Math.floor(startTime / 1000),
          end_time: Math.floor(endTime / 1000)
        }).then((res) => {
          this.logList = this.initLogData(res || [])
          loading.close()
        }).catch((err) => {
          this.logList = this.initLogData([])
          message(err.message)
          loading.close()
        })
      }
    },
    initLogData(data) {
      return data.map((item) => {
        return {
          id: item._id,
          podName: item._source.kubernetes.pod.name,
          time: new Date(item._source['@timestamp']).toLocaleString(),
          message: item._source.message,
          showMessage: item._source.message,
          detail: item
        }
      })
    },
    searchChange() {
      // if (!CSS.highlights) {
      //   message('CSS Custom Highlight API not supported.')
      //   return
      // }
      // CSS.highlights.clear()
      // const str = this.search.toLowerCase()
      // if (!str) return
      // this.$nextTick(() => {
      //   const articles = document.getElementsByClassName('LQAE-article')
      //   if (!articles) return
      //   const allTextNodes = []
      //   for (const article of articles) {
      //     const treeWalker = document.createTreeWalker(article, NodeFilter.SHOW_TEXT)
      //     let currentNode = treeWalker.nextNode()
      //     while (currentNode) {
      //       allTextNodes.push(currentNode)
      //       currentNode = treeWalker.nextNode()
      //     }
      //   }
      //   const ranges = allTextNodes
      //     .map((el) => {
      //       return { el, text: el.textContent.toLowerCase() }
      //     })
      //     .map(({ text, el }) => {
      //       const indices = []
      //       let startPos = 0
      //       while (startPos < text.length) {
      //         const index = text.indexOf(str, startPos)
      //         if (index === -1) break
      //         indices.push(index)
      //         startPos = index + str.length
      //       }

      //       // Create a range object for each instance of
      //       // str we found in the text node.
      //       return indices.map((index) => {
      //         const range = new Range()
      //         range.setStart(el, index)
      //         range.setEnd(el, index + str.length)
      //         return range
      //       })
      //     })

      //   // Create a Highlight object for the ranges.
      //   const searchResultsHighlight = new Highlight(...ranges.flat())

      //   // Register the Highlight object in the registry.
      //   CSS.highlights.set('search-results', searchResultsHighlight)
      // })
    }
  }
}
</script>

<style>
.logQAE-container {
  position: relative;
  height: 100%;
}
.logQAE-container > header {
  text-align: left;
  padding: 5px 10px;
  height: 42px;
  box-sizing: border-box;
}
.logQAE-container > header > * {
  margin-right: 10px;
}
.logQAE-container > footer {
  display: flex;
  justify-content: flex-end;
  padding: 5px 10px;
  height: 42px;
  box-sizing: border-box;
}
.logQAE-container > main {
  display: block;
  height: calc(100% - 42px * 2);
}
.LogQAE__popper {
  display: inline-block;
  max-width: 300px !important;
  max-height: 200px !important;
  overflow: auto;
}
</style>
