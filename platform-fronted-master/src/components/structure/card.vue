<!--
 * @FileDescription
 * 每个页面的卡片
 * @Author
 * Wen Long
 * @Date
 * 2024/4/1
 * @LastEditors
 * Wen Long
 * @LastEditTime
 * 2024/4/2
 -->
<template>
  <div
    ref="card"
    :class="{ 'structure__card--full': full,
              'structure__card--noscrollbar': noscrollbar}"
    class="structure__card"
  >
    <slot name="default" />
  </div>
</template>

<script>
export default {
  props: {
    /**
    * 占据全部区域
    * 那个区域只能存在一个card
    */
    full: {
      default: false,
      type: Boolean
    },
    /**
    * 有bug
    * 别用这个
    * 不希望出现滚动条（希望完全显示）
    * - 直接设置高度
    */
    noscrollbar: {
      default: false,
      type: Boolean
    }
  }
}
</script>

<style>
.structure__card {
  position: relative;
  transition: .3s;
  background-color: white;
  border: 1px solid #ebeef5;
  border-radius: 4px;
  overflow: auto;
  max-height: 100%;
  margin: 5px;
  width: calc(100% - 5px * 2 - 5px * 2);
  padding: 5px;
}
.structure__card:hover {
  transition: .3s;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, .1);
}
.structure__card--full {
  height: calc(100% - 5px * 2 - 5px * 2);
}
.structure__card--noscrollbar {
  display: flex;
  /* flex-direction: column; */
  /* display: block !important; */
  height: auto;
  /* overflow: hidden; */
  /* min-height: 100%; */
}

/* .structure__card::-webkit-scrollbar {
  width: 8px;
    height: 8px;
  visibility: hidden !important;
}
.structure__card::-webkit-scrollbar-track {
  background-color: rgba(0, 0, 0, 0.1) !important;
    border-radius: 4px;
}
.structure__card::-webkit-scrollbar-thumb {
    border-radius: 4px;
    background-color: rgba(0, 0, 0, 0.15) !important;
} */
</style>
