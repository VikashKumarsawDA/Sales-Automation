# ======================= IMPORTS =======================
from tkinter import Tk, Label, Frame, Entry, Button, messagebox, StringVar, BooleanVar,scrolledtext
from tkinter.ttk import Combobox
from tkinter import *
from PIL import Image, ImageTk ,ImageDraw
import time
import sqlite3, random
import random
from captchavalue import generatecaptcha, generatepass
from tablecreation import generate
from emailtest import send_openacn_akn
from otpf_pas import send_otp
from chat_table_creation import create_chat_table
from datetime import datetime
import smtplib
from email.message import EmailMessage
from tkinter import ttk
import re


create_chat_table()  # calling chat table
# ======================= DATABASE SETUP =======================
generate()  # Create database tables if not exists

# ======================= ROOT WINDOW =======================
root = Tk()
root.state('zoomed')
root.configure(bg='pink')
root.title("JMTG")
# Change logo
#icon = PhotoImage(file="images/krsna.png")
#root.iconphoto(True, icon)

# ======================= TITLE & LOGO =======================
title = Label(root, text="JMTG SALES AUTOMATION", font=('Arial', 50, 'bold'), bg='pink')
title.pack()

img = Image.open("images/sales.png").resize((150, 132)).convert("RGBA")

# Create rounded mask
mask = Image.new("L", img.size, 0)
draw = ImageDraw.Draw(mask)
draw.rounded_rectangle((0, 0, img.size[0], img.size[1]), radius=00, fill=265)  # radius=30 for roundness

# Apply mask
rounded_img = Image.new("RGBA", img.size)
rounded_img.paste(img, (0, 0), mask=mask)

# Convert to Tkinter image
imgtk = ImageTk.PhotoImage(rounded_img, master=root)

# Display logo
logo_lbl = Label(root, image=imgtk, bg="pink")
logo_lbl.place(relx=0, rely=0)

# ======================= DATE & TIME =======================
def show_dt():
    dt = time.strftime("%A %d-%b-%Y %r")
    dt_lbl.configure(text=dt)
    dt_lbl.after(1000, show_dt)  # Update every 1 second

dt_lbl = Label(root, font=('Arial', 15), bg='pink')
dt_lbl.pack()
show_dt()

# ======================= FOOTER =======================
footer_lbl = Label(root, font=('Arial', 15, 'bold'), bg='pink',
                   text="© 2025 Jai Maa Tara Garments Data Management System. All Rights Reserved \n Developed by Vikash Kumar Saw")
footer_lbl.pack(side='bottom')

