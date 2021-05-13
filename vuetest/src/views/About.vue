<template>
  <div class="about">
    <h1>账号注册</h1>
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
        <button @click="doRegister">注册</button>
      </div>
    </div>
  </div>
</template>

<script>
import qs from "qs";
export default {
  name: 'About',
  data() {
    return {
      username: "",
      password: "",
    };
  },
  methods: {
    doRegister() {
      this.$axios
        .post(
          "/api/register",
          qs.stringify({
            username: this.username,
            password: this.password,
          })
        )
        .then((res) => {
          if(res.data.msg == 'exist') {
            alert('该用户已存在！')
          }else {
            alert('注册成功！请登录')
          }
        });
    },
  },
}
</script>
