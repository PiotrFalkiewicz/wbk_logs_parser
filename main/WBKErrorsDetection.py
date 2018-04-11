import argparse

def readFile(filename):
    listOfLines = []
    with open(filename, 'r') as file:
        for line in file:
            listOfLines.append(line)
    return listOfLines

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("errorFile", help="Address of input log file", type=str)
    args = parser.parse_args()

    lines = readFile(args.errorFile)

    for it in range(len(lines)-1):
        lineAsList = lines[it].split(' ')
        if len(lineAsList) > 3:
            if lineAsList[2].upper() == 'STANDARD' and lineAsList[3].upper() == 'ERROR':
                time = lineAsList[0][1:]+' '+lineAsList[1][:-1]
                source = lineAsList[5]+' '+lineAsList[6]
                body = []
                it2 = 1
                while len(lines[it+it2]) > 1 and it + it2 < len(lines) - 1:
                    body.append(lines[it+it2])
                    it2+=1


                print("ERROR DETECTED ON {} IN {}\nERROR MESSAGE:\n{}\n".format(time, source, "\n".join(body) ))










if __name__ == "__main__":
    main()
