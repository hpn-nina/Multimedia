import * as constant from './enums/constant.js';

document.addEventListener("DOMContentLoaded", function(event) {
    let selectCrawlOption = document.getElementById("crawlOptions");
    let inputKeyword = document.getElementById("keyword");
    let inputPassword = document.getElementById("password");
    let inputTargetPage = document.getElementById("target-page-input");
    let inputQuantity = document.getElementById("quantity-facebook");
    let inputImageQuantity = document.getElementById("quantity");

    selectCrawlOption.addEventListener("change", (val) => {
        inputKeyword.disabled = false;
        let area = ''
        let areaList = []
        for (let i in constant.CrawlingOptions) {
            areaList.push(constant.CrawlingOptions[i].area)
        }
        switch (Number(selectCrawlOption.value)) {
            case constant.CrawlingOptions.RESEARCH_PAPER.value:
                area = constant.CrawlingOptions.RESEARCH_PAPER.area;
                document.querySelector(area).hidden = false;
                inputKeyword.placeholder = constant.CrawlingOptions.RESEARCH_PAPER.placeholder;
                break;
            case constant.CrawlingOptions.NEWS.value:
                area = constant.CrawlingOptions.NEWS.area;
                document.querySelector(area).hidden = false;
                inputKeyword.placeholder = constant.CrawlingOptions.NEWS.placeholder;
                break;
            case constant.CrawlingOptions.FACEBOOK.value:
                area = constant.CrawlingOptions.FACEBOOK.area;
                document.querySelector(area).hidden = false;
                inputKeyword.placeholder = constant.CrawlingOptions.FACEBOOK.placeholder;
                break;
            case constant.CrawlingOptions.GOOGLE_IMAGE.value:
                area = constant.CrawlingOptions.GOOGLE_IMAGE.area;
                document.querySelector(area).hidden = false;
                inputKeyword.placeholder = constant.CrawlingOptions.GOOGLE_IMAGE.placeholder;
                break;
        }
        inputKeyword.disabled = false;
        for (let i of areaList) {
            if (i !== area)
                document.querySelector(i).hidden = true; //Make all area not used go into hidden
        }
    })

    const checkValidForm = () => {
        let condition = inputKeyword.value.length > 0 && inputPassword.value.length > 0 && inputTargetPage.value.length > 0 && inputQuantity.value.length > 0;
        if (condition || inputPassword.hidden && inputKeyword.value.length > 0) {
            document.getElementById("submitBtn").disabled = false;
        } else
            document.getElementById("submitBtn").disabled = true;
    }

    const checkValidImageCrawl = () => {
        let condition = inputKeyword.value.length > 0 && inputImageQuantity.value.length > 0;
        if (condition)
            document.getElementById("submitBtn").disabled = false;
        else
            document.getElementById("submitBtn").disabled = true;
    }

    // Handle for Facebook search (Require username)
    inputKeyword.addEventListener("keyup", () => checkValidForm());
    inputPassword.addEventListener("keyup", () => checkValidForm());
    inputTargetPage.addEventListener("keyup", () => checkValidForm());
    inputQuantity.addEventListener("keyup", () => checkValidForm());

    // Handle for Google Image search (Require keyword)
    //inputImageQuantity.addEventListener("keyup", () => checkValidImageCrawl());
});