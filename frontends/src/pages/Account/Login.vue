<template>
    <b-row class="text-left text-center">
      <b-col></b-col>
      <b-col></b-col>
      <b-col>
        <div style="margin-top:100px">
          <b-form>
            <b-form-group
              id="input-group-1"
              label-for="input-1"
            >
              <b-form-input
                id="input-1"
                v-model="form.username"
                placeholder="用户名"
                required
              ></b-form-input>
            </b-form-group>

            <b-form-group
              id="input-group-2"
              label-for="input-2"
            >
              <b-form-input
                id="password"
                v-model="form.password"
                placeholder="密码"
                type="password"
                required
              ></b-form-input>
            </b-form-group>
            <b-button @click="handleClick" variant="primary">Submit</b-button>
          </b-form>
        </div>
      </b-col>
      <b-col></b-col>
      <b-col></b-col>
    </b-row>
</template>

<script>
import { login } from '../../services/userService';
export default {
  
    data() {
      return {
        form: {
          username: '',
          password: ''
        },
      }
    },
    methods: {
      handleClick:async function() {
        var resp = await login(JSON.stringify(this.form))
        if(resp.status){
          this.$router.push({ path: '/' })
        }
      },
    }
  }
</script>

<style></style>
