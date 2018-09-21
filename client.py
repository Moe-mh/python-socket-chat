
from PyQt4 import QtCore
from PyQt4 import QtGui

import socket
from PyQt4.QtNetwork import *



#########################################################33333
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def __init__(self, parent=None):
        super(Ui_MainWindow, self).__init__()


    
    def setupUi(self, MainWindow):
    
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.setFixedSize(800, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        
        
        self.log = QtGui.QPlainTextEdit(self.centralwidget)
        self.log.setGeometry(QtCore.QRect(40, 60, 681, 321))
        self.log.setObjectName(_fromUtf8("log"))
        self.log.setReadOnly (1)
        
        
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 30, 76, 19))
        self.label.setObjectName(_fromUtf8("label"))
        
        self.chat = QtGui.QPlainTextEdit(self.centralwidget)
        self.chat.setGeometry(QtCore.QRect(50, 430, 621, 101))
        self.chat.setObjectName(_fromUtf8("chat"))
        
        
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 400, 91, 19))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        

        self.button = QtGui.QPushButton(self.centralwidget)
        self.button.setGeometry(QtCore.QRect(680, 438, 110, 81))
        self.button.setObjectName(_fromUtf8("button"))
        ###############################################################
        
        self.thread=thread(self.log)
        self.thread.start()
        self.button.clicked.connect(self.func)



        ##############################################################
        MainWindow.setCentralWidget(self.centralwidget)

        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        

        
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


###################################################

    def func(self):

        m=self.chat.toPlainText()
        c.send(m.encode('utf-8'))
        if m:
            self.log.insertPlainText("you : "+m +" \n")
        self.chat.clear()
 



################################################
    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.label.setText(_translate("MainWindow", "Chat:", None))
        self.label_2.setText(_translate("MainWindow", "Type here:", None))
        self.button.setText(_translate("MainWindow", "send", None))

class thread(QtCore.QThread):
    def __init__(self,bo,  parent=None):
        super(thread, self).__init__(parent)
        self.bo=bo
    
    def run(self):
        while True:
            m=c.recv(4096)
            if m and m!='q':
                self.bo.insertPlainText(m.decode('utf-8')+'\n')




if __name__ == "__main__":
    host='localhost'
    port=1234
    BUFSIZ=4096
    ADDR=(host, port)
    c=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c.connect(ADDR)
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()

    ui.setupUi(MainWindow)
    MainWindow.show()

    sys.exit(app.exec_())

