import argparse

def utilDistinct(listArg):
    return(list(set(listArg)))

def readFile(filename):
    listOfLines = []
    with open(filename, 'r') as file:
        file.readline()
        for line in file:
            listOfLines.append(line)
    return listOfLines

def chooseCandidates(lines):
    result = []
    keyword = 'perform'
    for line in lines:
        if keyword in line:
            result.append(line)
    return result

def parseLinesToNames(candidates):
    result = []
    keyword = 'perform'
    for line in candidates:
        items = line.split('/')
        result.append(items[1])
    return result

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("inputFile", help="Address of input log file", type=str)
    args = parser.parse_args()

    lines = readFile(args.inputFile)

    candidates = chooseCandidates(lines)

    tasks = utilDistinct(parseLinesToNames(candidates))


    for name in tasks:
        print(name)


if __name__ == "__main__":
    main()
