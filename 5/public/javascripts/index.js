const t1 = document.getElementById("t1")

function getCookie(cname) {
    const name = cname + "=";
    const decodedCookie = decodeURIComponent(document.cookie);
    const ca = decodedCookie.split(';');
    for (let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) === ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) === 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

const cart = getCookie("cart").split("|");
console.log(cart);
let trs = t1.children[0].children
for (let i = 0; i < trs.length; i++) {
    if (trs[i].children.length) {
        if (cart.includes(trs[i].children[0].textContent)) {
            trs[i].style.border = "1px solid gray";
            trs[i].children[1].children[0].style.color = "gray";
            trs[i].children[0].style.color = "gray";
        } else {
            trs[i].children[1].children[0].onmouseover = function () {
                this.parentElement.parentElement.style.border = "2px solid darkmagenta";
            }
            trs[i].children[1].children[0].onmouseout = function () {
                this.parentElement.parentElement.style.border = "1px solid darkmagenta";
            }
            trs[i].children[1].children[0].onclick = function () {
                const cart = getCookie("cart");
                const item = this.parentElement.parentElement.children[0].textContent;
                document.cookie = "cart=" + cart + item + "|";
                this.parentElement.parentElement.style.border = "1px solid gray";
                this.style.color = "gray";
                this.parentElement.parentElement.children[0].style.color = "gray";
                this.onclick = null;
                this.onmouseout = null;
                this.onmouseover = null;
            }
        }
    }
}

const checkout = document.getElementById("checkout");
checkout.onmouseover = function () {
    this.style.color = "blue";
}
checkout.onmouseout = function () {
    this.style.color = "darkmagenta";
}
checkout.onclick = function () {
    if (getCookie('cart'))
        window.location.href = "/checkout"
    else alert("Your cart is empty.")
}