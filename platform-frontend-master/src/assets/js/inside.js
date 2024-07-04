$(function () {
  if ($('.scroll_box').length > 0) {
    var scroll_obj = $('.scroll_box')
    scroll_obj.each(function (i) {
      $(this).mCustomScrollbar({

        scrollButtons: {

          enable: true

        }

      })
    })
  }

  if ($('.bDetailBox_1').length > 0) {
    $('.bDetailBox_1 .bDetailCon .person .perPopup .perCon').mCustomScrollbar({

      scrollButtons: {

        enable: true

      }

    })

    setTimeout(function () {
      $('.bDetailBox_1 .bDetailCon .person .perPopup').css('display', 'none').css('opacity', '1')
    }, 10)
  }

  $('.bDetailBox_1 .bDetailCon .person').hover(function () {
    $(this).children('.perPopup').css('display', 'block')
    setTimeout(function () {
      $(this).children('.perPopup').children('.perCon').mCustomScrollbar({

        scrollButtons: {

          enable: true

        }

      })
    }, 200)
  }, function () {
    $(this).children('.perPopup').css('display', 'none')
  })

  /* 下拉框 */
  $('.selBox .selBtn').click(function () {
  	event.stopPropagation()
  	if ($(this).parent().hasClass('show')) {
  		$(this).parent().children('.dropDown').css('display', 'none')
  		$(this).parent().removeClass('show')
  	} else {
  		$(this).parent().siblings().children('.dropDown').css('display', 'none')
  		$(this).parent().siblings().removeClass('show')

  		$(this).parent().children('.dropDown').css('display', 'block')
  		$(this).parent().addClass('show')
  	}
  })

  $('body').click(function () {
    $('.selBox').removeClass('show')
    $('.selBox .dropDown').css('display', 'none')
  })
  $('.selBox .dropDown li').click(function () {
    $(this).addClass('cur')
    $(this).siblings().removeClass('cur')
    var eltxt = $(this).parent().parent().parent().children('.selBtn').children('.input')
    eltxt.val($(this).text())
    $(this).parent().parent().css('display', 'none')
    $(this).parent().parent().parent().removeClass('show')
  })

  /* 导读 */
  if ($('.swiper-guide').length > 0) {
    function swiper_guide () {
      var obj = $('.swiper-guide')
      var swiper = new Swiper(obj, {
        speed: 1000,
        navigation: {
          nextEl: '.swiper-guide-w .swiper-button-next',
          prevEl: '.swiper-guide-w .swiper-button-prev'
        }

      })
    }
    swiper_guide()
  }

  /* 图书列表 展开收起 */
  $(' .booksBox .list .btnS').click(function () {
    $(this).parent().parent().parent().children('.listsBox').slideToggle(100)
    $(this).toggleClass('btnSHiden')
  })

  /* 图书阅览展开全部 */
  $('.commBox .commTit .btnShow').click(function () {
    var obj = $(this).parent().parent().children('.commCon').children('.commTxt')
    if ($(this).hasClass('btnAll')) {
      obj.removeClass('commTxtAll')
      $(this).removeClass('btnAll')
      $(this).text('展开全部')
    } else {
      obj.addClass('commTxtAll')
      $(this).addClass('btnAll')
      $(this).text('收起全部')
    }
  })

  /* 知识检索 切换 */
  $('.ksSearchBox .tab li').click(function () {
    var num = $(this).index()
    $(this).addClass('cur')
    $(this).siblings().removeClass('cur')

    var obj = $(this).parent().parent().parent().children('.conz').children('.con')
    obj.eq(num).addClass('show')
    obj.eq(num).siblings().removeClass('show')
  })

  /* 知识服务 机构知识 切换 */
  $('.orgBox .tab li').click(function () {
    var num = $(this).index()
    $(this).addClass('cur')
    $(this).siblings().removeClass('cur')

    var obj = $(this).parent().parent().parent().parent().children('.conz').children('.con')
    obj.eq(num).addClass('show')
    obj.eq(num).siblings().removeClass('show')
  })

  /* 知识服务 人物知识  详情 切换 */
  $('.DTBox_2 .tab li').click(function () {
    var num = $(this).index()
    $(this).addClass('cur')
    $(this).siblings().removeClass('cur')

    var obj = $(this).parent().parent().parent().children('.conz').children('.con')
    obj.eq(num).addClass('show')
    obj.eq(num).siblings().removeClass('show')
  })

  /* 知识服务 人物知识  详情 人物筛选 选取 */
  $('.graphBox .graphBot .lipopup .lists li').click(function () {
    $(this).toggleClass('liChecked')
  })

  /* 个人中心 修改密码弹出 */
  $('.infoBox .changePassword').click(function () {
    $('.popup_center_box').css('display', 'flex')
  })

  $('.popup_center_box .btnClose').click(function () {
    $(this).parent().parent().css('display', 'none')
  })

  /* 图书阅览 收藏 弹出 */

  $('.bookDetail .box_F .btn_fav').click(function () {
    if ($(this).hasClass('btn_on')) {
      $(this).removeClass('btn_on')
    } else {
      $('.popup_fav_box').css('display', 'flex')
    }
  })

  if ($('.popup_fav_box .info').length > 0) {
    $('.popup_fav_box .info').mCustomScrollbar({

      scrollButtons: {

        enable: true

      }

    })

    setTimeout(function () {
      $('.popup_fav_box').css('display', 'none').css('opacity', '1')
    }, 100)
  }

  $('.popup_fav_box .btnClose').click(function () {
    $(this).parent().parent().css('display', 'none')
  })

  $('.popup_fav_box .btnCansel').click(function () {
    $('.popup_fav_box').css('display', 'none')
  })

  $('.popup_fav_box .btnSubmit').click(function () {
    $('.popup_fav_box').css('display', 'none')
    $('.bookDetail .box_F .btn_fav').addClass('btn_on')
  })

  /* 图书阅览 笔记本 弹出 */
  $('.bookDetail .box_F .btn_note').click(function () {
    $('.popup_note_box').css('display', 'block')
  })
  $('.popup_note_box .btnClose').click(function () {
    $(this).parent().parent().css('display', 'none')
  })
  $('.popup_note_box .btnCansel').click(function () {
    $('.popup_note_box').css('display', 'none')
  })
  $('.popup_note_box .btnSubmit').click(function () {
    $('.popup_note_box').css('display', 'none')
  })

  $('.btnGotop').click(function () {
    $(window).scrollTop(0)
  })

  if ($('.bookDetail .box_F').length == 1) {
    $(window).scroll(function () {
      if ($(window).scrollTop() > $('.bookDetail .box_F').offset().top) {
        $('.bookDetail .box_F .btnList').addClass('btnList_fixed')
      } else {
        $('.bookDetail .box_F .btnList').removeClass('btnList_fixed')
      }
    })

    var win_h = $(window).height() - 155
    var f_h = $('.bookDetail .box_F .btnList').height()
    var scale_s = win_h / f_h

    if (win_h < f_h) {
      console.log('----：win_h：' + win_h + '---f_h：' + f_h + '---scale_s：' + scale_s)
      $('.bookDetail .box_F .btnList').css('transform', 'scale(' + scale_s + ',' + scale_s + ')')
      // $(".bookDetail .box_F .btnList").css("color", "#ff0000")
    }
    $('.bookDetail .box_F .btnList').css('opacity', '1')
  }
})
