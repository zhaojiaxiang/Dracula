import axios from "axios";


export async function getProjectMaster(){
    var resp = await axios.get("/api/projects/")
    return resp;
}

export async function newProjectMaster(form){
    var resp = await axios.post("/api/projects/", form)
    return resp;
}

export async function deleteProjectMaster(id){
    var resp = await axios.delete("/api/projects/" + id + "/")
    return resp;
}

export async function getSystemMaster(){
    var resp = await axios.get("/api/systems/")
    return resp;
}

export async function newSystemMaster(form){
    var resp = await axios.post("/api/systems/", form)
    return resp;
}

export async function deleteSystemMaster(id){
    var resp = await axios.delete("/api/systems/" + id + "/")
    return resp;
}