import axios from "axios";

export async function getProjectDetailView(order_no){
    var resp = axios.get("/api/qa_project_detail_view/?order_no="+order_no)
    return resp;
}

export async function getQaProjectGroup(organization_id, project_code, order_no){
  var resp = axios.get("/api/qa_project_group/?forganization="+ organization_id +"&fprojectcd="+ project_code +"&fodrno=" + order_no)
  return resp;
}