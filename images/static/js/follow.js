function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrf_token = getCookie('csrftoken');


async function postData(url, data ) {
    const response = await fetch(url, {
        method: 'POST',    
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token
        },
        body: JSON.stringify(data)
    });
    return await response.json(); 
  }


// follow
const follow = document.getElementById('follow')
const total = document.getElementById('total')
follow.onclick = () => {
  let id = follow.attributes[1].textContent;
  let action = follow.attributes[2].textContent;
  let count = total.textContent;
  postData('http://localhost:8000/users/follow/', {id: id, action: action})
  .then((data) => {
    if (data['status'] === 'ok'){
        if (action === 'unfollow'){
            follow.attributes[2].textContent = 'follow';
            total.textContent = Number(count) - 1;
            follow.innerText = 'Follow';
            follow.style.background = '';
            follow.style.color = '';
           
        }else{
            follow.attributes[2].textContent = 'unfollow';
            total.textContent = Number(count) + 1;
            follow.innerText = 'Unfollow';
            follow.style.background = 'red';
            follow.style.color = 'white';
        }

    }
  })
}  