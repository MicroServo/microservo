<template>
  <div class="trace-topology">
    <div ref="chart" />
  </div>
</template>

<script>
import vis from 'vis'
export default {
  data() {
    return {
      edges: [
        { from: 1, to: 2, length: 100 },
        { from: 2, to: 3, length: 200 },
        { from: 2, to: 6, length: 200 },
        { from: 2, to: 7, length: 200 },
        { from: 2, to: 8, length: 200 },
        { from: 2, to: 9, length: 200 },
        { from: 2, to: 10, length: 200 },
        { from: 2, to: 11, length: 200 },
        { from: 3, to: 4, length: 200 },
        { from: 3, to: 5, length: 200 },
        { from: 3, to: 9, length: 200 },
        { from: 3, to: 10, length: 200 },
        { from: 3, to: 11, length: 200 },
        { from: 6, to: 9, length: 100 }
      ],
      nodes: [
        {
          id: 1,
          label: 'loadgenerator',
          image: require('@/assets/topology_images/python.png'),
          shape: 'circularImage'
        },
        {
          id: 2,
          label: 'frontend',
          image: require('@/assets/topology_images/go.png'),
          shape: 'circularImage'
        },
        {
          id: 3,
          label: 'checkoutservice',
          image: require('@/assets/topology_images/go.png'),
          shape: 'circularImage'
        },
        {
          id: 4,
          label: 'paymentservice',
          image: require('@/assets/topology_images/js.png'),
          shape: 'circularImage'
        },
        {
          id: 5,
          label: 'emailservice',
          image: require('@/assets/topology_images/python.png'),
          shape: 'circularImage'
        },
        {
          id: 6,
          label: 'adservice',
          image: require('@/assets/topology_images/java.png'),
          shape: 'circularImage',
          shapeProperties: {
            interpolation: false, // only for image and circularImage shapes
            useImageSize: false // only for image and circularImage shapes
          }
        },
        {
          id: 7,
          label: 'recommendationservice',
          image: require('@/assets/topology_images/python.png'),
          shape: 'circularImage'
        },
        {
          id: 8,
          label: 'cartservice',
          image: require('@/assets/topology_images/csharp.png'),
          shape: 'circularImage'
        },
        {
          id: 9,
          label: 'productcatalogservice',
          image: require('@/assets/topology_images/go.png'),
          shape: 'circularImage'
        },
        {
          id: 10,
          label: 'shippingservice',
          image: require('@/assets/topology_images/go.png'),
          shape: 'circularImage'
        },
        {
          id: 11,
          label: 'currencyservice',
          image: require('@/assets/topology_images/js.png'),
          shape: 'circularImage'
        }
      ],
      network: null
    }
  },
  mounted() {
    this.createVisTopology()
    window.addEventListener('resize', this.resize)
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.resize)
  },
  methods: {
    createVisTopology() {
      // 对this.edges和this.nodes进行深拷贝并转换为普通的JavaScript数组
      const data = {
        nodes: this.nodes,
        edges: this.edges
      }
      const options = {
        // 节点样式
        nodes: {
          size: 30,
          borderWidth: 2,
          color: {}
        },
        // 连接线的样式
        edges: {
          color: {
            color: 'rgb(97, 168, 224)',
            highlight: 'rgb(97, 168, 224)',
            hover: 'green',
            inherit: 'from',
            opacity: 1.0
          },
          font: {
            align: 'top' // 连接线的样式
          },
          smooth: true, // 是否显示方向箭头
          arrows: { to: true } // 箭头指向from节点
        },
        layout: { randomSeed: 2 },
        interaction: {
          navigationButtons: true,
          hover: true, // 鼠标移过后加粗该节点和连接线
          selectConnectedEdges: false // 选择节点后是否显示连接线
        },
        manipulation: {
          enabled: false
        }
      }

      this.network = new vis.Network(
        this.$refs.chart,
        data,
        options
      )
      this.resize() // 初始化时调整大小
    },
    resize() {
      if (this.network) {
        // const container = this.$refs.chart
        // this.network.setSize(
        //   container.clientWidth + 'px',
        //   container.clientHeight + 'px'
        // )
      }
    }
  }
}
</script>

<style>
.trace-topology {
  position: relative;
  width: 100%;
  height: 100%;
}
.trace-topology > div {
  width: 100%;
  height: 100%;
}
</style>
