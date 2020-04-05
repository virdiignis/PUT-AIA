var t1 = document.getElementById("t1");
var add_button = document.getElementById("new");

add_button.onclick = function () {
    var row = t1.insertRow();
    if (row.rowIndex % 2 === 1) {
        row.style.background = "lightgray";
    }
    var c1 = row.insertCell(0);
    var c2 = row.insertCell(1);
    var c3 = row.insertCell(2);

    c1.innerHTML = "<input type=\"text\" name=\"f_manufacturer\">";
    c2.innerHTML = "<input type=\"text\" name=\"f_model\">";

    var b1 = document.createElement("input");
    b1.type = "button";
    b1.value = "Save";
    b1.onclick = function () {
        if (b1.value === "Save"){
            b1.value = "Edit";
            for (let i=0; i<2; i++)
            {
                const text = b1.parentElement.parentElement.children[i].firstChild.value;
                b1.parentElement.parentElement.children[i].firstChild.remove();
                const l = document.createElement("b");
                l.textContent = text;
                b1.parentElement.parentElement.children[i].appendChild(l);
            }
        } else {
            b1.value = "Save";
            for (let i=0; i<2; i++)
            {
                const text = b1.parentElement.parentElement.children[i].firstChild.textContent;
                b1.parentElement.parentElement.children[i].firstChild.remove();
                const l = document.createElement("input");
                l.type = "text";
                l.value = text;
                b1.parentElement.parentElement.children[i].appendChild(l);
            }
        }
    };
    c3.appendChild(b1);

    var b2 = document.createElement("input");
    b2.type = "button";
    b2.value = "Remove";
    b2.onclick = function () {
        b2.parentElement.parentElement.remove();
        let rows = t1.getElementsByTagName("tr");
        for(var i = 0; i< rows.length; i++){
            if (rows[i].rowIndex % 2 === 1) {
                rows[i].style.background = "lightgray";
            } else {
                rows[i].style.background = "white";
            }
        }
    };
    c3.appendChild(b2);
};
