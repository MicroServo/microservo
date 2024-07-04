<template>
  <div class="fi-button">
    button
  </div>
</template>

<script>
export default {
  props: {
    type: {
      default: 'list',
      type: String
    }
  }
}
</script>

<style scoped>
.fi-button {
  position: relative;
  padding: 5px;
  margin: 0px 5px;
}
</style>
