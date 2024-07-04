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
      <card :full="true">
        <template #default>
          <slot name="card-r-1"/>
        </template>
      </card>
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
  }
}
</script>

<style scoped>

</style>
