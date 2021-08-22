from tkinter import *
from BadgesGUI import BadgesGUI
from GoalsPage import GoalsPage
from TaskPage import TasksPage
from DataEntry import DataBuffer
from FileHandler import FileHandler
from DataAnalysisGUI import DataAnalysingWindow


def read_tasks_file():
    # Reading tasks from tasks file
    file_handler = FileHandler.getInstance()
    task_list = file_handler.readFile("Tasks.txt", processData = False)
    return task_list


class HomeScreen:

    def __init__(self):
        # Creating Master
        self.root = Tk()
        self.root.title("Home")
        self.root.configure(bg='#F0F0F0')
        self.root.resizable(False, False)
        self.task_list = read_tasks_file()

        # Creating the frames for each section on the home menu
        frame_for_task_area = Frame(self.root, width=400, height=250, bg='#F0F0F0')
        frame_for_task_area.grid(row=0, column=0, padx=20, pady=20)
        frame_for_data_buttons = Frame(self.root, width=400, height=150, bg='#F0F0F0')
        frame_for_data_buttons.grid(row=1, column=0, padx=20, pady=20)

        # Creating Buttons to analyse data (show graphs), add data, look at badges, and add goals
        self.analyse_data_button = Button(frame_for_data_buttons, text="Analyse Data", font='Helvetica 10', width=10, height=2,
                                          command=self.analyse_data_pressed)
        self.analyse_data_button.grid(row=1, column=0)
        self.add_button = Button(frame_for_data_buttons, text="+", font='Helvetica 10', width=10, height=2,
                                 command=self.add_button_pressed)
        self.add_button.grid(row=0, column=0)
        self.badges_button = Button(frame_for_data_buttons, text="Badges",font='Helvetica 10', width=10, height=2,
                                    command=self.badges_button_pressed)
        self.badges_button.grid(row=1, column=1)
        self.goal_button = Button(frame_for_data_buttons, text="Goals",font='Helvetica 10', width=10, height=2,
                                  command=self.goal_button_pressed)
        self.goal_button.grid(row=0, column=1)

        # Creating task list button, and textbox
        self.task_list_button = Button(frame_for_task_area, text="Tasks", font='Helvetica 10', command=self.task_button_pressed)
        self.task_list_button.grid(row=0, column=1, pady=2)
        self.task_textbox = Text(frame_for_task_area, width=30, height=10)
        self.task_textbox.grid(row=1, column=1)
        self.display_tasks_on_menu()
        self.task_textbox.configure(state='disabled')
        self.root.mainloop()

    def analyse_data_pressed(self):
        self.root.destroy()
        data_analysis_window = DataAnalysingWindow()
        data_analysis_window.open_window()

    def add_button_pressed(self):
        self.root.destroy()
        env = DataBuffer()
        env.run()

    def task_button_pressed(self):
        self.root.destroy()
        task_page = TasksPage()

    def badges_button_pressed(self):
        self.root.destroy()
        badges = BadgesGUI()

    def goal_button_pressed(self):
        self.root.destroy()
        goals_page = GoalsPage()

    def display_tasks_on_menu(self):
        self.task_textbox.delete(1.0, END)
        for task in self.task_list:
            self.task_textbox.insert(INSERT, task + '\n')


def main():
    home_screen = HomeScreen()


if __name__ == "__main__":
    main()
