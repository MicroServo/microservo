<template>
  <div
    :class="{'trace-card--active': active}"
    class="trace-card"
    @click="click"
  >
    <header O-B>
      <span>{{ data.operation_name }}</span>
    </header>
    <main>
      <span O-B>{{ data.duration / 1000 }}ms</span>
      <span>{{ new Date(data.timestamp / 1000).toLocaleString() }}</span>
    </main>
  </div>
</template>

<script>
export default {
  props: {
    data: {
      default: () => {},
      type: Object
    },
    active: {
      default: false,
      type: Boolean
    }
  },
  methods: {
    click() {
      this.$emit('click')
    }
  }
}
</script>

<style>
.trace-card {
  cursor: pointer;
  box-sizing: border-box;
  padding: 10px;
  background-color: #F5F7F9;
  border-radius: 12px;
  transition: .3s;
  position: relative;
  overflow: hidden;
  margin: 10px 0px;
}
.trace-card::before {
  content: ' ';
  width: 3px;
  height: 100%;
  position: absolute;
  left: 0;
  top: 0;
  background-color: #00A0FF;
}
.trace-card:hover,
.trace-card--active {
  transition: .3s;
  background-color: #00A0FF;
  box-shadow: 0px 4px 12px 0px rgba(0,160,255,0.5);
}
.trace-card:hover *,
.trace-card--active * {
  transition: .3s;
  color: white;
}
.trace-card > header {
  transition: .3s;
  color: #00A0FF;
  margin-bottom: 5px;
  max-width: 100%;
  display: flex;
  align-content: center;
  height: 30px;
}
.trace-card > header > span {
  overflow: hidden;
}
.trace-card > header:hover > span {
  overflow: auto;
}
.trace-card > main > span {
  transition: .3s;
  margin-right: 15px;
}
.trace-card > main > span:nth-child(1) {
  background-color: #E1E4E6;
  border-radius: 8px;
  font-size: 13px;
  padding: 4px;
}
.trace-card > main > span:nth-child(2) {
  font-size: 12px;
}
.trace-card:hover > main > span:nth-child(1),
.trace-card--active > main > span:nth-child(1) {
  transition: .3s;
  background-color: rgba(255, 255, 255, 0.2);
}
</style>
