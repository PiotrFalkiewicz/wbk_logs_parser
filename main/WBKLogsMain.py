import argparse
import csv
import WBKLogsParser
from os import listdir
import glob
import os


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("planname", help="Name of the plan", type=str)
    parser.add_argument("inputDirectory", help="Address of input log files directory", type=str)
    parser.add_argument("numOfLogs", help="Number of logs to be analyzed", type=int)
    parser.add_argument("dependenciesFile", help="Address of input dependencies csv file", type=str)
    args = parser.parse_args()

    logs = glob.glob(args.inputDirectory + '/' + args.planname + '*')

    logs = sorted(logs, key=os.path.getctime, reverse=True)

    logs = logs[:args.numOfLogs]

    for log in logs:
        log = log.replace("\\", "/")
        print('')
        print('Output for log:')
        print(log)
        WBKLogsParser.main(log, args.dependenciesFile)

if __name__ == "__main__":
    main()