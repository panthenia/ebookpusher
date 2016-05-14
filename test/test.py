from Utils import BookDownloader

dl = BookDownloader.BookDownloader()
book_summaries = dl.seachBook('活着')
asummary = book_summaries[0]
print(asummary)
detail = dl.getBookDetail(asummary)
dlink = detail.downInfo[0][0]
print(dlink)
dl.downloadBook(booklink=dlink)
