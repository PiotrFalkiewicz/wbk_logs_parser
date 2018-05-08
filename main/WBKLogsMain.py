import argparse
import traceback
from datetime import datetime
import glob
import re

#script with parser
import WBKLogsParser

#Select last countOfLogs logs to be analayzed and starts the process
#
#Arguments:
#planname - Name of the plan
#inputDirectory - Directory where log files are storaged
#countOfLogs - Count of logs to be analyzed
#dependenciesFile - Address of input dependencies csv file
def main(planname, inputDirectory, countOfLogs, dependenciesFile):
    logs = glob.glob(inputDirectory + '/' + planname + '*.log')

    logsdates = []
    for i in range(len(logs)):
        #Extract datetime part of log file name
        match = re.search(r'\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2}', logs[i])
        #makes tuple made of log file name and date time of it's perform
        logsdates.append([logs[i],datetime.strptime(match.group(), '%Y-%m-%d-%H-%M-%S')])

    #sorts logs due to datetime (descending)
    logsdates = sorted(logsdates, key=lambda logdate: logdate[1], reverse=True)

    #select countOfLogs last logs
    logsdates = logsdates[:countOfLogs]

    #starts function to parse logs into csv files
    for log in logsdates:
        #todo - only Windows should need it - can be removed at the end
        log[0] = log[0].replace("\\", "/")
        print('')
        print('Output for log:')
        print(log[0])
        try:
            WBKLogsParser.main(log[0], dependenciesFile)
        except:
            traceback.print_exc()

#Extracts arguments from args and starts main program
#args:
#planname - Name of the plan
#inputDirectory - Directory where log files are storaged
#countOfLogs - Count of logs to be analyzed
#dependenciesFile - Address of input dependencies csv file
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("planname", help="Name of the plan", type=str)
    parser.add_argument("inputDirectory", help="Directory where log files are storaged", type=str)
    parser.add_argument("countOfLogs", help="Count of logs to be analyzed", type=int)
    parser.add_argument("dependenciesFile", help="Address of input dependencies csv file", type=str)
    args = parser.parse_args()
    main(args.planname, args.inputDirectory, args.countOfLogs, args.dependenciesFile)