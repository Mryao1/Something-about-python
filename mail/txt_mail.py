import smtplib
from email.mime.text import MIMEText
from email.header import Header

mail_host = "smtp.qq.com"
mail_user = "250946034@qq.com"
mail_pass = "chzuexjyfbpabgha"

sender = '250946034@qq.com'
#receivers = ['1015749498@qq.com']
#receivers = ['250946034@qq.com']
receivers = ['3293789781@qq.com']

message = MIMEText('冰冰！', 'plain', 'utf-8')
message['From'] = Header("耀<250946034@qq.com>", 'utf-8')
message['To'] = Header("zbb", 'utf-8')

subject = '冰冰！！！'
message['Subject'] = Header(subject, 'utf-8')

try:
    smtpObj = smtplib.SMTP()
    smtpObj.connect(mail_host, 25)
    smtpObj.login(mail_user, mail_pass)
    smtpObj.sendmail(sender, receivers, message.as_string())
    print("邮件发送成功")
except smtplib.SMTPException:
    print("Error: 无法发送邮件")


