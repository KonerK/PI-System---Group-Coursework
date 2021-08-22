# Class to handle reading and writing data from a given file
class FileHandler:
    # Meant to be a private attribute but python doesn't have any private variables (apart from usual scope
    # restrictions)
    _instance = None

    # Handles getting class instance and creates the class instance if it doesn't already exist
    @staticmethod
    def getInstance():
        if FileHandler._instance == None:
            FileHandler()

        return FileHandler._instance

    # Meant to be a private constructor but no such thing in python, work around is throwing an exception if you try
    # to create more than one instance of the class
    def __init__(self):
        if FileHandler._instance != None:
            raise Exception("You are trying to create another instance of a FileHandler class")
        else:
            FileHandler._instance = self

    # Reading from file
    # It will read up until and including the line specified by endLine
    # If startLine is not equal to 1 then the lines before startLine will be discarded
    def readFile(self, filename, startLine=1, endLine=-1, processData=True):
        with open(filename) as file:
            data = file.readlines()
            if endLine != -1: data = data[:endLine]
            file.close()
            data = [line.strip() for line in data[startLine - 1:]]  # Gets rid of newline characters (the "\n")
            return self.processData(data) if processData else data
            # If you just want an array of all the lines set processData = False when calling this method

    # Appends given list of data to file
    def appendData(self, filename, data):
        # Adding newline characters if they don't already exist for each line
        # If the characters weren't included then each line would be appended onto the end of the previous
        for index in range(len(data)):
            if data[index][-1] != "\n":
                data[index] += "\n"

        # If the file does not exist then "a+" mode creates the file and adds the data after
        with open(filename, "a+") as file:
            file.writelines(data)

    # Writes to file, will change certain lines if defaults values are changed otherwise overwrites entire file
    def writeData(self, filename, data, startLine=1, endLine=-1):
        # Reading the entire file (only way to do this will be slow if file is big)
        lines = self.readFile(filename=filename)

        # Going through lines that need to be changed
        for dataLineIndex in range(len(data)):
            lines[dataLineIndex + startLine - 1] = data[dataLineIndex]

        # Overwriting file, with new lines changed
        with open(filename, "w+") as file:
            file.writelines(lines)

    # Processes data so each line now becomes a dictionary
    def processData(self, data):
        processedData = []

        for line in data:
            processedData.append({})

            # Splitting up line on the spaces for easier processing
            # Example - "Date:22 Productivity:8" -> ["Date:22", "Productivity:8"]
            lineDataSplit = line.split(" ")
            for value in lineDataSplit:
                # Splitting data on the ":" so "Productivity:5" -> ["Productivity", "5"] If nothing is given after
                # the ":" then "Productivity:" -> ["Productivity", ""] but we don't want the blank so I just check if
                # the non split string has a ":" at the end And manually add the None, None is not a string it is
                # equivalent to null in Java
                valueSplit = value.split(":")
                processedData[-1][valueSplit[0]] = valueSplit[1] if value[-1] != ":" else None

        return processedData