""" 
mailer code
"""
import smtplib
from copy import deepcopy

from smtplib import *
from src.config import info
from scratch.simple import *
from src.framework.error import SendMailException
from src.framework.core import Utils

#from functional import *

message = {
           'subject':None,
           'body64':None,
           'html64':None,
           'from':None,
           'replyto':None,
           'to':[],
           'cc':[]
           }

messageToJSON = lambda  message: json.dumps(message)

def newMessage(msgFrom,replyto,to,subject,cc=None,body=None,html=None):
    """ new email message from/to/subject required """
    
    msg = deepcopy(message)
    msg['from'] = msgFrom
    msg['to'] = to
    msg['subject'] = subject
    
    if(cc): msg['cc'] = cc
    if(replyto): msg['replyTo'] = replyto
    if(body): msg['body64'] = body.encode('base64','strict')
    if(html): msg['html64'] = html.encode('base64','strict')
    
    return msg

    
def sendMail(message):
    """send message in text or/and html format = 'text' or 'html' """

    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    toList = ','.join(message['to'])
    
    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = message['subject']
    msg['From'] = message['from']
    msg['To'] = toList
    
    if(message['cc']): msg['Cc'] = ','.join(message['cc'])
    
    if(message['body64'] != None):
        text = message['body64'].decode('base64','strict')
        msg.attach(MIMEText(text, 'plain'))
    
    if(message['html64'] != None):
        html = message['html64'].decode('base64','strict')
        msg.attach(MIMEText(html, 'html'))
    
    # Send the message via local SMTP server.
    smtpClient = None
    
    try:
        smtpClient = smtplib.SMTP(info.smtpServer)
        smtpClient.login(info.smtpUser, info.smtpPwd)
        #sendmail function takes 3 arguments: sender's address, recipient's address 
        #and message to send - here it is sent as one string. """

        res = smtpClient.sendmail(message['from'], toList, msg.as_string())
        
        if(len(res.keys())>0):
            raise SendMailException("sendmail exception was %s" % ( Utils().ConvertDictToString(res)) )
        
        print " message sent"
    except SMTPException:
        print "Error: unable to send email"
        
    if smtpClient:
        smtpClient.quit()

        
if(__name__ == '__main__'):
    
    emails = []
    
    '''create list of emails to send'''
    for elem in list(range(3)):
        bod = generate()
        sub = "Subject example " + str(elem)
        emails.append( newMessage("grantsteinfeld@gmail.com","grantsteinfeld@gmail.com",["grantsteinfeld@gmail.com"],sub,None,bod) )
    
    
    '''send mail by way of map() '''
    #map(sendMail,emails)   
    
    import json
    
    for mail in emails:
        print mail['subject']
        print messageToJSON(mail)
    
    

        
        
        
        
        
        
        
