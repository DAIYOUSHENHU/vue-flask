<template>
  <div>
    <ChessBoard></ChessBoard>
    <button @click="getRandom">按钮</button>
    <h1>{{ randnum }}</h1>
  </div>
</template>

<script>
import ChessBoard from '../components/ChessBoard'
export default {
  name: 'Mychess',
  components: {
    ChessBoard
  },
  data() {
    return {
      randnum: 0
    }
  },
  methods: {
    getRandom() {
      this.$axios.get('/mytest')
      .then(res => {
        this.randnum = res.data
      })
    }
  },

}
</script>

<style>

</style>