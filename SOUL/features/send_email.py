import smtplib

def mail(sender_email, sender_password, receiver_email, msg):
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as mail:
            mail.ehlo()
            mail.starttls()
            mail.login(sender_email, sender_password)
            mail.sendmail(sender_email, receiver_email, msg)
        return True
    except Exception as e:
        print(f"Email sending failed: {e}")
        return False
