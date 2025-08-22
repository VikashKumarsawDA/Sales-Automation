import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# replace with your email and App password
email_id = "jaimaataragarnmentsbandarkuppi@gmail.com"    #also in codeline in main.py 366
app_pass = "bbym lpuz vmkw fsav"                         #also in codeline in main.py 367

def send_openacn_akn(uemail, uname, UserID, upass):
    
    subject = "Account Created Successfully - Jai Maa Tara Garments"
    body = f"""
    Dear {uname},
    Welcome to JAI MAA TARA GARMENTS your trusted fashion family!
    your account has been created with Jai Maa Tara Garments. Enjoy ✨Exclusive Offer and quality products
    Start shopping with us today!

    ✅ Your Account Details:
    User ID: {UserID}
    Password: {upass}
    Kindly change your password when you log in for the first time.

    Thanks,  
    Jai Maa Tara Garments 
    Dumri Road Bandarkuppi Chowk, Giridih (JH) 
    for any information kindly contact us our shop owner thankyou.
    Mr.Akash Saw 6205072278 , Mr.Prakash Saw 6204343957
    Ashok Saw (9693630197)
    """

    # Build email
    msg = MIMEMultipart()
    msg["From"] = email_id
    msg["To"] = uemail
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email_id, app_pass)
        server.sendmail(email_id, uemail, msg.as_string())
        server.quit()
        print("✅ Email sent successfully!")
    except Exception as e:
        print("❌ Error while sending email:", e)