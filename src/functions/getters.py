from xml.etree import ElementTree as ET
from PyQt6.QtWidgets import QFileDialog
from pathlib import Path
from ast import parse, Expression, Num, UnaryOp, USub, Invert, BinOp
from data import actorCatDebugToNormal, paramWidgets, binOps


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
    for actor in actorRoot:
        if actor.get("ID") == actorID:
            for elem in actor:
                if elem.tag == elemTag:
                    for item in elem:
                        identifier = item.text if (elemTag == "Type") else elem.get("Name")
                        if selectedType == identifier:
                            if elemTag == "Type":
                                return item.get("Params")
                            else:
                                return item.get("Value")
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


def getShiftFromMask(mask):
    """Returns the shift value from the mask"""

    # get the shift by subtracting the length of the mask
    # converted in binary on 16 bits (since the mask can be on 16 bits) with
    # that length but with the rightmost zeros stripped
    return int(f"{len(f'{mask:016b}') - len(f'{mask:016b}'.rstrip('0'))}", base=10)


def getListValue(actorRoot: ET.Element, listName: str, widget):
    for list in actorRoot:
        if list.tag == "List" and list.get("Name") == listName:
            for item in list:
                if widget.currentText() == item.get("Name"):
                    return item.get("Value")
    return


def getEvalParams(params):
    """
    Evaluate the params string argument to an integer
    Raises ValueError if something goes wrong
    """

    # remove spaces
    params = params.strip()

    try:
        node = parse(params, mode="eval")
    except Exception as e:
        raise ValueError(f"Could not parse params {params} as an AST.") from e

    def _eval(node):
        if isinstance(node, Expression):
            return _eval(node.body)
        elif isinstance(node, Num):
            return node.n
        elif isinstance(node, UnaryOp):
            if isinstance(node.op, USub):
                return -_eval(node.operand)
            elif isinstance(node.op, Invert):
                return ~_eval(node.operand)
            else:
                raise ValueError(f"Unsupported unary operator {node.op}")
        elif isinstance(node, BinOp):
            return binOps[type(node.op)](_eval(node.left), _eval(node.right))
        else:
            raise ValueError(f"Unsupported AST node {node}")

    return f"0x{_eval(node.body):04X}"
