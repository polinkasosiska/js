btn = document.getElementById('gen_btn')
let film_name = document.getElementById('name')
let description = document.getElementById('description')
let img = document.getElementById('img')

let current = 0

let container = document.getElementById('catalog_container')

let catalog = {}

fetch("http://localhost:80/jewelry").then((Response) => {
    return Response.json()
}).then((data) => {

    data.forEach(element => {
        catalog[element['id']] = element
        container.innerHTML += '<div class="card">\
        <h1>id:' + element['id'] + '</h1>\
        <h1>name:'+ element['name'] + '</h1>\
        <h1>price:'+ element['price'] + '</h1>\
        <button class="btn" onclick="addToCart('+ element['id'] + ')">Добавить</button>\
        </div>'
    })

})

function addToCart(id) {
    fetch("http://localhost:8001/cart", {
        method: "POST",
        body: JSON.stringify(catalog[id]),
        headers: {
            "Content-type": "application/json; charset=UTF-8"
        }
    });

}


