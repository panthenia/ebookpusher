from flask import Flask, url_for, request
from Utils import BookDownloader, BookPusher
from DataType.BookTypes import BookSummary
import json
app = Flask(__name__)
downloader = BookDownloader.BookDownloader()


@app.route('/search', methods=['GET'])
def search_book():
    search_word = request.args.get('q', None)
    if search_word:
        sumaris = downloader.seachBook(bookname=search_word)
        js = json.dumps(sumaris, default=lambda o: o.__dict__, ensure_ascii=False)
        return js
    else:
        return 'No input', 404


@app.route('/detail', methods=['GET'])
def get_book_detail():
    bookid = request.args.get('bookid', None)
    if bookid:
        sumary = BookSummary(name='', id=bookid)
        book_detail = downloader.getBookDetail(summary=sumary)
        js = json.dumps(book_detail, default=lambda o:o.__dict__, ensure_ascii=False)
        return js

if __name__ == '__main__':
    app.run(debug=True)