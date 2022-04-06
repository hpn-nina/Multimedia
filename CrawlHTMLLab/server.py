from flask import Flask, render_template, request, redirect, url_for
from crawler import facebook, images, news, researchPaper
from static.enums.constant import CRAWLING_OPTIONS, SELECT_VALUE
from decouple import config

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html', crawlOptions=CRAWLING_OPTIONS)

@app.route('/result', methods=['POST'])
def result():
  option = int(request.form['crawlOptions'])
  
  if option == CRAWLING_OPTIONS['FACEBOOK']['value']:
    crawl_result = facebook.crawl(request.form['keyword'], request.form['password'], request.form['target-page-input'], request.form['post-num'])
    
    js = open('./static/result.js', 'r')
    js_out = f"var crawl_result = JSON.parse('{crawl_result}');"
    
    result_value = {
      "target": request.form['target-page-input'],
      "crawlOption": SELECT_VALUE[option],
      "username": request.form['keyword'],
      "result": crawl_result,
    }
  elif option == CRAWLING_OPTIONS['RESEARCH_PAPER']['value']:
    crawl_result = researchPaper.crawler(request.form['keyword'])
    result_value = {
      "keyword": request.form['keyword'],
      "crawlOption": SELECT_VALUE[option],
      "result": crawl_result,
      "quantity": 10,
      "baseUrl": config('BASE_URL')
    }
  else:
    result_value = {
    "keyword": request.form['keyword'],
    "crawlOption": SELECT_VALUE[option],
    "quantity": 10,
    "result": {
      "json": "json",
    }
  }
  
  return render_template('result.html', result=result_value, select=SELECT_VALUE, crawlOption=SELECT_VALUE[option], isRadioSelect=False)


if __name__ == '__main__':
  app.run(debug=True)