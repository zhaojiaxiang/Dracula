import axios from 'axios'

export default function(vm) {
    axios.interceptors.request.use(config=>{
        config.headers.post["Content-Type"] = "application/json";
        let token = localStorage.getItem("token")
        if (token) {
            config.headers.Authorization = "JWT " + token;
        }
        return config;
    });

    axios.interceptors.response.use(resp=>{
        if (resp.data && resp.data.code && resp.data.code === 401){
            localStorage.removeItem("token")
            vm.$router.push("/login")
        }
        return resp;
    });
}