import smtplib
from email.mime.text import MIMEText
from email.header import Header

sender = 'xuchang@icsoc.net'
receiver = 'wangye@icsoc.net'
smtpserver = 'smtp.163.com'
username = 'xuchang'
password = 'pytest-html'

# 邮件主题
mail_title = '主题:测试报告3'

# 读取HTML文件的内容
# f = open('report_test.html', 'rb')
mail_body = "hello"  # f.read()
# f.close()

# 邮件内容格式
message = MIMEText(mail_body, 'html', 'utf-8')
message['From'] = sender
message['To'] = receiver
message['Subject'] = Header(mail_title, 'utf-8')

try:
    smtp = smtplib.SMTP()
    smtp.connect(smtpserver)
    smtp.login(username, password)
    smtp.sendmail(sender, receiver, message.as_string())
    print("发送邮件成功")
    smtp.quit()
except smtplib.SMTPException:
    print("邮件发送失败")
    raise
