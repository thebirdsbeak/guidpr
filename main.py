import sys
import csv
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QWidget
from designfiles import homeView


class MainDialog(QtWidgets.QMainWindow, homeView.Ui_MainWindow):

    # Variables

    # Setup 
    def __init__(self, parent=None):

        super(MainDialog, self).__init__(parent)
        self.setupUi(self)
        self.setupClauses()
        self.treeWidget.clicked.connect(self.selectClause)

    def listClauses(self):
        gdpr_list = []
        with open("gdpr.csv", "r") as gdpr_file:
            reader = csv.reader(gdpr_file)
            for i in reader:
                gdpr_list.append(i)
        return(gdpr_list)

    def printFullText(self):
        self.gdprBrowser.setHtml("Test string")

    def selectClause(self):
        gdpr_text = self.listClauses()
        search_text = self.treeWidget.currentItem().text(0)
        self.gdprBrowser.setText("")
        if search_text == "Full Text":
            self.printFullText()
        try:
            parent = self.treeWidget.currentItem().parent()
        except AttributeError:
            parent = False
        if not parent:
            for i in gdpr_text:
                if search_text.strip() == i[5].strip():
                    self.gdprBrowser.append(i[0].rstrip())
                    self.gdprBrowser.append("")
        else:
            try:
                second_parent = parent.parent()
            except AttributeError:
                second_parent = False
            if not second_parent:
                for i in gdpr_text:
                    if i[5] == parent.text(0) and i[3] == search_text.split(".")[1]:
                        self.gdprBrowser.append(i[0].rstrip())
                        self.gdprBrowser.append("")
            else:
                for i in gdpr_text:
                    if search_text == i[6]:
                        self. gdprBrowser.append(i[0].rstrip())
        self.gdprBrowser.verticalScrollBar().setValue(0)        

    def setupClauses(self):
        '''Loads in the GDPR tree widget contents'''
        # Load the gdpr in to a list
        gdpr_list = []
        sorted_list = []
        with open("gdpr.csv", "r") as gdpr_file:
            reader = csv.reader(gdpr_file)
            for i in reader:
                gdpr_list.append(i)

        full_text = QTreeWidgetItem(["Full Text"])        
        self.treeWidget.addTopLevelItem(full_text)

        # Grab and sort chapters (top level)
        chapters = list(set([i[5] for i in gdpr_list]))
        for x in chapters:
            y = x.split('.')
            sorted_list.append([int(y[0]), y[1]])
            
        sorted_chapters = sorted(sorted_list)
        for chapter in sorted_chapters:
            chapter_str = "{}.{}".format(str(chapter[0]), chapter[1])
            level = QTreeWidgetItem([chapter_str])
            self.treeWidget.addTopLevelItem(level)

            in_use = []
            for i in gdpr_list:
                if i[5].strip() == chapter_str.strip():
                    leveltwotext = i[2]
                    leveltwostr = "{}.{}".format(i[2], i[3])
                    if leveltwotext not in in_use:
                        newchild = QTreeWidgetItem([leveltwostr])
                        level.addChild(newchild)
                        in_use.append(leveltwotext)
                        for i in gdpr_list:
                            if i[2].strip() == leveltwotext:
                                levelthreetext = "{}".format(i[6])
                                thirdchild = QTreeWidgetItem([levelthreetext])
                                newchild.addChild(thirdchild)
                    
            self.treeWidget.addTopLevelItem(level)

        self.treeWidget.setColumnCount(1)
        self.treeWidget.setHeaderLabels(["Navigate"])


app = QtWidgets.QApplication(sys.argv)
form = MainDialog()
form.show()
app.exec_()
