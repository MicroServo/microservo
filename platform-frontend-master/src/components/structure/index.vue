<!--
 * @FileDescription
 * 每个页面的结构基础
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
  <div class="structure">
    <div
      :class="{
        'left--2': stype === 2,
        'left--3': stype === 3
      }"
      class="left">
      <slot name="left" />
    </div>
    <div
      :class="{
        'right--2': stype === 2,
        'right--3': stype === 3
      }"
      class="right">
      <slot name="right" />
    </div>
    <transition name="opacity300">
      <div
        v-if="shadow"
        class="structure-shadow">
        <slot name="shadow" />
      </div>
    </transition>
  </div>
</template>

<script>
export default {
  props: {
    stype: {
      default: 1,
      type: Number
    }
  },
  data() {
    return {
      shadow: false
    }
  },
  methods: {
    setShadow(shadow) {
      this.shadow = shadow
    }
  }
}
</script>

<style>
.structure {
  position: relative;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: space-between;
}

.left {
  display: flex;
  flex-direction: column;
  width: calc(300px - 5px * 2);
  padding: 5px;
}

.right {
  width: calc(100% - 300px - 5px * 2);
  padding: 5px;
}

/* type 2 */
.left--2 {
  width: calc(200px - 5px * 2) !important;
}

.right--2 {
  width: calc(100% - 200px - 5px * 2) !important;
}

/* type 3 */
.left--3 {
  display: none;
  width: 0px !important;
}

.right--3 {
  width: calc(100% - 5px * 2) !important;
}

.structure-shadow {
  position: fixed;
  width: 100vw;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  left: 0;
  top: 0;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 999;
}
</style>
