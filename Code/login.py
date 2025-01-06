from basics import *
from shared import complete
from start import start
trials = 0



            
def reset():
  name = input("Enter your name: ")
  password = input("You've forgetten your old password - Enter your new password: ")
  try:
    print("Please wait while your password is reset...")
    c.execute('''
      UPDATE Profile
      SET password = ?
      WHERE name = ?
      ''',(password,name))
    connection.commit()
  except Exception as e:
    print(e,"That name isn't valid. Enter the correct name for tohis account")
    reset()
  
def login(choice,trials):
  global name,complete
  # Sign up
  if choice == 1:    
    print("Sign up: ")
    print()
    cur = []
    name = input("Name: ")
    age = int(input("Age: "))
    gender = input("Gender: ")
    password = input("Password: ")
    c.execute('''
    INSERT INTO Profile (name,age,gender,split,password,PATH) VALUES (?,?,?,?,?,?)
    ''',(name,age,gender,"Five Day Split",password,find_file("SignIn.jpg")))
    connection.commit()
  # Login
  if choice == 2:
    print("Login")
    print()
    name = input("Enter your name: ")
    password = input("Enter your password: ")
    database_info_of_users = c.execute("SELECT * FROM Profile WHERE name = ? and password = ? ",(name,password)).fetchall()
    if trials <= 1:
      if database_info_of_users:
        print("Login successful")
        complete = True
        start()
      else:
        print("Login unsuccesssful")
        trials += 1
        login(2,trials)
    else:
      print("Login incorrect too many times, reset your password")
      reset()
