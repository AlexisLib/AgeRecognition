function simulateSendForm(){

     document.getElementById("sendForm").click();
}

function simulateSendFormAvance(){

     document.getElementById("sendFormAvance").click();
}

document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('select');
    var instances = M.FormSelect.init(elems, []);
});