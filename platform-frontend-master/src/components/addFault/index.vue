<template>
  <div class="add-fault">
    <div class="card-title">
      <span>{{ $t("menu.faultInjection") }}</span>
    </div>
    <div class="add-fault__main">
      <div>
        <span O-B>name</span>
        <el-input
          v-model="name"
          size="mini"/>
      </div>
      <div v-if="diffType.indexOf(type) !== -1">
        <span O-B>type</span>
        <el-select
          v-model="chooseType"
          :placeholder="$t('placeholder.choose')"
          :popper-append-to-body="false"
          size="mini">
          <el-option
            v-for="item in diffTypeDict[type]"
            :key="item"
            :label="item"
            :value="item"/>
        </el-select>
        <span O-R>{{ $t('fault.type1') }}</span>
      </div>
      <div>
        <span O-B>causeapp</span>
        <el-select
          v-model="app"
          :placeholder="$t('placeholder.choose')"
          :popper-append-to-body="false"
          size="mini"
          clearable
          @change="pods = []">
          <el-option
            v-for="item in appOptions"
            :key="item.value"
            :label="item.label"
            :value="item.value"
            size="mini"/>
        </el-select>
        <span O-R>{{ $t('fault.app') }}</span>
      </div>
      <div
        v-if="app !== ''"
        pods>
        <span O-B>causepods</span>
        <el-checkbox-group
          v-model="pods"
          size="mini">
          <el-checkbox
            v-for="p in (podsDict[app] === undefined ? 3 : podsDict[app])"
            :key="p"
            :label="app + '-' + (p - 1).toString()"
            border/>
        </el-checkbox-group>
        <span O-R>{{ $t('fault.source') }}pods</span>
      </div>
      <component
        v-if="diffType.indexOf(type) !== -1 && chooseType !== ''"
        ref="diffComponent"
        :is="componentName"/>
      <!-- <div>
        <span O-B>type</span>
        <el-select
          v-model="templateFolder"
          :popper-append-to-body="false"
          size="mini"
          placeholder="请选择">
          <el-option
            v-for="item in templateFolderOptions"
            :key="item.value"
            :label="item.label"
            :value="item.value"
            size="mini"/>
        </el-select>
      </div> -->
      <div>
        <span O-B>duration</span>
        <el-input
          v-model="duration"
          size="mini"/>
        <span O-R>Supported formats of the duration are: ms / s / m / h.</span>
      </div>
      <div>
        <span O-B>schedule</span>
        <div>
          <el-radio-group
            v-model="scheduleType"
            size="mini"
            style="margin-bottom: 5px;">
            <el-radio label="once">{{ $t('fault.once') }}</el-radio>
            <el-radio label="everyDay" >{{ $t('fault.everyday') }}</el-radio>
            <el-radio label="everyWeek">{{ $t('fault.everyweek') }}</el-radio>
          </el-radio-group>
          <el-date-picker
            v-if="scheduleType === 'once'"
            v-model="scheduleTime"
            :placeholder="$t('placeholder.selectTime')"
            type="datetime"
            popper-class="date-picker-popper-class"
            size="mini"
            format="yyyy-MM-dd HH:mm"
            style="margin-bottom: 5px;"/>
          <el-time-picker
            v-if="scheduleType !== 'once'"
            v-model="scheduleTime"
            :placeholder="$t('placeholder.selectTime')"
            size="mini"
            format="HH:mm"
            style="margin-bottom: 5px;"/>
          <br>
          <span
            v-if="scheduleType === 'everyWeek'"
            style="font-size: 14px;"
            O-R>{{ $t('fault.week') }}：</span>
          <el-select
            v-if="scheduleType === 'everyWeek'"
            v-model="scheduleDay"
            :placeholder="$t('placeholder.choose')"
            :popper-append-to-body="false"
            style="width: 80px;"
            clearable
            size="mini">
            <el-option
              v-for="item in scheduleDayOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
              size="mini"/>
          </el-select>
        </div>
        <!-- <span O-R>The schedule is expressed in the form of CronJob. If you are not familiar with it, you can use https://crontab.guru/ to help define it.</span> -->
      </div>
      <!-- <div>
        <span O-B>historyLimit</span>
        <el-input
          v-model="historyLimit"
          size="mini"/>
      </div> -->
    </div>
    <div class="add-fault__footer">
      <el-button
        type="primary"
        size="mini"
        plain
        @click="finish">{{ $t('button.cancel') }}</el-button>
      <el-button
        type="primary"
        size="mini"
        plain
        @click="submit">{{ $t('button.submit') }}</el-button>
    </div>
  </div>
