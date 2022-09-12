from xml.etree import ElementTree as ET
from data import subElemTags, tagToWidget, shownWidgets
from .add_widgets import addLabel, addComboBox, addLineEdit, addCheckBox
from .getters import (
    getActorItemList,
    getActorIDFromName,
    getListItems,
    getActorEnumParamValue,
    getWidgetFromName,
    getShiftFromMask,
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
    global shownWidgets
    shownWidgets = []
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
                            if widget is not None:
                                widget.setHidden(False)
                                shownWidgets.append((objName, label, widget))

                                if label is None:
                                    self.paramLayout.addRow(widget, None)
                                else:
                                    label.setHidden(False)
                                    self.paramLayout.addRow(label, widget)
                break


def removeActor(self, actorRoot: ET.Element):
    """Search for the selected actor then deletes it"""
    actorName = self.actorFoundBox.currentItem()
    if actorName is not None:
        actorName = actorName.text()
        for actor in actorRoot:
            if actor.get("Name") == actorName:
                actorRoot.remove(actor)


def updateParameters(self, actorRoot: ET.Element):
    global shownWidgets
    selectedItem = self.actorFoundBox.currentItem()
    actorID = getActorIDFromName(actorRoot, selectedItem.text())
    listName = None
    name = None
    params = []
    rotX = []
    rotY = []
    rotZ = []

    typeParam = (
        getActorEnumParamValue(actorRoot, self.actorTypeList.currentText(), actorID, "Type")
        if self.actorTypeList.isEnabled()
        else "0x0000"
    )

    for (objName, label, widget) in shownWidgets:
        enumParam = (
            getActorEnumParamValue(actorRoot, widget.currentText(), actorID, "Enum")
            if "ComboBox" in objName
            else "0x0000"
        )

        label = label.text()
        if "Chest Content" in label:
            listName = label
        elif "Collectible" in label:
            listName = "Collectibles"
        elif "Message" in label:
            listName = "Elf_Msg Message ID"
        if listName is not None:
            listValue = getListValue(actorRoot, listName, widget)
        else:
            listValue = ""

        for actor in actorRoot:
            for elem in actor:
                if elem.tag in subElemTags:
                    name = f"{actor.get('Key')}_{tagToWidget[elem.tag]}{elem.get('Index')}"
                if name == objName:
                    value = None
                    target = elem.get("Target", "Params")
                    mask = int(elem.get("Mask", "0x0"), base=16)
                    shift = getShiftFromMask(mask) if mask is not None else 0

                    if elem.tag == "ChestContent" or elem.tag == "Collectible" or elem.tag == "Message":
                        if shift > 0:
                            value = f"(({listValue} << {shift}) & 0x{mask:04X})"
                        else:
                            value = f"({listValue} & 0x{mask:04X})"
                    elif elem.tag == "Enum":
                        if shift > 0:
                            value = f"(({typeParam} << {shift}) & 0x{mask:04X})"
                        else:
                            value = f"({typeParam} & 0x{mask:04X})"
                    elif (elem.tag == "Property") or (elem.tag == "Flag"):
                        if shift > 0:
                            value = f"(({widget.text()} << {shift}) & 0x{mask:04X})"
                        else:
                            value = f"({widget.text()} & 0x{mask:04X})"
                    elif elem.tag == "Bool":
                        if widget.isChecked():
                            value = f"(1 << {shift})"
                        else:
                            value = ""
                    if value is not None:
                        if (target == "Params") and not value in params:
                            params.append(value)
                        elif (target == "XRot") and not value in rotX:
                            rotX.append(value)
                        elif (target == "YRot") and not value in rotY:
                            rotY.append(value)
                        elif (target == "ZRot") and not value in rotZ:
                            rotZ.append(value)
    paramValue = " | ".join(params)
    rotXValue = " | ".join(rotX)
    rotYValue = " | ".join(rotY)
    rotZValue = " | ".join(rotZ)
    if paramValue == "":
        paramValue = "0x0"
    if rotXValue == "":
        rotXValue = "0x0"
    if rotYValue == "":
        rotYValue = "0x0"
    if rotZValue == "":
        rotZValue = "0x0"
    self.paramBox.setText(f"0x{typeParam} | ({paramValue})")
    self.rotXBox.setText(rotXValue)
    self.rotYBox.setText(rotYValue)
    self.rotZBox.setText(rotZValue)
