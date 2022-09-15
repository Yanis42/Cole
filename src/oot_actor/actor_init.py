from xml.etree import ElementTree as ET
from cole.data import subElemTags, tagToWidget
from cole.getters import getCategories
from .actor_widgets import addComboBox, addLineEdit, addCheckBox
from .actor_getters import (
    getActorItemList,
    getActorIDFromName,
    getListItems,
)


def initActorConnections(self):
    """Initialises the actor callbacks"""
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


def initActorComponents(self):
    """Initialises the actor tab components"""
    self.actorCategoryList.clear()
    self.actorCategoryList.addItems(getCategories(self.actorRoot))
    self.searchBoxOnUpdate()
    self.paramLayout.setHorizontalSpacing(50)
    self.ignoreTiedBox.setHidden(True)
    initParamWidgets(self, self.actorRoot)


def initActorTypeBox(self):
    """Adds items to the type combo box"""
    selectedItem = self.actorFoundBox.currentItem()
    if selectedItem is not None:
        self.actorTypeList.clear()
        actorTypes = getActorItemList(self.actorRoot, getActorIDFromName(self.actorRoot, selectedItem.text()), "Type")
        if actorTypes is not None and (len(actorTypes) > 0):
            self.actorTypeList.addItems(actorTypes)
            self.actorTypeList.setEnabled(True)
        else:
            self.actorTypeList.setEnabled(False)


def initParamWidgets(self, actorRoot: ET.Element):
    """Creates necessary widgets for every parameter"""
    for actor in actorRoot:
        for elem in actor:
            items = None
            if elem.tag in subElemTags:
                widgetType = tagToWidget[elem.tag]
                objName = f"{actor.get('Key')}_{widgetType}{elem.get('Index')}"
                labelName = f"{objName}Label"
                labelText = elem.get("Name")

                if elem.tag == "Flag":
                    labelText = f"{elem.get('Type')} Flag"
                elif elem.tag in ["ChestContent", "Collectible", "Message"]:
                    if elem.tag == "ChestContent":
                        labelText = "Chest Content"
                    elif elem.tag == "Collectible":
                        labelText = "Collectibles"
                    elif elem.tag == "Message":
                        labelText = "Elf_Msg Message ID"
                    items = getListItems(actorRoot, labelText)

                if widgetType == "ComboBox":
                    if elem.tag == "Enum" and items is None:
                        items = [item.get("Name") for item in elem]
                    addComboBox(self, objName, labelName, labelText, items)
                elif widgetType == "LineEdit":
                    addLineEdit(self, objName, labelName, labelText)
                elif widgetType == "CheckBox":
                    addCheckBox(self, objName, labelText)