# ------------------- CALLING CAPTCHA GLOBALLY FOR USING NEW CAPTCHA-------------------
codecaptcha = generatecaptcha()
# ======================= MAIN SCREEN =======================
def main_screen():
    # ------------------- FRAME -------------------
    frm = Frame(root, highlightbackground='brown', highlightthickness=2, bg='powder blue')
    frm.place(relx=0, rely=0.17, relwidth=1, relheight=0.76)



    def refereshcaptcha():
        global codecaptcha
        codecaptcha = generatecaptcha()
        captcha_value_lbl.configure(text=codecaptcha)

    # ------------------- LOGIN FUNCTION -------------------
    def login():
        utype = usertype_cb.get()
        uid = userid_e.get()
        upas = userpas_e.get()

        ucaptcha = captcha_e.get()
        global codecaptcha
        codecaptcha = codecaptcha.replace(" ","")

        if utype == "Admin🤴":
            if uid=="jmtgadmin" and upas=="adminakash":
                if  codecaptcha == ucaptcha:
                    frm.destroy()
                    admin_screen()
                else:
                    messagebox.showerror("Login","Invalid Captcha ")
            else:
                messagebox.showerror("Login ❌","Wrong Admin/Password Please try after sometime Thankyou.")
        else:
            if  codecaptcha == ucaptcha:
                conobj = sqlite3.connect('sales.sqlite')
                curobj = conobj.cursor()
                query = 'SELECT * FROM users WHERE UserID=? AND UserPassword=?'
                curobj.execute(query, (uid, upas))
                row = curobj.fetchone()
                if row is None:
                    messagebox.showerror("Login", "Invalid ID/PassWord")
                else:
                    frm.destroy()
                    user_screen(row[0],row[1])  # row[1] is username
            else:
                messagebox.showerror("Login","Invalid Captcha ")
    # ------------------- FORGOT PASSWORD -------------------
    def forgot():
        frm.destroy()
        fp_screen()

    # ------------------- WIDGETS -------------------
    # User Type
    usertype_lbl = Label(frm, text='User Type ', font=('Arial', 20), bg='powder blue')
    usertype_lbl.place(relx=0.3, rely=0.15)
    usertype_cb = Combobox(frm, values=['User👨‍💼', 'Admin🤴'], font=('Arial', 20, 'bold'))
    usertype_cb.current(0)
    usertype_cb.place(relx=0.42, rely=0.15)

    # UserID
    userid_lbl = Label(frm, text='User ID👤  ', font=('Arial', 20, 'bold'), bg='powder blue')
    userid_lbl.place(relx=0.3, rely=0.25)
    userid_e = Entry(frm, font=('Arial', 20, 'bold'), bd=5)
    userid_e.place(relx=0.42, rely=0.25)
    userid_e.focus()

    # Password
    userpas_lbl = Label(frm, text='Password🔑', font=('Arial', 20, 'bold'), bg='powder blue')
    userpas_lbl.place(relx=0.3, rely=0.35)
    userpas_e = Entry(frm, font=('Arial', 20, 'bold'), bd=5, show='*')
    userpas_e.place(relx=0.42, rely=0.35)

    # Captcha
    #captcha_lbl = Label(frm, text='Captcha', font=('Arial', 20, 'bold'), bg='powder blue')
    #captcha_lbl.place(relx=0.3, rely=0.45)

    #Generate Captcha
    captcha_value_lbl = Label(frm, text=codecaptcha, fg='green', font=('Arial', 20, 'bold'), width=8)
    captcha_value_lbl.place(relx=0.3, rely=0.46)

    captcha_e = Entry(frm, font=('Arial', 20, 'bold'), bd=5,width=10)
    captcha_e.place(relx=0.42, rely=0.45)

    # Buttons
    referesh_btn = Button(frm, text='Refresh🔄', bd=5, command=refereshcaptcha, font=('Arial', 15), width=10)
    referesh_btn.place(relx=0.54, rely=0.45)

    Login_btn = Button(frm, text='Login', command=login, bd=5, font=('Arial', 15), bg="#49E454", width=10)
    Login_btn.place(relx=0.42, rely=0.55)

    forgot_btn = Button(frm, text='Forgot Password', command=forgot, bd=5, font=('Arial', 15), bg='#FF6666', width=14)
    forgot_btn.place(relx=0.51, rely=0.55)


# ======================= FORGOT PASSWORD SCREEN =======================

