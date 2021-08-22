from tkinter import *
from tkinter.ttk import Progressbar
from FileHandler import FileHandler


class BadgesGUI:
    def __init__(self):
        self.sleep_days = 0
        self.prod_days = 0
        self.qod_days = 0
        self.goal_hours = 0
        self.sleep_set = 0
        self.qod_set = 0
        self.prod_set = 0
        # List which stores the number of badges obtained as bronze, silver and gold(in that order)
        self.badges_achieved = [1, 2, 3]
        fileHandler = FileHandler.getInstance()
        data = fileHandler.readFile("Goals.txt", 1, -1, True)
        goals = data[0]
        self.sleep_set = int(goals['Sleep'])
        self.prod_set = int(goals['Productivity'])
        self.qod_set = int(goals['QoD'])

        datafile = "Data.txt"
        self.countDays(datafile, fileHandler)

        self.badges_window = Tk()
        self.badges_window.title("Badges")
        self.badges_window.geometry("400x400")
        self.badges_window.resizable(False, False)

        # Back Button closes the window.
        back_button = Button(self.badges_window, text="Back", font='Helvetica 10', command=self.back_button_pressed)

        title = Label(self.badges_window, text="Badges", font='Helvetica 14 bold', anchor=CENTER)
        empty_label = Label(self.badges_window, padx=30)
        sub_heading1 = Label(self.badges_window, text="Current Goals and Progress:", font='Helvetica 12 bold')
        label1 = Label(self.badges_window, text="   Badge Grade", font='Helvetica 12 bold')

        self.sleep_days = self.check_overflow(self.sleep_days, self.badges_achieved)
        self.prod_days = self.check_overflow(self.prod_days, self.badges_achieved)
        self.qod_days = self.check_overflow(self.qod_days, self.badges_achieved)

        sleep_label = Label(self.badges_window,
                            text="Slept for more than " + str(self.sleep_set) + " hours for " + str(self.sleep_days) +
                                 " days", font='Helvetica 10')
        sleep_prog = Progressbar(self.badges_window, orient=HORIZONTAL, length=150, mode='determinate')
        sleep_goal = self.determine_grade(self.sleep_days, self.badges_achieved)[1]
        sleep_prog['value'] = self.sleep_days / sleep_goal * 100
        sleep_frac = Label(self.badges_window, text=str(self.sleep_days) + "/" + str(sleep_goal))

        prod_label = Label(self.badges_window, text="Had " + str(self.prod_days) + " days where you were productive( "
                                                    + str(self.prod_set) + "/10)", font='Helvetica 10')
        prod_prog = Progressbar(self.badges_window, orient=HORIZONTAL, length=150, mode='determinate')
        prod_goal = self.determine_grade(self.prod_days, self.badges_achieved)[1]
        prod_prog['value'] = self.prod_days / prod_goal * 100
        prod_frac = Label(self.badges_window, text=str(self.prod_days) + "/" + str(prod_goal))

        qod_label = Label(self.badges_window, text="Had " + str(self.qod_days) + " days where you enjoyed yourself ("
                                                   + str(self.qod_set) + "/10)", font='Helvetica 10')
        qod_prog = Progressbar(self.badges_window, orient=HORIZONTAL, length=150, mode='determinate')
        qod_goal = self.determine_grade(self.qod_days, self.badges_achieved)[1]
        qod_prog['value'] = self.qod_days / qod_goal * 100
        qod_frac = Label(self.badges_window, text=str(self.qod_days) + "/" + str(qod_goal))

        sub_heading2 = Label(self.badges_window, text="Badges Awarded: ", font='Helvetica 12 bold')
        bronze_level = Label(self.badges_window, text="Bronze ", font='Helvetica 10')
        silver_level = Label(self.badges_window, text="Silver ", font='Helvetica 10')
        gold_level = Label(self.badges_window, text="Gold ", font='Helvetica 10')

        bronze = Label(self.badges_window, text=str(self.badges_achieved[0]), bg="tan2", padx=30)
        silver = Label(self.badges_window, text=str(self.badges_achieved[1]), bg="light grey", padx=30)
        gold = Label(self.badges_window, text=str(self.badges_achieved[2]), bg="gold2", padx=30)

        sleep_grade = Label(self.badges_window, bg=self.determine_grade(self.sleep_days, self.badges_achieved)[0],
                            padx=15)
        prod_grade = Label(self.badges_window, bg=self.determine_grade(self.prod_days, self.badges_achieved)[0],
                           padx=15)
        qod_grade = Label(self.badges_window, bg=self.determine_grade(self.qod_days, self.badges_achieved)[0], padx=15)

        title.grid(row=0, column=0)
        empty_label.grid(row=1, column=2)
        back_button.grid(row=0, column=1)
        sub_heading1.grid(row=2, column=0)
        label1.grid(row=2, column=1)
        sleep_label.grid(row=4, column=0)
        sleep_grade.grid(row=5, column=1)
        sleep_prog.grid(row=5, column=0)
        sleep_frac.grid(row=6, column=0)

        prod_label.grid(row=7, column=0)
        prod_grade.grid(row=8, column=1)
        prod_prog.grid(row=8, column=0)
        prod_frac.grid(row=9, column=0)

        qod_label.grid(row=10, column=0)
        qod_grade.grid(row=11, column=1)
        qod_prog.grid(row=11, column=0)
        qod_frac.grid(row=12, column=0)
        sub_heading2.grid(row=13, column=0)

        bronze_level.grid(row=14, column=0)
        silver_level.grid(row=15, column=0)
        gold_level.grid(row=16, column=0)
        bronze.grid(row=14, column=1)
        silver.grid(row=15, column=1)
        gold.grid(row=16, column=1)

        self.badges_window.mainloop()

    # Method checks whether goal grade has been achieved and if true, it returns the modulo of number of days.
    @staticmethod
    def check_overflow(days, badges_achieved):
        if days > 60:
            badges_achieved[2] += 1
            return days % 60
        else:
            return days

    # Method returns a colour label and goal days according to the number of days
    @staticmethod
    def determine_grade(days, badges_achieved):
        if days > 30:
            return "gold2", 60
        elif days > 7:
            if days == 30:
                badges_achieved[1] += 1
            return "light grey", 30
        else:
            if days == 7:
                badges_achieved[0] += 1
            return "tan2", 7

    def countDays(self, filename, fileHandler):
        filedata = fileHandler.readFile(filename, 1, -1, True)
        # Going through data in file to count number of days where respective goals have been met
        for data in filedata:
            prod = data['Productivity']
            if prod == "None": continue
            if int(prod) >= self.prod_set:
                self.prod_days += 1
            sleep = data['Sleep']
            if sleep == "None": continue
            if int(sleep) >= self.sleep_set:
                self.sleep_days += 1
            qod = data['QoD']
            if qod == "None": continue
            if int(qod) >= self.qod_set:
                self.qod_days += 1

    def back_button_pressed(self):
        self.badges_window.destroy()
        from HomeScreen import HomeScreen
        home_screen = HomeScreen()