</template>

<script>
import networkLoss from './networkLoss.vue'
import networkDelay from './networkDelay.vue'
import httpAbort from './httpAbort.vue'
import httpDelay from './httpDelay.vue'
import stressCpu from './stressCpu.vue'
import stressMemory from './stressMemory.vue'
import { faultInjection } from '../../network/api/fault'
import { message } from '../../utils/utils'
export default {
  components: {
    networkLoss,
    networkDelay,
    httpAbort,
    httpDelay,
    stressCpu,
    stressMemory
  },
  props: {
    type: {
      default: 'http',
      type: String
    }
  },
  data() {
    return {
      selectedTemplate: '',
      name: '',
      app: '',
      appOptions: [{
        value: 'cartservice',
        label: 'cartservice'
      }, {
        value: 'checkoutservice',
        label: 'checkoutservice'
      }, {
        value: 'currencyservice',
        label: 'currencyservice'
      }, {
        value: 'emailservice',
        label: 'emailservice'
      }, {
        value: 'frontend',
        label: 'frontend'
      }, {
        value: 'paymentservice',
        label: 'paymentservice'
      }, {
        value: 'productcatalogservice',
        label: 'productcatalogservice'
      }, {
        value: 'recommendationservice',
        label: 'recommendationservice'
      }, {
        value: 'redis-cart',
        label: 'redis-cart'
      }, {
        value: 'shippingservice',
        label: 'shippingservice'
      }],
      templateFolder: '',
      templateFolderOptions: [{
        value: 'experiment',
        label: 'experiment'
      }, {
        value: 'schedule',
        label: 'schedule'
      }],
      duration: '',
      scheduleType: 'once',
      scheduleTime: new Date(),
      scheduleDay: 0,
      scheduleDayOptions: [
        {
          value: 0,
          label: 'Sun.'
        },
        {
          value: 1,
          label: 'Mon.'
        },
        {
          value: 2,
          label: 'Tue.'
        },
        {
          value: 3,
          label: 'Wed.'
        },
        {
          value: 4,
          label: 'Thu.'
        },
        {
          value: 5,
          label: 'Fri.'
        },
        {
          value: 6,
          label: 'Sat.'
        }],
      historyLimit: '1000',
      podsDict: {
        'redis-cart': 2
      },
      pods: [],
      diffType: ['http', 'network', 'stress'],
      diffTypeDict: {
        http: ['delay', 'abort'],
        network: ['loss', 'delay'],
        stress: ['cpu', 'memory']
      },
      chooseType: ''
    }
  },
  computed: {
    componentName() {
      return this.type + this.chooseType.charAt(0).toUpperCase() + this.chooseType.slice(1)
    },
    schedule() {
      const time = this.scheduleTime
      if (this.scheduleType === 'once') {
        return time.getUTCMinutes().toString() + ' ' + time.getUTCHours().toString() + ' ' + time.getUTCDate().toString() + ' ' + (time.getUTCMonth() + 1).toString() + ' *'
      } else if (this.scheduleType === 'everyDay') {
        return time.getUTCMinutes().toString() + ' ' + time.getUTCHours().toString() + ' * * *'
      } else if (this.scheduleType === 'everyWeek') {
        return time.getUTCMinutes().toString() + ' ' + time.getUTCHours().toString() + ' * * ' + this.scheduleDay.toString()
      }
    },
    injectType() {
      return this.scheduleType === 'once' ? 'experiment' : 'schedule'
    }
  },
  mounted() {
    this.selectedTemplate = this.type
  },
  methods: {
    finish() {
      console.log('click')
      this.$emit('finish')
    },
    setData(data) {
      //
    },
    checkDuration(duration) {
      const r1 = /[1-9][0-9]*ms$/
      const r2 = /[1-9][0-9]*m$/
      const r3 = /[1-9][0-9]*s$/
      const r4 = /[1-9][0-9]*h$/
      if (r1.test(duration)) return true
      if (r2.test(duration)) return true
      if (r3.test(duration)) return true
      if (r4.test(duration)) return true
      return false
    },
    submit() {
      const base = {
        name: this.name,
        app: this.app,
        duration: this.duration,
        schedule: this.schedule,
        historyLimit: this.historyLimit,
        pods: this.pods,
        selected_template: this.selectedTemplate,
        inject_type: this.injectType,
        fault_type: this.type
      }
      
      if (this.diffType.indexOf(this.type) !== -1) {
        if (['cpu', 'memory'].indexOf(this.chooseType) !== -1) {
          base.selected_template = this.chooseType
        } else {
          base.selected_template += ('-' + this.chooseType)
        }
        Object.assign(base, this.$refs.diffComponent.getData())
      }
      const keys = Object.keys(base)
      for (const key of keys) {
        if (base[key] === '') {
          message(this.$t('fault.all'))
          return
        }
      }
      const cd = this.checkDuration(this.duration)
      if (!cd) {
        message(this.$t('fault.duration'))
        return
      }
      message(this.$t('fault.wait'), 'success')
      faultInjection({
        data: base
      }).then((res) => {
        console.log(res)
        if (window.calendarDataManager) window.calendarDataManager.refresh()
        if (window.calendarRefresh) window.calendarRefresh()
        if (window.faultListUpdate) window.faultListUpdate()
        message(this.$t('fault.success'), 'success')
        this.$emit('finish')
      }).catch((err) => {
        console.log(err)
        message(this.$t('fault.fail') + '：' + err.response.data.message)
        // this.$emit('finish')
      })
    }
  }
}
</script>

