from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
import smtplib

from backends.settings import env


def send_email(email_title, email_content, address_list, receivers):
    """
    邮件发送功能
    SMTP_SSL模式发送
    目前不使用多条邮件发送，将sleep进行注释
    多条邮件发送存在问题，如需使用 打开sleep
    """
    mail_host = env('MAIL_HOST')
    mail_user = env('MAIL_USER')
    mail_pass = env('MAIL_PASS')
    mail_port = env('MAIL_POST')

    message = MIMEMultipart()
    message.attach(MIMEText(email_content, 'html', 'utf-8'))
    message['From'] = mail_user
    message['To'] = address_list
    message['Subject'] = Header(email_title, 'utf-8')

    try:
        smtpObj = smtplib.SMTP_SSL(mail_host, mail_port)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(mail_user, receivers, message.as_string())
        smtpObj.quit()

    except smtplib.SMTPException as ex:
        return False

    return True


# def mail_send(html, sender, msg_to, mail_content, mail_host, mail_user, mail_pass, receivers, mail_post=587):
#     """
#     备用邮件发送功能
#     SMTP模式发送，当前不使用
#     """
#     # 定义邮件内容
#     message = MIMEMultipart()
#     message['From'] = Header(sender, 'utf-8')
#     message['To'] = msg_to
#     message['Subject'] = Header(mail_content, 'utf-8')
#     message.attach(MIMEText(html, 'html', 'utf-8'))
#
#     # 邮件发送
#     try:
#         smtpobj = smtplib.SMTP()
#         smtpobj.connect(mail_host, mail_post)
#         smtpobj.login(mail_user, mail_pass)
#         smtpobj.sendmail(sender, receivers, message.as_string())
#
#     except smtplib.SMTPException:
#         return False
#
#     return True
