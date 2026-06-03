from libs import umail
import utime
import network
import time
from libs.wifi import init_wifi
from libs.secrets import *

# Email details
sender_email = secrets["sender_email"]
sender_name = secrets["sender_name"]
sender_app_password = secrets["sender_app_password"]
recipient_email = secrets["recipient_email"]
email_subject = 'Alert'

def send_security_email(
        event,
        distance,
        light):

    # Send the email
    smtp = umail.SMTP('smtp.gmail.com', 465, ssl=True)  # Gmail's SSL port

    try:
        smtp.login(sender_email, sender_app_password)
        smtp.to(recipient_email)
        smtp.write("Subject:Raspberry Pi Security Alert\n")
        smtp.write("Security Alert!\n\n")
        smtp.write("Mode: Security Mode\n")
        smtp.write(f"Event: {event}\n")
        smtp.write(f"Distance: {distance:.1f} cm\n")
        smtp.write(f"Light Value: {light}\n")
        smtp.write(f"Time: {utime.localtime()}\n")
        smtp.send()
        print("Email Sent Successfully")

    except Exception as e:
        print("Failed to send email:", e)
    finally:
        smtp.quit()


