import argparse
import csv
import arrow

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
        reader = csv.reader(file, delimiter=';')
        for row in reader:
            rows.append(row)
    return rows[1:]

def parseTaskName(taskname):
    return taskname[:5].upper()+'_'+taskname[-1]

def chooseCandidates(lines):
    result = []
    keyword = 'perform'
    for line in range(len(lines)-1):
        if keyword in lines[line]:
            subresult = []
            subresult.append(lines[line])
            subresult.append(lines[line-1])
            result.append(subresult)
            # result.append(lines[line])
    # print(result)
    return result

def chooseCandidatesWithTime(lines):
    result = []
    keyword1 = 'STARTED'
    keyword2 = 'COMPLETED'
    for line in range(len(lines) - 1):
        if keyword1 in lines[line] or keyword2 in lines[line]:
            subresult = []
            subresult.append(lines[line])
            subresult.append(lines[line - 1])
            result.append(subresult)
            # result.append(lines[line])
    # print(result)
    return result

def getTypeNameTime(lines):
    items1 = lines[0].split(' ')
    date = lines[1].split('[')[1].split(']')[0]

    type = -1
    if items1[3] == 'STARTED':
        type = 0
    elif items1[3] == 'COMPLETED':
        type = 1

    name = parseTaskName(items1[-1].split('_')[0])

    time = arrow.get(date, 'YYYY-MM-DD HH:mm:ss').format('YYYY-MM-DD HH:mm:ss')
    return type, name, time

def parseLinesToNames(candidates):
    result = []
    mainLine = ''
    subcandidates = []
    for group in candidates:
        for line in group:
            if 'COMPLETED' not in line and 'STARTED' not in line:
                # print(line)
                subcandidates.append(line)
    for line in subcandidates:
        items = line.split('/')
        print(items[1])
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

def reformatRelations(collection):
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

def calculateTimes(collection, relations):
    result = []

    for task in collection:
        newLine = []
        newLine.append(task[0])
        isOnList = False
        processingTime = arrow.get(task[2], 'YYYY-MM-DD HH:mm:ss').timestamp-arrow.get(task[1], 'YYYY-MM-DD HH:mm:ss').timestamp
        pattern = ''
        for x in str(processingTime):
            pattern+='s'
        newLine.append(arrow.get(str(processingTime), pattern).format('HH:mm:ss'))
        anchestorTime = ''
        for dep in relations:
            if dep[0] == task[0]:
                isOnList = True
                for agTask in collection:
                    if agTask[0] == dep[1]:
                        anchestorTime = agTask[2]

        if not isOnList:
            newLine.append('')
        else:
            newLine.append((task[1].timestamp-anchestorTime.timestamp).format('YYYY-MM-DD HH:mm:ss'))
        result.append(newLine)

    return result



def main(inputFile, relationsFile, outputDirectory):
    lines = readFile(inputFile)

    csv = readCSVFile(relationsFile)
    #
    # for line in csv:
    #     print(line)

    candidates = chooseCandidatesWithTime(lines)

    tasks = utilDistinct(parseLinesToNames(chooseCandidates(lines)))


    print()
    newList = normalTasks(candidates, tasks)

    newRelations = reformatRelations(csv)

    for line in newRelations:
        print(line)

    print("")


    for item in newList:
        print(item)


    finalCollection = calculateTimes(newList, newRelations)

    print("")
    for line in finalCollection:
        print(line)

    return ["1", "2", "3", "4", "5", "6"]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("inputFile", help="Address of input log file", type=str)
    parser.add_argument("relationsFile", help="Address of input log file", type=str)
    parser.add_argument("outputDirectory", help="Address where to storage output csv file", type=str)
    args = parser.parse_args()
    main(args.inputFile, args.relationsFile, args.outputDirectory)
