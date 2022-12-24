
function add_like(user_id, post_id){
    const request = new XMLHttpRequest();
    api_url = "/api/like/" + user_id + "/" + post_id
    console.log(api_url)
    request.open("GET", api_url)
    request.send()
    request.onload = ()=>{
        console.log(request)
        if (request.status == 201){
            console.log(request.response)
            i_d = post_id + "_like"
            i_d_r = post_id + "_remove_like"
            console.log(i_d)
            const ele = document.getElementById(i_d)
            ele.style.display = 'none'
            const ele2 = document.getElementById(i_d_r)
            ele2.style.display = 'block'
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
            if (request.status == 201){
                console.log(request.response)
                i_d = post_id + "_like"
                i_d_r = post_id + "_remove_like"
                console.log(i_d)
                const ele = document.getElementById(i_d)
                ele.style.display = 'block'
                const ele2 = document.getElementById(i_d_r)
                ele2.style.display = 'none'
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
        if (request.status == 201){
            console.log(request.response)
            i_d = post_id + "_flag"
            i_d_r = post_id + "_remove_flag"
            console.log(i_d)
            const ele = document.getElementById(i_d)
            ele.style.display = 'none'
            const ele2 = document.getElementById(i_d_r)
            ele2.style.display = 'block'
        }
    }
}
function delete_flag(user_id, post_id){
    const request = new XMLHttpRequest();
    api_url = "/api/flag/" + user_id + "/" + post_id
    console.log(api_url)
    request.open("DELETE", api_url)
    request.send()
    request.onload = ()=>{
        console.log(request)
        if (request.status == 201){
            console.log(request.response)
            i_d = post_id + "_flag"
            i_d_r = post_id + "_remove_flag"
            console.log(i_d)
            const ele = document.getElementById(i_d)
            ele.style.display = 'block'
            const ele2 = document.getElementById(i_d_r)
            ele2.style.display = 'none'
        }
    }
}