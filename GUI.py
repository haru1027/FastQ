from tkinter import * 
from tkinter import messagebox
from tkinter.ttk import Combobox

import sqlite3

#Window page
window = Tk()
window.geometry("1920x1080")
window.title("FastQ")
window.config(background="white")
icon = PhotoImage(file="assets/FastQ Logo.png")
window.iconphoto(True, icon)
User_icon = PhotoImage(file="assets/FastQ Logo.png").subsample(16,16)

window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

#=======================================================
#Main frame/Choice frame
mainframe = Frame(window,bg='white')
mainframe.grid()
welcome = Label(mainframe,text='Welcome to FastQ',font=('poppins',30,'bold'),fg='Black',bg='white',image=User_icon,compound='left',padx=20)
welcome.grid(row=0,column=0,columnspan=2,pady=0)

text = Label(mainframe,text="Let's get you sorted out!",font=('poppins',10),fg='Black',bg='white')
text.grid(row=1,columnspan=2,pady=(0,80))

def redirect_student_frame():
     staff_frame.grid_remove()
     student_frame.grid()
def redirect_staff_frame():
     student_frame.grid_remove()
     staff_frame.grid(columnspan=2)

student_choice_button = Button(mainframe, text="I'm a student",font=("Poppins", 15),bg='#203c3c',fg='white',relief=RIDGE,command=redirect_student_frame)
student_choice_button.grid(row=2,column=0)

staff_choice_button = Button(mainframe, text="I'm a staff",font=("poppins", 15),bg='#a8ffff',fg='black',relief=RIDGE, command=redirect_staff_frame)
staff_choice_button.grid(row=2,column=1)

#=====================================================================================================================================
#Student log in frame

def login():
    usn = username.get()
    pw = password.get()
    if usn == '03-01-2425-044753' and pw == "1234" :
         mainframe.grid_forget()
         student_dashboard.grid()
    else:
         error =  messagebox.showerror("Error", "You entered wrong username or password!")
         password.delete(0,END)

student_frame = Frame(mainframe,bg='white')
student_frame.grid(columnspan=2)

username_label = Label(student_frame,text='Student ID',font=('poppins',15),bg='white')
username_label.grid(row=1,column=0,columnspan=2,padx=(0,240))

username = Entry(student_frame,font=('poppins', 20),bg='white')
username.grid(row=2,column=0,columnspan=2)

password_label = Label(student_frame,text='Password',font=('poppins',15),bg='white')
password_label.grid(row=3,column=0,columnspan=2,padx=(0,240))

password = Entry(student_frame,font=('poppins', 20),bg='white',show='*')
password.grid(row=4,column=0,columnspan=2)

login_btn = Button(student_frame,text='Log in',font=('poppins',12),fg = 'white',command=login,bg='#203c3c')
login_btn.grid(row=5,column=0,columnspan=2,pady=(30,60))

#remove this once everything is finisehd

username.insert(0,'03-01-2425-044753')
password.insert(0,'1234')
## remove til here ^^^^
     
#=======================================================================================================================================
#Staff login frame

def login():
    usn = username.get()
    pw = password.get()
    if usn == '03-01-2425-044753' and pw == "1234" :
         mainframe.grid_forget()
         staff_dashboard_frame.grid()
    else:
         error =  messagebox.showerror("Error", "You entered wrong username or password!")
         password.delete(0,END)

staff_frame = Frame(mainframe,bg='white')

username_label = Label(staff_frame,text='Staff username',font=('poppins',15),bg='white')
username_label.grid(row=1,column=0,columnspan=2,sticky=W,padx=(0,210))

username2 = Entry(staff_frame,font=('poppins', 20),bg='white')
username2.grid(row=2,column=0,columnspan=2)

password_label2 = Label(staff_frame,text='Password',font=('poppins',15),bg='white')
password_label2.grid(row=3,column=0,columnspan=2,padx=(0,240))

password2 = Entry(staff_frame,font=('poppins', 20),bg='white',show='*')
password2.grid(row=4,column=0,columnspan=2)

def stafflogin():
     usn2 = username2.get()
     pw2 = password2.get()
     if usn2 == 'admin' and pw2 == "1234" :
          mainframe.grid_remove()
          staff_dashboard_frame.grid()
              
     else:
          error2 =  messagebox.showerror("Error", "You entered wrong username or password!")
          password2.delete(0,END)

login_btn2 = Button(staff_frame,text='Log in',font=('poppins',12),fg = 'white',command=stafflogin,bg='#203c3c')
login_btn2.grid(row=5,column=0,columnspan=2,pady=(30,60))


