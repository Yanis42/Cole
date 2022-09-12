from xml.etree import ElementTree as ET
from xml.dom import minidom as MD
from PyQt6.QtWidgets import QFileDialog, QLabel, QComboBox, QLineEdit, QCheckBox, QFormLayout
from pathlib import Path
from data import actorCatDebugToNormal, subElemTags, tagToWidget, paramWidgets


def getRoot(xmlFile: str):
    """Try to parse an XML file, opens an 'Open File Dialog' if file not found"""
    try:
        root = ET.parse(xmlFile).getroot()
    except FileNotFoundError:
        print(f"[COLE:ERROR]: File ``{xmlFile}`` not found!")
        defaultDir = str(Path.home())
        fname = QFileDialog.getOpenFileName(None, "Open Actor List XML File", defaultDir, "*.xml")
        root = getRoot(fname[0])

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


def deleteWidgets(self):
    """Deletes every widget from the list"""
    global paramWidgets
    for elem in paramWidgets:
        for widget in elem:
            if widget is not None and not isinstance(widget, str):
                widget.deleteLater()
    if len(paramWidgets):
        paramWidgets = []


def resetUI(self):
    """Back to init state"""
    self.actorFoundBox.clear()
    self.actorCategoryList.clear()
    self.actorTypeList.clear()
    self.paramBox.setText("")
    self.rotXBox.setText("")
    self.rotYBox.setText("")
    self.rotZBox.setText("")
    self.actorFoundLabel.setText("Found: 0")
    self.ignoreTiedBox.setHidden(True)
    self.ignoreTiedBox.setChecked(False)
    deleteWidgets(self)


def writeActorFile(actorRoot: ET.Element, path: str):
    """Write the file to save to path"""
    xmlStr = MD.parseString(ET.tostring(actorRoot)).toprettyxml(indent="  ", encoding="UTF-8")
    xmlStr = b"\n".join([s for s in xmlStr.splitlines() if s.strip()])
    try:
        with open(path, "bw") as file:
            file.write(xmlStr)
    except:
        print("ERROR: The file can't be written. Update the permissions, this folder is probably read-only.")


def removeActor(self, actorRoot: ET.Element):
    actorName = self.actorFoundBox.currentItem()
    if actorName is not None:
        actorName = actorName.text()
        for actor in actorRoot:
            if actor.get("Name") == actorName:
                actorRoot.remove(actor)


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


def getWidgetFromName(objName: str):
    """Returns the label and the corresponding widget"""
    global paramWidgets
    for elem in paramWidgets:
        if objName in elem[0]:
            return elem[1], elem[2]


def addLabel(self, objName: str, text: str):
    """Creates and returns a new label widget"""
    label = QLabel(self.paramGroup)
    label.setObjectName(objName)
    label.setText(text)
    label.setHidden(True)
    return label


def addComboBox(self, objName: str, labelName: str, text: str, items: list):
    """Creates a combo box widget and add it to the UI with the corresponding label name"""
    comboBox = QComboBox(self.paramGroup)
    comboBox.setObjectName(objName)
    comboBox.addItems(items)
    label = addLabel(self, labelName, text)
    addWidgetToList(objName, label, comboBox)
    comboBox.setHidden(True)
    return comboBox


def addLineEdit(self, objName: str, labelName: str, text: str):
    """Creates a line edit widget and add it to the UI with the corresponding label name"""
    lineEdit = QLineEdit(self.paramGroup)
    lineEdit.setObjectName(objName)
    label = addLabel(self, labelName, text)
    addWidgetToList(objName, label, lineEdit)
    lineEdit.setHidden(True)
    return lineEdit


def addCheckBox(self, objName: str, text: str):
    """Creates a check box widget and add it to the UI with the corresponding label name"""
    checkBox = QCheckBox(self.paramGroup)
    checkBox.setObjectName(objName)
    checkBox.setText(text)
    addWidgetToList(objName, None, checkBox)
    checkBox.setHidden(True)
    return checkBox


def addWidgetToList(objName: str, label: QLabel, widget):
    global paramWidgets
    if len(paramWidgets) > 0:
        for elem in paramWidgets:
            if not (objName == elem[0]):
                paramWidgets.append((objName, label, widget))
                break
    else:
        paramWidgets.append((objName, label, widget))


def clearParamLayout(self):
    """Removes every widget from the form on the UI"""
    # get the widget of the current row, hide it, move on the next row
    # hide the other widget then remove the row (without deleting the widgets)
    while self.paramLayout.rowCount():
        label = self.paramLayout.itemAt(0, QFormLayout.ItemRole.LabelRole)
        widget = self.paramLayout.itemAt(0, QFormLayout.ItemRole.FieldRole)
        if label is not None:
            label.widget().setHidden(True)
        if widget is not None:
            widget.widget().setHidden(True)
        self.paramLayout.takeRow(0)


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


def initParamWidgets(self, actorRoot: ET.Element):
    """Creates necessary widgets for every parameter"""
    items = None
    for actor in actorRoot:
        for elem in actor:
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
                    if items is None:
                        items = [item.get("Name") for item in elem]
                    addComboBox(self, objName, labelName, labelText, items)
                elif widgetType == "LineEdit":
                    addLineEdit(self, objName, labelName, labelText)
                elif widgetType == "CheckBox":
                    addCheckBox(self, objName, labelText)


def processActor(self, actorRoot: ET.Element):
    """Adds needed widgets to the UI's form"""
    selectedItem = self.actorFoundBox.currentItem()
    if selectedItem is not None:
        typeParam = getActorEnumParamValue(
            actorRoot, self.actorTypeList.currentText(), getActorIDFromName(actorRoot, selectedItem.text()), "Type"
        )
        for actor in actorRoot:
            if actor.get("Name") == selectedItem.text():
                if len(actor) == 0:
                    label = addLabel(self, "noParamLabel", "This actor doesn't have parameters.")
                    label.setHidden(False)
                    self.paramLayout.addRow(label, None)
                    break
                for elem in actor:
                    if elem.tag in subElemTags:
                        widgetType = tagToWidget[elem.tag]
                        objName = f"{actor.get('Key')}_{widgetType}{elem.get('Index')}"
                        tiedTypeList = elem.get("TiedActorTypes")

                        if tiedTypeList is None:
                            self.ignoreTiedBox.setHidden(True)
                        else:
                            self.ignoreTiedBox.setHidden(False)

                        if (
                            tiedTypeList is None
                            or typeParam in tiedTypeList.split(",")
                            or self.ignoreTiedBox.isChecked()
                        ):
                            label, widget = getWidgetFromName(objName)
                            widget.setHidden(False)
                            if label is None:
                                self.paramLayout.addRow(widget, None)
                            else:
                                label.setHidden(False)
                                self.paramLayout.addRow(label, widget)
                break