def fp_screen():
    frm = Frame(root, highlightbackground='brown', highlightthickness=2, bg="#EC9696")
    frm.place(relx=0, rely=0.17, relwidth=1, relheight=0.76)

    otp_var = StringVar()

    def home():
        frm.destroy()
        main_screen()

    def forget_pass():
        uemail = email_e.get()
        uid = userid_e.get()

        conobj = sqlite3.connect('sales.sqlite')
        curobj = conobj.cursor()
        query = 'SELECT * FROM users WHERE UserID=?'
        curobj.execute(query, (uid,))
        row = curobj.fetchone()
        conobj.close()

        if row is None:
            messagebox.showerror("Forgot Password", "User ID does not exist")
        else:
            if uemail == row[2]:
                otp = random.randint(1000, 9999)
                otp_var.set(str(otp))

                if send_otp(uemail, otp):  # call external function
                    messagebox.showinfo("OTP Sent", f"OTP sent to {uemail}")
                else:
                    messagebox.showwarning("Email Error", f"Could not send OTP, check console.")

                # Show OTP entry
                otp_lbl = Label(frm, text="Enter OTP", font=('Arial', 20, 'bold'), bg="#EC9696")
                otp_lbl.place(relx=0.30, rely=.35)

                otp_e = Entry(frm, font=('Arial', 20, 'bold'), bd=5)
                otp_e.place(relx=0.42, rely=.35)

                def verify_otp():
                    if otp_e.get() == otp_var.get():
                        messagebox.showinfo("OTP Verified", "OTP matched! You can reset your password.")

                        # ---- Reset password fields ----
                        newpass_lbl = Label(frm, text="New Pass", font=('Arial', 20, 'bold'), bg="#EC9696")
                        newpass_lbl.place(relx=0.30, rely=.45)

                        newpass_e = Entry(frm, font=('Arial', 20, 'bold'), bd=5, show="*")
                        newpass_e.place(relx=0.42, rely=.45)

                        confpass_lbl = Label(frm, text="Confirm Pass", font=('Arial', 20, 'bold'), bg="#EC9696")
                        confpass_lbl.place(relx=0.30, rely=.55)

                        confpass_e = Entry(frm, font=('Arial', 20, 'bold'), bd=5, show="*")
                        confpass_e.place(relx=0.42, rely=.55)

                        def update_password():
                            np = newpass_e.get().strip()
                            cp = confpass_e.get().strip()

                            if np == "" or cp == "":
                                messagebox.showerror("Error", "Password fields cannot be empty")
                                return
                            if np != cp:
                                messagebox.showerror("Error", "Passwords do not match")
                                return

                            conobj = sqlite3.connect('sales.sqlite')
                            curobj = conobj.cursor()
                            curobj.execute("UPDATE users SET UserPassword=? WHERE UserID=?", (np, uid))
                            conobj.commit()
                            conobj.close()
                            messagebox.showinfo("Success", "Password updated successfully ✅")
                            frm.destroy()
                            main_screen()

                        update_btn = Button(frm, text="Update Password", command=update_password,
                                            bd=5, font=('Arial', 15), bg="#9DF4A3")
                        update_btn.place(relx=0.47, rely=.7)

                    else:
                        messagebox.showerror("Invalid OTP", "OTP does not match.")

                verify_btn = Button(frm, text='Verify OTP', command=verify_otp,
                                    bd=5, font=('Arial', 12), bg="#FFD580")
                verify_btn.place(relx=0.65, rely=.36)

            else:
                messagebox.showerror("Forgot Password", "Email does not match with User ID.")

    # UI
    Home_btn = Button(frm, text='Home🏠', command=home, bd=5, bg="#A3BDF6", font=('Arial', 15))
    Home_btn.place(relx=0.01, rely=0.02)

    userid_lbl = Label(frm, text='User ID 👤  ', font=('Arial', 20, 'bold'), bg="#EC9696")
    userid_lbl.place(relx=0.3, rely=.15)

    userid_e = Entry(frm, font=('Arial', 20, 'bold'), bd=5)
    userid_e.place(relx=0.42, rely=.15)

    email_lbl = Label(frm, text='Email ID✉️ ', font=('Arial', 20, 'bold'), bg="#EC9696")
    email_lbl.place(relx=0.3, rely=.25)
    email_e = Entry(frm, font=('Arial', 20, 'bold'), bd=5)
    email_e.place(relx=0.42, rely=.25)

    Check_btn = Button(frm, text='Check', command=forget_pass, bd=5, font=('Arial', 12), bg="#FFB094")
    Check_btn.place(relx=0.65, rely=.26)

