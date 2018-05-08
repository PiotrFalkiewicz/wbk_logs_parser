import sys, getopt
import plan_processing.main as plan
import log_processing.main as logs

def main(argv):
    planFile = ''
    outputDir = ''
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["plan=","rdir="])
    except getopt.GetoptError:
        printHelp()
        sys.exit(2)
    if len(opts) < 2:
        printHelp()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            printHelp()
            sys.exit()
        elif opt in ("-i", "--plan"):
            planFile = arg
        elif opt in ("-o", "--rdir"):
            outputDir = arg
			
    relationsFile, resourcesFile = plan.main(planFile, outputDir)
    logs.main(relationsFile, resourcesFile, outputDir)
	
def printHelp():
    print('Try with:')
    print('bizon.py -i <inputfile> -o <outputdirectory>')
    print('or')
    print('bizon.py --plan <inputfile> --rdir <outputdirectory>')

if __name__ == "__main__":
   main(sys.argv[1:])