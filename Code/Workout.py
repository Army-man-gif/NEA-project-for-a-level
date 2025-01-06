from constants import *
from Calendar import Calendar_Display
from Search_for_Images import *

class Workout_display_class():
  def __init__(self):
    self.images = {}
    self.H = 600
    self.W = 600

    self.inside2 = tk.Frame(tab_search("Workouts display"),height=self.H,width=self.W)
    self.canvas2 = tk.Canvas(self.inside2)

    self.change = tk.StringVar()
    self.var = tk.StringVar()

    self.inside = tk.Frame(tab_search("Workouts display"),height=self.H,width=self.W)
    self.inside.place(x=0,y=0)


    # Add canvas
    self.canvas = tk.Canvas(self.inside)
    self.canvas.pack(side = "left")
    self.canvas.config(width=2/5*self.W, height=self.H,background="yellow")
    # Add scrollbar
    self.scrollbar = tk.Scrollbar(self.inside,orient="vertical",command = self.canvas.yview,highlightthickness=border,highlightbackground="black")
    self.scrollbar.pack(side = "left", fill = "y")
    # Confugure canvas
    self.canvas.config(yscrollcommand = self.scrollbar.set)
    self.canvas.bind('<Configure>',lambda e: self.canvas.configure(scrollregion = self.canvas.bbox("all")))
    # Create another frame inside the canvas
    self.Sub_frame = tk.Frame(self.canvas)
    # Add this new frame to a window in the canvas
    self.canvas.create_window((100,250), window = self.Sub_frame, anchor = "nw")
    self.var = tk.StringVar()

    self.load()
    self.other_class = Specific_exercise_class()

    self.var.trace('w', self.on_radio_button_change)
  def load(self):
    self.Sub_frame.pack()
    a = c.execute("SELECT * From Program_Routine")
    all_workouts = a.fetchall()
    for line in all_workouts:
        try:
          img = Image.open(main(line[1]+' Day'+file_extension))
          img = img.resize((100, 100))
          self.images[line[1]] = ImageTk.PhotoImage(img)
          self.l = tk.Radiobutton(self.Sub_frame, text=line[1]+' Day',image=self.images[line[1]],compound=tk.TOP,command=lambda value2=line[1]:
          self.on_radio_button_change(value2), variable=self.var, value=line[1])
          self.l.pack()
        except:
          self.l = tk.Radiobutton(self.Sub_frame, text=line[1]+' Day',command=lambda value2=line[1]: self.on_radio_button_change(value2),
          variable=self.var, value=line[1])
          self.l.pack()
  def on_radio_button_change(self,*args):
    selected_value = self.var.get()
    self.other_class.select(selected_value)
    self.other_class.Specific_workout(selected_value)


from Treeview import display_in_treeview
def x():
  Database = display_in_treeview()
Button = tk.Button(tab_search("Display database in treeview"),text="Click to view all exercises",command=x)
Button.pack()



