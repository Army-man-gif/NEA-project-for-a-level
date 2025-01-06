from constants import *

def Frame(frame):
  if frame == tab_search("Display database in treeview"):
    #frame.config(width=W+600)
    for i in frames:
      if i != frame:
        i.config(width=W+1000,height=H+300)
  elif frame == tab_search("Workouts display"):
    #frame.config(width=W+150,height=H)
    for i in frames:
      if i != frame:
        i.config(width=W+1000,height=H+300)
  elif frame == tab_search("Caloric stuff"):
    frame.config(background="black")
    #frame.config(width=W+300,height=H)
    for i in frames:
      if i != frame:
        i.config(width=W+1000,height=H+300)
  else:
    for i in frames:
      i.config(width=W+1000,height=H+300)
  frame.tkraise()

options_frame = tk.Frame(root,width=W-400,height=H+300,highlightbackground='orange',highlightthickness=10,background="turquoise")
options_frame.place(x=0,y=0)
for index,val in enumerate(tab_strings):
  tabs[val] = tk.Frame(root,height=H+300,width=W+1000,highlightthickness=10,background=colours[index])



for i in tabs.keys():
  frames.append(tabs[i])  
  tabs[i].place(x=W-400,y=0)
  tabs[i].pack_propagate(False)
def Button(first_half_of_name,second_half_of_name,full_name):
  number_of_buttons = len(tab_strings)
  button_gap_distance = H // (number_of_buttons)
  button_gap_distance = int(button_gap_distance)
  number = re.findall(r'\d+', first_half_of_name)
  number = int(number[0])
  Buttons[full_name] = tk.Button(options_frame,text=texts[number-1],height=5,width=24,command=lambda:Frame(tabs[first_half_of_name]),wraplength=75)
  coordinate = (number-1) * (button_gap_distance)
  Buttons[full_name].place(x=0,y=coordinate)
for i in tabs.keys():
  second_part = "_button"
  combined = i + second_part
  Button(i,second_part,combined)

