<template>
    <div class="logdata-select-bar">
        <!-- search这个div就是最上面横的这一栏，这部分比较简单，但是需要对于样式进行一些修改 -->
        <div class="select-time">
            <!-- 这里是用来选择日期的 -->
            <el-date-picker class="timePicker" v-model="time" type="datetimerange" range-separator="至"
                start-placeholder="开始日期" end-placeholder="结束日期" :picker-options="picherOptions" tabindex="1"
                @change="searchData" />
        </div>
        <div class="search">
            <div class="form">
                <div class="form-item">
                    <div class="select-Podname">
                        Podname:
                        <el-select v-model="selectedPodname" placeholder="请选择" @change="filterData">
                            <el-option v-for="option in podname_options" :key="option.value" :value="option.value">
                            </el-option>
                        </el-select>
                    </div>
                    <div class="search-value">
                        <svg-icon icon-class="info" class-name="info-class" title="infomation" />
                        内容关键词：
                        <el-input ref="searchvalue" v-model="searchvalue" placeholder="请输入" tabindex="2"
                            @input="filterData" @keyup.enter.native="filterData" clearble />
                    </div>
                    <div class="remove-value">
                        内容不包含的关键词：
                        <el-input ref="removevalue" v-model="removevalue" placeholder="请输入" tabindex="2"
                            @keyup.enter.native="filterData" clearble />
                    </div>
                </div>
            </div>
            <!-- 下面这个就是之前的下载的逻辑 -->
            <div class="botton-item" style="margin-left:400px;">
                <DownloadProgress ref="downloadProgress" v-if="hasDownload"></DownloadProgress>
            </div>
            <div class="botton-item">
                <div class="download">
                    <el-button type="info" plain size="medium" class="download-button" @click="downloadLog"
                        :loading="downloadLoading">
                        <svg-icon icon-class="excel" class-name="excel-class" />
                        导出
                    </el-button>
                </div>
            </div>
        </div>
        <!-- 这个部分是用来展示搜索的表格的，但是一开始的时候这个表格先不显示 -->
        <div class="gray-rounded-rectangle" v-if="tableVisible">
            <el-card shadow="hover">
                <el-table v-loading="loading" class="logtable" :data="pagedData" :element-loading-text="loadingText"
                    @filter-change="handleFilterChange">
                    <el-table-column prop="id" label="ID" width="auto" />
                    <el-table-column prop="podname" label="PodName" width="auto" :filters="podFilter"
                        :filter-method="filterHandler" />
                    <el-table-column prop="time" label="时间" width="auto" />
                    <el-table-column prop="message" label="信息" width="auto">
                        <template slot-scope="scope">
                            <el-tooltip placement="top" effect="light">
                                <div slot="content">
                                    <div v-html="scope.row.message"></div>
                                </div>
                                <div v-html="scope.row.message" class="messageDiv"></div>
                            </el-tooltip>
                        </template>
                    </el-table-column>

                    <el-table-column label="操作" align="right">
                        <template slot-scope="scope">
                            <el-button style="border:none; color: #25b3cc;" size="mini"
                                @click="getDetails(scope.row)">查看message</el-button>
                        </template>
                    </el-table-column>
                </el-table>
                <el-pagination layout="-> , prev , pager , next , jumper" :current-page="currentPage"
                    :page-size="pageSize" :total="logTableData.length" @current-change="handleCurrentChange" />
            </el-card>
        </div>
        <!-- 这个部分就是最下面的Log数据量展示的部分 -->
        <div class="gray-rounded-rectangle">
            <el-card shadow="hover">
                <div id="podchart" style="height: 350px" />
            </el-card>
        </div>

    </div>
</template>

<script>
import { mapGetters } from 'vuex'
import { getLogNum } from '@/assets/js/log'
import { getLog } from '@/assets/js/log'
import * as echarts from 'echarts'
import websocket from '@/assets/js/websocket'
import DownloadProgress from '@/components/DownloadProgress'

