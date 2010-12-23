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

        label = QtGui.QLabel("SQLite Account")
        self.combo = QtGui.QComboBox()

        grid = QtGui.QHBoxLayout()
        grid.addWidget(label)
        grid.addWidget(self.combo)
        self.setLayout(grid)

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
        
        self.combo = QtGui.QComboBox()
        self.combo.addItem("---Choose Account Type---")
        self.combo.addItem("QFX:CitiCard")
        self.combo.addItem("CSV:Chase")
        self.combo.addItem("CSV:CitiCard")
        self.filename = QtGui.QLineEdit()
        button = QtGui.QPushButton("Choose", self) 
        
        grid = QtGui.QHBoxLayout()
        grid.addWidget(self.combo)
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
        #acct = parser.getData("SQLite:MoneyDroid:"+\
        #                          str(self.filename.text()))
        #if (isinstance(acct, pyf.accounts)):
        #    self.acct.combo.clear()
        #    self.acct.combo.addItem("All")
        #    for (a,i) in acct.accounts.items():
        #        self.acct.combo.addItem(a)



class MainWindow(QtGui.QDialog):
    """Main window of GUI application
    """
    def __init__(self, parent=None):
        """Initialize
        """
        super(MainWindow,self).__init__(parent)
        QtGui.QMainWindow.__init__(self)
        self.resize(500,600)
        self.setWindowTitle("PyFinance")

        sqliteacct = SQLiteAcctChooser(self)
        sqlitechooser = SQLiteChooser(sqliteacct, self)
        acctchooser = AcctChooser(self)
        list=QtGui.QListView(self)
        quitbutton = QtGui.QPushButton("Quit", self) 
        
        grid = QtGui.QVBoxLayout()
        grid.addWidget(sqlitechooser)
        grid.addWidget(sqliteacct)
        grid.addWidget(acctchooser)
        grid.addWidget(list)
        grid.addWidget(quitbutton)
        self.setLayout(grid)

        self.connect(quitbutton, QtCore.SIGNAL("clicked()"), QtGui.qApp,
                     QtCore.SLOT('quit()'))

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
