#!/usr/bin/env python

import sys
import getopt
import simplejson
import pyfinance.files as pyfiles

def usage():
    """Display usage
    """
    print "Usage "+sys.argv[0]+" <account to check against> <account to check>\n"+\
          "\n"+\
          "Accounts should be in the following format\n"+\
          "\t<File Format>:<Type>:<Filename>"+\
          "Options:\n"+\
          "-h/--help\n\tPrint this usage guide\n"+\
          ""

#Parse options and arguments
try:
    opts, args = getopt.getopt(sys.argv[1:], "hv",
                               ["help","verbose"])
except getopt.GetoptError:
    usage()
    sys.exit(2)

#Get options
verbose=False
for opt,arg in opts:
    if (opt in ("-h","--help")):
        usage()
        sys.exit(0)
    if (opt in ("-v","--verbose")):
        verbose = True
    else:
        print "Unknown option :"+str(opt)
        sys.exit(2)

#Check there is only one input file
if not (len(args) == 2):
    usage()
    sys.exit(2)

parser = pyfiles.dataParser()
checkagainst = parser.getData(args[0])
tocheck = parser.getData(args[1])

(ok, problems, leftover) = tocheck.crosscheck(checkagainst)
print str(len(ok))+" out of "+str(len(tocheck.transactions))+" entries has a single match"
if (verbose):
    for o in ok:
        print "\tmatch between\t"+str(o[0])+"\n\t\t\t"+str(o[1])+"\n"
    print

print "Left in Check-Against Account"
for t in leftover:
    print "\t"+str(t)
print
print
for (p, pdesc) in problems.items():
    print p
    print "\t"+pdesc[0]
    if (len(pdesc[1]) > 0):
        print "\tPossible matches"
        for cm in pdesc[1]:
            print "\t\t"+str(cm)
    print

