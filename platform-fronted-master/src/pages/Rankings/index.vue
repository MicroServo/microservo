<template>
  <structure3>
    <template #card-r-1>
      <div class="ranking-r-1">
        <main>
          <div>
            <el-select
              v-model="selectType"
              @change="selectChange">
              <el-option
                v-for="item in selectTypeOptions"
                :key="item.id"
                :label="item.algorithmTypeName"
                :value="item.id"/>
            </el-select>
            <span class="title">{{ $t('menu.rankingList') }}</span>
          </div>
          <div>
            <!-- <RankingMain/> -->
          </div>
          <div>
            <RankingDetail :table-show="tableShow"/>
          </div>
        </main>
      </div>
    </template>
  </structure3>
</template>

<script>
import rankingManager from './rangkingManager'
import structure3 from '@/components/structure/structure3.vue'
import RankingMain from '@/components/RankingMain'
import RankingDetail from '@/components/RankingDetail'
export default {
  name: 'Rankings',
  components: {
    structure3,
    RankingMain,
    RankingDetail
  },
  data() {
    return {
      selectType: '',
      selectTypeOptions: [],
      tableShow: true
    }
  },
  beforeMount() {
    rankingManager.addEventListener('update', this.rankingManagerUpdate.bind(this))
  },
  beforeDestroy() {
    rankingManager.removeEventListener('update', this.rankingManagerUpdate.bind(this))
  },
  mounted() {
    rankingManager.render()
  },
  methods: {
    rankingManagerUpdate(event) {
      switch (event.name) {
        case 'algorithmTypeList':
          this.selectType = event.data.value
          this.selectTypeOptions = event.data.data
          console.log(this.selectType, this.selectTypeOptions)
          break
        default:
          break
      }
    },
    selectChange() {
      rankingManager.setAlgorithmType(this.selectType)
      this.tableShow = true
    }
  }
}
</script>

<style>
.ranking-r-1 {
  text-align: left;
}
.ranking-r-1 > header {
  margin-bottom: 10px;
}
.ranking-r-1 > main > div {
  margin-bottom: 10px;
}
.title{
  font-size:18px;
  margin-left: 20px;
}
</style>
