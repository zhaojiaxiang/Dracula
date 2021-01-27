
export function getToken(){
    var token = localStorage.getItem('token');
    return token;
}

export function removeToken(){
    localStorage.removeItem('token');
}