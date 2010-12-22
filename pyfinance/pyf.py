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

    def match(self, other, tolerance=3, amtdev=0.00):
        """Check if transaction is matching
        """
        if (tolerance == ()):
            return (abs(abs(self.amount) - abs(other.amount)) <= amtdev)
        else:
            return (abs(abs(self.amount) - abs(other.amount)) <= amtdev) and \
                   (abs(self.date-other.date) <= datetime.timedelta(days=tolerance))

    def matchall(self, other):
        """Check if transaction matches all field
        """
        return (self.amount == other.amount) and \
            (self.date == other.date) and \
            (self.description == other.description) and \
            (self.type == other.type)    

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

    def sort(self, r=False):
        """Sort transactions
        """
        if (not self.sorted):
            self.transactions = sorted(self.transactions, reverse=r)
            self.sorted = True

    def get_matching(self, transaction, tolerance=3, amtdev=0.00, maximum=3):
        """Find matching transaction,
        with default tolerance of 3 days difference in date
        and maximum list of three
        """
        matching = []
        self.sort()
        for t in self.transactions:
            if t.match(transaction, tolerance, amtdev):
                matching.append(t)
            if (len(matching) >= maximum):
                break;
            
        return matching

    def remove(self, transaction):
        """Remove exact transaction
        """
        index = 0
        for t in self.transactions:
            if t.matchall(transaction):
                self.transactions.pop(index)
                return t
            else:
                index += 1

    def crosscheck(self, master):
        """Check all transactions in this account with another account,
        i.e., transactions should exist in both

        return (list of okay transaction pair,
                problematic transactions with possibilities,
                leftover transactions in master account)
        """
        masteracct = account(master.transactions)
        ok = []
        problemt = []
        problematic = {}
        for t in self.transactions:
            matches = masteracct.get_matching(t)

            if (len(matches) == 1):
                masteracct.remove(matches[0])
                ok.append((t,matches[0]))
            else:
                problemt.append(t)
        
        for t in problemt:
            matches = masteracct.get_matching(t)
            if (len(matches) == 0):
                matches = masteracct.get_matching(t, (), 1.00)
                problematic[t] = ("No close matches.", matches)
            else:
                problematic[t] = ("Multiple close matches.", matches)
                
        return (ok, problematic, masteracct.transactions)
        
class accounts(account):
    """Base accounts class

    @author ykk
    @date Dec 2010
    """
    def __init__(self):
        """Initialize
        """
        account.__init__(self, None)
        ##Dict of accounts
        self.accounts = {}
