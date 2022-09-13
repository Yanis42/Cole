from xml.etree import ElementTree as ET
from PyQt6.QtWidgets import QComboBox, QLabel
from data import subElemTags, tagToWidget, shownWidgets
from .add_widgets import addLabel, addComboBox, addLineEdit, addCheckBox
from .getters import (
    getActorItemList,
    getActorIDFromName,
    getEvalParams,
    getListItems,
    getActorEnumParamValue,
    getWidgetFromName,
    getParamValue,
    getListValue,
)


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


def processActor(self, actorRoot: ET.Element):
    """Adds needed widgets to the UI's form"""
    global shownWidgets
    shownWidgets = []
    selectedItem = self.actorFoundBox.currentItem()
    if selectedItem is not None:
        actorID = getActorIDFromName(actorRoot, selectedItem.text())
        for actor in actorRoot:
            typeParam = getActorEnumParamValue(actor, self.actorTypeList.currentText(), actorID, "Type")
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
                            if widget is not None:
                                widget.setHidden(False)
                                shownWidgets.append((objName, label, widget, elem.get("Target", "Params")))

                                if label is None:
                                    self.paramLayout.addRow(widget, None)
                                else:
                                    label.setHidden(False)
                                    self.paramLayout.addRow(label, widget)
                break


def removeActor(currentItem, actorRoot: ET.Element):
    """Search for the selected actor then deletes it"""
    if currentItem is not None:
        actorName = currentItem.text()
        for actor in actorRoot:
            if actor.get("Name") == actorName:
                actorRoot.remove(actor)


def updateParameters(self, actorRoot: ET.Element):
    """Updates the parameters from the 4 line edits"""
    global shownWidgets
    listName = listValue = None
    targetList = ["Params", "XRot", "YRot", "ZRot"]
    selectedItem = self.actorFoundBox.currentItem()
    if selectedItem is not None:
        actorID = getActorIDFromName(actorRoot, selectedItem.text())

        # get the value of the chest content, collectible or message id combo box
        # bug if multiple lists in one actor?
        for (objName, label, widget, curTarget) in shownWidgets:
            if label is not None and isinstance(widget, QComboBox):
                if isinstance(label, QLabel):
                    label = label.text()
                if "Chest Content" in label:
                    listName = label
                elif "Collectible" in label:
                    listName = "Collectibles"
                elif "Message" in label:
                    listName = "Elf_Msg Message ID"
                listValue = getListValue(actorRoot, listName, widget) if listName is not None else "0x0"

        listValue = listValue if not listValue is None else "0x0"
        for actor in actorRoot:
            # for each displayed widgets, get the param value, format it, remove useless elements
            # then generate a string out of the list and set that to the correct line edit widget
            typeParam = (
                getActorEnumParamValue(actor, self.actorTypeList.currentText(), actorID, "Type")
                if self.actorTypeList.isEnabled()
                else "0000"
            )

            if actor.get("ID") == actorID:
                for target in targetList:
                    params = getParamValue(actor, target, listValue, shownWidgets)
                    paramValue = " | ".join(params) if len(params) > 0 else "0x0"

                    if target == "Params":
                        paramValue = (
                            f"(0x{typeParam} | ({paramValue}))"
                            if int(getEvalParams(f"0x{typeParam}"), base=16) > 0
                            else f"({paramValue})"
                        )
                        self.paramBox.setText(paramValue)
                    elif target == "XRot":
                        self.rotXBox.setText(paramValue)
                    elif target == "YRot":
                        self.rotYBox.setText(paramValue)
                    elif target == "ZRot":
                        self.rotZBox.setText(paramValue)
