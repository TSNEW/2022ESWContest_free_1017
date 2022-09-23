import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.encoders import encode_base64
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate

def send_mail(e_mail):
    msg = MIMEMultipart()
    msg['From'] = 'qkrxotn369@naver.com'
    msg['To'] = e_mail
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = Header(s="간이문진표", charset='utf-8')

    body = MIMEText('작성하신 문진표와 측정치 결과입니다.\n본인이 아니라면 삭제해주시기 바랍니다.', _charset='utf-8')

    msg.attach(body)

    files = list()
    files.append('./save_data.csv')

    for f in files:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(open(f, 'rb').read())
        encode_base64(part)
        part.add_header('Content-Disposition',
                        'attachment; filename="%s"' % os.path.basename(f))
        msg.attach(part)

    server = smtplib.SMTP_SSL('smtp.naver.com')
    server.login('qkrxotn369@naver.com', 'pts333')
    server.send_message(msg)
    server.quit()
    print('Clear')