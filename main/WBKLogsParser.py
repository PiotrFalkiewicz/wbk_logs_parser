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

    date = items[-1].split('_')[1].split('-')
    time = str(int(date[3])*3600+int(date[4])*60+int(date[5]))

    return type, name, time

def parseLinesToNames(candidates):
    result = []
    for line in candidates:
        items = line.split('/')
        result.append(items[1])
    return result



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("inputFile", help="Address of input log file", type=str)
    parser.add_argument("dependenciesFile", help="Address of input log file", type=str)
    args = parser.parse_args()

    lines = readFile(args.inputFile)

    csv = readCSVFile(args.dependenciesFile)

    for line in csv:
        print(line)

    candidates = chooseCandidatesWithTime(lines)

    tasks = utilDistinct(parseLinesToNames(chooseCandidates(lines)))


    for task in tasks:
        print(task)


    for line in candidates:
        print(getTypeNameTime(line))
        print(line)


if __name__ == "__main__":
    main()
