<!--
 * @FileDescription
 * 结构需求2
 * 左全 / 右小顶 大底
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
  <structure :stype="2">
    <template #left>
      <card :full="true">
        <template #default>
          <slot name="card-l-1"/>
        </template>
      </card>
    </template>
    <template #right>
      <card style="height: calc(70px - 5px * 4);">
        <template #default>
          <slot name="card-r-1"/>
        </template>
      </card>
      <card style="height: calc(100% - 70px - 5px * 4);">
        <template #default>
          <slot name="card-r-2"/>
        </template>
      </card>
    </template>
    <template #shadow>
      <slot name="shadow"/>
    </template>
  </structure>
</template>

<script>
import card from './card.vue'
import structure from './index.vue'
export default {
  components: {
    structure,
    card
  },
  methods: {
    shadowEnter() {
      this.$refs.structure.setShadow(true)
    },
    shadowLeave() {
      this.$refs.structure.setShadow(false)
    }
  }
}
</script>

<style scoped>

</style>
