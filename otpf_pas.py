import smtplib

def send_otp(receiver, otp):
    """
    Sends OTP to given receiver email.
    If email fails, OTP will be printed in console.
    """
    try:
        sender = "jaimaataragarnmentsbandarkuppi@gmail.com"        # <-- replace with your Gmail
        app_pass = "bbym lpuz vmkw fsav"                           # <-- replace with your app password

        subject = "Password Reset OTP"
        body = f"Your OTP for password reset is: {otp}"
        msg = f"Subject: {subject}\n\n{body}\nDo not share your OTP with anyone\nThis OTP is valid to Update Your Password only.\n\n\n\n\nJMT Garnments\nThankyou."

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, app_pass)
        server.sendmail(sender, receiver, msg)
        server.quit()

        return True  # success
    except Exception as e:
        print(f"DEBUG OTP for {receiver}: {otp}")  # fallback for testing
        print("Email error:", e)
        return False
