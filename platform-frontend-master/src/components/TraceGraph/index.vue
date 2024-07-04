<template>
  <div class="trace-graph">
    <header O-R>
      <div>
        <!-- 暂时先不放东西了 -->
      </div>
      <div
        v-show="typeSet.size > 0"
        class="TG-header__type-list"
      >
        <span>{{ $t('trace.category') }}:</span>
        <span
          v-for="t in typeSet"
          :key="t.key + 'text'"
          :color-type="t"
          class="TG-header__type-item"
        >
          <span />
          <span>{{ t }}</span>
        </span>
      </div>
    </header>
    <main ref="main">
      <div class="TG-main__text">
        <!-- 文字内容 -->
        <!-- 文字内容不随着横向滚动 -->
        <div
          v-for="(item, i) in renderData"
          :key="item.key"
          :style="{'--margin-left': item.marginLeft}"
          class="TG-main__graph-text"
          @click="clickLine(i)"
        >
          <!-- 占位 -->
          <div style="height: 20px;" />
          <el-tooltip
            v-if="item.ruler !== true"
            placement="top"
            effect="light"
          >
            <template #content>
              <div>
                <span>status_code:{{ item.status_code }}</span>
                <br>
                <span>type:{{ item.type }}</span>
              </div>
            </template>
            <div
              v-if="item.ruler !== true"
              O-R
            >
              <span cmdbId>{{ item.cmdb_id }}</span>
              <span duration>{{ item.duration.toString() }}ms</span>
              <span opName>{{ item.operation_name }}</span>
            </div>
          </el-tooltip>
          <div
            v-for="j in item.level"
            :key="j"
            :style="{'--t-x': 'translateX(-' + (item.marginLeftNum - (j - 1) * marginLeft - marginLeft / 2).toString() + 'px)'}"
            :class="{'TG-main__graph-text--point--active': j === item.level}"
            class="TG-main__graph-text--point"
          />
        </div>
      </div>
      <div class="TG-main__graph">
        <!-- 线条图 -->
        <!-- 线条图随着横向滚动 -->
        <div
          v-for="item, i in renderData"
          :key="i"
          :class="{'TG-main__graph-line--ruler': item.ruler}"
          :style="{'--left': item.left, '--width': item.lineWidth}"
          :color-type="item.cmdb_id"
          class="TG-main__graph-line"
        >
          <div
            v-if="item.ruler"
            class="TG-main__graph-ruler"
          >
            <div
              v-for="ruler, j in item.lineList"
              :key="j"
              :style="{'--width': ruler.width}"
              class="TG-main__graph-ruler__item"
            >
              <span>{{ ruler.ms }}</span>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import { deepClone } from '@/utils/utils'
export default {
  props: {
    data: {
      default: () => [],
      type: Array
    }
  },
  data() {
    return {
      marginLeft: 40, // 线条左侧边距
      lineDuration: 1, // 1ms
      lineMinWidth: 150, // 1ms对应的线条最短长度
      lineWidth: 0, // 1ms对应的线条长度
      rulerLength: 1, // 刻度尺长度 1ms
      renderByData: [], // 准备用于渲染的数据
      renderData: [], // 用于渲染的数据
      typeSet: new Set(), // 类别set
      forceDraw: true // 强制绘制 数据修改后变为true
    }
  },
  watch: {
    data() {
      this.forceDraw = true
      this.dataInit()
      this.draw()
    }
  },
  mounted() {
    this.dataInit()
    this.draw()
    window.addEventListener('resize', this.draw)
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.draw)
  },
  methods: {
    draw() {
      // 绘制函数
      if (this.data.length === 0) {
        this.renderData = []
        this.typeSet.clear()
        return
      }
      const main = this.$refs.main
      const mainWidth = main.clientWidth - this.marginLeft - 8 // -8 是为了减去竖向滚动条宽度 保证底部不出现横向滚动条
      const renderByData = this.renderByData
      const fullDuration = renderByData[0].duration
      const minNeed = fullDuration / this.lineDuration * this.lineMinWidth
      let lineWidth = 0 // 和 this.lineDuration 一致
      if (minNeed <= mainWidth) {
        lineWidth = mainWidth / (fullDuration / this.lineDuration)
      } else {
        lineWidth = this.lineMinWidth
      }
      if (lineWidth === this.lineWidth) {
        if (this.forceDraw) this.forceDraw = false
        else return
      }
      this.lineWidth = lineWidth
      const begin = renderByData[0].timestamp
      renderByData.forEach((item) => {
        item.key = parseInt((Math.random() * 100000000)).toString()
        item.lineWidth = (item.duration / this.lineDuration * lineWidth).toString() + 'px'
        item.lineWidthNum = item.duration / this.lineDuration * lineWidth
        item.leftNum = this.marginLeft + (item.timestamp - begin) / this.lineDuration * lineWidth
        item.left = (this.marginLeft + (item.timestamp - begin) / this.lineDuration * lineWidth).toString() + 'px'
        item.marginLeftNum = item.level * this.marginLeft
        item.marginLeft = (item.level * this.marginLeft).toString() + 'px'
      })
      const d = this.rulerLength
      const lineDmsWidth = lineWidth / this.lineDuration * d
      const l = Math.ceil(fullDuration / d)
      const last = fullDuration / d * lineDmsWidth - (l - 1) * lineDmsWidth
      const lineList = []
      for (let i = 0; i < l; i++) {
        lineList.push({
          width: i < l - 1 ? lineDmsWidth.toString() + 'px' : last.toString() + 'px',
          ms: (i * d).toString() + 'ms'
        })
      }
      lineList.unshift({
        width: this.marginLeft.toString() + 'px',
        ms: ''
      }) // 占位
      const renderData = deepClone(renderByData)
      renderData.unshift({
        key: parseInt((Math.random() * 100000000)).toString(),
        ruler: true,
        left: this.marginLeft.toString() + 'px',
        lineWidth: (renderData[0].lineWidthNum + this.marginLeft).toString() + 'px',
        lineList: lineList
      })
      this.renderData = renderData
    },
    dataInit() {
      if (this.data.length === 0) return
      const temp = deepClone(this.data)
      temp.sort((a, b) => a.timestamp - b.timestamp)
      const res = []
      const stack = []
      this.typeSet.clear()
      temp.forEach((item) => {
        this.typeSet.add(item.cmdb_id)
        item.level = 1
        item.timestamp /= 1000
        item.duration /= 1000
        if (stack.length === 0) {
          stack.push(item)
          res.push(item)
        } else {
          while (stack.length > 0) {
            const top = stack.at(-1)
            if (item.parent_span === top.span_id) {
              item.level = stack.length + 1
              res.push(item)
              stack.push(item)
              break
            } else {
              stack.pop()
            }
          }
        }
      })
      this.renderByData = deepClone(res)
    },
    clickLine(index) {
      if (index > 0) {
        const data = this.renderData[index]
        this.$refs.main.scrollTo({
          left: data.leftNum - data.marginLeftNum,
          behavior: 'smooth'
        })
      }
    }
  }
}
</script>

