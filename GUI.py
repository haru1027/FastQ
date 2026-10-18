from tkinter import * 
from tkinter import messagebox
from tkinter.ttk import Combobox, Treeview, Style
import sqlite3
from PIL import Image, ImageTk

from datetime import datetime

# total fees per semester (made-up amounts, change them anytime)
COURSE_FEES = {
    "BS Information Technology": 28000,
    "BS Architecture": 34000,
    "BS Computer Engineering": 32000,
    "BS Civil Engineering": 31000,
    "BS Electrical Engineering": 31000,
    "BS Mechanical Engineering": 31000,
    "BS Nursing": 38000,
    "BS Pharmacy": 40000,
    "BS Medical Laboratory Science": 39000,
    "BS Psychology": 24000,
    "BS Accountancy": 27000,
    "BS Management Accounting": 25000,
    "BS Accounting Technology": 24000,
    "BS Hospitality Management": 30000,
    "BS Tourism Management": 27000,
    "BS Business Administration": 23000,
    "BSBA major in Marketing Management": 23000,
    "BSBA major in Financial Management": 23000,
    "BS Elementary Education": 20000,
    "BS Secondary Education major in English": 20000,
    "BS Secondary Education major in Mathematics": 20500,
    "BS Secondary Education major in Science": 21000,
    "BS Secondary Education major in Social Studies": 20000,
    "BS Criminology": 26000,}

