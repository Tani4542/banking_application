from tkinter import *
from tkinter.ttk import Combobox
from datetime import datetime, timedelta
from PIL import Image, ImageTk
from tkinter import filedialog
import re
from tkcalendar import DateEntry
from tkinter import messagebox
import gmail
import random
import sqlite3
import time
from tkinter.ttk import Combobox,Treeview,Style,Scrollbar
import io
from PIL import Image, ImageTk
import webbrowser

try:
    conobj = sqlite3.connect(database="banking.sqlite")
    curobj = conobj.cursor()

    curobj.execute("""CREATE TABLE user_details (
        "user_id" integer PRIMARY KEY AUTOINCREMENT,
        "account_no" int,
        "first_name" text,
        "last_name" text,
        "dob" text,
        "gender" text,
        "father_name" text,
        "mother_name" text,
        "mobile_no" text,
        "email" text,
        "aadhar_no" text,
        "account_type" text,
        "nominee_name" text,
        "nominee_relation" text,
        "address_1" text,
        "address_2" text,
        "pin_code" text,
        "city" text,
        "state" text,
        "country" text,
        "password" text,
        "user_image" BLOB,
        "account_create_date_time" text,
        "balance" float DEFAULT 0
    )""")

    curobj.execute("""CREATE TABLE txns (
        "txns_id" INTEGER PRIMARY KEY AUTOINCREMENT,
        "user_id" INTEGER NOT NULL,
        "txn_amt" FLOAT NOT NULL,
        "txn_type" TEXT NOT NULL,
        "txn_update_bal" FLOAT NOT NULL,
        "txn_date" TEXT NOT NULL
    )""")
    
    curobj.execute(""" CREATE TABLE help(
        "help_id" INTEGER PRIMARY KEY AUTOINCREMENT,
        "user_id" INTEGER NOT NULL,
        "help_sub" text NOT NULL,
        "help_desc" text NOT NULL,
        "help_date" text NOT NULL
    )""")

    print("Tables created")
    conobj.commit()
    
except sqlite3.Error as e:
    print("SQLite error:", e)
finally:
    conobj.close()



def countdown(label, remaining_time_var):
    remaining_time = remaining_time_var.get()
    if remaining_time <= 0:
        label.config(text="00:00")
        return

    minutes = remaining_time // 60
    seconds = remaining_time % 60
    label.config(text=f"{minutes:02d}:{seconds:02d}")
    remaining_time -= 1
    remaining_time_var.set(remaining_time)

    label.after(1000, countdown, label, remaining_time_var)
def mask_account_number(account_number):
    account_number_str = str(account_number)
    last_four_digits = account_number_str[-4:]
    masked_number = '*' * (len(account_number_str) - 4) + last_four_digits
    return masked_number
def resend_otp(label, remaining_time_var):
    remaining_time_var.set(total_seconds)
    countdown(label, remaining_time_var)
    x = random.randint(100000, 999999)
    con = gmail.GMail("chaudharyshivam702@gmail.com", "")
    print(x)
    otp_gen = gmail.Message(to="chaudharyshivam702@gmail.com", subject="OTP", text=f"Your OTP is: {x}")
    con.send(otp_gen)
def generate_and_send_otp(user_email,f_name,l_name):
    otp = random.randint(100000, 999999)
    con = gmail.GMail("chaudharyshivam702@gmail.com", "")
    otp_gen = gmail.Message(to=f"{user_email}", subject="One Time Password (OTP) for Account Create process on Bank", text=f"Dear{f_name}{l_name},\n\nYour One Time Password (OTP) for Forgot Password recovery on BANK is {otp}.\n\nPlease note, this OTP is valid only for mentioned transaction and cannot be used for any other transaction.\nPlease do not share this One Time Password with anyone.\n\n\nWarm Regards,\nCustomer Care\nBank.")
    con.send(otp_gen)
    return otp

def verify_otp(otp_to_verify, correct_otp):
    return otp_to_verify == correct_otp
win=Tk()
win.state("zoomed")
win.configure(bg="powder blue")
win.resizable(width=False,height=False)
title=Label(win,text="Banking Desktop Application",font=('arial',60,'bold','underline'),bg='powder blue')
title.pack()
footer=Label(win,text=f'Copyright 2024 \u00A9; Designed By Tanish Chaudhary',font=('arial',13,'bold','underline'),bg='powder blue')
footer.place(relx=0.35,rely=0.95)



def callback(url):
   webbrowser.open_new_tab(url)

ins_img=PhotoImage(file='instagram.png').subsample(7,7)
label_img = Label(win, image=ins_img,border=0)
label_img.image = ins_img
label_img.bind("<Button-1>", lambda e:
callback("https://www.instagram.com/tanish.chaudhary702/"))
label_img.place(relx=.45,rely=.91)

lin_img=PhotoImage(file='linkedin.png').subsample(6,6)
label_img = Label(win, image=lin_img,border=0)
label_img.image = lin_img
label_img.bind("<Button-1>", lambda e:
callback("https://www.linkedin.com/learning/"))
label_img.place(relx=.47,rely=.91)

total_seconds = 2 * 60

def home_screen():
    frm=Frame(win)
    frm.configure(bg="white")
    frm.place(relx=.1,rely=.2,relwidth=.8,relheight=.7)
    
    def open_click():
        frm.destroy()
        openaccount_screen()
    def recover_click():
        frm.destroy()
        recoverpass_screen()
        
    def login_click():
        user_account=acn_entry.get()
        user_password=pass_entry.get()
        if len(user_account)==0 and len(user_password)==0:
            Frame(frm,width=362,height=2,bg='black').place(relx=.45,rely=.26)
            acc_error=Label(frm,text="Empty fields are not allowed.",fg='red',bg='white',font=('arial',11,'bold'))
            acc_error.place(relx=.45,rely=.27)
            Frame(frm,width=362,height=2,bg='black').place(relx=.45,rely=.36)
            pass_error=Label(frm,text="Empty fields are not allowed.",fg='red',bg='white',font=('arial',11,'bold'))
            pass_error.place(relx=.45,rely=.37)
        elif len(user_account)==0:
            Frame(frm,width=362,height=2,bg='black').place(relx=.45,rely=.26)
            acc_error=Label(frm,text="Empty fields are not allowed.",fg='red',bg='white',font=('arial',11,'bold'))
            acc_error.place(relx=.45,rely=.27)
        elif len(user_password)==0:
            Frame(frm,width=362,height=2,bg='black').place(relx=.45,rely=.36)
            pass_error=Label(frm,text="Empty fields are not allowed.",fg='red',bg='white',font=('arial',11,'bold'))
            pass_error.place(relx=.45,rely=.37)
        else:
            con=sqlite3.connect(database="banking.sqlite")
            curobj=con.cursor()
            curobj.execute("select * from user_details where account_no=? and password=?",(user_account,user_password))
            tup=curobj.fetchone()
            conobj.close()
            if tup==None:
                Frame(frm,width=362,height=2,bg='black').place(relx=.45,rely=.26)
                acc_error=Label(frm,text="Invalid Account Number.",fg='red',bg='white',font=('arial',11,'bold'))
                acc_error.place(relx=.45,rely=.27)
                Frame(frm,width=362,height=2,bg='black').place(relx=.45,rely=.36)
                pass_error=Label(frm,text="Invalid Password.",fg='red',bg='white',font=('arial',11,'bold'))
                pass_error.place(relx=.45,rely=.37)
            else:
                global user_id,user_first_name,user_last_name
                user_id=tup[0]
                user_first_name=tup[2]
                user_last_name=tup[3]
                frm.destroy()
                welcome_screen()    
        
    img=PhotoImage(file='login.png')
    label_img = Label(frm, image=img, bg="white")
    label_img.image = img
    label_img.place(relx=.1,rely=.1)
    
    heading=Label(frm,text='Sign in', fg='#052c65',bg='white',font=('arial',23,'bold','underline'))
    heading.place(relx=.57,rely=.1)
      
        
    def on_enter(e):
        acn_entry.delete(0,'end')
    def on_leave(e):
        name=acn_entry.get()
        if name=='':
            acn_entry.insert(0,'Account Number')
    acn_entry=Entry(frm,font=('arial',11),bg='white',width=45,fg='black',border=0)
    # acn_lbl.focus()
    acn_entry.insert(0,'Account Number')
    acn_entry.bind('<FocusIn>',on_enter)
    acn_entry.bind('<FocusOut>',on_leave)
    acn_entry.place(relx=.45,rely=.22)
    
    Frame(frm,width=362,height=2,bg='black').place(relx=.45,rely=.26)
    def acn_clear():
        acn_entry.delete(0,"end")
    img=PhotoImage(file='images-removebg-preview.png')
    img = img.subsample(9, 9)
    btn_pro_img = Button(frm, image=img, bg="white", border=0,command=acn_clear)
    btn_pro_img.image = img
    btn_pro_img.place(relx=0.78, rely=0.2)
    
    
    def on_enter(e):
        pass_entry.delete(0,'end')
    def on_leave(e):
        name=pass_entry.get()
        if name=='':
            pass_entry.insert(0,'Password') 
    

    pass_entry=Entry(frm,font=('arial',11),bg='white',width=45,fg='black',border=0)
    pass_entry.insert(0,'Password')
    pass_entry.bind('<FocusIn>',on_enter)
    pass_entry.bind('<FocusOut>',on_leave)
    pass_entry.place(relx=.45,rely=.32)
    
    Frame(frm,width=362,height=2,bg='black').place(relx=.45,rely=.36)
    def pass_clear():
        pass_entry.delete(0,"end")
    def toggle_password_visibility():
        global password_visible
        if 'password_visible' not in globals():
            password_visible = False
        if password_visible:
            pass_entry.config(show='*')
            password_visible = False
            btn_pro_img.config(image=show_img)
        else:
            pass_entry.config(show='')
            password_visible = True
            btn_pro_img.config(image=hide_img)
        
    password_visible = False
    show_img = PhotoImage(file='show_img.png').subsample(7, 7)
    hide_img = PhotoImage(file='hide.png').subsample(11, 11)

    btn_pro_img = Button(frm, image=show_img, bg="white", border=0, command=toggle_password_visibility)
    btn_pro_img.image = show_img
    btn_pro_img.place(relx=0.78, rely=0.29)

    btn_recpass=Button(frm,font=('arial',9,'bold','underline'),text="Forgot Password",bg='white',cursor='hand2',fg='#0d6efd',width=15,border=0,command=recover_click)
    btn_recpass.place(relx=.7,rely=.42)
    
    btn_login=Button(frm,font=('arial',20,'bold'),text="Login",bg='#0d6efd',fg='white',width=21,pady=7,border=1,cursor="hand2",command=login_click)
    btn_login.place(relx=.45,rely=.5)
    
    lable=Label(frm,text="Don't have an account?",fg='black',bg='white',font=('arial',11,'bold'))
    lable.place(relx=.5,rely=.69)
    
    btn_new=Button(frm,font=('arial',9,'bold','underline'),text="Create account",bg='white',cursor='hand2',fg='#0d6efd',width=15,border=0,command=open_click)
    btn_new.place(relx=.67,rely=.69)
