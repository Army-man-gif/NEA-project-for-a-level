from constants import *
class Calendar_Display():
  def __init__(self,d):
    self.calendar  = None

    self.event_id = 0
    self.date = d

    self.l = tk.Label(tab_search("Calendar"),text = "Pick the exercise you want to view: 1 - 6: ")
    self.e = tk.Entry(tab_search("Calendar"))
    self.b = tk.Button(tab_search("Calendar"),text="Click to show")


    self.l2 = tk.Label(tab_search("Calendar"))
    self.e2 = tk.Entry(tab_search("Calendar"))
    self.b2 = tk.Button(tab_search("Calendar"),text="Click to decide")
    
    self.y  = 250
    self.x = 600
    ''' Different ways of formatting date'''
    # dd/mm/YY
    self.formatted2 = datetime.strptime(self.date.strftime("%m/%d/%y"), "%m/%d/%y").date()
    self.formatted = None
    self.day = self.date.strftime('%d')
    self.month = self.date.strftime('%m')
    self.year = self.date.strftime('%Y')
    self.display_Calendar_widget()
  def print(self):
    tk.Label(tab_search("Calendar"),text = f"Month abbreviation, day and year format = {self.d3}").pack(side="bottom")
    tk.Label(tab_search("Calendar"),text = f"dd/mm/YY format = {self.d1}").pack(side="bottom")
    tk.Label(tab_search("Calendar"),text = f"Textual month, day and year format = {self.d2}").pack(side="bottom")


  def display_Calendar_widget(self):
    self.calendar = Calendar(
      tab_search("Calendar"),
      selectmode="day",
      month=int(self.month),
      day=int(self.day),
      year=int(self.year),
      selectbackground = "red",
      selectforeground = "white"
      )
    self.calendar.place(x=0,y=0,width=W+300)
    self.revert()

    self.calendar.bind("<<CalendarSelected>>", self.handle_date_click)
    self.add_event()
  def delete_event(self):
    date = self.date
    if date is not None:
      events_on_date = self.calendar.calevent_get(date)
        
      for event in events_on_date:
        self.calendar.calevent_delete(event)


  def handle_date_click(self, event):

    reps = []
    rep_weights = []
    pr_weights = []
    
    for i in tab_search("Calendar").winfo_children():
      if i in (self.e,self.e2):
        i.delete(0, 'end')
      elif i == self.calendar:
        pass
      else:
        i.destroy()
    def summary_part1():
      val = int(self.e.get())-1
      specific_exercise_instance = Specific_exercise_class()
      try:
        specific_exercise_instance.show(self.exercises[val],"Calendar",None,200,self.x-600,400)
      
        self.display_Calendar_widget()
      except:
        messagebox.showwarning("Notification","Pick an exercise from 1-6")        
    def showing_on_calendar_tab():
      choice = int(self.e2.get())-1
      select = c.execute(f'''SELECT exercises FROM Summary WHERE date = '{self.formatted_date}' ''').fetchall()
      try:
        self.exercises = ast.literal_eval(select[choice][0])
        self.l = tk.Label(tab_search("Calendar"),text = "Pick the exercise you want to view: 1 - 6: ")

        self.e = tk.Entry(tab_search("Calendar"))
        self.b = tk.Button(tab_search("Calendar"),text="Click to show")
        self.l.place(x=self.x,y=self.y)
        self.e.place(x=self.x,y=self.y+50)
        self.b.config(command=summary_part1)
        self.b.place(x=self.x,y=self.y+100)
      except:
        messagebox.showwarning("Notification",f"Pick a workout from 1 - {number_of_entries_on_specific_date}")


    try:
      self.revert()
      self.exercises = ast.literal_eval(c.execute(f'''SELECT exercises FROM Summary WHERE date = '{self.date.strftime('%Y-%m-%d')}' ''').fetchall()[0][0])
      from Workout import Specific_exercise_class
      date_string = self.calendar.get_date()
      date_object = datetime.strptime(date_string, "%m/%d/%y").date()
      self.formatted_date = date_object.strftime('%Y-%m-%d')
      select = c.execute(f'''SELECT exercises FROM Summary WHERE date = '{self.formatted_date}' ''').fetchall()
      global number_of_entries_on_specific_date
      number_of_entries_on_specific_date = len(select)
      self.exercises = []
      for i in range(number_of_entries_on_specific_date):
        for j in ast.literal_eval(select[i][0]):
          self.exercises.append(j)
      for p in self.exercises:
        reps.append(c.execute(f'''SELECT reps FROM Exercise WHERE name = "{p}"''').fetchone()[0])
        pr_weights.append(c.execute(f'''SELECT PR_weight FROM Exercise WHERE name = "{p}"''').fetchone()[0])
        rep_weights.append(c.execute(f'''SELECT Rep_weight FROM Exercise WHERE name = "{p}"''').fetchone()[0])
      

      self.l2 = tk.Label(tab_search("Calendar"))
      self.e2 = tk.Entry(tab_search("Calendar"))
      self.b2 = tk.Button(tab_search("Calendar"),text="Click to decide")
          
      self.l2.config(text = f"Pick the workout you want to view: 1 - {number_of_entries_on_specific_date}: ")
      self.l2.place(x=self.x, y=self.y + 200)
      self.e2.place(x=self.x, y=self.y + 225)
      self.b2.config(command=showing_on_calendar_tab)
      self.b2.place(x=self.x, y=self.y + 250)
      date = date_object.strftime('%d-%m-%Y')
      tk.Label(tab_search("Calendar"),text=f'Your maximum reps in any exercise in your {number_of_entries_on_specific_date} workouts on the {date} was {max(reps)}',wraplength=200,background=colours[texts.index("Calendar")],foreground="white").place(x=self.x,y=self.y+300)
      tk.Label(tab_search("Calendar"),text=f'Your maximum rep weight in any exercise in your {number_of_entries_on_specific_date} workouts on the {date} was {max(rep_weights)} kg',wraplength=200,background=colours[texts.index("Calendar")],foreground="white").place(x=self.x,y=self.y+350)
      tk.Label(tab_search("Calendar"),text=f'Your maximum PR weight in any exercise in your {number_of_entries_on_specific_date} workouts on the {date} was {max(pr_weights)} kg',wraplength=200,background=colours[texts.index("Calendar")],foreground="white").place(x=self.x,y=self.y+400)
    except:
      messagebox.showwarning("Notification","You have no recorded workouts for this date")
      self.revert()


  def revert(self):
    def jump():
      self.display_Calendar_widget()
    tk.Button(tab_search("Calendar"),text="Click to go back to today",command=jump,background="black",foreground="yellow").place(x=225,y=300)
  def add_event(self):
      select = c.execute('''SELECT date from Summary''').fetchall()
      events = []
      for i in select:
        events.append(i[0])
      for i in events:
          if len(i) == 10:  # Check if the date string includes only the date part
            self.formatted2 = datetime.strptime(i, "%Y-%m-%d").date()
          else:
            self.formatted2 = datetime.strptime(i, "%Y-%m-%d %H:%M:%S").date()
            self.event_id = self.calendar.calevent_create(self.formatted2, "Red Dot", "dot")




