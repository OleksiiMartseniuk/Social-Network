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




async function postData(url = '', data = {}) {
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



//like
const icon = document.getElementById('icon')
const like = document.getElementById('like') 
const total_likes = document.getElementById('total') 
like.onclick = () => {
  let id = like.attributes[2].textContent
  let action = like.attributes[3].textContent
  let total = total_likes.textContent 
  postData('http://localhost:8000/images/like/', {id: id, action: action})
    .then((data) => {
        if (data['status'] == 'ok'){
            if (like.attributes[3].textContent === 'like') {
              like.attributes[3].textContent = 'unlike';
              total_likes.textContent = Number(total) + 1;
              icon.style['color'] = 'red';
            } else {
              like.attributes[3].textContent = 'like';
              total_likes.textContent = Number(total) - 1;
              icon.style['color'] = '';
            } 
        }
    });

  console.dir(icon.style['color'] = 'red')  
}