#==================================================================================
#student_dashboard
student_dashboard = Frame(window,bg='white',bd=1,relief=RIDGE)

student_dashboard_title = Label(student_dashboard,text='Welcome to FastQ',font=('poppins',30,'bold'),fg='Black',bg='white',compound='left')
student_dashboard_title.grid(row=0,column=0,columnspan=2,pady=(0,80))
##Name frame
name_frame = Frame(student_dashboard,relief=FLAT)
name_frame.grid(row=1,column=0,pady=(0,20),sticky=W)

name = Label(name_frame,text="Welcome, Bryan.",font=('times new roman',20,'italic'),bg='white')
name.grid(row=0,column=0,sticky=W)



##balance frame
balance_frame = Frame(student_dashboard,bd=10,relief=FLAT,bg='#203c3c')
balance_frame.grid(row=2,column=0,sticky=W)

balance_text = Label(balance_frame, text= "CURRENT BALANCE",font=("sans", 10),bg='#203c3c',fg='white')
balance_text.grid(row=0,column=0,sticky=W,columnspan=2)

balance = Label(balance_frame, text= '₱30,120',font=('Poppins',20),bg='#203c3c',fg='white')
balance.grid(row=1,column=0,sticky=W,columnspan=2)

balance_text2 = Label(balance_frame, text= 'After a transaction. amount shall be updated upon the next log-in.',font=("sans", 8),bg='#203c3c',fg='white')
balance_text2.grid(row=2,column=0,sticky=W,columnspan=2,pady=(0,30))

def pay_now():
    student_dashboard.grid_remove()
    payment_frame.grid()


pay = Button(balance_frame,text="Pay now",bg='#cf5a26',fg='white',font=('poppins',8,'bold'),command=pay_now)
pay.grid(row=3,column=1,sticky=E)



#Payment frame
payment_frame = Frame(window,bg='white')

def payment_frame_back():
    payment_frame.grid_remove()
    student_dashboard.grid()


payment_frame_heading = Label(payment_frame,text="Payment form",font=("poppins", 30,'bold'),bg='white',fg='black')
payment_frame_heading.grid(row=0,column=0,columnspan=2,pady=(0,50))

payment_frame_name_label = Label(payment_frame,text='Name ',font=('poppins',15),bg='white')
payment_frame_name_label.grid(row=1,column=0)


payment_frame_name = Entry(payment_frame,font=("poppins", 20),bg='white',fg='black')
payment_frame_name.insert(0,"Bryan Keith Bumanlag")
payment_frame_name.grid(row=1,column=1)

payment_frame_studentid_label = Label(payment_frame,text='Student ID: ',font=('poppins',15),bg='white')
payment_frame_studentid_label.grid(row=2,column=0)

payment_frame_studentid = Entry(payment_frame,font=("poppins", 20),bg='white',fg='black')
payment_frame_studentid.insert(0,"03-01-2425-044753")
payment_frame_studentid.grid(row=2,column=1)

whattopay = Combobox(payment_frame, values=['Tuition Fee', 'Books', 'Miscellaneous'], font=('poppins', 12))
whattopay.grid(row=3,column=0)

amounttopay = Entry(payment_frame,font=('poppins', 12),bd=1,relief=RIDGE)
amounttopay.grid(row=3,column=1)

payment_var = StringVar()
cash_check = Checkbutton(payment_frame, text="Cash", variable=payment_var, onvalue="cash", offvalue="", font=('poppins', 12), bg='white')
cash_check.grid(row=4, column=0, padx=50, pady=10)

# Online checkbox
online_check = Checkbutton(payment_frame, text="Online Payment", variable=payment_var, onvalue="online", offvalue="", font=('poppins', 12), bg='white')
online_check.grid(row=4, column=1, padx=50, pady=10)

number = 0
def get_queue_number():
    global number
    number += 1
    queue_label.config(text=f"Your queue number is #{number} ")
    payment_var.get()
    

get_queue_button = Button(payment_frame,text="Get queue number",command=get_queue_number,bg='white',font=('poppins',10))
get_queue_button.grid(row=5,column=0,columnspan=2)

queue_label = Label(payment_frame,bg='white', text="",font=("poppins", 20),fg='black')
queue_label.grid(row=6,column=0,columnspan=2)



payment_frame_back_button = Button(payment_frame,text="Back",command=payment_frame_back,bg='white',font=('poppins',10))
payment_frame_back_button.grid(row=7,column=0,columnspan=2)




##RECENT TRANSACTIONS FRAME

recent_transactions_frame = Frame(student_dashboard,bd=10,relief=FLAT,bg='white')
recent_transactions_frame.grid(row=3,column=0,sticky=W)

