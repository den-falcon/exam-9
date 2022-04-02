let imagesButtons = document.getElementsByName('images-favorite')
let albumButtons = document.getElementsByName('album-favorite')

async function likeOrUnlike(event, method='POST') {
    let eventTarget = event.target;
    let url = eventTarget.dataset.requestUrl;
    let csrf = document.cookie.match(/csrftoken=([\w-]+)/)[1];
    let request = new Request(url, {headers: {'X-CSRFToken': csrf}});
    let response;
    if (eventTarget.dataset.isLiked === 'false') {
        response = await fetch(request, {method});
    } else {
        method = 'DELETE'
        response = await fetch(request, {method});
    }

    if (response.ok) {
        let responseBody = await response.json();
        if (responseBody['is_fan']) {
            eventTarget.innerText = 'Удалить из избранного';
        } else {
            eventTarget.innerText = 'Добавить в избранное';
        }
        eventTarget.dataset.isLiked = responseBody['is_fan'];
        return responseBody;
    }
}


window.addEventListener('load', function() {
    for (let i=0; i<imagesButtons.length; i++) {
            imagesButtons[i].addEventListener('click', likeOrUnlike)
    }
    for (let i=0; i<albumButtons.length; i++) {
        albumButtons[i].addEventListener('click', likeOrUnlike)
    }
})