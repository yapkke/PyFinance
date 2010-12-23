"""This module create the GUI
"""
import sys
import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore

class MainWindow(QtGui.QDialog):
    """Main window of GUI application
    """
    def __init__(self, parent=None):
        """Initialize
        """
        super(MainWindow,self).__init__(parent)
        QtGui.QMainWindow.__init__(self)
        self.resize(250,150)
        self.setWindowTitle("PyFinance")

        quitbutton = QtGui.QPushButton("Quit", self) 
        
        grid = QtGui.QVBoxLayout()
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
