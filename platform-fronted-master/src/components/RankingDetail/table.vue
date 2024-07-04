<template>
  <div>
    <main>
      <row
        v-for="record in recordList"
        :key="record.key"
        :data="record"
        @showDetail="showDetail"/>
      <el-empty v-if="recordList.length===0" />
    </main>
  </div>
</template>

<script>
import rankingManager from '../../pages/Rankings/rangkingManager'
import row from './row.vue'
export default {
  components: {
    row
  },
  data() {
    return {
      recordList: []
    }
  },
  beforeMount() {
    rankingManager.addEventListener('update', this.rankingManagerUpdate.bind(this))
  },
  beforeDestroy() {
    rankingManager.removeEventListener('update', this.rankingManagerUpdate.bind(this))
  },
  methods: {
    rankingManagerUpdate(event) {
      switch (event.name) {
        case 'record':
          this.recordList = event.data.map((item) => {
            item.key = parseInt(Math.random() * 10000000)
            return item
          })
          break
        default:
          break
      }
    },
    selectChange() {
      rankingManager.setAlgorithmType(this.selectEM)
    },
    showDetail() {
      this.$emit('showDetail')
    }
  }
}
</script>

<style>

</style>
