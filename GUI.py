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
        cursor.execute("INSERT OR REPLACE INTO courses (course, total_fee) VALUES (?, ?)", (course_name, fee))
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
User_icon = PhotoImage(file="assets/FastQ Logo.png").subsample(16,16)

window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

pic = Image.open("assets/eye_open.jpg")
pic =  pic.resize((50,50))
pic2 = Image.open("assets/eye_closed.jpg")
pic2 =  pic2.resize((50,50))

eye_open = ImageTk.PhotoImage(pic)
eye_closed = ImageTk.PhotoImage(pic2)

#=======================================================
#Main frame/Choice frame
mainframe = Frame(window,bg='white')
mainframe.grid()
welcome = Label(mainframe,text='Welcome to FastQ',font=('poppins',30,'bold'),fg='Black',bg='white',image=User_icon,compound='left',padx=20)
welcome.grid(row=0,column=0,columnspan=2,pady=0)

text = Label(mainframe,text="Let's get you sorted out!",font=('poppins',10),fg='Black',bg='white')
text.grid(row=1,columnspan=2,pady=(0,80))



     
#=======================================================================================================================================
#Staff login frame

staff_frame = Frame(mainframe,bg='white')
staff_frame.grid()
username_label = Label(staff_frame,text='Username',font=('poppins',15),bg='white')
username_label.grid(row=1,column=0,sticky=W,padx=(0,190),columnspan=2)

username2 = Entry(staff_frame,font=('poppins', 20),bg='white')
username2.grid(row=2,column=0,columnspan=2)

password_label2 = Label(staff_frame,text='Password',font=('poppins',15),bg='white')
password_label2.grid(row=3,column=0,padx=(0,240),columnspan=2)

password2 = Entry(staff_frame,font=('poppins', 20),bg='white',show='*')
password2.grid(row=4,column=0,columnspan=2)

isShown2 = False

def show2():
     global isShown2
     if isShown2:
          password2.config(show="*")
          isShown2 = False
          show_password2.config(image=eye_closed)
     else:
          password2.config(show="")
          isShown2 = True
          show_password2.config(image=eye_open)



show_password2 = Button(staff_frame,command=show2,image=eye_closed,bg='white',bd=0,relief=GROOVE)
show_password2.grid(row=4,column=3,columnspan=2)

#REMOVE IF TAPOS NA

username2.insert(0,'admin')
password2.insert(0,'1234')

##remove til here


current_staff = ""
def stafflogin():
     global current_staff
     usn2 = username2.get()
     pw2 = password2.get()

     conn = sqlite3.connect("fastq.db")
     cur = conn.cursor()
     cur.execute('SELECT * FROM staff WHERE username=? AND password=?', (usn2, pw2))
     found = cur.fetchone()
     conn.close()

     if found or (usn2 == 'admin' and pw2 == "1234"):
          current_staff = usn2
          welcome2.config(text=f'Welcome, {current_staff}!')
          clear_filters()
          mainframe.grid_remove()
          staff_dashboard_frame.grid(sticky=NSEW)
          window.config(background="#f2f5f4")
     else:
          messagebox.showerror("Error", "You entered wrong username or password!")
          password2.delete(0,END)

login_btn2 = Button(staff_frame,text='Log in',font=('poppins',12),fg = 'white',command=stafflogin,bg='#203c3c')
login_btn2.grid(row=5,column=0,columnspan=2,pady=(30,60))
#=======================================================================================================================================
#Create account frame
create_frame = Frame(mainframe,bg='white')  

new_username_label = Label(create_frame,text='Username',font=('poppins',15),bg='white')
new_username_label.grid(row=1,column=0,sticky=W,padx=(0,190),columnspan=2)

new_username = Entry(create_frame,font=('poppins', 20),bg='white')
new_username.grid(row=2,column=0,columnspan=2)

new_password_label = Label(create_frame,text='Password',font=('poppins',15),bg='white')
new_password_label.grid(row=3,column=0,sticky=W,padx=(0,190),columnspan=2)

new_password = Entry(create_frame,font=('poppins', 20),bg='white',show='*')
new_password.grid(row=4,column=0,columnspan=2)

confirm_password_label = Label(create_frame,text='Confirm Password',font=('poppins',15),bg='white')
confirm_password_label.grid(row=5,column=0,sticky=W,padx=(0,190),columnspan=2)

