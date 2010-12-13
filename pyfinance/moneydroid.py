"""This module deals with MoneyDroid's SQLite database
"""
import sqlite3

class MoneyDroid:
    """Class to represent MoneyDroid data.
    
    @author ykk
    @date Dec 2010
    """
    def __init__(self, filename, account=None):
        """Initialize
        """
        conn = sqlite3.connect(filename)
        ##Account to use
        self.account = account
        ##Dict of accounts
        self.accounts = {}
        self.__get_accounts(conn)

    def __get_accounts(self, conn):
        """Get dictionary of accounts
        """
        c = conn.cursor()
        c.execute('''SELECT account_name,id FROM ACCOUNTS''')
        for row in c:
            self.accounts[row[0]] = row[1]
        c.close()
