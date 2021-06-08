<template>
  <div class="header-height">
    <b-navbar toggleable="lg" type="dark" variant="dark" class="header-height">
      <b-navbar-brand>上海埃米柯管理系统</b-navbar-brand>
      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav class="ml-auto">
          <b-nav-form>
            <b-input-group size="sm" class="mr-sm-2">
              <b-input-group-prepend is-text>
                <b-icon icon="search"></b-icon>
              </b-input-group-prepend>
              <b-form-input
                type="search"
                placeholder="暂时不可用..."
              ></b-form-input>
            </b-input-group>
          </b-nav-form>
          <b-nav-item-dropdown id="dropdown-1">
            <template #button-content>
              <b-icon icon="person-fill"></b-icon>{{ userInfo.name }}
            </template>
            <b-dropdown-item @click="profile"
              ><b-icon icon="gear-fill" aria-hidden="true"></b-icon>
              个人中心</b-dropdown-item
            >
            <b-dropdown-item @click="logout"
              ><b-icon icon="power" aria-hidden="true"></b-icon>
              退出</b-dropdown-item
            >
          </b-nav-item-dropdown>

          <b-avatar
            variant="info"
            :src="userInfo.avatar"
            :text="userInfo.str_avatar"
            class="mr-sm-2"
          ></b-avatar>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
  </div>
</template>

<script>
import { removeToken } from "@/utils/auth";
export default {
  data() {
    return {
      userInfo: {},
      settings: {},
      logo: localStorage.getItem("logo"),
    };
  },
  methods: {
    logout: function () {
      removeToken();
      window.location.reload();
    },
    profile() {
      this.$router.push({
        name: "Profile",
      });
    },
  },
  mounted: function () {
    this.bus.$on("login_succ", () => {
      this.userInfo = JSON.parse(localStorage.getItem("UserInfo"));
    });
    this.userInfo = JSON.parse(localStorage.getItem("UserInfo"));
  },
};
</script>

<style scoped>
.header-height {
  height: 100%;
}
</style>
