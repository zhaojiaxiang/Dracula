import axios from "axios";

axios.defaults.headers.post["Content-Type"] = "application/json";
axios.defaults.headers["Authorization"] =
    "JWT " + localStorage.getItem("token");


export async function getCheckoutList(applicant, chkstatus) {
    var resp = await axios.get("api/pb_file_checkout/?page_size=1000&fapplicant=" + applicant + "&fchkstatus=" + chkstatus)
    return resp;
}

export async function getAddressList() {
    var resp = await axios.get("api/accounts/")
    return resp;
}

export async function getCheckoutlistViaPagination(page, size, system, chkstatus, applicant, chkoutobj, slipno) {
    var resp = await axios.get("/api/pb_file_checkout/?page=" + page + "&page_size=" + size + "&fsystem=" + system +
        "&fslipno=" + slipno + "&fchkoutobj=" + chkoutobj + "&fchkstatus=" + chkstatus + "&fapplicant=" + applicant)
    return resp;
}

export async function deleteCheckoutData(id) {
    var resp = await axios.delete("/api/pb_file_checkout/" + id + "/");
    return resp;
}

export async function updateCheckoutData(id, chkoutInfo) {
    var resp = await axios.put("/api/pb_file_checkout/" + id + "/", chkoutInfo);
    return resp;
}

export async function newCheckoutData(chkoutInfo) {
    var resp = await axios.post("/api/pb_file_checkout/", chkoutInfo);
    return resp;
}

export async function getCheckoutData(id) {
    var resp = await axios.get("/api/pb_file_checkout/" + id + "/");
    return resp;
}

export async function sendMail(senddata) {
    var resp = await axios.post("/api/sendemail/",senddata);
    return resp;
}
