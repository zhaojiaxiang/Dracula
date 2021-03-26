import axios from "axios";

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


export async function getSettings(id){
  var resp = await axios.get("/api/accounts/system_setting/" +id+"/")
  return resp
}

export async function getWorkingOrganization(){
  var resp = await axios.get("/api/working_organization/")
  return resp
}

export async function getWorkingProject(organization){
  var resp = await axios.get("/api/working_project/?organization="+ organization)
  return resp
}