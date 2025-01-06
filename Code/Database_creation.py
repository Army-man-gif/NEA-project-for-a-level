import sqlite3
import requests
def Database():
  print("Please wait while we set up your database, this may take some time")
  connection = sqlite3.connect("My database")
  c = connection.cursor()
  c.execute("PRAGMA foreign_keys = ON")
  c.execute('''
  CREATE TABLE IF NOT EXISTS History (
  ID INTEGER PRIMARY KEY,
  exercise TEXT,
  date DATETIME,
  reps INTEGER,
  sets INTEGER,
  PR_weight FLOAT,
  Rep_weight FLOAT,
  Enjoyable INTEGER,
  How_difficult_it_felt INTEGER,
  equipment TEXT,
  difficulty TEXT,
  muscle TEXT
  )
  ''')  
  c.execute('''
  CREATE TABLE IF NOT EXISTS Summary (
  ID INTEGER PRIMARY KEY,
  exercises TEXT,
  date DATETIME
  )
  ''')
  c.execute('''
    CREATE TABLE IF NOT EXISTS Nutrition (
    ID INTEGER PRIMARY KEY,
    Name TEXT,
    Calories FLOAT,
    Serving_Size FLOAT,
    Total_fat FLOAT,
    Saturated_fat FLOAT,
    Protein FLOAT,
    Sodium FLOAT,
    Potassium FLOAT,
    Cholesterol FLOAT,
    Carbohydrate_TOTAL FLOAT,
    Fiber FLOAT,
    Sugar FLOAT
    )
    ''')
  c.execute('''CREATE TABLE IF NOT EXISTS Profile (
      ID INTEGER PRIMARY KEY,
      name TEXT,
      age INTEGER,
      gender TEXT,
      split TEXT,
      experience TEXT,
      password TEXT,
      PATH TEXT
  )''')
  c.execute('''
  CREATE TABLE IF NOT EXISTS Split (
  ID INTEGER PRIMARY KEY ,
  name TEXT
  )''')
  c.execute('''CREATE TABLE IF NOT EXISTS Program_Routine (
  ID INTEGER PRIMARY KEY,
  name TEXT,
  Number_of_workouts_completed INTEGER,
  Split_ID INTEGER,
  FOREIGN KEY (Split_ID) REFERENCES Split(ID)
  )''')
  c.execute('''CREATE TABLE IF NOT EXISTS Workout (
  ID INTEGER PRIMARY KEY,
  name TEXT,
  Program_Routine_ID INTEGER,
  FOREIGN KEY (Program_Routine_ID) REFERENCES Program_Routine(ID)
  )''')
  c.execute('''CREATE TABLE IF NOT EXISTS Exercise (
  ID INTEGER PRIMARY KEY,
  name TEXT,
  reps INTEGER,
  sets INTEGER,
  PR_weight FLOAT,
  Rep_weight FLOAT,
  Enjoyable INTEGER,
  How_difficult_it_felt INTEGER,
  equipment TEXT,
  difficulty TEXT,
  muscle TEXT,
  Workout_ID INTEGER,
  FOREIGN KEY (Workout_ID) REFERENCES Workout(ID)
  )
  ''')



  def m(option,muscle):
    url = "https://api.api-ninjas.com/v1/exercises"
    global response
    response = requests.get(f'{url}?{option}={muscle}',headers={'X-Api-Key': 'EYubhelGF0jRmCC4ZtZKZg==pWcZsqUXcpnwlFW7'})
    global request
    request = response.json()
    for exercise in request:
      exercise.setdefault('reps', 12)
      exercise.setdefault('sets', 3)
      exercise.setdefault('PR_weight', 0.0)
      exercise.setdefault('Rep_weight', 0.0)
      exercise.setdefault('Enjoyable', 0)
      exercise.setdefault('How_difficult_it_felt', 0)
    return request
  arr = ["muscle","type"]
  arr2 = ["glutes","biceps","forearms","traps","hamstrings","triceps","calves","quadriceps","abductors","lats","lower_back","middle_back","abdominals","cardio","stretching","strength"]

  c.execute('''
  INSERT INTO Split VALUES (
  0,"Five Day Split"
  )
  ''')
  class insert():
    def __init__(self,indexes_of_workouts_array,Program_ID,Program_Name):
      self.index = indexes_of_workouts_array
      self.Program_ID = Program_ID
      self.Program_Name = Program_Name
      self.current = [m(arr[1],arr2[self.index[0]])]
      for i in range(len(self.index)-1):
        self.current.append(m(arr[0],arr2[self.index[i]]))

    def iterate(self):
      c.execute(f'''
      INSERT INTO Program_Routine VALUES (
      {self.Program_ID},"{self.Program_Name}",0,0
      )
      ''')

      connection.commit()

      for i in range(len(self.current)):
        c.execute(f'''
        INSERT INTO Workout (name,Program_Routine_ID)VALUES(
       "{arr2[self.index[i]]}",{self.Program_ID}
        )
        ''')
        connection.commit()
        for j in range(len(self.current[i])):
          c.execute(f'''
          INSERT INTO Exercise (name,reps,sets,PR_weight,Rep_weight,Enjoyable,How_difficult_it_felt,equipment,difficulty,muscle,Workout_ID)VALUES(
          "{self.current[i][j]['name']}",{self.current[i][j]['reps']},{self.current[i][j]['sets']},{self.current[i][j]['PR_weight']},{self.current[i][j]['Rep_weight']},{self.current[i][j]['Enjoyable']},{self.current[i][j]['How_difficult_it_felt']},"{self.current[i][j]['equipment']}","{self.current[i][j]['difficulty']}","{self.current[i][j]['muscle']}",{workouts_IDs[i]}
          )
          ''')
          connection.commit()


  arr2 = ["glutes","biceps","forearms","traps","hamstrings","triceps","calves","quadriceps","abductors","lats","lower_back","middle_back","abdominals","cardio","stretching","strength","chest"]

  Program_Days = {
    "Legs": [0,4,6,7,8], "Arms": [1,2,5], "Back": [9,10,11], "Shoulders": [3], "Full body": [1,3,4,5,7,9,11,12],"Chest":[16]
  }

  nums = []
  nums.append(0)
  count = 0
  for i,value in enumerate(Program_Days):
    count = count + len(Program_Days[value])
    nums.append(count)
  nums.pop()
  workouts_IDs = []
  for j,value2 in enumerate(Program_Days):
    for z,value3 in enumerate(Program_Days[value2]):
      workout_ID = z+nums[j]
      workouts_IDs.append(workout_ID)
      program_ID = j

  for p,value4 in enumerate(Program_Days):
    ins=  insert(Program_Days[value4],p,value4)
    ins.iterate()
Database()
