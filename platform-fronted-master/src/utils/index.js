// utils: 公共函数，辅助函数文件夹
export default {
  getCookie: function() {
    if (document.cookie.length > 0) {
      var arr = document.cookie.split('; ')
      for (var i = 0; i < arr.length; i++) {
        var arr2 = arr[i].split('=')
        if (arr2[0] === 'manageName') {
          return true
        }
      }
    }
  }
}
