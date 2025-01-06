from constants import *
from GIF import GIF
class Profile():
  def __init__(self):
    self.file = ""
    self.name = c.execute('''SELECT name FROM Profile''').fetchone()[0]
    self.run() 
  def change(self,file):
    try:
      self.file=file
      img = Image.open(file)
      img = img.resize((400, 400))
      self.photo = ImageTk.PhotoImage(img)
      tk.Label(tab_search("Profile"),image=self.photo).place(x=400,y=100)
      c.execute('''UPDATE Profile SET PATH = ? WHERE name = ?''',(file,self.name))
      connection.commit()
    except:
      messagebox.showwarning("Warning!","The profile picture you selected has been moved. Please find and select the new location of it")
      self.dialog()
      

  def dialog(self):
    FILETYPES = [("JPEG files", "*.jpg"),["GIF files","*.gif"]]
    filename = filedialog.askopenfilename(initialdir = os.path.expanduser("~"),title="Select a file",filetypes=FILETYPES)
    if not filename:
      return
    self.change(filename)
  def run(self):
    x = c.execute('''SELECT PATH FROM Profile WHERE name = ?''',(self.name,)).fetchone()
    img_path = x[0]
    self.change(img_path)
    
    tk.Button(tab_search("Profile"),text="Change profile picture",command=self.dialog).pack()
    table_name = "Profile"
    names = c.execute(f'''PRAGMA table_info({table_name})''').fetchall()
    info = c.execute(f'''SELECT name,age,gender,split,experience FROM Profile WHERE name = "{self.name}"''').fetchall()
    x = 50
    y = 50
    names.remove(names[0])
    for i in range(len(info[0])):
      if names[i][1] != "ID":
        tk.Label(tab_search("Profile"),text=f'{names[i][1].capitalize()}  : {info[0][i]}',font=("Helvetica",18,"bold"),foreground="red").place(x=x,y=y)
        y += 100

 
