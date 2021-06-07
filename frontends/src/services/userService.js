import axios from "axios";

export async function login(loginInfo) {
  var resp = await axios.post("/api/login/", loginInfo);
  var token = resp.data.token; // 拿到服务器的令牌
  if (token) {
    // 把令牌保存下来
    localStorage.setItem("token", token);
    var user = resp.data.user;
    user.str_avatar = user.name.charAt(user.name.length-1)
    localStorage.setItem("UserInfo", JSON.stringify(user));
  }
  return resp;
}

export async function getLiaisons(loginInfo) {
  var resp = await axios.get("/api/liaisons/", loginInfo);
  var token = resp.headers.authorization; // 拿到服务器的令牌
  if (token) {
    // 把令牌保存下来
    localStorage.setItem("token", token);
  }
  return resp;
}

export async function getUserInfo(id){
  var resp = await axios.get("/api/accounts/" + id +"/")
  return resp
}


export async function updateUserPassword(passwordInfo){
  var resp = await axios.post("/api/update_password/", passwordInfo)
  return resp;
}

export async function updateEmailDays(email_days){
  var info = {
    "email_days":email_days
  }
  var resp = await axios.post("/api/update_email_days/", info)
  return resp;
}

export async function updateAvatar(form){
  var resp = await axios.post("/api/update_avatar/", form)
  return resp;
}