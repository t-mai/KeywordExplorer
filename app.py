import os
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from xgoogle.keywordanalyser import KeywordAnalyser

# create our little application :)
app = Flask(__name__)

@app.route('/')
def show_entries():
    return render_template('show_entries.html')

@app.route('/', methods=['POST'])
def show_result():
    keyword = request.form['keyword']
    analyser = KeywordAnalyser(keyword);
    if keyword == '':
        return render_template('show_entries.html', error="You did not enter a keyword!")
    else:
        try:
            scrapresult = analyser.scrap_data();
            title_keywords = analyser.extract_keyword_alchemy(scrapresult.titles)
            des_keywords = analyser.extract_keyword_alchemy(scrapresult.descriptions)
            content_keywords = analyser.extract_keyword_alchemy(scrapresult.contents)
            return render_template('show_entries.html', keyword=keyword, title_keywords=title_keywords, des_keywords=des_keywords, content_keywords=content_keywords)
        except Exception, e:
            return render_template('show_entries.html', keyword=keyword, error=e)