from xml.etree import ElementTree as ET
from ast import parse, Expression, Num, UnaryOp, USub, Invert, BinOp
from cole.data import actorCatDebugToNormal, binOps, tagToWidget
from cole.getters import getShiftFromMask


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


def getActorEnumParamValue(actor: ET.Element, selectedType: str, actorID: str, elemTag: str):
    """Returns an actor's type list or enum param value"""
    if actor.get("ID") == actorID:
        for elem in actor:
            if elem.tag == elemTag:
                for item in elem:
                    identifier = item.text if (elemTag == "Type") else item.get("Name")
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


def getListValue(actorRoot: ET.Element, listName: str, widget):
    """Returns the value from a <List> node"""
    for list in actorRoot:
        if list.tag == "List" and list.get("Name") == listName:
            for item in list:
                if widget.currentText() == item.get("Name"):
                    return item.get("Value")
    return


def getEvalParams(params: str):
    """
    Evaluate the params string argument to an integer
    Raises ValueError if something goes wrong
    """

    if params is None or "None" in params:
        return "0x0"

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

    return f"0x{_eval(node.body):X}"


def getFormattedParams(mask: int, value: str, isBool: bool):
    """Returns the parameter with the correct format"""
    shift = getShiftFromMask(mask) if mask is not None else 0

    if not int(getEvalParams(value), base=16):
        return
    elif not isBool:
        if shift > 0:
            return f"(({value} << {shift}) & 0x{mask:04X})"
        else:
            return f"({value} & 0x{mask:04X})"
    else:
        return f"({value} << {shift})"


def getParamValue(actor: ET.Element, target: str, listValue: str, shownWidgets: list):
    """Returns a list of the parameters for a specific target for widgets which are displayed"""
    # this function should be called when we know for sure it's the right actor
    params = []
    name = None

    # iterates through the sub-elements of the actor
    for elem in actor:
        # we don't want <Type> and <Notes>
        if not (elem.tag == "Type") and not (elem.tag == "Notes"):
            # iterate through the displayed widgets
            for (objName, label, widget, curTarget) in shownWidgets:
                name = f"{actor.get('Key')}_{tagToWidget[elem.tag]}{elem.get('Index')}"
                enumParam = (
                    getActorEnumParamValue(actor, widget.currentText(), actor.get("ID"), "Enum")
                    if (objName == name) and "ComboBox" in objName
                    else "0x0"
                )

                # get the value for each widget on screen
                if (objName == name) and (elem.get("Target", "Params") == curTarget == target):
                    # get the param value of this widget then add it to the list
                    value = None
                    mask = int(elem.get("Mask", "0x0"), base=16)
                    if elem.tag == "ChestContent" or elem.tag == "Collectible" or elem.tag == "Message":
                        value = listValue
                    elif elem.tag == "Enum":
                        value = enumParam if enumParam is not None else "0x0"
                    elif (elem.tag == "Property") or (elem.tag == "Flag"):
                        value = widget.text()
                    elif elem.tag == "Bool":
                        value = "1" if widget.isChecked() else "0"

                    if not (value == "0" or value == "1"):
                        value = getFormattedParams(mask, value, False)
                    else:
                        value = getFormattedParams(mask, value, True)

                    if value is not None and not value in params:
                        params.append(value)
    return params
