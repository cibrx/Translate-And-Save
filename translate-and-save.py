from googletrans import Translator
import sqlite3
from translateForm import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QWidget, QListWidget, QVBoxLayout, QListWidgetItem, QTableWidgetItem
import sys
from PyQt5 import QtWidgets

class Translate(QtWidgets.QMainWindow):
    def __init__(self):
        super(Translate,self).__init__()
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.combo_destLang.addItem("tr")
        self.con = sqlite3.connect("tutorial.db")
        self.cursor=self.con.cursor()
        self.transApp = Translator()
        self.cursor.execute("select * from languages")
        defLanguage=self.cursor.fetchall()

        for i in defLanguage:
            self.ui.combo_destLang.addItem(i[0])

        result = self.con.execute("select * from words")
        self.wordList = result.fetchall()
        self.ui.combo_destLang.setCurrentText("tr")    
        self.ui.btn_Translation.clicked.connect(self.translate)
        self.ui.btn_deleteToWord.clicked.connect(self.Delete)    
        self.AddTable()

    def AddTable(self):
        self.ui.tableWidget.setColumnCount(2)
        self.ui.tableWidget.setHorizontalHeaderLabels(("word1","word2"))
        for word in self.wordList : 
            self.row_count = self.ui.tableWidget.rowCount()
            self.ui.tableWidget.insertRow(self.row_count)
            self.ui.tableWidget.setItem(self.row_count, 0, QTableWidgetItem(word[0]))
            self.ui.tableWidget.setItem(self.row_count, 1, QTableWidgetItem(word[1]))
            self.row_count+=1

    def translate(self):
        self.cText=self.ui.txt_current.text()
        destLang=self.ui.combo_destLang.currentText()
        transOutput = self.transApp.translate(self.cText, src='auto', dest=str(destLang))
        self.ui.txt_translated.setText(transOutput.text)
        self.cursor.execute("select * from words where tr='%s'"%(self.ui.txt_current.text()))

        if self.ui.check_addToBox.isChecked()==True and self.cursor.fetchall()==[]:
            self.cursor.execute("INSERT INTO words values('%s', '%s')"%(self.cText,self.ui.txt_translated.text()))
            self.con.commit()
    
    def Delete(self):
        self.cursor.execute("DELETE from words where tr='%s'"%(self.ui.txt_deleteToWord.text()))
        self.con.commit()

def App():
    app=QtWidgets.QApplication(sys.argv)
    win=Translate()
    win.show()
    sys.exit(app.exec_())

App()