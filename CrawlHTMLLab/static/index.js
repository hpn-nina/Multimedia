document.addEventListener("DOMContentLoaded", function(event) { 
    let selectCrawlOption = document.getElementById("crawlOptions");
    let inputKeyword = document.getElementById("keyword");

    selectCrawlOption.addEventListener("change", () => {
        inputKeyword.disabled = false

        if (selectCrawlOption.value === "1")
            inputKeyword.placeholder = 'Enter author name';
        else 
            inputKeyword.placeholder = 'Enter keyword';
    })

    inputKeyword.addEventListener("keyup", () => {
        if (inputKeyword.value.length > 0) {
            document.getElementById("submitBtn").disabled = false;
        } else {
            document.getElementById("submitBtn").disabled = true;
        }
    })
    
});