confirm_password = Entry(create_frame,font=('poppins', 20),bg='white',show='*')
confirm_password.grid(row=6,column=0,columnspan=2)

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

show_password3 = Button(create_frame,command=show3,image=eye_closed,bg='white',bd=0,relief=GROOVE)
show_password3.grid(row=4,column=3,columnspan=2)


def back_to_login():
     create_frame.grid_forget()
     staff_frame.grid()

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

     # 5. save to the database
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

create_btn = Button(create_frame,text='Create account',font=('poppins',12),fg = 'white',command=save_account,bg='#203c3c')
create_btn.grid(row=7,column=0,columnspan=2,pady=(30,10))

back_label = Label(create_frame,text='Already have an account?',font=('poppins',10),bg='white')
back_label.grid(row=8,column=0,pady=(0,60),padx=(0,10))

back_button = Button(create_frame,text='Back to log in',font=('poppins',12,'underline'),command=back_to_login,bd=0,bg='white')
back_button.grid(row=8,column=1,pady=(0,60))
#=======================================================================================================================================
#Button on the log in page
def create_newaccount():
     staff_frame.grid_remove()   # hide the log in page
     create_frame.grid()         # show the create account page

create_newaccount_label = Label(staff_frame,text="Don't have an account yet?",font=('poppins',10),bg='white')
create_newaccount_label.grid(row=6,column=0,pady=(0,60),padx=(0,10))

create_newaccount_button = Button(staff_frame,text='Create a new account',font=('poppins',12,'underline'),command=create_newaccount,bd=0,bg='white')
create_newaccount_button.grid(row=6,column=1,pady=(0,60))


#=============================================================
#Staff dashboard
staff_dashboard_frame = Frame(window,bg='#f2f5f4')



def register():
     staff_dashboard_frame.grid_remove()
     window.config(background="white")
     regframe.grid()

def staff_dashboard_back():
     staff_dashboard_frame.grid_remove()
     window.config(background="white")
     mainframe.grid()

header = Frame(staff_dashboard_frame,bg='#203c3c')
header.grid(row=0,column=0,columnspan=2,sticky=EW,pady=(0,30))
header.grid_columnconfigure(1,weight=1)

FastQ_header= Label(header,text='FastQ',font=('poppins',18,'bold'),fg='white',bg='#203c3c',image=User_icon,compound='left',padx=10)
FastQ_header.grid(row=0,column=0,padx=(30,0),pady=10)

staff_dashboard_label = Label(header,text='Staff dashboard',font=('poppins',10),fg='#9fb8b5',bg='#203c3c')
staff_dashboard_label.grid(row=0,column=1,sticky=W,padx=(15,0))

welcome2 = Label(header,text='Welcome',font=('poppins',10),fg='white',bg='#203c3c')
welcome2.grid(row=0,column=2,padx=(0,25))

register_btn = Button(header,text='Register a student profile',font=('poppins',10),fg='white',bg='#203c3c',activebackground='#2d5250',activeforeground='white',relief=GROOVE,bd=1,command=register)
register_btn.grid(row=0,column=3,padx=(0,10))

staff_dashboard_backbtn = Button(header,text='Back',font=('poppins',10,'bold'),fg='black',bg='#f59a23',activebackground='#e08a15',relief=FLAT,padx=20,command=staff_dashboard_back)
staff_dashboard_backbtn.grid(row=0,column=4,padx=(0,30))

staff_dashboard_frame.grid_columnconfigure(0,weight=1)
staff_dashboard_frame.grid_columnconfigure(1,weight=1)
staff_dashboard_frame.grid_rowconfigure(10,weight=1)
#================================================================================================================================
#Queue List
queue_list_dashboard = Frame(staff_dashboard_frame,bg='white',bd=2,relief=FLAT)
queue_list_dashboard.grid(row=2,column=0,columnspan=2,pady=(30,0))

queue_list_label = Label(queue_list_dashboard,text='Queue list: ',font=('poppins',15,"bold"),bg="white")



queue_columns = ("Entry #","Name", "Student ID","Payment for","Amount","Payment method","Status","Created at")


style = Style()
style.theme_use('clam')
style.configure("Treeview.Heading", font=('Arial',10,'bold'), background='#f59a23', foreground='black')
style.map("Treeview.Heading", background=[('active', '#f59a23')])

