from xml.etree import ElementTree as ET
from PyQt6.QtWidgets import QCheckBox, QLineEdit, QComboBox
from PyQt6.QtCore import Qt
from cole.data import OoTActorProperty, paramPrefixList
from .actor_getters import (
    getEvalParams,
    getShiftFromMask,
    getListObjName,
)


def setActorType(self, elem: ET.Element, paramType: str):
    """Sets the actor type value"""
    if elem.tag == "Type":
        for item in elem:
            if item.get("Params") == paramType:
                self.actorTypeList.setCurrentText(item.text)
                return


def setActorComboBox(itemList: list, widget, paramPart: str):
    """Sets a ComboBox value"""
    for item in itemList:
        if paramPart == item[2]:
            widget.setCurrentText(item[1])
            return


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


def setParamsText(self, text: str):
    """Sets text for every parameter box"""
    for prefix in paramPrefixList:
        widget = getattr(self, f"{prefix}Box")
        if widget is not None:
            widget.setText(getEvalParams(widget.text()) if text is None else text)
