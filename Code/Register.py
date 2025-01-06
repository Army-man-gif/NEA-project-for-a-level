from constants import root,W,H
from PIL import Image,ImageTk, Image, ImageSequence
from basics import *
import tkinter as tk
root.withdraw()
login_window = tk.Toplevel(root)
login_window.geometry(f'{login_window.winfo_screenwidth()}x{login_window.winfo_screenheight()}')
experience_determination_window = tk.Toplevel(root)
experience_determination_window.withdraw()
experience_determination_window.geometry(f'{experience_determination_window.winfo_screenwidth()}x{experience_determination_window.winfo_screenheight()}')

experience_determination_window.title("Determining experience level")
login_window.geometry(f'{W}x{H}')
login_window.lift()

class GUI_login():
  def __init__(self,choice):
    self.choice = choice
    self.img = None
    self.img2 = None
    self.photo_for_login = None
    self.photo_for_registering = None
    self.image = None 
    self.image2 = None
    self.i = 1
    self.number = 0
    self.question_entry = None
    self.button = None
    if self.choice == 1:
      self.method1()
    elif self.choice == 2:
      self.method2()
    else:
      pass
  def record(self,event=None):
    try:
      self.number += int(self.question_entry.get())
    except ValueError:
        pass
    except:
        print(e)

  def run_both(self,event=None):
    self.record(event)
    self.move_on(event)
  def move_on(self,event=None):
      try:
        file = main(f"pic{self.i}.jpg")
        img = Image.open(file)
        img = img.resize((500,500))
        self.photo_for_login = ImageTk.PhotoImage(img)
        image = self.photo_for_login 
        pic = tk.Label(experience_determination_window, image=image) 
        pic.place(x=700,y=50)
        question_lbl = tk.Label(experience_determination_window, text="How many can you do?")
        question_lbl.place(x=50,y=50)
        self.question_entry = tk.Entry(experience_determination_window)
        self.question_entry.place(x=50,y=100)
        self.question_entry.focus_set()
        experience_determination_window.bind("<Return>",self.run_both)
  
        #question_ans_confirm = tk.Button(experience_determination_window,background="black",foreground="white", text = "Click to record your answer then press the foward button to go to the next question",command = self.record,wraplength=100)
        #question_ans_confirm.place(x=50,y=200)
        self.i += 1
      except Exception as e:
        experience_determination_window.bind("<Return>",self.run_it)

  def experience_determination(self):
    login_window.destroy()
    experience_determination_window.deiconify()
    self.move_on()
    #self.button = tk.Button(experience_determination_window,text="Forward",command=self.move_on)
    #self.button.place(x=400,y=0)

  def run_it(self,event=None):
    from start import start
    if  0 < self.number < 30:
      c.execute('''UPDATE Profile SET experience = ?''',("Beginner",))
    elif 30 < self.number <= 100:
      c.execute('''UPDATE Profile SET experience = ?''',("Intermediate",))
    elif self.number > 100:
      c.execute('''UPDATE Profile SET experience = ?''',("Advanced",))
    else:
      pass


    experience_determination_window.destroy()
    start()
  def method1(self):
    login_window.title("Sign up")
    def SignUp(event=None):
      name = name_entry_box.get()
      age = age_entry_box.get()
      gender = gender_entry_box.get()
      password = password_entry_box.get()
      try:
        name = str(name)
        gender = str(gender)
        password = str(password)
        c.execute(f'''
        INSERT INTO Profile (name,age,gender,split,password,PATH) VALUES ("{name}",{age},"{gender}","Five Day Split","{password}","{find_file("SignIn.jpg")}")
        ''')
        connection.commit()
        self.experience_determination()
        #self.run_it()
      except:
        name_entry_box.delete(0, "end")
        age_entry_box.delete(0, "end")
        gender_entry_box.delete(0, "end")
        password_entry_box.delete(0, "end")
        self.method1()





    
    self.img = Image.open(find_file("SignIn.jpg"))
    self.img = self.img.resize((700, 800))
    self.photo_for_login = ImageTk.PhotoImage(self.img)
    self.image = self.photo_for_login 
    lbl = tk.Label(login_window, image=self.image) 
    lbl.place(x=0,y=0)
    
    x = 500
    y = 50

    tk.Label(login_window,text="Sign up: ",font=("Helvetica",18,"bold")).place(x=x,y=y)

    name_lbl = tk.Label(login_window,text="Name: ",font=("Helvetica",18,"bold"),foreground="red")
    name_lbl.place(x=x - 150,y = y + 50)

    name_entry_box = tk.Entry(login_window,width=30)
    name_entry_box.place(x=x,y = y + 60)
    name_entry_box.focus_set()

    age_lbl = tk.Label(login_window,text="Age: ",font=("Helvetica",18,"bold"),foreground="red")
    age_lbl.place(x=x - 150,y = y + 100)

    age_entry_box = tk.Entry(login_window,width=30)
    age_entry_box.place(x=x,y = y + 110)


    gender_lbl = tk.Label(login_window,text="Gender: ",font=("Helvetica",18,"bold"),foreground="red")
    gender_lbl.place(x=x - 150,y = y + 150)

    gender_entry_box = tk.Entry(login_window,width=30)
    gender_entry_box.place(x=x,y = y + 160)


    password_lbl = tk.Label(login_window,text="Password: ",font=("Helvetica",18,"bold"),foreground="red")
    password_lbl.place(x=x - 150,y = y + 200)

    password_entry_box = tk.Entry(login_window,width=30)
    password_entry_box.place(x=x,y = y + 210)

    SignUp_Confirm_Button = tk.Button(login_window,text="Sign up",font=("Helvetica",15,"bold"),foreground="blue",command=SignUp)
    SignUp_Confirm_Button.place(x=x+5,y= y + 250)
    login_window.bind("<Return>",SignUp)

  def method2(self):
    login_window.title("Login")
    def LogIn(event=None):
      name = name_entry_box2.get()
      password = password_entry_box2.get()
      finding_from_profile = c.execute(f'''
      SELECT * FROM Profile WHERE name = ? AND password = ?
      ''',(name,password)).fetchall()
      if finding_from_profile:
        self.run_it()
      else:
        name_entry_box2.delete(0, "end")
        password_entry_box2.delete(0, "end")
        self.method2()

    
    self.img2 = Image.open(find_file("Image.jpg"))
    self.img2 = self.img2.resize((700, 800))
    self.photo_for_registering = ImageTk.PhotoImage(self.img2)
    self.image2 = self.photo_for_registering
    lbl2 = tk.Label(login_window, image=self.image2) 
    lbl2.place(x=0,y=0)
    
    x2 = 500
    y2 = 50

    tk.Label(login_window,text="Login: ",font=("Helvetica",18,"bold")).place(x=x2,y=y2)

    name_lbl2 = tk.Label(login_window,text="Name: ",font=("Helvetica",18,"bold"),foreground="red")
    name_lbl2.place(x=x2 - 100,y = y2 + 50)

    name_entry_box2 = tk.Entry(login_window,width=30)
    name_entry_box2.place(x=x2,y = y2 + 60)
    name_entry_box2.focus_set()


    password_lbl2 = tk.Label(login_window,text="Password: ",font=("Helvetica",18,"bold"),foreground="red")
    password_lbl2.place(x=x2 - 150,y = y2 + 100)

    password_entry_box2 = tk.Entry(login_window,width=30,show="*")
    password_entry_box2.place(x=x2,y = y2 + 110)

    Login_Confirm_Button2 = tk.Button(login_window,text="Login",font=("Helvetica",15,"bold"),foreground="blue",command=LogIn)
    Login_Confirm_Button2.place(x=x2+5,y= y2 + 250)
    login_window.bind("<Return>", LogIn)

