const checkout = document.getElementById("buy");
checkout.onmouseover = function () {
    this.style.color = "blue";
}
checkout.onmouseout = function () {
    this.style.color = "darkmagenta";
}
checkout.onclick = function () {
    window.location.href = "/buy"
}