def init_db():
    conn = sqlite3.connect("fastq.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT UNIQUE NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            course TEXT DEFAULT 'Not set',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            course TEXT PRIMARY KEY,
            total_fee REAL NOT NULL)""")
    for course_name, fee in COURSE_FEES.items():
        cursor.execute("INSERT OR IGNORE INTO courses (course, total_fee) VALUES (?, ?)", (course_name, fee))
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS staff (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL)""")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS queue (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            name TEXT NOT NULL,
            payment_for TEXT NOT NULL,
            amount REAL NOT NULL,
            payment_method TEXT NOT NULL,
            status TEXT DEFAULT 'Waiting',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")
    try:
        cursor.execute("ALTER TABLE queue ADD COLUMN staff TEXT")
        cursor.execute("UPDATE queue SET staff='admin'")   
    except sqlite3.OperationalError:
        pass  
    try:
        cursor.execute("ALTER TABLE students ADD COLUMN course TEXT DEFAULT 'Not set'")
    except sqlite3.OperationalError:
        pass   
    try:
        cursor.execute("ALTER TABLE staff ADD COLUMN role TEXT DEFAULT 'staff'")
    except sqlite3.OperationalError:
        pass
    cursor.execute("INSERT OR IGNORE INTO staff (username, password, role) VALUES ('admin', '1234', 'admin')")
    cursor.execute("UPDATE staff SET role='admin' WHERE username='admin'")
    conn.commit()
    conn.close()
init_db()


#Window page
window = Tk()
window.geometry("1920x1080")
window.title("FastQ")
window.config(background="white")
icon = PhotoImage(file="assets/FastQ Logo.png")
window.iconphoto(True, icon)
window.attributes("-fullscreen", True)
User_icon = PhotoImage(file="assets/FastQ Logo.png").subsample(16,16)

window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

pic = Image.open("assets/eye_open.jpg")
pic =  pic.resize((26,26))
pic2 = Image.open("assets/eye_closed.jpg")
pic2 =  pic2.resize((26,26))

eye_open = ImageTk.PhotoImage(pic)
eye_closed = ImageTk.PhotoImage(pic2)

#=======================================================
#Main frame (split screen: left panel + right panel)
mainframe = Frame(window,bg='white')
mainframe.grid(sticky=NSEW)
mainframe.grid_rowconfigure(0,weight=1)
mainframe.grid_columnconfigure(1,weight=1)

# ---------- Left panel (dark green) ----------
left_panel = Frame(mainframe,bg='#203c3c',width=640)
left_panel.grid(row=0,column=0,sticky=NSEW)
left_panel.grid_rowconfigure(1,weight=1)

brand_label = Label(left_panel,text='FastQ',font=('poppins',20,'bold'),fg='white',bg='#203c3c',image=User_icon,compound='left',padx=12)
brand_label.grid(row=0,column=0,sticky=W,padx=60,pady=(50,0))

left_middle = Frame(left_panel,bg='#203c3c')
left_middle.grid(row=1,column=0,sticky=W,padx=60)

headline_label = Label(left_middle,text='Payments without\nthe wait.',font=('poppins',32,'bold'),fg='white',bg='#203c3c',justify=LEFT)
headline_label.grid(row=0,column=0,sticky=W)

subtext_label = Label(left_middle,text='Manage the payment queue and check\nstudent balances, all in one place.',font=('poppins',12),fg='#9fb8b5',bg='#203c3c',justify=LEFT)
subtext_label.grid(row=1,column=0,sticky=W,pady=(15,0))


# ---------- Right panel (light gray, holds the login card) ----------
right_panel = Frame(mainframe,bg='#f2f5f4')
right_panel.grid(row=0,column=1,sticky=NSEW)
right_panel.grid_rowconfigure(0,weight=1)
right_panel.grid_columnconfigure(0,weight=1)

#=======================================================================================================================================
#Staff login frame (the white card)

staff_frame = Frame(right_panel,bg='white',padx=40,pady=40,highlightbackground='#dfe6e5',highlightthickness=1)
staff_frame.grid(row=0,column=0)


isShown = False

def show():
     global isShown
     if isShown:
          password.config(show="*")
          isShown = False
          show_password.config(image=eye_closed)
     else:
          password.config(show="")
          isShown = True
          show_password.config(image=eye_open)

login_title = Label(staff_frame,text='Welcome back',font=('poppins',22,'bold'),fg='black',bg='white')
login_title.grid(row=0,column=0,sticky=W)

login_subtitle = Label(staff_frame,text='Log in to your staff account',font=('poppins',10),fg='gray',bg='white')
login_subtitle.grid(row=1,column=0,sticky=W,pady=(4,25))

username_label = Label(staff_frame,text='Username',font=('poppins',10),fg='gray',bg='white')
username_label.grid(row=2,column=0,sticky=W)

user_box = Frame(staff_frame,bg='white',highlightbackground='#c5d0cf',highlightthickness=1)
user_box.grid(row=3,column=0,sticky=EW,pady=(4,0))
username = Entry(user_box,font=('poppins',12),bg='white',relief=FLAT,bd=0)
username.grid(sticky=W,ipady=8,padx=10)

password_label = Label(staff_frame,text='Password',font=('poppins',10),fg='gray',bg='white')
password_label.grid(row=4,column=0,sticky=W,pady=(18,0))

pw_box = Frame(staff_frame,bg='white',highlightbackground='#c5d0cf',highlightthickness=1)
pw_box.grid(row=5,column=0,sticky=EW,pady=(4,0))
pw_box.grid_columnconfigure(0,weight=1)
password = Entry(pw_box,font=('poppins',12),bg='white',relief=FLAT,bd=0,show='*')
password.grid(sticky=EW,padx=10,ipady=8)

show_password = Button(pw_box,command=show,image=eye_closed,bg='white',activebackground='white',bd=0,relief=FLAT)
show_password.grid(row=0,column=1,padx=(0,8))
#REMOVE IF TAPOS NA

username.insert(0,'admin')
password.insert(0,'1234')

##remove til here


current_staff = ""
current_role = ""
def stafflogin():
     global current_staff, current_role
     usn = username.get()
     pw = password.get()

     conn = sqlite3.connect("fastq.db")
     cur = conn.cursor()
     cur.execute('SELECT role FROM staff WHERE username=? AND password=?', (usn, pw))
     found = cur.fetchone()
     conn.close()

     if found:
          current_staff = usn
          current_role = found[0]
          if current_role == "admin":
               admin_tab.pack(side=LEFT,padx=(0,6))   # show the Admin tab
          else:
               admin_tab.pack_forget()                # hide it
          welcome.config(text=f'Welcome, {current_staff}!')
          clear_filters()
          clear_student_display()
          show_page('queue')
          mainframe.grid_remove()
          staff_dashboard_frame.grid(sticky=NSEW)
          window.config(background="#f2f5f4")
     else:
          messagebox.showerror("Error", "You entered wrong username or password!")
          password.delete(0,END)

login_btn2 = Button(staff_frame,text='Log in',font=('poppins',12,'bold'),fg='black',bg='#f59a23',activebackground='#e08a15',relief=FLAT,command=stafflogin)
login_btn2.grid(row=6,column=0,sticky=EW,pady=(28,0),ipady=6)
#=======================================================================================================================================
#Create account frame
create_frame = Frame(right_panel,bg='white',padx=40,pady=40,highlightbackground='#dfe6e5',highlightthickness=1)
create_frame.grid_columnconfigure(0,minsize=380)

isShown3 = False

def show3():
     global isShown3
     if isShown3:
          new_password.config(show="*")
          confirm_password.config(show="*")
          isShown3 = False
          show_password3.config(image=eye_closed)
     else:
          new_password.config(show="")
          confirm_password.config(show="")
          isShown3 = True
          show_password3.config(image=eye_open)

create_title = Label(create_frame,text='Create account',font=('poppins',22,'bold'),fg='black',bg='white')
create_title.grid(row=0,column=0,sticky=W)

create_subtitle = Label(create_frame,text='Set up a new staff account',font=('poppins',10),fg='gray',bg='white')
create_subtitle.grid(row=1,column=0,sticky=W,pady=(4,25))

new_username_label = Label(create_frame,text='Username',font=('poppins',10),fg='gray',bg='white')
new_username_label.grid(row=2,column=0,sticky=W)

new_user_box = Frame(create_frame,bg='white',highlightbackground='#c5d0cf',highlightthickness=1)
new_user_box.grid(row=3,column=0,sticky=EW,pady=(4,0))
new_username = Entry(new_user_box,font=('poppins',12),bg='white',relief=FLAT,bd=0)
new_username.pack(fill=X,padx=10,ipady=8)

new_password_label = Label(create_frame,text='Password',font=('poppins',10),fg='gray',bg='white')
new_password_label.grid(row=4,column=0,sticky=W,pady=(18,0))

new_pw_box = Frame(create_frame,bg='white',highlightbackground='#c5d0cf',highlightthickness=1)
new_pw_box.grid(row=5,column=0,sticky=EW,pady=(4,0))
new_pw_box.grid_columnconfigure(0,weight=1)
new_password = Entry(new_pw_box,font=('poppins',12),bg='white',relief=FLAT,bd=0,show='*')
new_password.grid(row=0,column=0,sticky=EW,padx=10,ipady=8)

show_password3 = Button(new_pw_box,command=show3,image=eye_closed,bg='white',activebackground='white',bd=0,relief=FLAT)
show_password3.grid(row=0,column=1,padx=(0,8))

confirm_password_label = Label(create_frame,text='Confirm password',font=('poppins',10),fg='gray',bg='white')
confirm_password_label.grid(row=6,column=0,sticky=W,pady=(18,0))

confirm_box = Frame(create_frame,bg='white',highlightbackground='#c5d0cf',highlightthickness=1)
confirm_box.grid(row=7,column=0,sticky=EW,pady=(4,0))
confirm_box.grid_columnconfigure(0,weight=1)
confirm_password = Entry(confirm_box,font=('poppins',12),bg='white',relief=FLAT,bd=0,show='*')
confirm_password.grid(row=0,column=0,sticky=EW,padx=10,ipady=8)

create_hint = Label(create_frame,text='Password: 8+ characters with an uppercase letter,\na lowercase letter, and a number.',font=('poppins',9),fg='gray',bg='white',justify=LEFT)
create_hint.grid(row=8,column=0,sticky=W,pady=(8,0))

def back_to_login():
     create_frame.grid_forget()
     staff_frame.grid(row=0,column=0)

def save_account():
     usn = new_username.get().strip()
     pw = new_password.get()
     cpw = confirm_password.get()

     if not usn or not pw or not cpw:
          messagebox.showerror("Error", "Please input all needed information!")
          return

     if not all(CHAR.isalnum() or CHAR == "_" for CHAR in usn):
          messagebox.showerror("Error", "Username can only have letters, numbers, and underscores!")
          return
     if len(usn) < 4:
          messagebox.showerror("Error", "Username must be at least 4 characters!")
          return
     if any(CHAR == " " for CHAR in pw):
          messagebox.showerror("Error", "Password must not include spaces!")
          return
     if len(pw) < 8 or not any(CHAR.isupper() for CHAR in pw) or not any(CHAR.islower() for CHAR in pw) or not any(CHAR.isdigit() for CHAR in pw):
          messagebox.showerror("Error", "Password must have 8 characters minimum and have at least one uppercase, one lowercase, and one digit.")
          return

     if pw != cpw:
          messagebox.showerror("Error", "Passwords do not match!")
          confirm_password.delete(0,END)
          return

     conn = sqlite3.connect("fastq.db")
     cur = conn.cursor()
     try:
          cur.execute('INSERT INTO staff (username, password) VALUES (?, ?)', (usn, pw))
          conn.commit()
     except sqlite3.IntegrityError:
          messagebox.showerror("Error", "That username is already taken!")
          return
     finally:
          conn.close()

     messagebox.showinfo("Success", "Account created! You can now log in.")
     new_username.delete(0,END)
     new_password.delete(0,END)
     confirm_password.delete(0,END)
     back_to_login()

create_btn = Button(create_frame,text='Create account',font=('poppins',12,'bold'),fg='black',bg='#f59a23',activebackground='#e08a15',relief=FLAT,command=save_account)
create_btn.grid(row=9,column=0,sticky=EW,pady=(24,0),ipady=6)

back_row = Frame(create_frame,bg='white')
back_row.grid(row=10,column=0,pady=(22,0))

back_label = Label(back_row,text='Already have an account?',font=('poppins',10),fg='gray',bg='white')
back_label.grid(row=0,column=0)

back_button = Button(back_row,text='Back to log in',font=('poppins',10,'bold','underline'),fg='gray',bg='white',activebackground='white',bd=0,command=back_to_login)
back_button.grid(row=0,column=1,padx=(6,0))
#=======================================================================================================================================
#Button on the log in page
def create_newaccount():
     staff_frame.grid_remove()   # hide the log in page
     create_frame.grid(row=0,column=0)   # show the create account page

signup_row = Frame(staff_frame,bg='white')
signup_row.grid(row=7,column=0,pady=(22,0))

create_newaccount_label = Label(signup_row,text="Don't have an account yet?",font=('poppins',10),fg='gray',bg='white')
create_newaccount_label.grid(row=0,column=0)

create_newaccount_button = Button(signup_row,text='Create a new account',font=('poppins',10,'bold','underline'),fg='gray',bg='white',activebackground='white',bd=0,command=create_newaccount)
create_newaccount_button.grid(row=0,column=1,padx=(6,0))


#=============================================================
#Staff dashboard (header with tabs + pages)
staff_dashboard_frame = Frame(window,bg='#f2f5f4')
staff_dashboard_frame.grid_columnconfigure(0,weight=1)
staff_dashboard_frame.grid_rowconfigure(1,weight=1)

def staff_dashboard_back():
     # Log out
     staff_dashboard_frame.grid_remove()
     window.config(background="white")
     mainframe.grid()

# ---------- Header bar ----------
header = Frame(staff_dashboard_frame,bg='#203c3c')
header.grid(row=0,column=0,sticky=EW)
header.grid_columnconfigure(2,weight=1)

FastQ_header = Label(header,text='FastQ',font=('poppins',18,'bold'),fg='white',bg='#203c3c',image=User_icon,compound='left',padx=10)
FastQ_header.grid(row=0,column=0,padx=(30,0),pady=10)

# the tabs
tabs_frame = Frame(header,bg='#203c3c')
tabs_frame.grid(row=0,column=1,padx=(40,0),sticky=S)

queue_tab = Button(tabs_frame,text='Queue',font=('poppins',10,'bold'),bd=0,relief=FLAT,highlightthickness=0,padx=20,pady=8,cursor='hand2',
                   bg='#203c3c',fg='#9fb8b5',activebackground='#203c3c',activeforeground='#9fb8b5',
                   command=lambda: show_page('queue'))
queue_tab.pack(side=LEFT,padx=(0,6))

finder_tab = Button(tabs_frame,text='Student Finder',font=('poppins',10,'bold'),bd=0,relief=FLAT,highlightthickness=0,padx=20,pady=8,cursor='hand2',
                    bg='#203c3c',fg='#9fb8b5',activebackground='#203c3c',activeforeground='#9fb8b5',
                    command=lambda: show_page('finder'))
finder_tab.pack(side=LEFT,padx=(0,6))

register_tab = Button(tabs_frame,text='Register student',font=('poppins',10,'bold'),bd=0,relief=FLAT,highlightthickness=0,padx=20,pady=8,cursor='hand2',
                      bg='#203c3c',fg='#9fb8b5',activebackground='#203c3c',activeforeground='#9fb8b5',
                      command=lambda: show_page('register'))
register_tab.pack(side=LEFT,padx=(0,6))

# Admin tab (only shows when an admin logs in)
admin_tab = Button(tabs_frame,text='Admin',font=('poppins',10,'bold'),bd=0,relief=FLAT,highlightthickness=0,padx=20,pady=8,cursor='hand2',
                   bg='#203c3c',fg='#9fb8b5',activebackground='#203c3c',activeforeground='#9fb8b5',
                   command=lambda: show_page('admin'))

welcome = Label(header,text='Welcome',font=('poppins',10),fg='white',bg='#203c3c')
welcome.grid(row=0,column=3,padx=(0,25))

staff_dashboard_backbtn = Button(header,text='Log out',font=('poppins',10,'bold'),fg='black',bg='#f59a23',activebackground='#e08a15',relief=FLAT,padx=20,command=staff_dashboard_back)
staff_dashboard_backbtn.grid(row=0,column=4,padx=(0,30))

# ---------- The pages ----------
pages_area = Frame(staff_dashboard_frame,bg='#f2f5f4')
pages_area.grid(row=1,column=0,sticky=NSEW)
pages_area.grid_rowconfigure(0,weight=1)
pages_area.grid_columnconfigure(0,weight=1)

queue_page = Frame(pages_area,bg='#f2f5f4')
finder_page = Frame(pages_area,bg='#f2f5f4')
register_page = Frame(pages_area,bg='#f2f5f4')
admin_page = Frame(pages_area,bg='#f2f5f4')
queue_page.grid_columnconfigure(0,weight=1)
finder_page.grid_columnconfigure(0,weight=1)
register_page.grid_columnconfigure(0,weight=1)
admin_page.grid_columnconfigure(0,weight=1)

pages = {"queue":queue_page,"finder":finder_page,"register":register_page,"admin":admin_page}

def show_page(name):
    for page in pages.values():
        page.grid_remove()
    pages[name].grid(row=0,column=0,sticky=NSEW)
    if name == "admin":
        show_staff_sub()

#================================================================================================================================
#QUEUE PAGE: payment strip (top) + queue list (bottom)
queue_page.grid_columnconfigure(0,weight=1)
queue_page.grid_rowconfigure(1,weight=1)

# ---------- Payment strip ----------
payment_frame = Frame(queue_page,bg='white',padx=24,pady=20)
payment_frame.grid(row=0,column=0,sticky=EW,padx=32,pady=(24,0))
payment_frame.grid_columnconfigure(1,weight=1)

payment_frame_heading = Label(payment_frame,text="New payment",font=("poppins", 15,'bold'),bg='white',fg='black')
payment_frame_heading.grid(row=0,column=0,sticky=W,pady=(0,14))

# ----- left column: Student ID + payment method -----
left_col = Frame(payment_frame,bg='white')
left_col.grid(row=1,column=0,sticky=NW,padx=(0,30))

payment_frame_studentid_label = Label(left_col,text='Student ID',font=('poppins',10),fg='#4d6361',bg='white')
payment_frame_studentid_label.grid(row=0,column=0,sticky=W)

payment_frame_studentid = Entry(left_col,font=("poppins", 12),bg='white',fg='black',width=22)
payment_frame_studentid.grid(row=1,column=0,sticky=EW,pady=(4,0),ipady=4)

method_label = Label(left_col,text='Payment method',font=('poppins',10),fg='#4d6361',bg='white')
method_label.grid(row=2,column=0,sticky=W,pady=(14,0))

payment_var = StringVar()
method_frame = Frame(left_col,bg='white')
method_frame.grid(row=3,column=0,sticky=EW,pady=(4,0))
method_frame.grid_columnconfigure(0,weight=1)
method_frame.grid_columnconfigure(1,weight=1)

cash_check = Radiobutton(method_frame,text="Cash",variable=payment_var,value="Cash",indicatoron=0,font=('poppins',10),bg='white',selectcolor='#f4c9b8',pady=6,relief=GROOVE)
cash_check.grid(row=0,column=0,sticky=EW,padx=(0,6))

online_check = Radiobutton(method_frame,text="Online",variable=payment_var,value="Online",indicatoron=0,font=('poppins',10),bg='white',selectcolor='#f4c9b8',pady=6,relief=GROOVE)
online_check.grid(row=0,column=1,sticky=EW)

# ---------- QR code (for online payments) ----------
qr_pic = Image.open("assets/qr_code.jpg")
qr_pic.thumbnail((320,320))          # makes it smaller but keeps the shape (so it still scans)
qr_image = ImageTk.PhotoImage(qr_pic)

# the little card that holds the QR (hidden at first)
qr_box = Frame(queue_page,bg='white',padx=20,pady=16,highlightbackground='#f59a23',highlightthickness=2)
Label(qr_box,text='Scan to pay online',font=('poppins',12,'bold'),bg='white').pack()
Label(qr_box,image=qr_image,bg='white').pack(pady=(10,0))

qr_shown = False

def toggle_qr():
    global qr_shown
    if qr_shown:
        qr_box.place_forget()                 # hide the card
        qr_button.config(text='Reveal QR')
        qr_shown = False
    else:
        qr_box.place(relx=0.5,rely=0.5,anchor=CENTER)   # show it in the middle
        qr_box.lift()                         # put it on top of everything
        qr_button.config(text='Hide QR')
        qr_shown = True

qr_button = Button(left_col,text='Reveal QR',font=('poppins',10),bg='white',relief=GROOVE,cursor='hand2',command=toggle_qr)
qr_button.grid(row=4,column=0,sticky=EW,pady=(10,0),ipady=2)

# ----- middle column: purpose of payment (tick boxes) -----
mid_col = Frame(payment_frame,bg='white')
mid_col.grid(row=1,column=1,sticky=NSEW)
mid_col.grid_columnconfigure(0,weight=1)
mid_col.grid_rowconfigure(1,weight=1)

purpose_label = Label(mid_col,text='Purpose of payment',font=('poppins',10),fg='#4d6361',bg='white')
purpose_label.grid(row=0,column=0,sticky=W)

purpose_table = Frame(mid_col,bg='white')
purpose_table.grid(row=1,column=0,sticky=NSEW,pady=(2,0))
for c in range(3):
    purpose_table.grid_columnconfigure(c,weight=1,uniform='purpose')
for r in range(2):
    purpose_table.grid_rowconfigure(r,weight=1)

purpose_items = ["Tuition Fee","Books","Uniforms","Registrar Transactions","Others"]

# where each one goes: (row, column, columnspan)
purpose_spots = {
    "Tuition Fee": (0,0,1),
    "Books": (0,1,1),
    "Uniforms": (0,2,1),
    "Registrar Transactions": (1,0,1),
    "Others": (1,1,2),}

purpose_vars = {}
purpose_amounts = {}
purpose_cells = {}
purpose_cell_widgets = {}

def set_cell_look(item, on):
    # ticked boxes get a light orange background and an orange border
    cell_bg = '#fff8ec' if on else 'white'
    border = '#f59a23' if on else '#d5dedd'
    purpose_cells[item].config(bg=cell_bg,highlightbackground=border,highlightcolor=border)
    for w in purpose_cell_widgets[item]:
        w.config(bg=cell_bg)

def update_total():
    total = 0
    for item in purpose_items:
        if purpose_vars[item].get():
            amt = purpose_amounts[item].get().replace(",","").strip()
            try:
                total += float(amt)
            except ValueError:
                pass
    total_label.config(text=f"₱{total:,.2f}")

def toggle_purpose(item):
    # the amount box only works while the purpose is ticked
    on = purpose_vars[item].get()
    if on:
        purpose_amounts[item].config(state=NORMAL)
        purpose_amounts[item].focus()
    else:
        purpose_amounts[item].delete(0,END)
        purpose_amounts[item].config(state=DISABLED)
    set_cell_look(item,on)
    update_total()

for item in purpose_items:
    spot_row, spot_col, spot_span = purpose_spots[item]

    cell = Frame(purpose_table,bg='white',highlightbackground='#d5dedd',highlightcolor='#d5dedd',highlightthickness=1)
    cell.grid(row=spot_row,column=spot_col,columnspan=spot_span,sticky=NSEW,padx=4,pady=4)
    cell.grid_columnconfigure(0,weight=1)
    purpose_cells[item] = cell

    purpose_vars[item] = BooleanVar()
    shown_text = "Others:" if item == "Others" else item
    chk = Checkbutton(cell,text=shown_text,variable=purpose_vars[item],font=('poppins',10),bg='white',
                      activebackground='white',anchor=W,command=lambda i=item: toggle_purpose(i))
    chk.grid(row=0,column=0,sticky=W,padx=(8,4),pady=8)
    cell_widgets = [chk]

    if item == "Others":
        others_text = Entry(cell,font=('poppins',10),width=14)   # what the "Others" payment is for
        others_text.grid(row=0,column=1,padx=(0,8))

    peso = Label(cell,text='₱',font=('poppins',10),bg='white')
    peso.grid(row=0,column=2)
    cell_widgets.append(peso)

    amount_entry = Entry(cell,font=('poppins',10),width=10,state=DISABLED,disabledbackground='#eeeeee',justify=RIGHT)
    amount_entry.grid(row=0,column=3,padx=(2,8))
    amount_entry.bind("<KeyRelease>", lambda e: update_total())
    purpose_amounts[item] = amount_entry
    purpose_cell_widgets[item] = cell_widgets

# ----- right column: total card + Add to queue -----
total_card = Frame(payment_frame,bg='#203c3c',padx=22,pady=16)
total_card.grid(row=1,column=2,sticky=NSEW,padx=(30,0))
total_card.grid_rowconfigure(1,weight=1)

total_text = Label(total_card,text='Total to pay',font=('poppins',10),bg='#203c3c',fg='#9fb8b5')
total_text.grid(row=0,column=0,sticky=W)

total_label = Label(total_card,text='₱0.00',font=('poppins',24,'bold'),bg='#203c3c',fg='#f59a23',width=11,anchor=W)
total_label.grid(row=1,column=0,sticky=NW)

#================================================================================================================================
#Queue List
queue_list_dashboard = Frame(queue_page,bg='white',padx=24,pady=18)
queue_list_dashboard.grid(row=1,column=0,sticky=NSEW,padx=32,pady=(20,28))
queue_list_dashboard.grid_rowconfigure(1,weight=1)
queue_list_dashboard.grid_columnconfigure(0,weight=1)

# ---------- Title + filters, all in one row ----------
filter_bar = Frame(queue_list_dashboard,bg='white')
filter_bar.grid(row=0,column=0,columnspan=2,sticky=EW,pady=(0,12))
filter_bar.grid_columnconfigure(6,weight=1)

queue_list_label = Label(filter_bar,text='Queue list',font=('poppins',15,'bold'),bg='white')
queue_list_label.grid(row=1,column=0,sticky=SW,padx=(0,24))

Label(filter_bar,text='Search',font=('poppins',10),fg='#4d6361',bg='white').grid(row=0,column=1,sticky=W)
search_entry = Entry(filter_bar,font=('poppins',10),width=24)
search_entry.grid(row=1,column=1,padx=(0,14),ipady=3)
search_entry.bind("<KeyRelease>", lambda e: load_queue())

Label(filter_bar,text='Status',font=('poppins',10),fg='#4d6361',bg='white').grid(row=0,column=2,sticky=W)
status_filter = Combobox(filter_bar,values=["All","Waiting","Paid"],font=('poppins',10),width=10,state='readonly')
status_filter.set("All")
status_filter.grid(row=1,column=2,padx=(0,14))
status_filter.bind("<<ComboboxSelected>>", lambda e: load_queue())

Label(filter_bar,text='Method',font=('poppins',10),fg='#4d6361',bg='white').grid(row=0,column=3,sticky=W)
method_filter = Combobox(filter_bar,values=["All","Cash","Online"],font=('poppins',10),width=10,state='readonly')
method_filter.set("All")
method_filter.grid(row=1,column=3,padx=(0,14))
method_filter.bind("<<ComboboxSelected>>", lambda e: load_queue())

Label(filter_bar,text='Date',font=('poppins',10),fg='#4d6361',bg='white').grid(row=0,column=4,sticky=W)
date_filter = Combobox(filter_bar,values=["All","Today"],font=('poppins',10),width=10,state='readonly')
date_filter.set("All")
date_filter.grid(row=1,column=4,padx=(0,14))
date_filter.bind("<<ComboboxSelected>>", lambda e: load_queue())

def clear_filters():
    search_entry.delete(0,END)
    status_filter.set("All")
    method_filter.set("All")
    date_filter.set("All")
    load_queue()

clear_filters_btn = Button(filter_bar,text='Clear',font=('poppins',10),bg='white',relief=GROOVE,padx=10,command=clear_filters)
clear_filters_btn.grid(row=1,column=5)



# ---------- The table (it grows to fill the screen) ----------
queue_columns = ("Entry #","Name", "Student ID","Payment for","Amount","Payment method","Status","Created at")

style = Style()
style.theme_use('clam')
style.configure("Treeview.Heading", font=('Arial',10,'bold'), background='#f59a23', foreground='black')
style.map("Treeview.Heading", background=[('active', '#f59a23')])
style.configure("Treeview", font=('poppins',10), rowheight=30)

queue_list = Treeview(queue_list_dashboard,columns=queue_columns,show='headings',height=10)
queue_list.grid(row=1,column=0,sticky=NSEW)

column_settings = [
    ("Entry #", 70, CENTER),
    ("Name", 220, W),
    ("Student ID", 190, CENTER),
    ("Payment for", 300, W),
    ("Amount", 120, E),
    ("Payment method", 130, CENTER),
    ("Status", 100, CENTER),
    ("Created at", 200, CENTER),]
    
for col_name, col_width, col_anchor in column_settings:
    queue_list.heading(col_name, text=col_name)
    queue_list.column(col_name, width=col_width, anchor=col_anchor)

queue_list.tag_configure('paid', background='#eaf6ef')   # paid rows turn light green

scrollbar = Scrollbar(queue_list_dashboard, orient=VERTICAL, command=queue_list.yview)
queue_list.config(yscrollcommand=scrollbar.set)
scrollbar.grid(row=1, column=1, sticky=NS)
#================================================================================================================================

def get_student_info(student_id):
    # returns (first name, last name, course) or None if not found
    conn = sqlite3.connect("fastq.db")
    cur = conn.cursor()
    cur.execute("SELECT first_name, last_name, course FROM students WHERE student_id=?", (student_id,))
    row = cur.fetchone()
    conn.close()
    return row

def get_balance(student_id, course):
    # course fee minus everything already paid
    conn = sqlite3.connect("fastq.db")
    cur = conn.cursor()
    cur.execute("SELECT total_fee FROM courses WHERE course=?", (course,))
    fee_row = cur.fetchone()
    if fee_row is None:
        conn.close()
        return None   # the student has no course set
    cur.execute("SELECT COALESCE(SUM(amount),0) FROM queue WHERE student_id=? AND status='Paid'", (student_id,))
    paid = cur.fetchone()[0]
    conn.close()
    return fee_row[0] - paid

def load_queue():
    for row in queue_list.get_children():
        queue_list.delete(row)

    query = """SELECT id, name, student_id, payment_for, amount, payment_method, status,
                      datetime(created_at, 'localtime')
               FROM queue WHERE staff=?"""
    params = [current_staff]

    search = search_entry.get().strip()
    if search:
        query += " AND (name LIKE ? OR student_id LIKE ?)"
        params += [f"%{search}%", f"%{search}%"]
    if status_filter.get() != "All":
        query += " AND status=?"
        params.append(status_filter.get())
    if method_filter.get() != "All":
        query += " AND payment_method=?"
        params.append(method_filter.get())
    if date_filter.get() == "Today":
        query += " AND date(created_at,'localtime') = date('now','localtime')"
    query += " ORDER BY id"

    conn = sqlite3.connect("fastq.db")
    cur = conn.cursor()
    cur.execute(query, params)
    rows = cur.fetchall()
    conn.close()

    for r in rows:
        if r[7]:
            time_text = datetime.strptime(r[7], "%Y-%m-%d %H:%M:%S").strftime("%b %d, %Y %I:%M %p")
        else:
            time_text = ""
        tag = 'paid' if r[6] == 'Paid' else ''
        queue_list.insert("", END, values=(r[0], r[1], r[2], r[3], f"₱{r[4]:,.2f}", r[5], r[6], time_text), tags=(tag,))


def add_to_queue():
    student_id = payment_frame_studentid.get().strip()
    payment_method = payment_var.get()

    if not student_id or not payment_method:
        messagebox.showerror("Error", "Please fill up all the fields.")
        return

    chosen = []
    total = 0
    for item in purpose_items:
        if purpose_vars[item].get():
            amt = purpose_amounts[item].get().replace(",", "").strip()
            if not amt or not amt.replace(".", "", 1).isdigit() or float(amt) <= 0:
                messagebox.showerror("Error", f"Please input a valid amount for {item}.")
                return
            label = item
            if item == "Others":
                other_what = others_text.get().strip()
                if not other_what:
                    messagebox.showerror("Error", "Please type what the 'Others' payment is for.")
                    return
                label = f"Others: {other_what}"
            chosen.append(label)
            total += float(amt)

    if not chosen:
        messagebox.showerror("Error", "Please tick at least one purpose of payment.")
        return
    payment_type = ", ".join(chosen)

    student = get_student_info(student_id)
    if student is None:
        messagebox.showerror("Error", "Student ID not found. Please register the student first.")
        return
    name = f"{student[0]} {student[1]}"

    # save to the queue table
    conn = sqlite3.connect("fastq.db")
    cur = conn.cursor()
    cur.execute("""INSERT INTO queue (student_id, name, payment_for, amount, payment_method, staff)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (student_id, name, payment_type, total, payment_method, current_staff))
    conn.commit()
    entry_number = cur.lastrowid
    conn.close()

    load_queue()
    if shown_student_id == student_id:
        show_student(shown_student_id)
    messagebox.showinfo("Added", f"{name} is now in the queue.\nEntry #{entry_number}")

    # clear the form
    payment_frame_studentid.delete(0, END)
    for item in purpose_items:
        purpose_vars[item].set(False)
        toggle_purpose(item)      # also resets the box look and the total
    others_text.delete(0, END)
    payment_var.set('')

get_queue_button = Button(total_card,text="Add to queue",command=add_to_queue,bg='#f59a23',activebackground='#e08a15',relief=FLAT,font=('poppins',11,'bold'),fg='Black')
get_queue_button.grid(row=2,column=0,sticky=EW,pady=(10,0),ipady=4)

def mark_as_paid():
    selected = queue_list.selection() 

    if not selected:
        messagebox.showerror("Error", "Please select an entry in the queue list first.")
        return

    values = queue_list.item(selected[0])['values']
    entry_number = values[0]
    status = values[6]

    if status == "Paid":
        messagebox.showinfo("Info", "This entry is already paid.")
        return

    conn = sqlite3.connect("fastq.db")
    cur = conn.cursor()
    cur.execute("UPDATE queue SET status='Paid' WHERE id=?", (entry_number,))
    conn.commit()
    conn.close()

    load_queue()  
    if shown_student_id:
        show_student(shown_student_id)   # refresh the balance on screen

mark_paid_button = Button(filter_bar,text="Mark as paid",font=('poppins',10,'bold'),fg='white',bg='#1f7a4d',activebackground='#186340',activeforeground='white',relief=FLAT,padx=18,pady=6,command=mark_as_paid)
mark_paid_button.grid(row=1,column=7)

#================================================================================================================================
#STUDENT FINDER PAGE
finder_page.grid_columnconfigure(0,weight=0)
finder_page.grid_columnconfigure(1,weight=1)
finder_page.grid_rowconfigure(0,weight=1)

BAR_WIDTH = 440   # used for wrapping the course name

def load_recent_transactions(student_id):
    for row in recent_list.get_children():
        recent_list.delete(row)
    if not student_id:
        return

    conn = sqlite3.connect("fastq.db")
    cur = conn.cursor()
    cur.execute("""SELECT datetime(created_at,'localtime'), payment_for, amount, payment_method, status
                   FROM queue WHERE student_id=? ORDER BY id DESC LIMIT 8""", (student_id,))
    rows = cur.fetchall()
    conn.close()

    for r in rows:
        date_text = datetime.strptime(r[0], "%Y-%m-%d %H:%M:%S").strftime("%b %d, %Y") if r[0] else ""
        tag = 'paid' if r[4] == 'Paid' else ''
        recent_list.insert("", END, values=(date_text, r[1], f"₱{r[2]:,.2f}", r[3], r[4]), tags=(tag,))


shown_student_id = ""   # remembers which student is on screen

def clear_student_display():  #clear lahat ng naka display sa student card
    global shown_student_id
    shown_student_id = ""
    studentname.config(text="Search a student")
    studentid_label.config(text="-")
    studentcourse.config(text="-")
    balance_label.config(text="-", fg='#f59a23')
    paid_label.config(text="Paid -")
    fee_label.config(text="Total fee -")
    load_recent_transactions("")

def show_student(student_id):
    global shown_student_id
    info = get_student_info(student_id)
    if info is None:
        return False
    first, last, course = info
    balance = get_balance(student_id, course)

    # get the course fee from the database
    conn = sqlite3.connect("fastq.db")
    cur = conn.cursor()
    cur.execute("SELECT total_fee FROM courses WHERE course=?", (course,))
    fee_row = cur.fetchone()
    conn.close()
    if fee_row is None:
        fee = None
    else:
        fee = fee_row[0]
    studentname.config(text=f"{first} {last}")
    studentid_label.config(text=student_id)
    studentcourse.config(text=course)

    if fee is None or balance is None:
        balance_label.config(text="N/A", fg='#f59a23')
        paid_label.config(text="Paid -")
        fee_label.config(text="Total fee -")
    else:
        paid = fee - balance
        balance_label.config(text=f"₱{balance:,.2f}", fg='#6fcf97' if balance <= 0 else '#f59a23')   # green = fully paid
        paid_label.config(text=f"Paid ₱{paid:,.2f}")
        fee_label.config(text=f"Total fee ₱{fee:,.2f}")

    shown_student_id = student_id
    load_recent_transactions(student_id)
    return True

def find():
    student_id = enterstudent_entry.get().strip()
    if not student_id:
        messagebox.showerror("Error", "Please enter a student number.")
        return
    if not show_student(student_id):
        clear_student_display()
        messagebox.showerror("Error", "Student not found.")

# ---------- Left side: search card + student card ----------
finder_left = Frame(finder_page,bg='#f2f5f4')
finder_left.grid(row=0,column=0,sticky=NSEW,padx=(32,0),pady=(24,28))
finder_left.grid_columnconfigure(0,weight=1)

search_card = Frame(finder_left,bg='white',padx=24,pady=20)
search_card.grid(row=0,column=0,sticky=EW)
search_card.grid_columnconfigure(0,weight=1)

studentfinder_label = Label(search_card,text="Find a student",font=('poppins',15,'bold'),bg='white')
studentfinder_label.grid(row=0,column=0,columnspan=2,sticky=W,pady=(0,12))

enterstudent_entry = Entry(search_card,font=('poppins',12),bg='white')
enterstudent_entry.grid(row=1,column=0,sticky=EW,padx=(0,10),ipady=6)
enterstudent_entry.bind("<Return>", lambda e: find())

studentfinder_button = Button(search_card,text="Search",font=('poppins',10,'bold'),bg='#f59a23',activebackground='#e08a15',relief=FLAT,padx=22,command=find)
studentfinder_button.grid(row=1,column=1,sticky=NS)

student_card = Frame(finder_left,bg='#203c3c',padx=28,pady=26)
student_card.grid(row=1,column=0,sticky=EW,pady=(20,0))

studentname = Label(student_card,text="Search a student",font=('poppins',16,'bold'),bg='#203c3c',fg='white',width=24,anchor=W)
studentname.grid(row=0,column=0,columnspan=2,sticky=SW)

studentid_label = Label(student_card,text="-",font=('poppins',10),bg='#203c3c',fg='#9fb8b5',anchor=W)
studentid_label.grid(row=1,column=0,columnspan=2,sticky=NW)

Label(student_card,text="Course",font=('poppins',10),bg='#203c3c',fg='#9fb8b5').grid(row=2,column=0,columnspan=2,sticky=W,pady=(22,0))
studentcourse = Label(student_card,text="-",font=('poppins',12),bg='#203c3c',fg='white',anchor=W,justify=LEFT,wraplength=BAR_WIDTH,height=2)
studentcourse.grid(row=3,column=0,columnspan=2,sticky=NW)

Frame(student_card,height=1,bg='#3d6360').grid(row=4,column=0,columnspan=2,sticky=EW,pady=(10,14))

Label(student_card,text="Remaining balance",font=('poppins',10),bg='#203c3c',fg='#9fb8b5').grid(row=5,column=0,columnspan=2,sticky=W)
balance_label = Label(student_card,text="-",font=('poppins',30,'bold'),bg='#203c3c',fg='#f59a23',width=14,anchor=W)
balance_label.grid(row=6,column=0,columnspan=2,sticky=W)

paid_fee_row = Frame(student_card,bg='#203c3c')
paid_fee_row.grid(row=8,column=0,columnspan=2,sticky=EW,pady=(10,0))
paid_fee_row.grid_columnconfigure(0,weight=1)
paid_label = Label(paid_fee_row,text="Paid -",font=('poppins',10),bg='#203c3c',fg='#9fb8b5')
paid_label.grid(row=0,column=0,sticky=W)
fee_label = Label(paid_fee_row,text="Total fee -",font=('poppins',10),bg='#203c3c',fg='#9fb8b5')
fee_label.grid(row=0,column=1,sticky=E)

# ---------- Right side: recent transactions ----------
recent_card = Frame(finder_page,bg='white',padx=24,pady=20)
recent_card.grid(row=0,column=1,sticky=NSEW,padx=(24,32),pady=(24,28))
recent_card.grid_rowconfigure(1,weight=1)
recent_card.grid_columnconfigure(0,weight=1)

recent_transactions = Label(recent_card,text='Recent transactions',font=('poppins',15,'bold'),bg='white')
recent_transactions.grid(row=0,column=0,sticky=W,pady=(0,12))
Label(recent_card,text='Last 8 payments',font=('poppins',10),bg='white',fg='#4d6361').grid(row=0,column=1,sticky=E)

recent_columns = ("Date","Payment for","Amount","Method","Status")
recent_list = Treeview(recent_card,columns=recent_columns,show='headings',height=10)
recent_list.grid(row=1,column=0,columnspan=2,sticky=NSEW)

recent_widths = [("Date",130,CENTER),("Payment for",300,W),("Amount",130,E),("Method",110,CENTER),("Status",100,CENTER)]
for col_name, col_width, col_anchor in recent_widths:
    recent_list.heading(col_name, text=col_name)
    recent_list.column(col_name, width=col_width, anchor=col_anchor)

recent_list.tag_configure('paid', background='#eaf6ef')   #paid row s turns light green

#============================================
#REGISTER PAGE

register_page.grid_columnconfigure(0,weight=1)

regframe = Frame(register_page,bg='white',padx=44,pady=40,highlightbackground='#dfe6e5',highlightthickness=1)
regframe.grid(row=0,column=0,pady=(60,0),sticky=N)
regframe.grid_columnconfigure(0,weight=1,uniform='names',minsize=230)
regframe.grid_columnconfigure(1,weight=1,uniform='names',minsize=230)

def make_entry(row, column, span=1, padx=(0,0)):
    # a text box with a thin border, same look as the login boxes
    box = Frame(regframe,bg='white',highlightbackground='#c5d0cf',highlightthickness=1)
    box.grid(row=row,column=column,columnspan=span,sticky=EW,padx=padx,pady=(4,0))
    entry = Entry(box,font=('poppins',12),bg='white',relief=FLAT,bd=0)
    entry.pack(fill=X,padx=10,ipady=8)
    return entry

create = Label(regframe,text="Register a student",font=('poppins',22,'bold'),fg='black',bg='white')
create.grid(row=0,column=0,columnspan=2,sticky=W)

create_label = Label(regframe,text='Add a new student profile to the system',font=('poppins',10),fg='gray',bg='white')
create_label.grid(row=1,column=0,columnspan=2,sticky=W,pady=(4,25))

create_firstname = Label(regframe,text='First name',font=('poppins',10),fg='gray',bg='white')
create_firstname.grid(row=2,column=0,sticky=W)
create_firstname_entry = make_entry(3,0,padx=(0,8))

create_lastname = Label(regframe,text='Last name',font=('poppins',10),fg='gray',bg='white')
create_lastname.grid(row=2,column=1,sticky=W,padx=(8,0))
create_lastname_entry = make_entry(3,1,padx=(8,0))

create_studentid = Label(regframe,text='Student ID',font=('poppins',10),fg='gray',bg='white')
create_studentid.grid(row=4,column=0,columnspan=2,sticky=W,pady=(18,0))
create_studentid_entry = make_entry(5,0,span=2)

course_list = list(COURSE_FEES.keys())

create_course = Label(regframe,text='Course',font=('poppins',10),fg='gray',bg='white')
create_course.grid(row=6,column=0,columnspan=2,sticky=W,pady=(18,0))
create_course_combo = Combobox(regframe,values=course_list,font=('poppins',12),state='readonly')
create_course_combo.grid(row=7,column=0,columnspan=2,sticky=EW,pady=(4,0),ipady=6)

style.map('TCombobox',
          fieldbackground=[('readonly','white')],
          selectbackground=[('readonly','white')],
          selectforeground=[('readonly','black')])
def clear_register_fields():
     create_firstname_entry.delete(0,END)
     create_lastname_entry.delete(0,END)
     create_studentid_entry.delete(0,END)
     create_course_combo.set('')

def back():
     # cancel tas clear yung fields
     clear_register_fields()
     show_page('queue')

def createaccount():
          cf = create_firstname_entry.get()
          cl = create_lastname_entry.get()
          cc = create_course_combo.get()
          cs = create_studentid_entry.get()
          if not cf or not cl or not cs or not cc:
               messagebox.showerror("Error","Please input all needed information!")
               return
          if not all(CHAR.isalpha() or CHAR == " " for CHAR in cf):
               messagebox.showerror("Error", "Only letters and spaces allowed in names!")
               return
          if not all(CHAR.isalpha() or CHAR == " " for CHAR in cl):
               messagebox.showerror("Error", "Only letters and spaces allowed in names!")
               return
          if not all(CHAR.isdigit() or CHAR == '-' for CHAR in cs):
               messagebox.showerror("Error", "Student ID must only contain numbers and dashes!")
               return
          if len(cs) != 17:
               messagebox.showerror("Error", "Student ID must be 17 characters!")
               return

          conn = sqlite3.connect("fastq.db")
          cursor = conn.cursor()
          try:
               cursor.execute("""
                    INSERT INTO students (student_id, first_name, last_name, course)
                    VALUES (?, ?, ?, ?)
               """, (cs, cf, cl, cc))
               conn.commit()
          except sqlite3.IntegrityError:
               messagebox.showerror("Error", "Student ID already exists!")
               return
          finally:
               conn.close()   # always closes, even when there's an error

          messagebox.showinfo("Success!", "Successfully registered the student")
          back()

buttons_row = Frame(regframe,bg='white')
buttons_row.grid(row=9,column=0,columnspan=2,sticky=EW,pady=(30,0))
buttons_row.grid_columnconfigure(0,weight=1)
buttons_row.grid_columnconfigure(1,weight=2)

regback = Button(buttons_row,text='Cancel',font=('poppins',12),bg='white',relief=GROOVE,command=back)
regback.grid(row=0,column=0,sticky=EW,padx=(0,10),ipady=4)

create_account = Button(buttons_row,text='Register student',font=('poppins',12,'bold'),fg='black',bg='#f59a23',activebackground='#e08a15',relief=FLAT,command=createaccount)
create_account.grid(row=0,column=1,sticky=EW,ipady=4)

#================================================================================================================================
#ADMIN PAGE: Staff accounts | All queues | Courses & fees | Students
admin_page.grid_rowconfigure(1,weight=1)

admin_subbar = Frame(admin_page,bg='#f2f5f4')
admin_subbar.grid(row=0,column=0,sticky=W,padx=32,pady=(20,0))

admin_content = Frame(admin_page,bg='#f2f5f4')
admin_content.grid(row=1,column=0,sticky=NSEW)
admin_content.grid_rowconfigure(0,weight=1)
admin_content.grid_columnconfigure(0,weight=1)

admin_staff_page = Frame(admin_content,bg='white',padx=24,pady=18)
admin_queue_page = Frame(admin_content,bg='white',padx=24,pady=18)
admin_fees_page = Frame(admin_content,bg='white',padx=24,pady=18)
admin_students_page = Frame(admin_content,bg='white',padx=24,pady=18)
admin_staff_page.grid_columnconfigure(0,weight=1)
admin_queue_page.grid_columnconfigure(0,weight=1)
admin_fees_page.grid_columnconfigure(0,weight=1)
admin_students_page.grid_columnconfigure(0,weight=1)

# ---------- the 4 buttons on top of the admin page ----------
def show_staff_sub():
    admin_queue_page.grid_remove()
    admin_fees_page.grid_remove()
    admin_students_page.grid_remove()
    admin_staff_page.grid(row=0,column=0,sticky=NSEW,padx=32,pady=(12,28))
    load_staff()

def show_queues_sub():
    admin_staff_page.grid_remove()
    admin_fees_page.grid_remove()
    admin_students_page.grid_remove()
    admin_queue_page.grid(row=0,column=0,sticky=NSEW,padx=32,pady=(12,28))
    # put all the staff names in the Staff filter
    conn = sqlite3.connect("fastq.db")
    cur = conn.cursor()
    cur.execute("SELECT username FROM staff UNION SELECT DISTINCT staff FROM queue WHERE staff IS NOT NULL ORDER BY 1")
    names = ["All"]
    for r in cur.fetchall():
        names.append(r[0])
    conn.close()
    aq_staff.config(values=names)
    load_all_queue()

def show_fees_sub():
    admin_staff_page.grid_remove()
    admin_queue_page.grid_remove()
    admin_students_page.grid_remove()
    admin_fees_page.grid(row=0,column=0,sticky=NSEW,padx=32,pady=(12,28))
    load_fees()

def show_students_sub():
    admin_staff_page.grid_remove()
    admin_queue_page.grid_remove()
    admin_fees_page.grid_remove()
    admin_students_page.grid(row=0,column=0,sticky=NSEW,padx=32,pady=(12,28))
    load_students()

staff_sub_btn = Button(admin_subbar,text='Staff accounts',font=('poppins',10,'bold'),bg='white',relief=GROOVE,padx=18,pady=6,cursor='hand2',command=show_staff_sub)
staff_sub_btn.pack(side=LEFT,padx=(0,8))

queues_sub_btn = Button(admin_subbar,text='All queues',font=('poppins',10,'bold'),bg='white',relief=GROOVE,padx=18,pady=6,cursor='hand2',command=show_queues_sub)
queues_sub_btn.pack(side=LEFT,padx=(0,8))

fees_sub_btn = Button(admin_subbar,text='Courses & fees',font=('poppins',10,'bold'),bg='white',relief=GROOVE,padx=18,pady=6,cursor='hand2',command=show_fees_sub)
fees_sub_btn.pack(side=LEFT,padx=(0,8))

students_sub_btn = Button(admin_subbar,text='Students',font=('poppins',10,'bold'),bg='white',relief=GROOVE,padx=18,pady=6,cursor='hand2',command=show_students_sub)
students_sub_btn.pack(side=LEFT,padx=(0,8))

#---------------------------------------------------------------------------------------------------------------------------------
# 1) STAFF ACCOUNTS
admin_staff_page.grid_rowconfigure(2,weight=1)
Label(admin_staff_page,text='Staff accounts',font=('poppins',15,'bold'),bg='white').grid(row=0,column=0,sticky=W,pady=(0,10))

staff_table = Treeview(admin_staff_page,columns=("ID","Username","Role"),show='headings',height=10)
staff_table.grid(row=2,column=0,sticky=NSEW)

staff_column_settings = [("ID",70,CENTER),("Username",300,W),("Role",120,CENTER)]
for col_name, col_width, col_anchor in staff_column_settings:
    staff_table.heading(col_name, text=col_name)
    staff_table.column(col_name, width=col_width, anchor=col_anchor)

staff_scrollbar = Scrollbar(admin_staff_page,orient=VERTICAL,command=staff_table.yview)
staff_table.config(yscrollcommand=staff_scrollbar.set)
staff_scrollbar.grid(row=2,column=1,sticky=NS)

def load_staff():
    for row in staff_table.get_children():
        staff_table.delete(row)
    conn = sqlite3.connect("fastq.db")
    cur = conn.cursor()
    cur.execute("SELECT id, username, role FROM staff ORDER BY id")
    rows = cur.fetchall()
    conn.close()
    for r in rows:
        staff_table.insert("",END,values=r)

def add_staff_account():
    usn = admin_new_user.get().strip()
    pw = admin_new_pw.get()
    role = admin_new_role.get()
    if not usn or not pw:
        messagebox.showerror("Error","Please input a username and a password!")
        return
    if not all(ch.isalnum() or ch == "_" for ch in usn):
        messagebox.showerror("Error","Username can only have letters, numbers, and underscores!")
        return
    if len(usn) < 4:
        messagebox.showerror("Error","Username must be at least 4 characters!")
        return
    if any(ch == " " for ch in pw):
        messagebox.showerror("Error","Password must not include spaces!")
        return
    if len(pw) < 8 or not any(ch.isupper() for ch in pw) or not any(ch.islower() for ch in pw) or not any(ch.isdigit() for ch in pw):
        messagebox.showerror("Error","Password must have 8 characters minimum and have at least one uppercase, one lowercase, and one digit.")
        return
    conn = sqlite3.connect("fastq.db")
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO staff (username, password, role) VALUES (?, ?, ?)",(usn,pw,role))
        conn.commit()
    except sqlite3.IntegrityError:
        messagebox.showerror("Error","That username is already taken!")
        return
    finally:
        conn.close()
    admin_new_user.delete(0,END)
    admin_new_pw.delete(0,END)
    admin_new_role.set("staff")
    load_staff()

def reset_staff_password():
    selected = staff_table.selection()
    if not selected:
        messagebox.showerror("Error","Pick an account from the list first.")
        return
    usn = staff_table.item(selected[0])['values'][1]
    pw = admin_new_pw.get()
    if any(ch == " " for ch in pw):
        messagebox.showerror("Error","Password must not include spaces!")
        return
    if len(pw) < 8 or not any(ch.isupper() for ch in pw) or not any(ch.islower() for ch in pw) or not any(ch.isdigit() for ch in pw):
        messagebox.showerror("Error","Password must have 8 characters minimum and have at least one uppercase, one lowercase, and one digit.")
        return
    conn = sqlite3.connect("fastq.db")
    cur = conn.cursor()
    cur.execute("UPDATE staff SET password=? WHERE username=?",(pw,usn))
    conn.commit()
    conn.close()
    admin_new_pw.delete(0,END)
    messagebox.showinfo("Done",f"Password for {usn} was changed.")

def remove_staff_account():
    selected = staff_table.selection()
    if not selected:
        messagebox.showerror("Error","Pick an account from the list first.")
        return
    usn = staff_table.item(selected[0])['values'][1]
    if usn == "admin":
        messagebox.showerror("Error","The main admin account can't be removed.")
        return
    if usn == current_staff:
        messagebox.showerror("Error","You can't remove the account you are logged in with.")
        return
    if not messagebox.askyesno("Remove",f"Remove the account '{usn}'?\n(Their past queue entries stay in the records.)"):
        return
    conn = sqlite3.connect("fastq.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM staff WHERE username=?",(usn,))
    conn.commit()
    conn.close()
    load_staff()

staff_form = Frame(admin_staff_page,bg='white')
staff_form.grid(row=1,column=0,columnspan=2,sticky=EW,pady=(0,12))

Label(staff_form,text='Username',font=('poppins',10),fg='#4d6361',bg='white').grid(row=0,column=0,sticky=W)
admin_new_user = Entry(staff_form,font=('poppins',10),width=20)
admin_new_user.grid(row=1,column=0,padx=(0,14),ipady=3)

Label(staff_form,text='Password (new or reset)',font=('poppins',10),fg='#4d6361',bg='white').grid(row=0,column=1,sticky=W)
admin_new_pw = Entry(staff_form,font=('poppins',10),width=22,show='*')
admin_new_pw.grid(row=1,column=1,padx=(0,14),ipady=3)

Label(staff_form,text='Role',font=('poppins',10),fg='#4d6361',bg='white').grid(row=0,column=2,sticky=W)
admin_new_role = Combobox(staff_form,values=["staff","admin"],font=('poppins',10),width=8,state='readonly')
admin_new_role.set("staff")
admin_new_role.grid(row=1,column=2,padx=(0,14))

add_staff_btn = Button(staff_form,text='Add staff',font=('poppins',10,'bold'),bg='#f59a23',fg='black',activebackground='#f59a23',relief=FLAT,padx=16,pady=4,cursor='hand2',command=add_staff_account)
add_staff_btn.grid(row=1,column=3,padx=(0,8))

reset_pw_btn = Button(staff_form,text='Reset password',font=('poppins',10,'bold'),bg='#e8eceb',fg='black',activebackground='#e8eceb',relief=FLAT,padx=16,pady=4,cursor='hand2',command=reset_staff_password)
reset_pw_btn.grid(row=1,column=4,padx=(0,8))

remove_staff_btn = Button(staff_form,text='Remove',font=('poppins',10,'bold'),bg='#c0392b',fg='white',activebackground='#c0392b',relief=FLAT,padx=16,pady=4,cursor='hand2',command=remove_staff_account)
remove_staff_btn.grid(row=1,column=5)

#---------------------------------------------------------------------------------------------------------------------------------
# 2) ALL QUEUES (every cashier)
admin_queue_page.grid_rowconfigure(2,weight=1)
Label(admin_queue_page,text='All queues',font=('poppins',15,'bold'),bg='white').grid(row=0,column=0,sticky=W,pady=(0,10))

aq_columns = ("Entry #","Staff","Name","Student ID","Payment for","Amount","Method","Status","Created at")
aq_table = Treeview(admin_queue_page,columns=aq_columns,show='headings',height=10)
aq_table.grid(row=2,column=0,sticky=NSEW)

aq_column_settings = [
    ("Entry #",70,CENTER),
    ("Staff",120,CENTER),
    ("Name",200,W),
    ("Student ID",180,CENTER),
    ("Payment for",280,W),
    ("Amount",110,E),
    ("Method",90,CENTER),
    ("Status",90,CENTER),
    ("Created at",190,CENTER),]
for col_name, col_width, col_anchor in aq_column_settings:
    aq_table.heading(col_name, text=col_name)
    aq_table.column(col_name, width=col_width, anchor=col_anchor)

aq_table.tag_configure('paid', background='#eaf6ef')

aq_scrollbar = Scrollbar(admin_queue_page,orient=VERTICAL,command=aq_table.yview)
aq_table.config(yscrollcommand=aq_scrollbar.set)
aq_scrollbar.grid(row=2,column=1,sticky=NS)

def load_all_queue():
    for row in aq_table.get_children():
        aq_table.delete(row)
    query = """SELECT id, staff, name, student_id, payment_for, amount, payment_method, status,
                      datetime(created_at,'localtime')
               FROM queue WHERE 1=1"""
    params = []
    if aq_staff.get() != "All":
        query += " AND staff=?"
        params.append(aq_staff.get())
    search = aq_search.get().strip()
    if search:
        query += " AND (name LIKE ? OR student_id LIKE ?)"
        params += [f"%{search}%",f"%{search}%"]
    if aq_status.get() != "All":
        query += " AND status=?"
        params.append(aq_status.get())
    if aq_method.get() != "All":
        query += " AND payment_method=?"
        params.append(aq_method.get())
    query += " ORDER BY id"
    conn = sqlite3.connect("fastq.db")
    cur = conn.cursor()
    cur.execute(query,params)
    rows = cur.fetchall()
    conn.close()
    for r in rows:
        if r[8]:
            time_text = datetime.strptime(r[8],"%Y-%m-%d %H:%M:%S").strftime("%b %d, %Y %I:%M %p")
        else:
            time_text = ""
        tag = 'paid' if r[7] == 'Paid' else ''
        aq_table.insert("",END,values=(r[0],r[1],r[2],r[3],r[4],f"₱{r[5]:,.2f}",r[6],r[7],time_text),tags=(tag,))

def clear_aq_filters():
    aq_search.delete(0,END)
    aq_staff.set("All")
    aq_status.set("All")
    aq_method.set("All")
    load_all_queue()

aq_bar = Frame(admin_queue_page,bg='white')
aq_bar.grid(row=1,column=0,columnspan=2,sticky=EW,pady=(0,12))

Label(aq_bar,text='Search',font=('poppins',10),fg='#4d6361',bg='white').grid(row=0,column=0,sticky=W)
aq_search = Entry(aq_bar,font=('poppins',10),width=24)
aq_search.grid(row=1,column=0,padx=(0,14),ipady=3)
aq_search.bind("<KeyRelease>",lambda e: load_all_queue())

Label(aq_bar,text='Staff',font=('poppins',10),fg='#4d6361',bg='white').grid(row=0,column=1,sticky=W)
aq_staff = Combobox(aq_bar,values=["All"],font=('poppins',10),width=14,state='readonly')
aq_staff.set("All")
aq_staff.grid(row=1,column=1,padx=(0,14))
aq_staff.bind("<<ComboboxSelected>>",lambda e: load_all_queue())

Label(aq_bar,text='Status',font=('poppins',10),fg='#4d6361',bg='white').grid(row=0,column=2,sticky=W)
aq_status = Combobox(aq_bar,values=["All","Waiting","Paid"],font=('poppins',10),width=10,state='readonly')
aq_status.set("All")
aq_status.grid(row=1,column=2,padx=(0,14))
aq_status.bind("<<ComboboxSelected>>",lambda e: load_all_queue())

Label(aq_bar,text='Method',font=('poppins',10),fg='#4d6361',bg='white').grid(row=0,column=3,sticky=W)
aq_method = Combobox(aq_bar,values=["All","Cash","Online"],font=('poppins',10),width=10,state='readonly')
aq_method.set("All")
aq_method.grid(row=1,column=3,padx=(0,14))
aq_method.bind("<<ComboboxSelected>>",lambda e: load_all_queue())

aq_clear_btn = Button(aq_bar,text='Clear',font=('poppins',10,'bold'),bg='white',fg='black',activebackground='white',relief=FLAT,padx=16,pady=4,cursor='hand2',command=clear_aq_filters)
aq_clear_btn.grid(row=1,column=4)

#---------------------------------------------------------------------------------------------------------------------------------
# 3) COURSES & FEES
admin_fees_page.grid_rowconfigure(1,weight=1)
Label(admin_fees_page,text='Courses & fees',font=('poppins',15,'bold'),bg='white').grid(row=0,column=0,sticky=W,pady=(0,10))

fees_table = Treeview(admin_fees_page,columns=("Course","Fee"),show='headings',height=10)
fees_table.grid(row=1,column=0,sticky=NSEW)

fees_column_settings = [("Course",520,W),("Fee",200,E)]
for col_name, col_width, col_anchor in fees_column_settings:
    fees_table.heading(col_name, text=col_name)
    fees_table.column(col_name, width=col_width, anchor=col_anchor)

fees_scrollbar = Scrollbar(admin_fees_page,orient=VERTICAL,command=fees_table.yview)
fees_table.config(yscrollcommand=fees_scrollbar.set)
fees_scrollbar.grid(row=1,column=1,sticky=NS)

def load_fees():
    for row in fees_table.get_children():
        fees_table.delete(row)
    conn = sqlite3.connect("fastq.db")
    cur = conn.cursor()
    cur.execute("SELECT course, total_fee FROM courses ORDER BY course")
    rows = cur.fetchall()
    conn.close()
    for r in rows:
        fees_table.insert("",END,values=(r[0],f"₱{r[1]:,.2f}"))

def on_fee_select(event):
    selected = fees_table.selection()
    if not selected:
        return
    values = fees_table.item(selected[0])['values']
    fee_selected.config(text=values[0])
    fee_entry.delete(0,END)
    fee_entry.insert(0,str(values[1]).replace("₱","").replace(",",""))

def save_fee():
    selected = fees_table.selection()
    if not selected:
        messagebox.showerror("Error","Pick a course from the list first.")
        return
    course = fees_table.item(selected[0])['values'][0]
    amt = fee_entry.get().replace(",","").strip()
    if not amt or not amt.replace(".","",1).isdigit() or float(amt) <= 0:
        messagebox.showerror("Error","Please input a valid fee.")
        return
    conn = sqlite3.connect("fastq.db")
    cur = conn.cursor()
    cur.execute("UPDATE courses SET total_fee=? WHERE course=?",(float(amt),course))
    conn.commit()
    conn.close()
    load_fees()
    if shown_student_id:
        show_student(shown_student_id)   # refresh the balance on the Student Finder
    messagebox.showinfo("Saved",f"New fee for {course}: ₱{float(amt):,.2f}")

fees_table.bind("<<TreeviewSelect>>",on_fee_select)

fee_edit = Frame(admin_fees_page,bg='white')
fee_edit.grid(row=2,column=0,columnspan=2,sticky=EW,pady=(12,0))
fee_selected = Label(fee_edit,text='Pick a course from the list',font=('poppins',10,'bold'),bg='white',width=46,anchor=W)
fee_selected.grid(row=0,column=0,padx=(0,14))
Label(fee_edit,text='New fee ₱',font=('poppins',10),bg='white').grid(row=0,column=1)
fee_entry = Entry(fee_edit,font=('poppins',10),width=14,justify=RIGHT)
fee_entry.grid(row=0,column=2,padx=(4,14),ipady=3)
save_fee_btn = Button(fee_edit,text='Save fee',font=('poppins',10,'bold'),bg='#f59a23',fg='black',activebackground='#f59a23',relief=FLAT,padx=16,pady=4,cursor='hand2',command=save_fee)
save_fee_btn.grid(row=0,column=3)

#---------------------------------------------------------------------------------------------------------------------------------
# 4) STUDENT RECORDS
admin_students_page.grid_rowconfigure(2,weight=1)
Label(admin_students_page,text='Student records',font=('poppins',15,'bold'),bg='white').grid(row=0,column=0,sticky=W,pady=(0,10))

students_table = Treeview(admin_students_page,columns=("Student ID","First name","Last name","Course"),show='headings',height=10)
students_table.grid(row=2,column=0,sticky=NSEW)

students_column_settings = [("Student ID",190,CENTER),("First name",200,W),("Last name",200,W),("Course",400,W)]
for col_name, col_width, col_anchor in students_column_settings:
    students_table.heading(col_name, text=col_name)
    students_table.column(col_name, width=col_width, anchor=col_anchor)

students_scrollbar = Scrollbar(admin_students_page,orient=VERTICAL,command=students_table.yview)
students_table.config(yscrollcommand=students_scrollbar.set)
students_scrollbar.grid(row=2,column=1,sticky=NS)

def load_students():
    for row in students_table.get_children():
        students_table.delete(row)
    query = "SELECT student_id, first_name, last_name, course FROM students"
    params = []
    search = st_search.get().strip()
    if search:
        query += " WHERE student_id LIKE ? OR first_name LIKE ? OR last_name LIKE ?"
        params = [f"%{search}%", f"%{search}%", f"%{search}%"]
    query += " ORDER BY last_name, first_name"
    conn = sqlite3.connect("fastq.db")
    cur = conn.cursor()
    cur.execute(query,params)
    rows = cur.fetchall()
    conn.close()
    for r in rows:
        students_table.insert("",END,values=r)

def clear_student_form():
    st_first.delete(0,END)
    st_last.delete(0,END)
    st_course.set('')

def on_student_select(event):
    selected = students_table.selection()
    if not selected:
        return
    values = students_table.item(selected[0])['values']
    clear_student_form()
    st_first.insert(0,values[1])
    st_last.insert(0,values[2])
    st_course.set(values[3])

def save_student_changes():
    selected = students_table.selection()
    if not selected:
        messagebox.showerror("Error","Pick a student from the list first.")
        return
    sid = str(students_table.item(selected[0])['values'][0])
    first = st_first.get().strip()
    last = st_last.get().strip()
    course = st_course.get()
    if not first or not last or not course:
        messagebox.showerror("Error","Please input all needed information!")
        return
    if not all(ch.isalpha() or ch == " " for ch in first + last):
        messagebox.showerror("Error","Only letters and spaces allowed in names!")
        return
    conn = sqlite3.connect("fastq.db")
    cur = conn.cursor()
    cur.execute("UPDATE students SET first_name=?, last_name=?, course=? WHERE student_id=?",(first,last,course,sid))
    cur.execute("UPDATE queue SET name=? WHERE student_id=?",(f"{first} {last}",sid))   # fix the name on old queue entries too
    conn.commit()
    conn.close()
    load_students()
    load_queue()
    if shown_student_id == sid:
        show_student(sid)
    clear_student_form()
    messagebox.showinfo("Saved","Student record updated.")

def delete_student():
    selected = students_table.selection()
    if not selected:
        messagebox.showerror("Error","Pick a student from the list first.")
        return
    sid = str(students_table.item(selected[0])['values'][0])
    if not messagebox.askyesno("Delete",f"Delete student {sid}?\n(Their past payments stay in the queue records.)"):
        return
    conn = sqlite3.connect("fastq.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM students WHERE student_id=?",(sid,))
    conn.commit()
    conn.close()
    if shown_student_id == sid:
        clear_student_display()
    load_students()
    clear_student_form()

students_table.bind("<<TreeviewSelect>>",on_student_select)

st_bar = Frame(admin_students_page,bg='white')
st_bar.grid(row=1,column=0,columnspan=2,sticky=EW,pady=(0,12))
Label(st_bar,text='Search',font=('poppins',10),fg='#4d6361',bg='white').grid(row=0,column=0,sticky=W)
st_search = Entry(st_bar,font=('poppins',10),width=30)
st_search.grid(row=1,column=0,ipady=3)
st_search.bind("<KeyRelease>",lambda e: load_students())

st_form = Frame(admin_students_page,bg='white')
st_form.grid(row=3,column=0,columnspan=2,sticky=EW,pady=(12,0))
Label(st_form,text='First name',font=('poppins',10),fg='#4d6361',bg='white').grid(row=0,column=0,sticky=W)
st_first = Entry(st_form,font=('poppins',10),width=18)
st_first.grid(row=1,column=0,padx=(0,14),ipady=3)
Label(st_form,text='Last name',font=('poppins',10),fg='#4d6361',bg='white').grid(row=0,column=1,sticky=W)
st_last = Entry(st_form,font=('poppins',10),width=18)
st_last.grid(row=1,column=1,padx=(0,14),ipady=3)
Label(st_form,text='Course',font=('poppins',10),fg='#4d6361',bg='white').grid(row=0,column=2,sticky=W)
st_course = Combobox(st_form,values=course_list,font=('poppins',10),width=40,state='readonly')
st_course.grid(row=1,column=2,padx=(0,14))

save_student_btn = Button(st_form,text='Save changes',font=('poppins',10,'bold'),bg='#f59a23',fg='black',activebackground='#f59a23',relief=FLAT,padx=16,pady=4,cursor='hand2',command=save_student_changes)
save_student_btn.grid(row=1,column=3,padx=(0,8))

delete_student_btn = Button(st_form,text='Delete',font=('poppins',10,'bold'),bg='#c0392b',fg='white',activebackground='#c0392b',relief=FLAT,padx=16,pady=4,cursor='hand2',command=delete_student)
delete_student_btn.grid(row=1,column=4)

load_queue()

window.mainloop()