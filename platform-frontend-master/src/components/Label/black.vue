<template>
  <div class="label-black">{{ value }}</div>
</template>

<script>
export default {
  name: 'LabelBlack',
  props: {
    value: String
  }
}
</script>

<style scoped>
.label-black {
  background-color: #40454e;
  color: #eeeeee;
  border-radius: 4px;
  padding: 2px 5px 0px 5px;
  margin-right: 10px;
}
</style>