# ---------- Admin screen ----------
def admin_screen():
    frm = Frame(root, highlightbackground='brown', highlightthickness=2, bg="#F3FFB5")
    frm.place(relx=0, rely=0.17, relwidth=1, relheight=0.76)

    # ---------- Logout ----------
    def logout():
        frm.destroy()
        main_screen()  # make sure main_screen() is defined

    Logout_btn = Button(frm, text='Logout🔚', command=logout, bd=5, bg="#E64C4C", font=('Arial', 12))
    Logout_btn.place(relx=0, rely=0.01)

    # ---------- Email Chat Box ----------
    def Emailbtn():
        frm2 = Toplevel(root)
        frm2.title("Admin Email Chat")
        frm2.geometry("500x400")
        frm2.config(bg="#ECECEC")

        Label(frm2, text="Admin Chat Box", font=('Arial', 14, 'bold'), bg="#ECECEC").pack(pady=5)

        chat_area = scrolledtext.ScrolledText(frm2, width=58, height=15, state='disabled', font=('Arial', 10))
        chat_area.pack(pady=5)

        msg_entry = Entry(frm2, width=40, font=('Arial', 12))
        msg_entry.pack(side=LEFT, padx=5, pady=10)

        # Load previous messages
        con = sqlite3.connect('sales.sqlite')
        cur = con.cursor()
        cur.execute("SELECT timestamp, sender, message FROM admin_chat ORDER BY id")
        rows = cur.fetchall()
        con.close()

        chat_area.config(state='normal')
        for timestamp, sender, message in rows:
            color = "blue" if sender == "Admin" else "green" if sender == "System" else "red"
            chat_area.insert(END, f"[{timestamp}] {sender}: {message}\n", sender)
            chat_area.tag_config(sender, foreground=color)
        chat_area.config(state='disabled')
        chat_area.yview(END)

        # ---------- Send message ----------
        def send_msg():
            msg_text = msg_entry.get().strip()
            if msg_text:
                timestamp = datetime.now().strftime("%H:%M:%S")

                # Display admin message
                chat_area.config(state='normal')
                chat_area.insert(END, f"[{timestamp}] Admin: {msg_text}\n", "Admin")
                chat_area.tag_config("Admin", foreground="blue")
                chat_area.config(state='disabled')
                chat_area.yview(END)
                msg_entry.delete(0, END)

                # Save message to DB
                con = sqlite3.connect('sales.sqlite')
                cur = con.cursor()
                cur.execute("INSERT INTO admin_chat (timestamp, sender, message) VALUES (?, ?, ?)",
                            (timestamp, "Admin", msg_text))
                con.commit()
                con.close()

                # Send email to all users
                try:
                    con = sqlite3.connect('sales.sqlite')
                    cur = con.cursor()
                    cur.execute("SELECT UserEmail FROM users")
                    emails = cur.fetchall()
                    con.close()

                    sender_email = "jaimaataragarnmentsbandarkuppi@gmail.com"
                    sender_pass = "bbym lpuz vmkw fsav"

                    for email in emails:
                        receiver_email = email[0]
                        msg = EmailMessage()
                        msg.set_content(msg_text)
                        msg['Subject'] = "Notification from Admin"
                        msg['From'] = sender_email
                        msg['To'] = receiver_email

                        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                            server.login(sender_email, sender_pass)
                            server.send_message(msg)

                    # System confirmation
                    chat_area.config(state='normal')
                    chat_area.insert(END, f"[{timestamp}] System: Message sent to all users ✅\n", "System")
                    chat_area.tag_config("System", foreground="green")
                    chat_area.config(state='disabled')
                    chat_area.yview(END)

                    # Save system message
                    con = sqlite3.connect('sales.sqlite')
                    cur = con.cursor()
                    cur.execute("INSERT INTO admin_chat (timestamp, sender, message) VALUES (?, ?, ?)",
                                (timestamp, "System", "Message sent to all users ✅"))
                    con.commit()
                    con.close()

                except Exception as e:
                    chat_area.config(state='normal')
                    chat_area.insert(END, f"[{timestamp}] System: Error - {str(e)}\n", "System")
                    chat_area.tag_config("System", foreground="red")
                    chat_area.config(state='disabled')
                    chat_area.yview(END)

            else:
                messagebox.showwarning("Empty Message", "Please type a message before sending.")

        send_btn = Button(frm2, text="Send 📩", command=send_msg, bg="#8686F0", fg="white", font=('Arial', 12))
        send_btn.pack(side=RIGHT, padx=5, pady=10)




    # ------------------- CREATE NEW USER -------------------


    def newuser():
        frm2 = Frame(root, highlightbackground='brown', highlightthickness=2, bg="#FFC98F")
        frm2.place(relx=0.3, rely=0.2, relwidth=0.5, relheight=0.6)

        Label(frm2, text='New User Account Creation', font=('Arial', 20, 'bold'), bg="#FFC98F", fg='purple').pack(pady=10)

        username_lbl = Label(frm2,text='User Name',font=('Arial',20,'bold'),bg='#FFC98F')
        username_lbl.place(relx=0.10,rely=0.2)
        username_e = Entry(frm2, font=('Arial', 15), bd=5)
        username_e.place(relx=0.35, rely=0.2)

        useremail_lbl = Label(frm2,text='Email ID',font=('Arial',20,'bold'),bg='#FFC98F')
        useremail_lbl.place(relx=0.10,rely=0.30)
        useremail_e = Entry(frm2, font=('Arial', 15), bd=5)
        useremail_e.place(relx=0.35, rely=0.3)

        usermob_lbl = Label(frm2,text='Mobile No.',font=('Arial',20,'bold'),bg='#FFC98F')
        usermob_lbl.place(relx=0.10,rely=0.4)
        usermob_e = Entry(frm2, font=('Arial', 15), bd=5)
        usermob_e.place(relx=0.35, rely=0.4)

        useradd_lbl = Label(frm2,text='Address',font=('Arial',20,'bold'),bg='#FFC98F')
        useradd_lbl.place(relx=0.10,rely=0.5)
        useradd_e = Entry(frm2, font=('Arial', 15), bd=5)
        useradd_e.place(relx=0.35, rely=0.5)

        # Create account
        def createacn():
            uname = username_e.get().strip()
            uemail = useremail_e.get().strip()
            umob = usermob_e.get().strip()
            uadd = useradd_e.get().strip()

            # --- Validation ---
            # 1. Name: Only letters & spaces, not empty
            if not uname or not re.match(r'^[A-Za-z\s]+$', uname):
                messagebox.showerror("Invalid Input", "❌ Please enter a valid Name (letters only).")
                return

            # 2. Email: Must match standard pattern
            if not uemail or not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', uemail):
                messagebox.showerror("Invalid Input", "❌ Please enter a valid Email ID.")
                return

            # --- Check duplicate email in DB ---
            conobj = sqlite3.connect('sales.sqlite', timeout=10)
            curobj = conobj.cursor()
            curobj.execute("SELECT 1 FROM users WHERE UserEmail = ?", (uemail,))
            if curobj.fetchone():
                messagebox.showerror("Duplicate Email", "❌ This Email ID is already registered. Please use another.")
                conobj.close()
                return

            # 3. Mobile: Indian format (10 digits, starts with 6-9)
            if not re.match(r'^[6-9]\d{9}$', umob):
                messagebox.showerror("Invalid Input", "❌ Please enter a valid Indian Mobile Number (10 digits, starts with 6-9).")
                conobj.close()
                return

            # 4. Address: Not empty
            if not uadd:
                messagebox.showerror("Invalid Input", "❌ Address cannot be empty.")
                conobj.close()
                return

            # --- If all validations pass ---
            upass = generatepass()
            upurchase = 0
            uopendt = time.strftime("%A %d-%b-%Y")

            try:
                curobj.execute('INSERT INTO users VALUES (NULL,?,?,?,?,?,?,?)',
                                (uname, uemail, umob, uadd, upass, upurchase, uopendt))
                curobj.execute("SELECT max(UserID) FROM users")
                UserID = curobj.fetchone()[0]
                conobj.commit()
                conobj.close()
                send_openacn_akn(uemail, uname, UserID, upass)
                messagebox.showinfo("Account Created", f"✅ Account for {uname} created!\nUserID: {UserID}\nPassword: {upass}")
                frm2.destroy()
                admin_screen()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create account: {e}")
                conobj.close()


        Submit_btn = Button(frm2, text='Submit', command=createacn, bg="#9DF4A3", bd=5, font=('Arial', 15), width=10)
        Submit_btn.place(relx=0.4, rely=0.7)


    # ------------------- VIEW USERS -------------------
    def viewusers():
        frm2 = Frame(root, highlightbackground='brown', highlightthickness=2, bg="#A6FFAE")
        frm2.place(relx=0.3, rely=0.2, relwidth=0.5, relheight=0.6)

        Label(frm2, text=' Details View ', font=('Arial', 20, 'bold'),
            fg='purple', bg="#A6FFAE").pack(pady=10)

        # ----- Create a Frame inside frm2 for Treeview + Scrollbar -----
        table_frame = Frame(frm2, bg="#A6FFAE")
        table_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # ----- Treeview Style -----
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"))  # Bold headings
        style.configure("Treeview", font=("Arial", 11))  # Normal rows

        # ----- Treeview Table (without password) -----
        cols = ("User ID", "User Name", "User Email", "User Mob.", "User Address",
                "User Purchase", "User Open Date")
        tree = ttk.Treeview(table_frame, columns=cols, show="headings")

        # Add only vertical Scrollbar
        vsb = Scrollbar(table_frame, orient=VERTICAL, command=tree.yview)
        tree.configure(yscroll=vsb.set)

        vsb.pack(side=RIGHT, fill=Y)
        tree.pack(side=LEFT, fill=BOTH, expand=True)

        # Define headings
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor=CENTER)

        # ----- Fetch Data from Database -----
        conobj = sqlite3.connect("sales.sqlite")
        curobj = conobj.cursor()
        curobj.execute("SELECT UserID, UserName, UserEmail, UserMob, UserAddress, UserPurchase, UserOpenDate FROM users")
        rows = curobj.fetchall()
        conobj.close()

        # Insert data row by row
        for row in rows:
            tree.insert("", END, values=row)

    # ------------------- DELETE USER -------------------

    def deluser():
        frm2 = Frame(root, highlightbackground='brown', highlightthickness=2, bg="#FFA7A7")
        frm2.place(relx=0.3, rely=0.2, relwidth=0.5, relheight=0.6)

        Label(frm2, text='Delete User Account', font=('Arial', 20, 'bold'),fg='purple', bg="#FFA7A7").pack(pady=20)

        userdel_lbl = Label(frm2, text='User ID ', font=('Arial', 20, 'bold'), bg='#FFA7A7')
        userdel_lbl.place(relx=0.20, rely=0.2)

        userdel_e = Entry(frm2, font=('Arial', 15), bd=5, width=10)
        userdel_e.place(relx=0.35, rely=0.2)

        # Label to display details
        details_lbl = Label(frm2, text="", font=('Arial', 12),
                            bg="#FFA7A7", justify="left", anchor="w")
        details_lbl.place(relx=0.1, rely=0.35)

        # --- Functions ---
        def delete_user(uid):
            con = sqlite3.connect("sales.sqlite")
            cur = con.cursor()
            cur.execute("DELETE FROM users WHERE UserID=?", (uid,))
            con.commit()
            con.close()
            details_lbl.config(text="")  # clear details
            userdel_e.delete(0, END)  # clear entry box
            messagebox.showinfo("Account Deleted",
                                f"Account with User ID {uid} has been deleted successfully!")

        def fetch_details():
            uid = userdel_e.get().strip()
            if uid == "":
                messagebox.showwarning("Input Error", "Please enter User ID")
                return

            con = sqlite3.connect("sales.sqlite")
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE UserID=?", (uid,))
            row = cur.fetchone()
            con.close()

            if row:
                details_lbl.config(
                    text=f"Name      : {row[1]}\nEmail     : {row[2]}\nMobile    : {row[3]}\nAddress   : {row[4]}\nPurchase  : {row[6]}\nJoin Date : {row[7]}"
                )
                # show delete button
                delete_btn = Button(frm2, text="Delete User", bg="red", fg="white", bd=3,
                                    font=('Arial', 12, 'bold'),
                                    command=lambda: delete_user(uid))
                delete_btn.place(relx=0.4, rely=0.85)
            else:
                details_lbl.config(text="No user found with this ID")

        # Fetch button (now defined AFTER function)
        fetch_btn = Button(frm2, text="Fetch Details", bg="#FFD966", bd=3,font=('Arial', 12), command=fetch_details)
        fetch_btn.place(relx=0.55, rely=0.2)

    mail_btn = Button(frm, text='Send 📩', command=Emailbtn, bd=5, bg="#3553CB", font=('Arial', 12))
    mail_btn.place(relx=0.065, rely=0.01)






    # ------------------- ADD USER AMOUNT-------------------

    def addamount():
        frm2 = Frame(root, highlightbackground='brown', highlightthickness=2, bg="#9191FA")
        frm2.place(relx=0.3, rely=0.2, relwidth=0.5, relheight=0.6)

        Label(frm2, text='Add Purchasing Amount', font=('Arial', 20, 'bold'), bg="#9191FA", fg='purple').pack(pady=10)

        # Variables to hold user details
        name_var = StringVar()
        balance_var = StringVar()
        userid_valid = BooleanVar(value=False)   # ✅ track if ID is valid

        # --- Function to fetch name when ID is entered ---
        def fetch_name():
            userid = userid_e.get().strip()
            if not userid:
                messagebox.showerror("Error", "Please enter a User ID")
                return

            conobj = sqlite3.connect('sales.sqlite')
            curobj = conobj.cursor()
            curobj.execute("SELECT UserName, UserPurchase FROM users WHERE UserID=?", (userid,))
            row = curobj.fetchone()
            conobj.close()

            if row:
                uname, upurchase = row
                name_var.set(f"Name: {uname}")
                balance_var.set(f"Current Purchase: ₹{upurchase}")
                userid_valid.set(True)   # ✅ mark as valid
            else:
                name_var.set("❌ User not found")
                balance_var.set("")
                userid_valid.set(False)  # ❌ invalid user

        # --- Function to add amount ---
        def add_amt():
            if not userid_valid.get():
                messagebox.showerror("Error", "Please fetch a valid User ID first")
                return

            try:
                uamt = float(addamt_e.get()) 
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid amount")
                return

            userid = userid_e.get().strip()

            conobj = sqlite3.connect('sales.sqlite')
            curobj = conobj.cursor()
            curobj.execute("SELECT UserPurchase FROM users WHERE UserID=?", (userid,))
            row = curobj.fetchone()

            if row:
                current_amt = row[0] if row[0] else 0
                new_amt = current_amt + uamt
                curobj.execute("UPDATE users SET UserPurchase=? WHERE UserID=?", (new_amt, userid))
                conobj.commit()
                conobj.close()

                messagebox.showinfo("Success", f"₹{uamt} added successfully!\nTotal Amount = ₹{new_amt}")
                frm2.destroy()
                admin_screen()

            else:
                conobj.close()
                messagebox.showerror("Error", f"User ID {userid} not found in records!")

        # --- UI Components ---
        userid_lbl = Label(frm2, text='User ID ', font=('Arial', 20, 'bold'), bg='#9191FA')
        userid_lbl.place(relx=0.10, rely=0.2)

        userid_e = Entry(frm2, font=('Arial', 15), bd=5)
        userid_e.place(relx=0.35, rely=0.2)

        fetch_btn = Button(frm2, text="Fetch Details", command=fetch_name, bg="#FFD966", bd=3, font=('Arial', 12))
        fetch_btn.place(relx=0.75, rely=0.2)

        name_lbl = Label(frm2, textvariable=name_var, font=('Arial', 15, 'bold'), bg="#9191FA", fg="black")
        name_lbl.place(relx=0.35, rely=0.3)

        balance_lbl = Label(frm2, textvariable=balance_var, font=('Arial', 15), bg="#9191FA", fg="green")
        balance_lbl.place(relx=0.35, rely=0.4)

        useramt_lbl = Label(frm2, text='Add Amount', font=('Arial', 20, 'bold'), bg='#9191FA')
        useramt_lbl.place(relx=0.10, rely=0.5)

        addamt_e = Entry(frm2, font=('Arial', 15), bd=5)
        addamt_e.place(relx=0.35, rely=0.5)

        addamt_btn = Button(frm2, text='Add Amount', command=add_amt, bg="#7EBEFF", bd=5, font=('Arial', 15))
        addamt_btn.place(relx=0.4, rely=0.7)



    # ------------------- ADMIN BUTTONS -------------------
    canc_btn=Button(frm, text='Create Account', command=newuser, bg="#FFC98F", bd=5, font=('Arial', 15), width=15)
    canc_btn.place(relx=0.0, rely=0.2)

    vanc_btn=Button(frm, text='View Account', command=viewusers, bd=5, bg="#A6FFAE", font=('Arial', 15), width=15)
    vanc_btn.place(relx=0.0, rely=0.4)

    danc_btn=Button(frm, text='Delete User', command=deluser, bd=5, bg="#FFA7A7", font=('Arial', 15), width=15)
    danc_btn.place(relx=0.0, rely=0.6)

    addamount_btn=Button(frm, text='Add Amount', command=addamount, bd=5, bg="#9191FA", font=('Arial', 15), width=15)
    addamount_btn.place(relx=0.0, rely=0.8)

