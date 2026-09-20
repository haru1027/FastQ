from tkinter import * 
from tkinter import messagebox
#Window page
window = Tk()
window.geometry("1920x1080")
window.title("FastQ")
window.config(background="white")
icon = PhotoImage(file="logo.png")
window.iconphoto(True, icon)
User_icon = PhotoImage(file="logo.png").subsample(4,4)


frame = Frame(window,bg='white',border=2,relief=RIDGE,padx=300)
frame.grid()

window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

#STAFF frame
staffframe = Frame(window,bg='white')
welcome2 = Label(staffframe,text="Welcome to FastQ",font=('poppins',20,'bold'),fg='Black',bg='white',padx=10,pady=0,image=User_icon,compound='left')
welcome2.grid(row=0,column=0,columnspan=2)

welcome3 = Label(staffframe,text='Staff window',font=('poppins','10'),fg='Black',bg='white',padx=10,pady=10)
welcome3.grid(row = 1,column=0,columnspan=2)

entrysection2 = Frame(staffframe,background='white')
entrysection2.grid(column=1,sticky=W)

username_label = Label(entrysection2,text='Staff username',font=('poppins',15),bg='white').grid(row=1,columnspan=2,sticky='w')
username2 = Entry(entrysection2,font=('poppins', 20),bg='white')
username2.grid(row=2, padx=20, pady=10)

password_label2 = Label(entrysection2, text='Password',font=('poppins',15),bg='white')
password_label2.grid(row=3,columnspan=2,sticky='w')

password2 = Entry(entrysection2,font=('poppins', 20),bg='white',show="*")
password2.grid(row=4, padx=20,pady=10)

def stafflogin():
     usn2 = username2.get()
     pw2 = password2.get()
     if usn2 == 'admin' and pw2 == "1234" :
          messagebox.showinfo('Success','Successfully Loggedin!')
              
              
     else:
          error2 =  messagebox.showerror("Error", "You entered wrong username or password!")
          password2.delete(0,END)

login_btn2 = Button(entrysection2,text="Log in", font=('poppins',12),fg = 'white',command=stafflogin,bg='#1f6035')
login_btn2.grid(row=5, column=0, columnspan=2, pady=15)

def staffback():
     staffframe.grid_forget()
     frame.grid()
login_btn2 = Button(entrysection2,text="Back", font=('poppins',12),fg = 'black',command=staffback,bg='white',bd=2,relief=RIDGE)
login_btn2.grid(row=6, column=0, columnspan=2, pady=15)



#==================================================================================
#STUDENT Log in frame

welcome = Label(frame,text="Welcome to FastQ",font=('poppins',20,'bold'),fg='Black',bg='white',padx=10,pady=100,image=User_icon,compound='left')
welcome.grid(row=0,column=0,columnspan=2)

entrysection = Frame(frame,background='white')
entrysection.grid(column=1,sticky=W)

username_label = Label(entrysection,text='Student ID',font=('poppins',15),bg='white').grid(row=1,columnspan=2,sticky='w')
username = Entry(entrysection,font=('poppins', 20),bg='white')
username.grid(row=2, padx=20, pady=10)

password_label = Label(entrysection, text='Password',font=('poppins',15),bg='white')
password_label.grid(row=3,columnspan=2,sticky='w')

password = Entry(entrysection,font=('poppins', 20),bg='white',show="*")
password.grid(row=4, padx=20,pady=10)

def login():
    usn = username.get()
    pw = password.get()
    if usn == '03-01-2425-044753' and pw == "1234" :
         frame.grid_forget()
         dashboard.grid()
         
         
    else:
         error =  messagebox.showerror("Error", "You entered wrong username or password!")
         password.delete(0,END)

login_btn = Button(entrysection,text="Log in", font=('poppins',12),fg = 'white',command=login,bg='#1f6035')
login_btn.grid(row=5, column=0, columnspan=2, pady=15)


#==================================================================================
#Main dashboard
dashboard = Frame(window,bg='white',bd=1,relief=RIDGE)
name = Label(dashboard,text="Hello there, if you see this, your code is working. Placeholder lang, build in-progress.")
name.grid()
def backdashboard():
     dashboard.grid_remove()
     frame.grid()
back_dashboard = Button(dashboard,text='Back',command=backdashboard,bg='white')
back_dashboard.grid()




def register():

     frame.grid_remove()
     regframe = Frame(window,border=2,relief=SUNKEN,background='white',padx=200)
     regframe.grid()

     create = Label(regframe,
              text="Create new account",
              font=('poppins',20),
              fg='Black',
              bg='White',
              padx=10,
              pady=10,
              image=User_icon,
              compound='left').grid(row=0,column=0,columnspan=2)
     
     create_name = Label(regframe, text='Name',font=('Poppins',15),bg='white').grid(row=1,column=0)
     create__entry = Entry(regframe,font=('poppins',15),bg='white').grid(row=2,column=0)
     create_studentid = Label(regframe, text='Student ID',font=('Poppins',15),bg='white').grid(row=3,column=0)
     create_studentid_entry = Entry(regframe,font=('poppins',15)).grid(row=4,column=0)
     create_password = Label(regframe, text='Password',font=('Poppins',15),bg='white').grid(row=5,column=0)
     create_password_entry = Entry(regframe,font=('poppins',15)).grid(row=6,column=0)


     def back():
          regframe.grid_remove()
          frame.grid()
     

     def createaccount():
          messagebox.showinfo("Success!","Successfuly created new account")

     create_account = Button(regframe, text='Create account',font=('poppins',10),bg='white',relief=SUNKEN,bd='2',command=createaccount)
     create_account.grid(row=7,column=0)
     regback = Button(regframe, text='Back',font=('poppins',10,'underline'),bg='white',relief=SUNKEN,bd='2',command=back)
     regback.grid(row=8,column=0)
     
     

    

frame_register = Frame(frame,bg='white')
frame_register.grid(row=2,columnspan=3,pady=50)
newuser = Label(frame_register, text="Don't have an account yet?",font=('poppins',10),bg='white')
newuser.grid(row=0,column=0, padx=5,sticky='w')
register_btn = Button(frame_register, text='Register now',font=('poppins',10,'underline'),bg='white',relief=FLAT,command=register)
register_btn.grid(column=1,sticky='e',row = 0, padx=5)

def staff():
     frame.grid_remove()
     staffframe.grid()
     

staff_option = Label(frame_register, text="Are you a staff?",font=('poppins',10),bg='white')
staff_option.grid(row=1,column=0, padx=5,sticky='e')
staff_option_btn = Button(frame_register, text='Click here',font=('poppins',10,'underline'),bg='white',relief=FLAT,command=staff)
staff_option_btn.grid(column=1,sticky='w',row = 1, padx=5)

window.mainloop()