def openaccount_screen():
    frm=Frame(win) 
    frm.configure(bg="white")
    frm.place(relx=.1,rely=.2,relwidth=.8,relheight=.7)
    
    def home_click():
        frm.destroy()
        home_screen()
    def openaccount_next_click(f_name,l_name,dob,gender,father_name,mother_name,mob_num,adh_num,email,acn_type,nominee_name,nominee_relation):
        fname=f_name_entry.get()
        lname=l_name_entry.get()
        dob=dob_entry.get()
        fathername=father_name_entry.get()
        mothername=mother_name_entry.get()
        mob=mob_entry.get()
        adh=adh_num_entry.get()
        email=email_entry.get()
        nomineename=nominee_name_entry.get()
        nomineerelation=nominee_relation_entry.get()
        
        # openaccount_next_screen()   
        
        if len(fname)==0 and len(lname)==0 and len(dob)==0 and len(fathername)==0 and len(mothername)== 0 and len(adh)==0 and len(email)==0 and len(nomineename)==0 and len(nomineerelation)==0:
            
            Frame(frm,width=220,height=1,bg='red').place(relx=.19,rely=.16)
            error_first_name = Label(frm, font=('arial', 8, 'bold'), bg='white', fg='red', border=0, text="Empty fields are not allowed.")
            error_first_name.place(relx=.19,rely=.17)
            
            Frame(frm,width=220,height=1,bg='red').place(relx=.7,rely=.16)
            error_last_name = Label(frm, font=('arial', 8, 'bold'), bg='white', fg='red', border=0, text="Empty fields are not allowed.")
            error_last_name.place(relx=.7,rely=.17)
            
            Frame(frm,width=220,height=1,bg='red').place(relx=.19,rely=.26)
            error_dob = Label(frm, font=('arial', 8, 'bold'), bg='white', fg='red', border=0, text="Empty fields are not allowed.")
            error_dob.place(relx=.19,rely=.27)
            
            Frame(frm,width=220,height=1,bg='red').place(relx=.19,rely=.36)
            error_father = Label(frm, font=('arial', 8, 'bold'), bg='white', fg='red', border=0, text="Empty fields are not allowed.")
            error_father.place(relx=.19,rely=.37)
            
            Frame(frm,width=220,height=1,bg='red').place(relx=.7,rely=.36)
            error_mother = Label(frm, font=('arial', 8, 'bold'), bg='white', fg='red', border=0, text="Empty fields are not allowed.")
            error_mother.place(relx=.7,rely=.37)
            
            Frame(frm,width=220,height=1,bg='red').place(relx=.19,rely=.46)
            error_mob = Label(frm, font=('arial', 8, 'bold'), bg='white', fg='red', border=0, text="Empty fields are not allowed.")
            error_mob.place(relx=.19,rely=.47)
            
            Frame(frm,width=220,height=1,bg='red').place(relx=.7,rely=.46)
            error_adh = Label(frm, font=('arial', 8, 'bold'), bg='white', fg='red', border=0, text="Empty fields are not allowed.")
            error_adh.place(relx=.7,rely=.47)
            
            Frame(frm,width=220,height=1,bg='red').place(relx=.19,rely=.56)
            error_email = Label(frm, font=('arial', 8, 'bold'), bg='white', fg='red', border=0, text="Empty fields are not allowed.")
            error_email.place(relx=.19,rely=.57)
            
            Frame(frm,width=220,height=1,bg='red').place(relx=.19,rely=.66)
            error_nom = Label(frm, font=('arial', 8, 'bold'), bg='white', fg='red', border=0, text="Empty fields are not allowed.")
            error_nom.place(relx=.19,rely=.67)
            Frame(frm,width=220,height=1,bg='red').place(relx=.7,rely=.66)
            error_nom_rel = Label(frm, font=('arial', 8, 'bold'), bg='white', fg='red', border=0, text="Empty fields are not allowed.")
            error_nom_rel.place(relx=.7,rely=.67)
        elif len(fname)==0:
            Frame(frm,width=220,height=1,bg='red').place(relx=.19,rely=.16)
            error_first_name = Label(frm, font=('arial', 8, 'bold'), bg='white', fg='red', border=0, text="Empty fields are not allowed.")
            error_first_name.place(relx=.19,rely=.17)            
        elif len(lname)==0:
            Frame(frm,width=220,height=1,bg='red').place(relx=.7,rely=.16)
            error_last_name = Label(frm, font=('arial', 8, 'bold'), bg='white', fg='red', border=0, text="Empty fields are not allowed.")
            error_last_name.place(relx=.7,rely=.17)
        elif len(dob)==0:
            Frame(frm,width=220,height=1,bg='red').place(relx=.19,rely=.26)
            error_dob = Label(frm, font=('arial', 8, 'bold'), bg='white', fg='red', border=0, text="Empty fields are not allowed.")
            error_dob.place(relx=.19,rely=.27)
        elif len(fathername)==0: 
            Frame(frm,width=220,height=1,bg='red').place(relx=.19,rely=.36)
            error_father = Label(frm, font=('arial', 8, 'bold'), bg='white', fg='red', border=0, text="Empty fields are not allowed.")
            error_father.place(relx=.19,rely=.37)
        elif len(mothername)==0:   
            Frame(frm,width=220,height=1,bg='red').place(relx=.7,rely=.36)
            error_mother = Label(frm, font=('arial', 8, 'bold'), bg='white', fg='red', border=0, text="Empty fields are not allowed.")
            error_mother.place(relx=.7,rely=.37)
        elif len(mob)==0:   
            Frame(frm,width=220,height=1,bg='red').place(relx=.19,rely=.46)
            error_mob = Label(frm, font=('arial', 8, 'bold'), bg='white', fg='red', border=0, text="Empty fields are not allowed.")
            error_mob.place(relx=.19,rely=.47)
        elif len(adh)==0:    
            Frame(frm,width=220,height=1,bg='red').place(relx=.7,rely=.46)
            error_adh = Label(frm, font=('arial', 8, 'bold'), bg='white', fg='red', border=0, text="Empty fields are not allowed.")
            error_adh.place(relx=.7,rely=.47)
        elif len(email)==0:    
            Frame(frm,width=220,height=1,bg='red').place(relx=.19,rely=.56)
            error_email = Label(frm, font=('arial', 8, 'bold'), bg='white', fg='red', border=0, text="Empty fields are not allowed.")
            error_email.place(relx=.19,rely=.57)
        elif len(nomineename)==0:    
            Frame(frm,width=220,height=1,bg='red').place(relx=.19,rely=.66)
            error_nom = Label(frm, font=('arial', 8, 'bold'), bg='white', fg='red', border=0, text="Empty fields are not allowed.")
            error_nom.place(relx=.19,rely=.67)            
        elif len(nomineerelation)==0:    
            Frame(frm,width=220,height=1,bg='red').place(relx=.7,rely=.66)
            error_nom_rel = Label(frm, font=('arial', 8, 'bold'), bg='white', fg='red', border=0, text="Empty fields are not allowed.")
            error_nom_rel.place(relx=.7,rely=.67)
            
        elif not fname.isalpha():
            Frame(frm,width=220,height=1,bg='red').place(relx=.19,rely=.16)
            error_first_name = Label(frm, font=('arial', 8, 'bold'), bg='white', fg='red', border=0, text="alphabets only no special characters & digits.")
            error_first_name.place(relx=.19,rely=.17)
        elif not lname.isalpha():
            Frame(frm,width=220,height=1,bg='red').place(relx=.7,rely=.16)
            error_last_name = Label(frm, font=('arial', 8, 'bold'), bg='white', fg='red', border=0, text="Alphabets only no special characters & digits.")
            error_last_name.place(relx=.7,rely=.17)
        elif not fathername.isalpha():
            Frame(frm,width=220,height=1,bg='red').place(relx=.19,rely=.36)
            error_father = Label(frm, font=('arial', 8, 'bold'), bg='white', fg='red', border=0, text="Alphabets only no special characters and digits")
            error_father.place(relx=.19,rely=.37)
        elif not mothername.isalpha():
            Frame(frm,width=220,height=1,bg='red').place(relx=.7,rely=.36)
            error_mother = Label(frm, font=('arial', 8, 'bold'), bg='white', fg='red', border=0, text="Alphabets only no special characters & digits.")
            error_mother.place(relx=.7,rely=.37)
        elif not re.fullmatch("(0|91)?[6-9][0-9]{9}", mob):
            Frame(frm,width=220,height=1,bg='red').place(relx=.19,rely=.46)
            error_mob = Label(frm, font=('arial', 8, 'bold'), bg='white', fg='red', border=0, text="Invalid Mobile Number")
            error_mob.place(relx=.19,rely=.47)
        elif not re.fullmatch("^[2-9]{1}[0-9]{11}$", adh):
            Frame(frm,width=220,height=1,bg='red').place(relx=.7,rely=.46)
            error_adh = Label(frm, font=('arial', 8, 'bold'), bg='white', fg='red', border=0, text="Invalid Aadhar Number")
            error_adh.place(relx=.7,rely=.47)
        elif not re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,3}\b',email):
            Frame(frm,width=220,height=1,bg='red').place(relx=.19,rely=.56)
            error_email = Label(frm, font=('arial', 8, 'bold'), bg='white', fg='red', border=0, text="Invalid Email Id")
            error_email.place(relx=.19,rely=.57)            
        elif not nomineename.isalpha():
            Frame(frm,width=220,height=1,bg='red').place(relx=.19,rely=.66)
            error_nom = Label(frm, font=('arial', 8, 'bold'), bg='white', fg='red', border=0, text="Alphabets only no special characters & digits.")
            error_nom.place(relx=.19,rely=.67)
        elif not nomineerelation.isalpha():
            Frame(frm,width=220,height=1,bg='red').place(relx=.7,rely=.66)
            error_nom_rel = Label(frm, font=('arial', 8, 'bold'), bg='white', fg='red', border=0, text="Alphabets only no special characters & digits.")
            error_nom_rel.place(relx=.7,rely=.67)
        else:            
            frm.destroy()
            openaccount_next_screen(f_name,l_name,dob,gender,father_name,mother_name,mob_num,adh_num,email,acn_type,nominee_name,nominee_relation)


    def clear():
        f_name_entry.delete(0,"end")
        l_name_entry.delete(0,"end")
        dob_entry.delete(0,"end")
        father_name_entry.delete(0,"end")
        mother_name_entry.delete(0,"end")
        mob_entry.delete(0,"end")
        adh_num_entry.delete(0,"end")
        email_entry.delete(0,"end")
        nominee_name_entry.delete(0,"end")
        nominee_relation_entry.delete(0,"end")
        f_name_entry.focus()
    # def next_click()
    heading=Label(frm,text='Create an Account', fg='#052c65',bg='white',font=('arial',23,'bold','underline'))
    heading.place(relx=.35,rely=0)
    
    
    f_name_lbl=Label(frm,font=('arial',16,'bold'),bg='white',fg='#000',border=0,text="First Name:")
    f_name_lbl.place(relx=.02,rely=.1)
    f_name_entry=Entry(frm,font=('arial',16),bg='white',border=0,width=18)
    f_name_entry.place(relx=.19,rely=.10)
    f_name_entry.focus()
    Frame(frm,width=220,height=1,bg='black').place(relx=.19,rely=.16)

    
    l_name_lbl=Label(frm,font=('arial',16,'bold'),bg='white',fg='#000',border=0,text="Last Name:")
    l_name_lbl.place(relx=.5,rely=.1)
    l_name_entry=Entry(frm,font=('arial',16),bg='white',border=0,width=18)
    l_name_entry.place(relx=.7,rely=.10)
    Frame(frm,width=220,height=1,bg='black').place(relx=.7,rely=.16)
    
    dob_lbl=Label(frm,font=('arial',16,'bold'),bg='white',fg='#000',border=0,text="Date of Birth:")
    dob_lbl.place(relx=.02,rely=.2)
    # dob_entry=Entry(frm,font=('arial',16),bg='white',border=0,width=18)
    dob_entry=DateEntry(frm,selectmode='day',font=('arial',16),bg='white',border=0,width=17)
    dob_entry.place(relx=.19,rely=.20)
    Frame(frm,width=220,height=1,bg='black').place(relx=.19,rely=.26)
    

    gender_lbl = Label(frm, font=('arial', 16, 'bold'), bg='white', fg='#000', border=0, text="Gender:")
    gender_lbl.place(relx=.5, rely=.2)

    
    selected_gender = StringVar()
    def select_gender(gender):
        selected_gender.set(gender)

    gen_btn1 = Checkbutton(frm, text="Male", variable=selected_gender, onvalue="Male", offvalue="",
                           width=10, fg='#000', bg='white', command=lambda: select_gender("Male"))
    gen_btn2 = Checkbutton(frm, text="Female", variable=selected_gender, onvalue="Female", offvalue="",
                           width=10, fg='#000', bg='white', command=lambda: select_gender("Female"))
    gen_btn3 = Checkbutton(frm, text="Other", variable=selected_gender, onvalue="Other", offvalue="",
                           width=10, fg='#000', bg='white', command=lambda: select_gender("Other"))

    gen_btn1.place(relx=.68, rely=.20)
    gen_btn2.place(relx=.75, rely=.20)
    gen_btn3.place(relx=.83, rely=.20)

    father_name_lbl=Label(frm,font=('arial',16,'bold'),bg='white',fg='#000',border=0,text="Father Name:")
    father_name_lbl.place(relx=.02,rely=.3)
    father_name_entry=Entry(frm,font=('arial',16),bg='white',border=0,width=18)
    father_name_entry.place(relx=.19,rely=.30)
    Frame(frm,width=220,height=1,bg='black').place(relx=.19,rely=.36)
    
    mother_name_lbl=Label(frm,font=('arial',16,'bold'),bg='white',fg='#000',border=0,text="Mother Name:")
    mother_name_lbl.place(relx=.5,rely=.3)
    mother_name_entry=Entry(frm,font=('arial',16),bg='white',border=0,width=18)
    mother_name_entry.place(relx=.7,rely=.30)
    Frame(frm,width=220,height=1,bg='black').place(relx=.7,rely=.36)
 
    mob_lbl=Label(frm,font=('arial',16,'bold'),bg='white',fg='#000',border=0,text="Mobile Numabr:")
    mob_lbl.place(relx=.02,rely=.4)
    mob_entry=Entry(frm,font=('arial',16),bg='white',border=0,width=18)
    mob_entry.place(relx=.19,rely=.40)
    Frame(frm,width=220,height=1,bg='black').place(relx=.19,rely=.46)
    
    adh_num_lbl=Label(frm,font=('arial',16,'bold'),bg='white',fg='#000',border=0,text="Aadhar Number:")
    adh_num_lbl.place(relx=.5,rely=.4)
    adh_num_entry=Entry(frm,font=('arial',16),bg='white',border=0,width=18)
    adh_num_entry.place(relx=.7,rely=.40)
    Frame(frm,width=220,height=1,bg='black').place(relx=.7,rely=.46)
    
    email_lbl=Label(frm,font=('arial',16,'bold'),bg='white',fg='#000',border=0,text="Email Id:")
    email_lbl.place(relx=.02,rely=.5)
    email_entry=Entry(frm,font=('arial',16),bg='white',border=0,width=18)
    email_entry.place(relx=.19,rely=.50)
    Frame(frm,width=220,height=1,bg='black').place(relx=.19,rely=.56)
    

    
    acntype_lbl=Label(frm,font=('arial',16,'bold'),bg='white',fg='#000',border=0,text="Account type:")  
    acntype_lbl.place(relx=.5,rely=.5)
    acntype_cb=Combobox(frm,font=('arial',16),values=['Select Account type','Saving','Current','Fixed Deposit'],width='17')
    acntype_cb.current(0)
    acntype_cb.place(relx=.7,rely=.50)
    
    
    nominee_name_lbl=Label(frm,font=('arial',16,'bold'),bg='white',fg='#000',border=0,text="Nominee Name:")
    nominee_name_lbl.place(relx=.02,rely=.6)
    nominee_name_entry=Entry(frm,font=('arial',16),bg='white',border=0,width=18)
    nominee_name_entry.place(relx=.19,rely=.6)
    Frame(frm,width=220,height=1,bg='black').place(relx=.19,rely=.66)
    
    
    nominee_relation_lbl=Label(frm,font=('arial',16,'bold'),bg='white',fg='#000',border=0,text="Nominee Relation:")
    nominee_relation_lbl.place(relx=.5,rely=.6)
    nominee_relation_entry=Entry(frm,font=('arial',16),bg='white',border=0,width=18)
    nominee_relation_entry.place(relx=.7,rely=.60)
    Frame(frm,width=220,height=1,bg='black').place(relx=.7,rely=.66)
    
    
    
    btn_create = Button(frm, font=('arial', 10, 'bold'), text="Next", bg='#198754', fg='white', width=15, border=1, cursor="hand2", 
                    command=lambda:openaccount_next_click(f_name_entry.get(), l_name_entry.get(), dob_entry.get(), selected_gender.get(), father_name_entry.get(),
                        mother_name_entry.get(), mob_entry.get(), adh_num_entry.get(), email_entry.get(), acntype_cb.get(),
                        nominee_name_entry.get(), nominee_relation_entry.get()))


    btn_create.place(relx=.35,rely=.83)
    btn_clear=Button(frm,font=('arial',10,'bold'),text="Clear",bg='#dc3545',fg='white',width=15,border=1,cursor="hand2",command=clear)
    btn_clear.place(relx=.5,rely=.83)
    lable=Label(frm,text="I have an account.",fg='#000',bg='white',font=('arial',11,'bold'))
    lable.place(relx=.4,rely=.93)
    btn_old_act=Button(frm,font=('arial',9,'bold','underline'),text="Login hear",bg='white',cursor='hand2',fg='#0d6efd',width=15,border=0,command=home_click)
    btn_old_act.place(relx=.53,rely=.93)
    
