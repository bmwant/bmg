/**
 * Created by Most Wanted on 09.04.15.
 */

function cleanData() {
    localStorage.clear();
}

function presentInLS(key) {
    var value = localStorage.getItem(key);
    return (value != undefined) && (value != "") && (value != null);
}

function getDataFromLS() {
    var data = {};
    for (var i = 0; i < localStorage.length; i++) {
        var key = localStorage.key(i);
        data[key] = localStorage.getItem(key);
    }
    return data;
}

function setDropdown(selector, value) {
    if (value) {
        $(selector).val(value);
        $(selector).change(); //fire change
    }
}