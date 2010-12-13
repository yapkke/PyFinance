"""Base classes
"""

class transaction:
    """Base transaction class
    
    @author ykk
    @date Dec 2010
    """
    def __init__(self, 
                 date=None,amount=None, description=None,type=None):
        """Initialize
        """
        ##Date of transaction
        self.date = date
        ##Amount (can be positive or negative)
        self.amount = amount
        ##Description (hopefully useful one)
        self.description = description
        ##Type (usu. available for financial institution's record)
        self.type = type

    def __str__(self):
        """Return string representation
        """
        return self.date.strftime("%d/%m/%y")+"\t"+\
               "$"+str(self.amount)+"\t\t"+\
               self.description+\
               "("+str(self.type).strip()+")"

    def __ge__(self, other):
        return (self.date >= other.date)

    def __le__(self, other):
        return (self.date <= other.date)

    def __gt__(self, other):
        return (self.date > other.date)

    def __lt__(self, other):
        return (self.date < other.date)

    def __eq__(self, other):
        return (self.date == other.date)

    def __ne__(self, other):
        return (self.date != other.date)

class account:
    """Base account class
    
    @author ykk
    @date Dec 2010
    """
    def __init__(self):
        """Initialize
        """
        ##List of transaction
        self.transactions = []
    
