"""Base classes
"""
import datetime

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

    def __hash__(self):
        return str(self).__hash__()

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

    def match(self, other, tolerance=3):
        """Check if transaction is matching
        """
        if (tolerance == ()):
            return (abs(self.amount) == abs(other.amount))
        else:
            return (abs(self.amount) == abs(other.amount)) and \
                   (abs(self.date-other.date) <= datetime.timedelta(days=tolerance))

class account:
    """Base account class
    
    @author ykk
    @date Dec 2010
    """
    def __init__(self, transactions=None):
        """Initialize
        """
        ##List of transaction
        if (transactions == None):
            self.transactions = []
        else:
            self.transactions = transactions[:]
        ##Sorted?
        self.sorted = False

    def get_matching(self, transaction, tolerance=3, maximum=3):
        """Find matching transaction,
        with default tolerance of 3 days difference in date
        and maximum list of three
        """
        matching = []
        if (not self.sorted):
            self.transactions = sorted(self.transactions, reverse=True)
            self.sorted = True

        for t in self.transactions:
            if t.match(transaction, tolerance):
                matching.append(t)
            if (len(matching) >= maximum):
                break;
            
        return matching
    
    def checkagainst(self, master):
        """Check all transactions in this account with the master account,
        i.e., transactions should exist in master account
        """
        masteracct = account(master.transactions)
        ok = []
        problematic = {}
        for t in self.transactions:
            matches = masteracct.get_matching(t)
            if (len(matches) == 0):
                matches = masteracct.get_matching(t, ())
                problematic[t] = ("No close matches.", matches)
            elif (len(matches) > 1):
                problematic[t] = ("Multiple close matches.", matches)
            else:
                masteracct.transactions.remove(matches[0])
                ok.append(t)
                
        return (ok, problematic)
        
