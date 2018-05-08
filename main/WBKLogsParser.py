import argparse
import csv

def utilDistinct(listArg):
    return(list(set(listArg)))

def readFile(filename):
    listOfLines = []
    with open(filename, 'r') as file:
        for line in file:
            listOfLines.append(line)
    return listOfLines

def readCSVFile(filename):
    rows = []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            rows.append(row)
    return rows[1:]

def parseTaskName(taskname):
    return taskname[:5].upper()+'_'+taskname[-1]

def chooseCandidates(lines):
    result = []
    keyword = 'perform'
    for line in lines:
        if keyword in line:
            result.append(line)
    return result

def chooseCandidatesWithTime(lines):
    result = []
    keyword1 = 'STARTED'
    keyword2 = 'COMPLETED'
    for line in lines:
        if keyword1 in line or keyword2 in line:
            result.append(line)
    return result

def getTypeNameTime(line):
    items = line.split(' ')

    type = -1
    if items[3] == 'STARTED':
        type = 0
    elif items[3] == 'COMPLETED':
        type = 1

    name = parseTaskName(items[-1].split('_')[0])

    date = items[-1].split('_')[-2].split('-')
    time = str(int(date[3])*3600+int(date[4])*60+int(date[5]))

    return type, name, time

def parseLinesToNames(candidates):
    result = []
    for line in candidates:
        items = line.split('/')
        result.append(items[1])
    return result

def normalTasks(candidates, tasks):
    result = []
    for task in tasks:
        row = []
        start = ''
        end = ''
        for line in candidates:
            if getTypeNameTime(line)[1] == parseTaskName(task):
                if getTypeNameTime(line)[0] == 0:
                    start = int(getTypeNameTime(line)[2])
                elif getTypeNameTime(line)[0] == 1:
                    end = int(getTypeNameTime(line)[2])
        if end != '' and start != '':
            row.append(parseTaskName(task))
            row.append(start)
            row.append(end)
            result.append(row)

    return result

def reformatDependencies(collection):
    newTable = []
    for line in collection:
        if len(newTable) > 0:
            isOnList = False
            newLine = []
            for currentLine in newTable:

                if currentLine[0] == line[1]:
                    if line[1] != '' and line[0] not in currentLine:
                        currentLine.append(line[0])

                elif currentLine[0] == line[2]:
                    if line[2] != '' and line[0] not in currentLine:
                        currentLine.append(line[0])

                elif currentLine[0] == line[1] or currentLine[0] == line[2]:
                    isOnList = True

            if not isOnList:
                if line[2] != '' and len(line[1]) == 0:
                    newLine.append(line[2])
                    newLine.append(line[0])
                    newTable.append(newLine)

                elif line[1] != '' and len(line[2]) == 0:
                    newLine.append(line[1])
                    newLine.append(line[0])
                    newTable.append(newLine)

                elif line[1] == line[2] and line[1] != '':
                    newLine.append(line[1])
                    newLine.append(line[0])
                    newTable.append(newLine)

        else:
            newLine = []
            if line[2] != '' and line[1] == '':
                newLine.append(line[2])
                newLine.append(line[0])
                newTable.append(newLine)

            elif line[1] != '' and line[2] == '':
                newLine.append(line[1])
                newLine.append(line[0])
                newTable.append(newLine)

            elif line[1] == line[2] and line[1] != '':
                newLine.append(line[1])
                newLine.append(line[0])
                newTable.append(newLine)

    return newTable

def calculateTimes(collection, dependencies):
    result = []

    for task in collection:
        newLine = []
        newLine.append(task[0])
        newLine.append(str(int(task[2])-int(task[1])))
        isOnList = False
        anchestorTime = ''
        for dep in dependencies:
            if dep[0] == task[0]:
                isOnList = True
                for agTask in collection:
                    if agTask[0] == dep[1]:
                        anchestorTime = agTask[2]

        if not isOnList:
            newLine.append('')
        else:
            newLine.append(str(int(task[1])-int(anchestorTime)))
        result.append(newLine)

    return result



def main(inputFile, dependenciesFile):
    lines = readFile(inputFile)

    csv = readCSVFile(dependenciesFile)
    #
    # for line in csv:
    #     print(line)

    candidates = chooseCandidatesWithTime(lines)

    tasks = utilDistinct(parseLinesToNames(chooseCandidates(lines)))


    print()
    newList = normalTasks(candidates, tasks)

    newDependencies = reformatDependencies(csv)

    for line in newDependencies:
        print(line)

    print("")


    for item in newList:
        print(item)


    finalCollection = calculateTimes(newList, newDependencies)

    print("")
    for line in finalCollection:
        print(line)






if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("inputFile", help="Address of input log file", type=str)
    parser.add_argument("dependenciesFile", help="Address of input log file", type=str)
    args = parser.parse_args()
    main(args.inputFile, args.dependenciesFile)
