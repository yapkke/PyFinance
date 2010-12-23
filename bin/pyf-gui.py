#!/usr/bin/env python

import sys
import getopt
import pyfinance.gui as gui

def usage():
    """Display usage
    """
    print "Usage "+sys.argv[0]+"\n"+\
          "\n"+\
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

app = gui.GUI(args)
app.run()

