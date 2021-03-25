import axios from "axios";

axios.defaults.headers.post["Content-Type"] = "application/json";

export function getToken() {
  var token = localStorage.getItem("token");
  return token;
}

export function removeToken() {
  localStorage.removeItem("token");
  localStorage.removeItem("UserInfo");
}

export async function isLogin() {
  axios.defaults.headers["Authorization"] =
  "JWT " + localStorage.getItem("token");
  var resp = await axios.get("/api/");
  console.log(resp);
  if (resp.data.code === 401) {
    return false;
  }
  return true;
}