queue_list = queue_list = Treeview(queue_list_dashboard,columns=queue_columns,show='headings',height=15)
queue_list.grid(column=0,columnspan=3,row=2)

column_settings = [
    ("Entry #", 60, CENTER),
    ("Name", 170, W),
    ("Student ID", 150, CENTER),
    ("Payment for", 220, CENTER),
    ("Amount", 90, E),
    ("Payment method", 120, CENTER),
    ("Status", 70, CENTER),
    ("Created at", 170, CENTER),]
    
for col_name, col_width, col_anchor in column_settings:
    queue_list.heading(col_name, text=col_name)
    queue_list.column(col_name, width=col_width, anchor=col_anchor)

queue_list_label.grid(row=0,column=0,sticky=W)
scrollbar = Scrollbar(queue_list_dashboard, orient=VERTICAL, command=queue_list.yview)
queue_list.config(yscrollcommand=scrollbar.set)
scrollbar.grid(row=2, column=3, sticky=NS)

# ---------- Filter bar ----------
filter_bar = Frame(queue_list_dashboard,bg='white')
filter_bar.grid(row=1,column=0,columnspan=4,sticky=EW,pady=(0,10))

Label(filter_bar,text='Search',font=('poppins',10),bg='white').grid(row=0,column=0,sticky=W)
search_entry = Entry(filter_bar,font=('poppins',10),width=22)
search_entry.grid(row=1,column=0,padx=(0,15))
search_entry.bind("<KeyRelease>", lambda e: load_queue())

Label(filter_bar,text='Status',font=('poppins',10),bg='white').grid(row=0,column=1,sticky=W)
status_filter = Combobox(filter_bar,values=["All","Waiting","Paid"],font=('poppins',10),width=9,state='readonly')
status_filter.set("All")
status_filter.grid(row=1,column=1,padx=(0,15))
status_filter.bind("<<ComboboxSelected>>", lambda e: load_queue())

Label(filter_bar,text='Method',font=('poppins',10),bg='white').grid(row=0,column=2,sticky=W)
method_filter = Combobox(filter_bar,values=["All","Cash","Online"],font=('poppins',10),width=9,state='readonly')
method_filter.set("All")
method_filter.grid(row=1,column=2,padx=(0,15))
method_filter.bind("<<ComboboxSelected>>", lambda e: load_queue())

Label(filter_bar,text='Date',font=('poppins',10),bg='white').grid(row=0,column=3,sticky=W)
date_filter = Combobox(filter_bar,values=["All","Today"],font=('poppins',10),width=9,state='readonly')
date_filter.set("All")
date_filter.grid(row=1,column=3,padx=(0,15))
date_filter.bind("<<ComboboxSelected>>", lambda e: load_queue())

def clear_filters():
    search_entry.delete(0,END)
    status_filter.set("All")
    method_filter.set("All")
    date_filter.set("All")
    load_queue()

clear_filters_btn = Button(filter_bar,text='Clear',font=('poppins',10),bg='white',relief=GROOVE,command=clear_filters)
clear_filters_btn.grid(row=1,column=4,padx=(0,15))

result_label = Label(filter_bar,text='',font=('poppins',10),fg='#4d6361',bg='white')
result_label.grid(row=1,column=5,sticky=E)
filter_bar.grid_columnconfigure(5,weight=1)
#================================================================================================================================
#Payment frame
payment_frame = Frame(staff_dashboard_frame,bg='white',relief=RIDGE,border=1,padx=20,pady=20)
payment_frame.grid(row=1,column=0,sticky=NE,padx=(0,10))
def payment_frame_back():
    payment_frame.grid_remove()
    student_finder_frame.grid()

payment_frame_heading = Label(payment_frame,text="Payment form",font=("poppins", 15,'bold'),bg='white',fg='black')
payment_frame_heading.grid(row=0,column=0,columnspan=3,pady=(0,15),sticky=W)

payment_frame_studentid_label = Label(payment_frame,text='Student ID',font=('poppins',10),bg='white')
payment_frame_studentid_label.grid(row=1,column=0,columnspan=2,sticky=W)

payment_frame_studentid = Entry(payment_frame,font=("poppins", 12),bg='white',fg='black',width=20)
payment_frame_studentid.grid(row=2,column=0,columnspan=2,sticky=W)

