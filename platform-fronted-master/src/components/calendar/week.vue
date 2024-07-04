<template>
  <div>
    <!-- 类都在index.vue里面 因为week和day组件类共用 -->
    <table class="calendar-table">
      <thead>
        <tr>
          <td
            v-for="(d, i) in table.week"
            :key="i"
          >
            <div>
              <div d-type="time">
                <div>{{ $t(d) }}</div>
                <div>{{ table.date[i] }}</div>
              </div>
              <div d-type="data">
                <div
                  v-for="(typeData, ti) in table.typeAmount[i]"
                  :key="ti"
                  :color-type="typeData.type"
                  d-type="data-ele"
                >{{ typeData.amount }}</div>
              </div>
            </div>
          </td>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="(t, i) in table.time"
          :key="i"
        >
          <td
            v-for="(_, j) in table.week"
            :key="j"
            :data-time="j === 0 && i > 0 ? t : null"
            td-type="calendar"
          >
            <!--  -->
          </td>
        </tr>
      </tbody>
      <table class="calendar-data-table">
        <thead>
          <tr>
            <td
              v-for="(d, i) in table.week"
              :key="i"
            />
          </tr>
        </thead>
        <tbody>
          <tr>
            <td
              v-for="(_, j) in 7"
              :key="j"
              @click="clickDataTd(j)"
              @dblclick="dblclickDataTd(j)"
            >
              <!--  -->
              <Card
                v-for="d in data[j]"
                v-show="selectType === 'all' || selectType === d.data.failure_type"
                :key="d.drawId"
                :v-if="d.draw"
                :type="d.data.failure_type"
                :card-data="d"
              />
            </td>
          </tr>
        </tbody>
      </table>
      <div
        ref="timeline"
        class="calendar-time-line"
      >
        <div time-type="left" />
        <div time-type="time">
          <span ref="timelineHour" />:<span ref="timelineMinutes" />
        </div>
        <div time-type="right" />
      </div>
    </table>
  </div>
</template>

<script>
import CalendarDataManager from './data'
import Card from './card.vue'
export default {
  components: {
    Card
  },
  props: {
    selectType: {
      default: 'all',
      type: String
    },
    page: {
      default: 'main',
      type: String
    }
  },
  data() {
    return {
      table: {
        week: ['header.Sunday', 'header.Monday', 'header.Tuesday', 'header.Wednesday', 'header.Thursday', 'header.Friday', 'header.Saturday'],
        date: new Array(7).fill(''),
        time: [],
        typeAmount: [[], [], [], [], [], [], []]
      },
      calendarDataManager: null,
      data: [[], [], [], [], [], [], []],
      timer: null,
      faultAmount: 0
    }
  },
  watch: {
    selectType() {
      this.updateFaultAmount()
    }
  },
  mounted() {
    this.initTime()
    this.initTimeLine()
    /**
     * 借用window实现单例
     */
    if (!window.calendarDataManager) window.calendarDataManager = new CalendarDataManager()
    this.calendarDataManager = window.calendarDataManager
    this.calendarDataManager.setType('week')
    setTimeout(() => {
      // this.getData()
    }, 0)
  },
  beforeDestroy() {
    if (this.timer) clearInterval(this.timer)
  },
  methods: {
    /**
     * 时间初始化
     */
    initTime() {
      for (let i = 0; i < 24; i++) {
        this.table.time.push((i < 10 ? '0' + i.toString() : i.toString()) + ':00')
      }
    },
    /**
     * 获取数据
     */
    async getData() {
      const data = await this.calendarDataManager.getDataSync(true, this.page === 'faultInjection')
      console.log(data)
      const week = this.calendarDataManager.getCalendarShowDate()
      const date = []
      week.forEach((d) => {
        date.push(d.M + '.' + d.d)
      })
      this.table.date = date

      this.render(data)
    },
    render(data) {
      this.data = data
      this.table.typeAmount = [[], [], [], [], [], [], []]
      this.faultAmount = 0
      data.forEach((day, i) => {
        day.forEach((err) => {
          const type = err.data.failure_type
          if (this.selectType !== 'all' && this.selectType !== type) return
          const ele = this.table.typeAmount[i].find((ele) => ele.type === type)
          if (ele === undefined) {
            this.table.typeAmount[i].push({
              type: type,
              amount: 1
            })
          } else {
            ele.amount++
          }
          this.faultAmount++
        })
        this.table.typeAmount[i].sort((a, b) => a.amount - b.amount)
      })
      this.$emit('changeFaultAmount', this.faultAmount)
    },
    lastWeek() {
      this.calendarDataManager.lastWeek()
      this.getData()
    },
    nextWeek() {
      this.calendarDataManager.nextWeek()
      this.getData()
    },
    setWeek(weekBegin) {
      this.calendarDataManager.setWeek(weekBegin)
      this.getData()
    },
    clickDataTd(index) {
      console.log(index)
    },
    dblclickDataTd(index) {
      console.log('dbl', index)
    },
    initTimeLine() {
      const ele = this.$refs.timeline
      const hour = this.$refs.timelineHour
      const minutes = this.$refs.timelineMinutes
      const TOP = 50
      const s = new Date().getSeconds()
      const DAY = 1000 * 60 * 60 * 24
      const analyse = (timestamp) => {
        const now = new Date(timestamp)
        const nowM = now.getMinutes() < 10 ? '0' + now.getMinutes().toString() : now.getMinutes().toString()
        const nowH = now.getHours() < 10 ? '0' + now.getHours().toString() : now.getHours().toString()
        const nowTimestamp = timestamp - new Date().setHours(0, 0, 0, 0)
        ele.style.top = 'calc((100% - ' + TOP.toString() + 'px) * ' + (nowTimestamp / DAY).toString() + ' + ' + TOP.toString() + 'px)'
        hour.textContent = nowH
        minutes.textContent = nowM
      }
      analyse(new Date().getTime())
      setTimeout(() => {
        analyse(new Date().getTime())
        this.timer = setInterval(() => {
          analyse(new Date().getTime())
        }, 60 * 1000)
      }, 60 * 1000 - s * 1000)
    },
    updateFaultAmount() {
      this.faultAmount = 0
      this.table.typeAmount = [[], [], [], [], [], [], []]
      this.data.forEach((day, i) => {
        day.forEach((err) => {
          const type = err.data.failure_type
          if (this.selectType !== 'all' && this.selectType !== type) return
          this.faultAmount++
          const ele = this.table.typeAmount[i].find((ele) => ele.type === type)
          if (ele === undefined) {
            this.table.typeAmount[i].push({
              type: type,
              amount: 1
            })
          } else {
            ele.amount++
          }
        })
        this.table.typeAmount[i].sort((a, b) => a.amount - b.amount)
      })
      this.$emit('changeFaultAmount', this.faultAmount)
    },
    getFaultAmount() {
      return this.faultAmount
    }
  }
}
</script>

<style>

</style>
