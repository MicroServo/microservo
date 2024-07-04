<template>
  <div
    :select="select"
    class="fault-button"
    @click="click">
    <div
      :type="type"
      icon/>
    <div
      name
      O-R>
      <slot/>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    type: {
      default: '',
      type: String
    },
    select: {
      default: 'false',
      type: String
    }
  },
  methods: {
    click(e) {
      this.$emit('click', e)
    }
  }
}
</script>

<style scoped>
.fault-button {
  display: flex;
  align-items: center;
  padding: 3px 5px;
  cursor: pointer;
  background: #EDF0F2;
  border-radius: 12px;
  border: 1px solid transparent;

  margin: 0px 5px;
}
.fault-button[select='true'] {
  background: #E5F5FF;
  border: 1px solid #00A0FF;
  color: #00A0FF;

}
.fault-button [icon] {
  width: 16px;
  height: 16px;
  background-position: center;
  background-size: contain;
  background-repeat: no-repeat;
}
.fault-button [type='list'] {
  background-image: url('../../assets/images/故障注入/编组备份 2@2x.png');
}
.fault-button[select='true'] [type='list'] {
  background-image: url('../../assets/images/故障注入/编组@2x(1).png');
}
.fault-button [type='table'] {
  background-image: url('../../assets/images/故障注入/编组@2x.png');
}
.fault-button[select='true'] [type='table'] {
  background-image: url('../../assets/images/故障注入/编组备份 3@2x.png');
}
.fault-button [name] {
  margin-left: 5px;
  font-size: 14px;
}
</style>
