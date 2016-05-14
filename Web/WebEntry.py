from flask import Flask, url_for, request
from Utils import BookDownloader, BookPusher
import json
app = Flask(__name__)
downloader = BookDownloader.BookDownloader()


@app.route('/search', methods=['GET'])
def index():
    search_word = request.args.get('q', None)
    if search_word:
        sumaris = downloader.seachBook(bookname=search_word)
        js = json.dumps(sumaris, default=lambda o: o.__dict__, ensure_ascii=False)
        return js
    else:
        return 'No input', 404


if __name__ == '__main__':
    app.run(debug=True)