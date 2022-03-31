document.addEventListener("DOMContentLoaded", function(event) { 
    let crawlType = document.getElementById("type");
    let resultContent = document.getElementById("result-content");
    let facebook = document.getElementById("facebook");
    let google = document.getElementById("google");
    let others = document.getElementById("others");

    window.onload = load();
    function load () {
        console.log('Run')
        if (crawlType.innerText === "{'value': 3, 'label': 'Facebook'}") {
            facebook.hidden = false;
        } else if (crawlType.innerText === "{'value': 4, 'label': 'Google Image'}") {
            google.hidden = false;
        } else {
            others.hidden = false;
        };
    };
});