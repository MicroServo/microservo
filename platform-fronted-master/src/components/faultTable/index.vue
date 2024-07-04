<template>
  <div class="fault-table">
    <card
      v-for="f, i in faultList"
      :type="f.type"
      :name="f.name"
      :key="i"
      @click="addFault(i)"
    />
  </div>
</template>

<script>
import card from './card.vue'
export default {
  components: {
    card
  },
  props: {
    faultList: {
      default: () => [],
      type: Array
    }
  },
  data() {
    return {

    }
  },
  methods: {
    addFault(index) {
      console.log(this.faultList[index])
      this.$emit('addFault', {
        type: this.faultList[index]
      })
    }
  }
}
</script>

<style scoped>
.fault-table {
  display: flex;
  flex-wrap: wrap;
  justify-content: start;
}
</style>
