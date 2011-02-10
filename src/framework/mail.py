""" 
mailer code
"""
import smtplib
from smtplib import *
from src.config import info
from scratch.simple import *

class message(object):
    def __init__(self,frm,to,subject,body):
        self._from = frm
        self._to = to
        self._subject = subject
        self._body = body
    def get_subject(self):
        return self._subject
    def get_to(self):
        return self._to
    def get_body(self):
        return self._body
    def get_from(self):
        return self._from
        
    subject = property(get_subject)
    frm = property(get_from)
    to = property(get_to)
    body = property(get_body)

    
class postOffice():
    def __init__(self):
        pass
    
    def sendMail(self,message,format):
        """send message in text or/and html format = 'text' or 'html' """

        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        
        me = message.frm
        you = message.to
        
        # Create message container - the correct MIME type is multipart/alternative.
        msg = MIMEMultipart('alternative')
        msg['Subject'] = message.subject
        msg['From'] = me
        msg['To'] = you
        
        # Create the body of the message (a plain-text and an HTML version).
        text = "Hi!\n\n%s \n\nHow are you?\n\nHere is the link you wanted:\nhttp://www.python.org"
        html = """\
        <html>
        <head></head>
        <body>
          <p>Hi!<br>
             <b>%s</b>
             <br>
             Here is the <a href="http://www.python.org">link</a> you wanted.
          </p>
        </body>
        </html>
        """
        
        html = html % (message.body)
        text = text % (message.body)
        # Record the MIME types of both parts - text/plain and text/html.
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')
        
        # Attach parts into message container.
        # According to RFC 2046, the last part of a multipart message, in this case
        # the HTML message, is best and preferred.
        
        msg.attach(part1)
        if(format == 'html'):
            msg.attach(part2)
        
        # Send the message via local SMTP server.
        try:
            s = smtplib.SMTP(info.smtpServer)
            s.login(info.smtpUser, info.smtpPwd)
        # sendmail function takes 3 arguments: sender's address, recipient's address
        # and message to send - here it is sent as one string.
            res = s.sendmail(me, you, msg.as_string())
        except SMTPException:
            print "Error: unable to send email"
        s.quit()
        print res
        

        
if(__name__ == '__main__'):
    for elem in list(range(2)):
        bod = generate("S")
        sub = "subject_" + str(elem)
        print bod
        print sub
        postOffice().sendMail(message("g@agentidea.com","grantsteinfeld@gmail.com",sub,bod),'text')
