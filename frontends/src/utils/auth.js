import axios from "axios";
import { getSettings } from "@/services/commonService.js";

axios.defaults.headers.post["Content-Type"] = "application/json";

export function getToken() {
  var token = localStorage.getItem("token");
  return token;
}

export async function initLogo() {
    var logo = localStorage.getItem("logo")
    if(!logo){
        var resp = await getSettings(1);
        localStorage.setItem("logo", resp.data.picture);
    }
  
}

export function removeToken() {
  localStorage.removeItem("token");
  localStorage.removeItem("UserInfo");
}

export async function isLogin() {
  axios.defaults.headers["Authorization"] =
  "JWT " + localStorage.getItem("token");
  var resp = await axios.get("/api/");
  if (resp.data.code === 401) {
    return false;
  }
  return true;
}