<style>
.add-fault {
  position: relative;
  background-color: white;
  max-height: calc(100% - 20px);
  box-sizing: border-box;
  padding: 10px;
  overflow: auto;
  /* width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999999;
  pointer-events: all; */
  transition: .3s;
}
.add-fault:hover {
  box-shadow: 0px 4px 12px 0px rgba(165,183,193,0.3);
  transition: .3s;
}
.add-fault__main {
  display: flex;
  width: 500px;
  flex-direction: column;
  text-align: left;
}
.add-fault__main > div,
.AF__diff-setting > main > div {
  margin: 10px 0;
  display: grid;
  grid-template-columns: 100px auto;
  grid-template-areas:  "n i"
                        "u s";
}
.add-fault__main > div > span:nth-of-type(1),
.AF__diff-setting > main > div > span:nth-of-type(1){
  font-size: 14px;
  word-break: break-all;
  text-align: right;
  padding-right: 5px;
}
.add-fault__main > div > span:nth-of-type(2),
.AF__diff-setting > main > div > span:nth-of-type(2){
  font-size: 12px;
  grid-area: s;
}
.add-fault__main div[pods] label {
  margin: 5px !important;
}
.add-fault__footer {
  display: flex;
  justify-content: flex-end;
}
.AF__diff-setting {
  display: flex !important;
  flex-direction: column !important;
}
.AF__diff-setting > header {
  margin-bottom: 10px;
  text-align: center;
}
</style>
