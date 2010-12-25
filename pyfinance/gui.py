"""This module create the GUI
"""
import sys
import os
import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import pyfinance.files as pyfiles
import pyfinance.pyf as pyf

class SQLiteAcctChooser(QtGui.QWidget):
    """SQLite account chooser
    """
    def __init__(self, parent=None):
        super(SQLiteAcctChooser,self).__init__(parent)
        QtGui.QWidget.__init__(self)
        self.parent = parent

        label = QtGui.QLabel("SQLite Account")
        self.combo = QtGui.QComboBox()

        grid = QtGui.QHBoxLayout()
        grid.addWidget(label)
        grid.addWidget(self.combo)
        self.setLayout(grid)

        self.connect(self.combo, 
                     QtCore.SIGNAL("currentIndexChanged(const QString&)"),
                     self.parent.load)


class SQLiteChooser(QtGui.QWidget):
    """SQLite file chooser
    """
    def __init__(self, acct, parent=None):
        super(SQLiteChooser,self).__init__(parent)
        QtGui.QWidget.__init__(self)
        self.acct = acct

        label = QtGui.QLabel("SQLite DB")
        self.filename = QtGui.QLineEdit()
        button = QtGui.QPushButton("Choose", self) 
        
        grid = QtGui.QHBoxLayout()
        grid.addWidget(label)
        grid.addWidget(self.filename)
        grid.addWidget(button)
        self.setLayout(grid)

        self.connect(button, QtCore.SIGNAL("clicked()"), self.choose)

    def choose(self):
        """Choose SQLite file
        """
        self.filename.setText(\
            QtGui.QFileDialog.getOpenFileName(self, 'Open file',
                                              os.getcwd()))
        self.load()

    def load(self):
        parser = pyfiles.dataParser()
        acct = parser.getData("SQLite:MoneyDroid:"+\
                                  str(self.filename.text()))
        if (isinstance(acct, pyf.accounts)):
            self.acct.combo.clear()
            self.acct.combo.addItem("All")
            for (a,i) in acct.accounts.items():
                self.acct.combo.addItem(a)

class AcctChooser(QtGui.QWidget):
    """Account file chooser
    """
    def __init__(self, parent=None):
        super(AcctChooser,self).__init__(parent)
        QtGui.QWidget.__init__(self)
        self.parent = parent

        self.filename = QtGui.QLineEdit()
        button = QtGui.QPushButton("Choose", self) 
        
        grid = QtGui.QHBoxLayout()
        grid.addWidget(self.filename)
        grid.addWidget(button)
        self.setLayout(grid)

        self.connect(button, QtCore.SIGNAL("clicked()"), self.choose)

    def choose(self):
        """Choose account file
        """
        self.filename.setText(\
            QtGui.QFileDialog.getOpenFileName(self, 'Open file',
                                              os.getcwd()))
        self.parent.load()

class LeftPanel(QtGui.QWidget):
    """Left panel
    """
    def __init__(self, parent=None):
        """Initialize
        """
        super(LeftPanel,self).__init__(parent)
        QtGui.QWidget.__init__(self)

        self.sqliteacct = SQLiteAcctChooser(self)
        self.sqlitechooser = SQLiteChooser(self.sqliteacct, self)
        self.masterlist=QtGui.QListWidget(self)

        grid = QtGui.QVBoxLayout()
        grid.addWidget(self.sqlitechooser)
        grid.addWidget(self.sqliteacct)
        grid.addWidget(self.masterlist)
        self.setLayout(grid)

    def account(self):
        """Get account name
        """
        sText = str(self.sqliteacct.combo.itemText(\
                self.sqliteacct.combo.currentIndex()))
        acctname = "SQLite:MoneyDroid:"+\
            str(self.sqlitechooser.filename.text())
        if (sText != "All"):
            acctname += ":"+sText
        return acctname

    def load(self):
        """Load account
        """
        parser = pyfiles.dataParser()
        acct = parser.getData(self.account())
        self.masterlist.clear()
        for t in acct.transactions:
            self.masterlist.addItem(str(t))
        self.masterlist.sortItems()

