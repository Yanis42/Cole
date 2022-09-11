from xml.etree import ElementTree as ET
from PyQt6.QtWidgets import QFileDialog, QLabel, QComboBox, QLineEdit, QCheckBox
from pathlib import Path
from data import actorCatDebugToNormal, subElemTags, tagToWidget


def getRoot(xmlFile: str):
    """Try to parse an XML file, opens an 'Open File Dialog' if file not found"""
    try:
        root = ET.parse(xmlFile).getroot()
    except FileNotFoundError:
        print(f"[COLE:ERROR]: File ``{xmlFile}`` not found!")
        defaultDir = str(Path.home())
        fname = QFileDialog.getOpenFileName(None, "Open Actor List XML File", defaultDir, "*.xml")
        root = ET.parse(fname[0]).getroot()

    return root


def findActors(actorRoot: ET.Element, searchInput: str, categoryInput: str):
    """Returns every actor that contains the value from ``searchInput`` and ``categoryInput``"""
    # using lowercase for every string
    searchInput = searchInput.lower()

    # search results list
    results = []

    # going through the XML data
    for actor in actorRoot:
        if actor is not None and actor.tag == "Actor":
            # search by ID, key, category and name
            actorID = actor.get("ID", "").lower()
            actorKey = actor.get("Key", "").lower()
            actorCategory = actor.get("Category")
            actorName = actor.get("Name", "")

            isInputInName = (
                searchInput in actorName.lower()
                or searchInput in actorKey
                or searchInput in actorID
                or (searchInput == "")
                or searchInput in actorID.replace("_", " ")
                or searchInput in actorKey.replace("_", " ")
            ) and (categoryInput in actorCatDebugToNormal[actorCategory] or (categoryInput == "All"))

            # add the actor if we have a match, else remove it,
            # check if the actor is already in the list for both case
            if isInputInName:
                if not actorName in results:
                    results.append(actorName)
            else:
                if actorName in results:
                    results.remove(actorName)
    return results


def findCategories(actorRoot: ET.Element):
    """Returns every categories"""
    results = ["All"]

    for actor in actorRoot:
        if actor is not None and actor.tag == "Actor":
            category = actorCatDebugToNormal[actor.get("Category")]
            if not category in results:
                results.append(category)

    return results


### [Component Manager] ###


def getActorIDFromName(actorRoot: ET.Element, actorName: str):
    """Returns an actor's ID from its name"""
    for actor in actorRoot:
        if actor.tag == "Actor" and actorName == actor.get("Name"):
            return actor.get("ID")
    return


def getActorItemList(actorRoot: ET.Element, actorID: str, listName: str):
    """Returns an actor's type list or enum node content"""
    return [
        item.text
        for actor in actorRoot
        if actorID == actor.get("ID")
        for elem in actor
        if elem.tag == listName
        for item in elem
    ]


def getActorEnumParamValue(actorRoot: ET.Element, selectedType: str, actorID: str, elemTag: str):
    """Returns an actor's type list or enum param value"""
    valueName = "Params" if elemTag == "Type" else "Value"
    for actor in actorRoot:
        if actor.get("ID") == actorID:
            for elem in actor:
                if elem.tag == elemTag:
                    for item in elem:
                        identifier = item.text if (elemTag == "Type") else elem.get("Name")
                        if selectedType == identifier:
                            return item.get("Params") if (elemTag == "Type") else item.get("Value")
    return


def getListItems(actorRoot: ET.Element, listName: str):
    """Returns a <List> node item list"""
    return [
        elem.get("Name") for list in actorRoot if list.tag == "List" and (list.get("Name") == listName) for elem in list
    ]


def addLabel(self, objName: str, text: str):
    """Creates and returns a new label widget"""
    label = QLabel(self.paramGroup)
    label.setObjectName(objName)
    label.setText(text)
    return label


def addComboBox(self, objName: str, labelName: str, text: str, items: list):
    """Creates a combo box widget and add it to the UI with the corresponding label name"""
    comboBox = QComboBox(self.paramGroup)
    comboBox.setObjectName(objName)
    comboBox.addItems(items)
    label = addLabel(self, labelName, text)
    self.paramLayout.addRow(label, comboBox)
    return comboBox


def addLineEdit(self, objName: str, labelName: str, text: str):
    """Creates a line edit widget and add it to the UI with the corresponding label name"""
    lineEdit = QLineEdit(self.paramGroup)
    lineEdit.setObjectName(objName)
    label = addLabel(self, labelName, text)
    self.paramLayout.addRow(label, lineEdit)
    return lineEdit


def addCheckBox(self, objName: str, text: str):
    """Creates a check box widget and add it to the UI with the corresponding label name"""
    checkBox = QCheckBox(self.paramGroup)
    checkBox.setObjectName(objName)
    checkBox.setText(text)
    self.paramLayout.addRow(checkBox, None)
    return checkBox


def clearParamLayout(self):
    """Removes every widget from the form on the UI"""
    while self.paramLayout.rowCount():
        self.paramLayout.removeRow(0)


### [Actor Processor] ###


def initActorTypeBox(self, actorRoot):
    """Adds items to the type combo box"""
    selectedItem = self.actorFoundBox.currentItem()
    if selectedItem is not None:
        self.actorTypeList.clear()
        actorTypes = getActorItemList(actorRoot, getActorIDFromName(actorRoot, selectedItem.text()), "Type")
        if actorTypes is not None and (len(actorTypes) > 0):
            self.actorTypeList.addItems(actorTypes)
            self.actorTypeList.setEnabled(True)
        else:
            self.actorTypeList.setEnabled(False)


def processActor(self, actorRoot: ET.Element):
    """Adds needed widgets to the UI's form"""
    items = None
    selectedItem = self.actorFoundBox.currentItem()
    if selectedItem is not None:
        typeParam = getActorEnumParamValue(
            actorRoot, self.actorTypeList.currentText(), getActorIDFromName(actorRoot, selectedItem.text()), "Type"
        )
        for actor in actorRoot:
            if actor.get("Name") == selectedItem.text():
                if len(actor) == 0:
                    label = addLabel(self, "noParamLabel", "This actor doesn't have parameters")
                    self.paramLayout.addRow(label, None)
                    break
                for elem in actor:
                    if elem.tag in subElemTags:
                        widgetType = tagToWidget[elem.tag]
                        objName = f"{actor.get('Key')}{widgetType}"
                        labelName = f"{objName}Label"
                        labelText = elem.get("Name")
                        tiedTypeList = elem.get("TiedActorTypes")

                        if tiedTypeList is None:
                            self.ignoreTiedBox.setHidden(True)
                        else:
                            self.ignoreTiedBox.setHidden(False)

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

                        if tiedTypeList is None or typeParam in tiedTypeList.split(",") or self.ignoreTiedBox.isChecked():
                            if widgetType == "ComboBox":
                                if items is None:
                                    items = [item.get("Name") for item in elem]
                                addComboBox(self, objName, labelName, labelText, items)
                            elif widgetType == "LineEdit":
                                addLineEdit(self, objName, labelName, labelText)
                            elif widgetType == "CheckBox":
                                addCheckBox(self, objName, labelText)
                break
