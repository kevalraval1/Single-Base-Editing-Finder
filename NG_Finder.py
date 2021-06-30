# print ("Enter your FASTA Sequence: ")
# FASTA = input()
# NG_Finder(FASTA)

from tkinter import *
import sys, os

window = Tk()
window.title("Prime Editing: NG Analysis program")

def reverser(FASTA, mutation):
    global newFASTA
    global newMutation
    complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A', 'a': 't', 'c': 'g', 'g': 'c', 't': 'a', '(': ')', ')': '('} 
    newFASTA = ''.join(complement.get(base, base) for base in reversed(FASTA))
    newMutation = ''.join(complement.get(base, base) for base in reversed(mutation))

def parsedFASTA (FASTA):
    global newString
    global position
    newString = ""
    counter = 0
    position = 0
    for char in FASTA:
        if (char != "(") and (char != ")"):
            newString = newString + char
            counter += 1
        elif (char == ")"):
            continue
        else:
            position = counter + 1
            continue
    if len(newString) < 11:
        return print("ERROR: FASTA given is too small, please enter a FASTA that is 11 or more base pairs.")
    if ((position - 7) < 0) or (position + 4 > len(newString)):
        return print("ERROR: Selected mutation site is out of bounds for editing in this FASTA file. Add more base pairs to the ends for editing.")
    if ((position - 27) < 0) or ((position + 11) > len(newString)):
        return print("ERROR: Some Spacer or Extension sequences may not be made, PAM may be out of bounds of the FASTA file.")
    return print("Successfully parsed FASTA")

def NG_Finder (newString, position):
    global listByPos
    listByPos = []
    optimal_string = ""
    answer = False
    for x in range (position-7, position+4):
        optimal_string = optimal_string + newString[x]
    counter = position - 7 
    print ("Mutation at 7th position in string: " + optimal_string)
    for x in optimal_string:
        if x == "G":
            if (counter != position-7):
                tuple = (counter, newString[counter-1]+"G")
                listByPos.append(tuple)
                answer = True
        counter += 1
    if answer == False:
        return print("No available NG PAM sites for given mutation.")
    if answer == True:
        return print(listByPos)

def spacer(newString, listByPos):
    global listOfSpacers
    listOfSpacers = []
    for tup in listByPos:
        spacerSequence = ""
        if (newString[tup[0]-21]) != "G":
            spacerSequence = spacerSequence + "G"
        for bases in range ((tup[0]-21), (tup[0]-1)):
            spacerSequence = spacerSequence + newString[bases]
        listOfSpacers.append(spacerSequence)
    return print(listOfSpacers)

def extension(newString, listByPos, mutation):
    global listOfExtensions
    listOfExtensions = []
    for tup in listByPos:
        extensionSequence = ""
        for bases in range ((tup[0]-17), (tup[0]+9)):
            if bases == position-1:
                extensionSequence = extensionSequence + mutation.lower()
                continue
            extensionSequence = extensionSequence + newString[bases]
        complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A', 'a': 't', 'c': 'g', 'g': 'c', 't': 'a'} 
        reverse_complement = ''.join(complement.get(base, base) for base in reversed(extensionSequence))
        listOfExtensions.append(reverse_complement)
    return (print(listOfExtensions))

def analysisPrinter(listByPos, listOfSpacers, listOfExtensions, file1):
    addString = ""
    for count in range (0, len(listByPos)):
        addString = addString + ("-------------------\n")
        if (listByPos[count][0] + 1 == position):
            addString = addString + ("** PAM DESTROYED **\n")
            addString = addString + ("PAM " + str(count + 1) + ": " + str(listByPos[count][1]) + "\n")
            addString = addString + ("Position: " + str(listByPos[count][0]) + "\n")
            addString = addString + ("Spacer sequence Top: " + "cacc" + listOfSpacers[count] + "gtttt" + "\n")
            addString = addString + ("Extension sequence Top: " + "gtgc" + listOfExtensions[count] + "\n")
            complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A', 'a': 't', 'c': 'g', 'g': 'c', 't': 'a'} 
            reverse_complement_spacer = ''.join(complement.get(base, base) for base in reversed(listOfSpacers[count]))
            reverse_complement_extension = ''.join(complement.get(base, base) for base in reversed(listOfExtensions[count]))
            addString = addString + ("Spacer sequence Bottom: " + "ctctaaaac" + reverse_complement_spacer + "\n")
            addString = addString + ("Extension sequence Bottom: " + "aaaa" + reverse_complement_extension + "\n")
            continue
        addString = addString + ("PAM " + str(count + 1) + ": " + str(listByPos[count][1]) + "\n")
        addString = addString + ("Position: " + str(listByPos[count][0]) + "\n")
        addString = addString + ("Spacer sequence Top: " + "cacc" + listOfSpacers[count] + "gtttt" + "\n")
        addString = addString + ("Extension sequence Top: " + "gtgc" + listOfExtensions[count] + "\n")
        complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A', 'a': 't', 'c': 'g', 'g': 'c', 't': 'a'} 
        reverse_complement_spacer = ''.join(complement.get(base, base) for base in reversed(listOfSpacers[count]))
        reverse_complement_extension = ''.join(complement.get(base, base) for base in reversed(listOfExtensions[count]))
        addString = addString + ("Spacer sequence Bottom: " + "ctctaaaac" + reverse_complement_spacer + "\n")
        addString = addString + ("Extension sequence Bottom: " + "aaaa" + reverse_complement_extension + "\n")
    addString = addString + ("----------------------------------")
    file1.write(addString)

def main():
    FASTA = FASTAEntry.get()
    mutation = mutationEntry.get()
    filename = filenameEntry.get()
    #For testing code:
    completename = os.path.join(os.path.dirname("NG_Finder.py"), (filename + ".txt"))
    #For testing executable:
    # completename = os.path.join(os.path.dirname(sys.executable), (filename + ".txt"))
    file1 = open(completename, "w")
    parsedFASTA(FASTA)
    NG_Finder(newString, position)
    spacer(newString, listByPos)
    extension(newString, listByPos, mutation)
    print ("Successfully found spacer and extension sequences for all PAMs.")
    file1.write("\n*PLUS STRAND ANALYSIS*\n\n")
    analysisPrinter(listByPos, listOfSpacers, listOfExtensions, file1)
    file1.write("\n\n*MINUS STRAND ANALYSIS*\n\n")
    reverser(FASTA, mutation)
    parsedFASTA(newFASTA)
    NG_Finder(newString, position)
    spacer(newString, listByPos)
    extension(newString, listByPos, newMutation)
    print ("Successfully found spacer and extension sequences for all PAMs.")
    analysisPrinter(listByPos, listOfSpacers, listOfExtensions, file1)
    print ("Exiting...")
    file1.close()
    sys.exit()

# FASTA = "ACCATGCTCTATCATCATCTCATGCTCTATCATCATCTCATGCTCTATCATCATCTCATGCTGTATCATCATCTTAGCGACGT(G)TAGCATGCTCTATCATCATCTCATGCTCTATCATCATCTGCATACGCATGCTCTATCATCATCTGTTAAATATAT"

# mutation = "T"
# main(FASTA, mutation)

canvas = Canvas(window, height = 200, width = 600)
canvas.pack()

frame = Frame(window,relief = 'groove')
frame.place(relx = 0.1, rely = 0.1, relwidth = 0.8, relheight = 0.8)

welcome = Label(frame, text = "Welcome to the Prime Editing Program for NG PAM analysis", fg = "Black")
welcome.pack(side = "top")


FASTAEntry = Entry(frame, width = 50)
FASTAEntry.pack(side = "top")
FASTAEntry.insert(0, "Please enter the DNA sequence")

mutationEntry = Entry(frame, width = 50)
mutationEntry.pack(side = "top")
mutationEntry.insert(0, "Please enter the desired mutation")

filenameEntry = Entry(frame, width = 50)
filenameEntry.pack(side = "top")
filenameEntry.insert(0, "Please enter the desired .txt filename")

enterButton = Button(window, text = "Start", padx = 10, pady = 5, fg = "Black", bg = "gray", command = main)
enterButton.pack()

window.mainloop()





