from constants import *
from Calendar import Calendar_Display
from Graphing import Graphing
class display_in_treeview():
  def __init__(self):
    self.entries = []
    self.search_entry = None
    table_name = "Exercise"
    c.execute(f"PRAGMA table_info({table_name})")
    table_info = c.fetchall()
    self.column_names = [info[1] for info in table_info]
    self.column_names = self.column_names[:-1]
    self.horizontal = 75
    self.vertical = 280
    self.labels = {}
    self.entries = {}
    self.call()
    self.view()
    self.define()
    #self.Record()
  def Update_ID(self):
    visible_items = self.my_tree.get_children("")
    i = 1
    for item in visible_items:
        self.my_tree.set(item, column="ID", value=i)
        i += 1
  def call(self):
    SQL = c.execute('''
SELECT name From Program_Routine
''')
    Program_Headers = SQL.fetchall()
    columns = ", ".join(self.column_names)
    params = ", ".join(["?" for _ in self.column_names])
    SQL2 = c.execute(f'''
SELECT {columns} from Exercise
''')

    self.Exercise_Headers = SQL2.fetchall()
  def view(self):    
    style = ttk.Style()
    # Pick a theme
    style.theme_use("default")
    # Configure our Treeview colours
    style.configure("Treeview",
                    background = "beige",
                    foreground = "black",
                    rowheight = 25,
                    fieldbackground = "silver")
    style.map('Treeview', background = [('selected','steel blue')])
    TreeViewFrame = tk.Frame(tab_search("Display database in treeview"),height=400,width=200,background="indigo")
    TreeViewFrame.place(x=0,y=25)
    self.my_tree = ttk.Treeview(TreeViewFrame)  
    # Define out columns
    self.my_tree['columns'] = self.column_names
    # Format our columns
    self.my_tree.column('#0',width=0, minwidth=0)
    column_name_to_index = {name: i for i, name in enumerate(self.column_names)}
    width = (1000-75-250)//len(self.column_names) 
    for name in self.column_names:
      if name == "ID":
        column_index = column_name_to_index[name]
        self.my_tree.column(column_index, anchor="center", width=75)
      elif name == "name":
        column_index = column_name_to_index[name]
        self.my_tree.column(column_index, anchor="center", width=250)
      else:
        column_index = column_name_to_index[name]
        self.my_tree.column(column_index, anchor="center", width=width)        

    # Create Headings
    self.my_tree.heading("#0", text=" ")
    for index, heading in enumerate(self.column_names):
      self.my_tree.heading(index, text=heading)

    # Create striped row tags
    self.my_tree.tag_configure('odd_row',background="light green")
    self.my_tree.tag_configure('even_row',background="gold")

    count = 0
    for i in self.Exercise_Headers:
        v = ()
        for j in range(len(self.column_names)):
            if type(i[j]) == str:
              v += (i[j].capitalize(),)
            else:
              v += (i[j],)
        if count % 2 == 0:
            self.my_tree.insert(parent = '', index='end',iid=count, text=" ",values=v,tags=('even_row',))
            self.my_tree.pack()
        else:
            self.my_tree.insert(parent = '', index='end',iid=count, text=" ",values=v,tags=('odd_row',))
            self.my_tree.pack()
        count += 1
    #my_tree.insert(parent = '1', index='end',iid=151,text="Parent",values=("hamstrings","horizontal leg press",151,55,20,"Giant 8000kg barbell","God tier difficulty- [but my warmup]"))
    self.Update_ID()

  def Update_row_colors(self):
    row_index = 0
    for iid in self.my_tree.get_children(""):
      # Alternate the row colors based on the row_index
      tag = "even_row" if row_index % 2 == 0 else "odd_row"

      # Set the tag of the Treeview item to the appropriate tag
      self.my_tree.item(iid, tags=(tag,))

      # Increment the row index for the next iteration
      row_index += 1
  def Search(self,auto):
    
    if auto == None:
      query = self.search_entry.get()
      self.my_tree.focus()  
      self.my_tree.selection_remove(self.my_tree.selection())

      # Search and highlight matching items
      for item in self.my_tree.get_children():
          values = self.my_tree.item(item, "values")
          if query.lower() in " ".join(map(str, values)).lower():
              self.my_tree.selection_add(item)
              self.my_tree.see(item)
              self.my_tree.focus(item) 
    else:
      query = auto  
      self.my_tree.focus()
      self.my_tree.selection_remove(self.my_tree.selection())
      # Search and highlight matching items
      for item in self.my_tree.get_children():
          values = self.my_tree.item(item, "values")
          if query.lower() in " ".join(map(str, values)).lower():
              self.my_tree.selection_add(item)
              self.my_tree.focus(item) 
              self.my_tree.see(item)
  
  def Up(self):
    rows = self.my_tree.selection()
    for row in rows:
      self.my_tree.move(row,self.my_tree.parent(row),self.my_tree.index(row)-1)
    self.Update_ID()
    self.Update_row_colors()
  def Down(self):
    rows = self.my_tree.selection()
    for row in reversed(rows):
      self.my_tree.move(row,self.my_tree.parent(row),self.my_tree.index(row)+1)
    self.Update_ID()
    self.Update_row_colors()
  def Clear(self):
    for key,value in self.entries.items():
      getattr(value,'delete')(0,'end')

  def Delete(self):
    select = self.my_tree.selection()
    previously_selected = select[-1]
    self.my_tree.delete(*select)
    values = self.my_tree.item("values")
    c.execute("DELETE FROM Exercise WHERE ID = ?", (values[0],))
    connection.commit()
    self.Update_row_colors()  
    self.Update_ID()
    self.my_tree.focus(previously_selected)
  def Update(self):
    selected = self.my_tree.focus()
    new_attributes = ()
    existing_attributes = self.my_tree.item(selected, "values")
    for i in self.entries.items():
      x = getattr(i[1],'get')()
      if x != "":
        new_attributes+= (x,)
      else:
        new_attributes += (existing_attributes[len(new_attributes)],)
    selected_item = self.my_tree.selection()
    self.my_tree.item(selected,text="",values=new_attributes)

    formatted = []
    table_name = "Exercise"
    c.execute(f"PRAGMA table_info({table_name})")
    table_info = c.fetchall()
    for index,column_name in enumerate(self.column_names):
      data_type = table_info[index][2]
      if data_type == "INTEGER" or data_type == "FLOAT":
        if new_attributes[index] == "":
          formatted.append(f"{column_name} = None,")
        else:
          formatted.append(f"{column_name} = {new_attributes[index]},")

      else:
        if new_attributes[index] == "":
          formatted.append(f" {column_name} = 'None', ")
        else:
          formatted.append(f"{column_name} = '{new_attributes[index]}',")
    formatted = '\n'.join(formatted)
    formatted = formatted[:len(formatted)-1]
    print(new_attributes[0])
    c.execute(f'''UPDATE Exercise SET {formatted} WHERE ID = {new_attributes[0]}''')
    connection.commit()


  def Add(self):
    attributes = ()
    for i in self.entries.items():
      x = getattr(i[1],'get')()
      attributes += (x,)
    parent_item = self.my_tree.selection()  # Get the selected parent item
    if parent_item:
      index = self.my_tree.index(parent_item) + 1  # Insert below the selected parent item
      self.my_tree.insert("", index, text="New record", values=attributes)
      self.Update_row_colors()  
      self.Update_ID()
    else:
      self.my_tree.insert("", index='end', text="New record", values=attributes)
      self.Update_row_colors()  
      self.Update_ID()
  def Record(self, e):
    self.Clear()
    found = self.my_tree.focus()
    if found:
        values = self.my_tree.item(found, 'values')

        for index, entry in self.entries.items():
          if index == 1:
            continue
          if index - 1 < len(values):
              entry.delete(0, tk.END)
              entry.insert(0, values[index - 1])
  def define(self):

    for i in self.column_names:
      if i.isupper():
        self.labels[self.column_names.index(i)+1]=i+'_label'
        self.entries[self.column_names.index(i)+1] = tk.Entry(tabs['tab3'],width=20)
      else:
        self.labels[self.column_names.index(i)+1]=i.capitalize()+'_label'
        self.entries[self.column_names.index(i)+1] = tk.Entry(tabs['tab3'],width=20)

      def column(arr):
        ox = self.horizontal
        oy = self.vertical + 60
        num_columns = 2
        nums = []
        label_items = list(arr.items())
        entry_items = list(self.entries.items())
        for key,value in label_items:
          j = key-1
          nums.append((ox, oy))
          ox += 300

          if j % (num_columns) == num_columns - 1:
            oy += 45
            ox = self.horizontal
          if self.column_names[key-1] == "ID":
            value = tk.Label(tab_search("Display database in treeview"),text=f"{self.column_names[key-1]} : ")
            self.entries[key]= tk.Entry(tab_search("Display database in treeview"),width=25)
          else:
            value = tk.Label(tab_search("Display database in treeview"),text=f"{self.column_names[key-1]} : ")
            self.entries[key]= tk.Entry(tab_search("Display database in treeview"),width=25)
            value.place(x = nums[key-1][0]-60,y = nums[key-1][1])
            self.entries[key].place(x = nums[key-1][0] + 65, y = nums[key-1][1] )


    ox = self.horizontal
    oy = self.vertical
    column(self.labels)
    little = 20
    Delete_Button = tk.Button(tab_search("Display database in treeview"),text="Delete Exercise",command= self.Delete)
    Delete_Button.place(x=ox-60,y=oy+little)
    Clear_Button = tk.Button(tab_search("Display database in treeview"),text="Clear entry boxes",command= self.Clear)
    Clear_Button.place(x=ox+75,y=oy+little)
    Move_Up_Button = tk.Button(tab_search("Display database in treeview"),text="Move up",command= self.Up)
    Move_Up_Button.place(x=ox+205,y=oy+little)
    Move_Down_Button = tk.Button(tab_search("Display database in treeview"),text="Move down",command= self.Down)
    Move_Down_Button.place(x=ox +290,y=oy+little)
    Update_Button = tk.Button(tab_search("Display database in treeview"),text="Update values",command= self.Update)
    Update_Button.place(x=ox+380,y=oy+little)
    Add_Exercise_Button = tk.Button(tab_search("Display database in treeview"),text="Add Exercise",command= self.Add)
    Add_Exercise_Button.place(x=ox+500,y=oy+little)
   
    self.search_entry = tk.Entry(tab_search("Display database in treeview"))
    self.search_entry.place(x=ox+700,y=oy+little)
    search_button = tk.Button(tab_search("Display database in treeview"),text="Search",command= lambda : self.Search(None))
    search_button.place(x=ox+620,y=oy+little)
    self.my_tree.bind("<ButtonRelease-1>",self.Record)
    self.my_tree.bind("<<TreeviewSelect>>", lambda event: self.Update_row_colors)

