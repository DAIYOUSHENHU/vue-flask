<template>
  <div id="body">
    <h1>棋盘</h1>
    <div>
      <audio id="music" src="../assets/long.mp3" autoplay loop></audio> 
    </div>

    <canvas
      id="canvas"
      width="480"
      height="480"
      @click="chessing($event)"
    ></canvas>

    <div style="color:white">等待落子：{{chesscolor[step%2]}}</div>
    
  </div>
</template>

<script>
import qs from "qs";
export default {
  name: "ChessBoard",
  data() {
    return {
      mcb: {}, //mychessboard 画布
      chesscolor: ["black", "white"],
      step: 0,
      chessmap: [], //二维棋盘
      username: this.$route.username
    };
  },
  methods: {
    initCanvas() {
      let canvas = document.getElementById("canvas");
      this.mcb = canvas.getContext("2d"); // 画棋盘
      for (let i = 1; i <= 15; i++) {
        this.mcb.moveTo(30 * i, 30);
        this.mcb.lineTo(30 * i, 450);
        this.mcb.moveTo(30, 30 * i);
        this.mcb.lineTo(450, 30 * i);
      }
      this.mcb.stroke();
    },

    drawchess(x, y, color) {
      //画棋子
      this.mcb.fillStyle = color;
      this.mcb.beginPath();
      this.mcb.arc(x, y, 15, 0, Math.PI * 2, false);
      this.mcb.fill();
      this.mcb.stroke();
    },

    chessing(e) {
      let lx = Math.floor((e.offsetX + 15) / 30) * 30; //location
      let ly = Math.floor((e.offsetY + 15) / 30) * 30;
      let mx = ly / 30 - 1; //maplocating
      let my = lx / 30 - 1;
      let mode = [
        [0, 1],
        [1, 0],
        [1, 1],
        [1, -1],
      ];
      if (lx == 0 || lx == 480 || ly == 0 || ly == 480) {
        return;
      }

      if (this.chessmap[ly / 30 - 1][lx / 30 - 1] != 0) {
        return;
      }

      this.drawchess(lx, ly, this.chesscolor[this.step % 2]);
      this.chessmap[mx][my] = (this.step % 2) + 1;

      this.checkwin(mx, my, (this.step % 2) + 1, mode[0]);
      this.checkwin(mx, my, (this.step % 2) + 1, mode[1]);
      this.checkwin(mx, my, (this.step % 2) + 1, mode[2]);
      this.checkwin(mx, my, (this.step % 2) + 1, mode[3]);

      this.step++;
    },

    checkwin(x, y, cn, mode) {
      let count = 1;
      for (let i = 1; i < 5; i++) {
        if (this.chessmap[x + i * mode[0]]) {
          if (this.chessmap[x + i * mode[0]][y + i * mode[1]] == cn) {
            count++;
          } else {
            break;
          }
        }
      }

      for (let i = 1; i < 5; i++) {
        if (this.chessmap[x - i * mode[0]]) {
          if (this.chessmap[x - i * mode[0]][y - i * mode[1]] == cn) {
            count++;
          } else {
            break;
          }
        }
      }
      if (count >= 5) alert(this.chesscolor[cn - 1] + " wins this round!");
    },

    doStore(username,mapx,mapy,color) {
      this.$axios
        .post(
          "/api/chessing",
          qs.stringify({
            username: username,
            mapx: mapx,
            mapy: mapy,
            color: color
          })
        )
        .then((res) => {
          console.log(res);
        });
    }
  },
  mounted() {
    this.initCanvas();
    for (let i = 0; i < 15; i++) {
      this.chessmap[i] = [];
      for (let j = 0; j < 15; j++) {
        this.chessmap[i][j] = 0;
      }
    }

    console.log(this.username);
  },
};
</script>

<style>
#body {
  background-image: url(../assets/bg.gif);
}

#music {
}

#canvas {
  display: block;
  margin: 10px auto;
  background-color: #fff;
}
</style>