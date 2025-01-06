from constants import *
def History():
    def show_history():
        x = c.execute('''SELECT exercise,reps,sets,PR_weight,Rep_weight,Enjoyable,How_difficult_it_felt,equipment,difficulty,muscle FROM History''').fetchall()
        text_widget.delete("1.0", "end")
        # Insert the data into the Text widget
        for i in range(len(x)):
          if i == 0:
            text_widget.insert("end"," ".join(map(str, x[i])))
          else:
            text_widget.insert("end", "\n" + " ".join(map(str, x[i])))

        # Add the Text widget to the window
        text_widget.pack(side="top", fill="both", expand=True)

        # Create a scrollbar for the Text widget
        scrollbar = tk.Scrollbar(tab_search("History"), command=text_widget.yview)
        scrollbar.pack(side="right", fill="y")
        text_widget.configure(yscrollcommand=scrollbar.set)

    text_widget = tk.Text(tab_search("History"), wrap="none")
    tk.Button(tab_search("History"),text="Click to view history",command=show_history).pack()

History()