# ======================= USER SCREEN =======================
def user_screen(uid,uname):
    frm = Frame(root, highlightbackground='brown', highlightthickness=2, bg="#C6D1FF")
    frm.place(relx=0, rely=0.17, relwidth=1, relheight=0.76)


    conobj = sqlite3.connect('sales.sqlite')
    curobj = conobj.cursor()
    query = 'SELECT * FROM users WHERE UserID=?'
    curobj.execute(query, (uid,))
    row = curobj.fetchone()
    conobj.close()


    def logout():
        frm.destroy()
        main_screen()


    def chkdetails():
        frm = Frame(root, highlightbackground='brown', highlightthickness=2, bg="#F6FDB2")
        frm.place(relx=0.3, rely=0.30, relwidth=0.5, relheight=0.5)

        uid_lbl = Label(frm, text=f"User ID\t\t{row[0]}", font=('Arial', 15,'bold'), bg="#F6FDB2")
        uid_lbl.place(relx=0.2, rely=0.1)

        uname_lbl = Label(frm, text=f"Name\t\t{row[1]}", font=('Arial', 15,'bold'), bg="#F6FDB2")
        uname_lbl.place(relx=0.2, rely=0.2)

        umob_lbl = Label(frm, text=f"Mobile\t\t{row[3]}", font=('Arial', 15,'bold'), bg="#F6FDB2")
        umob_lbl.place(relx=0.2, rely=0.3)

        uemail_lbl = Label(frm, text=f"Email\t\t{row[2]}", font=('Arial', 15,'bold'), bg="#F6FDB2")
        uemail_lbl.place(relx=0.2, rely=0.4)

        uadd_lbl = Label(frm, text=f"Address\t\t{row[4]}", font=('Arial', 15,'bold'), bg="#F6FDB2")
        uadd_lbl.place(relx=0.2, rely=0.5)

        udate_lbl = Label(frm, text=f"Joined On\t{row[7]}", font=('Arial', 15,'bold'), bg="#F6FDB2")
        udate_lbl.place(relx=0.2, rely=0.6)

        close_btn = Button(frm, text='Close', command=frm.destroy, bd=5, bg="#FF7777", font=('Arial', 15))
        close_btn.place(relx=0.47, rely=0.80)

    def updatedetails():
        frm = Frame(root, highlightbackground='brown', highlightthickness=2, bg="#FFA7A7")
        frm.place(relx=0.3, rely=0.30, relwidth=0.5, relheight=0.5)

        def update_details():
            uname = updatename_e.get()
            uemail = updateemail_e.get()
            umob = updateMob_e.get()
            upass = updatepas_e.get()
            uadd = updateadd_e.get()

            conobj = sqlite3.connect('sales.sqlite')
            curobj = conobj.cursor()

            query = 'update users set UserName = ?,UserEmail = ?,UserMob = ?,UserPassword=?,UserAddress = ? where UserID = ?'
            curobj.execute(query, (uname,uemail,umob,upass,uadd,uid))
            conobj.commit()
            conobj.close()
            messagebox.showinfo("Update","Details Updated 😊")
            frm.destroy()
            user_screen(uid,None)


        updatename_lbl = Label(frm, text="Name ", font=('Arial', 15), bg="#FFA7A7")
        updatename_lbl.place(relx=0.2, rely=0.1)

        updatename_e = Entry(frm, font=('Arial', 15), bd=5)
        updatename_e.place(relx=0.35, rely=0.1)
        updatename_e.insert(0,row[1])


        updateemail_lbl = Label(frm, text="Email ", font=('Arial', 15), bg="#FFA7A7")
        updateemail_lbl.place(relx=0.2, rely=0.25)

        updateemail_e = Entry(frm, font=('Arial', 15), bd=5)
        updateemail_e.place(relx=0.35, rely=0.25)
        updateemail_e.insert(0,row[2])

        updateMob_lbl = Label(frm, text="Mobile No ", font=('Arial', 15), bg="#FFA7A7")
        updateMob_lbl.place(relx=0.2, rely=0.4)

        updateMob_e = Entry(frm, font=('Arial', 15), bd=5)
        updateMob_e.place(relx=0.35, rely=0.4)
        updateMob_e.insert(0,row[3])

        updatepas_lbl = Label(frm, text="Password ", font=('Arial', 15), bg="#FFA7A7")
        updatepas_lbl.place(relx=0.2, rely=0.55)

        updatepas_e = Entry(frm, font=('Arial', 15), bd=5)
        updatepas_e.place(relx=0.35, rely=0.55)
        updatepas_e.insert(0,row[5])


        updateadd_lbl = Label(frm, text="Address  ", font=('Arial', 15), bg="#FFA7A7")
        updateadd_lbl.place(relx=0.2, rely=0.7)

        updateadd_e = Entry(frm, font=('Arial', 15), bd=5)
        updateadd_e.place(relx=0.35, rely=0.7)
        updateadd_e.insert(0,row[4])

        update_btn = Button(frm, text='Update', command=update_details, bd=5, bg="#6C7AF5", font=('Arial', 15))
        update_btn.place(relx=0.47, rely=0.83)


    def purchasedetails():
        frm = Frame(root, highlightbackground='brown', highlightthickness=2, bg="#A6FFAE")
        frm.place(relx=0.3, rely=0.30, relwidth=0.5, relheight=0.5)

        def close():
            frm.destroy()
            user_screen()


        conobj = sqlite3.connect('sales.sqlite')
        curobj = conobj.cursor()
        query = 'SELECT UserPurchase FROM users WHERE UserID=?'
        curobj.execute(query, (uid,))
        row = curobj.fetchone()
        conobj.close()
        if row:
            purchase_amount = row[0]  # extract purchase value
        else:
            purchase_amount = 0

        purchase_lbl = Label(frm, text=f"Your total purchasing from JMT Garnments\nAmount: ₹ {purchase_amount}", font=('Arial', 15,'bold'), bg="#A6FFAE")
        purchase_lbl.place(relx=0.2, rely=0.4)

        Close_btn = Button(frm, text='Close', command=close, bd=5, bg="#FF8F8F", font=('Arial', 15))
        Close_btn.place(relx=0.45, rely=0.80)

    Logout_btn = Button(frm, text='Logout🔚', command=logout, bd=5, bg="#FFABE0", font=('Arial', 15))
    Logout_btn.place(relx=0.01, rely=0.01)

    dispalyname_lbl = Label(frm, text=f'Welcome ,{row[1]}', font=('Arial', 20, 'bold'), bg='#C6D1FF', fg='purple')
    dispalyname_lbl.place(relx=0.1, rely=0.02)


    details_btn=Button(frm, text='Details',command=chkdetails, bd=5, bg="#F6FDB2", font=('Arial', 15), width=15)
    details_btn.place(relx=0.0, rely=0.25)

    update_btn=Button(frm, text='UpdateDetail',command=updatedetails, bd=5, bg="#FFA7A7", font=('Arial', 15), width=15)
    update_btn.place(relx=0.0, rely=0.45)

    purchase_btn=Button(frm, text='Total Purchase',command=purchasedetails, bd=5, bg="#A6FFAE", font=('Arial', 15), width=15)
    purchase_btn.place(relx=0.0, rely=0.65)






# ======================= START APPLICATION =======================
main_screen()
root.mainloop()
