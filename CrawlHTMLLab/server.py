from flask import Flask, render_template, request, redirect, url_for
from crawler import facebook, images, news, researchPaper
from static.enums.constant import CRAWLING_OPTIONS, SELECT_VALUE
from decouple import config
import mimetypes

app = Flask(__name__)
mimetypes.add_type('application/javascript', '.js')

@app.route('/')
def index():
  return render_template('index.html', crawlOptions=CRAWLING_OPTIONS)

@app.route('/result', methods=['POST'])
def result():
  option = int(request.form['crawlOptions'])
  
  if option == CRAWLING_OPTIONS['FACEBOOK']['value']:
    quantity = (10 if request.form['quantity-facebook'] == '' else int(request.form['quantity-facebook']))
    crawl_result = facebook.crawl(request.form['keyword'], request.form['username'], request.form['password'], request.form['target-page-input'], quantity)
    print(crawl_result)
    result_value = {
      "target": request.form['target-page-input'],
      "crawlOption": SELECT_VALUE[option],
      "username": request.form['username'],
      "keyword": request.form['keyword'],
      "result": crawl_result,
      "quantity": quantity
    }
  
  elif option == CRAWLING_OPTIONS['RESEARCH_PAPER']['value']:
    quantity = (10 if request.form['quantity-research-paper'] == '' else int(request.form['quantity-research-paper']))
    author = (False if request.form['author'] == 'False' else True)
    crawl_result = researchPaper.crawler(request.form['keyword'], author ,quantity)
    
    result_value = {
      "keyword": request.form['keyword'],
      "crawlOption": SELECT_VALUE[option],
      "result": crawl_result,
      "baseUrl": config('IEEE_BASE_URL'),
      "quantity": quantity
    }
    
  elif option == CRAWLING_OPTIONS['GOOGLE_IMAGE']['value']:
    quantity = (10 if request.form['quantity-google-image'] == '' else int(request.form['quantity-google-image']))
    crawl_result = images.crawler(request.form['keyword'], quantity)
    result_value = {
      "keyword": request.form['keyword'],
      "crawlOption": SELECT_VALUE[option],
      "result": crawl_result,
      "quantity": quantity
    }
  else:
    # Section for news
    quantity = (10 if request.form['quantity-news'] == '' else int(request.form['quantity-news']))
    crawl_result = news.crawler(request.form['keyword'], quantity)
    result_value = {
    "keyword": request.form['keyword'],
    "crawlOption": SELECT_VALUE[option],
    "quantity": quantity,
    "result": crawl_result
  }
  
  return render_template('result.html', result=result_value, 
                         select=SELECT_VALUE,
                         crawlOption=SELECT_VALUE[option], 
                         crawlOptions=CRAWLING_OPTIONS,
                         isRadioSelect=False)


if __name__ == '__main__':
  app.run(debug=True)