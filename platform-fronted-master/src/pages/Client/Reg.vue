<!-- 注册-->
<template>
  <div>
    <div class="Content">
      <div class="regBox">
        <div
          class="GoReg"
          @click="goReg()">
          <img
            src="../../assets/images/注册/密码@2x.png"
            class="regLogo">
          <p>{{ $t('login.back') }}<br>{{ $t('login.holder.login') }}</p>
        </div>
        <div class="regForm">
          <p class="text2">Hi！{{ $t('login.welcomereg') }}</p>
          <el-form
            ref="regForm"
            :rules="regRules"
            :model="regForm">
            <el-form-item prop="userName">
              <el-input
                ref="userName"
                v-model="regForm.userName"
                :placeholder="$t('login.holder.name')"
                prefix-icon="el-icon-user"
                name="userName"
                tabindex="1"/>
            </el-form-item>
            <el-form-item prop="email">
              <el-input
                ref="email"
                v-model="regForm.email"
                :placeholder="$t('login.holder.email')"
                prefix-icon="el-icon-message"
                name="email"
                tabindex="2"/>
            </el-form-item>
            <el-form-item
              prop="code"
              class="codeBox">
              <el-input
                ref="code"
                v-model="regForm.code"
                :placeholder="$t('login.holder.code')"
                style="max-width: 190px;margin-right:10px"
                prefix-icon="el-icon-chat-dot-round"
                name="code"
                tabindex="3"/>
              <el-button
                :disabled="regForm.waitTime > 0"
                type="primary"
                @click="sendEmailCode"
              >
                {{ regForm.waitTime > 0 ? regForm.waitTime + $t('login.holder.waiting') : $t('login.getCode') }}
              </el-button>
            </el-form-item>
            <el-form-item prop="password">
              <el-input
                ref="password"
                v-model="regForm.password"
                :placeholder="$t('login.holder.pwd')"
                prefix-icon="el-icon-lock"
                type="password"
                name="password"
                tabindex="4"/>
            </el-form-item>
            <el-form-item prop="rePassword">
              <el-input
                ref="rePassword"
                v-model="regForm.rePassword"
                :placeholder="$t('login.holder.repwd')"
                prefix-icon="el-icon-lock"
                type="password"
                name="rePassword"
                tabindex="5"
                @keyup.enter.native="handleReg"/>
            </el-form-item>
            <div class="RegBtn">
              <el-button
                type="primary"
                @click="handleReg">{{ $t('login.reg') }}</el-button>
            </div>
          </el-form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'UserManagement',
  components: {

  },
  data() {
    // 再次确认密码验证
    var validateCheckPass = (rule, value, callback) => {
      if (value === '') {
        callback(new Error(this.$t('login.holder.repwd')))
      } else if (value !== this.regForm.password) {
        callback(new Error(this.$t('login.holder.differ')))
      } else {
        callback()
      }
    }
    return {
      regForm:{
        userName: '',
        email: '',
        code: '',
        password: '',
        rePassword: '',
        checked: true,
        waitTime: 0
      },
      regRules: {
        userName: [{ required: true, trigger: 'blur' }],
        email: [
          { required: true, trigger: 'blur' },
          { pattern: /^\w+@\w+(\.\w+)+$/, message: this.$t('login.holder.emailFormat'), trigger: ['blur', 'change'] }],
        code: [{ required: true, trigger: 'blur' }],
        password: [
          { required: true, trigger: 'blur' },
          { pattern: /^(?=.*[A-Za-z])(?=.*\d).{8,15}$/, message: this.$t('login.holder.pwdFormat'), trigger: ['blur', 'change'] }
        ],
        rePassword: [{ validator: validateCheckPass, trigger: 'blur' }]
      }
    }
  },
  methods: {
    // http-发送验证码
    sendEmailCode() {
      this.$refs.regForm.validateField('email', (errMsg) => {
        if (errMsg) {
          console.log('邮箱校验未通过')
        } else {
          const url = '/api/sendEmail'
          this.$http({
            method: 'post',
            url: url,
            data:JSON.stringify({
              'email': this.regForm.email,
              'send_type': 'register'
            })
          }).then((res) => {
            const resData = res.data
            if (resData.code === 0) {
              this.$message.success(resData.message)
              this.regForm.waitTime = 60
              const clock = window.setInterval(() => {
                this.regForm.waitTime--
                if (this.regForm.waitTime <= 0) {
                  window.clearInterval(clock)
                }
              }, 1000)
            } else {
              this.$message.error(resData.message)
            }
          }).catch(error => {
            // 捕获和处理错误
            if (error.response) {
              const data = error.response.data
              if (data.code === 1) {
                this.$message.error(data.message)
              }
            }
          })
        }
      })
    },
    goReg() {
      this.$router.push('/login')
    },
    // http-reg
    handleReg() {
      this.$refs.regForm.validate(valid => {
        if (valid) {
          const url = '/api/register'
          this.$http({
            method: 'post',
            url: url,
            data:JSON.stringify({
              'username': this.regForm.userName,
              'email': this.regForm.email,
              'code':this.regForm.code,
              'password': this.regForm.password
            })
          }).then((res) => {
            const resData = res.data
            if (resData.code === 0) {
              this.$message.success(resData.message)
              setTimeout(() => {
                this.$router.push('/login')
              }, 500)
            } else {
              this.$message.error(resData.message)
            }
          }).catch(error => {
            // 捕获和处理错误
            if (error.response) {
              const data = error.response.data
              if (data.code === 1) {
                this.$message.error(data.message)
              }
            }
          })
        }
      })
    }
  }

}
</script>

<style scoped>
.Content{
  width: 100%;
  height: 100%;
  position: fixed;
  background-image: url('../../assets/images/登录/bg.png');
  background-repeat: no-repeat;
  background-size: 100% 100%;
}
.regBox{
  position: relative;
  left: 61%;
  top: 15%;
  width: 430px;
  height: 550px;
  background: rgba(255,255,255,0.5);
  box-shadow: 0px 0px 32px 0px rgba(205,213,218,0.5);
  border-radius: 24px;
  backdrop-filter: blur(20px);
}
.GoReg{
  background-image: url('../../assets/images/登录/矩形.png');
  position: relative;
  background-size: 100% 100%;
  width: 66px;
  height: 95px;
  left: 80%;
  cursor: pointer;
}
.GoReg{
  color: #00A0FF;
}
.GoReg p{
  margin: 0 0;
}
.regLogo{
  margin-top: 5px;
}
.regForm{
  padding: 0 40px;
  position: relative;
  top: -10%;
}
.text1{
  font-weight: normal;
  font-size: 20px;
  color: #374E5C;
  line-height: 26px;
  text-align: center;
  font-style: normal;
}
.text2{
  font-weight: normal;
  font-size: 1.5em;
  color: #374E5C;
  line-height: 44px;
  text-align: center;
  font-style: normal;
  margin-bottom: 40px;
}
.regForm /deep/ .el-input__inner{
  height: 45px;
  border: none;
}
.RegBtn /deep/ .el-button--primary{
  width: 100%;
}
.regForm /deep/ .el-input__icon{
  width: 25px;
  line-height: 45px;
  color: rgb(67, 88, 102);
}
.codeBox{
  display: flex;
}
</style>
