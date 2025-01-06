from constants import *
class Graphing():
  def __init__(self):
    self.start = 0
    self.reps_list = []
    self.pr_weights_list = []
    self.rep_weights_list = []
    self.sets_list = []
    self.exercises = []
    self.options = ["Reps against exercises","Reps against rep weight", "Reps against PR weight","Rep weight against exercises","PR weight against exercises","Sets against PR weight","Sets against rep weight","Sets against reps","Sets against exercises"]
    self.var = tk.StringVar(tab_search("Workout graph summaries"))
    self.shown = tk.Button(tab_search("Workout graph summaries"), text="Click to show graph", command=lambda: self.choice(1))
    self.shown.place(x=0,y=0)
    self.down = tk.Button(tab_search("Workout graph summaries"),text="           Down                  ")
    self.down.config(command=lambda: self.choice(2))
    self.res = tk.Button(tab_search("Workout graph summaries"),text="reset",command=self.go_back)
    self.res.place(x=0,y=400)
  def draw(self,values,labels,x_axis,y_axis):
    plt.close('all')
    fig, ax = plt.subplots(figsize=(5, 5))
    bars = ax.barh(labels, values, color='skyblue')
    
    # Add labels and values to the bars
    for bar in bars:
      yval = bar.get_width()
      plt.text(yval, bar.get_y() + bar.get_height()/2, round(yval, 2), va='center')

    ax.set_xlabel(x_axis)
    ax.set_ylabel(y_axis)

    plt.yticks(rotation=45, ha='right',fontsize=8)

    # Embed the Matplotlib figure in the Tkinter window
    canvas_width =  800
    canvas_height = 500

    # Calculate the center of the canvas
    center_x = canvas_width / 2
    center_y = canvas_height / 2
    canvas = FigureCanvasTkAgg(fig, master=tab_search("Workout graph summaries"))
    canvas.draw()
    canvas.get_tk_widget().place(x=center_x-300, y=center_y - 100, width=canvas_width, height=canvas_height)
  def search(self):
    self.reps_list = []
    self.pr_weights_list = []
    self.rep_weights_list = []
    self.sets_list = []

    select = c.execute(f'''SELECT name FROM Exercise ''').fetchall()
    number_of_entries_on_specific_date = len(select)
    self.exercises = []
    for i in range(number_of_entries_on_specific_date):
      self.exercises.append(select[i][0])
    for p in self.exercises:
      self.reps_list.append(c.execute(f'''SELECT reps FROM Exercise WHERE name = "{p}"''').fetchone()[0])
      self.pr_weights_list.append(c.execute(f'''SELECT PR_weight FROM Exercise WHERE name = "{p}"''').fetchone()[0])
      self.rep_weights_list.append(c.execute(f'''SELECT Rep_weight FROM Exercise WHERE name = "{p}"''').fetchone()[0])
      self.sets_list.append(c.execute(f'''SELECT sets FROM Exercise WHERE name = "{p}"''').fetchone()[0])


  def move(self,number):
    if number == 1:
      if self.start == 0:
        def run():
          self.draw(self.reps_list[0:15],self.exercises[0:15],"Reps","Exercises")
        self.start = self.start +15
        run()
        self.down.place(x=0,y=0)
      else:
        def run():
          self.draw(self.reps_list[self.start:self.start+15],self.exercises[self.start:self.start+15],"Reps","Exercises")
        self.start = self.start +15
        run()
    elif number == 2:
      if self.start == 0:
        def run():
          self.draw(self.reps_list[0:15],self.rep_weights_list[0:15],"Reps","Rep weights")
        self.start = self.start +15
        run()
        self.down.place(x=0,y=0)
      else:
        def run():
          self.draw(self.reps_list[self.start:self.start+15],self.rep_weights_list[self.start:self.start+15],"Reps","Rep weights")
        self.start = self.start +15
        run()
    elif number == 3:
      if self.start == 0:
        def run():
          self.draw(self.reps_list[0:15],self.pr_weights_list[0:15],"Reps","PR weights")
        self.start = self.start +15
        run()
        self.down.place(x=0,y=0)
      else:
        def run():
          self.draw(self.reps_list[self.start:self.start+15],self.pr_weights_list[self.start:self.start+15],"Reps","PR weights")
        self.start = self.start +15
        run()
    elif number == 4:
      if self.start == 0:
        def run():
          self.draw(self.rep_weights_list[0:15],self.exercises[0:15],"Rep weight","Exercises")
        self.start = self.start +15
        run()
        self.down.place(x=0,y=0)
      else:
        def run():
          self.draw(self.rep_weights_list[self.start:self.start+15],self.exercises[self.start:self.start+15],"Rep weight","Exercises")
        self.start = self.start +15
        run()
    elif number== 5:
      if self.start == 0:
        def run():
          self.draw(self.pr_weights_list[0:15],self.exercises[0:15],"PR weight","Exercises")
        self.start = self.start +15
        run()
        self.down.place(x=0,y=0)
      else:
        def run():
          self.draw(self.pr_weights_list[self.start:self.start+15],self.exercises[self.start:self.start+15],"PR weight","Exercises")
        self.start = self.start +15
        run()
    elif number== 6:
      if self.start == 0:
        def run():
          self.draw(self.sets_list[0:15],self.pr_weights_list[0:15],"Sets","PR weights")
        self.start = self.start +15
        run()
        self.down.place(x=0,y=0)
      else:
        def run():
          self.draw(self.sets_list[self.start:self.start+15],self.pr_weights_list[self.start:self.start+15],"Sets","PR weights")
        self.start = self.start +15
        run()
    elif number== 7:
      if self.start == 0:
        def run():
          self.draw(self.sets_list[0:15],self.rep_weights_list[0:15],"Sets","Rep weights")
        self.start = self.start +15
        run()
        self.down.place(x=0,y=0)
      else:
        def run():
          self.draw(self.sets_list[self.start:self.start+15],self.rep_weights_list[self.start:self.start+15],"Sets","Rep weights")
        self.start = self.start +15
        run()
    elif number== 8:
      if self.start == 0:
        def run():
          self.draw(self.sets_list[0:15],self.reps_list[0:15],"Sets","Reps")
        self.start = self.start +15
        run()
        self.down.place(x=0,y=0)
      else:
        def run():
          self.draw(self.sets_list[self.start:self.start+15],self.reps_list[self.start:self.start+15],"Sets","Reps")
        self.start = self.start +15
        run()
    elif number== 9:
      if self.start == 0:
        def run():
          self.draw(self.sets_list[0:15],self.exercises[0:15],"Sets","Exercises")
        self.start = self.start +15
        run()
        self.down.place(x=0,y=0)
      else:
        def run():
          self.draw(self.sets_list[self.start:self.start+15],self.exercises[self.start:self.start+15],"Sets","Exercises")
        self.start = self.start +15
        run()
    else:
      pass

  def go_back(self):
    self.search()
    self.start = 0
    self.move(self.options.index(self.var.get())+1)
  def select(self,variable):
    self.go_back()
  def choice(self,loop):
    if loop == 1:
      self.var.set("Make a choice")
      dropdown_menu = tk.OptionMenu(tab_search("Workout graph summaries"), self.var, *self.options,command=self.select)
      dropdown_menu.place(x=700,y=50)
    else:
      self.move(self.options.index(self.var.get())+1)
