from xml.etree import ElementTree as ET
from data import subElemTags, tagToWidget
from .add_widgets import addLabel, addComboBox, addLineEdit, addCheckBox
from .getters import getActorItemList, getActorIDFromName, getListItems, getActorEnumParamValue, getWidgetFromName


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


def removeActor(self, actorRoot: ET.Element):
    """Search for the selected actor then deletes it"""
    actorName = self.actorFoundBox.currentItem()
    if actorName is not None:
        actorName = actorName.text()
        for actor in actorRoot:
            if actor.get("Name") == actorName:
                actorRoot.remove(actor)
