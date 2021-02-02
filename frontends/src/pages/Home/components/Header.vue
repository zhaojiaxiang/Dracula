<template>
  <div class="header-height">
    <b-navbar toggleable="lg" type="dark" variant="dark" class="header-height">
      <b-img :src="settings.picture" alt="Transparent image"></b-img>
      <b-navbar-brand style="margin-left:20px">上海埃米柯管理系统</b-navbar-brand>
      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
      
      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav class="ml-auto">
          <b-nav-form>
            <b-input-group size="sm" class="mr-sm-2">
              <b-input-group-prepend is-text>
                <b-icon icon="search"></b-icon>
              </b-input-group-prepend>
              <b-form-input type="search" placeholder="Search"></b-form-input>
            </b-input-group>
          </b-nav-form>
          <b-nav-item @click="openSlipNoNew()">
              新建
          </b-nav-item>
          <b-nav-item-dropdown id="dropdown-1">
              <template #button-content>
              <b-icon icon="person-fill"></b-icon>{{userInfo.name}}
            </template>
            <b-dropdown-item @click="settingClick"><b-icon icon="gear-fill" aria-hidden="true"></b-icon>  设置</b-dropdown-item>
            <b-dropdown-item><b-icon icon="power" aria-hidden="true"></b-icon>  退出</b-dropdown-item>
          </b-nav-item-dropdown>

        <b-avatar variant="info" :src="userInfo.avatar" class="mr-sm-2"></b-avatar>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
  </div>
</template>

<script>
import { getLiaisons } from '@/services/userService'
import { getSettings } from "@/services/commonService.js";
export default {
  data() {
    return {
      userInfo:{},
      settings:{}
    }
  },
  methods: {
    openSlipNoNew(){
      this.bus.$emit('openSlipNoNew')
    },
    handleSelect(key, keyPath) {
      console.log(key, keyPath);
    },
    settingClick:function(){
      var resp = getLiaisons()
      console.log(resp)
    }
    
  },
  mounted:async function(){
    this.userInfo = JSON.parse(localStorage.getItem("UserInfo"));
    var resp = await getSettings(1)
    this.settings = resp.data
  }
};
</script>

<style scoped>
.header-height{
  height: 100%;
}
</style>
