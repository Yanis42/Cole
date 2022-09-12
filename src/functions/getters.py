from xml.etree import ElementTree as ET
from PyQt6.QtWidgets import QFileDialog
from pathlib import Path
from data import actorCatDebugToNormal, paramWidgets


def getRoot(xmlFile: str):
    """Try to parse an XML file, opens an 'Open File Dialog' if file not found"""
    try:
        root = ET.parse(xmlFile).getroot()
    except FileNotFoundError:
        print(f"[COLE:ERROR]: File ``{xmlFile}`` not found!")
        defaultDir = str(Path.home())
        fname = QFileDialog.getOpenFileName(None, "Open Actor List XML File", defaultDir, "*.xml")
        root = getRoot(fname[0])

    return root


def getActors(actorRoot: ET.Element, searchInput: str, categoryInput: str):
    """Returns every actor that contains the value from ``searchInput`` and ``categoryInput``"""
    # using lowercase for every string
    searchInput = searchInput.lower()

    # search results list
    results = []

    # going through the XML data
    for actor in actorRoot:
        if actor is not None and actor.tag == "Actor":
            # search by ID, key, category and name
            actorID = actor.get("ID", "").lower()
            actorKey = actor.get("Key", "").lower()
            actorCategory = actor.get("Category")
            actorName = actor.get("Name", "")

            isInputInName = (
                searchInput in actorName.lower()
                or searchInput in actorKey
                or searchInput in actorID
                or (searchInput == "")
                or searchInput in actorID.replace("_", " ")
                or searchInput in actorKey.replace("_", " ")
            ) and (categoryInput in actorCatDebugToNormal[actorCategory] or (categoryInput == "All"))

            # add the actor if we have a match, else remove it,
            # check if the actor is already in the list for both case
            if isInputInName:
                if not actorName in results:
                    results.append(actorName)
            else:
                if actorName in results:
                    results.remove(actorName)
    return results


def getCategories(actorRoot: ET.Element):
    """Returns every categories"""
    results = ["All"]

    for actor in actorRoot:
        if actor is not None and actor.tag == "Actor":
            category = actorCatDebugToNormal[actor.get("Category")]
            if not category in results:
                results.append(category)

    return results


def getActorIDFromName(actorRoot: ET.Element, actorName: str):
    """Returns an actor's ID from its name"""
    for actor in actorRoot:
        if actor.tag == "Actor" and actorName == actor.get("Name"):
            return actor.get("ID")
    return


def getActorItemList(actorRoot: ET.Element, actorID: str, listName: str):
    """Returns an actor's type list or enum node content"""
    return [
        item.text
        for actor in actorRoot
        if actorID == actor.get("ID")
        for elem in actor
        if elem.tag == listName
        for item in elem
    ]


def getActorEnumParamValue(actorRoot: ET.Element, selectedType: str, actorID: str, elemTag: str):
    """Returns an actor's type list or enum param value"""
    valueName = "Params" if elemTag == "Type" else "Value"
    for actor in actorRoot:
        if actor.get("ID") == actorID:
            for elem in actor:
                if elem.tag == elemTag:
                    for item in elem:
                        identifier = item.text if (elemTag == "Type") else elem.get("Name")
                        if selectedType == identifier:
                            return item.get("Params") if (elemTag == "Type") else item.get("Value")
    return


def getListItems(actorRoot: ET.Element, listName: str):
    """Returns a <List> node item list"""
    return [
        elem.get("Name") for list in actorRoot if list.tag == "List" and (list.get("Name") == listName) for elem in list
    ]


def getWidgetFromName(objName: str):
    """Returns the label and the corresponding widget"""
    global paramWidgets
    for elem in paramWidgets:
        if objName in elem[0]:
            return elem[1], elem[2]
