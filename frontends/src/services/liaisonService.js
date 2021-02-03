import axios from "axios";

axios.defaults.headers.post["Content-Type"] = "application/json";
axios.defaults.headers["Authorization"] =
  "JWT " + localStorage.getItem("token");

export async function getLiaisons() {
  var resp = await axios.get("/api/liaisons/");
  return resp;
}

export async function getLiaisonsViaPagination(page, size){
  var resp = await axios.get("/api/liaisons/?page="+ page +"&page_size="+size )
  return resp;
}

export async function newLiaison(liaisonInfo) {
  var resp = await axios.post("/api/liaisons/", liaisonInfo);
  return resp;
}

export async function getSingleLiaison(id) {
  var resp = await axios.get("/api/liaisons/" + id + "/");
  return resp;
}

export async function getSingleLiaisonBySlipNo(slipno) {
  var resp = await axios.get("/api/liaisons/?fslipno=" + slipno);
  return resp;
}

export async function updateLiaisonStatus(id, StatusInfo) {
  var resp = await axios.put("/api/liaison_update_status/" + id + "/", StatusInfo);
  return resp;
}

export async function deleteLiaison(id) {
  var resp = await axios.delete("/api/liaisons/" + id + "/");
  return resp;
}

export async function modifyLiaison(id, liaisonInfo) {
  var resp = await axios.put("/api/liaisons/" + id + "/", liaisonInfo);
  return resp;
}

export async function myOrderInfo(){
  var resp = await axios.get("api/mine_order_info/")
  return resp;
}

export async function getMyTaskBar(){
  var resp = await axios.get('/api/mine_task_bar/')
  return resp
}

export async function getMyMCL(){
  var resp = await axios.get('/api/mine_task_mcl/')
  return resp
}

export async function getMyPCL(){
  var resp = await axios.get('/api/mine_task_pcl/')
  return resp
}

export async function getMyApproval(){
  var resp = await axios.get('/api/mine_task_approval/')
  return resp
}

export async function getMyConfirm(){
  var resp = await axios.get('/api/mine_task_conform/')
  return resp
}

export async function getMyRelease(){
  var resp = await axios.get('/api/mine_task_release/')
  return resp
}

export async function liaisonfileUpdate(form){
  var resp = await axios.post("/api/liaison_file_upload/", form)
  return resp
}