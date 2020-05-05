const express = require('express');
const router = express.Router();

const itemModel = require('../models/Item');

itemModel.deleteMany(function (err, docs) {
});
const arr = [{name: "Goose"},
    {name: "Kokafeat crewneck"},
    {name: "A 5.0 card"},
    {name: "Bridge to Terabithia"},
    {name: "42"},
    {name: "4 elephants standing on a giant turtle"},
    {name: "Stylish facemask"}];
itemModel.insertMany(arr, function (err, docs) {
});

function getCookie(request, cname) {
    const name = cname + "=";
    const decodedCookie = decodeURIComponent(request.headers.cookie);
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

/* GET home page. */
router.get('/', function (req, res, next) {
    itemModel.find(function (err, items) {
        if (err) throw err;
        res.render('index', {items: items});
    });
});

router.get('/checkout', function (req, res, next) {
    const cart = getCookie(req, "cart").split("|");
    if (cart.length === 0) {
        res.render("invalidcart", {"error": "Your cart was empty."});
        return;
    }
    itemModel.find({name: {$in: cart}},
        function (err, items) {
            if (err) throw err;
            if (items.length + 1 !== cart.length) {
                res.render("invalidcart", {"error": "Some products from your cart were already bought."})
            } else {
                res.render('checkout', {items: items});
            }
        });
});

router.get('/buy', function (req, res, next) {
    const cart = getCookie(req, "cart").split("|");
    if (cart.length === 0) {
        res.render("invalidcart", {"error": "Your cart was empty."});
        return;
    }
    itemModel.find({name: {$in: cart}},
        function (err, items) {
            if (err) throw err;
            if (items.length + 1 !== cart.length) {
                res.render("invalidcart", {"error": "Some products from your cart were already bought."})
            } else {
                itemModel.deleteMany({name: {$in: cart}}, function (err, result) {
                    if (err) throw err;
                    res.render("bought")
                })

            }
        });
});

module.exports = router;
