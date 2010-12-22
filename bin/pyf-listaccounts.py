#!/usr/bin/env python

import sys
import getopt
import simplejson
import pyfinance.files as pyfiles

def usage():
    """Display usage
    """
    print "Usage "+sys.argv[0]+" <File Format>:<Type>:<Filename>\n"+\
          "\ne.g. "+sys.argv[0]+"SQLite:MoneyDroid:testing.db\n"+\
          "\n"+\
          "-h/--help\n\tPrint this usage guide\n"+\
          ""

#Parse options and arguments
try:
    opts, args = getopt.getopt(sys.argv[1:], "h",
                               ["help"])
except getopt.GetoptError:
    usage()
    sys.exit(2)

#Get options
for opt,arg in opts:
    if (opt in ("-h","--help")):
        usage()
        sys.exit(0)
    else:
        print "Unknown option :"+str(opt)
        sys.exit(2)

#Check there is only one input file
if not (len(args) == 1):
    usage()
    sys.exit(2)

parser = pyfiles.dataParser()
print simplejson.dumps(parser.getData(args[0]).accounts,
                       sort_keys=True, indent=4)
