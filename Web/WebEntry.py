import sys, os
print(sys.path)
sys.path.append(os.path.split(sys.path[0])[0])
from flask import Flask, url_for, request, render_template
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


@app.route('/detail', methods=['GET'])
def get_book_detail():
    bookid = request.args.get('bookid', None)

    if bookid:
        sumary = BookSummary(name='', id=bookid)
        detail = downloader.getBookDetail(summary=sumary)
        return render_template('book_detail.html', detail=detail)


@app.route('/')
def search_index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)