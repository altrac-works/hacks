// ==UserScript==
// @name         Paste form data
// @namespace    https://tris.fyi/
// @version      0.1
// @description  Paste form data into fields
// @author       Tris Emmy Wilson
// @match        https://actionnetwork.org/*
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    function $(x) { return document.querySelector(x); }
    function $$(x) { return document.querySelectorAll(x); }
    function each(x, y) { return Array.prototype.forEach.call(x, y); }

    function handlePasteFormData(event) {
        var data = event.clipboardData.getData("text").trim();
        data = data.split(";");

        console.log(data);
        each(data, function(kv) {
            kv = kv.split("=");
            var k = kv[0];
            var v = kv[1];

            var el = document.getElementById(k);
            if(el) {
                if(v === "UNCHECK") {
                    el.checked = false;
                } else if(v === "CHECK") {
                    el.checked = true;
                }
                else {
                    el.value = v;
                }
                el.dispatchEvent(new Event("change"));
            }
        });
    }
    document.body.addEventListener("paste", handlePasteFormData);

    document.addEventListener("DOMContentLoaded", function() {
        alert("here");
    });
})();
