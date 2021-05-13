<template>
  <div class="home">
    <img id="chesslogo" src="../assets/chess.jpg">
    <HelloWorld msg="Enjoy Your Game!!!"/>
  </div>
</template>

<script>
// @ is an alias to /src
import HelloWorld from '@/components/HelloWorld.vue'

export default {
  name: 'Home',
  components: {
    HelloWorld
  }
}
</script>

<style>
  #chesslogo {
    width: 150px;
    height: 150px;
  }
</style>
