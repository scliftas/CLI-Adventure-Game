#!/usr/bin/env python3

import random
import time

#Folders
def FileSystem():
    global CurrentDirectory
    CurrentDirectory = ("~")
    global contents
    contents = ["bin","home"]

def Bin():
    global PreviousDirectory
    PreviousDirectory = ("FileSystem")
    global CurrentDirectory
    CurrentDirectory = ("/bin")
    global contents
    contents = [""]

def Logs():
    global PreviousDirectory
    PreviousDirectory = ("FileSystem")
    global CurrentDirectory
    CurrentDirectory = ("/logs")
    global contents
    contents = [LogFile.name]

def Home():
    global PreviousDirectory
    PreviousDirectory = ("FileSystem")
    global CurrentDirectory
    CurrentDirectory = ("/home")
    global contents
    contents = ["documents", "downloads", "music", "pictures", "videos"]

def Documents():
    global PreviousDirectory
    PreviousDirectory = ("/home")
    global CurrentDirectory
    CurrentDirectory = ("/home/documents")
    global contents
    contents = [DocumentsOne.name]

def Downloads():
    global PreviousDirectory
    PreviousDirectory = ("/home")
    global CurrentDirectory
    CurrentDirectory = ("/home/downloads")
    global contents
    contents = [""]

def Music():
    global PreviousDirectory
    PreviousDirectory = ("/home")
    global CurrentDirectory
    CurrentDirectory = ("/home/music")
    global contents
    contents = [""]

def Pictures():
    global PreviousDirectory
    PreviousDirectory = ("/home")
    global CurrentDirectory
    CurrentDirectory = ("/home/pictures")
    global contents
    contents = [""]

def Videos():
    global PreviousDirectory
    PreviousDirectory = ("/home")
    global CurrentDirectory
    CurrentDirectory = ("/home/videos")
    global contents
    contents = [""]

#Files
class File:

    #Virus count can only go up to 1, meaning there can only be one virus source file
    VirusCount = 0
    VirusPath = ""

    #File object generator
    def __init__(self, name, path, content, compressed, potentVirus):
        self.name = str(name)
        self.path = str(path)
        self.content = str(content)
        self.compressed = bool(compressed)
        self.potentVirus = bool(potentVirus)

        #Randomly generate whether or not the file is the virus source file
        if self.potentVirus == True:
            self.generateVirus = random.choice([True, False])
            if self.generateVirus == True:
                if File.VirusCount == 0:
                    self.virus = random.choice([True, False])
                    if self.virus == True:
                        File.VirusCount = 1
                        File.VirusPath = (self.path+self.name)

    def displayProps(self):
        print("Name: ", self.name)
        print("File path: ", self.path)
        print("Compressed: ", self.compressed)
        print("Generate Virus: ", self.generateVirus)
        if self.generateVirus == True:
            print("Virus: ", self.virus)

    def displaycontent(self):
        print(self.content)


LogFile = File("virus_report.txt", "/logs/", "System found an error: exception 302.\nWe're not sure what this is, but it could mean your system is infected. \n \nPerhaps try finding the source file that generated the error?", False, False)
DocumentsOne = File("hello_world.txt", "/home/documents/", "Hello world", False, True)

#Bash commands

#View contets of folder or properties of file command
def gzip(Input):
    Dir = Input.split("gzip ", 1)[1]
    compDir = folder_dict[Dir]
    if compDir.compressed == True:
        compDir.compressed = False
        print("Uncompressed")
    elif compDir.compressed == False:
        print("This folder is not compressed!")
    else:
        print("bash: gzip:"+Dir+": No such compressed directory")

def ls(Input):
    Dir = Input.split("ls ", 1)[1]
    if "-l" not in Input:
        print('\n'.join('{}: {}'.format(*k) for k in enumerate(contents)))
    elif "-l" in Input:
        Dir = Input.split("-l ", 1)[1]
        FileProperties = file_dict[Dir].displayProps
        FileProperties()
    else:
        print("ls: cannot access '"+Dir+"': No such file or directory")

