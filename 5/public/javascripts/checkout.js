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

const cancel = document.getElementById("cancel");
cancel.onmouseover = function () {
    this.style.color = "blue";
}
cancel.onmouseout = function () {
    this.style.color = "darkmagenta";
}
cancel.onclick = function () {
    document.cookie = "cart=; expires=Thu, 01 Jan 1970 00:00:00 UTC;";
    window.location.href = "/"
}

const title = document.getElementById("title");
title.onmouseover = function () {
    this.style.color = "blue";
}
title.onmouseout = function () {
    this.style.color = "darkmagenta";
}

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

const t1 = document.getElementById("t1")
let trs = t1.children[0].children
for (let i = 0; i < trs.length; i++) {
    if (trs[i].children.length) {
        trs[i].children[1].onclick = function () {
            const item = this.parentElement.children[0].textContent;
            const cart = getCookie("cart").split("|");
            if(cart.length === 2){
                document.cookie = "cart=; expires=Thu, 01 Jan 1970 00:00:00 UTC;";
                window.location.replace("/");
            }
            document.cookie = "cart=" + cart.filter(function (value, index, arr) {
                return value !== item;
            }).join("|");
            this.parentElement.style.border = "1px solid gray";
            this.style.color = "gray";
            this.parentElement.children[0].style.color = "gray";
            this.onclick = null;
            this.onmouseout = null;
            this.onmouseover = null;
        }
    }
}