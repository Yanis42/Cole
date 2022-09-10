from xml.etree import ElementTree as ET
from PyQt6.QtWidgets import QFileDialog, QLabel, QComboBox, QLineEdit, QCheckBox
from PyQt6.QtCore import QRect
from pathlib import Path
from data import actorCatDebugToNormal

def getRoot(xmlFile: str):
    try:
        root = ET.parse(xmlFile).getroot()
    except FileNotFoundError:
        print(f"[COLE:ERROR]: File ``{xmlFile}`` not found!")
        defaultDir = str(Path.home())
        fname = QFileDialog.getOpenFileName(None, "Open Actor List XML File", defaultDir, "*.xml")
        root = ET.parse(fname[0]).getroot()

    return root

def findActors(actorRoot: ET.Element, searchInput: str, categoryInput: str):
    searchInput = searchInput.lower()
    results = []

    for actor in actorRoot:
        if actor is not None and actor.tag == "Actor":
            actorID = actor.get("ID", "").lower()
            actorKey = actor.get("Key", "").lower()
            actorCategory = actor.get("Category")
            actorName = actor.get("Name", "")

            isInputInName = (
                (searchInput in actorName.lower() or searchInput in actorKey or
                searchInput in actorID or (searchInput == "") or
                searchInput in actorID.replace("_", " ") or searchInput in actorKey.replace("_", " "))
                and (categoryInput in actorCatDebugToNormal[actorCategory]
                or (categoryInput == "All"))
            )

            if isInputInName:
                if not actorName in results:
                    results.append(actorName)
            else:
                if actorName in results:
                    results.remove(actorName)
    return results

def findCategories(actorRoot: ET.Element):
    results = ["All"]

    for actor in actorRoot:
        if actor is not None and actor.tag == "Actor":
            category = actorCatDebugToNormal[actor.get("Category")]
            if not category in results:
                results.append(category)

    return results

# Component Manager

# Get/Set

def getActorIDFromType(actorRoot: ET.Element, actorType):
    for actor in actorRoot:
        if actor.tag == "Actor" and actorType == actor.get("Name"):
            return actor.get("ID")
    return

def getActorTypeList(actorRoot: ET.Element, actorID: str):
    return [
        item.text for actor in actorRoot
        if actorID == actor.get("ID") for elem in actor
        if elem.tag == "Type" for item in elem
    ]

def getActorType(selectedType: str, actorRoot: ET.Element):
    for actor in actorRoot:
        for elem in actor:
            if elem.tag == "Type":
                for item in elem:
                    if selectedType == item.text:
                        return actor.get("Params")
    return

def getList(actorRoot: ET.Element, listName: str):
    return [elem.get("Name") for list in actorRoot if list.tag == "List" and (list.get("Name") == listName) for elem in list]

# Components Processor

def addLabel(self, objName: str, text: str):
    label = QLabel(self.paramGroup)
    label.setObjectName(objName)
    label.setText(text)
    self.paramLabelLayout.addStretch()
    return label

def addComboBox(self, objName: str):
    comboBox = QComboBox(self.paramGroup)
    comboBox.setObjectName(objName)
    self.paramLayout.addStretch()
    return comboBox

# Actor Processor

def initActorTypeBox(self, actorRoot):
    selectedItem = self.actorFoundBox.currentItem()
    if selectedItem is not None:
        self.actorTypeList.clear()
        actorTypes = getActorTypeList(actorRoot, getActorIDFromType(actorRoot, selectedItem.text()))
        if actorTypes is not None and (len(actorTypes) > 0):
            self.actorTypeList.addItems(actorTypes)
            self.actorTypeList.setEnabled(True)
        else:
            self.actorTypeList.setEnabled(False)
