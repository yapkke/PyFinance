"""Handle CSV files
"""
import pyfinance.pyf as pyf

class csv(pyf.account):
    """Base CSV file
     
    @author ykk
    @date Dec 2010
   """
    def __init__(self, filename):
        """Initialize
        """
        pyf.account.__init__(self)
        
        #Read CSV
        self._content = []
        fileRef = open(filename, "r")
        for line in fileRef:
            self._content.append(line.split(","))
        fileRef.close()

class CitiCard(csv):
    """CSV from CitiCard

    @author ykk
    @date Dec 2010
    """
    def __init__(self, filename):
        """Initialize
        """
        csv.__init__(self,filename)
        
        for x in self._content:
            self.transactions.append(pyf.transaction(x[0],
                                                     float(x[1].replace('$','')),
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
            self.transactions.append(pyf.transaction(x[1],
                                                     float(x[3].replace('$','')),
                                                     x[2],
                                                     x[0]))

