from xml.etree import ElementTree as ET
from PyQt6.QtWidgets import QCheckBox, QLineEdit, QComboBox
from PyQt6.QtCore import Qt
from cole.data import OoTActorProperty
from .actor_getters import (
    getEvalParams,
    getShiftFromMask,
    getListObjName,
)


def setActorType(self, elem: ET.Element, paramType: str):
    """Sets the actor type value"""
    curText = None
    if paramType is not None:
        if elem.tag == "Type":
            for item in elem:
                if item.get("Params") == paramType:
                    curText = item.text
                    break
        if curText is not None:
            self.actorTypeList.setCurrentText(curText)


def setActorComboBox(itemList: list, widget, paramPart: str):
    """Sets a ComboBox value"""
    curText = None
    for item in itemList:
        if paramPart == item[2]:
            curText = item[1]
            break
    if curText is not None:
        widget.setCurrentText(curText)


def setActorWidgets(actor: ET.Element, elem: ET.Element, params: int, objName: str):
    """Sets the widgets' values"""
    mask = int(elem.get("Mask", "0xFFFF"), base=16)
    shift = getShiftFromMask(mask)
    paramPart = f"0x{((params & mask) >> shift):02X}"
    evaledPart = int(getEvalParams(paramPart), base=16)

    widget = OoTActorProperty.__annotations__[objName]
    if widget is not None:
        if isinstance(widget, QLineEdit):
            widget.setText(paramPart)
        elif isinstance(widget, QCheckBox):
            state = Qt.CheckState.Checked if evaledPart else Qt.CheckState.Unchecked
            widget.setCheckState(state)
        elif isinstance(widget, QComboBox):
            itemName = getListObjName(elem, elem.tag, actor.get("Key"), elem.get("Index", "1"))
            if itemName is not None:
                itemList = OoTActorProperty.__annotations__[itemName]
                setActorComboBox(itemList, widget, paramPart)
