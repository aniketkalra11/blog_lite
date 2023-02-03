
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
            like_count_id = post_id + "_like_count"
            change_like_count(id= like_count_id, r_str = request.response)
        }
        else if (request.status == 403){
            console.log('already flagged post found')
            alert('you can\'t like a post that you already flagged')
        }else{
            alert('unable to process your request please try after some time')
        }
    }
}

function change_like_count(id, r_str){
    const ele3 = document.getElementById(id)
    j_obj = JSON.parse(r_str)
    console.log(j_obj)
    ele3.innerHTML = j_obj['likes']
}

function change_flag_count(id, r_str){
    const ele3 = document.getElementById(id)
    j_obj = JSON.parse(r_str)
    console.log(j_obj)
    ele3.innerHTML = j_obj['flags']
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
                like_count_id = post_id + "_like_count"
                change_like_count(id= like_count_id, r_str = request.response)
            }else{
                alert('unable to process your request please try after some time')
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
            flag_count_id = post_id + "_flag_count"
            change_flag_count(id=flag_count_id, request.response)
        }
        else if (request.status == 403){
            console.log('already flagged post found')
            alert('you can\'t flag a post that you already like')
        }
        else{
            alert('unable to process your request please try after some time')
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
            flag_count_id = post_id + "_flag_count"
            change_flag_count(id=flag_count_id, request.response)
        }else{
            alert('unable to process your request please try after some time')
        }
    }
}