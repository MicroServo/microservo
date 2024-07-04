<!-- 登录-->
<template>
  <div>
    <div class="Content">
      <div class="LoginBox">
        <div
          class="GoReg"
          @click="goReg">
          <img
            src="../../assets/images/登录/reg.png"
            class="regLogo">
          <p>{{ $t('login.immediate') }}<br>{{ $t('login.holder.reg') }}</p>
        </div>
        <div class="loginForm">
          <p class="text1">Hi！{{ $t('login.welcomelogin') }}</p>
          <p class="text2">{{ $t('menu.name') }}</p>
          <el-form
            ref="loginForm"
            :rules="loginRules"
            :model="loginForm"
            auto-complete="on">
            <el-form-item
              v-if="loginMode==='email'"
              prop="email">
              <el-input
                ref="email"
                v-model="loginForm.email"
                :placeholder="$t('login.holder.email')"
                prefix-icon="el-icon-message"
                name="email"
                tabindex="1"/>
            </el-form-item>
            <el-form-item
              v-if="loginMode==='user'"
              prop="userName">
              <el-input
                ref="userName"
                v-model="loginForm.userName"
                :placeholder="$t('login.holder.name')"
                prefix-icon="el-icon-user"
                name="userName"
                tabindex="1"/>
            </el-form-item>
            <el-form-item prop="password">
              <el-input
                ref="password"
                v-model="loginForm.password"
                :placeholder="$t('login.holder.pwd')"
                prefix-icon="el-icon-lock"
                type="password"
                name="password"
                tabindex="2"
                @keyup.enter.native="handleLogin"/>
            </el-form-item>
            <div class="tip">
              <!-- 登陆模式 -->
              <el-button
                v-if="loginMode==='user'"
                type="text"
                @click="changeMode">{{ $t('login.email') }}</el-button>
              <el-button
                v-if="loginMode==='email'"
                type="text"
                @click="changeMode">{{ $t('login.user') }}</el-button>
              <!-- 找回密码 -->
              <el-button
                type="text"
                @click="forgetPwd">{{ $t('login.forgetpwd') }}</el-button>
            </div>
            <el-button
              type="primary"
              @click="handleLogin">{{ $t('login.login') }}</el-button>
          </el-form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Login',
  data() {
    return {
      loginForm:{
        userName: '',
        email: '',
        password: '',
        checked: true
      },
      loginRules: {
        userName: [{ required: true, trigger: 'blur' }],
        email: [
          { required: true, trigger: 'blur' },
          { pattern: /^\w+@\w+(\.\w+)+$/, message: '输入正确的邮箱', trigger: ['blur', 'change'] }],
        password: [{ required: true, trigger: 'blur' }]
      },
      loginMode: 'user'
    }
  },
  methods: {
    goReg() {
      this.$router.push('/reg')
    },
    forgetPwd() {
      this.$router.push('/pwdReset')
    },
    // 切换登录模式
    changeMode() {
      if (this.loginMode === 'user') {
        this.loginMode = 'email'
      } else {
        this.loginMode = 'user'
      }
    },
    // http-login
    handleLogin() {
      this.$refs.loginForm.validate(valid => {
        if (valid) {
          if (this.loginMode === 'user') {
            const url = '/api/loginByUsername'
            this.$http({
              method: 'post',
              url: url,
              data:JSON.stringify({
                'username': this.loginForm.userName,
                'password': this.loginForm.password
              })
            }).then((res) => {
              const resData = res.data
              if (res.status === 200) {
                if (resData.code === 0) {
                  localStorage.setItem('token', resData.data.token)
                  localStorage.setItem('username', resData.data.username)
                  localStorage.setItem('email', resData.data.email)
                  this.$message.success(resData.message)
                  setTimeout(() => {
                    if (this.$route.query.redirect) {
                      this.$router.push(this.$route.query.redirect)
                    } else {
                      this.$router.push('/')
                    }
                  }, 500)
                } else {
                  this.$message.error(resData.message)
                }
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
          } else {
            const url = '/api/loginByEmail'
            this.$http({
              method: 'post',
              url: url,
              data:JSON.stringify({
                'email':this.loginForm.email,
                'password':this.loginForm.password
              })
            }).then((res) => {
              const resData = res.data
              if (resData.code === 0) {
                localStorage.setItem('token', resData.data.token)
                localStorage.setItem('username', resData.data.username)
                localStorage.setItem('email', resData.data.email)
                this.$message.success(resData.message)
                setTimeout(() => {
                  if (this.$route.query.redirect) {
                    this.$router.push(this.$route.query.redirect)
                  } else {
                    this.$router.push('/')
                  }
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
.LoginBox{
  position: relative;
  left: 61%;
  top: 15%;
  width: 430px;
  height: 470px;
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
  font-size: 1em;
  line-height: 1.2em;
}
.regLogo{
  margin-top: 5px;
}
.loginForm{
  padding: 0 40px;
  position: relative;
  top: -10%;
}
.text1{
  font-weight: normal;
  font-size: .8em;
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
.loginForm /deep/ .el-input__inner{
  height: 45px;
  border: none;
}
.loginForm /deep/ .el-button--primary{
  width: 100%;
}
.tip{
  display: flex;
  justify-content: space-between;
  margin: 10px 0;
}
.loginForm /deep/ .el-input__icon{
  width: 25px;
  line-height: 45px;
  color: rgb(67, 88, 102);
}
</style>
