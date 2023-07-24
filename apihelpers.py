import os
import uuid
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dbcreds import smtp_password, sender_email

def save_file(file, folder, extensions):
    if('.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in extensions):
        filename = uuid.uuid4().hex + '.' + file.filename.rsplit('.', 1)[1].lower()
        try:
            file.save(os.path.join(folder, filename))
            return filename
        except Exception as error:
            print('FILE SAVE ERROR:' , error)
def delete_file(file, folder):
        try:
            if(os.path.isfile(os.path.join(folder, file))):
                os.remove(os.path.join(folder, file))
                print("Succesfully deleted")
                return 
            print("File does not exist")
            return 
        except Exception as error:
            print('FILE SAVE ERROR:' , error)
def check_data(data_type, required_data):
    for data in required_data:
        if(data_type.get(data) == None):
            return f'The {data} parameter is missing.'
def send_email(sender, receiver, subject, body):
    try:
        message = MIMEMultipart()
        message["To"] = receiver
        message["From"] = sender
        message["Subject"] = subject
        messageText = MIMEText(body,'html')
        message.attach(messageText)
        email = sender_email
        password = smtp_password
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo('Gmail')
        server.starttls()
        server.login(email,password)
        server.sendmail(sender,receiver,message.as_string())
        print('EMAIL SENT')
    except Exception as error:
        print('EMAIL ERROR:', error)
    finally:
        if (server != None):
            server.quit()
