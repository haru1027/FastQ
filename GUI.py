from tkinter import * 
from tkinter import messagebox
#Window page
window = Tk()
window.geometry("1920x1080")
window.title("FastQ")
window.config(background="white")
icon = PhotoImage(file="FastQ/logo.png")
window.iconphoto(True, icon)
User_icon = PhotoImage(file="FastQ/logo.png").subsample(4,4)

window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

#============================================
#Account registration

def register():
     student_frame.grid_remove()
     regframe = Frame(window,background='white',padx=300)
     regframe.grid()

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
          student_frame.grid()
     def createaccount():
          ce = create__entry.get()
          cs = create_studentid_entry.get()
          cp = create_password_entry.get()
          if  len(ce and cs and cp) == 0:
               messagebox.showerror("Error","Please input all needed information!")
          
          else: 
               messagebox.showinfo("Success!","Successfuly created new account")

     create_account = Button(regframe, text='Create account',font=('poppins',12),relief=SUNKEN,bd='2',bg='#1f6035',fg='white',command=createaccount)
     create_account.grid(row=7,column=0,pady=(50,20))
     regback = Button(regframe, text='Back',font=('poppins',10,'underline'),bg='white',relief=SUNKEN,bd='2',command=back)
     regback.grid(row=9,column=0)

#=====================================================================================================================================
#STUDENT window

def login():
    usn = username.get()
    pw = password.get()
    if usn == '03-01-2425-044753' and pw == "1234" :
         student_frame.grid_forget()
         dashboard.grid()
    else:
         error =  messagebox.showerror("Error", "You entered wrong username or password!")
         password.delete(0,END)

student_frame = Frame(window,bg='white')
student_frame.grid()

welcome = Label(student_frame,text='Welcome to FastQ',font=('poppins',20,'bold'),fg='Black',bg='white',image=User_icon,compound='left',padx=20)
welcome.grid(row=0,column=0,columnspan=2,pady=(20,80))

username_label = Label(student_frame,text='Student ID',font=('poppins',15),bg='white')
username_label.grid(row=1,column=0,columnspan=2,padx=(0,240))

username = Entry(student_frame,font=('poppins', 20),bg='white')
username.grid(row=2,column=0,columnspan=2)

password_label = Label(student_frame,text='Password',font=('poppins',15),bg='white')
password_label.grid(row=3,column=0,columnspan=2,padx=(0,240))

password = Entry(student_frame,font=('poppins', 20),bg='white',show='*')
password.grid(row=4,column=0,columnspan=2)

login_btn = Button(student_frame,text='Log in',font=('poppins',12),fg = 'white',command=login,bg='#1f6035')
login_btn.grid(row=5,column=0,columnspan=2,pady=(30,60))

newuser = Label(student_frame, text="Don't have an account yet?",font=('poppins',10),bg='white')
newuser.grid(row=6,column=0)
register_btn = Button(student_frame, text='Register now',font=('poppins',10,'underline'),bg='white',relief=FLAT,command=register)
register_btn.grid(row=6,column=1,padx=(0,80))
  
def staff():
     student_frame.grid_remove()
     staffframe.grid()

staff_option = Label(student_frame, text="Are you a staff?",font=('poppins',10),bg='white')
staff_option.grid(row=7,column=0,padx=(80,0))
staff_option_btn = Button(student_frame, text='Click here',font=('poppins',10,'underline'),bg='white',relief=FLAT,command=staff)
staff_option_btn.grid(row=7,column=1,padx=(0,80))

#============================================================
#Staff window
staffframe = Frame(window,bg='white')
welcome2 = Label(staffframe,text='Welcome to FastQ',font=('poppins',20,'bold'),fg='Black',bg='white',image=User_icon,compound='left',padx=20)
welcome2.grid(row=0,column=0,columnspan=2)

welcome3 = Label(staffframe,text='Staff window',font=('poppins','10'),fg='Black',bg='white')
welcome3.grid(row = 1,column=0,columnspan=2,pady=(0,80))

username_label = Label(staffframe,text='Staff username',font=('poppins',15),bg='white')
username_label.grid(row=2,columnspan=2,padx=(0,210     ))
username2 = Entry(staffframe,font=('poppins', 20),bg='white')
username2.grid(row=3)

password_label2 = Label(staffframe, text='Password',font=('poppins',15),bg='white')
password_label2.grid(row=4,columnspan=2,padx=(0,260))

password2 = Entry(staffframe,font=('poppins', 20),bg='white',show="*")
password2.grid(row=5,pady=(0,20))

def stafflogin():
     usn2 = username2.get()
     pw2 = password2.get()
     if usn2 == 'admin' and pw2 == "1234" :
          
          messagebox.showinfo('Success','Successfully Logged in!')
              
     else:
          error2 =  messagebox.showerror("Error", "You entered wrong username or password!")
          password2.delete(0,END)

login_btn2 = Button(staffframe,text="Log in", font=('poppins',12),fg = 'white',command=stafflogin,bg='#1f6035')
login_btn2.grid(row=6, columnspan=2,pady=(0,100))

def staffback():
     staffframe.grid_forget()
     student_frame.grid()

login_back = Button(staffframe,text="Back", font=('poppins',12),fg = 'black',command=staffback,bg='white')
login_back.grid(row=7,columnspan=2)

   
#==================================================================================
#Main dashboard
dashboard = Frame(window,bg='white',bd=1,relief=RIDGE)
name = Label(dashboard,text="Hello there, if you see this, your code is working. Placeholder lang, build in-progress.")
name.grid()
def backdashboard():
     dashboard.grid_remove()
     student_frame.grid()
back_dashboard = Button(dashboard,text='Back',command=backdashboard,bg='white')
back_dashboard.grid()



     
     

    






window.mainloop()