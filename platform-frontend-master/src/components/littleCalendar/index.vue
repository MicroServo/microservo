<!--
 * @FileDescription
 * 首页小日历
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
  <div>
    <div>
      <div class="lc-month-picker">
        <img
          src="../../assets/images/主页/编组 8.png"
          draggable="false"
          @click="lastMonth"
        >
        <span>{{ showYear }} - {{ showMonth }}</span>
        <img
          src="../../assets/images/主页/编组 8备份.png"
          draggable="false"
          @click="nextMonth"
        >
      </div>
    </div>
    <table class="little-calendar-table">
      <thead>
        <tr>
          <td
            v-for="day, j in table.week"
            :key="j"
          >
            <div>
              <div>
                {{ $t(day) }}
              </div>
            </div>
          </td>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="date, i in table.date"
          :key="i">
          <td
            v-for="day, j in date"
            :key="j"
            :class="{'little-calendar-item--gray': day.gray,
                     'little-calendar-item--today': day.today}"
          >
            <div>
              <div>
                {{ day.day }}
              </div>
            </div>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  data() {
    return {
      table: {
        week: ['header.Sunday', 'header.Monday', 'header.Tuesday', 'header.Wednesday', 'header.Thursday', 'header.Friday', 'header.Saturday'],
        date: [[], [], [], [], [], []]
      },
      year: new Date().getFullYear(),
      month: new Date().getMonth() + 1,
      showYear: new Date().getFullYear(),
      showMonth: new Date().getMonth() + 1
    }
  },
  mounted() {
    this.table.date = this.generateCalendar(this.year, this.month)
  },
  methods: {
    generateCalendar(year, month) {
      this.showYear = new Date(year, month - 1, 1).getFullYear()
      this.showMonth = new Date(year, month - 1, 1).getMonth() + 1
      const nM = new Date().getMonth() + 1
      const nD = new Date().getDate()
      const firstDay = new Date(year, month - 1, 1).getDay() // 获取该月第一天是星期几
      const daysInMonth = new Date(year, month, 0).getDate() // 获取该月的天数
      const calendar = []

      // 获取上个月的天数
      const lastMonthDays = new Date(year, month - 1, 0).getDate()

      // 补齐上个月的日期
      for (let i = firstDay - 1; i >= 0; i--) {
        calendar.push({
          day: lastMonthDays - i,
          gray: true,
          today: false
        })
      }

      // 填充本月的日期
      for (let i = 1; i <= daysInMonth; i++) {
        calendar.push({
          day: i,
          gray: false,
          today: nM === month && nD === i
        })
      }

      // 获取下个月的天数
      const nextMonthFirstDay = new Date(year, month, 1).getDay()

      // 补齐下个月的日期
      for (let i = 1; i <= 7 - nextMonthFirstDay; i++) {
        calendar.push({
          day: i,
          gray: true,
          today: false
        })
      }

      // 将得到的数组按每7个元素分成一行，组成6行数组
      const result = []
      for (let i = 0; i < calendar.length; i += 7) {
        result.push(calendar.slice(i, i + 7))
      }

      return result
    },
    lastMonth() {
      this.month--
      this.table.date = this.generateCalendar(this.year, this.month)
    },
    nextMonth() {
      this.month++
      this.table.date = this.generateCalendar(this.year, this.month)
    }
  }
}
</script>

<style>
.little-calendar-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 12px;
  user-select: none;
}
.little-calendar-table td {
  padding: 0;
  height: 30px;
}
.little-calendar-table td > div {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}
.little-calendar-table td > div > div {
  width: 24px;
  height: 24px;
}
.little-calendar-table > thead,
.little-calendar-item--gray{
  color: #748C9A;
}
.little-calendar-item--today > div > div {
  border-radius: 50%;
  background-color: #00A0FF;
  color: white;
  box-shadow: 0px 2px 8px 0px rgba(0, 160, 255, 0.5);;
}
.lc-month-picker {
  display: flex;
  width: 100%;
  justify-content: space-between;
  text-align: center;
  background-color: #F5F7F9;
  border-radius: 4px;
}
.lc-month-picker > span {
  display: inline;
  font-size: 14px;
  font-weight: bold;
  line-height: 28px;
}
.lc-month-picker > img {
  cursor: pointer;
  user-select: none;
  width: 28px;
  height: 28px;
  margin: 0px 3px;
}
</style>
