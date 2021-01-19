import axios from "axios";

axios.defaults.headers.post["Content-Type"] = "application/json";
axios.defaults.headers["Authorization"] =
  "JWT " + localStorage.getItem("token");

export async function getProjects() {
  var resp = await axios.get("/api/projects/");
  return resp;
}

export async function getSystems() {
  var resp = await axios.get("/api/systems/");
  return resp;
}

export async function getGroupUsers(){
  var resp = await axios.get("/api/group_users/")
  return resp
}

export async function getAllUsers(){
  var resp = await axios.get("/api/accounts/")
  return resp
}