# ---------- Purpose of payment (tick boxes) ----------
purpose_label = Label(payment_frame,text='Purpose of Payment',font=('poppins',10),bg='white')
purpose_label.grid(row=3,column=0,columnspan=3,sticky=W,pady=(15,0))

purpose_table = Frame(payment_frame,bg='white')
purpose_table.grid(row=4,column=0,columnspan=3,sticky=EW,pady=(5,0))
purpose_table.grid_columnconfigure(0,weight=1,uniform='purpose')
purpose_table.grid_columnconfigure(1,weight=1,uniform='purpose')

purpose_items = ["Tuition Fee","Books","Uniforms","Registrar Transactions","Others"]

# where each one goes: (row, column, columnspan)
purpose_spots = {
    "Tuition Fee": (0,0,1),
    "Books": (0,1,1),
    "Uniforms": (1,0,1),
    "Registrar Transactions": (1,1,1),
    "Others": (2,0,2),}


purpose_vars = {}
purpose_amounts = {}

def toggle_purpose(item):
    # the amount box only works while the purpose is ticked
    if purpose_vars[item].get():
        purpose_amounts[item].config(state=NORMAL)
        purpose_amounts[item].focus()
    else:
        purpose_amounts[item].delete(0,END)
        purpose_amounts[item].config(state=DISABLED)

for item in purpose_items:
    spot_row, spot_col, spot_span = purpose_spots[item]

    cell = Frame(purpose_table,bg='white',highlightbackground='black',highlightthickness=1)
    cell.grid(row=spot_row,column=spot_col,columnspan=spot_span,sticky=NSEW)
    cell.grid_columnconfigure(0,weight=1)

    purpose_vars[item] = BooleanVar()
    shown_text = "Others:" if item == "Others" else item
    Checkbutton(cell,text=shown_text,variable=purpose_vars[item],font=('poppins',10),bg='white',
                activebackground='white',anchor=W,command=lambda i=item: toggle_purpose(i)).grid(row=0,column=0,sticky=W,padx=10,pady=6)

    if item == "Others":
        others_text = Entry(cell,font=('poppins',10),width=10)   # what the "Others" payment is for
        others_text.grid(row=0,column=1,padx=(0,10))

    Label(cell,text='₱',font=('poppins',10),bg='white').grid(row=0,column=2)
    purpose_amounts[item] = Entry(cell,font=('poppins',10),width=10,state=DISABLED,disabledbackground='#eeeeee')
    purpose_amounts[item].grid(row=0,column=3,padx=(2,10))

# ---------- Cash / Online ----------
payment_var = StringVar()

cash_check = Radiobutton(payment_frame,text="Cash",variable=payment_var,value="Cash",indicatoron=0,font=('poppins',10),bg='white',selectcolor='#f4c9b8',width=14,pady=6,relief=GROOVE)
cash_check.grid(row=5,column=0,padx=(0,10),pady=(15,0),sticky=W)

online_check = Radiobutton(payment_frame,text="Online Payment",variable=payment_var,value="Online",indicatoron=0,font=('poppins',10),bg='white',selectcolor='#f4c9b8',width=14,pady=6,relief=GROOVE)
online_check.grid(row=5,column=1,pady=(15,0),sticky=W)

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
        queue_list.insert("", END, values=(r[0], r[1], r[2], r[3], f"₱{r[4]:,.2f}", r[5], r[6], time_text))

    result_label.config(text=f"Showing {len(rows)} entries")

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
    messagebox.showinfo("Added", f"{name} is now in the queue.\nEntry #{entry_number}")

    # clear the form
    payment_frame_studentid.delete(0, END)
    for item in purpose_items:
        purpose_vars[item].set(False)
        toggle_purpose(item)
    others_text.delete(0, END)
    payment_var.set('')
    
         

get_queue_button = Button(payment_frame,text="Add to queue",command=add_to_queue,bg='#f59a23',font=('poppins',10),fg='Black')
get_queue_button.grid(row=5,column=2,sticky=E,pady=(15,0))

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

mark_paid_button = Button(queue_list_dashboard,text="Mark as paid",font=('poppins',10),fg='white',bg='#1f7a4d',command=mark_as_paid)
mark_paid_button.grid(row=0,column=2,sticky=E,pady=(10,10))

