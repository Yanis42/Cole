from pathlib import Path
from PyQt6 import uic, QtWidgets
from PyQt6.QtWidgets import QFileDialog
from xml.etree import ElementTree as ET
from sys import exit, argv
from os import name as osName
from cole.data import uiFile
from cole.getters import getRoot
from oot_actor.actor_getters import getActors, getEvalParams
from cole.general import copyToClipboard
from oot_actor.actor_init import initActorConnections, initActorComponents, initActorTypeBox, initParamBox
from oot_actor.actor import (
    processActor,
    removeActor,
    updateParameters,
    clearParamLayout,
    resetActorUI,
    writeActorFile,
    paramsToWidgets,
)


class MainWindow(QtWidgets.QMainWindow):
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

            myappid = "cole.oot_mod_helper".encode("UTF-8")  # encoding probably useless but just in case
            windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    def initConnections(self):
        """Links the widgets to their callback function"""
        initActorConnections(self)

    def initComponents(self):
        """Initialise the UI widgets"""
        initActorComponents(self)

    # connections callbacks

    def searchBoxOnUpdate(self):
        """Called everytime the search box is updated"""
        searchResults = getActors(self.actorRoot, self.searchBox.text(), self.actorCategoryList.currentText())
        self.actorFoundBox.clear()
        self.actorFoundBox.addItems(searchResults)
        self.actorFoundLabel.setText(f"Found: {len(searchResults)}")

    def foundBoxOnUpdate(self):
        """Called everytime a new actor is chosen"""
        initActorTypeBox(self)
        processActor(self, self.actorRoot)
        self.paramOnUpdate()

    def typeBoxOnUpdate(self):
        """Called everytime the actor type is changed"""
        processActor(self, self.actorRoot)
        self.evalParamBox.setEnabled((False if self.ignoreTiedBox.isChecked() else True))
        initParamBox(self)

    def openActorFile(self):
        """Called everytime the 'open file' button is clicked"""
        defaultDir = str(Path.home())
        path = QFileDialog.getOpenFileName(None, "Open Actor List XML File", defaultDir, "*.xml")[0]
        if len(path):
            self.actorRoot = ET.parse(path).getroot()
            resetActorUI(self)
            self.initComponents()

    def saveActorFile(self):
        """Called everytime the 'save file' button is clicked"""
        defaultDir = str(Path.home())
        path = QFileDialog.getSaveFileName(None, "Save File", defaultDir, "*.xml")[0]
        if len(path):
            writeActorFile(self.actorRoot, path)
            self.setWindowTitle(f"{self.title}")

    def deleteActor(self):
        """Called everytime the 'delete actor' button is clicked"""
        index = self.actorFoundBox.currentRow()
        removeActor(self.actorFoundBox.currentItem(), self.actorRoot)
        resetActorUI(self)
        self.initComponents()
        self.actorFoundBox.setCurrentRow(index)
        self.setWindowTitle(f"{self.title} (unsaved changes)")

    def paramOnUpdate(self):
        """Called everytime a parameter widget is updated"""
        if self.actorFoundBox.currentRow() >= 0:
            self.evalOnUpdate()

    def evalOnUpdate(self):
        """Called everytime the eval checkbox is updated"""
        updateParameters(self, self.actorRoot)
        if self.evalParamBox.isChecked():
            if self.paramBox is not None:
                self.paramBox.setText(getEvalParams(self.paramBox.text()))
            if self.rotXBox is not None:
                self.rotXBox.setText(getEvalParams(self.rotXBox.text()))
            if self.rotYBox is not None:
                self.rotYBox.setText(getEvalParams(self.rotYBox.text()))
            if self.rotZBox is not None:
                self.rotZBox.setText(getEvalParams(self.rotZBox.text()))

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
        actor = self.actorRoot[0]
        if actor.tag == "Actor":
            self.actorRoot.remove(actor)
            self.deleteAll()
            return
        resetActorUI(self)
        self.initComponents()
        self.setWindowTitle(f"{self.title} (unsaved changes)")

    def setParams(self):
        """Called when the user updates one of the 4 parameter boxes"""
        try:
            paramsToWidgets(self)
            self.evalOnUpdate()
        except ValueError:
            # prevents errors made by the user
            pass


# start the app
if __name__ == "__main__":
    app = QtWidgets.QApplication(argv)
    mainWindow = MainWindow()
    mainWindow.show()
    exit(app.exec())
