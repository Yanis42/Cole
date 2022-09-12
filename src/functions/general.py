from xml.etree import ElementTree as ET
from xml.dom import minidom as MD
from PyQt6.QtWidgets import QFormLayout
from data import paramWidgets


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
