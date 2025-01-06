from basics import *
from login import login
from start import start
from Register import GUI_login,login_window





#print(c.execute('''SELECT Enjoyable FROM Exercise WHERE name = ?''',("Step-up with knee raise",)).fetchall())
#c.execute('''DELETE FROM PROFILE''')
available = c.execute('''SELECT * FROM Profile''').fetchall()

if available: 
  GUI_login(2)    
else:
  GUI_login(1)  

  
login_window.mainloop()





  


























#available = c.execute('''SELECT * FROM Profile''').fetchall()
#if available:
#  login(2,0)
#  start()
#else:
#  login(1,0)
#  start()
