document.addEventListener("DOMContentLoaded", function(event) { 
    let crawlType = document.getElementById("type");
    let resultContent = document.getElementById("result-content");
    let facebook = document.getElementById("facebook");
    let others = document.getElementById("others");

    window.onload = load();
    function load () {
        console.log('Run')
        if (crawlType.innerText === 'Facebook') {
            facebook.hidden = false;
        } else {
            others.hidden = false;
        };
    };
});