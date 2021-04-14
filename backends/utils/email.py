from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
import smtplib


def send_email(html, msg_from, msg_to, msg_subject, mail_host, mail_post, mail_user, mail_pass, receivers):
    """
    邮件发送功能
    SMTP_SSL模式发送
    目前不使用多条邮件发送，将sleep进行注释
    多条邮件发送存在问题，如需使用 打开sleep
    """
    message = MIMEMultipart()
    message.attach(MIMEText(html, 'html', 'utf-8'))
    message['From'] = msg_from
    message['To'] = msg_to
    message['Subject'] = Header(msg_subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP_SSL(mail_host, mail_post)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(msg_from, receivers, message.as_string())
        smtpObj.quit()

    except smtplib.SMTPException as ex:
        return False

    # time.sleep(1)
    return True


def mail_send(html, sender, msg_to, mail_content, mail_host, mail_user, mail_pass, receivers, mail_post=587):
    """
    备用邮件发送功能
    SMTP模式发送，当前不使用
    """
    # 定义邮件内容
    message = MIMEMultipart()
    message['From'] = Header(sender, 'utf-8')
    message['To'] = msg_to
    message['Subject'] = Header(mail_content, 'utf-8')
    message.attach(MIMEText(html, 'html', 'utf-8'))

    # 邮件发送
    try:
        smtpobj = smtplib.SMTP()
        smtpobj.connect(mail_host, mail_post)
        smtpobj.login(mail_user, mail_pass)
        smtpobj.sendmail(sender, receivers, message.as_string())

    except smtplib.SMTPException:
        return False

    return True
