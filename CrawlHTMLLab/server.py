from flask import Flask, render_template, request, redirect, url_for
from crawler import facebook, images, news, researchPaper

app = Flask(__name__)

select_value = {
  1: "ResearchPaper",
  2: "News",
  3: "Facebook",
  4: "Google Image"
}

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
  chose_option = int(request.form['crawlOptions'])
  result_value = {
    "keyword": request.form['keyword'],
    "crawlOption": select_value[chose_option],
    "result": {
      "json": "json",
    }
  }
  return render_template('result.html', result=result_value)


if __name__ == '__main__':
  app.run(debug=True)