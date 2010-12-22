"""Utilites to handle different data files.
"""
import pyfinance.moneydroid as moneydroid
import pyfinance.csv as csv
import pyfinance.quicken as quicken

class dataParser:
    """Data parser for understand what file to load, e.g.,

    SQLite:MoneyDroid:<filename> for MoneyDroid's SQLite Database
    SQLite:MoneyDroid:<filename>:<account name> for MoneyDroid's Account
    CSV:Chase:<filename> for Chase's CSV file
    CSV:CitiCard:<filename> for CitiCard's CSV file
    QFX:CitiCard:<filename> for CitiCard's Quicken file

    @author ykk
    @date Dec 2010
    """
    def __init__(self):
        """Initialize (does nothing)
        """
        pass

    def parse(self,string):
        """Parse string for file format, type and filename
        
        return list of [file format, type, filename]
        """
        return string.split(":")
    
    def getData(self,string):
        """Return data for specified file (in string or tuple)
        """
        #Ensure tuple
        tuple = None
        if isinstance(string,list):
            tuple = string
        elif isinstance(string, str):
            tuple = self.parse(string)
        
        if (tuple[0] == "SQLite"):
            if (tuple[1] == "MoneyDroid"):
                if (len(tuple) > 3):
                    return moneydroid.MoneyDroid(tuple[2], tuple[3])
                else:
                    return moneydroid.MoneyDroid(tuple[2])
            else:
                print "Unknown SQLite type :"+tuple[1]
        elif (tuple[0] == "CSV"):
            if (tuple[1] == "CitiCard"):
                return csv.CitiCard(tuple[2])
            elif (tuple[1] == "Chase"):
                return csv.Chase(tuple[2])
            else:
                print "Unknown CSV type :"+tuple[1]
        elif (tuple[0] == "QFX"):
            if (tuple[1] == "CitiCard"):
                return quicken.CitiCardQFX(tuple[2])
            else:
                print "Unknown QFX type :"+tuple[1]
        else:
            print "Unknown file format :"+tuple[0]
