import * as constant from './enums/constant.js';

document.addEventListener("DOMContentLoaded", function(event) { 
    let selectCrawlOption = document.getElementById("crawlOptions");
    let inputKeyword = document.getElementById("keyword");
    let labelKeyword = document.getElementById("label-keyword");
    let inputPassword = document.getElementById("password");
    let labelPassword = document.getElementById("label-password");
    let targetPage = document.getElementById("target-page");
    let inputTargetPage = document.getElementById("target-page-input");
    let inputQuantity = document.getElementById("post-num");
    let labelImageQuantity = document.getElementById("label-quantity");
    let inputImageQuantity = document.getElementById("quantity");


    const checkValidForm = () => {
        let condition = inputKeyword.value.length > 0 && inputPassword.value.length > 0 && inputTargetPage.value.length > 0 && inputQuantity.value.length > 0;
        if(condition || (inputPassword.hidden && inputKeyword.value.length > 0))
                document.getElementById("submitBtn").disabled = false;
        else 
            document.getElementById("submitBtn").disabled = true;
    }

    const checkValidImageCrawl = () => {
        let condition = inputKeyword.value.length > 0 && inputImageQuantity.value.length > 0;
        if(condition)
                document.getElementById("submitBtn").disabled = false;
        else 
            document.getElementById("submitBtn").disabled = true;
    }

    selectCrawlOption.addEventListener("change", () => {
        inputKeyword.disabled = false;
        inputPassword.hidden = labelPassword.hidden = targetPage.hidden = inputImageQuantity.hidden = labelImageQuantity.hidden = true;
        let requireField = '<span style="color:red">* </span>';

        switch (Number(selectCrawlOption.value)) {
            case constant.CrawlingOptions.RESEARCH_PAPER.value:
                inputKeyword.placeholder = constant.CrawlingOptions.RESEARCH_PAPER.placeholder;
                labelKeyword.innerHTML = requireField + constant.CrawlingOptions.RESEARCH_PAPER.inputLabel;
                break;
            case constant.CrawlingOptions.NEWS.value:
                inputKeyword.placeholder = constant.CrawlingOptions.NEWS.placeholder;
                labelKeyword.innerHTML = requireField + constant.CrawlingOptions.NEWS.inputLabel;
                break;
            case constant.CrawlingOptions.FACEBOOK.value:
                inputKeyword.placeholder = constant.CrawlingOptions.FACEBOOK.placeholder;
                labelKeyword.innerHTML = requireField + constant.CrawlingOptions.FACEBOOK.inputLabel;
                inputPassword.hidden = labelPassword.hidden = targetPage.hidden = false;
                break;
            case constant.CrawlingOptions.GOOGLE_IMAGE.value:
                inputKeyword.placeholder = constant.CrawlingOptions.GOOGLE_IMAGE.placeholder;
                labelKeyword.innerHTML = requireField + constant.CrawlingOptions.GOOGLE_IMAGE.inputLabel;
                labelImageQuantity.hidden = inputImageQuantity.hidden = false;
                break;
        }
        inputKeyword.disabled = false;
    })

    // Handle for Facebook search (Require username)
    inputKeyword.addEventListener("keyup", () => checkValidForm())
    inputPassword.addEventListener("keyup", () => checkValidForm())
    inputTargetPage.addEventListener("keyup", () => checkValidForm())
    inputQuantity.addEventListener("keyup", () => checkValidForm())

    // Handle for Google Image search (Require keyword)
    inputImageQuantity.addEventListener("keyup", () => checkValidImageCrawl())
    inputKeyword.addEventListener("keyup", () => checkValidImageCrawl())
});