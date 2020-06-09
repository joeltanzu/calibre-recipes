import smtplib
import getpass
import os
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
# Print email sending list
print("Sending files to", to)
subject = 'kindlebook'
mail_content = 'Sending kindle books'

# List files in the current folder
files = os.listdir()
print("List of files currently in folder:")
# Print out files in current folder
for i in range(len(files)):
    print(f"{i}. {files[i]}")
filenum = input("Select the file number you wish to upload: ")

# Check if valid integer added
try:
    filenum = int(filenum)
except ValueError:
    print("Please insert a valid integer")
    input("Press any key to quit")
    exit
finally:
    filenum = int(filenum)

# Check if file number given is valid
if filenum > (len(files)-1) or filenum < 0:
    print("Please give a valid selection")
    input("Press any key to quit")
    exit
else:
    filename = files[filenum]

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

# Display status before quitting
input("Press any key to quit")