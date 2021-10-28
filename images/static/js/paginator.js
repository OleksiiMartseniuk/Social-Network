

let page = 1
let empty_page = false
let block_request = false

window.addEventListener('scroll', () => {
    const scrollable = document.documentElement.scrollHeight - window.innerHeight;
    const scrolled = window.scrollY;
    if (Math.ceil(scrolled) === scrollable && empty_page === false && block_request === false){
        block_request = true;
        page += 1;
     
        fetch('?page=' + page)
        .then(data => {
            if (data === ''){
                empty_page = true;
            }else {
                block_request = false;
                console.log(data.results)
               
            }
        })
        
    }
});


