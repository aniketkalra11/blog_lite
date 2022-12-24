
function add_like(user_id, post_id){
    const request = new XMLHttpRequest();
    api_url = "/api/like/" + user_id + "/" + post_id
    console.log(api_url)
    request.open("GET", api_url)
    request.send()
    request.onload = ()=>{
        console.log(request)
        if (request.status == 200){
            console.log(request.response)
        }
    }
}
function delete_like(user_id, post_id){
    const request = new XMLHttpRequest();
        api_url = "/api/like/" + user_id + "/" + post_id
        console.log(api_url)
        request.open("DELETE", api_url)
        request.send()
        request.onload = ()=>{
            console.log(request)
            if (request.status == 200){
                console.log(request.response)
            }
        }
}

function add_flag(user_id, post_id){
    const request = new XMLHttpRequest();
    api_url = "/api/flag/" + user_id + "/" + post_id
    console.log(api_url)
    request.open("GET", api_url)
    request.send()
    request.onload = ()=>{
        console.log(request)
        if (request.status == 200){
            console.log(request.response)
        }
    }
}
function delete_like(user_id, post_id){
    const request = new XMLHttpRequest();
    api_url = "/api/flag/" + user_id + "/" + post_id
    console.log(api_url)
    request.open("DELETE", api_url)
    request.send()
    request.onload = ()=>{
        console.log(request)
        if (request.status == 200){
            console.log(request.response)
        }
    }
}