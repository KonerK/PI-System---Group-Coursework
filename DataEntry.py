from tkinter import *
from FileHandler import FileHandler
from datetime import date


# super class for data entry pages
class dataEntryPage:

    def __init__(self, root, dimension='400x350', titleText='Example Title', questionText='Example question?'):
        self.saveData = None

        # master is passed from the child class
        self.root = root
        self.root.title("Data Entry")
        self.root.geometry(dimension)
        self.root['bg'] = '#F0F0F0'

        # create common frames for all three data pages
        self.titleFrame = Frame(self.root, height='75', width='400', bg='#F0F0F0')
        self.titleFrame.grid(column=0, row=0)

        self.dataFrame = Frame(self.root, height='250', width='400', bg='#F0F0F0')
        self.dataFrame.grid(column=0, row=1)

        self.saveFrame = Frame(self.root, height='25', width='400', bg='#F0F0F0')
        self.saveFrame.grid(column=0, row=2)

        # title different for each data page
        self.Title = Label(self.titleFrame, text=titleText, fg='black', bg='#F0F0F0', height='3', font="Helvetica 18 bold")
        self.Title.grid(column=0, row=0)

        self.buildDataInput(questionText)

    # this can be overridden for the sleep page
    def buildDataInput(self, questionText):
        # question and slider common for productivity and QoD
        self.qLabel = Label(self.dataFrame, text=questionText, fg='black', bg='#F0F0F0', height='3',
                            font=("Helvetica 16"))
        self.qLabel.grid(column=0, row=0, padx=(10, 10))

        self.slider = Scale(self.dataFrame, from_=0, to=10, orient=HORIZONTAL, bg='#F0F0F0', length='300')
        self.slider.grid(column=0, row=1)

    # accessor for saved data
    def getData(self):
        return self.saveData


# Productivity page
class prodPage(dataEntryPage):

    def __init__(self):
        self.prodRoot = Tk()

        dataEntryPage.__init__(self, self.prodRoot, titleText='Productivity',
                               questionText='How do you rate your productivity today?')

        def saveData():
            val = int(self.slider.get())
            self.saveData = val
            self.prodRoot.destroy()
            # print(self.prodValues)

        self.saveButton = Button(self.saveFrame, text='Save', font=("Helvetica 16"), command=saveData)
        self.saveButton.grid(pady=(30, 0))

        self.prodRoot.mainloop()


# Quality of Day page
class qodPage(dataEntryPage):

    def __init__(self):
        self.diaryEntry = None
        self.qodRoot = Tk()

        dataEntryPage.__init__(self, self.qodRoot, dimension='400x500', titleText='Quality of Day',
                               questionText='How do you feel about your day today?')

        # additional diary feature on QoD page
        self.commentLabel = Label(self.dataFrame, text='Diary Entry:', fg='black', bg='#F0F0F0', height='3',
                                  font=("Helvetica 16"))
        self.commentLabel.grid(column=0, row=2, padx=(10, 260))

        self.diaryTxt = Text(self.dataFrame, height=5, width=40)
        self.diaryTxt.grid(column=0, row=3)

        def saveData():
            val = int(self.slider.get())
            entry = self.diaryTxt.get(1.0, 'end-1c')
            self.diaryTxt.delete(1.0, 'end')
            self.saveData = val
            self.diaryEntry = entry
            self.qodRoot.destroy()

        self.saveButton = Button(self.saveFrame, text='Save', font=("Helvetica 16"), command=saveData)
        self.saveButton.grid(pady=(30, 0))

        self.qodRoot.mainloop()

    def getDiary(self):
        return self.diaryEntry


class sleepPage(dataEntryPage):

    def __init__(self):

        self.sleepRoot = Tk()

        self.OptionList = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
        self.time = ['am', 'pm']

        dataEntryPage.__init__(self, self.sleepRoot, titleText='Sleep Quality')

        def saveData():
            x = int(self.startClicked.get())
            y = int(self.endClicked.get())

            ampm = [self.ampmClicked1.get(), self.ampmClicked2.get()]

            if ampm[0] != ampm[1]:
                ans = (12 - x) + y
            else:
                if x <= y:
                    ans = y - x
                else:
                    ans = (12 - x) + 12 + y
            self.saveData = ans
            self.sleepRoot.destroy()
            # print(self.timeList)

        self.saveButton = Button(self.saveFrame, text='Save', font=("Helvetica 16"), command=saveData)
        self.saveButton.grid(pady=(30, 0))

        self.sleepRoot.mainloop()

    # Overrides Parent class
    def buildDataInput(self, questionText):

        self.startLabel = Label(self.dataFrame, text='Start Time:', fg='black', bg='#F0F0F0', height='3',
                                font=("Helvetica 16"))
        self.startLabel.grid(column=0, row=0, padx=(50, 10))

        # datatype of menu text
        self.startClicked = StringVar()

        # initial menu text
        self.startClicked.set("10")

        # Create Dropdown menu for start times
        startDrop = OptionMenu(self.dataFrame, self.startClicked, *self.OptionList)
        startDrop.config(font=("Helvetica 16"))
        startDrop.grid(column=1, row=0, padx=(10, 10))

        # drop down meny for start am/pm
        self.ampmClicked1 = StringVar()

        self.ampmClicked1.set("pm")

        self.ampmDrop1 = OptionMenu(self.dataFrame, self.ampmClicked1, *self.time)
        self.ampmDrop1.config(font=("Helvetica 16"))
        self.ampmDrop1.grid(column=2, row=0, padx=(10, 10))

        self.endLabel = Label(self.dataFrame, text='End Time:', fg='black', bg='#F0F0F0', height='3',
                              font=("Helvetica 16"))
        self.endLabel.grid(column=0, row=1, padx=(30, 0))

        # datatype of menu text
        self.endClicked = StringVar()

        # initial menu text
        self.endClicked.set("07")

        # Create Dropdown menu for end time
        self.endDrop = OptionMenu(self.dataFrame, self.endClicked, *self.OptionList)
        self.endDrop.config(font=("Helvetica 16"))
        self.endDrop.grid(column=1, row=1)

        # drop down menu of end am/pm
        self.ampmClicked2 = StringVar()

        self.ampmClicked2.set("am")

        self.ampmDrop2 = OptionMenu(self.dataFrame, self.ampmClicked2, *self.time)
        self.ampmDrop2.config(font=("Helvetica 16"))
        self.ampmDrop2.grid(column=2, row=1)


# class that leads the user through the pages
# then saves the input data

class DataBuffer():
    def __init__(self):
        self.dataLine = None

        # get and format today's date
        self.dateNow = date.today()
        self.currentDate = str(self.dateNow.day) + '/' + str(self.dateNow.month) + '/' + str(self.dateNow.year)
        self.fileHandler = FileHandler.getInstance()

    def run(self):
        # lead users through data pages
        # then access saved data
        sleep = sleepPage()
        sleepData = sleep.getData()

        productivity = prodPage()
        prodData = productivity.getData()

        QoD = qodPage()
        qodData = QoD.getData()
        diaryCurrent = QoD.getDiary()

        # save data to file
        self.dataLine = 'Date:' + self.currentDate + ' Sleep:' + str(sleepData) + ' Productivity:' + str(
            prodData) + ' QoD:' + str(qodData)
        self.fileHandler.appendData('Data.txt', [self.dataLine])

        # save diary entries to file
        self.diaryLine = 'Date: ' + self.currentDate + ' Entry:' + str(diaryCurrent)
        self.fileHandler.appendData('Diary.txt', [self.diaryLine])
        from HomeScreen import HomeScreen
        home_screen = HomeScreen()



