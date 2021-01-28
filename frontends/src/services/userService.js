import axios from "axios";

axios.defaults.headers.post['Content-Type'] = 'application/json';

export async function login(loginInfo) {
  var resp = await axios.post("/api/login/", loginInfo);
  var token = resp.data.token; // 拿到服务器的令牌
  if (token) {
    // 把令牌保存下来
    localStorage.setItem("token", token);
    var user = resp.data.user;
    localStorage.setItem("UserInfo", JSON.stringify(user));
  }
  return resp;
}

axios.defaults.headers['Authorization'] = 'JWT ' + localStorage.getItem("token");
export async function getLiaisons(loginInfo) {
  var resp = await axios.get("/api/liaisons/", loginInfo);
  var token = resp.headers.authorization; // 拿到服务器的令牌
  if (token) {
    // 把令牌保存下来
    localStorage.setItem("token", token);
  }
  return resp;
}
