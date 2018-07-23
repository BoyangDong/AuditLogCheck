import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import ntpath
from . import env


class Mail:
    def __init__(self, subject):
        self.server = smtplib.SMTP(env.get('EMAIL_SERVER'))
        self.server.starttls()
        self.email = env.get('EMAIL')
        self.pw = env.get('PASSWORD')
        self.msg = MIMEMultipart()
        self.msg['From'] = "QH/Victory Jobrunner"
        self.msg['Subject'] = subject

    def send(self, msg, to=[]):
        self.msg.attach(MIMEText(msg))
        self.msg['To'] = ', '.join(to)
        self.server.login(self.email, self.pw)
        self.server.sendmail(self.email, to, self.msg.as_string())
        self.server.quit()

    def attach(self, file_name):
        ''' attach a file '''
        if os.path.isfile(file_name):
            attachment = open(file_name, 'rb')
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition',
                            'attachment; filename=%s' %
                            (ntpath.basename(file_name)))
            self.msg.attach(part)
        else:
            print('cannot read attachment')

    def attach_content_as_file(self, content, name):
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(content)
        encoders.encode_base64(part)
        part.add_header('Content-Disposition',
                        'attachment; filename=%s' % (name))
        self.msg.attach(part)
