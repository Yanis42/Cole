from PyQt6.QtWidgets import QLabel, QComboBox, QLineEdit, QCheckBox
from PyQt6.QtCore import Qt


def stringProperty(self, objName: str = "strProp", name: str = "", default: str = "", hidden: bool = True):
    """Creates and returns a new LineEdit widget"""
    strProp = QLabel(self.paramGroup)
    strProp = QLineEdit(self.paramGroup)
    strProp.setObjectName(objName)
    strProp.setHidden(hidden)
    strProp.setText(default)
    strProp.editingFinished.connect(self.paramOnUpdate)
    label = addLabel(self, f"{objName}.label", name)
    return strProp, label


def enumProperty(self, objName: str = "enumProp", name: str = "", items: list = [], hidden: bool = True):
    """Creates and returns a new ComboBox widget"""
    itemList = [elem[1] for elem in items]
    enumProp = QComboBox(self.paramGroup)
    enumProp.setObjectName(objName)
    enumProp.addItems(itemList)
    enumProp.setHidden(hidden)
    enumProp.setCurrentIndex(0)
    enumProp.currentTextChanged.connect(self.paramOnUpdate)
    label = addLabel(self, f"{objName}.label", name)
    return enumProp, label


def boolProperty(self, objName: str = "boolProp", name: str = "", default: bool = False, hidden: bool = True):
    """Creates and returns a new CheckBox widget"""
    boolProp = QCheckBox(self.paramGroup)
    boolProp.setObjectName(objName)
    boolProp.setText(name)
    boolProp.setHidden(hidden)
    boolProp.setCheckState(Qt.CheckState.Checked if default else Qt.CheckState.Unchecked)
    boolProp.stateChanged.connect(self.paramOnUpdate)
    return boolProp


def addLabel(self, objName: str, text: str):
    """Creates and returns a new label widget"""
    label = QLabel(self.paramGroup)
    label.setObjectName(objName)
    label.setText(text)
    label.setHidden(True)
    return label
