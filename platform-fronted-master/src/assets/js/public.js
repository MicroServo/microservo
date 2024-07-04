$(function () {
  /* 主导航下拉菜单 */
  $('.nav li').hover(function () {
    $(this).children('.sub_nav').css('display', 'block')
    $(this).addClass('hover')
  }, function () {
    $(this).children('.sub_nav').css('display', 'none')
    $(this).removeClass('hover')
  })

  /* 主导航 用户 下拉菜单 */
  $('.btnUserBox').hover(function () {
    $(this).children('.dropDown').css('display', 'block')
  }, function () {
    $(this).children('.dropDown').css('display', 'none')
  })

  /* 高级搜索重置 首页 图书检索页 */
  $('.searchBox .consList .btnReset').click(function () {
    $(this).parent().parent().parent().find('.inputp2').val('')
    $(this).parent().parent().parent().find('.input').val('')
  })

  /* 登录框展开收起 */
  $('.header .btnLogin').click(function () {
    $('.popup_login').toggle()
    $('.popup_reg').css('display', 'none')
    $('.popup_findPw').css('display', 'none')
  })

  /* 注册框展开收起 */
  $('.header .btnReg').click(function () {
    $('.popup_reg').toggle()
    $('.popup_login').css('display', 'none')
    $('.popup_findPw').css('display', 'none')
  })

  $('.header .goReg').click(function () {
    $('.popup_reg').css('display', 'block')
    $('.popup_login').css('display', 'none')
    $('.popup_findPw').css('display', 'none')
  })

  /* 记住密码 */
  $('.popup_user .dot').click(function () {
    var obj = $(this)
    if (obj.hasClass('checked')) {
      obj.removeClass('checked')
    } else {
      obj.addClass('checked')
    }
  })

  // 美化滚动条 解读详情
  // if ($('.scroll_box1').length > 0) {
  // 	$('.scroll_box1').customScrollbar('0px', '#ae916c');
  // }

//  if($(".bookDetail").length>0){
// 	if($(".bookDetail .box_L .cataBox .list ul").height()>352){
// 		//$('.scroll_box1').customScrollbar('0px', '#ae916c');
// 	}else {

// 	}
// }else {

// }
})
