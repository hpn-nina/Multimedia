import * as constant from './enums/constant.js';

document.addEventListener("DOMContentLoaded", function(event) {
    let selectCrawlOption = document.getElementById("crawlOptions");
    let inputKeyword = document.getElementById("keyword");
    let inputUsername = document.getElementById("username")
    let inputPassword = document.getElementById("password");
    let inputTargetPage = document.getElementById("target-page-input");

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
                break;
            case constant.CrawlingOptions.NEWS.value:
                area = constant.CrawlingOptions.NEWS.area;
                document.querySelector(area).hidden = false;
                break;
            case constant.CrawlingOptions.FACEBOOK.value:
                area = constant.CrawlingOptions.FACEBOOK.area;
                document.querySelector(area).hidden = false;
                break;
            case constant.CrawlingOptions.GOOGLE_IMAGE.value:
                area = constant.CrawlingOptions.GOOGLE_IMAGE.area;
                document.querySelector(area).hidden = false;
                break;
        }
        inputKeyword.disabled = false;
        for (let i of areaList) {
            if (i !== area)
                document.querySelector(i).hidden = true; //Make all area not used go into hidden
        }
    })

    const checkValidForm = () => {
        if (selectCrawlOption.value !== constant.CrawlingOptions.FACEBOOK.value) {
            // Check keyword have been enter or not
            if (inputKeyword.value.length != 0)
                document.querySelector('#submitBtn').disabled = false
            else
                document.querySelector('#submitBtn').disabled = true;
        } else {
            checkValidFacebookForm()
        }
    }

    const checkValidFacebookForm = () => {
        if (document.querySelector('.facebook-area').hidden !== true) {
            let condition = inputKeyword && inputUsername && inputPassword && inputTargetPage;
            if (condition)
                document.querySelector('#submitBtn').disabled = true;
            else
                document.querySelector('#submitBtn').disabled = false;
        }
    }

    // Handle for Facebook search (Require username)
    inputKeyword.addEventListener("keyup", () => checkValidForm());
    inputUsername.addEventListener("keyup", () => checkValidFacebookForm());
    inputPassword.addEventListener("keyup", () => checkValidFacebookForm());
    inputTargetPage.addEventListener("keyup", () => checkValidFacebookForm());
});