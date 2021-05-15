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

    <div style="color: white">等待落子：{{ chesscolor[step % 2] }}</div>

    <div>
      <button id="regret" @click="regret">悔棋</button>
      <button id="newgame" @click="newgame()">重新开始</button>
    </div>
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
      beforemap: [],
      username: this.$route.query.username,
      mode: [
        [0, 1],
        [1, 0],
        [1, 1],
        [1, -1],
      ],
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
    initchessmap() {
      for (let i = 0; i < 15; i++) {
        this.chessmap[i] = [];
        for (let j = 0; j < 15; j++) {
          this.chessmap[i][j] = 0;
        }
      }
    },

    drawchess(mx, my, colornum) {
      //画棋子
      this.painting(mx, my, colornum);

      if (this.chessmap[mx][my] != 0) {
        this.step++;
        return;
      }
      this.doStore(this.username, mx, my, colornum + 1, this.step + 1);

      this.chessmap[mx][my] = colornum + 1;

      this.checkwin(mx, my, (this.step % 2) + 1, this.mode);

      this.step++;
    },

    painting(mx, my, colornum) {
      let color = this.chesscolor[colornum];
      let lx = (+my + 1) * 30; //maplocating
      let ly = (+mx + 1) * 30;
      this.mcb.fillStyle = color;
      this.mcb.beginPath();
      this.mcb.arc(lx, ly, 15, 0, Math.PI * 2, false);
      this.mcb.fill();
      this.mcb.stroke();
    },

    chessing(e) {
      let lx = Math.floor((e.offsetX + 15) / 30) * 30; //location
      let ly = Math.floor((e.offsetY + 15) / 30) * 30;
      let mx = ly / 30 - 1; //maplocating
      let my = lx / 30 - 1;

      if (lx == 0 || lx == 480 || ly == 0 || ly == 480) {
        return;
      }

      if (this.chessmap[mx][my] != 0) {
        return;
      }

      this.drawchess(mx, my, this.step % 2);
    },

    checkwin(x, y, cn, mode) {
      for (let k = 0; k < 4; k++) {
        let count = 1;
        for (let i = 1; i < 5; i++) {
          if (this.chessmap[x + i * mode[k][0]]) {
            if (this.chessmap[x + i * mode[k][0]][y + i * mode[k][1]] == cn) {
              count++;
            } else {
              break;
            }
          }
        }

        for (let i = 1; i < 5; i++) {
          if (this.chessmap[x - i * mode[k][0]]) {
            if (this.chessmap[x - i * mode[k][0]][y - i * mode[k][1]] == cn) {
              count++;
            } else {
              break;
            }
          }
        }

        if (count >= 5) alert(this.chesscolor[cn - 1] + " wins this round!");
        
      }
    },

    doStore(username, mapx, mapy, color, step) {
      this.$axios
        .post(
          "/api/chessing",
          qs.stringify({
            username: username,
            mapx: mapx,
            mapy: mapy,
            color: color,
            step: step,
          })
        )
        .then((res) => {});
    },

    drawbeforemap(username) {
      this.$axios
        .post(
          "/api/getmap",
          qs.stringify({
            username: username,
          })
        )
        .then((res) => {
          res = res.data.res;
          if (res.length > 0) {
            for (let i = 0; i < res.length; i++) {
              this.chessmap[res[i][0]][res[i][1]] = res[i][2];
              this.drawchess(res[i][0], res[i][1], this.step % 2);
            }
          }
        });
    },

    regret() {
      this.$axios
        .post(
          "/api/regret",
          qs.stringify({
            username: this.username,
            step: this.step,
          })
        )
        .then((res) => {
          if (res.data.msg == "regret") {
            this.$router.go(0);
          }
        });
    },

    newgame() {
      this.$axios
        .post(
          "/api/newgame",
          qs.stringify({
            username: this.username,
          })
        )
        .then((res) => {
          if (res.data.msg == "newgame") {
            this.$router.go(0);
          }
        });
    },
  },
  mounted() {
    this.initCanvas();
    this.initchessmap();
    this.drawbeforemap(this.username);
  },
};
</script>

<style>
#body {
  background-image: url(../assets/bg.gif);
}

#regret {
  margin-right: 200px;
  margin-bottom: 50px;
}

#music {
}

#canvas {
  display: block;
  margin: 10px auto;
  background-color: #fff;
}
</style>