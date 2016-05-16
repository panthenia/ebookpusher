from flask import Flask, url_for, request, render_template
from Utils import BookDownloader, BookPusher
from DataType.BookTypes import BookSummary
import json
app = Flask(__name__)
downloader = BookDownloader.BookDownloader()


@app.route('/search', methods=['GET'])
def index():
    search_word = request.args.get('q', None)
    if search_word:
        sumaris = downloader.seachBook(bookname=search_word)
        return render_template('search_result.html', sumaris=sumaris, query=search_word)
    else:
        return 'No input', 404


@app.route('/detail', methods=['GET'])
def get_book_detail():
    bookid = request.args.get('bookid', None)
    if bookid:
        sumary = BookSummary(name='', id=bookid)
        detail = downloader.getBookDetail(summary=sumary)
        return render_template('book_detail.html', detail=detail)

if __name__ == '__main__':
    app.run(debug=True)