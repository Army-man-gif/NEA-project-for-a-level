from constants import *
class GIF():
  def __init__(self,file,tab,W,H,x,y,speed):
    self.file = file
    self.W = W
    self.H = H
    self.speed = speed
    self.tab = tab
    self.x = x
    self.y = y
    self.execute()

  def play_gif(self):
    #tk.Label(self.tab,text="Gifs").pack()
    file = self.file
    global img
    print(file)
    img = Image.open(file)
    num = img.n_frames
    lbl = tk.Label(self.tab)
    #print(num)
    lbl.place(x = self.x,y = self.y)
    for img in ImageSequence.Iterator(img):
      img = img.resize((self.W, self.H))
      img = ImageTk.PhotoImage(img)
      lbl.config(image=img)
      time.sleep(self.speed)
      root.update()
    lbl.destroy()
  def execute(self):
    self.play_gif()
