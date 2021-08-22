from tkinter import *
from tkinter import messagebox
import matplotlib.pyplot as plt
from FileHandler import FileHandler


class DataAnalysingWindow:

    def __init__(self):
        self.window = Tk()
        self.window.title("Analyse Data")
        self.window.geometry('370x270')
        self.window.resizable(False, False)

        self.slider_val = IntVar()
        self.sleep = IntVar()
        self.qod = IntVar()
        self.prod = IntVar()
        self.time = IntVar()
        self.final_choices = []
        self.grapher = GraphCreator()

        self.title = Label(self.window, text = "Analyse data", font='Helvetica 14 bold').grid(row =0, column =0, padx = (125,0))
        self.label = Label(self.window, text="Select 2 Variables to graph:",font='Helvetica 10 bold').grid(
            row=1, column=0, sticky=W)
        self.c1 = Checkbutton(self.window, text="Sleep", fg="black", font='Helvetica 10', variable=self.sleep).grid(
            row=2, column=0, sticky=W)
        self.c2 = Checkbutton(self.window, text="Quality of day", fg="black", font="Helvetica 10",
                              variable=self.qod).grid(row=3, column=0, sticky=W)
        self.c3 = Checkbutton(self.window, text="Productivity", fg="black", font="Helvetica 10",
                              variable=self.prod).grid(row=4, column=0, sticky=W)
        self.c4 = Checkbutton(self.window, text="Time", fg="black", font="Helvetica 10", variable=self.time).grid(row=5,
                                                                                                                  column=0,
                                                                                                                  sticky=W)
        self.label2 = Label(self.window, text="Time period (weeks):", fg="black", font="Helvetica 10 bold").grid(row=6,
                                                                                                            column=0,
                                                                                                            sticky=W)
        self.slider = Scale(self.window, from_=0, to_=20, orient=HORIZONTAL, command=self.get_slider_val).grid(row=6,
                                                                                                               column=1,
                                                                                                               sticky=W)

        self.reveal_graph_button = Button(self.window, text="Reveal graph", fg="black", font="Helvetica 12 bold",
                                          command=self.get_choices).grid(row=7, column=0, sticky=W, padx= (125,0))

        self.back_button = Button(self.window, text="Back", fg="black", font="Helvetica 10",
                                  command=self.return_to_home)
        self.back_button.grid(row=0, column=1, sticky=W, padx = 75)

    def open_window(self):
        self.window.mainloop()
        return self.final_choices, self.slider_val

    def get_slider_val(self, value):
        self.slider_val = value
        return self.slider_val

    def get_choices(self):
        choices = ['Sleep', 'QoD', 'Productivity', 'Time']
        nums = []
        self.final_choices = []
        nums.append(self.sleep.get())
        nums.append(self.qod.get())
        nums.append(self.prod.get())
        nums.append(self.time.get())
        for i, j in zip(nums, choices):
            if i == 1:
                self.final_choices.append(j)

        if len(self.final_choices) == 2:
            self.grapher.makeGraph(self.final_choices[1], self.final_choices[0], int(self.slider_val))
        else:
            messagebox.showwarning("Error", "You need to select two options")

    def return_to_home(self):
        self.window.destroy()
        from HomeScreen import HomeScreen
        home_screen = HomeScreen()


class GraphCreator:
    def __init__(self):
        self.fileName = "Data.txt"
        self.fileInst = FileHandler.getInstance()

    def plotter(self, axes, data1, data2, paramdict, cat1,
                cat2):  # This function is for plotting the inputted data onto a single graph
        if cat1 == 'Time':
            axes.plot(data1, data2, label='labelInp', **paramdict)
        else:
            axes.scatter(data1, data2, label='labelInp', **paramdict)

        if cat1 == 'QoD':
            cat1 = "Quality of Day"
        if cat2 == 'QoD':
            cat2 = "Quality of Day"

        axes.set_xlabel(cat1)
        axes.set_ylabel(cat2)

    def initPlot(self, data1, data2, cat1, cat2):
        fig, ax = plt.subplots(1, 1)
        self.plotter(ax, data1, data2, {'marker': 'X'}, cat1, cat2)

        plt.show()

    def getRelevantData(self, cat1, cat2, time_period, filename):
        try:
            data = self.fileInst.readFile(filename, 1 - time_period * 7)

            cat = [cat1, cat2]
            array_of_data_stuff = [[], []]
            for i in range(2):
                for x in range(0, (time_period * 7)):
                    if cat[i] == 'Time':
                        array_of_data_stuff[i].append(x + 1)
                    else:
                        array_of_data_stuff[i].append(int(data[x][cat[i]]))

            return array_of_data_stuff[0], array_of_data_stuff[1]
        except IndexError:
            return "Error", "Error"

    def makeGraph(self, cat1, cat2, time_period):
        data1, data2 = self.getRelevantData(cat1, cat2, time_period, self.fileName)

        if data1 == "Error":
            messagebox.showwarning("Error", "Data does not go back this far")
        else:
            self.initPlot(data1, data2, cat1, cat2)
