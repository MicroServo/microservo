<template>
  <div class="box">
    <BlueButton @click.native="addDialog=true"><i class="el-icon-plus"/>创建</BlueButton>
    <el-divider/>
    <el-table
      :data="tableData"
      stripe
      size="medium">
      <el-table-column
        prop="rank"
        width="80"
        align="center"
        label="角色等级"/>
      <el-table-column
        prop="name"
        align="center"
        label="角色名称"/>
      <el-table-column
        prop="des"
        align="center"
        label="角色描述"/>
      <el-table-column
        prop="createTime"
        align="center"
        label="创建时间"/>
      <el-table-column
        prop="editTime"
        align="center"
        label="最后修改时间"/>
      <el-table-column
        align="center"
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
    <!-- 新增角色dialog -->
    <Dialog
      :dialogVisible="addDialog"
      title="创建角色"
      @changeDialog="changeDialog">
      <template slot="content">
        <el-form :model="formLabelAlign" label-position="left" label-width="70px">
          <el-form-item label="角色名称">
            <el-input placeholder="请输入角色名称"/>
          </el-form-item>
          <el-form-item label="角色描述">
            <el-input placeholder="请输入角色描述" type="textarea"/>
          </el-form-item>
          <el-form-item label="权限选择">
            <el-checkbox-group v-model="checkList">
              <el-checkbox label="故障注入"/>
              <el-checkbox label="数据监控"/>
              <el-checkbox label="排行榜"/>
              <el-checkbox label="算法管理"/>
              <el-checkbox label="算法模板"/>
              <el-checkbox label="评估数据"/>
              <el-checkbox label="用户管理"/>
            </el-checkbox-group>
          </el-form-item>
        </el-form>
      </template>
      <template slot="footer">
        <WhiteButton @click.native="changeDialog(false)">取消</WhiteButton>
        <BlueButton >确定</BlueButton>
      </template>
    </Dialog>
    <!-- 编辑角色dialog -->
    <Dialog
      :dialogVisible="editDialog"
      title="创建角色"
      @changeDialog="changeDialog">
      <template slot="content">
        <el-form :model="formLabelAlign" label-position="left" label-width="70px">
          <el-form-item label="角色名称">
            <el-input placeholder="请输入角色名称"/>
          </el-form-item>
          <el-form-item label="角色描述">
            <el-input placeholder="请输入角色描述" type="textarea"/>
          </el-form-item>
          <el-form-item label="权限选择">
            <el-checkbox-group v-model="checkList">
              <el-checkbox label="故障注入"/>
              <el-checkbox label="数据监控"/>
              <el-checkbox label="排行榜"/>
              <el-checkbox label="算法管理"/>
              <el-checkbox label="算法模板"/>
              <el-checkbox label="评估数据"/>
              <el-checkbox label="用户管理"/>
            </el-checkbox-group>
          </el-form-item>
        </el-form>
      </template>
      <template slot="footer">
        <WhiteButton @click.native="changeDialog(false)">取消</WhiteButton>
        <BlueButton >确定</BlueButton>
      </template>
    </Dialog>
    <!-- 删除角色dialog -->
    <Dialog
      :dialogVisible="deleteDialog"
      title="删除角色"
      @changeDialog="changeDialog">
      <template slot="content">
        <p>确认删除角色名为user的角色？</p>
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
import Dialog from '@/components/dialog/index.vue'
export default {
  name: 'SystemManage',
  components:{
    BlueButton,
    WhiteButton,
    Dialog
  },
  data() {
    return {
      tableData: [{
        rank: '1',
        name: 'admin',
        des: '管理员',
        createTime: '2016-05-04',
        editTime: '2016-05-04'
      }, {
        rank: '2',
        name: 'user',
        des: '机构用户',
        createTime: '2016-05-04',
        editTime: '2016-05-04'
      }, {
        rank: '3',
        name: 'guest',
        des: '',
        createTime: '2016-05-04',
        editTime: '2016-05-04'
      }],
      addDialog: false,
      editDialog: false,
      deleteDialog: false,
      formLabelAlign:[],
      checkList: []
    }
  },
  mounted: {

  },
  methods: {
    changeDialog(v) {
      this.addDialog = v
      this.editDialog = v
      this.deleteDialog = v
    }
  }
}
</script>

<style scoped>
.box{
  text-align: left;
}
</style>