class Specific_exercise_class(display_in_treeview):
  def __init__(self,**kwargs):
    super().__init__(**kwargs)
    self.H = 600
    self.W = 600
    self.HeadingVar = tk.IntVar()
    self.clicked = tk.StringVar()
    self.indexes = []
    self.inside = tk.Frame(tab_search("Workouts display"),height=self.H,width=self.W)
    self.inside2 = tk.Frame(tab_search("Workouts display"),height=self.H,width=self.W)
    self.canvas2 = tk.Canvas(self.inside2)
    self.change = tk.StringVar()
    self.var = tk.StringVar()



    self.inside3 = tk.Frame(tab_search("Workouts display"),height=self.H,width=self.W)
    self.canvas3 = tk.Canvas(self.inside3)
    self.Sub_frame3 = tk.Frame(self.canvas3)

    self.num = 0
    self.l = tk.Label()
    self.random_numbers = []
  def select(self,SELECT): 
    for widget in self.canvas2.winfo_children():
      widget.destroy()
    self.inside2.place(x=self.W-450,y=0)

    highest = c.execute('''
    SELECT ID FROM Program_Routine
    WHERE name = ?
    ''',(SELECT,))
    Program_ID = highest.fetchall()[0][0]
    mid_level = c.execute('''
    SELECT ID,name FROM Workout
    WHERE Program_Routine_ID = ?
    ''',(Program_ID,))
    Muscles = mid_level.fetchall()
    self.y = []
    for i in range(len(Muscles)):
      muscle_name = Muscles[i][1]
      # Create the SQL query with a placeholder
      sql_query = "SELECT name FROM Exercise WHERE muscle = ?"
      # Execute the query with the parameter
      x = c.execute(sql_query, (muscle_name,))
      order = []
      p = x.fetchall()
      for j in p:
        self.y.append(j[0])
    if list(set(self.y)) != self.y:
      self.y = list(set(self.y))
  def add(self):
      current = []
      for i in self.indexes:
        current.append(self.y[i])
      #print(current)
      now = datetime.now()
      #now = now + timedelta(days=6)
      current = json.dumps(current)
      if self.HeadingVar.get() == 1:
        from History import History
        find = c.execute(" SELECT exercises FROM Summary WHERE date = ? ",(now.strftime('%Y-%m-%d'),)).fetchall()
        changed = ast.literal_eval(current)
        for i in changed:
          temporary = c.execute('''SELECT reps,sets,PR_weight,Rep_weight,Enjoyable,How_difficult_it_felt,
          equipment,difficulty,muscle FROM Exercise WHERE name = ?''',(i,)).fetchall()
          temporary = list(temporary[0])
          temporary.insert(0,i)
          temporary.insert(1,now.strftime('%Y-%m-%d'))
          temporary = tuple(temporary)
          c.execute('''INSERT INTO History (exercise,date,reps,sets,PR_weight,Rep_weight,Enjoyable,
          How_difficult_it_felt,equipment,difficulty,muscle) VALUES (?,?,?,?,?,?,?,?,?,?,?)''',temporary)
          connection.commit()
          
            
        if current != find:
          query = '''
          INSERT INTO Summary (exercises, date) VALUES (?, ?)
          '''
          values = (current, now.strftime('%Y-%m-%d'))
          c.execute(query, values)
          connection.commit()
        C = Calendar_Display(now)
      else:
        c.execute(f'''
        DELETE FROM Summary
        WHERE date = ?
        ''',(now.strftime('%Y-%m-%d'),))
        c.execute('''DELETE FROM History WHERE date = ?''',(now.strftime('%Y-%m-%d'),))
        C = Calendar_Display(now)
        C.delete_event()
  def display_dropdown(self,value):
    def display():
      for widget in self.Sub_frame2.winfo_children():
        widget.destroy()

      self.Heading = tk.Checkbutton(self.Sub_frame2, text="Your workout:",variable=self.HeadingVar, onvalue=1, offvalue=0,command = self.add)
      self.HeadingVar.set(0)
      self.Heading.pack()
      for i in range(6):
        if i == value[1]:
          self.change.set(self.clicked.get())  # Set the value for the changed exercise

          p = tk.Radiobutton(self.Sub_frame2, text=f'Exercise {i + 1}: {self.change.get()}', variable=self.change,
          value=self.change.get(),command=lambda value=self.change.get(): self.show(value,"Workouts display","active",300,600,100), wraplength=200)
          p.pack()
          self.m = tk.Button(self.Sub_frame2, text="Change", background="red", command=lambda value=[self.y[self.num],i]: self.display_dropdown(value))
          self.m.pack()
          new_index = self.y.index(self.change.get())
          self.indexes[value[1]] = new_index
        else:
          #print(self.change.get(),", index: ",self.y.index(self.change.get()))
          p = tk.Radiobutton(self.Sub_frame2, text=f'Exercise {i + 1}: {self.y[self.indexes[i]]}', variable=self.change,
          value=self.y[self.indexes[i]],command=lambda value=self.y[self.indexes[i]]: self.show(value,"Workouts display","active",300,600,100),
          wraplength=200)
          p.pack()
          self.m = tk.Button(self.Sub_frame2, text="Change", background="red", command=lambda value=[self.y[self.num],i]: self.display_dropdown(value))
          self.m.pack()
    self.clicked.set(value[0])
    drop = tk.OptionMenu(self.Sub_frame2, self.clicked, *self.y)
    drop.pack()
    tk.Button(self.Sub_frame2,text="Confirm",command=display).pack()
    l = tk.Label(self.Sub_frame2)
  def same(self,arr):
    value = arr[0]
    identical = False
    for i in arr:
      if i == value:
        identical = True
      else:
        identical = False
    return identical
  def Specific_workout(self,value):
    self.canvas2.pack()
    self.canvas2.config(width=3/5*self.W, height=self.H,background="red")
    # Create another frame inside the canvas
    self.Sub_frame2 = tk.Frame(self.canvas2)
    # Add this new frame to a window in the canvas
    self.canvas2.create_window((250,100), window = self.Sub_frame2, anchor = "ne")


    self.Heading = tk.Checkbutton(self.Sub_frame2, text="Your workout:",variable=self.HeadingVar, onvalue=1, offvalue=0,command=self.add)
    self.HeadingVar.set(0)
    self.Heading.pack()
    self.indexes = []
    new = []
    probability = c.execute('''SELECT Enjoyable FROM Exercise''').fetchall()
    for i in probability:
      new.append(i[0])

    
 
    if self.same(new):
      random_numbers = random.sample(range(0, len(self.y)), 6)
      for i in range(6):
          self.num  = random_numbers[i]
          key = self.y[self.num]
          self.indexes.append(self.num)
          self.change.set(key)  # Set the initial value for the radio button
          p = tk.Radiobutton(self.Sub_frame2, text=f'Exercise {i + 1}: {self.change.get()}', variable=self.change,
          value=key, command=lambda value=key: self.show(value,"Workouts display","active",300,600,100), wraplength=200)
          p.pack()

          self.m = tk.Button(self.Sub_frame2, text="Change", background="red", command=lambda value=[key,i]: self.display_dropdown(value))
          self.m.pack()
    else:
      random_numbers = []
      for i in range(new):
        random_numbers.append(max(new))
        new.remove(max(new))
      print("not the same so random indexes generated from max of new",random_numbers)
      for i in range(6):
        self.num  = random_numbers[i]
        key = self.y[self.num]
        self.indexes.append(self.num)
        self.change.set(key)  # Set the initial value for the radio button
        p = tk.Radiobutton(self.Sub_frame2, text=f'Exercise {i + 1}: {self.change.get()}', variable=self.change,
        value=key, command=lambda value=key: self.show(value,"Workouts display","active",300,600,100), wraplength=200)
        p.pack()

        self.m = tk.Button(self.Sub_frame2, text="Change", background="red", command=lambda value=[key,i]: self.display_dropdown(value))
        self.m.pack()
        
        
  def show(self,selection,tab,state,size,x,y):
    tab = tab_search(tab)
    s = tk.Label(tab,wraplength=500)
    for widget in self.Sub_frame3.winfo_children():
      widget.destroy()

    self.Sub_frame3 = tk.Frame(self.canvas3)
    self.inside3.place(x=self.W-150,y=0)
    self.canvas3.pack(side = "left")
    self.canvas3.config(width=self.W, height=self.H,background="green")
    self.canvas3.create_window((250,100), window = self.Sub_frame3, anchor = "ne")

    img_path = main(selection+'.jpg')
    path = r"C:\Users\khait\OneDrive\Desktop\Project pictures\GIFs"+selection+'.gif'
    def show_it():
        SQL_command = c.execute(f'''SELECT * FROM Exercise 
        WHERE name = ?
          ''',(selection,))
        info = SQL_command.fetchone()
        info = list(info)
        info.pop(0)
        info.pop(len(info)-1)
        print(info)
        if state == "active": 
          self.l = tk.Label(tab,text=f'''This exercise: \n Name: {info[0]} \n Works the: {info[9].capitalize()} \n Reps: {info[1]} \n Sets: {info[2]} \n
          Equipment needed: {info[7].capitalize()} \n Difficulty level: {info[8].capitalize()} \n Current Pr Weight: {info[3]} \n Current Rep Weight:
          {info[4]} \n How much you liked the exercise: {info[5]}, \n How difficult you found it: {info[6]}
          ''',wraplength=600,height=15,width=85,background="green",foreground="white")
          self.l.place(x=x-150,y=y+275)  
        else:
          s.config(text=f'''Summary: \n Name: {info[0]} \n Works the: {info[9].capitalize()} \n Reps: {info[1]} \n Sets: {info[2]} \n
          Equipment needed: {info[7].capitalize()} \n Difficulty level: {info[8].capitalize()} \n Current Pr Weight: {info[3]} \n Current Rep Weight:
          {info[4]} \n How much you liked the exercise: {info[5]}, \n How difficult you found it: {info[6]}''',wraplength=550,background=colours[texts.index("Calendar")],foreground="white")
          s.place(x=x+300,y=y-80)  

    if state  == "active":
      def To_Treeview():
        from GUI_basics import Frame
        tab_search("Display database in treeview").tkraise()

        inst = super(Specific_exercise_class, self)
        inst.Search(selection)

      def replace(text):
        messagebox.showinfo("Notification",text)
        FILETYPES = [("All files", "*.*")]
        filename = filedialog.askopenfilename(initialdir = os.path.expanduser("~"),title="Select a file",filetypes=FILETYPES)
        if not filename:
          return 
        else:
          filename_changed  = selection + ".jpg"
          shutil.move(filename, os.path.join(base_path, filename_changed))
          img_path = main(selection+'.jpg')   
          img = Image.open(img_path)
          img = img.resize((size, size))
          self.photo = ImageTk.PhotoImage(img)
          if state=="active":
            tk.Label(tab,image=self.photo,background=colours[texts.index("Workouts display")]).place(x=x,y=y-75)
          else:
            tk.Label(tab,image=self.photo).place(x=x,y=y+100)

      Button = tk.Button(tab,text="Done",command=To_Treeview)
      Button.place(x=x+300,y=y-100)
      Button2 = tk.Button(tab, text="Change picture for exercise", command=lambda: replace("Select picture which you want to replace the current picture with"))
      Button2.place(x=x-100,y=y-100)
      
    try:
      img = Image.open(img_path)
      img = img.resize((size, size))
      self.photo = ImageTk.PhotoImage(img)
      if state=="active":
        tk.Label(tab,image=self.photo,background=colours[texts.index("Workouts display")]).place(x=x,y=y-75)
      else:
        tk.Label(tab,image=self.photo).place(x=x,y=y+100)
      show_it()
    except Exception as e:
      try:
        messagebox.showinfo("Warning!","There isn't a picture for this exercise so please search for, download and then select the location of a new picture of your choice")
        Button2 = tk.Button(tab, text="Change", command=lambda: replace("Select the picture you downloaded"))
        Button2.place(x=x-100,y=y-100)
        show_it()
      except Exception as e:
        print('Exception:',e)
        if state=="active":
          tk.Label(tab,text='Image current unavailable.....',background=colours[texts.index("Workouts display")]).place(x=x,y=y-75)
        else:
          tk.Label(tab,text='Image current unavailable.....').place(x=x,y=y+100)
        show_it()

