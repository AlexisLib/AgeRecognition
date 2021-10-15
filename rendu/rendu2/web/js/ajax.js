// Create the XHR object.
function createCORSRequest(method, url) {
    var xhr = new XMLHttpRequest();
    if ("withCredentials" in xhr) {
        // XHR for Chrome/Firefox/Opera/Safari.
        xhr.open(method, url, true);
        xhr.withCredentials = true;
    }else if (typeof XDomainRequest != "undefined"){
        // XDomainRequest for IE.
        xhr = new XDomainRequest();
        xhr.open(method, url);
    }else{
        // CORS not supported.
        xhr = null;
    }
    return xhr;
}

function fillTableResult(jsonResult){

    console.log(jsonResult);

    var tbody = document.getElementById("tbodyResults")

    for (var element in jsonResult["order"]){

        var row = document.createElement('tr')
        
        var cell = document.createElement('td')
        cell.innerHTML = jsonResult["order"][element]
        row.appendChild(cell)

        cell = document.createElement('td')
        cell.innerHTML = jsonResult["implement"][jsonResult["order"][element]]
        row.appendChild(cell)

        cell = document.createElement('td')
        cell.innerHTML = jsonResult["framework"][jsonResult["order"][element]]
        row.appendChild(cell)    

        tbody.appendChild(row)
    }        
}

// Make the actual CORS request.
function getResults() {
    // This is a sample server that supports CORS.
    var url = 'http://192.168.1.20:1111/results/';

    var xhr = createCORSRequest('GET', url);
    if (!xhr) {
        alert('CORS not supported');
        return;
    }

    // Response handlers.
    xhr.onload = function() {
        var text = xhr.responseText;
        //alert('Response from CORS request to ' + url + ': is ok : ' + text);
        fillTableResult(JSON.parse(text));
    };

    xhr.onerror = function() {
        alert('Erreur AJAX API.');
    };

    xhr.send();
}