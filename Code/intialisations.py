from shared import complete
if complete:
  from constants import *
  root.lift()
  from GUI_basics import *


  from History import History



  from Profile import Profile
  P = Profile()
  from Workout import Workout_display_class
  tab_search("Workouts display").tkraise()
  Workout = Workout_display_class()
  from Calendar import Calendar_Display
  now = datetime.now()
  Cal = Calendar_Display(now)
  Cal.display_Calendar_widget()
  from Cal import Caloric
  C = Caloric("Male") 
  from Treeview import display_in_treeview
  from Graphing import Graphing 
  G = Graphing()  
  G.search()
  from Search_for_Images import *
  #Scrape_and_save_Images_Locally_Execution_Function(True,0)   
  #Scrape_and_save_Images_Locally_Execution_Function(False,['Arms Day','Shoulders Day','Legs Day','Back Day','Full body Day'])
  #Scrape_and_save_Images_Locally_Execution_Function(False,['Legs Day'])

  try:
      root.mainloop()
  except Exception as e:
      print(f"An error occurred: {e}")
