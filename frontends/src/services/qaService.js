import axios from "axios";

axios.defaults.headers.post["Content-Type"] = "application/json";
axios.defaults.headers["Authorization"] =
  "JWT " + localStorage.getItem("token");

export async function getQaHead(id) {
  var resp = await axios.get("/api/qa/mcl_head/" + id + "/");
  return resp;
}

export async function getQaHeadBySlipNo(slipno) {
  var resp = await axios.get("/api/qa/mcl_head/?fslipno=" + slipno);
  return resp;
}

export async function newQaHead(qaHeadInfo) {
  var resp = await axios.post("/api/qa/mcl_head/", qaHeadInfo);
  return resp;
}

export async function updateQaHead(id, qaHeadInfo) {
  var resp = await axios.put("/api/qa/mcl_head/" + id + "/", qaHeadInfo);
  return resp;
}

export async function updateQaHeadSummary(id, qaHeadInfo) {
  var resp = await axios.put("/api/qa/mcl_head_update_summary/" + id + "/", qaHeadInfo);
  return resp;
}

export async function getQaHeadModifyDetail(id) {
  var resp = await axios.get("/api/qa/mcl_head_modify_detail/" + id + "/");
  return resp;
}

export async function updateQaHeadModifyDetail(id, qaHeadInfo) {
  var resp = await axios.put("/api/qa/mcl_head_modify_detail/" + id + "/", qaHeadInfo);
  return resp;
}

export async function deleteQaHead(id) {
  var resp = await axios.delete("/api/qa/mcl_head/" + id + "/");
  return resp;
}

export async function newQaDetail(qaDetailInfo) {
  var resp = await axios.post("/api/qa/mcl_detail/", qaDetailInfo);
  return resp;
}

export async function getQaDetailByQaHead(id) {
  var resp = await axios.get("/api/qa/mcl_detail/?qahf=" + id);
  return resp;
}

export async function getQaDetailContentText(id) {
  var resp = await axios.get(
    "/api/qa/mcl_detail_update_content_text/" + id + "/"
  );
  return resp;
}

export async function updateQaDetailContentText(id, form) {
  var resp = await axios.put(
    "/api/qa/mcl_detail_update_content_text/" + id + "/", form
  );
  return resp;
}


export async function updateQaDetail(id, qaDetailInfo) {
  var resp = await axios.put("/api/qa/mcl_detail/" + id + "/", qaDetailInfo);
  return resp;
}

export async function getQaDetail(id) {
  var resp = await axios.get("/api/qa/mcl_detail/" + id + "/");
  return resp;
}

export async function deleteQaDetail(id) {
  var resp = await axios.delete("/api/qa/mcl_detail/" + id + "/");
  return resp;
}

export async function getQaHeadPlanActual(id){
  var resp = await axios.get("/api/qa/mcl_head_target_actual/" + id + "/");
  return resp;
}

export async function updateQaDetailResult(id, qaDetailInfo){
  var resp = await axios.put("/api/qa/mcl_detail_update_result/"+ id +"/", qaDetailInfo)
  return resp
}

export async function fileUpdate(form){
  var resp = await axios.post("/api/file_upload/", form)
  return resp
}