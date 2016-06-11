import sys, os

sys.path.append(os.path.split(sys.path[0])[0])
from flask import Flask, url_for, request, render_template, redirect, session
from Utils import BookDownloader, BookPusher
from DataType.BookTypes import BookSummary
import json


app = Flask(__name__)
downloader = BookDownloader.BookDownloader()
pusher = BookPusher.BookPusher()


@app.route('/search', methods=['GET'])
def index():
    search_word = request.args.get('q', None)
    page = request.args.get('page', 1)
    if search_word:
        sumaris, total_page = downloader.seachBook(bookname=search_word, page=page)
        return render_template('search_result.html', sumaris=sumaris, query=search_word, page=page, total_page=total_page)
    else:
        return 'No input', 404

@app.route('/push', methods=['POST'])
def push_book():
    book_url = request.form['url']
    file_location = downloader.downloadBook(booklink=book_url)
    pusher.push_book(file_location)
    return 'suucess'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method =='POST':
        user = request.form['act']
        psw = request.form['psd']
        if True:
            session['account'] = user
            app.logger.debug('%s,%s' % (user, psw,))
            return redirect('/')
        else:
            return

@app.route('/logout', methods=['GET'])
def logout():
    if 'account' in session:
        session.pop('account', None)

@app.route('/detail', methods=['GET'])
def get_book_detail():
    if 'account' in session:
        bookid = request.args.get('bookid', None)

        if bookid:
            sumary = BookSummary(name='', id=bookid)
            detail = downloader.getBookDetail(summary=sumary)
            return render_template('book_detail.html', detail=detail)
    else:
        return redirect('/login')

@app.route('/')
def search_index():
    if 'account' in session:
        return render_template('index.html')
    else:
        return redirect('/login')
app.secret_key = os.urandom(24)

if __name__ == '__main__':
    app.run(port=8888, debug=True)