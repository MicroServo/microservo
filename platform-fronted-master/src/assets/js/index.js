$(function() {
  $('#goAdvSearch').click(function() {
    $('#advSearchBox').css('display', 'none')
    $('#genSearchBox').css('display', 'flex')
  })
  $('#goGenSearch').click(function() {
    $('#advSearchBox').css('display', 'flex')
    $('#genSearchBox').css('display', 'none')
  })

  $('.newBox .tab li').click(function() {
    var num = $(this).index()
    $(this).addClass('cur')
    $(this).siblings().removeClass('cur')

    var obj = $(this).parent().parent().parent().children('.conz').children('.con')
    obj.eq(num).addClass('show')
    obj.eq(num).siblings().removeClass('show')
  })

  if ($('.newBox').length > 0) {
    var num_0 = $('.newBox .swiper-new').eq(0).find('.swiper-slide').length
    console.log('num_0:' + num_0)
    if (num_0 > 6) {
      function swiper_new_0() {
        var obj = $('.newBox .swiper-new').eq(0)
        var objn = $('.newBox .con').eq(0).find('.swiper-button-next')
        var objp = $('.newBox .con').eq(0).find('.swiper-button-prev')

        var swiper = new Swiper(obj, {
          speed: 500,
          autoplay: false,
          effect: 'slide',
          slidesPerView: 6,
          spaceBetween: 17,
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
      swiper_new_0()
    }

    var num_1 = $('.newBox .swiper-new').eq(1).find('.swiper-slide').length
    console.log('num_1:' + num_1)
    if (num_1 > 6) {
      function swiper_new_1() {
        var obj = $('.newBox .swiper-new').eq(1)
        var objn = $('.newBox .con').eq(1).find('.swiper-button-next')
        var objp = $('.newBox .con').eq(1).find('.swiper-button-prev')

        var swiper = new Swiper(obj, {
          speed: 500,
          autoplay: false,
          effect: 'slide',
          slidesPerView: 6,
          spaceBetween: 17,
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
      swiper_new_1()
    }

    var num_2 = $('.newBox .swiper-new').eq(2).find('.swiper-slide').length
    console.log('num_2:' + num_2)
    if (num_2 > 6) {
      function swiper_new_2() {
        var obj = $('.newBox .swiper-new').eq(2)
        var objn = $('.newBox .con').eq(2).find('.swiper-button-next')
        var objp = $('.newBox .con').eq(2).find('.swiper-button-prev')

        var swiper = new Swiper(obj, {
          speed: 500,
          autoplay: false,
          effect: 'slide',
          slidesPerView: 6,
          spaceBetween: 17,
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
      swiper_new_2()
    }

    var num_3 = $('.newBox .swiper-new').eq(3).find('.swiper-slide').length
    console.log('num_3:' + num_3)
    if (num_3 > 6) {
      function swiper_new_3() {
        var obj = $('.newBox .swiper-new').eq(3)
        var objn = $('.newBox .con').eq(3).find('.swiper-button-next')
        var objp = $('.newBox .con').eq(3).find('.swiper-button-prev')

        var swiper = new Swiper(obj, {
          speed: 500,
          autoplay: false,
          effect: 'slide',
          slidesPerView: 6,
          spaceBetween: 17,
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
      swiper_new_3()
    }

    var num_4 = $('.newBox .swiper-new').eq(4).find('.swiper-slide').length
    console.log('num_4:' + num_4)
    if (num_4 > 6) {
      function swiper_new_4() {
        var obj = $('.newBox .swiper-new').eq(4)
        var objn = $('.newBox .con').eq(4).find('.swiper-button-next')
        var objp = $('.newBox .con').eq(4).find('.swiper-button-prev')

        var swiper = new Swiper(obj, {
          speed: 500,
          autoplay: false,
          effect: 'slide',
          slidesPerView: 6,
          spaceBetween: 17,
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
      swiper_new_4()
    }

    var num_5 = $('.newBox .swiper-new').eq(5).find('.swiper-slide').length
    console.log('num_5:' + num_5)
    if (num_5 > 6) {
      function swiper_new_5() {
        var obj = $('.newBox .swiper-new').eq(5)
        var objn = $('.newBox .con').eq(5).find('.swiper-button-next')
        var objp = $('.newBox .con').eq(5).find('.swiper-button-prev')

        var swiper = new Swiper(obj, {
          speed: 500,
          autoplay: false,
          effect: 'slide',
          slidesPerView: 6,
          spaceBetween: 17,
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
      swiper_new_5()
    }
  }

  /* 下拉框 */
  $('.selBox .selBtn').click(function() {
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
  $('body').click(function() {
    $('.selBox').removeClass('show')
    $('.selBox .dropDown').css('display', 'none')
  })
  $('.selBox .dropDown li').click(function() {
    $(this).addClass('cur')
    $(this).siblings().removeClass('cur')
    var eltxt = $(this).parent().parent().parent().children('.selBtn').children('.input')
    eltxt.val($(this).text())
    $(this).parent().parent().css('display', 'none')
    $(this).parent().parent().parent().removeClass('show')
  })
})
