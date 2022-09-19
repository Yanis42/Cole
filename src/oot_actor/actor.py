from xml.etree import ElementTree as ET
from xml.dom import minidom as MD
from PyQt6.QtWidgets import QFormLayout, QCheckBox
from cole.data import OoTActorProperty, subElemTags, objNameToTarget
from .actor_init import initOoTActorProperties
from .actor_widgets import addLabel
from .actor_setters import setActorType, setActorWidgets
from .actor_getters import (
    getActorIDFromName,
    getEvalParams,
    getActorTypeValue,
    getParamValue,
    getObjName,
    getTiedParams,
)


def processActor(self, actorRoot: ET.Element):
    """Adds needed widgets to the UI's form"""
    selectedItem = self.actorFoundBox.currentItem()
    if selectedItem is not None:
        label = addLabel(self, "noParamLabel", "This actor doesn't have parameters.")
        label.setFixedWidth(200)
        actorID = getActorIDFromName(actorRoot, selectedItem.text())
        for actor in actorRoot:
            typeParam = getActorTypeValue(self, actor, self.actorTypeList.currentText(), actorID)
            if actor.get("Name") == selectedItem.text():
                if len(actor) == 0:
                    label.setHidden(False)
                    self.paramLayout.addRow(label, None)
                    break
                label.deleteLater()
                for elem in actor:
                    if elem.tag in subElemTags:
                        tiedTypeList = elem.get("TiedActorTypes")
                        objName = getObjName(actor, elem)

                        if tiedTypeList is None:
                            self.ignoreTiedBox.setHidden(True)
                        else:
                            self.ignoreTiedBox.setHidden(False)

                        if (
                            objName is not None
                            and getTiedParams(tiedTypeList, typeParam)
                            or self.ignoreTiedBox.isChecked()
                        ):
                            label = OoTActorProperty.__annotations__[f"{objName}.label"]
                            widget = OoTActorProperty.__annotations__[objName]

                            if widget is not None:
                                widget.setHidden(False)
                                if isinstance(widget, QCheckBox):
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
    targetList = ["Params", "XRot", "YRot", "ZRot"]
    selectedItem = self.actorFoundBox.currentItem()
    if selectedItem is not None:
        actorID = getActorIDFromName(actorRoot, selectedItem.text())

        for actor in actorRoot:
            # for each displayed widgets, get the param value, format it, remove useless elements
            # then generate a string out of the list and set that to the correct line edit widget
            typeParam = getActorTypeValue(self, actor, self.actorTypeList.currentText(), actorID)

            if actor.get("ID") == actorID:
                for target in targetList:
                    params = getParamValue(self, actor, target)
                    paramValue = " | ".join(params) if len(params) > 0 else "0x0"

                    if target == "Params":
                        evalType = int(getEvalParams(f"0x{typeParam}"), base=16)
                        evalParamValue = int(getEvalParams(paramValue), base=16)
                        if evalType and evalParamValue:
                            paramValue = f"(0x{typeParam} | ({paramValue}))"
                        elif evalType and not evalParamValue:
                            paramValue = f"0x{typeParam}"
                        elif not evalType and evalParamValue:
                            paramValue = f"({paramValue})"
                        else:
                            paramValue = "0x0"
                        self.paramBox.setText(paramValue)
                    elif target == "XRot":
                        self.rotXBox.setText(paramValue)
                    elif target == "YRot":
                        self.rotYBox.setText(paramValue)
                    elif target == "ZRot":
                        self.rotZBox.setText(paramValue)


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


def writeActorFile(actorRoot: ET.Element, path: str):
    """Write the file to save to path"""
    xmlStr = MD.parseString(ET.tostring(actorRoot)).toprettyxml(indent="  ", encoding="UTF-8")
    xmlStr = b"\n".join([s for s in xmlStr.splitlines() if s.strip()])
    try:
        with open(path, "bw") as file:
            file.write(xmlStr)
    except:
        print("ERROR: The file can't be written. Update the permissions, this folder is probably read-only.")


def resetActorUI(self):
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
    OoTActorProperty.__annotations__.clear()
    initOoTActorProperties(self)


def paramsToWidgets(self):
    """Updates the widgets' values when a new parameter is set in the paramBox"""
    sender = self.sender()
    paramWidget = sender.text()
    selectecItem = self.actorFoundBox.currentItem()
    paramList = paramWidget.split(" | ")

    actorID = None
    if selectecItem is not None:
        actorID = getActorIDFromName(self.actorRoot, selectecItem.text())

    paramType = self.paramBox.text().split(" | ")[0]
    if not "<<" in paramType and not "&" in paramType:
        paramType = int(getEvalParams(paramType.lstrip("(").rstrip(")")), base=16)
    else:
        paramType = None

    for actor in self.actorRoot:
        if actorID is not None and actor.get("ID") == actorID:
            typeParam = getActorTypeValue(self, actor, self.actorTypeList.currentText(), actorID)
            for part in paramList:
                for elem in actor:
                    objName = getObjName(actor, elem)
                    tiedTypeList = elem.get("TiedActorTypes")
                    target = elem.get("Target", "Params")
                    tiedParams = getTiedParams(tiedTypeList, typeParam)

                    if elem.tag == "Type":
                        paramType &= int(elem.get("Mask", "0xFFFF"), base=16)
                        setActorType(self, elem, f"{paramType:04X}")
                    elif not elem.tag == "Notes" and (objNameToTarget[sender.objectName()] == target) and tiedParams:
                        setActorWidgets(actor, elem, int(getEvalParams(part), base=16), objName)
            break