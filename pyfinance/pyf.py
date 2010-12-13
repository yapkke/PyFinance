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
    