def openaccount_next_screen(f_name,l_name,dob,gender,father_name,mother_name,mob_num,adh_num,email,acn_type,nominee_name,nominee_relation):
    frm=Frame(win) 
    frm.configure(bg="white")
    frm.place(relx=.1,rely=.2,relwidth=.8,relheight=.7)
    
    def mask_email(email):
        username, domain = email.split('@')
        masked_username = username[:2] + '*'*(len(username)-4) + username[-2:]
        masked_email = masked_username + '@' + domain  
        return masked_email
  
        
    def generate_account_number(starting_number=1800100020240000):
        try:
            conobj = sqlite3.connect(database="banking.sqlite")
            curobj = conobj.cursor()
            curobj.execute("SELECT account_no FROM user_details ORDER BY user_id DESC LIMIT 1")
            last_account = curobj.fetchone()
            last_account_number = last_account[0] if last_account else starting_number - 1
            account_number = last_account_number + 1
            conobj.close()
            return account_number
        except Exception as e:
            print("Error generating account number:", str(e))
            return None    
    def get_create_account_otp_screen(correct_otp,f_name,l_name,dob,gender,father_name,mother_name,mob_num,adh_num,email,acn_type,nominee_name,nominee_relation,address1,address2,pincode,state,city,country,password):
        frm = Frame(win)
        frm.configure(bg="white")
        frm.place(relx=.1, rely=.2, relwidth=.8, relheight=.7)
        
        def home_click():
            frm.destroy()
            home_screen()
        img = PhotoImage(file='forgot_otp_img.png')
        label_img = Label(frm, image=img, bg="white")
        label_img.image = img
        label_img.place(relx=.11, rely=.25)
        heading = Label(frm, text='Reset Your Password', fg='#052c65', bg='white', font=('arial', 23, 'bold', 'underline'))
        heading.place(relx=.45, rely=.08)
        inf_details = Label(frm, text='We have just sent 6 digit OTP to your registered email ID', fg='#000', bg='white',
                            font=('arial', 10, 'bold'))
        inf_details.place(relx=.45, rely=.2)
        inf_email = Label(frm, text=f'Registered id: {mask_email(email)}', fg='#000', bg='white',
                          font=('arial', 10, 'bold'))
        inf_email.place(relx=.45, rely=.28)
        inf_email_proc = Label(frm, text='Enter that code hear to proceed', fg='#000', bg='white',
                               font=('arial', 10, 'bold'))
        inf_email_proc.place(relx=.45, rely=.35)

        def handle_key_release(event):
            entry_widget = event.widget
            entry_str = entry_widget.get()
            entry_str = ''.join(char for char in entry_str if char.isdigit())
            entry_widget.delete(0, END)
            entry_widget.insert(0, entry_str)

            if entry_str and event.char.isdigit():
                entry_widget.tk_focusNext().focus()


        otp_entries = []
        for i in range(6):
            otp_entry = Entry(frm, font=('arial', 18), bg='white', border=1, width=3)
            otp_entry.place(relx=0.45 + i * 0.05, rely=0.42, relheight=0.08)
            otp_entry.bind('<KeyRelease>', handle_key_release)
            Frame(frm, width=43, height=1, bg='black').place(relx=0.45 + i * 0.05, rely=0.5)
            otp_entries.append(otp_entry)
        otp_entries[0].focus()
        
        
        def submit_otp():
            otp_input = "".join(entry.get() for entry in otp_entries)
            if verify_otp(int(otp_input), correct_otp):
                current_time = time.ctime()
                new_account_number = generate_account_number()
                if filename:
                    with open(filename, "rb") as file:
                        image_data = file.read()
                        conobj=sqlite3.connect(database='banking.sqlite')
                        curobj=conobj.cursor()
                        curobj.execute("insert into user_details(account_no,first_name,last_name,dob,gender,father_name,mother_name,mobile_no,email,aadhar_no,account_type,nominee_name,nominee_relation,address_1,address_2,pin_code,city,state,country,password,user_image,account_create_date_time) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(new_account_number,f_name,l_name,dob,gender,father_name,mother_name,mob_num,email,adh_num,acn_type,nominee_name,nominee_relation,address1,address2,pincode,city,state,country,password,sqlite3.Binary(image_data),current_time))
                        conobj.commit()            
                        curobj.close()
                        curobj=conobj.cursor()
                        curobj.execute("select max(account_no) from user_details")
                        tup=curobj.fetchone()
                        conobj.close()
                        try:
                            con = gmail.GMail("chaudharyshivam702@gmail.com", "")

                            cre_gen = gmail.message(to=email, subject="Your account has been successfully created.", text=f"Dear {f_name} {l_name},\n\nCongratulations! You have successfully created an account. Your bank account number is {new_account_number}. You can now use banking funds from your account. Please do not share this account number and password with anyone.\n\nWarm Regards,\nCustomer Care\nBank.")

                            con.send(cre_gen) 
                        except:
                            print("mail failed")                     
                        messagebox.showinfo("Open Account",f"Your Account is Opend with ACN:{tup[0]}")
                        frm.destroy()
                        home_screen()
            else:
                for i in range(6):
                    Frame(frm, width=43, height=1, bg='red').place(relx=0.45 + i * 0.05, rely=0.5)
                inavald_otp=Label(frm,text="Invalid Otp! Please try again.",font=('arial',8,'bold'),fg='red',bg='white')
                inavald_otp.place(relx=.45,rely=.51)

        inf_don = Label(frm, text="Don't get OTP?- regenerate OTP", fg='#000', bg='white', font=('arial', 10, 'bold'))
        inf_don.place(relx=.45, rely=.55)
        remaining_time_var = IntVar(value=total_seconds)
        label_countdown = Label(win, text="", fg='#000', bg='white', font=('arial', 10, 'bold'))
        label_countdown.place(relx=.625, rely=.582)
        countdown(label_countdown, remaining_time_var)
        btn_resend = Button(win, font=('arial', 15, 'bold'), text="Resend Otp", bg='#17a2b8', cursor='hand2',
                            fg='white', width=10, border=1, command=lambda: resend_otp(label_countdown, remaining_time_var))
        btn_resend.place(relx=.56, rely=.69)
        btn_submit = Button(frm, font=('arial', 15, 'bold'), text="Submit", bg='#28a745', fg='white', border=1,
                            cursor="hand2", command=submit_otp)
        btn_submit.place(relx=.45, rely=.7)
        btn_can = Button(frm, font=('arial', 15, 'bold'), text="Cancel", bg='#28a745', fg='white', border=1,
                            cursor="hand2", command=home_click)
        btn_can.place(relx=.7, rely=.7)

    
    def create_account_click():
        add1=add1_entry.get()
        add2=add2_entry.get()
        pincode=pin_entry.get()
        city=city_entry.get()
        state=state_entry.get()
        country=country_entry.get()
        password=pass_entry.get()
        con_password=con_pass_entry.get()
        if len(add1)==0 and len(pincode)==0 and len(city)==0 and len(state) and len(country)==0 and len(password)==0 and len(con_password)==0:
            Frame(frm,width=265,height=1,bg='red').place(relx=.19,rely=.16)
            error_add1 = Label(frm, font=('arial', 8, 'bold'), bg='white', fg='red', border=0, text="Empty fields are not allowed.")
            error_add1.place(relx=.19,rely=.17)
            
            Frame(frm,width=265,height=1,bg='red').place(relx=.19,rely=.26)
            error_pin = Label(frm, font=('arial', 8, 'bold'), bg='white', fg='red', border=0, text="Empty fields are not allowed.")
            error_pin.place(relx=.19,rely=.27)
            
            Frame(frm,width=265,height=1,bg='red').place(relx=.7,rely=.26)
            error_city = Label(frm, font=('arial', 8, 'bold'), bg='white', fg='red', border=0, text="Empty fields are not allowed.")
            error_city.place(relx=.7,rely=.27)
            
            Frame(frm,width=265,height=1,bg='red').place(relx=.19,rely=.36)
            error_state = Label(frm, font=('arial', 8, 'bold'), bg='white', fg='red', border=0, text="Empty fields are not allowed.")
            error_state.place(relx=.19,rely=.37)
            
            Frame(frm,width=265,height=1,bg='red').place(relx=.7,rely=.36)
            error_country = Label(frm, font=('arial', 8, 'bold'), bg='white', fg='red', border=0, text="Empty fields are not allowed.")
            error_country.place(relx=.7,rely=.37)
            
            Frame(frm,width=265,height=1,bg='red').place(relx=.7,rely=.46)
            error_pass = Label(frm, font=('arial', 8, 'bold'), bg='white', fg='red', border=0, text="Empty fields are not allowed.")
            error_pass.place(relx=.7,rely=.47)
            
            Frame(frm,width=265,height=1,bg='red').place(relx=.7,rely=.56)
            error_con_pass = Label(frm, font=('arial', 8, 'bold'), bg='white', fg='red', border=0, text="Empty fields are not allowed.")
            error_con_pass.place(relx=.7,rely=.57)
        elif len(add1)==0:
            Frame(frm,width=265,height=1,bg='red').place(relx=.19,rely=.16)
            error_add1 = Label(frm, font=('arial', 8, 'bold'), bg='white', fg='red', border=0, text="Empty fields are not allowed.")
            error_add1.place(relx=.19,rely=.17)
        elif len(pincode)==0:
            Frame(frm,width=265,height=1,bg='red').place(relx=.19,rely=.26)
            error_pin = Label(frm, font=('arial', 8, 'bold'), bg='white', fg='red', border=0, text="Empty fields are not allowed.")
            error_pin.place(relx=.19,rely=.27)
        elif len(city)==0:
            Frame(frm,width=265,height=1,bg='red').place(relx=.7,rely=.26)
            error_city = Label(frm, font=('arial', 8, 'bold'), bg='white', fg='red', border=0, text="Empty fields are not allowed.")
            error_city.place(relx=.7,rely=.27)
        elif len(state)==0:
            Frame(frm,width=265,height=1,bg='red').place(relx=.7,rely=.36)
            error_state = Label(frm, font=('arial', 8, 'bold'), bg='white', fg='red', border=0, text="Empty fields are not allowed.")
            error_state.place(relx=.19,rely=.37)
        elif len(country)==0:
            Frame(frm,width=265,height=1,bg='red').place(relx=.7,rely=.36)
            error_country = Label(frm, font=('arial', 8, 'bold'), bg='white', fg='red', border=0, text="Empty fields are not allowed.")
            error_country.place(relx=.7,rely=.37)
        elif len(password)==0:    
            Frame(frm,width=265,height=1,bg='red').place(relx=.7,rely=.46)
            error_pass = Label(frm, font=('arial', 8, 'bold'), bg='white', fg='red', border=0, text="Empty fields are not allowed.")
            error_pass.place(relx=.7,rely=.47)
        elif len(con_password)==0:    
            Frame(frm,width=265,height=1,bg='red').place(relx=.7,rely=.56)
            error_con_pass = Label(frm, font=('arial', 8, 'bold'), bg='white', fg='red', border=0, text="Empty fields are not allowed.")
            error_con_pass.place(relx=.7,rely=.57)
        elif len(pincode)!=6:
            Frame(frm,width=265,height=1,bg='red').place(relx=.19,rely=.26)
            error_pin = Label(frm, font=('arial', 8, 'bold'), bg='white', fg='red', border=0, text="Invalid Pin code")
            error_pin.place(relx=.19,rely=.27)
        elif not pincode.isdigit():
            Frame(frm,width=265,height=1,bg='red').place(relx=.19,rely=.26)
            error_pin = Label(frm, font=('arial', 8, 'bold'), bg='white', fg='red', border=0, text="Digits only no special characters & alphabets.")
            error_pin.place(relx=.19,rely=.27)
        elif not state.isalpha():
            Frame(frm,width=265,height=1,bg='red').place(relx=.19,rely=.36)
            error_state = Label(frm, font=('arial', 8, 'bold'), bg='white', fg='red', border=0, text="Alphabets only no special characters & digits.")
            error_state.place(relx=.19,rely=.37)
        elif not country.isalpha():
            Frame(frm,width=265,height=1,bg='red').place(relx=.7,rely=.36)
            error_country = Label(frm, font=('arial', 8, 'bold'), bg='white', fg='red', border=0, text="Alphabets only no special characters & digits.")
            error_country.place(relx=.7,rely=.37)
        elif len(password)<8:
            Frame(frm,width=265,height=1,bg='red').place(relx=.7,rely=.46)
            error_pass = Label(frm, font=('arial', 8, 'bold'), bg='white', fg='red', border=0, text="Minimum of 8 Characters")
            error_pass.place(relx=.7,rely=.47)
        elif not re.match("^[A-Z]",password):
            Frame(frm,width=265,height=1,bg='red').place(relx=.7,rely=.46)
            error_pass = Label(frm, font=('arial', 8, 'bold'), bg='white', fg='red', border=0, text="uppercase letter at the beginning")
            error_pass.place(relx=.7,rely=.47)
        elif not (any(c.isalpha() for c in password) and any(c.isdigit() for c in password)):
            Frame(frm, width=265, height=1, bg='red').place(relx=.7, rely=.46)
            error_pass = Label(frm, font=('arial', 8, 'bold'), bg='white', fg='red', border=0, text="At least one letter")
            error_pass.place(relx=.7, rely=.47)
        elif password!=con_password:
            Frame(frm,width=265,height=1,bg='black').place(relx=.7,rely=.56)
            error_pass_match = Label(frm, font=('arial', 8, 'bold'), bg='white', fg='red', border=0, text="Password is not match")
            error_pass_match.place(relx=.7, rely=.57)           
        else:
            frm.destroy()            
            otp=generate_and_send_otp(email,f_name,l_name)            
            get_create_account_otp_screen(otp,f_name,l_name,dob,gender,father_name,mother_name,mob_num,adh_num,email,acn_type,nominee_name,nominee_relation,add1,add2,pincode,city,state,country,password)
            
    def openaccount_click():
        frm.destroy()
        openaccount_screen()
        
    def clear():
        add1_entry.delete(0,"end")
        add2_entry.delete(0,"end")
        pin_entry.delete(0,"end")
        city_entry.delete(0,"end")
        country_entry.delete(0,"end")
        state_entry.delete(0,"end")
        
    heading=Label(frm,text='Create an Account', fg='#052c65',bg='white',font=('arial',23,'bold','underline'))
    heading.place(relx=.35,rely=0)
    # curnt=Label(frm,text='Create an Account', fg='#052c65',bg='white',font=('arial',23,'bold','underline'))
    # heading.place(relx=.35,rely=0)
    add1_lbl=Label(frm,font=('arial',16,'bold'),bg='white',fg='#000',border=0,text="Address 1:")
    add1_lbl.place(relx=.02,rely=.1)
    add1_entry=Entry(frm,font=('arial',16),bg='white',border=0,width=22)
    add1_entry.place(relx=.19,rely=.10)
    

    add1_entry.focus()
    Frame(frm,width=265,height=1,bg='black').place(relx=.19,rely=.16)
    
    add_dec_lbl=Label(frm,font=('arial',8,'bold'),bg='white',fg='#000',border=0,text="Street address, P.O, company name")
    add_dec_lbl.place(relx=.19,rely=.165)
    
    add2_lbl=Label(frm,font=('arial',16,'bold'),bg='white',fg='#000',border=0,text="Address 2:")
    add2_lbl.place(relx=.5,rely=.1)
    add2_entry=Entry(frm,font=('arial',16),bg='white',border=0,width=22)
    add2_entry.place(relx=.7,rely=.10)
    Frame(frm,width=265,height=1,bg='black').place(relx=.7,rely=.16)
    add_dec_lbl=Label(frm,font=('arial',8,'bold'),bg='white',fg='#000',border=0,text="Apartment,unit,floor etc")
    add_dec_lbl.place(relx=.7,rely=.165)
    
    pin_lbl=Label(frm,font=('arial',16,'bold'),bg='white',fg='#000',border=0,text="Pin Code:")
    pin_lbl.place(relx=.02,rely=.2)
    pin_entry=Entry(frm,font=('arial',16),bg='white',border=0,width=22)
    pin_entry.place(relx=.19,rely=.20)
    Frame(frm,width=265,height=1,bg='black').place(relx=.19,rely=.26)
    
    
    city_lbl=Label(frm,font=('arial',16,'bold'),bg='white',fg='#000',border=0,text="City:")
    city_lbl.place(relx=.5,rely=.2)
    city_entry=Entry(frm,font=('arial',16),bg='white',border=0,width=22)
    city_entry.place(relx=.7,rely=.20)
    Frame(frm,width=265,height=1,bg='black').place(relx=.7,rely=.26)
    
    state_lbl=Label(frm,font=('arial',16,'bold'),bg='white',fg='#000',border=0,text="State:")
    state_lbl.place(relx=.02,rely=.3)
    state_entry=Entry(frm,font=('arial',16),bg='white',border=0,width=22)
    state_entry.place(relx=.19,rely=.30)
    Frame(frm,width=265,height=1,bg='black').place(relx=.19,rely=.36)
    
    
    country_lbl=Label(frm,font=('arial',16,'bold'),bg='white',fg='#000',border=0,text="Country:")
    country_lbl.place(relx=.5,rely=.3)
    country_entry=Entry(frm,font=('arial',16),bg='white',border=0,width=32)
    country_entry.place(relx=.7,rely=.30)
    Frame(frm,width=265,height=1,bg='black').place(relx=.7,rely=.36)
    
    img_upl_lbl=Label(frm,font=('arial',16,'bold'),bg='white',fg='#000',border=0,text="Upload Image:")
    img_upl_lbl.place(relx=.02,rely=.5)
    
    Frame(frm,width=122,height=1,bg='black').place(relx=.2,rely=.40)
    Frame(frm,width=1,height=122,bg='black').place(relx=.2,rely=.4)
    Frame(frm,width=1,height=122,bg='black').place(relx=.32,rely=.4)
    Frame(frm,width=122,height=1,bg='black').place(relx=.2,rely=.65)
    
    uplaod_btn = Button(frm, text='Upload File', width=20, command=lambda: upload_file())
    uplaod_btn.place(relx=.19,rely=.66)
    
    def upload_file():
        global img
        global filename
        f_types = [('Jpg Files', '*.jpg')]
        filename = filedialog.askopenfilename(filetypes=f_types)
        img = Image.open(filename)
        img = img.resize((100, 100), Image.LANCZOS)
        img = ImageTk.PhotoImage(img)
        b2 = Button(frm, image=img) 
        b2.place(relx=.21,rely=.41)
        
        
    pass_lbl=Label(frm,font=('arial',16,'bold'),bg='white',fg='#000',border=0,text="Password:")
    pass_lbl.place(relx=.5,rely=.4)
    pass_entry=Entry(frm,font=('arial',16),bg='white',border=0,width=32)
    pass_entry.place(relx=.7,rely=.40)
    Frame(frm,width=265,height=1,bg='black').place(relx=.7,rely=.46)
    
    con_pass_lbl=Label(frm,font=('arial',16,'bold'),bg='white',fg='#000',border=0,text="Confirm Password:")
    con_pass_lbl.place(relx=.5,rely=.5)
    con_pass_entry=Entry(frm,font=('arial',16),bg='white',border=0,width=32)
    con_pass_entry.place(relx=.7,rely=.50)
    Frame(frm,width=265,height=1,bg='black').place(relx=.7,rely=.56)
    
    btn_back=Button(frm,font=('arial',10,'bold'),text="Back",bg='#17a2b8',fg='white',width=15,border=1,cursor="hand2",command=openaccount_click)
    btn_back.place(relx=.25,rely=.83)
    
    btn_create=Button(frm,font=('arial',10,'bold'),text="Create Account",bg='#198754',fg='white',width=15,border=1,cursor="hand2",command=create_account_click)
    btn_create.place(relx=.4,rely=.83)
    
    btn_clear=Button(frm,font=('arial',10,'bold'),text="Clear",bg='#dc3545',fg='white',width=15,border=1,cursor="hand2",command=clear)
    btn_clear.place(relx=.55,rely=.83)

    
    
def recoverpass_screen():
    frm=Frame(win) 
    frm.configure(bg="white")
    frm.place(relx=.1,rely=.2,relwidth=.8,relheight=.7)
    
    def home_click():
        frm.destroy()
        home_screen()
    def get_otp_click():
     
        account = acn_entry.get()
        email = email_entry.get()
        mobile = mob_entry.get()
        
        conobj = sqlite3.connect(database='banking.sqlite')
        curobj = conobj.cursor()
        curobj.execute("SELECT account_no, first_name, last_name, mobile_no, email FROM user_details WHERE account_no=? and email=? and mobile_no=?", (account, email, mobile))
        tup = curobj.fetchone()
        curobj.close()
        
        if len(account) == 0 or len(email) == 0 or len(mobile) == 0:
            messagebox.showerror("Error", "Please fill in all fields.")
        elif tup is None:
            messagebox.showerror("Error", "Invalid account number, email, or mobile number.")
        else:
            try:
                otp = random.randint(100000, 999999)
                con = gmail.GMail("chaudharyshivamchaudhary702@gmail.com", "")
                otp_gen = gmail.Message(to=email, subject="One Time Password (OTP) for Account recovery process on Bank", text=f"Dear {tup[1]} {tup[2]},\n\n\n\nYour One Time Password (OTP) for Forgot Password recovery of Account No. {account} on BANK is {otp}.\n\nPlease note, this OTP is valid only for mentioned transaction and cannot be used for any other transaction.\nPlease do not share this One Time Password with anyone.\n\n\nWarm Regards,\nCustomer Care\nBank.")
                con.send(otp_gen)
                frm.destroy()
                get_otp_screen(otp, email, account)
            except Exception as e:
                messagebox.showerror("Sorber", f"An error occurred: {str(e)}")
                frm.destroy()
                home_screen()
                
    img=PhotoImage(file='forgot.png').subsample(1,1)
    label_img = Label(frm, image=img, bg="white")
    label_img.image = img
    label_img.place(relx=.13,rely=.2)
    
    heading=Label(frm,text='Forgot your password?', fg='#052c65',bg='white',font=('arial',23,'bold','underline'))
    heading.place(relx=.45,rely=.08)
    heading_details=Label(frm,text='Please enter your details,you use to signin.', fg='#000',bg='white',font=('arial',8))
    heading_details.place(relx=.45,rely=.17)
    
    
    def on_enter(e):
        acn_entry.delete(0,'end')
    def on_leave(e):
        name=acn_entry.get()
        if name=='':
            acn_entry.insert(0,'Acount Number')
    acn_entry=Entry(frm,font=('arial',11),bg='white',width=45,fg='#000',border=0)
    acn_entry.insert(0,'Acount Number')
    acn_entry.bind('<FocusIn>',on_enter)
    acn_entry.bind('<FocusOut>',on_leave)
    acn_entry.place(relx=.45,rely=.26)
    Frame(frm,width=362,height=2,bg='black').place(relx=.45,rely=.3)
    def acn_clear():
        acn_entry.delete(0,"end")
    img=PhotoImage(file='images-removebg-preview.png')
    img = img.subsample(9, 9)
    btn_pro_img = Button(frm, image=img, bg="white", border=0,command=acn_clear)
    btn_pro_img.image = img
    btn_pro_img.place(relx=0.78, rely=0.24)
    
    def on_enter(e):
        mob_entry.delete(0,'end')
    def on_leave(e):
        name=mob_entry.get()
        if name=='':
            mob_entry.insert(0,'Mobile Number')
    mob_entry=Entry(frm,font=('arial',11),bg='white',width=45,fg='#000',border=0)
    mob_entry.insert(0,'Mobile Number')
    mob_entry.bind('<FocusIn>',on_enter)
    mob_entry.bind('<FocusOut>',on_leave)
    mob_entry.place(relx=.45,rely=.36)    
    Frame(frm,width=362,height=2,bg='black').place(relx=.45,rely=.4)
    def acn_clear():
        mob_entry.delete(0,"end")
    img=PhotoImage(file='images-removebg-preview.png')
    img = img.subsample(9, 9)
    btn_pro_img = Button(frm, image=img, bg="white", border=0,command=acn_clear)
    btn_pro_img.image = img
    btn_pro_img.place(relx=0.78, rely=0.34)
    
    def on_enter(e):
        email_entry.delete(0,'end')
    def on_leave(e):
        name=email_entry.get()
        if name=='':
            email_entry.insert(0,'Email Id')
    email_entry=Entry(frm,font=('arial',11),bg='white',width=45,fg='#000',border=0)
    email_entry.insert(0,'Email Id')
    email_entry.bind('<FocusIn>',on_enter)
    email_entry.bind('<FocusOut>',on_leave)
    email_entry.place(relx=.45,rely=.46)
    Frame(frm,width=362,height=2,bg='black').place(relx=.45,rely=.5)
    
    def acn_clear():
        email_entry.delete(0,"end")
    img=PhotoImage(file='images-removebg-preview.png')
    img = img.subsample(9, 9)
    btn_pro_img = Button(frm, image=img, bg="white", border=0,command=acn_clear)
    btn_pro_img.image = img
    btn_pro_img.place(relx=0.78, rely=0.44)
    
    
    rem_ckb = Checkbutton(frm, onvalue=1, offvalue=0, width=0,fg='#000',bg='white')
    rem_ckb.place(relx=.45,rely=.58)
    rem_leb=Label(frm,text='Remember me next time.', fg='#000',bg='white',font=('arial',12))
    rem_leb.place(relx=.47,rely=.58)
    
  
    btn_reset=Button(frm,font=('arial',20,'bold'),text="Get otp",bg='#0d6efd',fg='white',width=21,border=1,cursor="hand2",command=get_otp_click)
    btn_reset.place(relx=.45,rely=.7)
    btn_back=Button(frm,font=('arial',9,'bold','underline'),text="Back to Sign in",bg='white',cursor='hand2',fg='#0d6efd',width=15,border=0,command=home_click)
    btn_back.place(relx=.56,rely=.84)
    def get_otp_screen(otp,email,account):
        frm=Frame(win) 
        frm.configure(bg="white")
        frm.place(relx=.1,rely=.2,relwidth=.8,relheight=.7)        
        
        def get_forgot_click(account):            
            frm.destroy()
            get_forgot_screen(account)
        
        img=PhotoImage(file='forgot_otp_img.png')
        label_img = Label(frm, image=img, bg="white")
        label_img.image = img
        label_img.place(relx=.11,rely=.25)
        
        def mask_email(email):
            username, domain = email.split('@')
            masked_username = username[:2] + '*'*(len(username)-4) + username[-2:]
            masked_email = masked_username + '@' + domain  
            return masked_email

        heading=Label(frm,text='Reset Your Password', fg='#052c65',bg='white',font=('arial',23,'bold','underline'))
        heading.place(relx=.45,rely=.08)
        inf_details=Label(frm,text='We have just sent 6 digit OTP to your registered email ID', fg='#000',bg='white',font=('arial',10,'bold'))
        inf_details.place(relx=.45,rely=.2)
        
        inf_email=Label(frm,text=f'Registered id: {mask_email(email)}', fg='#000',bg='white',font=('arial',10,'bold'))
        inf_email.place(relx=.45,rely=.28)
        
        inf_email_proc=Label(frm,text='Enter that code hear to proceed', fg='#000',bg='white',font=('arial',10,'bold'))
        inf_email_proc.place(relx=.45,rely=.35)
                
    
        def handle_key_release(event):
            entry_widget = event.widget
            entry_str = entry_widget.get()
            entry_str = ''.join(char for char in entry_str if char.isdigit())
            entry_widget.delete(0, END)
            entry_widget.insert(0, entry_str)

            if entry_str and event.char.isdigit():
                entry_widget.tk_focusNext().focus()


        otp_entries = []
        for i in range(6):
            otp_entry = Entry(frm, font=('arial', 18), bg='white', border=1, width=3)
            otp_entry.place(relx=0.45 + i * 0.05, rely=0.42, relheight=0.08)
            otp_entry.bind('<KeyRelease>', handle_key_release)
            Frame(frm, width=43, height=1, bg='black').place(relx=0.45 + i * 0.05, rely=0.5)
            otp_entries.append(otp_entry)
        otp_entries[0].focus()
        
        
        def submit_otp():
            otp_input = "".join(entry.get() for entry in otp_entries)
            if verify_otp(int(otp_input), otp):
                frm.destroy()
                get_forgot_click(account)
            else:
                for i in range(6):
                    Frame(frm, width=43, height=1, bg='red').place(relx=0.45 + i * 0.05, rely=0.5)
                inavald_otp=Label(frm,text="Invalid Otp! Please try again.",font=('arial',8,'bold'),fg='red',bg='white')
                inavald_otp.place(relx=.45,rely=.51)   
    
        
        inf_don=Label(frm,text=f"Don't get OTP?- regenerate OTP", fg='#000',bg='white',font=('arial',10,'bold'))
        inf_don.place(relx=.45,rely=.55)
        
        remaining_time_var = IntVar(value=total_seconds) 

        label_countdown = Label(win, text="", fg='#000', bg='white', font=('arial', 10, 'bold'))
        label_countdown.place(relx=.625, rely=.582)

        countdown(label_countdown, remaining_time_var)

        btn_resend = Button(win, font=('arial', 15, 'bold'), text="Resend Otp", bg='#17a2b8', cursor='hand2',
                            fg='white', width=10, border=1)
        btn_resend.place(relx=.62, rely=.69)
        
        btn_reset=Button(frm,font=('arial',15,'bold'),text="Reset Password",bg='#28a745',fg='white',border=1,cursor="hand2",command=submit_otp)
        btn_reset.place(relx=.45,rely=.7)
        btn_back=Button(frm,font=('arial',9,'bold','underline'),text="Back to Sign in",bg='white',cursor='hand2',fg='#0d6efd',width=15,border=0,command=home_click)
        btn_back.place(relx=.56,rely=.84)
        


    def get_forgot_screen(account):
        frm=Frame(win) 
        frm.configure(bg="white")
        frm.place(relx=.1,rely=.2,relwidth=.8,relheight=.7)
               
        
        
        
        def submit_pass_click():
            conobj=sqlite3.connect(database='banking.sqlite')
            curobj=conobj.cursor()
            curobj.execute("SELECT password FROM user_details WHERE account_no=?",(account,))
            tup=curobj.fetchone()
            curobj.close()
            new_pass=new_pass_entry.get()
            con_pass=con_pass_entry.get()
            if len(new_pass)==0 and len(con_pass)==0:
                Frame(frm,width=362,height=2,bg='red').place(relx=.45,rely=.26)
                error_new_pass = Label(frm, font=('arial', 8, 'bold'), bg='white', fg='red', border=0, text="Empty fields are not allowed")
                error_new_pass.place(relx=.45, rely=.27)
                Frame(frm,width=362,height=2,bg='red').place(relx=.45,rely=.36)
                error_con_pass = Label(frm, font=('arial', 8, 'bold'), bg='white', fg='red', border=0, text="Empty fields are not allowed")
                error_con_pass.place(relx=.45, rely=.37)
            elif len(new_pass)==0:
                Frame(frm,width=362,height=2,bg='red').place(relx=.45,rely=.26)
                error_new_pass = Label(frm, font=('arial', 8, 'bold'), bg='white', fg='red', border=0, text="Empty fields are not allowed")
                error_new_pass.place(relx=.45, rely=.27)
            elif len(new_pass)<8:
                Frame(frm,width=362,height=2,bg='red').place(relx=.45,rely=.26)
                error_pass = Label(frm, font=('arial', 8, 'bold'), bg='white', fg='red', border=0, text="Minimum of 8 Characters")
                error_pass.place(relx=.45,rely=.27)
            elif not re.match("^[A-Z]",new_pass):
                Frame(frm,width=362,height=2,bg='red').place(relx=.45,rely=.26)
                error_pass = Label(frm, font=('arial', 8, 'bold'), bg='white', fg='red', border=0, text="uppercase letter at the beginning")
                error_pass.place(relx=.45,rely=.27)
            elif not (any(c.isalpha() for c in new_pass) and any(c.isdigit() for c in new_pass)):
                Frame(frm, width=362, height=2, bg='red').place(relx=.45, rely=.26)
                error_pass = Label(frm, font=('arial', 8, 'bold'), bg='white', fg='red', border=0, text="At least one digit")
                error_pass.place(relx=.45, rely=.27)
            elif new_pass!=con_pass:
                Frame(frm,width=362,height=2,bg='black').place(relx=.45,rely=.36)
                error_pass_match = Label(frm, font=('arial', 8, 'bold'), bg='white', fg='red', border=0, text="Password is not match")
                error_pass_match.place(relx=.45, rely=.37)
            elif new_pass==tup[0]:
                Frame(frm,width=362,height=2,bg='red').place(relx=.45,rely=.26)
                old_pass_error=Label(frm,font=('arial',8),bg='white',fg='red',border=0,text="New Passwords and Old Passwords Match")
                old_pass_error.place(relx=.45,rely=.27)
            else:
                conobj=sqlite3.connect(database="banking.sqlite")
                curobj=conobj.cursor()
                curobj.execute("UPDATE user_details SET password=? WHERE account_no=?", (new_pass,account))
                conobj.commit()
                conobj.close()
                
                conobj=sqlite3.connect(database="banking.sqlite")
                curobj=conobj.cursor()
                curobj.execute("select email,first_name,last_name from user_details where account_no=?", (account,))
                tup=curobj.fetchone()
                conobj.close()        
                try:
                    con = gmail.GMail("chaudharyshivam702@gmail.com", "")
                    # mail_gen_pass = gmail.Message(to=f"{tup[0]}", subject="Password change", text=f"Password Updated Successfully")
                    maill_gen = gmail.Message(to=f"{tup[0]}", subject="Password Update Successfully", text=f"Dear {tup[1]} {tup[2]},\n\nYour Password Frogot successfully.\n\nSincerely,\nYour Bank")
                    con.send(maill_gen)
                except:
                    print("Error: Email Not sending")  
                finally:  
                    messagebox.showinfo("Success", "Password changed successfully.")
                    frm.destroy()
                    home_screen()
                
        img=PhotoImage(file='forgot_otp_img.png')
        label_img = Label(frm, image=img, bg="white")
        label_img.image = img
        label_img.place(relx=.11,rely=.25)
        heading=Label(frm,text='Set Your Password', fg='#052c65',bg='white',font=('arial',23,'bold','underline'))
        heading.place(relx=.45,rely=.08)
        def on_enter(e):
            new_pass_entry.delete(0,'end')
        def on_leave(e):
            new_name=new_pass_entry.get()
            if new_name=='':
                new_pass_entry.insert(0,'New Password') 


        new_pass_entry=Entry(frm,font=('arial',11),bg='white',width=45,fg='black',border=0)
        new_pass_entry.insert(0,'New Password')
        new_pass_entry.bind('<FocusIn>',on_enter)
        new_pass_entry.bind('<FocusOut>',on_leave)
        new_pass_entry.place(relx=.45,rely=.22)

        Frame(frm,width=362,height=2,bg='black').place(relx=.45,rely=.26)
        def pass_clear():
            new_pass_entry.delete(0,"end")
        def toggle_password_visibility():
            global password_visible
            if 'password_visible' not in globals():
                password_visible = False
            if password_visible:
                new_pass_entry.config(show='*')
                password_visible = False
                btn_pass_img.config(image=show_img)
            else:
                new_pass_entry.config(show='')
                password_visible = True
                btn_pass_img.config(image=hide_img)

        password_visible = False
        show_img = PhotoImage(file='show_img.png').subsample(7, 7)
        hide_img = PhotoImage(file='hide.png').subsample(11, 11)

        btn_pass_img = Button(frm, image=show_img, bg="white", border=0, command=toggle_password_visibility)
        btn_pass_img.image = show_img
        btn_pass_img.place(relx=0.78, rely=0.22)
        
        def on_enter(e):
            con_pass_entry.delete(0,'end')
        def on_leave(e):
            con_name=con_pass_entry.get()
            if con_name=='':
                con_pass_entry.insert(0,'Confirm Password') 


        con_pass_entry=Entry(frm,font=('arial',11),bg='white',width=45,fg='black',border=0)
        con_pass_entry.insert(0,'Confirm Password')
        con_pass_entry.bind('<FocusIn>',on_enter)
        con_pass_entry.bind('<FocusOut>',on_leave)
        con_pass_entry.place(relx=.45,rely=.32)

        Frame(frm,width=362,height=2,bg='black').place(relx=.45,rely=.36)
        def pass_clear():
            con_pass_entry.delete(0,"end")
        def toggle_password_visibility():
            global password_visible
            if 'password_visible' not in globals():
                password_visible = False
            if password_visible:
                con_pass_entry.config(show='*')
                password_visible = False
                btn_con_pass_img.config(image=show_img)
            else:
                con_pass_entry.config(show='')
                password_visible = True
                btn_con_pass_img.config(image=hide_img)

        password_visible = False
        show_img = PhotoImage(file='show_img.png').subsample(7, 7)
        hide_img = PhotoImage(file='hide.png').subsample(11, 11)

        btn_con_pass_img = Button(frm, image=show_img, bg="white", border=0, command=toggle_password_visibility)
        btn_con_pass_img.image = show_img
        btn_con_pass_img.place(relx=0.78, rely=0.32)
        
        pass_dis_title_lbl=Label(frm,text='Password Must contain:',font=('arial',10,'bold'),bg='white',fg='#000')
        pass_dis_title_lbl.place(relx=.45,rely=.4)
        
        
        pass_dis_lbl1=Label(frm,text='Minimum of 8 Characters',font=('arial',10,'bold'),bg='white',fg='#000')
        pass_dis_lbl1.place(relx=.48,rely=.46)
            
        img=PhotoImage(file='correct.png')
        img = img.subsample(8, 8)
        label_img = Label(frm, image=img, bg="white")            
        label_img.image = img
        label_img.place(relx=.45,rely=.45)
            
        pass_dis_lbl2=Label(frm,text='At least one lowercase letter',font=('arial',10,'bold'),bg='white',fg='#000')
        pass_dis_lbl2.place(relx=.48,rely=.52)
        img=PhotoImage(file='correct.png')
        img = img.subsample(8, 8)
        label_img = Label(frm, image=img, bg="white")            
        label_img.image = img
        label_img.place(relx=.45,rely=.51)
            
            
        pass_dis_lbl3=Label(frm,text='At least one uppercase letter',font=('arial',10,'bold'),bg='white',fg='#000')
        pass_dis_lbl3.place(relx=.48,rely=.58)
        img=PhotoImage(file='correct.png')
        img = img.subsample(8, 8)
        label_img = Label(frm, image=img, bg="white")            
        label_img.image = img
        label_img.place(relx=.45,rely=.57)
        
        pass_dis_lbl=Label(frm,text='At least one number',font=('arial',10,'bold'),bg='white',fg='#000')
        pass_dis_lbl.place(relx=.48,rely=.64)            
        img=PhotoImage(file='correct.png')
        img = img.subsample(8, 8)
        label_img = Label(frm, image=img, bg="white")            
        label_img.image = img
        label_img.place(relx=.45,rely=.63)

        pass_dis_lbl=Label(frm,text='At least one special character',font=('arial',10,'bold'),bg='white',fg='#000')
        pass_dis_lbl.place(relx=.48,rely=.7)
        img=PhotoImage(file='correct.png')
        img = img.subsample(8, 8)
        label_img = Label(frm, image=img, bg="white")            
        label_img.image = img
        label_img.place(relx=.45,rely=.69)
        
        btn_reset=Button(frm,font=('arial',15,'bold'),text="Reset Password",bg='#28a745',fg='white',border=1,cursor="hand2",command=submit_pass_click)
        btn_reset.place(relx=.54,rely=.77)


def welcome_screen():
    frm=Frame(win) 
    frm.configure(bg="white")
    frm.place(relx=.0,rely=.2,relwidth=1,relheight=.8)
    def profile_screen():
        def welcome_click():
            frm.destroy()
            welcome_screen()
        def update_click():
            ifrm.destroy()
            update_screen()
        def password_change_click():
            ifrm.destroy()
            password_change_screen()
        def profile_image_update_click():
            ifrm.destroy()
            profile_image_update_screen()
        def email_update_click():
            ifrm.destroy()
            email_update_screen()
            
        def update_screen():
            ifrm=Frame(frm,highlightthickness=2,highlightbackground='black')
            ifrm.configure(bg="white")
            ifrm.place(relx=.1,rely=.13,relwidth=.82,relheight=.75)
            
            def clear():
                f_name_entry.delete(0,"end")
                l_name_entry.delete(0,"end")
                dob_entry.delete(0,"end")
                father_name_entry.delete(0,"end")
                mother_name_entry.delete(0,"end")
                mob_entry.delete(0,"end")
                nominee_name_entry.delete(0,"end")
                nominee_relation_entry.delete(0,"end")
                add_entry.delete(0,"end")
                add_entry2.delete(0,"end")
                pin_entry.delete(0,"end")
                city_entry.delete(0,"end")
                f_name_entry.focus()
                
            def update_profiles_db():
                f_name=f_name_entry.get()
                l_name=l_name_entry.get()
                dob=dob_entry.get()
                mob=mob_entry.get()
                father_name=father_name_entry.get()
                mother_name=mother_name_entry.get()
                nominee_name=nominee_name_entry.get()
                nominee_relation=nominee_relation_entry.get()
                add1=add_entry.get()
                add2=add_entry2.get()
                pin_code=pin_entry.get()
                city=city_entry.get()
                
                if  not f_name.isalpha() and not l_name.isalpha() and not father_name.isalpha() and not mother_name.isalpha() and not mob.isdigit() and not nominee_name.isalpha() and not nominee_relation.isalpha() and not pin_code.isdigit() and not city.isalpha():
                    Frame(ifrm,width=220,height=1,bg='green').place(relx=.2,rely=.16)
                    # error_f_name=Label(ifrm,font=('arial',8),bg='white',fg='red',border=0,text="Alphabets only no special characters & digits.")
                    # error_f_name.place(relx=.2,rely=17)
                    
                    
                    Frame(ifrm,width=220,height=1,bg='green').place(relx=.7,rely=.16)
                    # error_l_name=Label(ifrm,font=('arial',8),bg='white',fg='red',border=0,text="Alphabets only no special characters & digits.")
                    # error_l_name.place(relx=.7,rely=17)
                    
                    Frame(ifrm,width=220,height=1,bg='green').place(relx=.7,rely=.26)
                    # error_mob=Label(ifrm,font=('arial',8),bg='white',fg='red',border=0,text="Degits only no special characters & Alphabets.")
                    # error_mob.place(relx=.7,rely=27)
                    
                    Frame(ifrm,width=220,height=1,bg='green').place(relx=.2,rely=.36)
                    # error_father=Label(ifrm,font=('arial',8),bg='white',fg='red',border=0,text="Alphabets only no special characters & Degits.")
                    # error_father.place(relx=.2,rely=37)
                    
                    Frame(ifrm,width=220,height=1,bg='green').place(relx=.7,rely=.36)
                    # error_mother=Label(ifrm,font=('arial',8),bg='white',fg='red',border=0,text="Alphabets only no special characters & Degits.")
                    # error_mother.place(relx=.7,rely=37)
                    
                    Frame(ifrm,width=220,height=1,bg='green').place(relx=.2,rely=.46)
                    # error_nominee_name=Label(ifrm,font=('arial',8),bg='white',fg='red',border=0,text="Alphabets only no special characters & Degits.")
                    # error_nominee_name.place(relx=.2,rely=47)
                    
                    Frame(ifrm,width=220,height=1,bg='green').place(relx=.7,rely=.46)
                    # error_nominee_relation=Label(ifrm,font=('arial',8),bg='white',fg='red',border=0,text="Alphabets only no special characters & Degits.")
                    # error_nominee_relation.place(relx=.7,rely=47)
                    
                    Frame(ifrm,width=220,height=1,bg='green').place(relx=.2,rely=.66)
                    # error_pin=Label(ifrm,font=('arial',8),bg='white',fg='red',border=0,text="Degits only no special characters & Degits.")
                    # error_pin.place(relx=.2,rely=67)
                    
                    Frame(ifrm,width=220,height=1,bg='green').place(relx=.7,rely=.66)
                    # error_city=Label(ifrm,font=('arial',8),bg='white',fg='red',border=0,text="Alphabets only no special characters & Degits.")
                    # error_city.place(relx=.7,rely=67)
                    messagebox.showerror("Invalid","Invalid Input")
                    
                elif not f_name.isalpha():
                    Frame(ifrm,width=220,height=1,bg='red').place(relx=.2,rely=.16)
                    # error_f_name=Label(ifrm,text="Alphabets only no special characters & digits.",font=('arial',8),bg='white',fg='red',border=0)
                    # error_label = Label(ifrm, font=('arial', 8), bg='white', fg='red', border=0, text="message")
                    # error_label.place(relx=.2,rely=17)
                    messagebox.showerror("First Name","Alphabets only no special characters & digits.")
                
                elif not l_name.isalpha():
                    Frame(ifrm,width=220,height=1,bg='red').place(relx=.7,rely=.16)
                    # error_l_name=Label(ifrm,font=('arial',8),bg='white',fg='red',border=0,text="Alphabets only no special characters & digits.")
                    # error_l_name.place(relx=.7,rely=17)
                    messagebox.showerror("Last Name","Alphabets only no special characters & digits.")
                    
                elif not re.fullmatch("(0|91)?[6-9][0-9]{9}", mob):
                    Frame(ifrm,width=220,height=1,bg='red').place(relx=.7,rely=.26)
                    # error_mob=Label(ifrm,font=('arial',8),bg='white',fg='red',border=0,text="Invalid Mobile Number")
                    # error_mob.place(relx=.7,rely=27)
                    messagebox.showerror("First Name","Invalid Mobile Number.")
                    
                elif not father_name.isalpha():
                    Frame(ifrm,width=220,height=1,bg='red').place(relx=.2,rely=.36)
                    # error_father=Label(ifrm,font=('arial',8),bg='white',fg='red',border=0,text="Alphabets only no special characters & Degits.")
                    # error_father.place(relx=.2,rely=37)
                    messagebox.showerror("Father Name","Alphabets only no special characters & digits.")
                elif not mother_name.isalpha():
                    Frame(ifrm,width=220,height=1,bg='red').place(relx=.7,rely=.36)
                    # error_mother=Label(ifrm,font=('arial',8),bg='white',fg='red',border=0,text="Alphabets only no special characters & Degits.")
                    # error_mother.place(relx=.7,rely=37)
                    messagebox.showerror("Mother Name","Alphabets only no special characters & digits.")
                          
                elif not nominee_name.isalpha():
                    Frame(ifrm,width=220,height=1,bg='red').place(relx=.2,rely=.46)
                    # error_nominee_name=Label(ifrm,font=('arial',8),bg='white',fg='red',border=0,text="Alphabets only no special characters & Degits.")
                    # error_nominee_name.place(relx=.2,rely=47)
                    messagebox.showerror("Nominee Name","Alphabets only no special characters & digits.")
                    
                elif not nominee_relation.isalpha():
                    Frame(ifrm,width=220,height=1,bg='red').place(relx=.7,rely=.46)
                    # error_nominee_relation=Label(ifrm,font=('arial',8),bg='white',fg='red',border=0,text="Alphabets only no special characters & Degits.")
                    # error_nominee_relation.place(relx=.7,rely=47)
                    messagebox.showerror("Nominee Relation Name","Alphabets only no special characters & digits.")
                    
                elif len(pin_code)!=6:
                    Frame(ifrm,width=220,height=1,bg='red').place(relx=.2,rely=.66)
                    # error_pin=Label(ifrm,font=('arial',8),bg='white',fg='red',border=0,text="Invalid PinCode!")
                    # error_pin.place(relx=.2,rely=67)
                    messagebox.showerror("Pin Code","Invalid Pin Code")
                    
                elif not pin_code.isdigit():
                    Frame(ifrm,width=220,height=1,bg='red').place(relx=.2,rely=.66)
                    # error_pin=Label(ifrm,font=('arial',8),bg='white',fg='red',border=0,text="Degits only no special characters & Degits.")
                    # error_pin.place(relx=.2,rely=67)
                    messagebox.showerror("Pin Code","Alphabets only no special characters & digits.")
                elif not city.isalpha():
                    Frame(ifrm,width=220,height=1,bg='red').place(relx=.7,rely=.66)
                    messagebox.showerror("City","Alphabets only no special characters & digits.")
                else:
                    conobj=sqlite3.connect(database="banking.sqlite")
                    curobj=conobj.cursor()
                    curobj.execute("update user_details set first_name=?,last_name=?,dob=?,father_name=?,mother_name=?,mobile_no=?,nominee_name=?,nominee_relation=?,address_1=?,address_2=?,pin_code=?, city=?",(f_name,l_name,dob,father_name,mother_name,mob,nominee_name,nominee_relation,add1,add2,pin_code,city))
                    conobj.commit()
                    conobj.close()
                    
                    conobj=sqlite3.connect(database="banking.sqlite")
                    curobj=conobj.cursor()
                    curobj.execute("select email from user_details where user_id=?",(user_id,))
                    tup=curobj.fetchone()
                    conobj.close()
                    try:        
                        con = gmail.GMail("chaudharyshivam702@gmail.com", "")
                        otp_gen = gmail.Message(to=f"{tup[0]}", subject="profile updated successfully", text=f"Your profile updated successfully")
                        con.send(otp_gen)
                    except:
                        print("Failed to send") 
                    finally:   
                        messagebox.showinfo("Update Profile","Profile Updated")
                        frm.destroy()
                        welcome_screen()
            conobj=sqlite3.connect(database="banking.sqlite")
            curobj=conobj.cursor()
            curobj.execute("select * from user_details where user_id=?",(user_id,))
            tup=curobj.fetchone()
            conobj.close()        

            
            title_lbl=Label(ifrm,text='Update Profile',font=('arial',20,'bold'),bg='white',fg='purple')
            title_lbl.pack()
            f_name_lbl=Label(ifrm,font=('arial',16,'bold'),bg='white',fg='#000',border=0,text="First Name:")
            f_name_lbl.place(relx=.02,rely=.1)
            f_name_entry=Entry(ifrm,font=('arial',16),bg='white',border=0,width=18)
            f_name_entry.place(relx=.2,rely=.10)
            f_name_entry.insert(0,tup[2])
            # f_name_entry.focus()    
            Frame(ifrm,width=220,height=1,bg='black').place(relx=.2,rely=.16)
    
            l_name_lbl=Label(ifrm,font=('arial',16,'bold'),bg='white',fg='#000',border=0,text="Last Name:")
            l_name_lbl.place(relx=.5,rely=.1)
            l_name_entry=Entry(ifrm,font=('arial',16),bg='white',border=0,width=18)
            l_name_entry.place(relx=.7,rely=.10)
            l_name_entry.insert(0,tup[3])
            Frame(ifrm,width=220,height=1,bg='black').place(relx=.7,rely=.16)
    
            dob_lbl=Label(ifrm,font=('arial',16,'bold'),bg='white',fg='#000',border=0,text="Date of Birth:")
            dob_lbl.place(relx=.02,rely=.2)
            dob_entry=Entry(ifrm,font=('arial',16),bg='white',border=0,width=18)
            dob_entry.place(relx=.2,rely=.2)
            dob_entry.insert(0,tup[4])
            Frame(ifrm,width=220,height=1,bg='black').place(relx=.2,rely=.26)

            mob_lbl=Label(ifrm,font=('arial',16,'bold'),bg='white',fg='#000',border=0,text="Mobile Numabr:")
            mob_lbl.place(relx=.5, rely=.2)
            mob_entry=Entry(ifrm,font=('arial',16),bg='white',border=0,width=18)
            mob_entry.place(relx=.7,rely=.20)
            mob_entry.insert(0,tup[8])
            Frame(ifrm,width=220,height=1,bg='black').place(relx=.7,rely=.26)

            
            
            father_name_lbl=Label(ifrm,font=('arial',16,'bold'),bg='white',fg='#000',border=0,text="Father Name:")
            father_name_lbl.place(relx=.02,rely=.3)
            father_name_entry=Entry(ifrm,font=('arial',16),bg='white',border=0,width=18)
            father_name_entry.place(relx=.2,rely=.30)
            father_name_entry.insert(0,tup[6])
            Frame(ifrm,width=220,height=1,bg='black').place(relx=.2,rely=.36)

            mother_name_lbl=Label(ifrm,font=('arial',16,'bold'),bg='white',fg='#000',border=0,text="Mother Name:")
            mother_name_lbl.place(relx=.5,rely=.3)
            mother_name_entry=Entry(ifrm,font=('arial',16),bg='white',border=0,width=18)
            mother_name_entry.place(relx=.7,rely=.30)
            mother_name_entry.insert(0,tup[7])
            Frame(ifrm,width=220,height=1,bg='black').place(relx=.7,rely=.36)
            
            nominee_name_lbl=Label(ifrm,font=('arial',16,'bold'),bg='white',fg='#000',border=0,text="Nominee Name:")
            nominee_name_lbl.place(relx=.02, rely=.4)
            nominee_name_entry=Entry(ifrm,font=('arial',16),bg='white',border=0,width=18)
            nominee_name_entry.place(relx=.2,rely=.40)
            nominee_name_entry.insert(0,tup[12])
            Frame(ifrm,width=220,height=1,bg='black').place(relx=.2,rely=.46)

            

            nominee_relation_lbl=Label(ifrm,font=('arial',16,'bold'),bg='white',fg='#000',border=0,text="Nominee Relation:")
            nominee_relation_lbl.place(relx=.5,rely=.4)
            nominee_relation_entry=Entry(ifrm,font=('arial',16),bg='white',border=0,width=18)
            nominee_relation_entry.place(relx=.7,rely=.40)
            nominee_relation_entry.insert(0,tup[13])
            Frame(ifrm,width=220,height=1,bg='black').place(relx=.7,rely=.46)
            


            add_lbl=Label(ifrm,font=('arial',16,'bold'),bg='white',fg='#000',border=0,text="Address 1:")
            add_lbl.place(relx=.02,rely=.5)
            add_entry = Entry(ifrm,font=('arial',16),bg='white',border=0,width=18)
            add_entry.place(relx=.2, rely=.5)
            add_entry.insert(0,tup[14])
            Frame(ifrm,width=220,height=1,bg='black').place(relx=.2,rely=.56)
            
            
            add_lbl2=Label(ifrm,font=('arial',16,'bold'),bg='white',fg='#000',border=0,text="Address 2:")
            add_lbl2.place(relx=.5,rely=.5)
            add_entry2 = Entry(ifrm,font=('arial',16),bg='white',border=0,width=18)
            add_entry2.place(relx=.7, rely=.5)
            add_entry2.insert(0,tup[15])
            Frame(ifrm,width=220,height=1,bg='black').place(relx=.7,rely=.56)
            
            
            pin_lbl=Label(ifrm,font=('arial',16,'bold'),bg='white',fg='#000',border=0,text="Pin COde:")
            pin_lbl.place(relx=.02,rely=.6)
            pin_entry = Entry(ifrm,font=('arial',16),bg='white',border=0,width=18)
            pin_entry.place(relx=.2, rely=.6)
            pin_entry.insert(0,tup[16])
            Frame(ifrm,width=220,height=1,bg='black').place(relx=.2,rely=.66)
            
            
            city_lbl=Label(ifrm,font=('arial',16,'bold'),bg='white',fg='#000',border=0,text="City:")
            city_lbl.place(relx=.5,rely=.6)
            city_entry = Entry(ifrm,font=('arial',16),bg='white',border=0,width=18)
            city_entry.place(relx=.7, rely=.6)
            city_entry.insert(0,tup[17])
            Frame(ifrm,width=220,height=1,bg='black').place(relx=.7,rely=.66)
    
    
            btn_back=Button(frm,font=('arial',10,'bold'),text="Cancel",bg='#17a2b8',fg='white',width=15,border=1,cursor="hand2",command=welcome_click)
            btn_back.place(relx=.26,rely=.8)
            btn_create=Button(frm,font=('arial',10,'bold'),text="Update Profile",bg='#198754',fg='white',width=15,border=1,cursor="hand2",command=update_profiles_db)
            btn_create.place(relx=.38,rely=.8)
            btn_clear=Button(frm,font=('arial',10,'bold'),text="Clear",bg='#dc3545',fg='white',width=15,border=1,cursor="hand2",command=clear)
            btn_clear.place(relx=.5,rely=.8)
            
            
            
        
            
        def password_change_screen():
            ifrm=Frame(frm,highlightthickness=2,highlightbackground='black')
            ifrm.configure(bg="white")
            ifrm.place(relx=.1,rely=.13,relwidth=.82,relheight=.75)
        
            title_lbl=Label(ifrm,text='Password change',font=('arial',20,'bold'),bg='white',fg='purple')
            title_lbl.pack()
            dec_lbl=Label(ifrm,text='Please choose a new password',font=('arial',11,'bold'),bg='white',fg='Red')
            dec_lbl.place(relx=.02,rely=.09)
            
            def password_db():
                old_pass=old_pass_entry.get()
                new_pass=new_pass_entry.get()
                con_pass=con_pass_entry.get()
                
                conobj=sqlite3.connect(database='banking.sqlite')
                curobj=conobj.cursor()
                curobj.execute("SELECT password FROM user_details WHERE user_id=?",(user_id,))
                tup=curobj.fetchone()
                curobj.close()
                
                if len(old_pass)==0 and len(new_pass)==0 and len(con_pass)==0:
                    Frame(ifrm,width=220,height=1,bg='red').place(relx=.25,rely=.27)
                    old_pass_error=Label(ifrm,font=('arial',8),bg='white',fg='red',border=0,text="Empaty failed not allowed.")
                    old_pass_error.place(relx=.25,rely=.28)
                    
                    Frame(ifrm, width=220, height=1, bg='red').place(relx=.25, rely=.39)
                    error_pass_old = Label(ifrm, font=('arial', 8, 'bold'), bg='white', fg='red', border=0, text="Empaty failed not allowed.")
                    error_pass_old.place(relx=.25, rely=.4)
                    
                    Frame(ifrm,width=220,height=1,bg='black').place(relx=.25,rely=.51)
                    error_pass_match = Label(ifrm, font=('arial', 8), bg='white', fg='red', border=0, text="Empaty failed not allowed.")
                    error_pass_match.place(relx=.25, rely=.52)
                
                elif len(old_pass)==0:                    
                    Frame(ifrm,width=220,height=1,bg='red').place(relx=.25,rely=.27)
                    old_pass_error=Label(ifrm,font=('arial',8),bg='white',fg='red',border=0,text="Empaty failed not allowed.")
                    old_pass_error.place(relx=.25,rely=.28)
                elif len(new_pass)==0:  
                    Frame(ifrm, width=220, height=1, bg='red').place(relx=.25, rely=.39)
                    error_pass_old = Label(ifrm, font=('arial', 8, 'bold'), bg='white', fg='red', border=0, text="Empaty failed not allowed.")
                    error_pass_old.place(relx=.25, rely=.4)
                elif len(con_pass)==0:   
                    Frame(ifrm,width=220,height=1,bg='black').place(relx=.25,rely=.51)
                    error_pass_match = Label(ifrm, font=('arial', 8), bg='white', fg='red', border=0, text="Empaty failed not allowed.")
                    error_pass_match.place(relx=.25, rely=.52)  
                    
                elif len(new_pass)<8:
                    Frame(ifrm,width=220,height=1,bg='red').place(relx=.25,rely=.39)
                    error_pass = Label(ifrm, font=('arial', 8), bg='white', fg='red', border=0, text="Minimum of 8 Characters")
                    error_pass.place(relx=.25,rely=.4)
                elif not re.match("^[A-Z]",new_pass):
                    Frame(ifrm,width=220,height=1,bg='red').place(relx=.7,rely=.39)
                    error_pass = Label(ifrm, font=('arial', 8), bg='white', fg='red', border=0, text="uppercase letter at the beginning")
                    error_pass.place(relx=.25,rely=.4)
                elif not (any(c.isalpha() for c in new_pass) and any(c.isdigit() for c in new_pass)):
                    Frame(ifrm, width=220, height=1, bg='red').place(relx=.25, rely=.39)
                    error_pass = Label(ifrm, font=('arial', 8, 'bold'), bg='white', fg='red', border=0, text="At least one letter")
                    error_pass.place(relx=.25, rely=.4)
                elif old_pass==new_pass:
                    Frame(ifrm, width=220, height=1, bg='red').place(relx=.25, rely=.39)
                    error_pass_old = Label(ifrm, font=('arial', 8, 'bold'), bg='white', fg='red', border=0, text="Old Password and new Password is match")
                    error_pass_old.place(relx=.25, rely=.4)
                elif new_pass!=con_pass:
                    Frame(ifrm,width=220,height=1,bg='black').place(relx=.25,rely=.51)
                    error_pass_match = Label(ifrm, font=('arial', 8), bg='white', fg='red', border=0, text="Password is not match")
                    error_pass_match.place(relx=.25, rely=.52) 
                elif old_pass!=tup[0]:
                    Frame(ifrm,width=220,height=1,bg='red').place(relx=.25,rely=.27)
                    old_pass_error=Label(ifrm,font=('arial',8),bg='white',fg='red',border=0,text="Old Passwords Not Match")
                    old_pass_error.place(relx=.25,rely=.28)
                else:
                    conobj=sqlite3.connect(database="banking.sqlite")
                    curobj=conobj.cursor()
                    curobj.execute("UPDATE user_details SET password=? WHERE user_id=?", (new_pass, user_id))
                    conobj.commit()
                    conobj.close()
                    
                    conobj=sqlite3.connect(database="banking.sqlite")
                    curobj=conobj.cursor()
                    curobj.execute("select email from user_details where user_id=?",(user_id,))
                    tup=curobj.fetchone()
                    conobj.close()        
                    try:
                        con = gmail.GMail("chaudharyshivam702@gmail.com", "")
                        mail_gen_pass = gmail.Message(to=f"{tup[0]}", subject="Password change", text=f"Password Updated Successfully")
                        con.send(mail_gen_pass)
                    except:
                        print("Error: Email Not sending")  
                    finally:  
                        messagebox.showinfo("Success", "Password changed successfully.")
                        frm.destroy()
                        welcome_screen()
                
            
            def toggle_password_visibility():
                global password_visible
                if 'password_visible' not in globals():
                    password_visible = False
                if password_visible:
                    old_pass_entry.config(show='*')
                    password_visible = False
                    btn_old_pass_img.config(image=show_img)
                else:
                    old_pass_entry.config(show='')
                    password_visible = True
                    btn_old_pass_img.config(image=hide_img)
                
            password_visible = False
            show_img = PhotoImage(file='hide.png').subsample(11, 11)
            hide_img = PhotoImage(file='show_img.png').subsample(7, 7)

                       
            old_pass_lbl=Label(ifrm,font=('arial',16,'bold'),bg='white',fg='#000',border=0,text="Old Password:")
            old_pass_lbl.place(relx=.02,rely=.2)
            old_pass_entry=Entry(ifrm,font=('arial',16),bg='white',border=0,width=18,show="*")
            old_pass_entry.place(relx=.25,rely=.2)
            old_pass_entry.focus()
            Frame(ifrm,width=220,height=1,bg='black').place(relx=.25,rely=.27)
            btn_old_pass_img = Button(ifrm, image=show_img, bg="white", border=0, command=toggle_password_visibility)
            btn_old_pass_img.image = show_img
            btn_old_pass_img.place(relx=0.45, rely=0.21)
            
            def toggle_password_visibility():
                global password_visible
                if 'password_visible' not in globals():
                    password_visible = False
                if password_visible:
                    new_pass_entry.config(show='*')
                    password_visible = False
                    btn_new_img.config(image=show_img)
                else:
                    new_pass_entry.config(show='')
                    password_visible = True
                    btn_new_img.config(image=hide_img)
                
            password_visible = False
            show_img = PhotoImage(file='hide.png').subsample(11, 11)
            hide_img = PhotoImage(file='show_img.png').subsample(7, 7)
            
               
            new_pass_lbl=Label(ifrm,font=('arial',16,'bold'),bg='white',fg='#000',border=0,text="New Password:")
            new_pass_lbl.place(relx=.02,rely=.33)
            new_pass_entry=Entry(ifrm,font=('arial',16),bg='white',border=0,width=18,show="*")
            new_pass_entry.place(relx=.25,rely=.33)
            Frame(ifrm,width=220,height=1,bg='black').place(relx=.25,rely=.39)
            btn_new_img = Button(ifrm, image=show_img, bg="white", border=0, command=toggle_password_visibility)
            btn_new_img.image = show_img
            btn_new_img.place(relx=0.45, rely=0.33)
            
            def toggle_password_visibility():
                global password_visible
                if 'password_visible' not in globals():
                    password_visible = False
                if password_visible:
                    con_pass_entry.config(show='*')
                    password_visible = False
                    btn_con_img.config(image=show_img)
                else:
                    con_pass_entry.config(show='')
                    password_visible = True
                    btn_con_img.config(image=hide_img)
                
            password_visible = False
            show_img = PhotoImage(file='hide.png').subsample(11, 11)
            hide_img = PhotoImage(file='show_img.png').subsample(7, 7)
            
               
            con_pass_lbl=Label(ifrm,font=('arial',16,'bold'),bg='white',fg='#000',border=0,text="Confirm Passord:")
            con_pass_lbl.place(relx=.02,rely=.45)
            con_pass_entry=Entry(ifrm,font=('arial',16),bg='white',border=0,width=18,show="*")
            con_pass_entry.place(relx=.25,rely=.45)
            Frame(ifrm,width=220,height=1,bg='black').place(relx=.25,rely=.51)
            btn_con_img = Button(ifrm, image=show_img, bg="white", border=0, command=toggle_password_visibility)
            btn_con_img.image = show_img
            btn_con_img.place(relx=0.45, rely=0.45)
            
            
            pass_dis_title_lbl=Label(ifrm,text='Password Must contain:',font=('arial',10,'bold'),bg='white',fg='#000')
            pass_dis_title_lbl.place(relx=.61,rely=.14)
            img=PhotoImage(file='correct.png')
            img = img.subsample(8, 8)
            label_img = Label(ifrm, image=img, bg="white")            
            label_img.image = img
            label_img.place(relx=.6,rely=.2)
            
            pass_dis_lbl1=Label(ifrm,text='Minimum of 8 Characters',font=('arial',10,'bold'),bg='white',fg='#000')
            pass_dis_lbl1.place(relx=.64,rely=.21)
            
            img=PhotoImage(file='correct.png')
            img = img.subsample(8, 8)
            label_img = Label(ifrm, image=img, bg="white")            
            label_img.image = img
            label_img.place(relx=.6,rely=.3)
            
            pass_dis_lbl2=Label(ifrm,text='At least one lowercase letter',font=('arial',10,'bold'),bg='white',fg='#000')
            pass_dis_lbl2.place(relx=.64,rely=.31)
            img=PhotoImage(file='correct.png')
            img = img.subsample(8, 8)
            label_img = Label(ifrm, image=img, bg="white")            
            label_img.image = img
            label_img.place(relx=.6,rely=.4)
            
            
            pass_dis_lbl3=Label(ifrm,text='At least one uppercase letter',font=('arial',10,'bold'),bg='white',fg='#000')
            pass_dis_lbl3.place(relx=.64,rely=.41)
            img=PhotoImage(file='correct.png')
            img = img.subsample(8, 8)
            label_img = Label(ifrm, image=img, bg="white")            
            label_img.image = img
            label_img.place(relx=.6,rely=.5)
            pass_dis_lbl=Label(ifrm,text='At least one number',font=('arial',10,'bold'),bg='white',fg='#000')
            pass_dis_lbl.place(relx=.64,rely=.51)
            
            img=PhotoImage(file='correct.png')
            img = img.subsample(8, 8)
            label_img = Label(ifrm, image=img, bg="white")            
            label_img.image = img
            label_img.place(relx=.6,rely=.6)
            pass_dis_lbl=Label(ifrm,text='At least one special character',font=('arial',10,'bold'),bg='white',fg='#000')
            pass_dis_lbl.place(relx=.64,rely=.61)
            btn_back=Button(ifrm,font=('arial',10,'bold'),text="Cancel",bg='#17a2b8',fg='white',width=18,border=1,cursor="hand2",command=welcome_click)
            btn_back.place(relx=.2,rely=.7)
            btn_create=Button(ifrm,font=('arial',10,'bold'),text="Submit",bg='#198754',fg='white',width=18,border=1,cursor="hand2",command=password_db)
            btn_create.place(relx=.02,rely=.7)
        
        def profile_image_update_screen():
            ifrm=Frame(frm,highlightthickness=2,highlightbackground='black')
            ifrm.configure(bg="white")
            ifrm.place(relx=.3,rely=.13,relwidth=.4,relheight=.75)
            
            def welcome_click():
                ifrm.destroy()
                welcome_screen()
  
            img_upl_lbl=Label(ifrm,font=('arial',16,'bold','underline'),bg='white',fg='#000',border=0,text="Upload Image")
            img_upl_lbl.pack()
            
            Frame(ifrm,width=305,height=1,bg='black').place(relx=.2,rely=.15)
            Frame(ifrm,width=1,height=220,bg='black').place(relx=.2,rely=.15)
            Frame(ifrm,width=1,height=220,bg='black').place(relx=.8,rely=.15)
            Frame(ifrm,width=305,height=1,bg='black').place(relx=.2,rely=.68)
            
            uplaod_btn = Button(ifrm, text='Upload File', width=20, command=lambda: upload_file(),font=('arial',8,'bold','underline'))
            uplaod_btn.place(relx=.35,rely=.7)
            
            def upload_file():
                global img
                global update_filename
                f_types = [('Jpg Files', '*.jpg')]
                update_filename = filedialog.askopenfilename(filetypes=f_types)
                img = Image.open(update_filename)
                img = img.resize((202, 202), Image.LANCZOS)
                img = ImageTk.PhotoImage(img)
                b2 = Button(ifrm, image=img) 
                b2.place(relx=.3,rely=.16)
            
            def profile_image_update_db():
                try:
                    if update_filename:
                        with open(update_filename, "rb") as file:
                            image_data = file.read()
                            conobj=sqlite3.connect(database='banking.sqlite')
                            curobj=conobj.cursor()
                            curobj.execute("UPDATE user_details SET user_image=? where  user_id=?",(sqlite3.Binary(image_data),user_id))
                            conobj.commit()            
                            curobj.close()
                    messagebox.showinfo("User details updated", "Profile Image Updated  Successfully.")
                except:    
                    messagebox.showerror("Error", "Image update failed")
                finally:
                    frm.destroy()
                    welcome_screen()
                
            btn_sub=Button(ifrm,font=('arial',10,'bold'),text="Submit",bg='#17a2b8',fg='white',width=17,border=1,cursor="hand2",command=profile_image_update_db)
            btn_sub.place(relx=.2,rely=.8)
            btn_back=Button(ifrm,font=('arial',10,'bold'),text="Cancel",bg='#198754',fg='white',width=17,border=1,cursor="hand2",command=welcome_click)
            btn_back.place(relx=.52,rely=.8)

        def email_update_screen(): 
            ifrm=Frame(frm,highlightthickness=2,highlightbackground='black')
            ifrm.configure(bg="white")
            ifrm.place(relx=.3,rely=.13,relwidth=.4,relheight=.75)
            
            def welcome_click():
                ifrm.destroy()
                welcome_screen()
                
            conobj = sqlite3.connect(database="banking.sqlite")
            corobj = conobj.cursor()
            corobj.execute("SELECT email FROM user_details WHERE user_id=?",(user_id,))
            tup=corobj.fetchone()
            corobj.close()
                
            email_upl_lbl=Label(ifrm,font=('arial',16,'bold','underline'),bg='white',fg='#000',border=0,text="Change My Email")
            email_upl_lbl.pack()
            
            email_lbl=Label(ifrm,font=('arial',12,'bold'),bg='white',fg='#000',border=0,text="New Email")
            email_lbl.place(relx=.15,rely=.15)
            email_entry = Entry(ifrm,font=('arial',16),bg='white',border=1,width=25,show="*")
            email_entry.place(relx=.15, rely=.25)
            
            
            c_email_lbl=Label(ifrm,font=('arial',12,'bold'),bg='white',fg='#000',border=0,text="Confirm Email")
            c_email_lbl.place(relx=.15,rely=.37)
            c_email_entry = Entry(ifrm,font=('arial',16),bg='white',border=1,width=25)
            c_email_entry.place(relx=.15, rely=.45)
            
            c_email_tag=Label(ifrm,font=('arial',8,'bold'),bg='white',fg='#000',border=0,text="We need current otp to verify this update request")
            c_email_tag.place(relx=.15,rely=.53)
            
            def email_otp_generate():
                email=email_entry.get()
                c_email=c_email_entry.get()
                conobj = sqlite3.connect(database="banking.sqlite")
                corobj = conobj.cursor()
                corobj.execute("SELECT email,first_name,last_name FROM user_details WHERE user_id=?",(user_id,))
                tup=corobj.fetchone()
                corobj.close()
                if len(email)==0 and len(c_email)==0:
                    error_email_lbl=Label(ifrm,font=('arial',8,'bold'),bg='white',fg='red',border=0,text="Empty failed not allowed.")
                    error_email_lbl.place(relx=.15,rely=.32)
                    error_c_email_lbl=Label(ifrm,font=('arial',8,'bold'),bg='white',fg='red',border=0,text="Empty failed not allowed.")
                    error_c_email_lbl.place(relx=.15,rely=.52)
                elif len(email)==0:
                    error_email_lbl=Label(ifrm,font=('arial',8,'bold'),bg='white',fg='red',border=0,text="Empty failed not allowed.")
                    error_email_lbl.place(relx=.15,rely=.52)
                elif len(c_email)==0:
                    error_c_email_lbl=Label(ifrm,font=('arial',8,'bold'),bg='white',fg='red',border=0,text="Empty failed not allowed.")
                    error_c_email_lbl.place(relx=.15,rely=.52)
                elif c_email!=email:
                    error_c_email_lbl=Label(ifrm,font=('arial',8,'bold'),bg='white',fg='red',border=0,text="Email id not matching.")
                    error_c_email_lbl.place(relx=.15,rely=.52)                   
                elif not re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,3}\b',email):
                    # Frame(ifrm,width=220,height=1,bg='red').place(relx=.19,rely=.56)
                    error_email = Label(frm, font=('arial', 8, 'bold'), bg='white', fg='red', border=0, text="Invalid Email Id")
                    error_email.place(relx=.15,rely=.32)
                elif email==tup[0]:
                    error_email_lbl=Label(ifrm,font=('arial',8,'bold'),bg='white',fg='red',border=0,text="Old Email or New Email Match.")
                    error_email_lbl.place(relx=.15,rely=.32)
                else:
                    try:
                        old_email_otp = random.randint(100000, 999999)
                        con = gmail.GMail("chaudharyshivam702@gmail.com", "")
                        otp_gen = gmail.Message(to=f"{tup[0]}", subject="One Time Password (OTP) ", text=f"Dear {tup[1]} {tup[2]},\n\nYour One Time Password (OTP) for Email Update recovery on BANK is {old_email_otp}.\n\nPlease note, this OTP is valid only for mentioned transaction and cannot be used for any other transaction.\nPlease do not share this One Time Password with anyone.\n\n\nWarm Regards,\nCustomer Care\nBank.")
                        con.send(otp_gen)
                        
                        new_otp = random.randint(100000, 999999)
                        con = gmail.GMail("chaudharyshivam702@gmail.com", "")
                        otp_gent = gmail.Message(to=f"{email}", subject="One Time Password (OTP) ", text=f"Dear {tup[1]} {tup[2]},\n\nYour One Time Password (OTP) for Email Update recovery on BANK is {new_otp}.\n\nPlease note, this OTP is valid only for mentioned transaction and cannot be used for any other transaction.\nPlease do not share this One Time Password with anyone.\n\n\nWarm Regards,\nCustomer Care\nBank.")
                        con.send(otp_gent)
                        ifrm.destroy()
                        email_otp_screen(new_otp,old_email_otp,email)
                    except:
                        messagebox.showerror("Error","something went wrong please try again")
                        frm.destroy()
                        welcome_screen()
                        
                    
            
            
            
            btn_sub=Button(ifrm,font=('arial',10,'bold'),text="Submit",bg='#17a2b8',fg='white',width=17,border=1,cursor="hand2",command=email_otp_generate)
            btn_sub.place(relx=.2,rely=.8)
            btn_back=Button(ifrm,font=('arial',10,'bold'),text="Cancel",bg='#198754',fg='white',width=17,border=1,cursor="hand2",command=welcome_click)
            btn_back.place(relx=.52,rely=.8)
            
        def email_otp_screen(new_otp,old_email_otp,email):
            ifrm=Frame(frm,highlightthickness=2,highlightbackground='black')
            ifrm.configure(bg="white")
            ifrm.place(relx=.3,rely=.13,relwidth=.4,relheight=.75)
            
            
            conobj = sqlite3.connect(database="banking.sqlite")
            corobj = conobj.cursor()
            corobj.execute("SELECT email FROM user_details WHERE user_id=?",(user_id,))
            tup=corobj.fetchone()
            corobj.close()
            
            def welcome_click():
                ifrm.destroy()
                welcome_screen()
        
            #   1800100020240000
            def mask_email(email):
                username, domain = email.split('@')
                masked_username = username[:2] + '*'*(len(username)-4) + username[-2:]
                masked_email = masked_username + '@' + domain  
                return masked_email
            heading=Label(ifrm,text='Update Your Email', fg='#052c65',bg='white',font=('arial',23,'bold','underline'))
            heading.pack()
            inf_details=Label(ifrm,text='We have just sent 6 digit OTP to your Old email ID', fg='#000',bg='white',font=('arial',10,'bold'))
            inf_details.place(relx=.1,rely=.15)
            
            inf_email=Label(ifrm,text=f'Registered id: {mask_email(tup[0])}', fg='#000',bg='white',font=('arial',10,'bold'))
            inf_email.place(relx=.1,rely=.23)
            
            inf_email_proc=Label(ifrm,text='Enter that code hear to proceed', fg='#000',bg='white',font=('arial',10,'bold'))
            inf_email_proc.place(relx=.1,rely=.30)
                    
        
            def handle_key_release(event):
                entry_widget = event.widget
                entry_str = entry_widget.get()
                entry_str = ''.join(char for char in entry_str if char.isdigit())
                entry_widget.delete(0, END)
                entry_widget.insert(0, entry_str)
                if entry_str and event.char.isdigit():
                    entry_widget.tk_focusNext().focus()
            otp_entries = []
            for i in range(6):
                otp_entry = Entry(ifrm, font=('arial', 18), bg='white', border=1, width=3)
                otp_entry.place(relx=0.1 + i * 0.1, rely=0.37, relheight=0.08)
                otp_entry.bind('<KeyRelease>', handle_key_release)
                Frame(ifrm, width=43, height=1, bg='black').place(relx=0.1 + i * 0.1, rely=0.45)
                otp_entries.append(otp_entry)
                otp_entries[0].focus()
                
            new_inf_details=Label(ifrm,text='We have just sent 6 digit OTP to your New email ID', fg='#000',bg='white',font=('arial',10,'bold'))
            new_inf_details.place(relx=.1,rely=.5)
            
            new_inf_email=Label(ifrm,text=f'Registered id: {mask_email(email)}', fg='#000',bg='white',font=('arial',10,'bold'))
            new_inf_email.place(relx=.1,rely=.57)
            
            new_inf_email_proc=Label(ifrm,text='Enter that code hear to proceed', fg='#000',bg='white',font=('arial',10,'bold'))
            new_inf_email_proc.place(relx=.1,rely=.64)
                    
        
            new_otp_entries = []
            for i in range(6):
                otp_entry = Entry(ifrm, font=('arial', 18), bg='white', border=1, width=3)
                otp_entry.place(relx=0.1 + i * 0.1, rely=0.7, relheight=0.08)
                otp_entry.bind('<KeyRelease>', handle_key_release)
                Frame(ifrm, width=40, height=1, bg='black').place(relx=0.1 + i * 0.1, rely=0.77)
                new_otp_entries.append(otp_entry)
                # new_otp_entries[0].focus()
                
            def submit_otp():
                otp_input = "".join(entry.get() for entry in otp_entries)
                print(type(otp_input),otp_input)
                otp_input_new = "".join(entry.get() for entry in new_otp_entries)
                print(type(otp_input_new),otp_input_new)
                if verify_otp(int(otp_input), old_email_otp) and verify_otp(int(otp_input_new), new_otp):
                    
                    conobj = sqlite3.connect(database="banking.sqlite")
                    corobj = conobj.cursor()
                    corobj.execute("update user_details set email=? WHERE user_id=?",(email,user_id,))
                    conobj.commit()
                    corobj.close()
                    messagebox.showinfo("User Email updated","Email updated successfully.")
                    frm.destroy()
                    welcome_screen()                    
                    
                else:
                    
                    messagebox.showwarning("Invalid otp","Invalid otp please try again.")
                
            
            btn_sub=Button(ifrm,font=('arial',10,'bold'),text="Submit",bg='#17a2b8',fg='white',width=17,border=1,cursor="hand2",command=submit_otp)
            btn_sub.place(relx=.2,rely=.8)
            btn_back=Button(ifrm,font=('arial',10,'bold'),text="Cancel",bg='#198754',fg='white',width=17,border=1,cursor="hand2",command=welcome_click)
            btn_back.place(relx=.52,rely=.8)
        
    
    
    
        ifrm=Frame(frm) 
        ifrm.configure(bg="white")
        ifrm.place(relx=.8,rely=0.07,relwidth=0.12,relheight=.25)
        
        
        btn_profile=Button(ifrm,width=15,font=('arial',8,'bold','underline'),text="Profile Setting",fg='black',border=1,cursor="hand2",command=update_click)
        btn_profile.place(relx=0.12,rely=0.02)    
        
        btn_profile_pass=Button(ifrm,width=15,font=('arial',8,'bold','underline'),text="Password Change",fg='black',border=1,cursor="hand2",command=password_change_click)
        btn_profile_pass.place(relx=0.12,rely=0.23)
        
        btn_profile_img=Button(ifrm,width=15,font=('arial',8,'bold','underline'),text="Image Update",fg='black',border=1,cursor="hand2",command=profile_image_update_click)
        btn_profile_img.place(relx=0.12,rely=0.43)
        
        btn_profile_email=Button(ifrm,width=15,font=('arial',8,'bold','underline'),text="Email Update",fg='black',border=1,cursor="hand2",command=email_update_click)
        btn_profile_email.place(relx=0.12,rely=0.61)
        
        img=PhotoImage(file='cancle.png')
        img = img.subsample(8, 8)
        btn_can_img = Button(ifrm, image=img, bg="white", border=1,command=welcome_click)
        btn_can_img.image = img
        btn_can_img.place(relx=0.12, rely=0.82)
        btn_can_back=Button(ifrm,font=('arial',9,'bold','underline'),text="Cancel",cursor='hand2',fg='black',width=12,border=0,command=welcome_click)
        btn_can_back.place(relx=0.26,rely=0.82)  
        
         
       
    def profile_click():
        frm.destroy()
        profile_screen()
    
    
    def logout_click():
        res=messagebox.askquestion("Logout","Do you want to exit from application?")
        if res=='yes':
            frm.destroy()
            # ifrm.destroy()
            home_screen()
            
            
    conn = sqlite3.connect("banking.sqlite")
    cursor = conn.cursor()
    cursor.execute("SELECT user_image FROM user_details WHERE user_id = ?",(user_id,))
    row = cursor.fetchone()
    image_data = row[0]
    try:
        image = Image.open(io.BytesIO(image_data))
        image = image.resize((20, 20), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
    except Exception as e:  
        
        print("Error loading image:", e)
        photo = PhotoImage(file='images.png').subsample(7,7)
        

    btn_profile_img = Button(frm, image=photo, bg="white", border=1, command=profile_screen)
    btn_profile_img.image = photo  
    btn_profile_img.place(relx=0.829, rely=0.01)

    conn.close()

          
    
    
    
    
    btn_back=Button(frm,font=('arial',12,'bold','underline'),text=f"{user_first_name}",bg='white',cursor='hand2',fg='#0d6efd',width=5,border=0,command=profile_screen)
    btn_back.place(relx=0.85,rely=0.01)
    
    img=PhotoImage(file='logout.png')
    img = img.subsample(10, 10)
    btn_log_img = Button(frm, image=img, bg="white", border=1,command=logout_click)
    btn_log_img.image = img
    btn_log_img.place(relx=0.9, rely=0.01)
    btn_back=Button(frm,font=('arial',12,'bold','underline'),text="Logout",bg='white',cursor='hand2',fg='#0d6efd',width=6,border=0,command=logout_click)
    btn_back.place(relx=0.92,rely=0.01)

    
    img=PhotoImage(file='bank.png')
    img = img.subsample(1, 1)
    label_img = Label(frm, image=img, bg="white")
    label_img.image = img
    label_img.place(relx=0.2,rely=.06)
    # btn_back=Button(frm,font=('arial',20,'bold'),text="Update Profile",bg='#6c757d',cursor='hand2',fg='white',width=15,border=0,command=home_click)
    # btn_back.place(relx=0.82,rely=0.1)
    def balance_screen():
        ifrm=Frame(frm,highlightthickness=2,highlightbackground='black')
        ifrm.configure(bg='#d5d4fe')
        ifrm.place(relx=.1,rely=.13,relwidth=.82,relheight=.75)
        def welcome_click():
            frm.destroy()
            welcome_screen()
            
        conobj=sqlite3.connect(database="banking.sqlite")
        curobj=conobj.cursor()
        curobj.execute("select balance from user_details where user_id=?",(user_id,))
        tup=curobj.fetchone()
        conobj.close()
        title_lbl=Label(ifrm,text='Check balance',font=('arial',20,'bold'),bg='#d5d4fe',fg='purple')
        title_lbl.pack()
        
        img=PhotoImage(file='Check_balance.png').subsample(2,2)
        label_img = Label(ifrm, image=img, bg="#d5d4fe")
        label_img.image = img
        label_img.place(relx=.04,rely=.04)
        
        lable=Label(ifrm,text="Availabel Balance",fg='#000',bg='#d5d4fe',font=('arial',23,'bold'))
        lable.place(relx=.43,rely=.19)
        lable=Label(ifrm,text=f"{tup[0]}",fg='#000',bg='#d5d4fe',font=('arial',50,'bold','underline'))
        lable.place(relx=.4,rely=.3)
        
        btn_can_back=Button(ifrm,font=('arial',20,'bold','underline'),bg="#d5d4fe",text="Cancel",cursor='hand2',fg='#0d6efd',width=8,border=0,command=welcome_click)
        btn_can_back.place(relx=0.47,rely=0.55)
        
    def deposit_screen():
        ifrm=Frame(frm,highlightthickness=2,highlightbackground='black')
        ifrm.configure(bg="#d5d4fe")
        ifrm.place(relx=.1,rely=.13,relwidth=.82,relheight=.75)
        
        def deposit_db():
            amt = float(dep_entry.get())
            
            try:
                conobj = sqlite3.connect(database="banking.sqlite")
                curobj = conobj.cursor()        
                curobj.execute("SELECT balance,email,first_name,last_name,account_no FROM user_details WHERE user_id=?", (user_id,))
                tup = curobj.fetchone()
                if tup is not None:
                    bal = tup[0]
                else:
                    bal = 0                
                if bal is not None:  
                    curobj.execute("INSERT INTO txns (user_id, txn_amt, txn_type, txn_update_bal, txn_date) VALUES (?, ?, ?, ?, ?)",
                                (user_id, amt, 'Credit Amount', bal + amt, time.ctime()))
                else:
                    curobj.execute("INSERT INTO txns (user_id, txn_amt, txn_type, txn_update_bal, txn_date) VALUES (?, ?, ?, ?, ?)",
                                (user_id, amt, 'Credit Amount', amt, time.ctime()))
                curobj.execute("UPDATE user_details SET balance = balance + ? WHERE user_id=?", (amt, user_id))
                conobj.commit()
                
                try:     
                    curobj.execute("SELECT txns_id FROM txns WHERE user_id=? ORDER by txns_id desc", (user_id,))
                    txn_id = curobj.fetchone()
                    con = gmail.GMail("chaudharyshivam702@gmail.com", "")
                    mail_gen = gmail.Message(to=f"{tup[1]}", subject="Credit Amount", text=f" Dear {tup[2]} {tup[3]}\n\nRs. {amt} credits to a/c{mask_account_number(tup[4])} on {time.ctime()} transaction id {txn_id[0]} \n\n\n Warm Regard\nCustomer Care\nBank.")
                    con.send(mail_gen)
                except:
                    print("Error sending")
                finally:
                    messagebox.showinfo("Deposit Amt", f"{amt} deposited ")
                
            except sqlite3.Error as e:
                print("SQLite Error:", e)
            finally:
                if curobj:
                    curobj.close()
                if conobj:
                    conobj.close()
            

        
        img=PhotoImage(file='Check_balance.png').subsample(2,2)
        label_img = Label(ifrm, image=img, bg="#d5d4fe")
        label_img.image = img
        label_img.place(relx=.04,rely=.04)
        def welcome_click():
            frm.destroy()
            welcome_screen()
        
        title_lbl=Label(ifrm,text='Deposit Balance',font=('arial',20,'bold'),bg='#d5d4fe',fg='purple')
        title_lbl.pack()
        dep_lbl=Label(ifrm,font=('arial',20,'bold'),bg='#d5d4fe',fg='#000',border=0,text="Amount")
        dep_lbl.place(relx=.54,rely=.19)
        dep_entry=Entry(ifrm,font=('arial',40),bg='white',border=0,width=13)
        dep_entry.place(relx=.4,rely=.4)
        Frame(ifrm,width=380,height=1,bg='black').place(relx=.4,rely=.55)
        btn_deposit=Button(ifrm,font=('arial',20,'bold','underline'),text="Submit",cursor='hand2',bg="#d5d4fe",fg='#0d6efd',width=8,border=0,command=deposit_db)
        btn_deposit.place(relx=0.4,rely=0.6)
        
        btn_can_back=Button(ifrm,font=('arial',20,'bold',"underline"),text="Cancel",cursor='hand2',fg='#0d6efd',bg="#d5d4fe",width=8,border=0,command=welcome_click)
        btn_can_back.place(relx=0.63,rely=0.6)
        
    def withdraw_screen():
        ifrm=Frame(frm,highlightthickness=2,highlightbackground='black')
        ifrm.configure(bg="#d5d4fe")
        ifrm.place(relx=.1,rely=.13,relwidth=.82,relheight=.75)
        
        img=PhotoImage(file='Check_balance.png').subsample(2,2)
        label_img = Label(ifrm, image=img, bg="#d5d4fe")
        label_img.image = img
        label_img.place(relx=.04,rely=.04)
        def welcome_click():
            frm.destroy()
            welcome_screen()
        def withdraw_db():
            amt=float(wit_entry.get())
            conobj=sqlite3.connect(database="banking.sqlite")
            curobj=conobj.cursor()
            curobj.execute("select balance, email,first_name,last_name,account_no from user_details where user_id=?",(user_id,))
            tup=curobj.fetchone()
            bal=tup[0]
            curobj.close()
            if bal>=amt:
                curobj=conobj.cursor()
                curobj.execute("INSERT INTO txns (user_id, txn_amt, txn_type, txn_update_bal, txn_date) VALUES (?, ?, ?, ?, ?)",
                                (user_id, amt, 'Debit Amount', bal-amt, time.ctime()))
                curobj.execute("UPDATE user_details SET balance = balance - ? WHERE user_id=?", (amt, user_id))
                conobj.commit()
                conobj.close()
                try:
                    conobj=sqlite3.connect(database="banking.sqlite")
                    curobj=conobj.cursor()
                    curobj.execute("SELECT txns_id FROM txns WHERE user_id=? ORDER by txns_id desc", (user_id,))
                    txn_id = curobj.fetchone()
                    con = gmail.GMail("chaudharyshivam702@gmail.com", "")
                    # mail_gen = gmail.Message(to=f"{tup[1]}", subject="Debit  Amount", text=f" {amt}")
                    mail_gen = gmail.Message(to=f"{tup[1]}", subject="Debit Amount", text=f" Dear {tup[2]} {tup[3]}\n\nAmt withdraw Rs. {amt} from Bank A/C{mask_account_number(tup[4])} on {time.ctime()} transaction id {txn_id[0]} \n\n\n Warm Regard\nCustomer Care\nBank.")
                    con.send(mail_gen)   
                except:
                    print("Error") 
                finally:
                    messagebox.showinfo("Withdraw Amt",f"{amt} withdrawn ")
            else:
                messagebox.showinfo("Withdraw Amt","Insufficient Bal")
        
        title_lbl=Label(ifrm,text='Withdrwal Balance',font=('arial',20,'bold'),bg='#d5d4fe',fg='purple')
        title_lbl.pack()
        wit_lbl=Label(ifrm,font=('arial',20,'bold'),bg='#d5d4fe',fg='#000',border=0,text="Amount")
        wit_lbl.place(relx=.54,rely=.19)
        wit_entry=Entry(ifrm,font=('arial',40),bg='white',border=0,width=13)
        wit_entry.place(relx=.4,rely=.4)
        Frame(ifrm,width=380,height=1,bg='black').place(relx=.4,rely=.55)
        btn_withdraw=Button(ifrm,font=('arial',20,'bold','underline'),text="Submit",cursor='hand2',bg="#d5d4fe",fg='#0d6efd',width=8,border=0,command=withdraw_db)
        btn_withdraw.place(relx=0.4,rely=0.6)
        
        btn_can_back=Button(ifrm,font=('arial',20,'bold',"underline"),text="Cancel",cursor='hand2',fg='#0d6efd',bg="#d5d4fe",width=8,border=0,command=welcome_click)
        btn_can_back.place(relx=0.63,rely=0.6)
    def mini_statement_screen():
        ifrm=Frame(frm,highlightthickness=2,highlightbackground='black')
        ifrm.configure(bg="#d5d4fe")
        # ifrm.place(relx=.1,rely=.13)
        ifrm.place(relx=.1,rely=.13,relwidth=.82,relheight=.75)
        
        
        
        def welcome_click():
            frm.destroy()
            welcome_screen()
        def all_txan():
            tv=Treeview(ifrm)
            tv.place(relx=0,rely=0.13,relheight=0.76,relwidth=1)
            
            style = Style()
            style.configure("Treeview.Heading", font=('Arial',15,'bold'),background='#d5d4fe',froground='#d5d4fe')
            sb=Scrollbar(ifrm,orient='vertical',command=tv.yview)
            sb.place(relx=.98,rely=0.13,relheight=0.76)
            
            tv['columns']=('Txn date','Txn amount','Txn type','Updated bal')
            
            tv.column('Txn date',width=150,anchor='c')
            tv.column('Txn amount',width=100,anchor='c')
            tv.column('Txn type',width=100,anchor='c')
            tv.column('Updated bal',width=100,anchor='c')

            tv.heading('Txn date',text='Txn date')
            tv.heading('Txn amount',text='Txn amount')
            tv.heading('Txn type',text='Txn type')
            tv.heading('Updated bal',text='Updated bal')
            
            tv['show']='headings'
            con=sqlite3.connect(database="banking.sqlite")
            cur=con.cursor()
            cur.execute("select txn_date,txn_amt,txn_type,txn_update_bal from txns where user_id=? order by txn_date desc",(user_id,))
            for row in cur:
                tv.insert("","end",values=(row[0],row[1],row[2],row[3]),tags='ft')
                tv.tag_configure('ft',font=('',12))
            con.close()
        def credits():
            tv=Treeview(ifrm)
            tv.place(relx=0,rely=0.13,relheight=0.76,relwidth=1)
            
            style = Style()
            style.configure("Treeview.Heading", font=('Arial',15,'bold'),background='#d5d4fe',froground='#d5d4fe')
            sb=Scrollbar(ifrm,orient='vertical',command=tv.yview)
            sb.place(relx=.98,rely=0.13,relheight=0.76)
            
            tv['columns']=('Txn date','Txn amount','Txn type','Updated bal')
            
            tv.column('Txn date',width=150,anchor='c')
            tv.column('Txn amount',width=100,anchor='c')
            tv.column('Txn type',width=100,anchor='c')
            tv.column('Updated bal',width=100,anchor='c')

            tv.heading('Txn date',text='Txn date')
            tv.heading('Txn amount',text='Txn amount')
            tv.heading('Txn type',text='Txn type')
            tv.heading('Updated bal',text='Updated bal')
            
            tv['show']='headings'
            con=sqlite3.connect(database="banking.sqlite")
            cur=con.cursor()
            cur.execute("select txn_date,txn_amt,txn_type,txn_update_bal from txns where user_id=? and txn_type=? order by txn_date desc",(user_id,'Credit Amount'))
            for row in cur:
                tv.insert("","end",values=(row[0],row[1],row[2],row[3]),tags='ft')
                tv.tag_configure('ft',font=('',12))
            con.close()
        def debits():
            
            tv=Treeview(ifrm)
            tv.place(relx=0,rely=0.13,relheight=0.76,relwidth=1)
            
            style = Style()
            style.configure("Treeview.Heading", font=('Arial',15,'bold'),background='#d5d4fe',froground='#d5d4fe')
            sb=Scrollbar(ifrm,orient='vertical',command=tv.yview)
            sb.place(relx=.98,rely=0.13,relheight=0.76)
            
            tv['columns']=('Txn date','Txn amount','Txn type','Updated bal')
            
            tv.column('Txn date',width=150,anchor='c')
            tv.column('Txn amount',width=100,anchor='c')
            tv.column('Txn type',width=100,anchor='c')
            tv.column('Updated bal',width=100,anchor='c')

            tv.heading('Txn date',text='Txn date')
            tv.heading('Txn amount',text='Txn amount')
            tv.heading('Txn type',text='Txn type')
            tv.heading('Updated bal',text='Updated bal')
            
            tv['show']='headings'
            con=sqlite3.connect(database="banking.sqlite")
            cur=con.cursor()
            cur.execute("select txn_date,txn_amt,txn_type,txn_update_bal from txns where user_id=? and txn_type=? order by txn_date desc",(user_id,'Debit Amount'))
            for row in cur:
                tv.insert("","end",values=(row[0],row[1],row[2],row[3]),tags='ft')
                tv.tag_configure('ft',font=('',12))
            con.close()
        def transfers():
            tv=Treeview(ifrm)
            tv.place(relx=0,rely=0.13,relheight=0.76,relwidth=1)
            
            style = Style()
            style.configure("Treeview.Heading", font=('Arial',15,'bold'),background='#d5d4fe',froground='#d5d4fe')
            sb=Scrollbar(ifrm,orient='vertical',command=tv.yview)
            sb.place(relx=.98,rely=0.13,relheight=0.76)
            
            tv['columns']=('Txn date','Txn amount','Txn type','Updated bal')
            
            tv.column('Txn date',width=150,anchor='c')
            tv.column('Txn amount',width=100,anchor='c')
            tv.column('Txn type',width=100,anchor='c')
            tv.column('Updated bal',width=100,anchor='c')

            tv.heading('Txn date',text='Txn date')
            tv.heading('Txn amount',text='Txn amount')
            tv.heading('Txn type',text='Txn type')
            tv.heading('Updated bal',text='Updated bal')
            
            tv['show']='headings'
            con=sqlite3.connect(database="banking.sqlite")
            cur=con.cursor()
            cur.execute("select txn_date,txn_amt,txn_type,txn_update_bal from txns where user_id=? and txn_type=? order by txn_date desc",(user_id,'Transfer Amount'))
            for row in cur:
                tv.insert("","end",values=(row[0],row[1],row[2],row[3]),tags='ft')
                tv.tag_configure('ft',font=('',12))
            con.close()
        
        
        title_lbl=Label(ifrm,text='Transaction History',font=('arial',20,'bold','underline'),bg='#d5d4fe',fg='purple')
        title_lbl.pack()
        
        btn_all=Button(ifrm,font=('arial',10,'bold'),text="All",cursor='hand2',bg='#17a2b8',fg='White',width=8,border=0,command=all_txan)
        btn_all.place(relx=.01,rely=0.08)
        btn_cradit=Button(ifrm,font=('arial',10,'bold'),text="Credit",cursor='hand2',bg='#007bff',fg='white',width=8,border=0,command=credits)
        btn_cradit.place(relx=0.08,rely=0.08)
        btn_deposit=Button(ifrm,font=('arial',10,'bold'),text="Debit",cursor='hand2',bg='#007bff',fg='white',width=8,border=0,command=debits)
        btn_deposit.place(relx=0.15,rely=0.08)
        btn_transfer=Button(ifrm,font=('arial',10,'bold'),text="Transfer",cursor='hand2',bg='#007bff',fg='White',width=8,border=0,command=transfers)
        btn_transfer.place(relx=0.22,rely=0.08)
        
        tv=Treeview(ifrm)
        tv.place(relx=0,rely=0.13,relheight=0.76,relwidth=1)
        
        style = Style()
        style.configure("Treeview.Heading", font=('Arial',15,'bold'),background='#d5d4fe',froground='#d5d4fe')
        sb=Scrollbar(ifrm,orient='vertical',command=tv.yview)
        sb.place(relx=.98,rely=0.13,relheight=0.76)
        
        tv['columns']=('Txn date','Txn amount','Txn type','Updated bal')
        
        tv.column('Txn date',width=150,anchor='c')
        tv.column('Txn amount',width=100,anchor='c')
        tv.column('Txn type',width=100,anchor='c')
        tv.column('Updated bal',width=100,anchor='c')

        tv.heading('Txn date',text='Txn date')
        tv.heading('Txn amount',text='Txn amount')
        tv.heading('Txn type',text='Txn type')
        tv.heading('Updated bal',text='Updated bal')
        
        tv['show']='headings'

        con=sqlite3.connect(database="banking.sqlite")
        cur=con.cursor()
        cur.execute("select txn_date,txn_amt,txn_type,txn_update_bal from txns where user_id=? order by txn_date desc",(user_id,))
        for row in cur:
            tv.insert("","end",values=(row[0],row[1],row[2],row[3]),tags='ft')
            tv.tag_configure('ft',font=('',12))
        con.close()
        
        btn_can_back=Button(ifrm,font=('arial',14,'bold'),text="Cancel",cursor='hand2',fg='White',width=8,border=0,bg='#28a745',command=welcome_click)
        btn_can_back.place(relx=0.85,rely=0.88) 
        
    def transfer_screen():
        ifrm=Frame(frm,highlightthickness=2,highlightbackground='black')
        ifrm.configure(bg="#d5d4fe")
        ifrm.place(relx=.1,rely=.13,relwidth=.82,relheight=.75)
        
        
        
        def transfer_db():
            get_amt=tfr_amo_entry.get()
            amt=float(get_amt)
            print(type(amt))
            txan_acc=tfr_acn_entry.get()
            txan_con_acc=tfr_con_acn_entry.get()
            print(txan_acc, txan_con_acc)
            print(type(txan_acc), type(txan_con_acc), type(amt))
            
            if len(txan_acc)==0:
                Frame(ifrm,width=218,height=1,bg='red').place(relx=.58,rely=.31)
                error_acn_lbl=Label(ifrm,font=('arial',8,'bold'),bg='#d5d4fe',fg='red',border=0,text="Empty field not allowed")
                error_acn_lbl.place(relx=.58,rely=.32)
            elif txan_acc != txan_con_acc:
                Frame(ifrm,width=218,height=1,bg='red').place(relx=.58,rely=.41)
                error_con_acn_lbl=Label(ifrm,font=('arial',8,'bold'),bg='#d5d4fe',fg='red',border=0,text="Account Number Not Match")
                error_con_acn_lbl.place(relx=.58,rely=.42)
            else:
                conobj=sqlite3.connect(database="banking.sqlite")
                curobj=conobj.cursor()
                curobj.execute("select balance,email from user_details where user_id=?",(user_id,))
                tup_fr=curobj.fetchone()
                bal_frm=tup_fr[0]
                curobj.close()

                curobj=conobj.cursor()
                curobj.execute("select balance, email,user_id from user_details where account_no=?",(txan_acc,))
                tup_to=curobj.fetchone()
                bal_to=tup_to[0]
                curobj.close()
                

                curobj=conobj.cursor()
                curobj.execute("select account_no from user_details where account_no=?",(txan_acc,))
                tup=curobj.fetchone()
                curobj.close()
                if tup==None:
                    messagebox.showerror("Transfer",f"To ACN {txan_acc} does not exist !")
                else:
                    if bal_frm>=amt:
                        curobj=conobj.cursor()
                        curobj.execute("update user_details set balance=balance-? where user_id=?",(amt,user_id))
                        curobj.execute("update user_details set balance=balance+? where account_no=?",(amt,txan_acc))
                        curobj.execute("INSERT INTO txns (user_id, txn_amt, txn_type, txn_update_bal, txn_date) VALUES (?, ?, ?, ?, ?)",
                                (user_id, amt, 'Transfer Amount', bal_frm-amt, time.ctime()))
                        curobj.execute("INSERT INTO txns (user_id, txn_amt, txn_type, txn_update_bal, txn_date) VALUES (?, ?, ?, ?, ?)",
                                (tup_to[2], amt, 'Credit Amount', bal_to+amt, time.ctime()))
                        conobj.commit()
                        conobj.close()
                        con = gmail.GMail("chaudharyshivam702@gmail.com", "")
                        mail_gen = gmail.Message(to=f"{tup_fr[1]}", subject="Transfer Amount", text=f" {amt}")
                        con.send(mail_gen)
                        con = gmail.GMail("chaudharyshivam702@gmail.com", "")
                        mail_gen = gmail.Message(to=f"{tup_to[1]}", subject="Credit sdAmount", text=f"{amt}")
                        con.send(mail_gen)  
                        messagebox.showinfo("Transfer Amt",f"{amt} transfered to ACN {txan_acc} ")
                    else:
                        messagebox.showwarning("Withdraw Amt","Insufficient Bal")
       
        
        img=PhotoImage(file='Check_balance.png').subsample(2,2)
        label_img = Label(ifrm, image=img, bg="#d5d4fe")
        label_img.image = img
        label_img.place(relx=.04,rely=.04)
        
        title_lbl=Label(ifrm,text='This is Transfer Screen',font=('arial',20,'bold'),bg='white',fg='purple')
        title_lbl.pack()
        def welcome_click():
            frm.destroy()
            welcome_screen()
        tfr_acn_lbl=Label(ifrm,font=('arial',16,'bold'),bg='#d5d4fe',fg='#000',border=0,text="Account Number:")
        tfr_acn_lbl.place(relx=.32,rely=.25)
        tfr_acn_entry=Entry(ifrm,font=('arial',16),bg='white',border=0,width=18,show="*")
        tfr_acn_entry.place(relx=.58,rely=.25)
        tfr_acn_entry.focus()
        Frame(ifrm,width=218,height=1,bg='black').place(relx=.58,rely=.31)
        
        tfr_con_acn_lbl=Label(ifrm,font=('arial',16,'bold'),bg='#d5d4fe',fg='#000',border=0,text="Confirm Account:")
        tfr_con_acn_lbl.place(relx=.32,rely=.35)
        tfr_con_acn_entry=Entry(ifrm,font=('arial',16),bg='white',border=0,width=18)
        tfr_con_acn_entry.place(relx=.58,rely=.35)
        Frame(ifrm,width=218,height=1,bg='black').place(relx=.58,rely=.41)
        
        tfr_hname_lbl=Label(ifrm,font=('arial',16,'bold'),bg='#d5d4fe',fg='#000',border=0,text="Account Holder Name:")
        tfr_hname_lbl.place(relx=.32,rely=.45)
        tfr_hname_entry=Entry(ifrm,font=('arial',16),bg='white',border=0,width=18)
        tfr_hname_entry.place(relx=.58,rely=.45)
        Frame(ifrm,width=218,height=1,bg='black').place(relx=.58,rely=.51)
        
        tfr_amo_lbl=Label(ifrm,font=('arial',16,'bold'),bg='#d5d4fe',fg='#000',border=0,text="Amount:")
        tfr_amo_lbl.place(relx=.32,rely=.55)
        tfr_amo_entry=Entry(ifrm,font=('arial',16),bg='white',border=0,width=18)
        tfr_amo_entry.place(relx=.58,rely=.55)
        Frame(ifrm,width=218,height=1,bg='black').place(relx=.58,rely=.61)
        
        
        btn_tfr=Button(ifrm,font=('arial',20,'bold'),text="Submit",cursor='hand2',bg='#d5d4fe',fg='#0d6efd',width=8,border=0,command=transfer_db)
        btn_tfr.place(relx=0.36,rely=0.75)
        
        btn_can_back=Button(ifrm,font=('arial',20,'bold'),text="Cancel",cursor='hand2',fg='#0d6efd',width=8,border=0,bg='#d5d4fe',command=welcome_click)
        btn_can_back.place(relx=0.55,rely=0.75) 
    
    def help_screen():
        ifrm=Frame(frm,highlightthickness=2,highlightbackground='black')
        ifrm.configure(bg="#d5d4fe")
        ifrm.place(relx=.1,rely=.13,relwidth=.82,relheight=.75)
        
        def help_db():
            
            sub=sub_entry.get()
            mail=mail_entry.get("1.0","end")
            # try:
            conobj=sqlite3.connect(database="banking.sqlite")
            curobj=conobj.cursor()
            curobj.execute("INSERT INTO help (user_id, help_sub,help_desc, help_date) VALUES (?, ?, ?, ?)",(user_id,sub,mail, time.ctime()))
            conobj.commit()
            conobj.close()
            messagebox.showinfo("Email","Email sent successfully")
            # except:
                # print("Help Error")
        
        img=PhotoImage(file='help.png').subsample(1,1)
        label_img = Label(ifrm, image=img, bg="#d5d4fe")
        label_img.image = img
        label_img.place(relx=.04,rely=.2)
        
        title_lbl=Label(ifrm,text='Help Screen',font=('arial',20,'bold'),bg='#d5d4fe',fg='purple')
        title_lbl.pack()
        def welcome_click():
            frm.destroy()
            welcome_screen()
            
        
        sub_lbl=Label(ifrm,text='Subject',font=('arial',10,'bold','underline'),bg='#d5d4fe',fg='purple')
        sub_lbl.place(relx=.28,rely=.1)
        sub_entry=Entry(ifrm,font=('arial',16),bg='white',border=1,width=55)
        sub_entry.place(relx=.28,rely=.15)
        Frame(ifrm,width=663,height=2,bg='black').place(relx=.28,rely=.21)
        
        mail_lbl=Label(ifrm,text='Compose Email',font=('arial',10,'bold','underline'),bg='#d5d4fe',fg='purple')
        mail_lbl.place(relx=.28,rely=.223)
        mail_entry=Text(ifrm,font=('arial',16),bg='white',border=1,width=55)
        mail_entry.place(relx=.28,rely=.27,relheight=.58)
        
              
        btn_tfr=Button(ifrm,font=('arial',20,'bold','underline'),text="Send",cursor='hand2',bg='#28a745',fg='White',width=8,border=0,pady=0,command=help_db)
        btn_tfr.place(relx=0.4,rely=0.86)
        
        btn_can_back=Button(ifrm,font=('arial',20,'bold','underline'),text="Cancel",cursor='hand2',fg='White',width=8,border=0,pady=0,bg='#17a2b8',command=welcome_click)
        btn_can_back.place(relx=0.55,rely=0.86) 
        
        
        
        
    btn_bla=Button(frm,font=('arial',20,'bold'),text="Check balance",bg='#0dcaf0',cursor='hand2',fg='#000',width=15,border=0,command=balance_screen)
    btn_bla.place(relx=0.1,rely=0.15,relheight=0.2)
        
    btn_deposit=Button(frm,font=('arial',20,'bold'),text="Deposit",bg='#0dcaf0',cursor='hand2',fg='#000',width=15,border=0,command=deposit_screen)
    btn_deposit.place(relx=0.40,rely=0.15,relheight=0.2)
    
    btn_withdraw=Button(frm,font=('arial',20,'bold'),text="Withdraw",bg='#0dcaf0',cursor='hand2',fg='#000',width=15,border=0,command=withdraw_screen)
    btn_withdraw.place(relx=0.7,rely=0.15,relheight=0.2)
    
    btn_mini_statement=Button(frm,font=('arial',20,'bold'),text="Transaction History",bg='#0dcaf0',cursor='hand2',fg='#000',width=15,border=0,command=mini_statement_screen)
    btn_mini_statement.place(relx=0.1,rely=0.5,relheight=0.2)
    
    btn_transfer=Button(frm,font=('arial',20,'bold'),text="Transfer",bg='#0dcaf0',cursor='hand2',fg='#000',width=15,border=0,command=transfer_screen)
    btn_transfer.place(relx=0.4,rely=0.5,relheight=0.2)
    
    btn_help=Button(frm,font=('arial',20,'bold'),text="Help",bg='#0dcaf0',cursor='hand2',fg='#000',width=15,border=0,command=help_screen)
    btn_help.place(relx=0.7,rely=0.5,relheight=0.2)
    
home_screen()

win.mainloop()
