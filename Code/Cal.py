from constants import *
class Caloric():
  def __init__(self,sex):
    self.E = None
    self.Text = None
    self.Button = None
    self.sex = sex
    self.general = None
    self.keys = []
    self.array = []
    self.array2 = []
    self.vals = []
    self.E = None
    self.lbl = tk.Label(tab_search("Caloric stuff"))
    self.Base()
    #self.convert()
  def delete(self):
    c.execute('''DELETE FROM Nutrition''')
  def print(self):
    print(c.execute('''SELECT * FROM Nutrition''').fetchall())
  
  def convert(self):
    pounds = int(input("Enter pounds to be converted to kg"))
    kg = 0.454 * pounds
    tk.Label(tab_search("Caloric stuff"),text=round(kg,3)).pack(side="right")
  def Calorie_split(self):
    messagebox.showwarning("Notification","Internet connection is required now")
    self.vals = []
    self.keys = []
    for i in tab_search("Caloric stuff").winfo_children():
      if i not in (self.Text, self.E, self.Button,self.lbl,self.general):
            i.destroy()
    split = self.E.get()
    api_url = 'https://api.api-ninjas.com/v1/nutrition?query={}'.format(split)
    response = requests.get(api_url, headers={'X-Api-Key': 'EYubhelGF0jRmCC4ZtZKZg==pWcZsqUXcpnwlFW7'})
    request = response.json()
    y  = 0
    for a_set in request:
      for key,value in a_set.items():
        self.keys.append(key)
        self.vals.append(value)
        tk.Label(tab_search("Caloric stuff"),text=f'{key.capitalize()} : {value}',background="black",foreground="white").place(x=800,y=y)
        y += 20
  def insert(self):
    search = self.E.get()
    check = '''
      SELECT * FROM Nutrition
      WHERE Name = ? 
            '''
    c.execute(check, (search,))
    exist = c.fetchone()
    if exist:
      names = c.execute("PRAGMA table_info(Nutrition)").fetchall()
      column_names = [column[1] for column in names]
      existing_record = exist[1:len(names)]
      column_names = column_names[1:len(names)]
      self.vals = existing_record
      self.keys = column_names
      y = 0
      for index,value in enumerate(existing_record):
        tk.Label(tab_search("Caloric stuff"),text=f'{column_names[index]} : {value}',background="black",foreground="white").place(x=800,y=y)
        y += 20
    else:
      self.Calorie_split()
      insert_sql = '''
      INSERT INTO Nutrition (Name, Calories, Serving_Size, Total_fat, Saturated_fat, Protein, Sodium, Potassium, Cholesterol, Carbohydrate_TOTAL, Fiber, Sugar)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
      '''
      c.execute(insert_sql, self.vals)
      connection.commit()

  def Recipe(self):
    query  = self.E.get()
    query = query.split()
    for ind,val in enumerate(query):
      try:
        for char in val:
          if char.isdigit():
            query.remove(val)

      except ValueError:
        continue

    query = ' '.join(query)
    api_url = 'https://api.api-ninjas.com/v1/recipe?query={}'.format(query)
    response = requests.get(api_url, headers={'X-Api-Key': 'EYubhelGF0jRmCC4ZtZKZg==pWcZsqUXcpnwlFW7'})
    if response.status_code == requests.codes.ok:
      text = response.json()
      try:
        if len(text) != 0:
          for i in text[0]:
            cur = text[0][i]
            cur = cur.split('.,')
            for j in cur:
              self.lbl.config(text=j,wraplength=350,foreground = "red")
              self.lbl.place(x = 700,y=300)
      except Exception as e:
            self.lbl.config(text="Recipe not avaiable",wraplength=350,foreground = "red")
            self.lbl.place(x = 700,y=300)
            print(e)
    self.E.delete(0,'end')
  def Chart(self):
    k = self.keys
    v = self.vals
    self.values = []
    self.labels = []
    canvas_width =  500
    canvas_height = 500
    # Calculate the center of the canvas
    center_x = canvas_width / 2
    center_y = canvas_height / 2

    tk.Label(tab_search("Caloric stuff"), text="Split").place(x=center_x, y=center_y-200)

    canvas = tk.Canvas(tab_search("Caloric stuff"), width=canvas_width, height=canvas_height)
    canvas.place(x=center_x - 100, y=center_y-100)

    colours = ['red', 'green', 'orange', 'blue', 'yellow', 'white', 'purple', 'pink', 'gold', 'turquoise', 'violet',
               'indigo']
    start = 0
    colour_index = 0
    for index, value in enumerate(v):
        if k[index] != "calories" and k[index] != "serving_size_g":
          if type(value) == float or type(value) == int:
              self.values.append(value)
              self.labels.append(k[index])
    total = 0
    for i in self.array:
      total = total + int(i)
    y = np.array(self.values)
    mylabels = self.labels
    fig, ax = plt.subplots(figsize=(30,30))
    x = ax.pie(y, labels=mylabels,autopct='%1.1f%%')
    # Embed the Matplotlib figure in the Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=tab_search("Caloric stuff"))
    canvas.draw()
    canvas.get_tk_widget().place(x=center_x - 100, y=center_y-100, width=canvas_width, height=canvas_height)
    
  def Caloric_general(self):
    if self.sex == "Male":
      maintain = 2500
      cut = 1900
      bulk = maintain + 2000
      self.general = tk.Label(tab_search("Caloric stuff"),text=f'To maintain: {maintain} \n To cut: {cut} \n To bulk: {bulk}')
      self.general.place(x=800,y=500)
    else:
      maintain = 2000
      cut = 1400
      bulk = maintain + 1600
      self.general = tk.Label(tab_search("Caloric stuff"),text=f' To maintain: {maintain} \n To cut: {cut} \n To bulk: {bulk}')
      self.general.place(x=800,y=600)
  def combined(self):
    self.Caloric_general()
    #self.delete()
    self.insert()
    #self.Recipe()
    self.Chart()
  def Base(self):
    self.Text = tk.Label(tab_search("Caloric stuff"),text="Enter to get calories of a meal : ")
    self.Text.place(x=0,y=0)
    self.E = tk.Entry(tab_search("Caloric stuff"))
    self.E.place(x=200,y=0)
    self.Button = tk.Button(tab_search("Caloric stuff"),text="Click",command=self.combined)
    self.Button.place(x=0,y=60)