recent_transactions = Label(recent_transactions_frame,text= 'Recent transactions',font=("Poppins", 12),bg='white',fg='black')
recent_transactions.grid(row=0,column=0,sticky=W)

recent_transactions2 = Label(recent_transactions_frame,text= 'Activity posted  to your student account',font=("sans", 8),bg='white',fg='black')
recent_transactions2.grid(row=1,column=0,sticky=W,pady=(0,20))




def backdashboard():
     student_dashboard.grid_remove()
     mainframe.grid()
back_dashboard = Button(student_dashboard,text='Back',command=backdashboard,bg='white')
back_dashboard.grid()
#=============================================================
#Staff dashboard
staff_dashboard_frame = Frame(window,bg='white')
staff_dashboard_welcome = Label(staff_dashboard_frame,text='Welcome to FastQ Staff',font=('poppins',20,'bold'),fg='Black',bg='white',image=User_icon,compound='left',padx=20)
staff_dashboard_welcome.grid()

def register():
     staff_dashboard_frame.grid_remove()
     regframe.grid()

def staff_dashboard_back():
     staff_dashboard_frame.grid_remove()
     mainframe.grid()

staff_dashboard_backbtn = Button(staff_dashboard_frame, text='Back',font=('poppins',10,'underline'),bg='white',relief=SUNKEN,bd='2',command=staff_dashboard_back)
staff_dashboard_backbtn.grid()

newuser = Label(staff_dashboard_frame, text="Don't have an account yet?",font=('poppins',10),bg='white')
newuser.grid(row=6,column=0)
register_btn = Button(staff_dashboard_frame, text='Register now',font=('poppins',10,'underline'),bg='white',relief=FLAT,command=register)
register_btn.grid(row=6,column=1,padx=(0,80))




#============================================
#Account registration



regframe = Frame(window,background='white',padx=300)
create = Label(regframe,text="Create new account",font=('poppins',20,'bold'),fg='Black',bg='White',image=User_icon,compound='left')
create.grid(row=0,column=0,columnspan=2,pady=(0,70))
     
create_name = Label(regframe, text='Name',font=('Poppins',15),bg='white')
create_name.grid(row=1,column=0,sticky='w',padx=(18,0))
create__entry = Entry(regframe,font=('poppins',15),bg='white')
create__entry.grid(row=2,column=0)
create_studentid = Label(regframe, text='Student ID',font=('Poppins',15),bg='white')
create_studentid.grid(row=3,column=0,sticky='w',padx=(18,0))
create_studentid_entry = Entry(regframe,font=('poppins',15))
create_studentid_entry.grid(row=4,column=0)
create_password = Label(regframe, text='Password',font=('Poppins',15),bg='white')
create_password.grid(row=5,column=0,sticky='w',padx=(18,0))
create_password_entry = Entry(regframe,font=('poppins',15))
create_password_entry.grid(row=6,column=0)

def back():
          regframe.grid_remove()
          staff_dashboard_frame.grid()
def createaccount():
          ce = create__entry.get()
          cs = create_studentid_entry.get()
          cp = create_password_entry.get()
          if not ce or not cs or not cp:
               messagebox.showerror("Error","Please input all needed information!")
               return
          if len(ce) < 7 or any(CHAR.isdigit() for CHAR in ce):
               messagebox.showerror("Error", "Please put a valid name!")
               return
          if not all(CHAR.isdigit() or CHAR == '-' for CHAR in cs):
               messagebox.showerror("Error", "Student ID must only contain numbers and dashes!")
               return
          if len(cs) != 17:
               messagebox.showerror("Error", "Student ID must be 17 characters!")
               return
          elif len(cp) < 8 or not any(CHAR.isupper() for CHAR in cp) or not any(CHAR.islower() for CHAR in cp) or not any(CHAR.isdigit() for CHAR in cp):
               messagebox.showerror("Error","Password must have 8 characters minimum and have atleast one uppercase, one lowercase, and one digit.")
               return
          elif any(CHAR == " " for CHAR in cp):
               messagebox.showerror("Error","Must not include spaces!")
               return   
          else: 
               messagebox.showinfo('Success!','Successfully Created account')


create_account = Button(regframe, text='Create account',font=('poppins',12),relief=SUNKEN,bd='2',bg='#203c3c',fg='white',command=createaccount)
create_account.grid(row=7,column=0,pady=(50,20))
regback = Button(regframe, text='Back',font=('poppins',10,'underline'),bg='white',relief=SUNKEN,bd='2',command=back)
regback.grid(row=9,column=0)



window.mainloop()