#Navigate to directory command
def cd(Input):
    CDDir = Input.split("cd ", 1)[1]
    if CDDir in folder_dict:
        folder_dict[CDDir]()
    elif Input == "cd":
        folder_dict[PreviousDirectory]()
    else:
        print("bash: cd:"+CDDir+": No such file or directory")

#View contents of file command
def cat(Input):
    CatFile = Input.split("cat ", 1)[1]
    if CatFile in file_dict:
        FileContent = file_dict[CatFile].displaycontent
        print("")
        FileContent()
        print("")
    else:
        print("cat: "+CatFile+": No such file or directory")

#Delete file command
def rm(Input):
    rmDir = Input.split("rm ", 1)[1]
    if rmDir in folder_dict:
        print("You cannot delete entire folders!")
    elif rmDir in file_dict:
        VirusCheck = file_dict[rmDir].virus
        del file_dict[rmDir]
        print(rmDir + " has been deleted.")
        if VirusCheck == True:
            win()

#Original commands
def help(Input):
    print("Commands:"+"\n - ls [directory] to display folder contents \n - ls -l [directory] to view file properties \n - cd [directory] to move to a different folder "+
                                          "\n - cat [directory] to view file contents \n - rm [directory] to delete a file \n - exit to exit the game" +
                                          "\n - gzip [directory] to uncompress a folder")

def win():

    #Calculating time taken and score
    end = time.time()
    timeTaken = (end - start)
    minutes, seconds = divmod(timeTaken, 60)
    hours, minutes = divmod(minutes, 60)
    MaxScore = 100000
    Score = (int(MaxScore - timeTaken))

    print("\nCongratulations, you have found the source file of the virus!")
    print("Time: %d:%02d:%02d" % (hours, minutes, seconds))
    print("Your total score is:", Score)

    #Encrypting score and writing score to scoreboard.txt
    Score = str(Score)
    scoreWrite = (str(Username+":"+Score))
    scoreWrite = [ord(i) for i in scoreWrite]
    scoreWrite = [chr(i + 5) for i in scoreWrite]
    scoreWrite = ''.join(scoreWrite)
    scoreboard = open("scoreboard.txt", "a")
    scoreboard.write(scoreWrite+"\n")
    scoreboard.close()

    #Decrypting scoreboard.txt and storing lines to array
    scoreboard = open("scoreboard.txt", "r")
    print("SCOREBOARD:")
    fileContents = []
    for line in scoreboard:
        line = [ord(i)for i in line]
        line = [chr(i-5) for i in line]
        line = ''.join(line)
        line = line.split("\x05", 1)[0]
        fileContents.append(line)
    scoreboard.close()

    #Printing scoreboard.txt array as a sorted list
    fileContSort = sorted(fileContents, reverse =True)
    fileContSort = '\n'.join(fileContSort)
    print(fileContSort)

#Exit function to close game
def gameExit(Input):
    exit()

#Main Program
start = time.time()

#Custom dictionaries linking phrases to functions
command_dict = {"ls":ls, "help":help, "cd":cd, "cat":cat, "rm":rm, "exit":gameExit}
folder_dict = {"FileSystem": FileSystem, "/home":Home, "/bin":Bin, "/home/documents":Documents, "/home/downloads":Downloads, "/home/music":Music, "/home/pictures":Pictures, "/home/videos":Videos, "/log":Logs}
file_dict = {"/home/documents/hello_world.txt":DocumentsOne, "/logs/virus_report.txt":LogFile}

print(File.VirusPath)

Username = (input(str("Please enter your username: ")))
CurrentDirectory = ("")
contents = [""]

print("WARNING: Potential virus detected! Report saved to log file. Please see /logs/virus_report.txt")

FileSystem()

while True:

    #Display command line input area
    UserInput = (input(str(Username+"@System:"+CurrentDirectory+"$ ")))
    Input = UserInput.lower()

    #Shorten the input to the first word, making it a command, then referencing dictionaries
    Command = Input.split(" ", 1)[0]
    if Command in command_dict:
        command_dict[Command](Input)

    elif Command not in command_dict:
        print("Invalid command!")
