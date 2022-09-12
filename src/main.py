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
    initParamWidgets,
)


class MainWindow(QtWidgets.QMainWindow):
    global actorRoot
    actorRoot = getRoot("res/actorList.xml")

    def __init__(self):
        """Main initialisation function"""
        super(MainWindow, self).__init__()
        uic.loadUi(uiFile, self)
        self.initConnections()
        self.initComponents()

    def initConnections(self):
        """Links the widgets to their callback function"""
        self.searchBox.textChanged.connect(self.searchBoxOnUpdate)
        self.actorCategoryList.currentTextChanged.connect(self.searchBoxOnUpdate)
        self.actorFoundBox.currentTextChanged.connect(self.foundBoxOnUpdate)
        self.actorTypeList.currentTextChanged.connect(self.typeBoxOnUpdate)
        self.ignoreTiedBox.stateChanged.connect(self.typeBoxOnUpdate)

    def initComponents(self):
        """Initialise the UI widgets"""
        self.actorCategoryList.clear()
        self.actorCategoryList.addItems(findCategories(actorRoot))
        self.searchBoxOnUpdate()
        self.paramLayout.setHorizontalSpacing(50)
        self.ignoreTiedBox.setHidden(True)
        initParamWidgets(self, actorRoot)

    # connections callbacks

    def searchBoxOnUpdate(self):
        """Called everytime the search box is updated"""
        searchResults = findActors(actorRoot, self.searchBox.text(), self.actorCategoryList.currentText())
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


# start the app
if __name__ == "__main__":
    app = QtWidgets.QApplication(argv)
    mainWindow = MainWindow()
    mainWindow.show()
    exit(app.exec())
