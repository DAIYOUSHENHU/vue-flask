<template>
  <div>
    <h1>Mychess</h1>
    <button @click="getRandom">按钮</button>
    <h1>{{ randnum }}</h1>
  </div>
</template>

<script>
export default {
  name: 'Mychess',
  data() {
    return {
      randnum: 0
    }
  },
  methods: {
    getRandom() {
      this.$axios.get('http://127.0.0.1:5000/mytest')
      .then(res => {
        this.randnum = res.data
      })
    }
  },

}
</script>

<style>

</style>