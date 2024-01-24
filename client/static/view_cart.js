let container = document.getElementById('cart_container')

fetch("http://localhost:8001/cart").then((Response) => {
    return Response.json()
}).then((data) => {
    data.forEach(element => {
        container.innerHTML += '<div class="card">\
        <h1>id:' + element['id'] + '</h1>\
        <h1>name:'+ element['name'] + '</h1>\
        <h1>price:'+ element['price'] + '</h1>\
        </div>'
    })

    // console.log(data);
    // current = data["kinopoiskId"]
    // film_name.textContent = data["nameOriginal"];
    // img.src = data['posterUrl']
    // description.textContent = data['description']

})