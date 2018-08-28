# -*- coding: latin5 -*-
# Import smtplib for the actual sending function
import smtplib
import logging
import os, sys

from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.message import MIMEMessage

def sendemail(frommail, tomail, pngs,projectname,week):
    sendemail_logger = logging.getLogger('AvailabilityGraphSender.SendMail')
    COMMASPACE = ', '
    msg = MIMEMultipart()
    msg['Subject'] = week+' UAT Ortamı Kullanılabilirlik Raporu - ' + projectname
    # me == the sender's email address
    # family = the list of all recipients' email addresses
    msg['From'] = frommail
    msg['To'] = COMMASPACE.join(tomail)
    sendemail_logger.info('Sending Mail to:' + COMMASPACE.join(tomail))
    sendemail_logger.info('Sending Attachments:' +'-'.join(pngs))

    #msg['To'] = tomail
    msg.preamble = week+' UAT Ortamı Kullanılabilirlik Raporu - ' + projectname
    dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))
    rbody = open(os.path.join(dirname, "textfile.txt"), 'r')
    body = MIMEText(rbody.read().replace("ProjectName", projectname), 'html', 'latin5')
    msg.attach(body)    
    rbody.close()
    i=0
    for file in pngs:
        i+=1
        filename='image' + str(i)+'.png'
        fp = open(file, 'rb')
        img = MIMEImage(fp.read())
        img.add_header('Content-Disposition', "attachment; filename= %s" % filename)
        fp.close()
        msg.add_header('Content-ID', filename)
        msg.add_header('Content-Disposition', 'inline')
        msg.attach(img)
    msg["Content-type"] = "text/html;charset=latin5"
    # Send the email via our own SMTP server.
    s = smtplib.SMTP('xxx.xxx',25)
    s.sendmail(frommail, tomail, msg.as_string().encode('latin5'))
    sendemail_logger.info('Mail Sent to:' + tomail)
    s.quit()


