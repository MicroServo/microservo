<template>
  <structure3>
    <template #card-r-1>
      <div class="content">
        <el-row
          type="flex"
          justify="space-between"
          align="center">
          <el-col
            :span="10"
            style="text-align: center">
            <el-avatar style="width: 256px; height: 256px" src="https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png"/>
            <!-- <el-divider />
            <el-form style="width: 100%">
              <el-form-item :label="$t('userCenter.signature')">
                <el-input
                  v-model="user.description"
                  :placeholder="$t('placeholder.input')"
                  :disabled="!isEditState"
                  type="textarea" />
              </el-form-item>
            </el-form> -->
          </el-col>
          <el-col :span="10">
            <el-form style="width: 100%">
              <el-form-item :label="$t('userCenter.userName')">
                <el-input
                  v-model="user.name"
                  :disabled="!isEditState"
                  clearable
                  required />
              </el-form-item>
              <!-- <el-form-item :label="$t('userCenter.phone')">
                <el-input
                  v-model="user.phone"
                  :disabled="!isEditState"
                  clearable
                  required />
              </el-form-item> -->
              <el-form-item :label="$t('userCenter.email')">
                <el-input
                  v-model="user.email"
                  :disabled="!isEditState"
                  clearable
                  required />
              </el-form-item>
              <!-- <el-form-item :label="$t('userCenter.department')">
                <el-input
                  v-model="user.department"
                  :disabled="!isEditState"
                  clearable
                  required />
              </el-form-item> -->
            </el-form>
            <!-- <div style="margin: 16px 0; color: rgb(77, 77, 77); font-size: 14px"><b>{{ $t('userCenter.role') }}</b></div>
            <el-tag
              v-for="role in user.ownRoles"
              :key="role"
              style="margin-right: 8px"
              type="success">{{ role }}</el-tag> -->
          </el-col>
        </el-row>
        <!-- <el-divider />
        <el-row
          type="flex"
          justify="center"
          align="center">
          <el-button
            type="warning"
            icon="el-icon-edit"
            @click="isEditState = !isEditState">
            {{ isEditState ? $t('button.exitEditing') : $t('button.edit') }}</el-button>
          <el-button
            type="primary"
            @click="handleSave">{{ $t('button.save') }}</el-button>
        </el-row> -->
      </div>
    </template>
  </structure3>
</template>

<script>
import structure3 from '@/components/structure/structure3.vue'
export default {
  name: 'UserCenter',
  components: {
    structure3
  },
  data() {
    return {
      isEditState: false, // 编辑状态
      user: {
        id: 1,
        name: localStorage.getItem('username'),
        phone: '12454784545',
        email: localStorage.getItem('email'),
        password: '',
        department: '纳税',
        description: '',
        createTime: '',
        lastEditTime: '',
        ownRoles: ['admin', 'user']
      }
    }
  },
  mounted() {
    this.fetchUserInfo()
  },
  methods: {
    handleSave() {
      this.user['createTime'] = Date.parse(this.user['createTime'])
      this.user['lastEditTime'] = Date.now()
      this.user['password'] = ''
      this.$store
        .dispatch('user/updateInfo', this.user)
        .then((data) => {
          this.user = data
        })
        .catch((error) => {
          console.log(error)
          this.$message({
            type: 'error',
            message: '个人信息更新失败',
            duration: this.$store.state.promptDuration
          })
        })
        .then(() => {
          this.fetchUserInfo()
          this.isEditState = false
        })
    },
    fetchUserInfo() {
      this.$store
        .dispatch('user/getInfo')
        .then((data) => {
          this.user = data
        })
        .catch((error) => {
          console.log(error)
          this.$message({
            type: 'error',
            message: '个人信息获取失败',
            duration: this.$store.state.promptDuration
          })
        })
    }
  }

}
</script>

<style scoped>
.content{
  width: 60%;
  padding-top: 50px;
  margin: 0 auto;
}
</style>
