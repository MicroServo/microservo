<template>
  <div class="fault-list">
    <div header>
      <div
        left
        O-B>
        <div
          v-for="(item, i) in faultList"
          :key="i"
          :select="i === selectIndex ? 'true' : 'false'"
          item
          @click="changeShow(i)">
          <span O-B>{{ item.name }}</span>
        </div>
      </div>
      <div right>
        <!-- right -->
        <faultButton
          type="list"
          @click="changeToList">{{ $t('header.calendar') }}</faultButton>
        <faultButton
          type="table"
          select="true">{{ $t('header.table') }}</faultButton>
      </div>
    </div>
    <div body>
      <item
        v-for="(data, i) in showData"
        :key="i"
        :data="data"
        @updateData="updateData"/>
      <el-empty
        v-if="showData.length === 0"/>
    </div>
    <div footer>
      <el-pagination
        :total="total"
        :pager-count="5"
        :page-size="pageSize"
        :current-page="currentPage"
        background
        layout="prev, pager, next"
        @current-change="change"/>
    </div>
  </div>
</template>

<script>
import faultButton from '@/components/button/faultButton.vue'
import item from './item.vue'
import { getFaultList } from '../../network/api/fault'
export default {
  components: {
    item,
    faultButton
  },
  props: {
    faultList: {
      default: () => [],
      type: Array
    }
  },
  data() {
    return {
      currentPage: 1,
      pageSize: 10,
      dataList: [],
      selectIndex: 0
    }
  },
  computed: {
    filterData() {
      return this.dataList.filter((item) => this.faultList[this.selectIndex].contain.indexOf(item.spec.failure_type) !== -1)
    },
    showData() {
      return this.filterData.slice((this.currentPage - 1) * this.pageSize, this.currentPage * this.pageSize)
    },
    total() {
      return this.filterData.length
    }
  },
  mounted() {
    this.updateData()
    window.faultListUpdate = this.updateData.bind(this)
  },
  beforeDestory() {
    window.faultListUpdate = null
  },
  methods: {
    change(i) {
      console.log(i)
    },
    updateData() {
      getFaultList().then((res) => {
        this.dataList = res
      })
    },
    changeShow(i) {
      this.selectIndex = i
      console.log(this.selectIndex)
    },
    changeToList() {
      this.$emit('changeDataShower', 'list')
    }
  }
}
</script>

<style scoped>
.fault-list {
  height: 100%;
}
.fault-list [header] {
  position: relative;
  height: 40px;
  display: flex;
  justify-content: space-between;
}
.fault-list [header]::after {
  content: ' ';
  left: -5px;
  bottom: 0;
  position: absolute;
  width: calc(100% + 10px);
  height: 1px;
  background-color: rgba(0, 0, 0, 0.2);
}
.fault-list [footer] {
  display: flex;
  align-items: center;
  justify-content: end;
  height: 40px;
}
.fault-list [body] {
  height: calc(100% - 40px * 2);
  overflow: auto;
}
.fault-list [left],
.fault-list [right] {
  display: flex;
  align-items: center;
}
.fault-list [left] [item] {
  cursor: pointer;
  position: relative;
  display: flex;
  align-items: center;
  padding: 0px 10px;
  height: 100%;
  color: #A5B7C1;
  transition: .3s;
}
.fault-list [left] [item]::after {
  transition: .3s;
  content: ' ';
  left: 10px;
  bottom: 0;
  position: absolute;
  width: calc(100% - 10px * 2);
  height: 2px;
  background-color: transparent;
}
.fault-list [left] [select='true'] {
  transition: .3s;
  color: #374E5C;
}
.fault-list [left] [select='true']::after {
  transition: .3s;
  content: ' ';
  left: 10px;
  bottom: 0;
  position: absolute;
  width: calc(100% - 10px * 2);
  height: 2px;
  background-color: #00A0FF;
}
</style>
