from PyQt6.QtWidgets import QLabel, QComboBox, QLineEdit, QCheckBox
from data import paramWidgets


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
