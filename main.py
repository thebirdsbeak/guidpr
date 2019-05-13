import sys
import csv
import json
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QWidget
from designfiles import homeView

class MainDialog(QtWidgets.QMainWindow, homeView.Ui_MainWindow):

    # Variables
    with open("gdpr.json", "r") as gdpr_file:
        data = json.load(gdpr_file)

    # Setup 
    def __init__(self, parent=None):

        super(MainDialog, self).__init__(parent)
        self.setupUi(self)
        self.setupClauses()
        self.treeWidget.clicked.connect(self.selectClause)
        self.printFullText()

    def listClauses(self):
        gdpr_list = []
        with open("gdpr.csv", "r") as gdpr_file:
            reader = csv.reader(gdpr_file)
            for i in reader:
                gdpr_list.append(i)
        return(gdpr_list)

    def printFullText(self):
        used_chapters = []
        used_sections = []
        used_subtitles = []
        for i in self.data:
            if i['chapter'] not in used_chapters:
                self.gdprBrowser.append("Chapter: {}\n".format(i['chapter']))
                used_chapters.append(i['chapter'])
            elif i['section'] not in used_sections:
                self.gdprBrowser.append("Section: {}\n".format(i['section']))
                used_sections.append(i['section'])
            elif i['subtitle'] not in used_subtitles:
                self.gdprBrowser.append("Subtitle: {}\n".format(i['subtitle']))
                used_subtitles.append(i['subtitle'])
            if i['section'] == "Recitals":
                article_string = '{}\n'.format(i['text'].strip())
            else:
                article_string = '{}({}) {}\n'.format(i['article'], i['num'], i['text'].strip())
            self.gdprBrowser.append(article_string)
        self.gdprBrowser.verticalScrollBar().setValue(0)            

    def selectClause(self):
        gdpr_text = self.data
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
                if search_text.strip() == i['chapter'].strip():
                    print_string = "{}({}) {}".format(i['article'], i['num'], i['text'])
                    self.gdprBrowser.append(print_string.strip())
                    self.gdprBrowser.append("")
        else:
            try:
                second_parent = parent.parent()
            except AttributeError:
                second_parent = False
            if not second_parent:
                for i in gdpr_text:
                    if i['chapter'] == parent.text(0) and i['subtitle'] == search_text.split(".")[1]:
                        print_string = "{}({}) {}".format(i['article'], i['num'], i['text'])
                        self.gdprBrowser.append(print_string.strip())
                        self.gdprBrowser.append("")
            else:
                for i in gdpr_text:
                    levelthreetext = "{}({})".format(i['article'], i['num'])
                    if search_text == levelthreetext:
                        print_string = "{}({}) {}".format(i['article'], i['num'], i['text'])
                        self. gdprBrowser.append(print_string.strip())
        self.gdprBrowser.verticalScrollBar().setValue(0)        

    def setupClauses(self):
        '''Loads in the GDPR tree widget contents'''
        # Load the gdpr in to a list

        sorted_list = []

        full_text = QTreeWidgetItem(["Full Text"])        
        self.treeWidget.addTopLevelItem(full_text)

        # Grab and sort chapters (top level)
        chapters = list(set([i['chapter'] for i in self.data]))
        for x in chapters:
            y = x.split('.')
            sorted_list.append([int(y[0]), y[1]])
            
        sorted_chapters = sorted(sorted_list)
        for chapter in sorted_chapters:
            chapter_str = "{}.{}".format(str(chapter[0]), chapter[1])
            level = QTreeWidgetItem([chapter_str])
            self.treeWidget.addTopLevelItem(level)

            in_use = []
            for i in self.data:
                if i['chapter'] == chapter_str:
                    leveltwotext = i['article']
                    leveltwostr = "{}.{}".format(i['article'], i['subtitle'])
                    if leveltwotext not in in_use:
                        newchild = QTreeWidgetItem([leveltwostr])
                        level.addChild(newchild)
                        in_use.append(leveltwotext)
                        for i in self.data:
                            if i['article'] == leveltwotext:
                                levelthreetext = "{}({})".format(i['article'], i['num'])
                                thirdchild = QTreeWidgetItem([levelthreetext])
                                newchild.addChild(thirdchild)

            self.treeWidget.addTopLevelItem(level)

        self.treeWidget.setColumnCount(1)
        self.treeWidget.setHeaderLabels(["Navigate"])


app = QtWidgets.QApplication(sys.argv)
form = MainDialog()
form.show()
app.exec_()

