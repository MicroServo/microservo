<!--
 * @FileDescription
 * 日历故障显示组件
 * @Author
 * Wen Long
 * @Date
 * 2024/3/30
 * @LastEditors
 * Wen Long
 * @LastEditTime
 * 2024/4/2
 -->
<template>
  <div class="calendar">
    <div class="calendar-header">
      <div v-if="page === 'main'">
        <div class="calendar-header__left">
          <weekPicker
            v-if="weekShow"
            ref="weekPicker"
            @lastWeek="lastWeek"
            @nextWeek="nextWeek"
            @setWeek="setWeek"/>
          <datePicker
            v-if="!weekShow"
            ref="datePicker"
            @lastDate="lastDate"
            @nextDate="nextDate"
            @setDate="setDate"/>
          <span>{{ $t('header.detected') }}<span style="color: #00A0FF;">{{ ' '+faultAmount+' ' }}</span>{{ $t('header.message') }}</span>
        </div>
        <div class="calendar-header__right">
          <div class="header__controller">
            <span>{{ $t("header.faultType") }}：</span>
            <el-select
              v-model="selectValue"
              :placeholder="$t('placeholder.pleaseChoose')"
              style="width: 80px;"
              size="mini">
              <el-option
                v-for="item in options"
                :key="item"
                :value="item"/>
            </el-select>
            <div class="controller__weekday">
              <span
                :class="{'controller__weekday--selected': !weekShow}"
                @click="weekShow = false">
                {{ $t('header.day') }}
              </span>
              <span
                :class="{'controller__weekday--selected': weekShow}"
                @click="weekShow = true">
                {{ $t('header.week') }}
              </span>
            </div>
          </div>
          <div class="data__controller">
            <el-button
              size="mini"
              type="primary"
              @click="toDataMonitor">
              {{ $t("menu.dataMonitor") }}
            </el-button>
            <el-button
              size="mini"
              type="primary"
              @click="downloadData">
              {{ $t("header.download") }}
          </el-button></div>
        </div>
      </div>
      <div v-if="page === 'faultInjection'">
        <div class="calendar-header__left">
          <weekPicker
            v-if="weekShow"
            ref="weekPicker"
            @lastWeek="lastWeek"
            @nextWeek="nextWeek"
            @setWeek="setWeek"/>
          <datePicker
            v-if="!weekShow"
            ref="datePicker"
            @lastDate="lastDate"
            @nextDate="nextDate"
            @setDate="setDate"/>
          <span>{{ $t('header.detected') }}<span style="color: #00A0FF;">{{ ' '+faultAmount+' ' }}</span>{{ $t('header.message') }}</span>
        </div>
        <div class="calendar-header__right">
          <div class="header__controller">
            <div class="controller__weekday">
              <span
                :class="{'controller__weekday--selected': !weekShow}"
                @click="weekShow = false">
                {{ $t('header.day') }}
              </span>
              <span
                :class="{'controller__weekday--selected': weekShow}"
                @click="weekShow = true">
                {{ $t('header.week') }}
              </span>
            </div>
          </div>
          <div class="data__controller">
            <faultButton
              type="list"
              select="true">{{ $t('header.calendar') }}</faultButton>
          <!-- <faultButton
              type="table"
              @click="changeToTable">{{ $t('header.table') }}</faultButton> -->
          </div>
        </div>
      </div>
      <div v-if="page === 'dataMonitor'">
        <div class="calendar-header__left">
          <weekPicker
            v-if="weekShow"
            ref="weekPicker"
            @lastWeek="lastWeek"
            @nextWeek="nextWeek"
            @setWeek="setWeek"/>
          <datePicker
            v-if="!weekShow"
            ref="datePicker"
            @lastDate="lastDate"
            @nextDate="nextDate"
            @setDate="setDate"/>
          <div class="header__controller">
            <div class="controller__weekday">
              <span
                :class="{'controller__weekday--selected': !weekShow}"
                @click="weekShow = false">
                {{ $t('header.day') }}
              </span>
              <span
                :class="{'controller__weekday--selected': weekShow}"
                @click="weekShow = true">
                {{ $t('header.week') }}
              </span>
            </div>
          </div>
        </div>
        <div class="calendar-header__right">

          <div class="data__controller">
            <!-- <el-button
              size="mini"
              type="primary"
              @click="downloadData">
              导出
            </el-button> -->
            <blueButton
              :size="'inline'"
              @click.native="downloadData">
              <i class="el-icon-upload"/>
              {{ $t("header.download") }}
            </blueButton>
          </div>
        </div>
      </div>
    </div>
    <div class="calendar-body">
      <week
        v-if="weekShow"
        ref="week"
        :page="page"
        :select-type="selectValue"
        @changeFaultAmount="changeFaultAmount" />
      <day
        v-if="!weekShow"
        ref="day"
        :page="page"
        :select-type="selectValue"
        @changeFaultAmount="changeFaultAmount"/>
    </div>
  </div>
