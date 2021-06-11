import axios from "axios";

export async function getReportList(order_no) {
  var resp = await axios.get("/api/report_list/?fodrno=" + order_no);
  return resp;
}

export async function getReportPCLList(order_no) {
  var resp = await axios.get("/api/report_list_pcl/?fodrno=" + order_no);
  return resp;
}

export async function getReportLiaisonInfo(slip_no) {
  var resp = await axios.get("/api/report_liaison_info/?slip_no=" + slip_no);
  return resp;
}

export async function getReportQaInfo(slip_no, image) {
  var resp = await axios.get(
    "/api/report_qa_info/?slip_no=" + slip_no + "&image=" + image
  );
  return resp;
}

export async function getReportOrderInfo(order_no, multiple_slip, image) {
  var resp = await axios.get(
    "/api/report_order_info/?order_no=" + order_no + "&multiple_slip=" + multiple_slip + "&image=" + image
  );
  return resp;
}
