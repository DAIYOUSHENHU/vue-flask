<template>
<div id="body">
  <h1>棋盘</h1>
  <div>
    <audio id="music" src="../assets/long.mp3" autoplay loop></audio>
  </div>

  <canvas id="canvas"></canvas>
</div>


  
</template>

<script>
export default {
  name: 'ChessBoard',
  data() {
    return {
      
    }
  },

}
</script>

<style>
#body {
  background-image: url(../assets/bg.gif);
}

#music {

}
  
#canvas {
  width: 450px;
  height: 450px;
  display: block;
  margin: 20px auto;
  background-color: #fff;
}

</style>