<style>
.trace-graph {
  position: relative;
  width: 100%;
  height: 100%;
}
.trace-graph > header {
  width: 100%;
  position: sticky;
  top: 0;
  left: 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  height: 30px;
}
.TG-header__type-list {
  user-select: none;
  display: flex;
  align-items: center;
  max-width: 60%;
  max-height: 30px;
  overflow: auto;
  overflow-y: hidden;
  font-size: 14px;
}
.TG-header__type-list > span:nth-of-type(1) {
  min-width: 40px;
}
.TG-header__type-item {
  margin: 0px 5px;
  display: flex;
  align-items: center;
}
.TG-header__type-item > span:nth-child(1) {
  display: inline-block;
  width: 10px;
  height: 10px;
  border-radius: 999px;
  background-color: var(--base-color);
  margin-right: 6px;
}
.trace-graph > main {
  position: relative;
  width: 100%;
  height: calc(100% - 40px);
  overflow: auto;
}
.TG-main__graph {
  pointer-events: none;
  position: absolute;
  left: 0;
  top: 0;
}
.TG-main__graph-line {
  position: relative;
  left: var(--left);
  width: var(--width);
  height: 20px;
  background-color: var(--base-color);
  margin-bottom: 40px;
}
.TG-main__text {
  position: sticky;
  left: 0;
  width: 100%;
  /* overflow: hidden; */
}
.TG-main__graph-text {
  cursor: pointer;
  user-select: none;
  position: relative;
  height: 60px;
  margin-left: var(--margin-left);
}
.TG-main__graph-text--point {
  position: absolute;
  top: 50%;
  width: 1px;
  height: 100%;
  transform: var(--t-x);
  background-color: #DCDEE6;
  z-index: 1;
}
.TG-main__graph-text--point--active::before {
  content: ' ';
  width: 8px;
  height: 8px;
  border-radius: 999px;
  box-sizing: border-box;
  background-color: white;
  border: 1px solid #374E5C;
  position: absolute;
  left: 0;
  top: 0;
  transform: translateX(-50%) translateY(-50%);
}
.TG-main__graph-line--ruler {
  position: sticky;
  top: 0;
  z-index: 999;
  height: 20px;
}
.TG-main__graph-ruler {
  width: 100%;
  display: flex;
  justify-content: flex-start;
  align-content: center;
  background-color: #EDF0F2;
}
.TG-main__graph-ruler__item {
  display: flex;
  height: 20px;
  width: var(--width);
  font-size: 10px;
  position: relative;
  align-items: center;
}
.TG-main__graph-ruler__item::before {
  content: ' ';
  position: absolute;
  width: 2px;
  height: 5px;
  background-color: #DCDEE6;
  bottom: 0px;
}
.TG-main__graph-ruler__item > span {
  transform: translateX(-50%);
}
.TG-main__graph-text span {
  font-size: 12px;
  margin: 0px 5px;
}
.TG-main__graph-text span[cmdbId] {
  color: #A5B7C1;
}
.TG-main__graph-text span[duration] {
  color: #00A0FF;
}
.TG-main__graph-text span[opName] {
  color: #374E5C;
}
</style>