class RightPanel(QtGui.QWidget):
    """Right panel
    """
    def __init__(self, parent=None):
        """Initialize
        """
        super(RightPanel,self).__init__(parent)
        QtGui.QWidget.__init__(self)

        self.combo = QtGui.QComboBox()
        self.combo.addItem("---Choose Account Type---")
        self.combo.addItem("QFX:CitiCard")
        self.combo.addItem("CSV:Chase")
        self.combo.addItem("CSV:CitiCard")
        self.acctchooser = AcctChooser(self)
        self.accountlist=QtGui.QListWidget(self)

        grid = QtGui.QVBoxLayout()
        grid.addWidget(self.combo)
        grid.addWidget(self.acctchooser)
        grid.addWidget(self.accountlist)
        self.setLayout(grid)

    def account(self):
        """Get account name
        """
        return str(self.combo.itemText(\
                self.combo.currentIndex()))+":"+\
                str(self.acctchooser.filename.text())
    
    def load(self):
        """Load account
        """
        parser = pyfiles.dataParser()
        acct = parser.getData(self.account())
        self.accountlist.clear()
        for t in acct.transactions:
            self.accountlist.addItem(str(t))
        self.accountlist.sortItems()

class MainPanel(QtGui.QWidget):
    """Main panel
    """
    def __init__(self, parent=None):
        """Initialize
        """
        super(MainPanel,self).__init__(parent)
        QtGui.QWidget.__init__(self)

        self.left = LeftPanel(self)
        self.right = RightPanel(self)

        grid = QtGui.QHBoxLayout()
        grid.addWidget(self.left)
        grid.addWidget(self.right)
        self.setLayout(grid)

    def get_left_account(self):
        """Get account on left
        """
        return self.left.account()

    def get_right_account(self):
        """Get account on right
        """
        return self.right.account()

class BottomPanel(QtGui.QWidget):
    """Main panel
    """
    def __init__(self, parent=None):
        """Initialize
        """
        super(BottomPanel,self).__init__(parent)
        QtGui.QWidget.__init__(self)
        self.parent = parent

        quitbutton = QtGui.QPushButton("Quit", self) 
        checkbutton = QtGui.QPushButton("Cross-check", self) 
        matchbutton = QtGui.QPushButton("Match and Check-off", self) 
        
        grid = QtGui.QHBoxLayout()
        grid.addWidget(checkbutton)
        grid.addWidget(matchbutton)
        grid.addWidget(quitbutton)
        self.setLayout(grid)

        self.connect(quitbutton, QtCore.SIGNAL("clicked()"), QtGui.qApp,
                     QtCore.SLOT('quit()'))
        self.connect(checkbutton, QtCore.SIGNAL("clicked()"), 
                     self.parent.crosscheck)
        self.connect(matchbutton, QtCore.SIGNAL("clicked()"), 
                     self.parent.match)


class MainWindow(QtGui.QDialog):
    """Main window of GUI application
    """
    def __init__(self, parent=None):
        """Initialize
        """
        super(MainWindow,self).__init__(parent)
        QtGui.QMainWindow.__init__(self)
        self.resize(1000,600)
        self.setWindowTitle("PyFinance")

        self.mainpanel = MainPanel(self)
        bottompanel = BottomPanel(self)
        
        grid = QtGui.QVBoxLayout()
        grid.addWidget(self.mainpanel)
        grid.addWidget(bottompanel)
        self.setLayout(grid)

    def crosscheck(self):
        """Cross check accounts
        """
        parser = pyfiles.dataParser()
        checkagainst = parser.getData(self.mainpanel.get_left_account())
        tocheck = parser.getData(self.mainpanel.get_right_account())
        
        (ok, problems, leftover) = tocheck.crosscheck(checkagainst)

        self.mainpanel.left.masterlist.clear()
        for t in leftover:
            self.mainpanel.left.masterlist.addItem(str(t))
        self.mainpanel.left.masterlist.sortItems()

        self.mainpanel.right.accountlist.clear()
        for (p, pdesc) in problems.items():
            self.mainpanel.right.accountlist.addItem(str(p))
        self.mainpanel.right.accountlist.sortItems()
    
    def match(self):
        """Declare entries as matched
        """
        left = self.mainpanel.left.masterlist
        right = self.mainpanel.right.accountlist
        if ((len(left.selectedItems()) == 1) and
            (len(right.selectedItems()) == 1)):
            left.takeItem(left.currentRow())
            right.takeItem(right.currentRow()) 

class GUI(QtGui.QApplication):
    """Main Qt Application

    @author ykk
    @date Dec 2010
    """
    def __init__(self, argv):
        """Initailize
        """
        QtGui.QApplication.__init__(self,argv)

    def run(self):
        """Execute application
        """
        main = MainWindow()
        main.show()
        sys.exit(self.exec_())
