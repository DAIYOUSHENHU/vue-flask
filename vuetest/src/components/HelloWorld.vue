<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <h1>请先注册登录</h1>
    <div>
      <div>
        <label for="username">Username</label>
        <input v-model="username" placeholder="用户名" />
      </div>
      <div>
        <label for="password">Password</label>
        <input v-model="password" placeholder="密码" />
      </div>

      <div>
        <button id="login" @click="doLogin">登录</button>
      </div>
    </div>
  </div>
</template>

<script>
import qs from "qs";
export default {
  name: "HelloWorld",
  data() {
    return {
      username: "",
      password: "",
    };
  },
  methods: {
    doLogin() {
      this.$axios
        .post(
          "/login",
          qs.stringify({
            username: this.username,
            password: this.password,
          })
        )
        .then((res) => {
          if (res.data.msg == "success") {
            this.$router.push({
              path: "/mychess",
              query: { username: this.username },
            });
          } else {
            alert("账号或密码错误！");
          }
        });
    },
  },
  props: {
    msg: String,
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

#login {
  margin-top: 10px;
}
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
