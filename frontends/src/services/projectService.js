import axios from "axios";

axios.defaults.headers.post["Content-Type"] = "application/json";
axios.defaults.headers["Authorization"] =
  "JWT " + localStorage.getItem("token");


export async function getProjectDetailView(order_no){
    var resp = axios.get("/api/qa_project_detail_view/?order_no="+order_no)
    return resp;
}

export async function getQaProjectGroup(project_code, order_no){
  var resp = axios.get("/api/qa_project_group/?fprojectcd="+ project_code +"&fodrno=" + order_no)
  return resp;
}