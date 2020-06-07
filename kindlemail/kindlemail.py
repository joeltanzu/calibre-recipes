import smtplib
import getpass
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

"""
---INSERT LOGIN DETAILS HERE---
"""
# Log in details
port = 465 # Port set to 465 for SSL usage
user = 'youremail@gmail.com' # Insert your email here
# Getpass utilised to mask password input. Note that Gmail might require you to insert an app password in lieu of gmail password.
password = getpass.getpass(prompt='Password: ', stream=None) # Insert your password here. 

"""
---INSERT EMAIL DETAILS HERE---
"""
# Email details
sent_from = user
to = 'yourkindleemail@kindle.com' # Put in your kindle email here
subject = 'kindlebook'
mail_content = 'Sending kindle books'
# Filename must be in same directory as script
filename = 'kindlefilename.mobi' # Put your kindle filename you want to upload here

"""
---TOUCH ANYTHING BELOW HERE AT YOUR OWN RISK---
"""
# MIME settings
message = MIMEMultipart()
message['From'] = user
message['To'] = to
message['Subject'] = subject

# Attachment details
message.attach(MIMEText(mail_content, 'plain'))
# Open the file via binary mode
attachment = open(filename, 'rb')
payload = MIMEBase('application', 'octet-stream')
payload.set_payload(attachment.read())
# Encode the attachment
encoders.encode_base64(payload) 
# Add payload header with filename
payload.add_header('Content-Disposition', 'attachment', filename=filename)
# Add attachment to message and convert to string
message.attach(payload)
text = message.as_string()

# Email sending details
try:
    # SSL required instead of just SMTP for secured connection
    server = smtplib.SMTP_SSL('smtp.gmail.com', port)
    server.ehlo()
    server.login(user, password)

    server.sendmail(sent_from, to, text)
    server.close()
    print('Email sent successfully')
except:
    print('Unable to establish connection')