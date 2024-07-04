<template>
  <el-drawer
    :visible.sync="drawerVisible"
    :show-close="false"
    :size="size"
    :append-to-body="body"
  >
    <template #header="{ close, titleId }">
      <CardTitle :id="titleId">
        {{ title }}
      </CardTitle>
      <el-icon
        style="cursor: pointer;"
        class="el-icon--left"
        @click="close"
      ><Close /></el-icon>
    </template>
    <slot />
  </el-drawer>
</template>

<script>
import CardTitle from '@/components/CardTitle'
export default {
  components: {
    CardTitle
  },
  props: {
    visible: {
      default: false,
      type: Boolean
    },
    title: {
      default: '',
      type: String
    },
    size: {
      default: '30%',
      type: String
    },
    body: {
      default: false,
      type: Boolean
    }
  },
  computed: {
    drawerVisible: {
      get() {
        return this.visible
      },
      set(val) {
        this.$emit('changeVisible', val)
        this.$emit('update:visible', val)
      }
    }
  }
}
</script>

<style>

</style>
