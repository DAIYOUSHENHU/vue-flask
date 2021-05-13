<template>
  <div>
    <ChessBoard></ChessBoard>
    <button @click="getRandom">按钮</button>
    <h1>{{ randnum }}</h1>
    <h1>{{ randnum111 }}</h1>
  </div>
</template>

<script>
import ChessBoard from "../components/ChessBoard";

export default {
  name: "Mychess",
  components: {
    ChessBoard,
  },
  data() {
    return {
      randnum: 0,
      randnum111: 0,
    };
  },
  methods: {
    getRandom() {
      this.$axios.get("/api/mytest").then((res) => {
        this.randnum = res.data.randnum1;
      });

      this.$axios.get("/api/mytest111/aaa").then((res) => {
        this.randnum111 = res.data;
      });

      this.$axios.get("/api/mytest/user/2").then((res) => {
        console.log(res);
      });
    },
  },
};
</script>

<style>
</style>