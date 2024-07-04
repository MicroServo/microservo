<template>
  <div class="fault-list-item">
    <div left>
      <div
        state
        O-M>
        <!-- <div iconContainer>
          <div icon/>
        </div> -->
        <div stateName>Running</div>
        <div
          name
          O-M>{{ data.name }}</div>
        <div
          faultType
          O-M>{{ data.spec.failure_type }}</div>
      </div>
    </div>
    <div right>
      <!-- <div
        time
        O-R>
        Created at 1 mouth ago
      </div> -->
      <el-button
        type="text"
        @click="drawer = true">{{ $t('table.detail') }}</el-button>
      <div buttonGroup>
        <!-- <div
          button
          run="true"
          pause="false"
          @click="pauseItem"/> -->
        <div
          button
          delete
          @click="deleteItem"/>
      </div>
    </div>
    <el-drawer
      :visible.sync="drawer"
      size="500px">
      <JsonViewer
        :value="data"
        class="platform-json-viewer"
        style="text-align: left;"
        theme="my-json-theme"
        copyable
        boxed
      />
    </el-drawer>
    <el-dialog
      :visible.sync="confirmShow"
      :title="$t('fault.confirm')"
      width="30%">
      <div style="margin-bottom: 10px;color: #F56C6C;">
        <span>{{ $t('fault.delete') }} {{ data.name }}</span>
      </div>
      <div>
        <el-button
          size="small"
          plain
          type="primary"
          @click="confirmShow = false">{{ $t('button.cancel') }}</el-button>
        <el-button
          size="small"
          type="danger"
          plain
          @click="confirmDelete">{{ $t('button.delete') }}</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import Dialog from '@/components/dialog/index.vue'
import { faultDelete } from '../../network/api/fault'
import JsonViewer from 'vue-json-viewer'
import { message } from '../../utils/utils'
export default {
  components: {
    JsonViewer,
    Dialog
  },
  props: {
    data: {
      default: () => {},
      type: Object
    }
  },
  data() {
    return {
      drawer: false,
      confirmShow: false
    }
  },
  methods: {
    pauseItem() {
      //
    },
    deleteItem() {
      this.confirmShow = true
    },
    confirmDelete() {
      this.confirmShow = false
      message('已上传，请等待', 'success')
      faultDelete({
        name: this.data.name
      }).then((res) => {
        if (window.calendarDataManager) window.calendarDataManager.refresh()
        if (window.calendarRefresh) window.calendarRefresh()
        this.$emit('updateData')
        message('删除成功', 'success')
      })
    }
  }
}
</script>

<style scoped>
.fault-list-item {
  width: calc(100% - 10px * 2);
  padding: 0 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 10px 0;
  height: 45px;
  background-color: #F5F7F9;
  border-radius: 8px;
  transition: .3s;
}
.fault-list-item:hover {
  transition: .3s;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, .1);
}
.fault-list-item [left],
.fault-list-item [right] {
  overflow: auto;
}
.fault-list-item > div,
.fault-list-item [buttonGroup],
.fault-list-item [state] {
  display: flex;
  align-items: center;
}
.fault-list-item [time] {
  font-size: 12px;
  margin-right: 10px;
  color: #374E5C;
  white-space: nowrap;
}
.fault-list-item [button] {
  margin: 0 5px;
  width: 35px;
  height: 35px;
  border-radius: 50%;
  background-size: contain;
  background-position: center;
  cursor: pointer;
  transition: .3s;
}
.fault-list-item [run='true'] {
  background-image: url('../../assets/images/故障注入/编组 14@2x(1).png');
}
.fault-list-item [run='true']:hover {
  transition: .3s;
  background-image: url('../../assets/images/故障注入/编组 14@2x.png');
}
.fault-list-item [pause='true'] {
  background-image: url('../../assets/images/故障注入/编组 14备份 2@2x.png');
}
.fault-list-item [pause='true']:hover {
  transition: .3s;
  background-image: url('../../assets/images/故障注入/编组 14@2x(2).png');
}
.fault-list-item [delete] {
  background-image: url('../../assets/images/故障注入/编组 14备份@2x(1).png');
}
.fault-list-item [delete]:hover {
  transition: .3s;
  background-image: url('../../assets/images/故障注入/编组 14备份@2x.png');
}

.fault-list-item [state] {
  color: #00A0FF;
}
.iconContainer [iconContainer] {
  overflow: hidden;
  width: 16px;
  height: 16px;
  /* 为了icon旋转不出现滚动条 */
}
.fault-list-item [icon] {
  width: 16px;
  height: 16px;
  background-image: url('../../assets/images/故障注入/编组备份@2x.png');
  background-size: contain;
  background-position: center;
  animation-name: rotate;
  animation-iteration-count: infinite;
  animation-duration: 1.5s;
  animation-timing-function: linear;
}
.fault-list-item > div:nth-child(1) > div > div {
  position: relative;
}
.fault-list-item > div:nth-child(1) > div > div:nth-child(n+2) {
  margin-left: 20px;
}
.fault-list-item > div:nth-child(1) > div > div:nth-child(n+2)::before {
  content: ' ';
  display: inline-block;
  width: 1px;
  height: 90%;
  background-color: #B5BEC4;
  position: absolute;
  left: -10px;
  top: 50%;
  transform: translateY(-50%);
}
.fault-list-item [stateName] {
  /* margin-left: 5px; */
}
.fault-list-item [name] {
  color: #374E5C;
  font-size: 14px;
}
.fault-list-item [faultType] {
  color: #748C9A;
  font-size: 14px;
}
</style>
<style>
@keyframes rotate {
  from{
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>