load_queue()
#STUDENT FINDER

shown_student_id = ""   # remembers which student is on screen

def load_recent_transactions(student_id):
    for row in recent_list.get_children():
        recent_list.delete(row)
    if not student_id:
        return

    conn = sqlite3.connect("fastq.db")
    cur = conn.cursor()
    cur.execute("""SELECT datetime(created_at,'localtime'), payment_for, amount, status
                   FROM queue WHERE student_id=? ORDER BY id DESC LIMIT 5""", (student_id,))
    rows = cur.fetchall()
    conn.close()

    for r in rows:
        date_text = datetime.strptime(r[0], "%Y-%m-%d %H:%M:%S").strftime("%b %d, %Y") if r[0] else ""
        tag = 'paid' if r[3] == 'Paid' else ''
        recent_list.insert("", END, values=(date_text, r[1], f"₱{r[2]:,.2f}", r[3]), tags=(tag,))

def clear_student_display():
    global shown_student_id
    shown_student_id = ""
    studentname.config(text="Search a student", fg="gray")
    studentcourse.config(text="Course: -")
    balance_label.config(text="-", fg='#f59a23')
    load_recent_transactions("")



def show_student(student_id):
    global shown_student_id
    info = get_student_info(student_id)
    if info is None:
        return False
    first, last, course = info
    balance = get_balance(student_id, course)

    studentname.config(text=f"{first} {last}", fg="white")
    studentcourse.config(text=f"Course: {course}")
    if balance is None:
        balance_label.config(text="N/A", fg='#f59a23')
    elif balance <= 0:
        balance_label.config(text=f"₱{balance:,.2f}", fg='#6fcf97')   # fully paid = green
    else:
        balance_label.config(text=f"₱{balance:,.2f}", fg='#f59a23')
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

student_finder_frame = Frame(staff_dashboard_frame,bg='white',bd=1,relief=RIDGE,padx=20,pady=20)
student_finder_frame.grid(row=1,column=1,sticky=NW,padx=(10,0))



studentfinder_label = Label(student_finder_frame,text="Student Finder",font=('poppins',15,'bold'),bg='white')
studentfinder_label.grid(row=0,column=0,columnspan=2,sticky=W,pady=(0,15))


enterstudent_label = Label(student_finder_frame,text="Student number",bg='white',font=('poppins',10))
enterstudent_label.grid(row=1,column=0,columnspan=2,sticky=W)


enterstudent_entry = Entry(student_finder_frame,font=('poppins',12),relief=RIDGE,bd=1)
enterstudent_entry.grid(row=2,column=0,sticky=EW,padx=(0,10))

studentfinder_button = Button(student_finder_frame,text="Search",font=('poppins',10),bg='#203c3c',fg='white',command=find)
studentfinder_button.grid(row=2,column=1,sticky=E)

balance_frame = Frame(student_finder_frame,relief=FLAT,bg='#203c3c',padx=20,pady=15)
balance_frame.grid(row=3,column=0,columnspan=2,sticky=EW,pady=(20,0))
balance_frame.grid_columnconfigure(0,weight=1)

studentname_label = Label(balance_frame,font=('poppins',10),text="Student name",bg='#203c3c',fg='#9fb8b5')
studentname_label.grid(row=0,column=0,sticky=W)

studentname = Label(balance_frame,font=('poppins',12),text="Search a student",fg="gray",bg='#203c3c',width=22,anchor=W,justify=LEFT,wraplength=260,height=2)
studentname.grid(row=1,column=0,sticky=W)

balance_text = Label(balance_frame,text="Remaining balance",font=('poppins',10),bg='#203c3c',fg='#9fb8b5')
balance_text.grid(row=0,column=1,sticky=E)

balance_label = Label(balance_frame,text="-",font=('poppins',20,'bold'),bg='#203c3c',fg='#f59a23',width=10,anchor=E)
balance_label.grid(row=1,column=1,sticky=E)

studentcourse = Label(balance_frame,font=('poppins',10),text="Course: -",fg='white',bg='#203c3c',anchor=W,justify=LEFT,wraplength=380,height=2)
studentcourse.grid(row=2,column=0,columnspan=2,sticky=EW,pady=(8,0))

