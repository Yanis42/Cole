from pathlib import Path
from PyQt6 import uic, QtWidgets
from PyQt6.QtWidgets import QFileDialog
from xml.etree import ElementTree as ET
from sys import exit, argv
from data import uiFile, actorRoot
from functions.actor import initActorTypeBox, processActor, initParamWidgets, removeActor
from functions.getters import getRoot, getActors, getCategories
from functions.general import clearParamLayout, resetUI, writeActorFile


class MainWindow(QtWidgets.QMainWindow):
    global actorRoot
    actorRoot = getRoot("res/actorList.xml")

    def __init__(self):
        """Main initialisation function"""
        super(MainWindow, self).__init__()
        uic.loadUi(uiFile, self)
        self.initConnections()
        self.initComponents()
        self.title = self.windowTitle()

    def initConnections(self):
        """Links the widgets to their callback function"""
        self.searchBox.textChanged.connect(self.searchBoxOnUpdate)
        self.actorCategoryList.currentTextChanged.connect(self.searchBoxOnUpdate)
        self.actorFoundBox.currentTextChanged.connect(self.foundBoxOnUpdate)
        self.actorTypeList.currentTextChanged.connect(self.typeBoxOnUpdate)
        self.ignoreTiedBox.stateChanged.connect(self.typeBoxOnUpdate)
        self.openActorFileBtn.clicked.connect(self.openActorFile)
        self.saveActorFileBtn.clicked.connect(self.saveActorFile)
        # self.addActorBtn.clicked.connect()
        self.deleteActorBtn.clicked.connect(self.deleteActor)

    def initComponents(self):
        """Initialise the UI widgets"""
        self.actorCategoryList.clear()
        self.actorCategoryList.addItems(getCategories(actorRoot))
        self.searchBoxOnUpdate()
        self.paramLayout.setHorizontalSpacing(50)
        self.ignoreTiedBox.setHidden(True)
        initParamWidgets(self, actorRoot)

    # connections callbacks

    def searchBoxOnUpdate(self):
        """Called everytime the search box is updated"""
        searchResults = getActors(actorRoot, self.searchBox.text(), self.actorCategoryList.currentText())
        self.actorFoundBox.clear()
        self.actorFoundBox.addItems(searchResults)
        self.actorFoundLabel.setText(f"Found: {len(searchResults)}")

    def foundBoxOnUpdate(self):
        """Called everytime a new actor is chosen"""
        initActorTypeBox(self, actorRoot)

    def typeBoxOnUpdate(self):
        """Called everytime the actor type is changed"""
        clearParamLayout(self)
        processActor(self, actorRoot)

    def openActorFile(self):
        """Called everytime the 'open file' button is clicked"""
        global actorRoot
        defaultDir = str(Path.home())
        path = QFileDialog.getOpenFileName(None, "Open Actor List XML File", defaultDir, "*.xml")[0]
        if len(path):
            actorRoot = ET.parse(path).getroot()
            resetUI(self)
            self.initComponents()

    def saveActorFile(self):
        """Called everytime the 'save file' button is clicked"""
        defaultDir = str(Path.home())
        path = QFileDialog.getSaveFileName(None, "Save File", defaultDir, "*.xml")[0]
        if len(path):
            writeActorFile(actorRoot, path)
            self.setWindowTitle(f"{self.title}")

    def deleteActor(self):
        """Called everytime the 'delete actor' button is clicked"""
        index = self.actorFoundBox.currentRow()
        removeActor(self, actorRoot)
        resetUI(self)
        self.initComponents()
        self.actorFoundBox.setCurrentRow(index)
        self.setWindowTitle(f"{self.title} (unsaved changes)")


# start the app
if __name__ == "__main__":
    app = QtWidgets.QApplication(argv)
    mainWindow = MainWindow()
    mainWindow.show()
    exit(app.exec())
