<template>
  <div
    :color-type="type"
    class="card"
    @click="click">
    <!--  -->
    <div
      :img-type="type"
      img/>
    <div>
      <div>{{ name }}</div>
      <div add>+{{ $t("fault.addFault") }}</div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    type: {
      default: 'http',
      type: String
    },
    name: {
      default: 'http',
      type: String
    }
  },
  data() {
    return {
    }
  },
  methods: {
    click() {
      this.$emit('click')
    }
  }
}
</script>

<style scoped>
.card {
  position: relative;
  padding: 5px;
  margin: 5px;
  width: calc(50% - 5px * 2 - 1px * 2 - 5px * 2);
  /* border */
  display: flex;
  border: 1px solid transparent;
  font-size: 16px;
  text-align: left;
  background-color: #F5F7F9;
  border-radius: 8px;
  transition: .3s;
  user-select: none;
  cursor: pointer;
}
.card [img] {
  width: 35px;
  height: 35px;
  margin-right: 5px;
  background-size: contain;
  background-repeat: no-repeat;
  transition: .3s;
}
.card:hover {
  transition: .3s;
  background-color: var(--base-color);
  box-shadow: 0px 4px 16px 0px var(--shadow-color);
  color: white;
}
.card:hover [img] {
  transition: .3s;
}
.card [add] {
  font-size: 12px;
  line-height: 12px;
}
.card [img-type='http'] {
  background-image: url('../../assets/images/故障注入/编组 11备份 13@2x.png');
}
.card:hover [img-type='http'] {
  background-image: url('../../assets/images/故障注入/编组 11备份 18@2x.png');
}
.card [img-type='net'] {
  background-image: url('../../assets/images/故障注入/编组 11备份 12@2x.png');
}
.card:hover [img-type='net'] {
  background-image: url('../../assets/images/故障注入/编组 11备份 17@2x.png');
}
.card [img-type='stress'] {
  background-image: url('../../assets/images/故障注入/编组 11备份 14@2x.png');
}
.card:hover [img-type='stress'] {
  background-image: url('../../assets/images/故障注入/编组 11备份 19@2x.png');
}
.card [img-type='pod'] {
  background-image: url('../../assets/images/故障注入/编组 11备份 16@2x.png');
}
.card:hover [img-type='pod'] {
  background-image: url('../../assets/images/故障注入/编组 11备份 21@2x.png');
}
.card [img-type='io'] {
  background-image: url('../../assets/images/故障注入/编组 11备份 15@2x.png');
}
.card:hover [img-type='io'] {
  background-image: url('../../assets/images/故障注入/编组 11备份 20@2x.png');
}
</style>
