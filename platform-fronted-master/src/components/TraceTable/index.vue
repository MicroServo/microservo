<template>
  <div class="trace-table">
    <el-table
      :data="renderData"
      style="width: 100%"
      height="100%"
    >
      <el-table-column
        label="Method"
        min-width="400"
      >
        <template #default="scope">
          <span truncated>
            {{ scope.row.operation_name }}
          </span>
        </template>
      </el-table-column>
      <el-table-column
        :label="$t('placeholder.startTime')"
        prop="startTime"
        width="200"
      />
      <el-table-column
        :label="$t('trace.duration')+'(ms)'"
        prop="duration"
        width="150"
      />
      <el-table-column
        prop="cmdb_id"
        label="Service"
        min-width="180"
      />
    </el-table>
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
      renderData: []
    }
  },
  watch: {
    data() {
      this.initData()
    }
  },
  mounted() {
    this.initData()
  },
  methods: {
    initData() {
      this.renderData = this.data.map((item) => {
        const t = deepClone(item)
        t.startTime = new Date(Math.floor(t.timestamp / 1000)).toLocaleString()
        t.duration /= 1000
        return t
      })
    }
  }
}
</script>

<style>
.trace-table {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: auto;
}
</style>
