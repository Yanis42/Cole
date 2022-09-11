from sys import exit, argv
from PyQt6 import uic, QtWidgets
from data import uiFile, actorRoot
from functions import (
    getRoot,
    findActors,
    findCategories,
    initActorTypeBox,
    clearParamLayout,
    processActor,
)


class MainWindow(QtWidgets.QMainWindow):
    global actorRoot
    actorRoot = getRoot("res/actorList.xml")

    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi(uiFile, self)
        self.initConnections()
        self.initComponents()

    def initConnections(self):
        self.searchBox.textChanged.connect(self.searchBoxOnUpdate)
        self.actorCategoryList.currentTextChanged.connect(self.searchBoxOnUpdate)
        self.actorFoundBox.currentTextChanged.connect(self.foundBoxOnUpdate)

    def initComponents(self):
        self.actorCategoryList.clear()
        self.actorCategoryList.addItems(findCategories(actorRoot))
        self.searchBoxOnUpdate()
        self.paramLayout.setHorizontalSpacing(50)

    # connections callbacks

    def searchBoxOnUpdate(self):
        searchResults = findActors(actorRoot, self.searchBox.text(), self.actorCategoryList.currentText())
        self.actorFoundBox.clear()
        self.actorFoundBox.addItems(searchResults)
        self.actorFoundLabel.setText(f"Found: {len(searchResults)}")

    def foundBoxOnUpdate(self):
        clearParamLayout(self)
        initActorTypeBox(self, actorRoot)
        processActor(self, actorRoot)


if __name__ == "__main__":
    app = QtWidgets.QApplication(argv)
    mainWindow = MainWindow()
    mainWindow.show()
    exit(app.exec())
