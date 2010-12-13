"""This module deals with MoneyDroid's SQLite database
"""
import sqlite3
import pyfinance.pyf as pyf

class MoneyDroid(pyf.account):
    """Class to represent MoneyDroid data.
    
    @author ykk
    @date Dec 2010
    """
    def __init__(self, filename, account=None):
        """Initialize
        """
        pyf.account.__init__(self)
 
        conn = sqlite3.connect(filename)
        ##Account to use
        self.account = account
        ##Dict of accounts
        self.accounts = {}
        self.__get_accounts(conn)
        ##Dict of categories
        self.categories = {}
        self.__get_categories(conn)
        ##Get transactions
        self.__get_transactions(conn)
        
        conn.close()

    def __get_accounts(self, conn):
        """Get dictionary of accounts
        """
        c = conn.cursor()
        c.execute('''SELECT account_name,id FROM Accounts''')
        for row in c:
            self.accounts[row[0]] = row[1]
        c.close()

    def __get_categories(self, conn):
        """Get dictionary of accounts
        """
        c = conn.cursor()
        c.execute('''SELECT id,category_name FROM Categories''')
        for row in c:
            self.categories[row[0]] = row[1]
        c.close()

    def __get_transactions(self, conn):
        """Get transactions for account
        If no specific account, get all.
        """
        #Get id
        id_select = None
        if (self.account != None):
            if not self.account in self.accounts:
                raise RuntimeError("Unknown account :Account"+\
                                       self.account+" not found")
            else:
                id_select = str(self.accounts[self.account]).strip()

        #Get transactions
        c = conn.cursor()
        if (id_select == None):
            c.execute('''SELECT time,note,amount,category_id FROM Items''')
        else:
            c.execute('SELECT time,note,amount,category_id FROM Items WHERE account_id==? ORDER BY time',
                      (id_select,))
        for row in c:
            self.transactions.append(pyf.transaction(row[0],
                                                     row[2]/100,
                                                     row[1],
                                                     row[3]))        
        
        c.close()

                
                