export default {
    name: 'DataMonitorLog',
    data() {
        return {
            hasDownload: false, // 
            downloadLoading: false, // 是否正在下载
            // 表格数据
            logTableData: [],
            //真正展示出来的数据（也就是经过podName筛选出的数据）
            showData: [],
            // 表格响应loading辅助数据
            loading: false,
            loadingText: 'Loading...',
            // 时间日期选择器
            picherOptions: {
                disabledDate(date) {
                    // disabledDate 文档上：设置禁用状态，参数为当前日期，要求返回 Boolean
                    return (
                        date.getTime() > Date.now()
                    )
                },
                // 这个是要用来帮助快速选择的一个方式
                shortcuts: [{
                    text: '最近一分钟',
                    onClick(picker) {
                        const end = new Date()
                        const start = new Date()
                        start.setTime(start.getTime() - 1000 * 60 * 1)
                        picker.$emit('pick', [start, end])
                    }
                }, {
                    text: '最近五分钟',
                    onClick(picker) {
                        const end = new Date()
                        const start = new Date()
                        start.setTime(start.getTime() - 1000 * 60 * 5)
                        picker.$emit('pick', [start, end])
                    }
                }, {
                    text: '最近十分钟',
                    onClick(picker) {
                        const end = new Date()
                        const start = new Date()
                        start.setTime(start.getTime() - 1000 * 60 * 10)
                        picker.$emit('pick', [start, end])
                    }
                }]
            },
            // Podname下拉框选项
            podname_options: [
                { value: 'cartservice' },
                { value: 'checkoutservice' },
                { value: 'currencyservice' },
                { value: 'emailservice' },
                { value: 'frontend' },
                { value: 'paymentservice' },
                { value: 'productcatalogservice' },
                { value: 'recommendationservice' },
                { value: 'redis' },
                { value: 'shippingservice' }
            ],
            searchkey: '',
            searchvalue: '',
            removevalue: '',
            time: '',
            selectedPodname: '',
            searchtable: '',
            // 后台返回的图表数据
            chart_data: [],
            // 后台返回的表格数据
            table_data: [],
            // 后台返回数据进行筛选后的数据
            filter_table_data: [],
            // 分页相关数据
            currentPage: 1, // 当前页码
            pageSize: 10, // 每页显示的数据条数
            tableVisible: false, //搜索表格是否可视
            podFilter: [], // 统计podname
            currentFilters: {}// 用于存储当前的筛选条件
        }
    },

    components: {
        DownloadProgress
    },

    computed: {
        ...mapGetters([
            'name'
        ]),

        // 分页信息函数
        pagedData() {
            const startIndex = (this.currentPage - 1) * this.pageSize
            const endIndex = startIndex + this.pageSize
            return this.logTableData.slice(startIndex, endIndex)
        }
    },

    mounted() {
        getLogNum()
            .then(res => {
                console.log('log num', res)
                this.chart_data = res.slice(-14)
                this.drawChart(this.chart_data)
            })
            .catch(error => {
                console.error('获取日志数量失败:', error)
            })
    },

    methods: {
        /**
        * @description: 将时间戳转换成日期
        * @param: 传入的时间戳
        * @return 返回日期
        */
        handleDate(n) {
            n = new Date(n)
            return n.toLocaleDateString().replace(/\//g, "-") + " " + n.toTimeString().substr(0, 8)
        },

        /**
        * @description: podname选择
        * @param value: 被选择的Podname的值
        * @param row: 表格中的一行
        * @return boolean值，判断这一行的podname是否是选择的value
        */
        filterHandler(value, row, column) {
            return row.podname === value;
        },

        /**
        * @description: 获取podname的种类
        * @return void
        */
        getPodnameType() {
            let data = this.logTableData
            let res = []
            data.forEach(item => {
                res.push(item.podname)
            })
            res = Array.from(new Set(res))
            let podFilter = []
            for (let i = 0; i < res.length; i++) {
                podFilter.push({
                    text: res[i],
                    value: res[i]
                })
            }
            this.podFilter = podFilter
        },
        /**
        * @description: 在message中对用户的搜索词进行高亮
        * @param text: 表示这一行的文本信息，把其中的筛选词高亮显示
        * @return 高亮的搜索词和文本
        */
        hightLightText(text) {
            if (text) {
                const regExp = new RegExp(this.searchvalue, 'g')
                return text.replace(regExp, `<span style="background: yellow;">${this.searchvalue}</span>`)
            }
            else
                return text;
        },


        /**
        * @description: 跳转到message详情页
        * @param row: 表示目前是哪一行的详情要被点击
        * @return void
        */
        getDetails(row) {
            const newData = {
                detail: row.detail
            }

            this.$router.push({
                name: 'LogDetail',
                query: { newData: JSON.stringify(newData) }
            })

            this.$store.commit('saveData', this.data)
        },
        /**
        * @description: 在日志页面，对于需要过滤的数据进行过滤的操作
        * @return void
        */
        handleFilterChange(filters) {
            console.log(filters)
            this.currentFilters = filters
            this.filterDataPod()
        },
        /**
        * @description:   日志页面功能，对已过滤数据再进行PodName过滤并显示在表格上
        * @return void
        */
        filterDataPod() {
            console.log("filter")
            if (Object.keys(this.currentFilters).length > 0) {
                this.showData = this.logTableData.filter((item) => {
                    return Object.keys(this.currentFilters).every((key) => {
                        return item[key] === this.currentFilters[key];
                    });
                });
            } else {
                // 没有筛选条件时，使用所有数据
                this.showData = Array.from(this.logTableData);
            }

            // 重新计算分页数据
            this.getPodnameType(); // 可能需要重新计算 podFilter
            console.log(showData)
            console.log("这是showdata")
        },
        /**
        * @description:   日志页面功能，对后端数据过滤 并显示在表格上,不仅要保留searchvalue，还要去掉removevalue,并且这里还要筛选掉下拉框的选项
        * @return void
        */
        filterData() {
            // 先保留searchvalue
            if (this.searchvalue !== '') {
                this.filter_table_data = this.table_data.map(item => {
                    return {
                        id: item._id,
                        podname: item._source.kubernetes.labels.app,
                        time: this.handleDate(item._source['@timestamp']),
                        message: this.hightLightText(item._source.message),
                        detail: item
                    }
                }).filter(item2 => item2.message.includes(this.searchvalue))
            } else {
                this.filter_table_data = this.table_data.map(item => {
                    return {
                        id: item._id,
                        podname: item._source.kubernetes.labels.app,
                        time: this.handleDate(item._source['@timestamp']),
                        message: item._source.message,
                        detail: item
                    }
                })
            }
            // 再过滤removevalue
            if (this.removevalue !== '') {
                this.filter_table_data = this.filter_table_data.map(item => {
                    return {
                        id: item.id,
                        podname: item.podname,
                        time: item.time,
                        message: item.message,
                        detail: item
                    }
                }).filter(item2 => !item2.message.includes(this.removevalue))
            } else {
                this.filter_table_data = this.filter_table_data.map(item => {
                    return {
                        id: item.id,
                        podname: item.podname,
                        time: item.time,
                        message: item.message,
                        detail: item
                    }
                })
            }
            // 再过滤Podname
            if (this.selectedPodname !== '') {
                this.filter_table_data = this.filter_table_data.map(item => {
                    return {
                        id: item.id,
                        podname: item.podname,
                        time: item.time,
                        message: item.message,
                        detail: item
                    }
                }).filter(item2 => item2.podname.includes(this.selectedPodname))
            }
            else {
                this.filter_table_data = this.filter_table_data.map(item => {
                    return {
                        id: item.id,
                        podname: item.podname,
                        time: item.time,
                        message: item.message,
                        detail: item
                    }
                })
            }
            this.logTableData = Array.from(this.filter_table_data)
            this.getPodnameType()
        },

        /**
        * @description: 对数据搜索功能，并且要做到每次选择或者修改时间，包含信息的时候都要修改
        * @return void
        */
        searchData() {
            // 由于时间会在选择事件，搜索信息，过滤信息任何一个被选择之后被刷新，所以需要确定时间
            if (!this.time[0] && !this.time[1]) {
                this.$message({
                    type: 'error',
                    message: '请选择搜索时间',
                    duration: this.$store.state.promptDuration
                })
                return
            }
            if (!(this.time[1] - this.time[0] <= 1000 * 60 * 15)) {
                this.$message({
                    type: 'warning',
                    message: "时间范围请限制在15分钟以内",
                    duration: this.$store.state.promptDuration
                })
                return
            }
            this.tableVisible = true
            this.pagedData = []
            this.loading = true
            if (this.time[0] && this.time[1]) {
                const start_timestamp = Math.floor(this.time[0].getTime() / 1000)
                const end_timestamp = Math.floor(this.time[1].getTime() / 1000)
                getLog(
                    {
                        'node': 'minikube',
                        'start_time': start_timestamp,
                        'end_time': end_timestamp
                    })
                    .then(res => {
                        console.log(res)
                        this.table_data = res
                        this.filterData()
                        this.loading = false
                    })

            }
        },

        /**
        * @description: 分页功能辅助函数，记录当前是第几页
        * @param page: 当前是第几页的页数
        * @return void
        */
        handleCurrentChange(page) {
            this.currentPage = page
        },

        // 绘制图表函数
        async drawChart(chart_data) {
            this.myChart = echarts.init(document.getElementById('podchart'))

            const x_data = chart_data.map((item) => item.date)
            const y_data = chart_data.map((item) => item.log_count)

            const option = {
                title: {
                    text: 'log数据量展示'
                },
                tooltip: {
                    trigger: 'axis',
                    axisPointer: {
                        type: 'shadow'
                    }
                },
                grid: {
                    containLabel: true
                },

                xAxis: {
                    type: 'category',
                    data: x_data,
                    axisTick: {
                        alignWithLabel: true
                    }
                },
                yAxis: {
                    type: 'value'
                },
                series: [
                    {
                        name: 'Count',
                        data: y_data,
                        type: 'bar',
                        itemStyle: {
                            color: '#1E90FF'
                        }
                    }
                ]
            }

            this.myChart.setOption(option)
        },

        // 下载数据
        downloadLog() {
            if (!(this.time[1] - this.time[0] <= 1000 * 60 * 60 * 24)) {
                this.$message({
                    type: 'warning',
                    message: "时间范围请限制在24h以内",
                    duration: this.$store.state.promptDuration
                })
                return
            }
            if (this.hasDownload) this.$refs.downloadProgress.resetting()
            const start_time = Math.round(this.time[0] / 1000)
            const end_time = Math.round(this.time[1] / 1000)
            this.downloadLoading = true
            this.hasDownload = true
            const download = websocket.getLogDownloadFunction({ start_time: start_time, end_time: end_time }, () => {
                this.$refs.downloadProgress.setPMS(100, '导出完成，请等待下载弹窗', 'success')
                this.downloadLoading = false
                download()
            }, (err) => {
                this.$refs.downloadProgress.setPMS(100, '导出失败', 'exception')
                this.$message({
                    type: 'error',
                    message: err.error,
                    duration: this.$store.state.promptDuration
                });
                this.downloadLoading = false
            }, (waiting) => {
                console.log('step:', waiting.step, ' progress:', waiting.progress)
                this.$refs.downloadProgress.setPMS(waiting.progress, waiting.step, '')
            })
        }
    }

}
</script>

<style scoped>
* {
    font-size: 12px;
}

.timePicker {
    width: 400px;
}

.search {
    border-bottom: 1px solid #dcdfe6;
    display: flex;
    padding: 0px 20px 5px 20px;
}

.form {
    /* display: flex; */
    width: 1200px;
    flex-wrap: wrap;
    margin-left: 30px;
}

.form-item {
    display: flex;
    flex-direction: row;
    align-items: center;
    color: #a7aebb;
    margin-bottom: 5px;
    margin-right: 10px;
    flex-shrink: 0;
    margin-top: 20px;
}

.form-item div {
    white-space: nowrap;
}

.search-key-value {
    display: flex;
    margin-top: 20px;
    margin-right: 10px;
}

.search-key {
    margin-right: 10px;
    flex-shrink: 0;
}

.search-value {
    margin-left: 10px;
    flex-shrink: 0;
    display: inline-flex;
    align-items: center;
    /* 将图标与文字垂直居中对齐 */
}

.botton-item {
    margin-top: 20px;
    margin-right: 30px;
    float: right;
}

.download {
    float: right;
}

.download-button {
    float: right;
    /* display: inline-flex; */
    align-items: center;
    /* 将图标与文字垂直居中对齐 */
    flex-shrink: 0;
    margin-top: 3px;
}

.excel-class {
    margin-right: 10px;
}



.gray-rounded-rectangle {
    margin: 40px;
    padding: 10px;
}

.messageDiv {
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
    -o-text-overflow: ellipsis;
}

.info-class {
    width: 3em;
    height: 3em;
}

.remove-value {
    margin-left: 10px;
}
</style>

<style>
.el-tooltip__popper {
    max-width: 40%;
}
</style>
