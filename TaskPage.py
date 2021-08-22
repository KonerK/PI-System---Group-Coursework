from tkinter import *
from tkinter import ttk
from FileHandler import FileHandler
from tkinter import messagebox


# Scrollable Frames https://blog.teclado.com/tkinter-scrollable-frames/
class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")


class TasksPage:
    def __init__(self):
        self.master = Tk()
        self.master.title("Tasks")
        self.master.geometry('400x400')
        self.task_list = []
        self.master.resizable(False, False)

        self.back_button_frame = Frame(self.master)
        self.back_button = Button(self.back_button_frame, text="Back",font='Helvetica 10', command=self.return_to_home)
        self.back_button.pack(side=RIGHT)
        self.back_button_frame.pack(fill=X)

        self.main_frame = ScrollableFrame(self.master)
        self.title = Label(self.main_frame.scrollable_frame, anchor = NW, text="My Tasks", font= 'Helvetica 14 bold', padx = 150)
        self.title.pack(fill=X)

        # get original values for the variables stored in a text file
        self.fileHandler = FileHandler.getInstance()
        file_data = self.fileHandler.readFile("Tasks.txt", 1, -1, False)
        self.task_list_empty = True
        self.no_tasks_label = Label(self.main_frame.scrollable_frame, text="No active tasks",
                                    font='Helvetica 12 italic',
                                    fg='grey')
        if file_data == []:  # if no tasks in document
            self.no_tasks_label.pack(side=LEFT)
        else:
            self.task_list_empty = False
            for data in file_data:
                self.add_task(data, False)

        self.main_frame.pack()
        self.add_tasks_frame = Frame(self.master)
        self.task_entry = Text(self.add_tasks_frame, height=2, width=22)
        self.task_entry.pack(side=LEFT)
        self.add_button = Button(self.add_tasks_frame, text="Add task", font='Helvetica 10',
                                 command=lambda: self.add_task(self.task_entry.get("1.0", "end-1c"), True), height=1,
                                 width=6)
        self.add_button.pack(side=RIGHT)
        self.add_tasks_frame.pack()
        self.master.mainloop()

    def add_task(self, task, new_task):

        if (task not in self.task_list) and len(task) != 0:
            self.task_list_empty = False
            if not self.task_list_empty:
                self.no_tasks_label.destroy()
                self.task_list_empty = False

            if new_task:
                self.task_entry.delete("0.0", "end-1c")
                # Open a file with access mode 'a'
                file_object = open('Tasks.txt', 'a')
                # Append 'hello' at the end of file
                file_object.write(task)
                file_object.write('\n')
                # Close the file
                file_object.close()

            task_button = None
            task_button = Checkbutton(self.main_frame.scrollable_frame,
                                      command=lambda: self.remove_task(task_button, task), text=task,
                                      anchor="nw",
                                      font='Helvetica 12', fg='grey', padx=2, pady=2)
            task_button.pack(fill=X)
            self.task_list.append(task)
        else:
            messagebox.showerror('Add task error', 'Please enter an appropriate task.')

    def remove_task(self, task_button, task):
        task_button.destroy()
        # https://stackoverflow.com/questions/4710067/how-to-delete-a-specific-line-in-a-file
        with open("Tasks.txt", "r") as f:
            lines = f.readlines()
        with open("Tasks.txt", "w") as f:
            for line in lines:
                if line.strip("\n") != task:
                    f.write(line)

        file_data = self.fileHandler.readFile("Tasks.txt", 1, -1, False)
        if file_data == []:  # if task list empty show no tasks label
            self.task_list_empty = True
            self.no_tasks_label = Label(self.main_frame.scrollable_frame, text="No active tasks",
                                        font='Helvetica 12 italic',
                                        fg='grey')
            self.no_tasks_label.pack(side=LEFT)
        self.task_list.remove(task)

    def return_to_home(self):
        self.master.destroy()
        from HomeScreen import HomeScreen
        home_screen = HomeScreen()
