
function add_follower(user_id, f_user_id){
    const request = new XMLHttpRequest();
    api_url = "/api/follow/" + user_id + "/" + f_user_id
    console.log(api_url)
    request.open("GET", api_url)
    request.send()
    request.onload = ()=>{
        console.log(request)
        if (request.status == 201){
            console.log(request.response)
            i_d = f_user_id + "_follow"
            i_d_r = f_user_id + "_unfollow"
            console.log(i_d)
            const ele = document.getElementById(i_d)
            ele.style.display = 'none'
            const ele2 = document.getElementById(i_d_r)
            ele2.style.display = 'inline-block'
            p_id = f_user_id + '_p'
            const p = document.getElementById(p_id)
            res = request.responseText
            parse = JSON.parse(res)
            console.log(parse)
            console.log(res)
            p.innerHTML = parse['num_followers']
        }
    }
}
function delete_follower(user_id, f_user_id){
    const request = new XMLHttpRequest();
    api_url = "/api/follow/" + user_id + "/" + f_user_id
    console.log(api_url)
    request.open("DELETE", api_url)
    request.send()
    request.onload = ()=>{
        console.log(request)
        if (request.status == 201){
            console.log(request.response)
            i_d = f_user_id + "_follow"
            i_d_r = f_user_id + "_unfollow"
            console.log(i_d)
            const ele = document.getElementById(i_d)
            ele.style.display = 'inline-block'
            const ele2 = document.getElementById(i_d_r)
            ele2.style.display = 'none'
            p_id = f_user_id + '_p'
            const p = document.getElementById(p_id)
            res = request.responseText
            parse = JSON.parse(res)
            console.log(parse)
            console.log(res)
            p.innerHTML = parse['num_followers']
        }
    }
}