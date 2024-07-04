$(function() {

})
// 判断为空的函数
function isNullOrUndefinedOrEmpty(_value) {
  if (_value == undefined || _value == null || _value == '') {
    return true
  } else {
    return false
  }
}
function Scrool() {
  this.scrollBoxHeight = ''
  this.scrollContHeight = ''
  this.scrollTiaoHheight = ''
  this.contMaxjuli = ''
  this.scrollHuakuaiHeight = ''
  this.huakuaiMaxjuli = ''
}
$.fn.extend({
  customScrollbar: function(initTop, huakuaiColor) {
    $(this).each(function() {
      var self = $(this)
      //			console.log(self.html());
      // 拼接
      var strCont = ''
	        strCont = '<div class="scroll_tiao">' +
	        '<div class="scroll_huakuai"></div>'
	        self.find('.scroll_box').append(strCont)

	        // 初始化
      self.find('.scroll_box').find('.scroll_tiao').css({
        'height':'100%',
        'position':'absolute',
        'background-color':'#ccc',
        'width':'16px',
        'right':'0',
        'top':'0'
      })
      self.find('.scroll_box').find('.scroll_cont').css({
        'position':'absolute',
        'top':'0',
        'left':'0'
        // 'margin-right':'20px'
      })
      self.find('.scroll_box').find('.scroll_huakuai').css({
        'width':'13px',
        'height':'40px',
        'z-index': '999',
        'margin-left':'1px',
        'position': 'absolute',
        'right':'1px'
      })

      var scrool = new Scrool()
	        //	最外层容器box的高度
      scrool.scrollBoxHeight = self.height()
      //	内容层的高度
      scrool.scrollContHeight = self.find('.scroll_cont').height()
      //	滚动条容器的高度
      scrool.scrollTiaoHheight = scrool.scrollBoxHeight
      //  内容能滚动的最大高度
      scrool.contMaxjuli = scrool.scrollContHeight - scrool.scrollBoxHeight
      //	滑块的高度
      scrool.scrollHuakuaiHeight = self.find('.scroll_huakuai').height()
      //	滑块能滚动的最大范围
      scrool.huakuaiMaxjuli = scrool.scrollTiaoHheight - scrool.scrollHuakuaiHeight

      // 判断第一个参数，如果为空，给initTop一个初始值。如果不为空，判断是像素的模式还是百分比模式，无论哪个模式，initTop的值都不能大于滑块能滚动的最大高度
      if (isNullOrUndefinedOrEmpty(initTop)) {
        initTop = 0
	        } else if (initTop.indexOf('px') > 0) {
	        	var initTop1 = parseInt(initTop)
	        	if (initTop1 > scrool.huakuaiMaxjuli) {
	        		throw '您传入的第一个参数不正确，不能大于滑块能滚动的最大高度'
	        		return false
	        	}
	        } else if (initTop.indexOf('%') > 0) {
	        	var initTop2 = parseInt(initTop)
	        	var percent_top = (scrool.huakuaiMaxjuli / scrool.scrollTiaoHheight) * 100
	        	if (initTop2 > percent_top) {
	        		throw '您传入的第一个参数不正确，不能大于滑块能滚动的最大高度%'
	        	}
	        }
	        // 判断第二个参数
	        if (isNullOrUndefinedOrEmpty(huakuaiColor)) {
	        	huakuaiColor = 'red'
	        }

	        self.find('.scroll_box').find('.scroll_huakuai').css({
        'top':initTop,
        'background-color':huakuaiColor
      })

      // 初始化  initTop
      var huakuaiTop = parseInt(self.find('.scroll_box').find('.scroll_huakuai').css('top'))
      var scroll_contTop = -(scrool.contMaxjuli * (huakuaiTop / scrool.huakuaiMaxjuli))
      self.find('.scroll_box').find('.scroll_huakuai').css({
	            'top':huakuaiTop + 'px'
	        })
      self.find('.scroll_box').find('.scroll_cont').css({
	            'top':scroll_contTop + 'px'
	        })

      // 当内容的高度大于容器的高度时，滚动条才显示
      if (scrool.scrollContHeight <= scrool.scrollBoxHeight) {
        self.find('.scroll_box').find('.scroll_tiao').hide()
      } else {
        self.find('.scroll_box').find('.scroll_tiao').show()
        // 滚轮事件 $(this)=$('.scroll_box')
        function wheel() {
          self.find('.scroll_box').bind('mousewheel DOMMouseScroll', function(e) {
				    	e.preventDefault()
				        var _delta = parseInt(e.originalEvent.wheelDelta || -e.originalEvent.detail)
				       	var huakuaiTop = parseInt(self.find('.scroll_box').find('.scroll_huakuai').css('top'))
				        var scroll_contTop = 0
				        if (_delta > 0) { // 向上
				        	huakuaiTop -= 10
				        	scroll_contTop = -(scrool.contMaxjuli * (huakuaiTop / scrool.huakuaiMaxjuli))
				        	if (huakuaiTop < 0) {
				        		self.find('.scroll_box').find('.scroll_huakuai').css({
					                'top':0 + 'px'
					            })
					            self.find('.scroll_box').find('.scroll_cont').css({
					                'top':0 + 'px'
					            })
				        		return false
				        	}
				    		self.find('.scroll_box').find('.scroll_huakuai').css({
				                'top':huakuaiTop + 'px'
				            })
				            self.find('.scroll_box').find('.scroll_cont').css({
				                'top':scroll_contTop + 'px'
				            })
				            return false
				        } else {       // 向下
				        	huakuaiTop += 10
				        	scroll_contTop = -(scrool.contMaxjuli * (huakuaiTop / scrool.huakuaiMaxjuli))
				        	if (huakuaiTop > scrool.huakuaiMaxjuli) {
				        		self.find('.scroll_box').find('.scroll_huakuai').css({
					                'top':scrool.huakuaiMaxjuli + 'px'
					            })
					            self.find('.scroll_box').find('.scroll_cont').css({
					                'top':-scrool.contMaxjuli + 'px'
					            })

				        		return false
				        	}
				    		self.find('.scroll_box').find('.scroll_huakuai').css({
				                'top':huakuaiTop + 'px'
				            })
				            self.find('.scroll_box').find('.scroll_cont').css({
				                'top':scroll_contTop + 'px'
				            })
				            return false
				        }
				        return false
				    })
        }

        // 鼠标拖动滑块事件 $(this)=$('.scroll_box')
        function drag() {
			        self.find('.scroll_box').find('.scroll_huakuai').bind('mousedown', function(event) {
			        	if (event.button == 0) {    // 判断是否点击鼠标左键 ,event.button=0|1|2     分别是鼠标左中右键
			            	// 鼠标按下那一刻，先算出鼠标距离小块左边和上边的距离gapX,gapY，后面根据这个距离以及鼠标的坐标，算出小块的位置
			                obj_offsetTop = self.find('.scroll_huakuai').offset().top
			                gapY = event.clientY - self.find('.scroll_huakuai').offset().top
			                self.find('.scroll_box').bind('mousemove', move)
			                $(document).bind('mouseup', stop)
			                function move(e1) {
			                	// 整个大的容器距离网页最顶端的高度为box_margin_top
					        	var box_margin_top = parseInt(self.find('.scroll_box').offset().top)
					        	// 拖拽，滑块随着鼠标走
					        	var huakuaiTop = e1.clientY - gapY - box_margin_top

					        	// 内容部分top值计算
					        	var scroll_contTop = -(scrool.contMaxjuli * (huakuaiTop / scrool.huakuaiMaxjuli))
					        	if (huakuaiTop < 0) {
					        		huakuaiTop = 0
					        		scroll_contTop = 0
					        	} else if (huakuaiTop > scrool.huakuaiMaxjuli) {
					        		huakuaiTop = scrool.huakuaiMaxjuli
					        		scroll_contTop = -scrool.contMaxjuli
					        	}
					    		self.find('.scroll_huakuai').css({
					                'top':huakuaiTop + 'px'
					            })
					            self.find('.scroll_cont').css({
					                'top':scroll_contTop + 'px'
					            })
			                }
			                function stop() {
                self.find('.scroll_box').unbind('mousemove', move)
                self.find('.scroll_box').find('.scroll_huakuai').unbind('mouseup', stop)
              }
			        	}
			        	event.preventDefault()// 取消默认事件  (鼠标碰到文字默认选中)
			        })
			    }
			    wheel()
		   		drag()
      }
    })
  }
})

