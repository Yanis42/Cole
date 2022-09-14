from pathlib import Path
from PyQt6 import uic, QtWidgets
from PyQt6.QtWidgets import QFileDialog
from xml.etree import ElementTree as ET
from sys import exit, argv
from os import name as osName
from data import uiFile, actorRoot
from functions.actor import initActorTypeBox, processActor, initParamWidgets, removeActor, updateParameters
from functions.getters import getRoot, getActors, getCategories, getEvalParams
from functions.general import clearParamLayout, resetUI, writeActorFile, copyToClipboard


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

        # taskbar icon trick for Windows
        if osName == "nt":
            from ctypes import windll
            myappid = u"cole.oot_mod_helper"
            windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

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
        self.evalParamBox.stateChanged.connect(self.evalOnUpdate)
        self.paramLabel.clicked.connect(self.copyParam)
        self.rotXLabel.clicked.connect(self.copyRotX)
        self.rotYLabel.clicked.connect(self.copyRotY)
        self.rotZLabel.clicked.connect(self.copyRotZ)
        self.deleteAllBtn.clicked.connect(self.deleteAll)

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
        self.paramBox.setText("0x0")
        self.rotXBox.setText("0x0")
        self.rotYBox.setText("0x0")
        self.rotZBox.setText("0x0")

    def typeBoxOnUpdate(self):
        """Called everytime the actor type is changed"""
        clearParamLayout(self)
        processActor(self, actorRoot)
        self.paramOnUpdate()

        enabled = False if self.ignoreTiedBox.isChecked() else True
        self.evalParamBox.setEnabled(enabled)
        self.paramBox.setEnabled(enabled)
        self.rotXBox.setEnabled(enabled)
        self.rotYBox.setEnabled(enabled)
        self.rotZBox.setEnabled(enabled)
        self.paramLabel.setEnabled(enabled)
        self.rotXLabel.setEnabled(enabled)
        self.rotYLabel.setEnabled(enabled)
        self.rotZLabel.setEnabled(enabled)

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
        removeActor(self.actorFoundBox.currentItem(), actorRoot)
        resetUI(self)
        self.initComponents()
        self.actorFoundBox.setCurrentRow(index)
        self.setWindowTitle(f"{self.title} (unsaved changes)")

    def paramOnUpdate(self):
        """Called everytime a parameter widget is updated"""
        updateParameters(self, actorRoot)
        if self.evalParamBox.isChecked():
            self.evalOnUpdate()

    def evalOnUpdate(self):
        """Called everytime the eval checkbox is updated"""
        if self.actorFoundBox.currentRow() >= 0:
            if self.evalParamBox.isChecked():
                if self.paramBox is not None:
                    self.paramBox.setText(getEvalParams(self.paramBox.text()))
                if self.rotXBox is not None:
                    self.rotXBox.setText(getEvalParams(self.rotXBox.text()))
                if self.rotYBox is not None:
                    self.rotYBox.setText(getEvalParams(self.rotYBox.text()))
                if self.rotZBox is not None:
                    self.rotZBox.setText(getEvalParams(self.rotZBox.text()))
            else:
                updateParameters(self, actorRoot)

    def copyParam(self):
        """Called when the user clicks on a parameter 'label'"""
        copyToClipboard(self.paramBox.text())

    def copyRotX(self):
        """Called when the user clicks on a parameter 'label'"""
        copyToClipboard(self.rotXBox.text())

    def copyRotY(self):
        """Called when the user clicks on a parameter 'label'"""
        copyToClipboard(self.rotYBox.text())

    def copyRotZ(self):
        """Called when the user clicks on a parameter 'label'"""
        copyToClipboard(self.rotZBox.text())

    def deleteAll(self):
        """Called when the user wants to delete every actors"""
        actor = actorRoot[0]
        if actor.tag == "Actor":
            actorRoot.remove(actor)
            self.deleteAll()
            return
        resetUI(self)
        self.initComponents()
        self.setWindowTitle(f"{self.title} (unsaved changes)")


# start the app
if __name__ == "__main__":
    app = QtWidgets.QApplication(argv)
    mainWindow = MainWindow()
    mainWindow.show()
    exit(app.exec())
