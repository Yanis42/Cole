from PyQt6.QtGui import QGuiApplication


def copyToClipboard(paramValue: str):
    """Copies the param value in the system's clipboard"""
    if not paramValue == "":
        clipBoard = QGuiApplication.clipboard()
        clipBoard.clear(clipBoard.Mode.Clipboard)
        clipBoard.setText(paramValue, clipBoard.Mode.Clipboard)
