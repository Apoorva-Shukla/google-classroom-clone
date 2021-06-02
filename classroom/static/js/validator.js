document.querySelector('form').addEventListener('submit', (e) => {
    let div = document.createElement("div");
    div.className += "overlay";
    document.body.appendChild(div);
});