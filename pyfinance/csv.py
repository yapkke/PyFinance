"""Handle CSV files
"""
import datetime
import pyfinance.pyf as pyf

class csv(pyf.account):
    """Base CSV file
     
    @author ykk
    @date Dec 2010
   """
    def __init__(self, filename, delimiter=","):
        """Initialize
        """
        pyf.account.__init__(self)
        
        #Read CSV
        self._content = []
        fileRef = open(filename, "r")
        for line in fileRef:
            self._content.append(line.split(delimiter))
        fileRef.close()

class CitiCard(csv):
    """CSV from CitiCard

    @author ykk
    @date Dec 2010
    """
    def __init__(self, filename):
        """Initialize
        """
        csv.__init__(self,filename, ";")
        
        for x in self._content:
            y = x[0].split("/")
            self.transactions.append(pyf.transaction(datetime.date(int(y[2]),
                                                                   int(y[0]),
                                                                   int(y[1])),
                                                     float(x[1].replace('$','').replace(',','')),
                                                     x[2],
                                                     x[3]))

class Chase(csv):
    """CSV from Chase

    @author ykk
    @date Dec 2010
    """
    def __init__(self, filename):
        """Initialize
        """
        csv.__init__(self,filename)
        
        for x in self._content:
            y = x[1].split("/")
            self.transactions.append(pyf.transaction(datetime.date(int(y[2]),
                                                                   int(y[0]),
                                                                   int(y[1])),
                                                     float(x[3].replace('$','')),
                                                     x[2],
                                                     x[0]))