</template>

<script>
/**
 * 本组件需要适配多个页面多种不同情况
 * 所以函数并不是每个页面都会用到，修改的时候需要注意查看
 * 同时基于不同的页面，页面结构也不会相同，修改的时候需要注意查看
 * 页面style不能用scoped!!!本页面style有涉及到其子组件共用的情况，不能设置scoped，否则子组件用不了
 * (当然你也可以选择在子组件（week和day）重写两遍相似的css
 */
import { saveAs } from 'file-saver'
import router from '@/router'
import week from './week.vue'
import day from './day.vue'
import weekPicker from './weekPicker.vue'
import datePicker from './datePicker.vue'
import faultButton from '@/components/button/faultButton.vue'
import { faultExtract } from '../../network/api/fault'
import blueButton from '@/components/button/blueButton.vue'
export default {
  components: {
    week,
    day,
    weekPicker,
    datePicker,
    faultButton,
    blueButton
  },
  props: {
    /**
     * page代表组件用于哪个页面
     * 可选值：
     * - main（主页）
     * - faultInjection（故障注入页面）
     * - dataMonitor（故障监控页面）
     */
    page: {
      default: 'main',
      type: String
    }
  },
  data() {
    return {
      weekMonday: new Date().setDate(new Date().getDate() - new Date().getDay() + 1),
      weekShow: true,
      options: ['all', 'cpu', 'pod-failure', 'network-delay', 'memory', 'loss', 'abort', 'delay'],
      selectValue: 'all',
      faultAmount: 0,
      download:'导出',
      day:'日',
      week:'周'
    }
  },
  watch: {
    weekShow() {
      this.$nextTick(() => {
        if (this.weekShow) {
          this.$refs.weekPicker.setWeek()
        } else {
          this.$refs.datePicker.setDate()
        }
      })
    }
  },
  mounted() {
    if (this.weekShow) {
      this.$refs.weekPicker.setWeek()
    } else {
      this.$refs.datePicker.setDate()
    }
    window.calendarRefresh = this.refresh.bind(this)
  },
  beforeDestory() {
    window.calendarRefresh = null
  },
  methods: {
    refresh() {
      if (this.weekShow) {
        if (this.$refs.weekPicker) this.$refs.weekPicker.setWeek()
      } else {
        if (this.$refs.datePicker) this.$refs.datePicker.setDate()
      }
    },
    lastWeek() {
      if (!this.$refs.week) return
      this.$refs.week.lastWeek()
    },
    nextWeek() {
      if (!this.$refs.week) return
      this.$refs.week.nextWeek()
    },
    setWeek(weekMonday) {
      if (!this.$refs.week) return
      this.$refs.week.setWeek(weekMonday - 1000 * 60 * 60 * 24)
    },
    lastDate() {
      if (!this.$refs.day) return
      this.$refs.day.lastDay()
    },
    nextDate() {
      if (!this.$refs.day) return
      this.$refs.day.nextDay()
    },
    setDate(date) {
      if (!this.$refs.day) return
      this.$refs.day.setDay(date)
    },
    changeToTable() {
      this.$emit('changeDataShower', 'table')
    },
    toDataMonitor() {
      router.push({
        path: '/dataMonitor'
      })
    },
    changeFaultAmount(val) {
      console.log('val', val)
      this.faultAmount = val
    },
    downloadData() {
      const time = [0, 0]
      if (this.weekShow) {
        const t = this.$refs.weekPicker.getTime()
        time[0] = t[0]
        time[1] = t[1]
      } else {
        const t = this.$refs.datePicker.getTime()
        time[0] = t[0]
        time[1] = t[1]
      }
      faultExtract({
        start_time: Math.floor(time[0] / 1000),
        end_time: Math.floor(time[1] / 1000)
      }).then((res) => {
        console.log(res)
        saveAs(new Blob([res]), 'data.zip')
      })
    }
  }
}
</script>

