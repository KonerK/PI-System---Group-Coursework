from tkinter import *
from FileHandler import FileHandler


class GoalsPage:
    def __init__(self):
        self.master = Tk()
        self.master.title("Goals:")
        self.master.geometry('340x200')
        self.master.resizable(False, False)

        # self.back_button = Button(self.badges_window, text="Back", font='Helvetica 10', command=self.back_button_pressed)
        self.back_button = Button(self.master, text="Back",font='Helvetica 10', command=self.return_to_home)
        self.back_button.grid(row=0, column=1, sticky=E)

        self.title = Label(self.master, text="Goals", font='Helvetica 14 bold')
        self.title.grid(row=0, column=0, sticky=W, padx=(100, 25), pady=(10))

        self.edit = Label(self.master, text="Edit goal:", font='Helvetica 10 italic')
        self.edit.grid(row=1, column=1, sticky=W, padx=(25, 0))

        original_sleep = 0
        original_productivity = 0
        original_day_rating = 0

        # get original values for the variables stored in a text file
        file_handler = FileHandler.getInstance()
        file_data = file_handler.readFile("Goals.txt", 1, -1, True)
        for data in file_data:
            original_sleep = data['Sleep']
            original_productivity = data['Productivity']
            original_day_rating = data['QoD']

        # sleep option menu setup
        self.sleep_hours = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16',
                            '17', '18']
        self.sleep_hours_goal = StringVar(self.master)
        self.sleep_hours_goal.set(original_sleep)  # default value
        self.sleep_duration = OptionMenu(self.master, self.sleep_hours_goal, *self.sleep_hours, )
        self.sleep_duration.grid(row=2, column=1, sticky=E, padx=(25, 0))
        self.sleep_hours_goal.trace_add('write', self.update_sleep_goal)

        # day rating menu setup
        self.day_ratings = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        self.day_rating_goal = StringVar()
        self.day_rating_goal.set(original_day_rating)
        self.day_rating = OptionMenu(self.master, self.day_rating_goal, *self.day_ratings)
        self.day_rating.grid(row=3, column=1, sticky=E)
        self.day_rating_goal.trace('w', self.update_day_rating_goal)

        # productivity percentage menu setup
        self.productivity_ratings = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        self.productivity_rating_goal = StringVar()
        self.productivity_rating_goal.set(original_productivity)
        self.productivity_rating = OptionMenu(self.master, self.productivity_rating_goal,
                                              *self.productivity_ratings)
        self.productivity_rating.grid(row=4, column=1, sticky=E)
        self.productivity_rating_goal.trace('w', self.update_productivity_goal)

        # goal messages
        self.sleep_label = Label(self.master,
                                 text="Sleep an average of {} hours a day.".format(self.sleep_hours_goal.get()), font ='Helvetica 10 ')
        self.sleep_label.grid(row=2, column=0, sticky=W)


        self.day_rating_label = Label(self.master,
                                      text="Achieve an average day rating of {}/10.".format(self.day_rating_goal.get()), font ='Helvetica 10')
        self.day_rating_label.grid(row=3, column=0, sticky=W)

        self.productivity_label = Label(self.master, text="Maintain an average productivity of {}/10.".format(
            self.productivity_rating_goal.get()), font ='Helvetica 10')
        self.productivity_label.grid(row=4, column=0, sticky=W)

        self.master.mainloop()

    def update_sleep_goal(self, *args):
        self.sleep_label.configure(text="Sleep an average of {} hours a day.".format(self.sleep_hours_goal.get()), font ='Helvetica 10')
        self.update_goals_document()

    def update_day_rating_goal(self, *args):
        self.day_rating_label.configure(text="Achieve an average day rating of {}/10.".format(self.day_rating_goal.get()), font ='Helvetica 10')
        self.update_goals_document()

    def update_productivity_goal(self, *args):
        self.productivity_label.configure(
            text="Maintain an average productivity of {}/10.".format(self.productivity_rating_goal.get()), font ='Helvetica 10')
        self.update_goals_document()

    def update_goals_document(self):
        goals_document = open("Goals.txt", "w")
        goals_document.write(
            "Sleep:{} Productivity:{} QoD:{}".format(self.sleep_hours_goal.get(), self.productivity_rating_goal.get(),
                                                     self.day_rating_goal.get()))
        goals_document.close()

    # Implement function to exit current window and return to home page
    def return_to_home(self):
        self.master.destroy()
        from HomeScreen import HomeScreen
        home_screen = HomeScreen()
