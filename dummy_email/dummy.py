import smtplib
from email.message import EmailMessage

email = 'dodot09atestsenderemail@gmail.com'
password = 'dodotestemail123'

msg = EmailMessage()
msg['Subject'] = 'Test!'
msg['From'] = email
msg['To'] = 'dodoiteration3@gmail.com'
msg.set_content("This is an email.")

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(email, password)
    smtp.send_message(msg)




