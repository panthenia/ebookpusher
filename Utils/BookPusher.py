import smtplib
from email import encoders
from email.mime.multipart import MIMEBase,MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
from Utils.DataBaseHelper import DbHelper
import os


class BookPusher(object):
    def __init__(self):
        dbhelper = DbHelper()
        self.act, self.psw = dbhelper.getPushEmailAccount()

    def push_book(self, path):
        mail = MIMEMultipart()
        mail['Subject'] = Header('书籍推送', 'utf-8').encode()
        mail['To'] = formataddr(('2309623743', '2309623743@qq.com'), 'utf-8')
        mail['From'] = formataddr(('pusher', self.act), 'utf-8')
        mail.attach(MIMEText('book pusher', 'plain', 'utf-8'))
        attachment = self.prepare_attachment(path)
        mail.attach(attachment)

        server = smtplib.SMTP('smtp.sina.com', 25)
        server.set_debuglevel(1)
        server.login(self.act, self.psw)
        server.sendmail(self.act, ['2309623743@qq.com'], mail.as_string())
        server.quit()

    def prepare_attachment(self, path):
        filename = os.path.split(path)[1]
        bookname = filename.split('.')[0]
        booktype = filename.split('.')[1]
        with open(path, 'rb') as f:
            # 设置附件的MIME和文件名，这里是png类型:
            mime = MIMEBase(bookname, booktype, filename=filename)
            # 加上必要的头信息:
            mime.add_header('Content-Disposition', 'attachment', filename=filename)
            mime.add_header('Content-ID', '<0>')
            mime.add_header('X-Attachment-Id', '0')
            # 把附件的内容读进来:
            mime.set_payload(f.read())
            # 用Base64编码:
            encoders.encode_base64(mime)
            # 添加到MIMEMultipart:
            return mime