<style>
.calendar {
  width: 100%;
  height: 100%;
  overflow: auto;
}
.calendar-header > div {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 13px;
}
.calendar-header__left,
.calendar-header__right {
  display: flex;
  justify-content: start;
  align-items: center;
}
.header__controller{
    margin-left: 10px;
}
.header__controller,
.data__controller {
  display: flex;
  justify-content: start;
  align-items: center;
  margin-right: 20px;
  user-select: none !important;
}
/* .header__controller::after {
  content: ' ';
  transform: translateX(10px);
  height: 24px;
  border-right: 1px solid #B5BEC4;
} */
.controller__weekday {
  margin-left: 10px;
  background-color: #F5F7F9;
  border-radius: 8px;
}
.controller__weekday > span {
  display: inline-block;
  width: 40px;
  height: 30px;
  line-height: 30px;
  border-radius: 8px;
  cursor: pointer;
}
.controller__weekday--selected {
  color: #00A0FF;
  background-color: #E5F5FF;
}

/* week and day */
.calendar-table,
.calendar-data-table {
  table-layout: fixed;
}
.calendar-table td,
.calendar-data-table td {
  padding: 0;
}
.calendar-table {
  position: relative;
  margin-left: 50px;
  width: calc(100% - 50px);
  border-collapse: collapse;
  text-align: left;
  font-family: 'OPPOSans';
  overflow-y: hidden;
  border: 1px solid rgb(208, 208, 208);
  /* 没有该字体 */
}
.calendar-table > thead {
  position: sticky;
  z-index: 990;
  top: -1px;
  background-color: #F5F7F9;
  border-collapse: initial;
}
.calendar-table > thead td {
  height: 50px;
  border: 1px solid rgb(208, 208, 208);
}
.calendar-table > thead td > div {
  display: flex;
  align-items: center;
  height: 100%;
  width: 100%;
}
.calendar-table > thead td > div > div {
  display: flex;
  height: 100%;
}
.calendar-table tr {
  width: 100%;
}
.calendar-table > tbody tr > td:first-child::before {
  position: absolute;
  transform: translateX(-120%) translateY(-50%);
  top: 0;
  content: attr(data-time);
}
.calendar-table > thead tr > td:first-child::before {
  position: absolute;
  width: 50px;
  /* 与上面margin相同 */
  height: 100%;
  transform: translateX(calc(-110%));
  /* top: 0; */
  content: ' ';
  background-color: rgb(255, 255, 255);
}
.calendar-table td[td-type='calendar'] {
  position: relative;
  height: 80px;
  border: 1px solid rgb(208, 208, 208);
}
/* .calendar-table thead > td > div >  */
div[d-type=time] {
  flex-direction: column;
  justify-content: center;
  width: calc(50px - 5px);
  padding-left: 5px;
  z-index: 99;
  user-select: none;
}
div[d-type=time] > div:first-child {
  font-weight: bold;
}
div[d-type=data] {
  height: calc(100% - 10px) !important;
  max-width: calc(100% - 50px);
  width: calc(100% - 50px);
  align-items: center;
  justify-content: start;
  overflow-x: hidden;
}
div[d-type=data]:hover {
  overflow-x: auto;
}
div[d-type=data-ele] {
  display: inline-block;
  user-select: none;
  color: white;
  min-width: 24px;
  width: auto;
  height: 24px;
  background-color: var(--base-color);
  border-radius: 4px;
  margin: 3px;
  text-align: center;
  line-height: 24px;
}

.calendar-data-table {
  position: absolute;
  border-collapse: collapse;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow-y: hidden;
  /* background-color: rgba(0, 0, 0, 0.1); */
}
.calendar-data-table td {
  position: relative;
  border: 1px solid transparent;
  overflow: hidden;
}
.calendar-data-table > thead td {
  height: 50px;
}

.calendar-time-line {
  pointer-events: none;
  position: absolute;
  top: 0;
  height: 1px;
  width: 100%;
  background-color: #00A0FF;
  z-index: 800;
}
.calendar-time-line div[time-type='left'],
.calendar-time-line div[time-type='right'] {
  position: absolute;
  top: 0;
  transform: translateY(calc(-50% + 0.5px));
  border: 6px solid transparent;
}
.calendar-time-line div[time-type='left'] {
  left: 0;
  border-left: 6px solid #00A0FF;
}
.calendar-time-line div[time-type='right'] {
  right: 0;
  border-right: 6px solid #00A0FF;
}
.calendar-time-line div[time-type='time'] {
  position: absolute;
  left: 0;
  top: 0;
  padding: 1px 2px;
  background-color: #00A0FF;
  border-radius: 4px;
  color: white;
  transform: translateX(calc(-100% - 5px)) translateY(calc(-50% + 0.5px));
}
</style>
