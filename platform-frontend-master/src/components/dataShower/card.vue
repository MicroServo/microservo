<template>
  <div class="data-shower-item">
    <header>
      <div
        :color-type="
        data.failure_type"
        O-B
      >
        <span>failure_type：</span>
        <span>{{ data.failure_type }}</span>
      </div>
      <div>
        <span>{{ new Date(data.timestamp * 1000).toLocaleTimeString() }}</span>
      </div>
    </header>
    <main O-R>
      <div>
        <span>service：</span>
        <span>{{ data.service }}</span>
      </div>
      <div>
        <span>cmdb_id：</span>
        <span>{{ data.cmdb_id_list }}</span>
      </div>
      <div>
        <span>duration：</span>
        <span>{{ data.duration }}s</span>
      </div>
    </main>
  </div>
</template>

<script>
export default {
  props: {
    data: {
      default: () => {},
      type: Object
    }
  }
}
</script>

<style>
.data-shower-item {
  width: 100%;
  background-color: #F5F7F9;
  border-radius: 12px;
  margin: 10px 0px;
  padding: 10px;
  box-sizing: border-box;
  text-align: left;
}
.data-shower-item > header {
  display: flex;
  justify-content: space-between;
}
.data-shower-item > header > div:nth-of-type(1) {
  color: var(--base-color);
}
.data-shower-item > header > div:nth-of-type(2) {
  color: #748C9A;
}
.data-shower-item > main > div > span:nth-of-type(1) {
  color: #748C9A;
  font-size: 13px;
}
.data-shower-item > main > div > span:nth-of-type(2) {
  color: #374E5C;
  font-size: 13px;
}
</style>
