$(function() {
  $('.popup_coll_box').css('height', $('body').height() + 'px')
	 // $(".popup_coll").css("height",$("body").height()-170+"px");

  /* 个人中心 收藏 弹出*/
  $('.swiper-coll .num').click(function() {
    $('.popup_coll_box').css('display', 'flex')
    setTimeout(function() {
      $('.popup_coll_box .popup_coll').addClass('show')
    }, 50)

    setTimeout(function() {
      var list_h = $('.popup_coll .noteBox').height() - $('.popup_coll .noteBox .tit').height()
      $('.popup_coll .noteBox .list').css('height', list_h - 5 + 'px')
      // var noteList=$(".popup_coll .noteBox .list").html();
      // $(".popup_coll .noteBox .list").mCustomScrollbar({
      // 		scrollButtons: {
      // 			enable: true
      // 		}
      // });
    }, 100)
  })

  $('.popup_coll .btnHide').click(function() {
    $('.popup_coll_box .popup_coll').removeClass('show')
    setTimeout(function() {
      $('.popup_coll_box').css('display', 'none')
    }, 500)
  })

  /* 笔记列表 展开收起*/
  $('.popup_coll .btnShow').click(function() {
    if ($(this).hasClass('btnCut')) {
      $(this).parent().parent().children('.txt').removeClass('txtAll')
      $(this).removeClass('btnCut')
      $(this).text('展开')
    } else {
      $(this).parent().parent().children('.txt').addClass('txtAll')
      $(this).addClass('btnCut')
      $(this).text('收起')
    }
  })
  /* 笔记列表 选中*/
  $('.popup_coll .noteBox .list li').click(function() {
    $(this).toggleClass('liSel')

    if ($('.popup_coll .noteBox li').length == $('.popup_coll .noteBox li.liSel').length) {
      $('.popup_coll .noteBox .tit .about .check').addClass('checked')
    } else {
      $('.popup_coll .noteBox .tit .about .check').removeClass('checked')
    }
  })
  $('.popup_coll .noteBox .tit .about .check').click(function() {
    if ($(this).hasClass('checked')) {
      $(this).removeClass('checked')
      $(this).parent().parent().parent().find('li').removeClass('liSel')
    } else {
      $(this).addClass('checked')
      $(this).parent().parent().parent().find('li').addClass('liSel')
    }
  })

  $('.collBox .tab li').click(function() {
    var num = $(this).index()
    $(this).addClass('cur')
    $(this).siblings().removeClass('cur')

    var obj = $(this).parent().parent().parent().children('.conz').children('.con')
    obj.eq(num).addClass('show')
    obj.eq(num).siblings().removeClass('show')
  })

  if ($('.collBox').length > 0) {
    var num_0 = $('.collBox .swiper-coll').eq(0).find('.swiper-slide').length
    console.log('num_0:' + num_0)
    if (num_0 > 6) {
      function swiper_coll_0() {
        var obj = $('.collBox .swiper-coll').eq(0)
        var objn = $('.collBox .con').eq(0).find('.swiper-button-next')
        var objp = $('.collBox .con').eq(0).find('.swiper-button-prev')

        var swiper = new Swiper(obj, {
          speed: 500,
          autoplay: false,
          effect: 'slide',
          slidesPerView: 4,
          spaceBetween: 54,
          slidesPerGroup: 1,
          loop: true,
          onlyExternal: false,
          navigation: {
            nextEl: objn,
            prevEl: objp
          },
          loopFillGroupWithBlank: true,

          keyboard: {
            enabled: true
          }

        })
      }
      swiper_coll_0()
    }

    var num_1 = $('.collBox .swiper-coll').eq(1).find('.swiper-slide').length
    console.log('num_1:' + num_1)
    if (num_1 > 6) {
      function swiper_coll_1() {
        var obj = $('.collBox .swiper-coll').eq(1)
        var objn = $('.collBox .con').eq(1).find('.swiper-button-next')
        var objp = $('.collBox .con').eq(1).find('.swiper-button-prev')

        var swiper = new Swiper(obj, {
          speed: 500,
          autoplay: false,
          effect: 'slide',
          slidesPerView: 4,
          spaceBetween: 54,
          slidesPerGroup: 1,
          loop: true,
          onlyExternal: false,
          navigation: {
            nextEl: objn,
            prevEl: objp
          },
          loopFillGroupWithBlank: true,

          keyboard: {
            enabled: true
          }

        })
      }
      swiper_coll_1()
    }

    var num_2 = $('.collBox .swiper-coll').eq(2).find('.swiper-slide').length
    console.log('num_2:' + num_2)
    if (num_2 > 6) {
      function swiper_coll_2() {
        var obj = $('.collBox .swiper-coll').eq(2)
        var objn = $('.collBox .con').eq(2).find('.swiper-button-next')
        var objp = $('.collBox .con').eq(2).find('.swiper-button-prev')

        var swiper = new Swiper(obj, {
          speed: 500,
          autoplay: false,
          effect: 'slide',
          slidesPerView: 4,
          spaceBetween: 54,
          slidesPerGroup: 1,
          loop: true,
          onlyExternal: false,
          navigation: {
            nextEl: objn,
            prevEl: objp
          },
          loopFillGroupWithBlank: true,

          keyboard: {
            enabled: true
          }

        })
      }
      swiper_coll_2()
    }

    var num_3 = $('.collBox .swiper-coll').eq(3).find('.swiper-slide').length
    console.log('num_3:' + num_3)
    if (num_3 > 6) {
      function swiper_coll_3() {
        var obj = $('.collBox .swiper-coll').eq(3)
        var objn = $('.collBox .con').eq(3).find('.swiper-button-next')
        var objp = $('.collBox .con').eq(3).find('.swiper-button-prev')

        var swiper = new Swiper(obj, {
          speed: 500,
          autoplay: false,
          effect: 'slide',
          slidesPerView: 4,
          spaceBetween: 54,
          slidesPerGroup: 1,
          loop: true,
          onlyExternal: false,
          navigation: {
            nextEl: objn,
            prevEl: objp
          },
          loopFillGroupWithBlank: true,

          keyboard: {
            enabled: true
          }

        })
      }
      swiper_coll_3()
    }

    var num_4 = $('.collBox .swiper-coll').eq(4).find('.swiper-slide').length
    console.log('num_4:' + num_4)
    if (num_4 > 6) {
      function swiper_coll_4() {
        var obj = $('.collBox .swiper-coll').eq(4)
        var objn = $('.collBox .con').eq(4).find('.swiper-button-next')
        var objp = $('.collBox .con').eq(4).find('.swiper-button-prev')

        var swiper = new Swiper(obj, {
          speed: 500,
          autoplay: false,
          effect: 'slide',
          slidesPerView: 4,
          spaceBetween: 54,
          slidesPerGroup: 1,
          loop: true,
          onlyExternal: false,
          navigation: {
            nextEl: objn,
            prevEl: objp
          },
          loopFillGroupWithBlank: true,

          keyboard: {
            enabled: true
          }

        })
      }
      swiper_coll_4()
    }

    var num_5 = $('.collBox .swiper-coll').eq(5).find('.swiper-slide').length
    console.log('num_5:' + num_5)
    if (num_5 > 6) {
      function swiper_coll_5() {
        var obj = $('.collBox .swiper-coll').eq(5)
        var objn = $('.collBox .con').eq(5).find('.swiper-button-next')
        var objp = $('.collBox .con').eq(5).find('.swiper-button-prev')

        var swiper = new Swiper(obj, {
          speed: 500,
          autoplay: false,
          effect: 'slide',
          slidesPerView: 4,
          spaceBetween: 54,
          slidesPerGroup: 1,
          loop: true,
          onlyExternal: false,
          navigation: {
            nextEl: objn,
            prevEl: objp
          },
          loopFillGroupWithBlank: true,

          keyboard: {
            enabled: true
          }

        })
      }
      swiper_coll_5()
    }
  }
})