recent_transactions = Label(student_finder_frame,text='Recent transactions',font=('poppins',12,'bold'),bg='white',fg='black')
recent_transactions.grid(row=4,column=0,columnspan=2,sticky=W,pady=(20,0))

recent_columns = ("Date","Payment for","Amount","Status")
recent_list = Treeview(student_finder_frame,columns=recent_columns,show='headings',height=5)
recent_list.grid(row=5,column=0,columnspan=2,sticky=EW,pady=(8,0))

recent_list.heading("Date", text="Date")
recent_list.heading("Payment for", text="Payment for")
recent_list.heading("Amount", text="Amount")
recent_list.heading("Status", text="Status")

recent_list.column("Date", width=100, anchor=CENTER)
recent_list.column("Payment for", width=170, anchor=W)
recent_list.column("Amount", width=90, anchor=E)
recent_list.column("Status", width=70, anchor=CENTER)

recent_list.tag_configure('paid', background='#eaf6ef')   # paid rows turn light green
#============================================
#Account registration



regframe = Frame(window,background='white',padx=300)
create = Label(regframe,text="Create new account",font=('poppins',20,'bold'),fg='Black',bg='White',image=User_icon,compound='left')
create.grid(row=0,column=0,columnspan=2,pady=(0,70))
     
form_width = 30   # change this one number to make ALL the boxes bigger or smaller

create_firstname = Label(regframe, text='First name',font=('Poppins',15),bg='white')
create_firstname.grid(row=1,column=0,columnspan=2,sticky=W)
create_firstname_entry = Entry(regframe,font=('poppins',15),bg='white',width=form_width)
create_firstname_entry.grid(row=2,column=0,columnspan=2,sticky=EW)

create_lastname = Label(regframe, text='Last name',font=('Poppins',15),bg='white')
create_lastname.grid(row=3,column=0,columnspan=2,sticky=W,pady=(10,0))
create_lastname_entry = Entry(regframe,font=('poppins',15),bg='white',width=form_width)
create_lastname_entry.grid(row=4,column=0,columnspan=2,sticky=EW)

create_studentid = Label(regframe, text='Student ID',font=('Poppins',15),bg='white')
create_studentid.grid(row=5,column=0,columnspan=2,sticky=W,pady=(10,0))
create_studentid_entry = Entry(regframe,font=('poppins',15),bg='white',width=form_width)
create_studentid_entry.grid(row=6,column=0,columnspan=2,sticky=EW)

course_list = list(COURSE_FEES.keys())

create_course = Label(regframe, text='Course',font=('Poppins',15),bg='white')
create_course.grid(row=7,column=0,columnspan=2,sticky=W,pady=(10,0))
create_course_combo = Combobox(regframe,values=course_list,font=('poppins',15),width=form_width,state='readonly')
create_course_combo.grid(row=8,column=0,columnspan=2,sticky=EW)

style.map('TCombobox',
          fieldbackground=[('readonly','white')],
          selectbackground=[('readonly','white')],
          selectforeground=[('readonly','black')])

def back():
          regframe.grid_remove()
          staff_dashboard_frame.grid(sticky=NSEW)
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
          #if len(cf) < 7 or any(CHAR.isdigit() for CHAR in cf):
               messagebox.showerror("Error", "Please put a valid name!")
               return
          if not all(CHAR.isdigit() or CHAR == '-' for CHAR in cs):
               messagebox.showerror("Error", "Student ID must only contain numbers and dashes!")
               return
          if len(cs) != 17:
               messagebox.showerror("Error", "Student ID must be 17 characters!")
               return

          else:
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

               create_firstname_entry.delete(0,END)
               create_lastname_entry.delete(0,END)
               create_studentid_entry.delete(0,END)
               create_course_combo.set('')

               messagebox.showinfo("Success!", "Successfully created new account")
               back()


create_account = Button(regframe, text='Create account',font=('poppins',12),relief=SUNKEN,bd='2',bg='#203c3c',fg='white',command=createaccount)
create_account.grid(row=9,column=0,pady=(50,20),columnspan=2)
regback = Button(regframe, text='Back',font=('poppins',10,'underline'),bg='white',relief=SUNKEN,bd='2',command=back)
regback.grid(row=10,column=0,columnspan=2)







def remove_border():
     student_finder_frame.config(bd=0, relief=FLAT)
     payment_frame.config(bd=0, relief=FLAT)
remove_border()


window.mainloop()