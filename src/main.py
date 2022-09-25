#!/usr/bin/env python3

from pathlib import Path
from PyQt6 import uic, QtWidgets
from PyQt6.QtWidgets import QFileDialog
from xml.etree import ElementTree as ET
from sys import exit, argv
from os import path, name as osName
from cole.getters import getRoot
from oot_actor.actor_getters import getActors
from oot_actor.actor_setters import setParamsText
from cole.general import copyToClipboard
from cole.data import paramPrefixList
from oot_actor.actor_init import initActorConnections, initActorComponents, initActorTypeBox, initParamBox
from oot_actor.actor import (
    processActor,
    removeActor,
    updateParameters,
    resetActorUI,
    writeActorFile,
    paramsToWidgets,
)


class MainWindow(QtWidgets.QMainWindow):
    actorRoot = getRoot(path.dirname(path.abspath(__file__)) + "/../res/actorList.xml")

    def __init__(self):
        """Main initialisation function"""
        super(MainWindow, self).__init__()
        uic.loadUi((path.dirname(path.abspath(__file__)) + "/../res/MainWindow.ui"), self)
        initActorConnections(self)
        initActorComponents(self)
        self.title = self.windowTitle()

        # taskbar icon trick for Windows
        if osName == "nt":
            from ctypes import windll

            # encoding probably useless but just in case
            windll.shell32.SetCurrentProcessExplicitAppUserModelID("cole.oot_mod_helper".encode("UTF-8"))

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
        initParamBox(self)
        processActor(self, self.actorRoot)
        self.paramOnUpdate()

    def typeBoxOnUpdate(self):
        """Called everytime the actor type is changed"""
        processActor(self, self.actorRoot)
        self.evalParamBox.setEnabled((False if self.ignoreTiedBox.isChecked() else True))
        self.paramOnUpdate()

    def openActorFile(self):
        """Called everytime the 'open file' button is clicked"""
        defaultDir = str(Path.home())
        path = QFileDialog.getOpenFileName(None, "Open Actor List XML File", defaultDir, "*.xml")[0]
        if len(path):
            self.actorRoot = ET.parse(path).getroot()
            resetActorUI(self)
            initActorComponents(self)

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
        initActorComponents(self)
        self.actorFoundBox.setCurrentRow(index)
        self.setWindowTitle(f"{self.title} (unsaved changes)")

    def paramOnUpdate(self):
        """Called everytime the parameters need to be updated"""
        updateParameters(self, self.actorRoot)
        if self.actorFoundBox.currentRow() >= 0 and self.evalParamBox.isChecked():
            setParamsText(self, None)

    def copyParam(self):
        """Called when the user clicks on a parameter 'label'"""
        for prefix in paramPrefixList:
            widget = getattr(self, f"{prefix}Box")
            if widget is not None and widget == self.sender():
                copyToClipboard(widget.text())

    def deleteAll(self):
        """Called when the user wants to delete every actors"""
        actor = self.actorRoot[0]
        if actor.tag == "Actor":
            self.actorRoot.remove(actor)
            self.deleteAll()
            return
        resetActorUI(self)
        initActorComponents(self)
        self.setWindowTitle(f"{self.title} (unsaved changes)")

    def setParams(self):
        """Called when the user updates one of the 4 parameter boxes"""
        try:
            paramsToWidgets(self)
            self.paramOnUpdate()
        except ValueError:
            # prevents errors made by the user
            pass


# start the app
if __name__ == "__main__":
    app = QtWidgets.QApplication(argv)
    mainWindow = MainWindow()
    mainWindow.show()
    exit(app.exec())
