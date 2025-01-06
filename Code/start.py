from shared import complete
from constants import *
from GUI_basics import *
from History import History
from Profile import Profile
from Workout import Workout_display_class
from Calendar import Calendar_Display
from Cal import Caloric
from Treeview import display_in_treeview
from Graphing import Graphing
from Search_for_Images import *
from Register import login_window   
def start():
    print("Starting appplication")
    root.deiconify()
    root.lift()
    P = Profile()
    tab_search("Workouts display").tkraise()
    Workout = Workout_display_class()
    now = datetime.now()
    Cal = Calendar_Display(now)
    Cal.display_Calendar_widget()
    C = Caloric("Male")
    G = Graphing()
    G.search()
    #Scrape_and_save_Images_Locally_Execution_Function(True,0)
    #Scrape_and_save_Images_Locally_Execution_Function(False,['Arms Day','Shoulders Day','Legs Day','Back Day','Full body Day'])
    #Scrape_and_save_Images_Locally_Execution_Function(False,['Legs Day'])
    try:
        root.mainloop()
    except Exception as e:
        print(f"An error occurred: {e}")
