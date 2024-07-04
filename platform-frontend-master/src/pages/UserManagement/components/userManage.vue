<template>
  <div>
    <div class="button-box">
      <el-input placeholder="请输入要搜索的用户名"/>
      <BlueButton><i class="el-icon-search" />搜索</BlueButton>
      <BlueButton @click.native="addDialog=true"><i class="el-icon-plus" />创建</BlueButton>
      <WhiteButton><i class="el-icon-delete" />批量删除</WhiteButton>
    </div>
    <el-divider/>
    <el-table
      ref="multipleTable"
      :data="tableData"
      fit
      size="medium"
      @selection-change="handleSelectionChange">
      <el-table-column
        type="selection"/>
      <el-table-column
        prop="name"
        label="用户名"/>
      <el-table-column
        prop="name"
        label="邮箱"/>
      <el-table-column
        prop="name"
        label="创建时间"/>
      <el-table-column
        prop="name"
        label="最近修改时间"/>
      <el-table-column
        prop="name"
        label="已授予角色"/>
      <el-table-column
        prop="name"
        label="操作">
        <el-button
          type="text"
          icon="el-icon-edit"
          size="medium"
          @click="editDialog=true">
          编辑 </el-button>
        <el-button
          type="text"
          size="medium"
          icon="el-icon-delete"
          style="color: red"
          @click="deleteDialog=true">
          删除 </el-button>
      </el-table-column>
    </el-table>
    <!-- 新增用户dialog -->
    <Dialog
      :dialogVisible="addDialog"
      title="新增用户"
      @changeDialog="changeDialog">
      <template slot="content">
        <el-form :model="formLabelAlign" label-position="left" label-width="70px">
          <el-form-item label="用户名">
            <el-input placeholder="请输入用户名"/>
          </el-form-item>
          <el-form-item label="邮箱">
            <el-input placeholder="请输入邮箱"/>
          </el-form-item>
          <el-form-item label="密码">
            <el-input placeholder="请输入密码"/>
          </el-form-item>
          <el-form-item label="授权角色">
            <el-select v-model="role" placeholder="请选择">
              <el-option
                v-for="item in roles"
                :key="item.value"
                :label="item.label"
                :value="item.value"/>
            </el-select>
          </el-form-item>
        </el-form>
      </template>
      <template slot="footer">
        <WhiteButton @click.native="changeDialog(false)">取消</WhiteButton>
        <BlueButton >确定</BlueButton>
      </template>
    </Dialog>
  </div>
</template>

<script>
import BlueButton from '@/components/button/blueButton.vue'
import WhiteButton from '@/components/button/whiteButton.vue'
export default {
  name: 'UserManage',
  components:{
    BlueButton,
    WhiteButton
  },
  data() {
    return {
      tableData: [{
        date: '2016-05-03',
        name: '王小虎',
        address: '上海市普陀区金沙江路 1518 弄'
      }, {
        date: '2016-05-02',
        name: '王小虎',
        address: '上海市普陀区金沙江路 1518 弄'
      }, {
        date: '2016-05-04',
        name: '王小虎',
        address: '上海市普陀区金沙江路 1518 弄'
      }, {
        date: '2016-05-01',
        name: '王小虎',
        address: '上海市普陀区金沙江路 1518 弄'
      }, {
        date: '2016-05-08',
        name: '王小虎',
        address: '上海市普陀区金沙江路 1518 弄'
      }, {
        date: '2016-05-06',
        name: '王小虎',
        address: '上海市普陀区金沙江路 1518 弄'
      }, {
        date: '2016-05-07',
        name: '王小虎',
        address: '上海市普陀区金沙江路 1518 弄'
      }],
      roles: [{
        value: '选项1',
        label: '黄金糕'
      }, {
        value: '选项2',
        label: '双皮奶'
      }, {
        value: '选项3',
        label: '蚵仔煎'
      }, {
        value: '选项4',
        label: '龙须面'
      }, {
        value: '选项5',
        label: '北京烤鸭'
      }],
      role: '',
      formLabelAlign: '',
      addDialog: false,
      editDialog: false,
      deleteDialog: false
    }
  },
  mounted: {

  },
  methods: {
    handleSelectionChange(val) {
      this.multipleSelection = val
    },
    changeDialog(v) {
      this.addDialog = v
      this.editDialog = v
      this.deleteDialog = v
    }
  }
}
</script>

<style scoped>
.button-box{
  display: flex;
}
.button-box /deep/ .el-input{
  width: 200px;
  margin-right: 10px;
}
</style>
